"""C257 authoring tests use explicit synthetic lookup models, not capability evidence."""
import ast
from collections import defaultdict
import contextlib
import copy
import hashlib
import io
import itertools
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
import torch
from torch import nn
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c257_unseen_fact_order as b


def fixture():
    train = {(0,1,2),(0,1,3),(0,2,1),(1,0,2),(1,0,3),(1,3,0),(2,0,3),(2,3,0),(2,3,1),(3,1,2),(3,2,0),(3,2,1)}
    result = {s: [] for s in b.SPLITS}
    for assignment in itertools.permutations(range(4), 3):
        split = "TRAIN" if assignment in train else "HOLDOUT"
        for lang, names in (("en", ("a","b","c")), ("ja", ("甲","乙","丙"))):
            for order in (0, 1):
                for query in (0, 1, 2):
                    sequence = (0,1,2) if order == 0 else (2,1,0)
                    result[split].append(dict(id=f"{lang}-{assignment[0]}{assignment[1]}{assignment[2]}-{order}-{query}",
                        assignment=list(assignment), language=lang, order=order, query=query, target=48+assignment[query],
                        prompt=";".join(names[k]+"="+str(assignment[k]) for k in sequence)+";"+names[query]+"="))
    return result


class Factory:
    @staticmethod
    def prefix_tensor(raw):
        return torch.tensor([257, *raw, 258, *([256]*(46-len(raw)))], dtype=torch.int64)
    @staticmethod
    def new_model(seed):
        return seed  # Only a construction token for the explicitly synthetic parent adapter.


class LookupFixture(nn.Module):
    """A test oracle with known outputs and checkpointable weights; NOT a learned model."""
    def __init__(self, seed, arm):
        super().__init__()
        self.marker = nn.Parameter(torch.zeros(14256, dtype=torch.float64))
        with torch.no_grad():
            self.marker[-1] = seed / 1e9
        self.arm = arm; self.answers = {}
        parts = fixture(); novel = b.novel_dataset(parts)
        for split in b.SPLITS:
            for row in parts[split] + novel[split]:
                self.answers[row["prompt"].encode()] = row["target"]
        self.eval().requires_grad_(False)
    def forward(self, tokens, tasks):
        value = torch.full((len(tokens), 256), -10., dtype=torch.float64)
        for i, row in enumerate(tokens):
            raw = bytes(x for x in row.tolist() if x < 256)
            target = self.answers.get(raw, 48)
            if b"?" not in raw and self.arm == b.ARMS[1]:
                target = 48 + (target-48+1) % 4
            value[i, target] = 10.
        return value + self.marker[-1] * 0


class Parent:
    @staticmethod
    def fingerprint(model):
        digest = hashlib.sha256()
        for name, value in sorted(model.state_dict().items()):
            digest.update(name.encode()); digest.update(value.detach().cpu().numpy().tobytes())
        return digest.hexdigest()
    @staticmethod
    def render(row, view):
        names = {"en":("a","b","c"),"ja":("甲","乙","丙")}[row["language"]]
        seq = (0,1,2) if row["order"] == 0 else (2,1,0)
        return ";".join(names[k]+"="+("?" if view=="evidence_blind" else str(row["assignment"][k])) for k in seq)+";"+("?" if view=="query_blind" else names[row["query"]])+"="
    @staticmethod
    def metrics(rows, outputs):
        predictions = {v: x.argmax(-1).tolist() for v, x in outputs.items()}
        loss = F.cross_entropy(outputs["normal"], torch.tensor([r["target"] for r in rows]), reduction="none")
        metrics = {}
        for lang in ("en","ja"):
            ids = [i for i, r in enumerate(rows) if r["language"]==lang]
            acc = {v: sum(p[i]==rows[i]["target"] for i in ids)/72 for v,p in predictions.items()}
            orders, queries = defaultdict(list), defaultdict(list)
            for i in ids:
                r = rows[i]; orders[(tuple(r["assignment"]),r["query"])].append(i); queries[(tuple(r["assignment"]),r["order"])].append(i)
            metrics[lang] = dict(rows=72, accuracy=acc["normal"], answer_nll=float(loss[ids].mean()),
                evidence_blind_accuracy=acc["evidence_blind"], query_blind_accuracy=acc["query_blind"],
                evidence_drop=acc["normal"]-acc["evidence_blind"], query_drop=acc["normal"]-acc["query_blind"],
                order_pair_accuracy=sum(all(predictions["normal"][i]==rows[i]["target"] for i in g) for g in orders.values())/36,
                query_triplet_accuracy=sum(all(predictions["normal"][i]==rows[i]["target"] for i in g) for g in queries.values())/24)
        return metrics, predictions
    @staticmethod
    def metric_error(left, right):
        return max(abs(left[s][l][k]-right[s][l][k]) for s in b.SPLITS for l in ("en","ja") for k in left[s][l])
    @staticmethod
    def cell_pass(cell):
        return b.new_cell_pass(cell) and cell["order_pair_accuracy"]>=.8
    @staticmethod
    def evaluate(model, parts, factory):
        raw, metrics, predictions = {}, {}, {}
        with torch.no_grad():
            for split in b.SPLITS:
                raw[split] = {}
                for view in b.VIEWS:
                    tokens = torch.stack([factory.prefix_tensor(Parent.render(r,view).encode()) for r in parts[split]])
                    raw[split][view] = model(tokens, torch.zeros(len(tokens),dtype=torch.int64))
                metrics[split], predictions[split] = Parent.metrics(parts[split],raw[split])
        return metrics, predictions, raw
    @staticmethod
    def make_model(backbone, arm, seed, c252, reader):
        return LookupFixture(seed,arm)
    @staticmethod
    def dataset():
        return fixture()


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("synthetic-input-"): return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):
        path = (Path(root)/name).resolve()
        if path.parent!=Path(root).resolve(): raise ValueError("unsafe path")
        return path
    @staticmethod
    def git(root,*args):
        if args==("rev-parse","HEAD"): return b"synthetic-head"
        if args==("branch","--show-current"): return b"feat/sft-target-loss"
        return b""


def protection():
    pins = {f"old-{i}":"fixture" for i in range(382)}; pins.update({n:"fixture" for n in b.OWN})
    return pins, {f"synthetic-input-{i}":"0"*64 for i in range(635)}


class C257Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2); cls.parts = fixture(); cls.new = b.novel_dataset(cls.parts)
        cls.refs=[]; cls.records=[]; cls.models=[]
        for seed,arm in b.identities():
            model=LookupFixture(seed,arm); final,pred,_=Parent.evaluate(model,cls.parts,Factory)
            ref=dict(seed=seed,arm=arm,final_sha256=Parent.fingerprint(model),final=final,predictions=pred)
            cls.models.append(model); cls.refs.append(ref)
            cls.records.append(b.probe_one(model,cls.parts,cls.new,ref,Parent,Factory))

    def test_01_fixed_hash_and_registration_rejection(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),b.PARENT_ARTIFACTS["dataset.json"])
        self.assertEqual(b.digest(self.new),b.ORDER_SHA)
        with contextlib.redirect_stdout(io.StringIO()):
            b.validate_registration(388,635)
            with self.assertRaisesRegex(ValueError,"source/input counts"): b.validate_registration(387,635)
            with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaisesRegex(ValueError,"manifest hash"): b.validate_registration(388,635)

    def test_02_original_orders_render_identically(self):
        for rows in self.parts.values():
            for row in rows:
                converted=dict(row,permutation=list(b.KNOWN[row["order"]]))
                for view in b.VIEWS:self.assertEqual(b.render(converted,view),Parent.render(row,view))

    def test_03_new_rows_keep_assignment_query_and_target(self):
        for split,rows in self.new.items():
            old={r["id"]:r for r in self.parts[split]}; self.assertEqual(len(rows),288)
            for row in rows:
                source=old[row["source_id"]]
                for key in ("assignment","query","target","language"):self.assertEqual(row[key],source[key])
                self.assertEqual(row["prompt"],b.render(row,"normal"))
                self.assertLessEqual(len(row["prompt"].encode()),46)

    def test_04_all_positions_and_six_permutations(self):
        self.assertEqual(set(b.KNOWN+b.NOVEL),set(itertools.permutations(range(3))))
        self.assertTrue(set(b.KNOWN).isdisjoint(b.NOVEL))
        self.assertEqual({p.index(1) for p in b.KNOWN},{1})
        self.assertEqual({p.index(1) for p in b.NOVEL},{0,2})

    def test_05_changed_original_or_order_hash_rejected(self):
        bad=copy.deepcopy(self.parts);bad["TRAIN"][0]["target"]=51
        with self.assertRaises(ValueError):b.novel_dataset(bad)
        with patch.object(b,"ORDER_SHA","0"*64),self.assertRaisesRegex(ValueError,"new dataset hash"):b.novel_dataset(self.parts)

    def test_06_new_metrics_perfect_model(self):
        cells,pred=b.new_metrics(self.new["HOLDOUT"],self.records[0]["outputs"]["novel"]["HOLDOUT"])
        self.assertEqual(len(cells),8);self.assertTrue(all(b.new_cell_pass(c) for c in cells))
        self.assertTrue(all(c["rows"]==36 and c["correct"]==36 and c["query_triplet_accuracy"]==1 for c in cells))
        self.assertEqual(len(pred["normal"]),288)

    def test_07_one_new_order_cannot_hide_in_average(self):
        records=copy.deepcopy(self.records);rows=self.new["HOLDOUT"]
        ids=[i for i,r in enumerate(rows) if r["language"]=="en" and tuple(r["permutation"])==b.NOVEL[0]][:4]
        logits=records[0]["outputs"]["novel"]["HOLDOUT"]["normal"]
        logits[ids]=-10.;logits[ids,200]=10.
        measurements,summary=b.analyze(self.parts,self.new,records,self.refs,Parent)
        self.assertFalse(summary["candidate_gate"]);self.assertEqual(summary["seed_pass_counts"][b.ARMS[0]],4)
        self.assertEqual(measurements[0]["outcome"],"NEW_ORDER_MISS")

    def test_08_six_order_group_denominator_and_missing_pair(self):
        ref=self.refs[0];pred=self.records[0]["outputs"]["novel"]["TRAIN"]["normal"].argmax(-1).tolist()
        score=b.six_order_metrics(self.parts["TRAIN"],self.new["TRAIN"],ref["predictions"]["TRAIN"]["normal"],pred)
        self.assertEqual(score,{l:dict(groups=36,all_six_correct=36,accuracy=1.) for l in ("en","ja")})
        malformed=copy.deepcopy(self.new["TRAIN"]);malformed[0]["permutation"]=malformed[1]["permutation"]
        with self.assertRaises(ValueError):b.six_order_metrics(self.parts["TRAIN"],malformed,ref["predictions"]["TRAIN"]["normal"],pred)

    def test_09_every_new_cell_threshold_is_required(self):
        cell=b.new_metrics(self.new["TRAIN"],self.records[0]["outputs"]["novel"]["TRAIN"])[0][0]
        for key,val in (("accuracy",.89),("query_triplet_accuracy",.79),("evidence_drop",.34),("query_drop",.34)):
            self.assertFalse(b.new_cell_pass(dict(cell,**{key:val})))

    def test_10_replay_tolerance_and_exact_argmax(self):
        x=torch.zeros(2,256,dtype=torch.float64);x[:,0]=1.
        self.assertLessEqual(b.replay(x,x+5e-10),b.TOL)
        with self.assertRaises(ValueError):b.replay(x,x+2e-9)
        tied=torch.zeros_like(x);other=tied.clone();other[:,1]=5e-10
        with self.assertRaises(ValueError):b.replay(tied,other)
        with self.assertRaises(ValueError):b.replay(x*float("nan"),x)

    def test_11_original_replay_barrier_before_new_inputs(self):
        ref=copy.deepcopy(self.refs[0]);ref["predictions"]["TRAIN"]["normal"][0]=200
        with patch.object(b,"evaluate_new") as scoring,self.assertRaisesRegex(ValueError,"original C256"):
            b.probe_one(self.models[0],self.parts,self.new,ref,Parent,Factory)
        scoring.assert_not_called();self.assertFalse(self.models[0]._forward_hooks)

    def test_12_actual_probe_counts_restore_and_no_weights_changed(self):
        before=Parent.fingerprint(self.models[0]);record=b.probe_one(self.models[0],self.parts,self.new,self.refs[0],Parent,Factory)
        self.assertEqual((record["forward_calls"],record["row_presentations"]),(18,3456))
        self.assertEqual(before,Parent.fingerprint(self.models[0]));self.assertEqual(record["restore_error"],0.)

    def test_13_freeze_and_state_mutation_guards(self):
        model=copy.deepcopy(self.models[0]).train()
        with self.assertRaises(ValueError):b.probe_one(model,self.parts,self.new,self.refs[0],Parent,Factory)
        model.eval().requires_grad_(True)
        with self.assertRaises(ValueError):b.probe_one(model,self.parts,self.new,self.refs[0],Parent,Factory)
        model.requires_grad_(False)
        def mutate(module,args,output):
            with torch.no_grad():module.marker[0].add_(1.)
        handle=model.register_forward_hook(mutate)
        try:
            with self.assertRaisesRegex(ValueError,"mutation"):b.probe_one(model,self.parts,self.new,self.refs[0],Parent,Factory)
        finally:handle.remove()
        self.assertFalse(model._forward_hooks)

    def test_14_archive_integrity_and_restored_corruption(self):
        for key,value in (("forward_calls",17),("weights_preserved",False),("restore_error",float("nan"))):
            records=copy.deepcopy(self.records);records[0][key]=value
            with self.assertRaises(ValueError):b.analyze(self.parts,self.new,records,self.refs,Parent)
        with self.assertRaises(ValueError):b.analyze(self.parts,self.new,list(reversed(self.records)),self.refs,Parent)
        records=copy.deepcopy(self.records);records[0]["outputs"]["restored"]["TRAIN"]["normal"]+=.1
        with self.assertRaises(ValueError):b.analyze(self.parts,self.new,records,self.refs,Parent)

    def test_15_frozen_model_strict_load_and_capacity(self):
        state=self.models[0].state_dict()
        model=b.frozen_model(self.refs[0],state,Parent,None,None,Factory)
        self.assertEqual(Parent.fingerprint(model),self.refs[0]["final_sha256"])
        self.assertFalse(any(p.requires_grad for p in model.parameters()))
        with self.assertRaises(RuntimeError):b.frozen_model(self.refs[0],{},Parent,None,None,Factory)
        with self.assertRaises(ValueError):b.frozen_model(dict(self.refs[0],final_sha256="wrong"),state,Parent,None,None,Factory)

    def test_16_main_path_has_no_optimizer_or_training(self):
        source=Path(b.__file__).read_text(encoding="utf-8")
        for node in ast.walk(ast.parse(source)):
            if isinstance(node,ast.Call):
                name=node.func.id if isinstance(node.func,ast.Name) else node.func.attr if isinstance(node.func,ast.Attribute) else ""
                self.assertNotIn(name,{"fit","train_one","backward","AdamW","step"})

    def test_17_actual_run_and_saved_postcheck(self):
        parent=SimpleNamespace(**{name:getattr(Parent,name) for name in ("fingerprint","evaluate","make_model","metrics","metric_error","cell_pass")},
                               load_bundle=Mock(return_value=[m.state_dict() for m in self.models]))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,None,None,Factory,Audit)), \
             patch.object(b,"precheck",return_value=protection()) as pre,patch.object(b,"load_inputs",return_value=(self.parts,self.refs)) as loader:
            root=Path(d);out=root/"out"
            with contextlib.redirect_stdout(io.StringIO()):result=b.run(c256_summary=root/"summary.json",output_dir=out,expected_head="synthetic-head")
            loader.assert_called_once();parent.load_bundle.assert_called_once();self.assertEqual(pre.call_count,2)
            with patch.object(b,"probe_one",side_effect=AssertionError("postcheck must not score")):
                self.assertEqual(b.verify_artifacts(out,root/"summary.json","synthetic-head")[0],result)
            self.assertEqual(result["validation_summary"]["seed_pass_counts"],{b.ARMS[0]:5,b.ARMS[1]:0})
            with self.assertRaisesRegex(ValueError,"saved HEAD"):
                b.verify_artifacts(out,root/"summary.json","wrong-head")
            (out/"measurements.json").write_text("[]",encoding="utf-8")
            with self.assertRaises(ValueError):b.verify_artifacts(out,root/"summary.json","synthetic-head")

    def test_18_loader_calls_actual_parent_interface(self):
        payload={"status":"PASS","validation_summary":{"seed_pass_counts":{b.ARMS[0]:5,b.ARMS[1]:0}}}
        parent=SimpleNamespace(verify_artifacts=Mock(return_value=(payload,self.refs)),dataset=fixture)
        audit=SimpleNamespace(sha=lambda p:b.PARENT_SHA,read_json=Audit.read_json)
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,None,None,None,audit)):
            root=Path(d);(root/"dataset.json").write_bytes(b.blob(self.parts))
            self.assertEqual(b.load_inputs(root/"summary.json"),(self.parts,self.refs))
            parent.verify_artifacts.assert_called_once_with(root,b.PARENT_EXECUTION)
            payload["status"]="FAIL"
            with self.assertRaises(ValueError):b.load_inputs(root/"summary.json")

    def test_19_count_and_result_scope_contract(self):
        summary=b.analyze(self.parts,self.new,self.records,self.refs,Parent)[1];pins,protected=protection()
        payload=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",
            source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,
            gate_f_candidate=False,production_adoption=False,network_calls=0)
        b.validate_result(payload)
        for key,value in (("model_forward_calls",179),("new_training_steps",1)):
            changed=copy.deepcopy(payload);changed["validation_summary"][key]=value
            with self.assertRaises(ValueError):b.validate_result(changed)
        with self.assertRaises(ValueError):b.validate_result(dict(payload,production_adoption=True))

    def test_20_masks_and_group_scope(self):
        for rows in self.new.values():
            for row in rows:
                self.assertEqual(b.render(row,"evidence_blind").count("?"),3)
                self.assertTrue(b.render(row,"query_blind").endswith("?="))
                self.assertEqual(row["target"],48+row["assignment"][row["query"]])
        output=copy.deepcopy(self.records[0]["outputs"]["novel"]["TRAIN"]);output["normal"][0,0]=float("inf")
        with self.assertRaises(ValueError):b.new_metrics(self.new["TRAIN"],output)

    def test_21_unique_own_ids_and_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self))
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        self.assertEqual(len({t.id() for t in b.flatten(suite)}),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        source=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_22_runner_cli_and_whitespace_robust_parser_order(self):
        root=Path(__file__).resolve().parents[1];runner=(root/"tools/run_c257.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools/invoke_c257.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant)
                    and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1});self.assertEqual(argv(blocks[2]),{1,2,3})
        failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher);self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start())
        self.assertIn("c256-v5b-three-entity-3f95a0d190e4424f91634cb8813d7987",launcher)

    def test_23_run_load_score_save_order(self):
        import inspect
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "")
               for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first=lambda name:min(i for i,n in calls if n==name)
        for left,right in (("load_inputs","load_bundle"),("load_bundle","probe_one"),("probe_one","save"),("analyze","save")):
            self.assertLess(first(left),first(right))

    def test_24_per_order_scores_and_six_order_contrast(self):
        rows=self.new["TRAIN"];outputs=copy.deepcopy(self.records[0]["outputs"]["novel"]["TRAIN"])
        chosen=[i for i,r in enumerate(rows) if r["language"]=="en" and tuple(r["permutation"])==b.NOVEL[0]][0]
        outputs["normal"][chosen]=-10.;outputs["normal"][chosen,200]=10.
        cells,pred=b.new_metrics(rows,outputs)
        self.assertEqual(cells[0]["correct"],35);self.assertEqual(cells[0]["query_triplet_accuracy"],11/12)
        self.assertTrue(all(c["correct"]==36 for c in cells[1:]))
        score=b.six_order_metrics(self.parts["TRAIN"],rows,self.refs[0]["predictions"]["TRAIN"]["normal"],pred["normal"])
        self.assertEqual(score["en"]["all_six_correct"],35);self.assertEqual(score["ja"]["all_six_correct"],36)


if __name__=="__main__":
    unittest.main(verbosity=2)
