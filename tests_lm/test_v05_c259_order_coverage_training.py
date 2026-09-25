"""C259 authoring fixtures are synthetic and do not establish learned capability."""
import ast
from collections import Counter, defaultdict
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
from fold_lm.v05_benchmarks import model_c259_order_coverage_training as b


class Factory:
    @staticmethod
    def prefix_tensor(raw):
        b.require(len(raw) <= 46, "length")
        return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)
    @staticmethod
    def new_model(seed):
        return Tiny(seed)


class Tiny(nn.Module):
    """Synthetic training fixture, not the production C252 architecture."""
    def __init__(self,seed):
        super().__init__(); torch.manual_seed(seed)
        self.backbone = nn.Embedding(259,16)
        self.read = nn.Linear(16,256)
        self.unused = nn.Parameter(torch.zeros(5760))
        self.double().eval()
    def forward(self,tokens,tasks):
        return self.read(self.backbone(tokens).mean(1))


class Base:
    @staticmethod
    def dataset():
        train={(0,1,2),(0,1,3),(0,2,1),(1,0,2),(1,0,3),(1,3,0),(2,0,3),(2,3,0),(2,3,1),(3,1,2),(3,2,0),(3,2,1)}
        parts={s:[] for s in b.SPLITS}
        for a in itertools.permutations(range(4),3):
            split="TRAIN" if a in train else "HOLDOUT"
            for lang in ("en","ja"):
                for order in (0,1):
                    for q in range(3):
                        row=dict(id=f"{lang}-{a[0]}{a[1]}{a[2]}-{order}-{q}",assignment=list(a),language=lang,order=order,query=q,target=48+a[q])
                        row["prompt"]=Orders.render(dict(row,permutation=list(b.ORDERS[order])),"normal")
                        parts[split].append(row)
        return parts
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for name,t in sorted(model.state_dict().items()):
            v=t.detach().cpu().contiguous();h.update(name.encode());h.update(str(v.dtype).encode());h.update(str(tuple(v.shape)).encode());h.update(v.numpy().tobytes())
        return h.hexdigest()
    @staticmethod
    def make_model(backbone,arm,seed,aligned,reader):
        return backbone
    @staticmethod
    def metrics(rows,outputs):
        for x in outputs.values():Orders.check_logits(x,144)
        pred={v:x.argmax(-1).tolist() for v,x in outputs.items()};result={}
        loss=F.cross_entropy(outputs["normal"],torch.tensor([r["target"] for r in rows]),reduction="none")
        for lang in ("en","ja"):
            ids=[i for i,r in enumerate(rows) if r["language"]==lang]
            acc={v:sum(pred[v][i]==rows[i]["target"] for i in ids)/72 for v in b.VIEWS}
            og,qg=defaultdict(list),defaultdict(list)
            for i in ids:
                r=rows[i];og[(tuple(r["assignment"]),r["query"])].append(i);qg[(tuple(r["assignment"]),r["order"])].append(i)
            result[lang]=dict(rows=72,accuracy=acc["normal"],answer_nll=float(loss[ids].mean()),
                evidence_blind_accuracy=acc["evidence_blind"],query_blind_accuracy=acc["query_blind"],
                evidence_drop=acc["normal"]-acc["evidence_blind"],query_drop=acc["normal"]-acc["query_blind"],
                order_pair_accuracy=sum(all(pred["normal"][i]==rows[i]["target"] for i in g) for g in og.values())/36,
                query_triplet_accuracy=sum(all(pred["normal"][i]==rows[i]["target"] for i in g) for g in qg.values())/24)
        return result,pred
    @staticmethod
    def cell_pass(m):
        return Orders.new_cell_pass(m) and m["order_pair_accuracy"]>=.8
    @staticmethod
    def evaluate(model,parts,factory):
        raw={};metrics={};pred={};model.eval()
        with torch.no_grad():
            for split,rows in parts.items():
                raw[split]={}
                for view in b.VIEWS:
                    x=torch.stack([factory.prefix_tensor(Orders.render(dict(r,permutation=list(b.ORDERS[r["order"]])),view).encode()) for r in rows])
                    raw[split][view]=model(x,torch.zeros(len(x),dtype=torch.int64))
                metrics[split],pred[split]=Base.metrics(rows,raw[split])
        return metrics,pred,raw


class Orders:
    @staticmethod
    def render(r,view):
        names=("a","b","c") if r["language"]=="en" else ("甲","乙","丙")
        return ";".join(names[i]+"="+("?" if view=="evidence_blind" else str(r["assignment"][i])) for i in r["permutation"])+";"+("?" if view=="query_blind" else names[r["query"]])+"="
    @staticmethod
    def novel_dataset(parts):
        result={s:[] for s in b.SPLITS}
        for split,rows in parts.items():
            for old in rows:
                if old["order"]!=0:continue
                for perm in b.ORDERS[2:]:
                    r=dict(source_id=old["id"],id=old["id"]+":"+"".join(map(str,perm)),assignment=old["assignment"],language=old["language"],query=old["query"],target=old["target"],permutation=list(perm))
                    r["prompt"]=Orders.render(r,"normal");result[split].append(r)
        return result
    @staticmethod
    def check_logits(x,n):
        b.require(x.shape==(n,256) and x.dtype==torch.float64 and x.device.type=="cpu" and bool(torch.isfinite(x).all()),"finite logits")
    @staticmethod
    def replay(x,y):
        Orders.check_logits(x,len(y));Orders.check_logits(y,len(y));error=float((x-y).abs().max())
        b.require(error<=b.TOL and torch.equal(x.argmax(-1),y.argmax(-1)),"logit/argmax replay")
        return error
    @staticmethod
    def new_metrics(rows,outputs):
        for x in outputs.values():Orders.check_logits(x,288)
        pred={v:x.argmax(-1).tolist() for v,x in outputs.items()};cells=[]
        loss=F.cross_entropy(outputs["normal"],torch.tensor([r["target"] for r in rows]),reduction="none")
        for lang in ("en","ja"):
            for perm in b.ORDERS[2:]:
                ids=[i for i,r in enumerate(rows) if r["language"]==lang and tuple(r["permutation"])==perm]
                groups=defaultdict(list)
                for i in ids:groups[tuple(rows[i]["assignment"])].append(i)
                acc={v:sum(pred[v][i]==rows[i]["target"] for i in ids)/36 for v in b.VIEWS}
                cells.append(dict(language=lang,permutation=list(perm),rows=36,correct=round(acc["normal"]*36),accuracy=acc["normal"],
                    query_triplet_accuracy=sum(all(pred["normal"][i]==rows[i]["target"] for i in g) for g in groups.values())/12,
                    evidence_blind_accuracy=acc["evidence_blind"],query_blind_accuracy=acc["query_blind"],
                    evidence_drop=acc["normal"]-acc["evidence_blind"],query_drop=acc["normal"]-acc["query_blind"],answer_nll=float(loss[ids].mean())))
        return cells,pred
    @staticmethod
    def new_cell_pass(c):
        return c["accuracy"]>=.9 and c["query_triplet_accuracy"]>=.8 and c["evidence_drop"]>=.35 and c["query_drop"]>=.35
    @staticmethod
    def six_order_metrics(old,new,op,np):
        groups=defaultdict(list)
        for rows,pred in ((old,op),(new,np)):
            for r,p in zip(rows,pred,strict=True):groups[(r["language"],tuple(r["assignment"]),r["query"])].append(p==r["target"])
        b.require(len(groups)==72 and all(len(g)==6 for g in groups.values()),"groups")
        return {lang:dict(groups=36,all_six_correct=sum(all(g) for k,g in groups.items() if k[0]==lang),accuracy=sum(all(g) for k,g in groups.items() if k[0]==lang)/36) for lang in ("en","ja")}
    @staticmethod
    def evaluate_new(model,parts,factory):
        result={}
        with torch.no_grad():
            for split,rows in parts.items():
                result[split]={}
                for view in b.VIEWS:
                    x=torch.stack([factory.prefix_tensor(Orders.render(r,view).encode()) for r in rows]);result[split][view]=model(x,torch.zeros(len(x),dtype=torch.int64))
        return result


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("synthetic-input-"):return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):
        child=(Path(root)/name).resolve();b.require(child.parent==Path(root).resolve(),"unsafe path");return child
    @staticmethod
    def git(root,*args):
        if args==("rev-parse","HEAD"):return b"synthetic-head"
        if args==("branch","--show-current"):return b"feat/sft-target-loss"
        return b""


def protection():
    return {**{f"old-{i}":"fixture" for i in range(394)},**{n:"fixture" for n in b.OWN}},{f"synthetic-input-{i}":"0"*64 for i in range(659)}


def perfect_records(parts,extra):
    raw={}
    for name,data in (("original",parts),("extra",extra)):
        raw[name]={}
        for split,rows in data.items():
            raw[name][split]={}
            for view in b.VIEWS:
                x=torch.full((len(rows),256),-10.,dtype=torch.float64)
                for i,r in enumerate(rows):x[i,r["target"] if view=="normal" else 48]=10.
                raw[name][split][view]=x
    return [dict(seed=seed,arm=arm,parameters=14256,initial_sha256=str(seed),backbone_initial_sha256=str(seed),final_sha256="final",
        weights_changed=True,backbone_changed=True,head_changed=True,checkpoint_roundtrip=True,reload_max_error=0.,
        forward_calls=812,row_presentations=40992,replay_forward_calls=12,replay_row_presentations=2592,
        fit=dict(steps=800,answer_presentations=38400,logical_batch_sha256="synthetic",order_pair_updates=[800,0,0] if arm=="two_order" else [267,267,266]),
        raw=copy.deepcopy(raw)) for seed,arm in b.identities()]


class C259Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.parts=Base.dataset();cls.extra=Orders.novel_dataset(cls.parts)
        cls.tokens,cls.targets=b.training_tables(cls.parts,Factory,Orders)
        cls.records=perfect_records(cls.parts,cls.extra)

    def test_01_fixed_manifest_and_dataset_hashes(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),b.manifest()["original_dataset_sha256"])
        self.assertEqual(b.digest(self.extra),b.manifest()["extra_dataset_sha256"])
        with contextlib.redirect_stdout(io.StringIO()):
            b.validate_registration(400,659)
            with self.assertRaises(ValueError):b.validate_registration(399,659)
            with patch.object(b,"MANIFEST_SHA","wrong"),self.assertRaises(ValueError):b.validate_registration(400,659)

    def test_02_all800_batches_are_paired(self):
        counts=Counter()
        for step in range(800):
            a,pa=b.training_plan(b.SEEDS[0],step,"two_order");c,pc=b.training_plan(b.SEEDS[0],step,"six_order")
            self.assertTrue(torch.equal(a,c));self.assertEqual((len(a),pa),(48,0));counts[pc]+=1
        self.assertEqual([counts[i] for i in range(3)],[267,267,266])

    def test_03_complete_epoch_no_duplicate_or_omission(self):
        for seed in b.SEEDS:
            for epoch in (0,1,20,265):
                ids=torch.cat([b.training_plan(seed,3*epoch+i,"two_order")[0] for i in range(3)])
                self.assertEqual(sorted(ids.tolist()),list(range(144)))

    def test_04_nine_step_order_coverage_for_each_base_question(self):
        seen=defaultdict(list)
        for step in range(9):
            ids,pair=b.training_plan(b.SEEDS[0],step,"six_order")
            for i in ids.tolist():
                r=self.parts["TRAIN"][i];seen[(tuple(r["assignment"]),r["language"],r["query"])].append(b.ORDERS[2*pair+r["order"]])
        self.assertEqual(len(seen),72)
        for perms in seen.values():self.assertEqual(set(perms),set(b.ORDERS));self.assertEqual(len(perms),6)

    def test_05_visible_bytes_and_targets_only_order_changes(self):
        for i,r in enumerate(self.parts["TRAIN"]):
            self.assertEqual(self.targets[i].item(),r["target"])
            for pair in range(3):
                raw=bytes(v for v in self.tokens[pair,i].tolist() if v<256).decode()
                self.assertEqual(raw.split(";")[-1],r["prompt"].split(";")[-1])
                self.assertEqual(sorted(raw.split(";")[:-1]),sorted(r["prompt"].split(";")[:-1]))
            self.assertEqual(bytes(v for v in self.tokens[0,i].tolist() if v<256).decode(),r["prompt"])

    def test_06_no_holdout_optimization_and_fresh_seeds(self):
        altered=copy.deepcopy(self.parts);altered["HOLDOUT"]=[]
        x,y=b.training_tables(altered,Factory,Orders)
        self.assertTrue(torch.equal(x,self.tokens));self.assertTrue(torch.equal(y,self.targets))
        self.assertTrue(set(b.SEEDS).isdisjoint(range(256001,256006)))
        with self.assertRaises(ValueError):b.training_plan(b.SEEDS[0],800,"six_order")

    def test_07_actual_fit_gradient_and_paired_trace(self):
        source=Tiny(b.SEEDS[0]);out=[]
        with patch.object(b,"STEPS",3):
            for arm in b.ARMS:
                model=copy.deepcopy(source);before=Base.fingerprint(model)
                result=b.fit(model,self.tokens,self.targets,b.SEEDS[0],arm);out.append(result)
                self.assertNotEqual(before,Base.fingerprint(model));self.assertEqual(result["steps"],3)
                self.assertIsNotNone(model.backbone.weight.grad);self.assertIsNotNone(model.read.weight.grad)
        self.assertEqual(out[0]["logical_batch_sha256"],out[1]["logical_batch_sha256"])

    def test_08_identical_complete_initial_states(self):
        source=Tiny(b.SEEDS[0]);a,c=copy.deepcopy(source),copy.deepcopy(source)
        self.assertEqual(Base.fingerprint(a),Base.fingerprint(c));self.assertEqual(sum(p.numel() for p in a.parameters()),14256)
        self.assertNotEqual(Base.fingerprint(a),Base.fingerprint(Tiny(b.SEEDS[1])))

    def test_09_actual_train_and_checkpoint_workload(self):
        model=Tiny(b.SEEDS[0])
        with contextlib.redirect_stdout(io.StringIO()):r,state=b.train_one(model,self.parts,self.extra,self.tokens,self.targets,b.SEEDS[0],"two_order",Base,Orders,Factory)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(812,40992))
        b.replay_one(Tiny(b.SEEDS[0]),state,r,self.parts,self.extra,Base,Orders,Factory)
        self.assertEqual((r["replay_forward_calls"],r["replay_row_presentations"]),(12,2592))
        self.assertTrue(r["checkpoint_roundtrip"]);self.assertLessEqual(r["reload_max_error"],b.TOL)
        self.assertTrue(all(r[k] for k in ("backbone_changed","head_changed","weights_changed")))

    def test_10_evaluation_preserves_weights(self):
        m=Tiny(b.SEEDS[0]);before=Base.fingerprint(m);b.evaluate(m,self.parts,self.extra,Base,Orders,Factory)
        self.assertEqual(before,Base.fingerprint(m))

    def test_11_perfect_gate_and_independent_control(self):
        rows,s=b.analyze(self.records,self.parts,self.extra,Base,Orders)
        self.assertEqual(s["seed_pass_counts"],{"two_order":5,"six_order":5})
        self.assertTrue(s["candidate_gate"]);self.assertTrue(all(c["accuracy_delta"]==c["six_order_delta"]==0 for c in s["comparisons"]))

    def test_12_one_treatment_miss_fails_primary(self):
        records=copy.deepcopy(self.records);records[1]["raw"]["extra"]["HOLDOUT"]["normal"][:]=0
        _,s=b.analyze(records,self.parts,self.extra,Base,Orders)
        self.assertFalse(s["candidate_gate"]);self.assertEqual(s["seed_pass_counts"]["six_order"],4)
        self.assertEqual(s["seed_pass_counts"]["two_order"],5)

    def test_13_original_gate_retained(self):
        records=copy.deepcopy(self.records);records[1]["raw"]["original"]["TRAIN"]["normal"][:]=0
        rows,_=b.analyze(records,self.parts,self.extra,Base,Orders)
        self.assertEqual(rows[1]["outcome"],"ORIGINAL_CRITERIA_MISS")

    def test_14_every_extra_permutation_separate(self):
        records=copy.deepcopy(self.records);rows=self.extra["HOLDOUT"]
        ids=[i for i,r in enumerate(rows) if r["language"]=="en" and tuple(r["permutation"])==b.ORDERS[2]][:4]
        records[1]["raw"]["extra"]["HOLDOUT"]["normal"][ids]=0
        rows,_=b.analyze(records,self.parts,self.extra,Base,Orders);self.assertEqual(rows[1]["outcome"],"EXTRA_ORDER_MISS")

    def test_15_six_order_consistency_not_pooled_accuracy(self):
        records=copy.deepcopy(self.records);rows=self.extra["TRAIN"]
        assignments=sorted({tuple(r["assignment"]) for r in rows})
        for p,perm in enumerate(b.ORDERS[2:]):
            ids=[i for i,r in enumerate(rows) if r["language"]=="en" and tuple(r["permutation"])==perm and r["query"]==0 and tuple(r["assignment"]) in assignments[2*p:2*p+2]]
            records[1]["raw"]["extra"]["TRAIN"]["normal"][ids]=0
        out,_=b.analyze(records,self.parts,self.extra,Base,Orders)
        self.assertEqual(out[1]["outcome"],"SIX_ORDER_MISS");self.assertEqual(out[1]["six_order"]["TRAIN"]["en"]["all_six_correct"],28)

    def test_16_paired_identity_and_schedule_guards(self):
        for key in ("initial_sha256","backbone_initial_sha256"):
            records=copy.deepcopy(self.records);records[1][key]="mismatch"
            with self.assertRaises(ValueError):b.analyze(records,self.parts,self.extra,Base,Orders)
        records=copy.deepcopy(self.records);records[1]["fit"]["logical_batch_sha256"]="mismatch"
        with self.assertRaises(ValueError):b.analyze(records,self.parts,self.extra,Base,Orders)

    def test_17_nonfinite_replay_and_wrong_record_counts(self):
        records=copy.deepcopy(self.records);records[1]["raw"]["extra"]["TRAIN"]["normal"][0,0]=float("nan")
        with self.assertRaises(ValueError):b.analyze(records,self.parts,self.extra,Base,Orders)
        with self.assertRaises(ValueError):b.analyze(self.records[:-1],self.parts,self.extra,Base,Orders)
        records=copy.deepcopy(self.records);records[1]["reload_max_error"]=2e-9
        with self.assertRaises(ValueError):b.analyze(records,self.parts,self.extra,Base,Orders)

    def test_18_parent_loader_contract_and_corruption(self):
        parent=SimpleNamespace(validate_result=lambda p:None,manifest=lambda:{"synthetic":True})
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);saved={"attributed_rows":8640}
            for name in b.PARENT_ARTIFACTS:(root/name).write_bytes(b.blob(saved if name=="validation-summary.json" else parent.manifest()))
            artifacts=[dict(file=n,sha256=Audit.sha(root/n),serialized_bytes=(root/n).stat().st_size) for n in b.PARENT_ARTIFACTS]
            payload=dict(commit_sha=b.PARENT_EXECUTION,status="PASS",capability_pass_claim=False,causal_mechanism_claim=False,artifacts=artifacts,validation_summary=saved)
            (root/"summary.json").write_bytes(b.blob(payload))
            with patch.object(b,"context",return_value=(parent,Base,Orders,None,None,Factory,Audit)),patch.object(b,"PARENT_SHA",Audit.sha(root/"summary.json")),patch.object(b,"PARENT_ARTIFACTS",{a["file"]:a["sha256"] for a in artifacts}):
                self.assertEqual(b.load_parent(root/"summary.json"),saved)
                with self.assertRaises(ValueError):b.validate_parent(dict(payload,capability_pass_claim=True),parent)
                (root/"audit-plan.json").write_bytes(b"changed")
                with self.assertRaises(ValueError):b.load_parent(root/"summary.json")

    def test_19_result_scope_and_workload(self):
        _,s=b.analyze(self.records,self.parts,self.extra,Base,Orders);pins,protected=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",source_blobs=pins,input_sha256=protected,
            artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False,unseen_order_transfer_claim=False,causal_mechanism_claim=False,network_calls=0)
        b.validate_result(p)
        with self.assertRaises(ValueError):b.validate_result(dict(p,unseen_order_transfer_claim=True))
        p["validation_summary"]["train_steps"]=7999
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_20_actual_run_and_persisted_postcheck_dispatch(self):
        def synthetic_train(model,parts,extra,tokens,targets,seed,arm,base,orders,factory):
            initial=base.fingerprint(model);back=base.fingerprint(model.backbone)
            with torch.no_grad():model.backbone.weight.add_(.01);model.read.weight.add_(.01)
            r=copy.deepcopy(self.records[b.identities().index((seed,arm))]);r.update(initial_sha256=initial,backbone_initial_sha256=back,final_sha256=base.fingerprint(model),raw=b.evaluate(model,parts,extra,base,orders,factory))
            return r,copy.deepcopy(model.state_dict())
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(None,Base,Orders,None,None,Factory,Audit)),patch.object(b,"precheck",return_value=protection()) as pre,patch.object(b,"train_one",side_effect=synthetic_train) as training:
            root=Path(d);out=root/"out"
            with contextlib.redirect_stdout(io.StringIO()):p=b.run(c258_summary=root/"parent.json",output_dir=out,expected_head="synthetic-head")
            self.assertEqual(training.call_count,10);self.assertEqual(pre.call_count,2)
            with patch.object(b,"evaluate",side_effect=AssertionError("postcheck must not evaluate")),patch.object(b,"load_bundle",side_effect=AssertionError("postcheck must not load weights")):
                self.assertEqual(b.verify_artifacts(out,"synthetic-head")[0],p)
            with self.assertRaisesRegex(ValueError,"saved HEAD"):b.verify_artifacts(out,"wrong")
            (out/"measurements.json").write_bytes(b"[]")
            with self.assertRaises(ValueError):b.verify_artifacts(out,"synthetic-head")

    def test_21_semantic_own_count_and_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self))
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        source=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture-{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_22_runner_cli_and_parser_order(self):
        root=Path(__file__).resolve().parents[1];runner=(root/"tools/run_c259.ps1").read_text(encoding="utf-8");launcher=(root/"tools/invoke_c259.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3);indices=[]
        for block in blocks:
            compile(block,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(block)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"})
        self.assertEqual(indices,[{1},set(),{1,2,3}])
        failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher);self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start());self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        self.assertIn("93386fd77e3749bab4122685ff57720d",launcher)

    def test_23_actual_source_call_order_and_parent_protection(self):
        import inspect
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first=lambda name:min(i for i,n in calls if n==name)
        for left,right in (("precheck","training_tables"),("training_tables","train_one"),("train_one","load_bundle"),("load_bundle","replay_one"),("replay_one","analyze")):
            self.assertLess(first(left),first(right))
        tree=ast.parse(inspect.getsource(b.precheck));self.assertTrue(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="load_parent" for n in ast.walk(tree)))

    def test_24_checkpoint_schema_and_identity_order(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"bundle.pt";states=[{} for _ in b.identities()]
            archive=dict(schema="fold-c259-order-coverage-models-v1",identities=[list(x) for x in b.identities()],states=states)
            torch.save(archive,path);self.assertEqual(b.load_bundle(path),states)
            archive["identities"].reverse();torch.save(archive,path)
            with self.assertRaises(ValueError):b.load_bundle(path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
