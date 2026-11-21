"""Synthetic fixtures validate C262 authoring, not real FOLD capability."""
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
from unittest.mock import patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c262_minibatch_order as b


class Core(nn.Module):
    def __init__(self):
        super().__init__(); self.weight = nn.Parameter(torch.zeros(3328))
    def forward(self, x):
        return x + self.weight[:16].tanh()


class Tiny(nn.Module):
    """Synthetic capacity/count fixture; core math is NOT the production FOLD core."""
    def __init__(self, seed):
        super().__init__(); torch.manual_seed(seed)
        self.backbone = nn.Module()
        self.backbone.embedding = nn.Embedding(259,16)
        self.backbone.core = Core()
        self.read = nn.Linear(16,256)
        self.padding = nn.Parameter(torch.zeros(2432))
        self.double().eval()
    def forward(self, tokens, tasks):
        x = self.backbone.embedding(tokens).mean(1)
        for _ in range(4):
            x = self.backbone.core(x)
        return self.read(x)


class Factory:
    @staticmethod
    def new_model(seed):
        return Tiny(seed)
    @staticmethod
    def prefix_tensor(raw):
        b.require(len(raw) <= 46, "length")
        return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)


class Base:
    @staticmethod
    def fingerprint(model):
        h = hashlib.sha256()
        for name,x in sorted(model.state_dict().items()):
            h.update(name.encode()); h.update(x.detach().cpu().numpy().tobytes())
        return h.hexdigest()
    @staticmethod
    def make_model(model, arm, seed, aligned, reader):
        b.require(arm == "aligned_precore_read", "fixture arm")
        return model
    @staticmethod
    def dataset():
        train = {(0,1,2),(0,1,3),(0,2,1),(1,0,2),(1,0,3),(1,3,0),(2,0,3),(2,3,0),(2,3,1),(3,1,2),(3,2,0),(3,2,1)}
        parts = {s:[] for s in b.SPLITS}
        for a in itertools.permutations(range(4),3):
            split = "TRAIN" if a in train else "HOLDOUT"
            for language in ("en","ja"):
                for order in (0,1):
                    for query in range(3):
                        r = dict(id=f"{language}-{a[0]}{a[1]}{a[2]}-{order}-{query}", assignment=list(a), language=language,
                                 order=order, query=query, target=48+a[query])
                        r["prompt"] = Orders.render(dict(r,permutation=list(Orders.ALL[order])),"normal")
                        parts[split].append(r)
        return parts


class Orders:
    ALL = ((0,1,2),(2,1,0),(0,2,1),(1,0,2),(1,2,0),(2,0,1))
    @staticmethod
    def render(r, view):
        names = ("a","b","c") if r["language"] == "en" else ("甲","乙","丙")
        return ";".join(names[i]+"="+("?" if view=="evidence_blind" else str(r["assignment"][i])) for i in r["permutation"])+";"+("?" if view=="query_blind" else names[r["query"]])+"="
    @staticmethod
    def novel_dataset(parts):
        result = {s:[] for s in b.SPLITS}
        for split, rows in parts.items():
            for old in rows:
                if old["order"] != 0:
                    continue
                for p in Orders.ALL[2:]:
                    r = dict(source_id=old["id"],id=old["id"]+":"+"".join(map(str,p)),assignment=list(old["assignment"]),
                             language=old["language"],query=old["query"],target=old["target"],permutation=list(p))
                    r["prompt"] = Orders.render(r,"normal"); result[split].append(r)
        return result


class Trainer:
    @staticmethod
    def training_tables(parts, factory, orders):
        rows = parts["TRAIN"]
        return torch.stack([torch.stack([factory.prefix_tensor(orders.render(dict(r,permutation=list(orders.ALL[2*p+r["order"]])),"normal").encode()) for r in rows]) for p in range(3)]), torch.tensor([r["target"] for r in rows])
    @staticmethod
    def evaluate(model, parts, extra, base, orders, factory):
        raw = {}; model.eval()
        with torch.no_grad():
            for stage,data in (("original",parts),("extra",extra)):
                raw[stage] = {}
                for split,rows in data.items():
                    raw[stage][split] = {}
                    for view in b.VIEWS:
                        converted = [dict(r,permutation=list(orders.ALL[r["order"]])) if stage=="original" else r for r in rows]
                        x = torch.stack([factory.prefix_tensor(orders.render(r,view).encode()) for r in converted])
                        raw[stage][split][view] = model(x,torch.zeros(len(x),dtype=torch.int64))
        return raw
    @staticmethod
    def replay_one(model,state,r,parts,extra,base,orders,factory):
        model.load_state_dict(state,strict=True); model.eval()
        b.require(base.fingerprint(model)==r["final_sha256"],"checkpoint")
        raw = Trainer.evaluate(model,parts,extra,base,orders,factory); error=0.
        for stage in raw:
            for split in b.SPLITS:
                for view in b.VIEWS:
                    x,y=raw[stage][split][view],r["raw"][stage][split][view]
                    error=max(error,float((x-y).abs().max()))
                    b.require(torch.isfinite(x).all() and torch.equal(x.argmax(-1),y.argmax(-1)),"argmax")
        b.require(error<=b.TOL,"raw replay")
        r.update(checkpoint_roundtrip=True,reload_max_error=error,replay_forward_calls=12,replay_row_presentations=2592)


class Scorer:
    @staticmethod
    def core_counter(model):
        calls=[0]
        def counted(module,args,output):
            calls[0]+=1
        return calls,model.backbone.core.register_forward_hook(counted)
    @staticmethod
    def score(raw,parts,extra,base,orders):
        b.require(set(raw)=={"original","extra"},"stages")
        outputs={}; original={}; added={}; six={}; accuracy={}
        for stage,data in (("original",parts),("extra",extra)):
            b.require(set(raw[stage])==set(b.SPLITS),"splits")
            for split,rows in data.items():
                b.require(set(raw[stage][split])==set(b.VIEWS),"views")
                for view,x in raw[stage][split].items():
                    b.require(x.shape==(len(rows),256) and x.dtype==torch.float64 and bool(torch.isfinite(x).all()),"finite logits")
                    outputs[stage,split,view]=x.argmax(-1).tolist()
        def cell(rows,stage,split,ids):
            p={v:outputs[stage,split,v] for v in b.VIEWS}
            acc={v:sum(p[v][i]==rows[i]["target"] for i in ids)/len(ids) for v in b.VIEWS}
            groups=defaultdict(list)
            for i in ids:
                r=rows[i]; groups[tuple(r["assignment"]),r.get("order",tuple(r.get("permutation",())))].append(i)
            q=sum(all(p["normal"][i]==rows[i]["target"] for i in g) for g in groups.values())/len(groups)
            return dict(accuracy=acc["normal"],query_triplet_accuracy=q,evidence_drop=acc["normal"]-acc["evidence_blind"],query_drop=acc["normal"]-acc["query_blind"])
        def passed(c):
            return c["accuracy"]>=.9 and c["query_triplet_accuracy"]>=.8 and c["evidence_drop"]>=.35 and c["query_drop"]>=.35
        old_ok=new_ok=six_ok=True
        for split in b.SPLITS:
            original[split]={}; added[split]=[]; six[split]={}; accuracy[split]={}
            for lang in ("en","ja"):
                ids=[i for i,r in enumerate(parts[split]) if r["language"]==lang]
                c=cell(parts[split],"original",split,ids); groups=defaultdict(list)
                for i in ids:
                    r=parts[split][i]; groups[tuple(r["assignment"]),r["query"]].append(i)
                c["order_pair_accuracy"]=sum(all(outputs["original",split,"normal"][i]==parts[split][i]["target"] for i in g) for g in groups.values())/36
                original[split][lang]=c; old_ok &= passed(c) and c["order_pair_accuracy"]>=.8
                for perm in orders.ALL[2:]:
                    ids=[i for i,r in enumerate(extra[split]) if r["language"]==lang and tuple(r["permutation"])==perm]
                    c=cell(extra[split],"extra",split,ids); added[split].append(dict(language=lang,permutation=list(perm),**c)); new_ok &= passed(c)
                groups=defaultdict(list); correct=0
                for stage,rows in (("original",parts[split]),("extra",extra[split])):
                    for i,r in enumerate(rows):
                        if r["language"]!=lang: continue
                        ok=outputs[stage,split,"normal"][i]==r["target"]; correct+=ok
                        groups[tuple(r["assignment"]),r["query"]].append(ok)
                b.require(len(groups)==36 and all(len(v)==6 for v in groups.values()),"six groups")
                count=sum(all(v) for v in groups.values()); six_ok &= count/36>=.8
                six[split][lang]=dict(groups=36,all_six_correct=count,accuracy=count/36)
                accuracy[split][lang]=dict(correct=correct,rows=216,accuracy=correct/216)
        return dict(original=original,extra_orders=added,six_order=six,all_order_accuracy=accuracy,passed=old_ok and new_ok and six_ok,
                    outcome="ORIGINAL_CRITERIA_MISS" if not old_ok else "EXTRA_ORDER_MISS" if not new_ok else "SIX_ORDER_MISS" if not six_ok else "PASS")


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("fixture-input-"): return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):
        child=(Path(root)/name).resolve(); b.require(child.parent==Path(root).resolve(),"safe path"); return child
    @staticmethod
    def git(root,*args):
        if args==("rev-parse","HEAD"): return b"fixture-head"
        if args==("branch","--show-current"): return b"feat/sft-target-loss"
        return b""


def protection():
    return {**{f"old-{i}":"fixture" for i in range(412)},**{n:"fixture" for n in b.OWN}}, {f"fixture-input-{i}":"0"*64 for i in range(697)}


def perfect_records(data):
    raw={}
    for stage,parts in data.items():
        raw[stage]={}
        for split,rows in parts.items():
            raw[stage][split]={}
            for view in b.VIEWS:
                x=torch.full((len(rows),256),-10.,dtype=torch.float64)
                for i,r in enumerate(rows): x[i,r["target"] if view=="normal" else 48]=10.
                raw[stage][split][view]=x
    return [dict(seed=s,arm=a,parameters=14256,initial_sha256=str(s),final_sha256="fixture",weights_changed=True,backbone_changed=True,head_changed=True,
        checkpoint_roundtrip=True,reload_max_error=0.,forward_calls=812,row_presentations=40992,core_forward_calls=3248,
        replay_forward_calls=12,replay_row_presentations=2592,replay_core_forward_calls=48,
        fit=dict(steps=800,training_rows=38400,**b.schedule(s,a)[2]),raw=copy.deepcopy(raw)) for s,a in b.identities()]


class C262Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2); parts=Base.dataset(); cls.data=dict(original=parts,extra=Orders.novel_dataset(parts))
        cls.tokens,cls.targets=Trainer.training_tables(parts,Factory,Orders); cls.records=perfect_records(cls.data)

    def test_01_fixed_manifest(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        with contextlib.redirect_stdout(io.StringIO()):
            b.validate_registration(418,697)
            with self.assertRaises(ValueError): b.validate_registration(417,697)
            with patch.object(b,"MANIFEST_SHA","bad"),self.assertRaises(ValueError): b.validate_registration(418,697)

    def test_02_exact_data_hashes_and_no_holdout_training(self):
        for key in ("original","extra"): self.assertEqual(b.digest(self.data[key]),b.manifest()[key+"_dataset_sha256"])
        x,y=Trainer.training_tables(dict(self.data["original"],HOLDOUT=[]),Factory,Orders)
        self.assertTrue(torch.equal(x,self.tokens)); self.assertTrue(torch.equal(y,self.targets))

    def test_03_complete_epoch_same_blocks_reverse_order(self):
        for seed in b.SEEDS:
            for epoch in (0,1,100,265):
                forward=[b.batch_plan(seed,3*epoch+i,b.ARMS[0])[0] for i in range(3)]
                reverse=[b.batch_plan(seed,3*epoch+i,b.ARMS[1])[0] for i in range(3)]
                self.assertTrue(all(torch.equal(a,c) for a,c in zip(forward,reversed(reverse))))
                self.assertEqual(sorted(torch.cat(forward).tolist()),list(range(144)))

    def test_04_final_tail_keeps_the_same_two_blocks(self):
        for seed in b.SEEDS:
            a=[b.batch_plan(seed,s,b.ARMS[0])[0] for s in (798,799)]
            c=[b.batch_plan(seed,s,b.ARMS[1])[0] for s in (798,799)]
            self.assertTrue(torch.equal(a[0],c[1]) and torch.equal(a[1],c[0]))
            self.assertEqual(len(set(torch.cat(a).tolist())),96)

    def test_05_batch_identity_guards(self):
        for args in ((260001,0,b.ARMS[0]),(b.SEEDS[0],800,b.ARMS[0]),(b.SEEDS[0],True,b.ARMS[0]),(b.SEEDS[0],0,"other")):
            with self.assertRaises(ValueError): b.batch_plan(*args)

    def test_06_equal_prompt_exposures_but_different_chronology(self):
        for seed in b.SEEDS:
            a,c=[b.schedule(seed,arm)[2] for arm in b.ARMS]
            self.assertEqual(a["exposure_counts"],c["exposure_counts"]); self.assertEqual(a["exposure_sha256"],c["exposure_sha256"])
            self.assertNotEqual(a["chronology_sha256"],c["chronology_sha256"])
            self.assertEqual(sum(a["exposure_counts"]),38400); self.assertEqual(a["order_pair_updates"],[267,267,266])

    def test_07_identical_initial_clone_no_shared_storage(self):
        t=Tiny(b.SEEDS[0]); a,c=copy.deepcopy(t),copy.deepcopy(t)
        self.assertEqual(Base.fingerprint(a),Base.fingerprint(c)); self.assertEqual(sum(p.numel() for p in a.parameters()),14256)
        with torch.no_grad(): a.read.weight.add_(1.)
        self.assertEqual(Base.fingerprint(c),Base.fingerprint(t)); self.assertNotEqual(Base.fingerprint(a),Base.fingerprint(c))

    def test_08_actual_short_fit_updates_weights(self):
        model=Tiny(b.SEEDS[0]); before=Base.fingerprint(model)
        with patch.object(b,"STEPS",3): r=b.fit(model,self.tokens,self.targets,b.SEEDS[0],b.ARMS[1])
        self.assertEqual(r["steps"],3); self.assertNotEqual(before,Base.fingerprint(model))

    def test_09_actual_800_step_train_and_replay(self):
        model=Tiny(b.SEEDS[0])
        with contextlib.redirect_stdout(io.StringIO()):
            r,state=b.train_one(model,b.SEEDS[0],b.ARMS[0],self.data,self.tokens,self.targets,Scorer,Trainer,Base,Orders,Factory)
        b.replay_one(Tiny(b.SEEDS[0]),state,r,self.data,Scorer,Trainer,Base,Orders,Factory)
        self.assertEqual((r["forward_calls"],r["core_forward_calls"],r["replay_core_forward_calls"]),(812,3248,48))
        self.assertEqual(r["reload_max_error"],0.); self.assertTrue(r["checkpoint_roundtrip"])

    def test_10_exception_cleans_count_hooks(self):
        model=Tiny(b.SEEDS[0])
        with patch.object(b,"fit",side_effect=RuntimeError("fixture failure")),self.assertRaises(RuntimeError):
            b.train_one(model,b.SEEDS[0],b.ARMS[0],self.data,self.tokens,self.targets,Scorer,Trainer,Base,Orders,Factory)
        self.assertFalse(model._forward_hooks); self.assertFalse(model.backbone.core._forward_hooks)

    def test_11_perfect_joint_gate(self):
        _,s=b.analyze(self.records,self.data,Scorer,Base,Orders)
        self.assertTrue(s["joint_gate"]); self.assertEqual(s["seed_pass_counts"],{a:5 for a in b.ARMS})
        self.assertTrue(all(c["disagreements"]==0 for c in s["comparisons"]))

    def test_12_neither_arm_can_rescue_other(self):
        for index in (0,1):
            r=copy.deepcopy(self.records); r[index]["raw"]["extra"]["HOLDOUT"]["normal"][:]=0
            _,s=b.analyze(r,self.data,Scorer,Base,Orders)
            self.assertFalse(s["joint_gate"]); self.assertEqual(s["seed_pass_counts"][b.ARMS[index]],4)

    def test_13_one_weak_order_not_hidden_by_average(self):
        r=copy.deepcopy(self.records); rows=self.data["extra"]["TRAIN"]
        ids=[i for i,x in enumerate(rows) if x["language"]=="en" and tuple(x["permutation"])==Orders.ALL[2]][:4]
        r[1]["raw"]["extra"]["TRAIN"]["normal"][ids]=0
        m,_=b.analyze(r,self.data,Scorer,Base,Orders); self.assertEqual(m[1]["outcome"],"EXTRA_ORDER_MISS")

    def test_14_six_order_gate_required(self):
        r=copy.deepcopy(self.records); rows=self.data["extra"]["TRAIN"]; assignments=sorted({tuple(x["assignment"]) for x in rows})
        for j,p in enumerate(Orders.ALL[2:]):
            ids=[i for i,x in enumerate(rows) if x["language"]=="en" and tuple(x["permutation"])==p and x["query"]==0 and tuple(x["assignment"]) in assignments[2*j:2*j+2]]
            r[1]["raw"]["extra"]["TRAIN"]["normal"][ids]=0
        self.assertEqual(b.analyze(r,self.data,Scorer,Base,Orders)[0][1]["outcome"],"SIX_ORDER_MISS")

    def test_15_nonfinite_and_replay_error_rejected(self):
        r=copy.deepcopy(self.records); r[0]["raw"]["extra"]["HOLDOUT"]["normal"][0,0]=float("nan")
        with self.assertRaises(ValueError): b.analyze(r,self.data,Scorer,Base,Orders)
        r=copy.deepcopy(self.records); r[0]["reload_max_error"]=2e-9
        with self.assertRaises(ValueError): b.analyze(r,self.data,Scorer,Base,Orders)

    def test_16_initial_state_mismatch_rejected(self):
        r=copy.deepcopy(self.records); r[1]["initial_sha256"]="different"
        with self.assertRaisesRegex(ValueError,"initial"): b.analyze(r,self.data,Scorer,Base,Orders)

    def test_17_wrong_registered_exposure_and_chronology(self):
        for key in ("exposure_sha256","chronology_sha256"):
            r=copy.deepcopy(self.records); r[1]["fit"][key]="different"
            with self.assertRaisesRegex(ValueError,"schedule"): b.analyze(r,self.data,Scorer,Base,Orders)
        r=copy.deepcopy(self.records); r[1]["fit"]["exposure_counts"][0]+=1
        with self.assertRaises(ValueError): b.analyze(r,self.data,Scorer,Base,Orders)

    def test_18_missing_records_and_wrong_budget(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.data,Scorer,Base,Orders)
        r=copy.deepcopy(self.records); r[0]["fit"]["steps"]=801
        with self.assertRaises(ValueError): b.analyze(r,self.data,Scorer,Base,Orders)

    def test_19_directional_flip_accounting(self):
        left=copy.deepcopy(self.records[0]["raw"]); right=copy.deepcopy(left)
        left["original"]["HOLDOUT"]["normal"][0]=0
        right["original"]["HOLDOUT"]["normal"][1]=0
        left["original"]["HOLDOUT"]["normal"][2]=0
        right["original"]["HOLDOUT"]["normal"][2]=-10.; right["original"]["HOLDOUT"]["normal"][2,200]=10.
        c=b.compare_answers(left,right,self.data,"en")
        self.assertEqual((c["disagreements"],c["correct_to_wrong"],c["wrong_to_correct"],c["both_wrong_different"]),(3,1,1,1))

    def test_20_actual_parent_loader_no_learned_bundle(self):
        parent=SimpleNamespace(validate_result=lambda p:None,manifest=lambda:{"fixture":True})
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); summary={"seed_pass_counts":{"with_core":4,"without_core":3}}
            for n in b.PARENT_ARTIFACTS: (root/n).write_bytes(b.blob(summary if n=="validation-summary.json" else parent.manifest()))
            artifacts=[dict(file=n,sha256=Audit.sha(root/n),serialized_bytes=(root/n).stat().st_size) for n in b.PARENT_ARTIFACTS]
            p=dict(commit_sha=b.PARENT_EXECUTION,status="FAIL",validation_summary=summary,artifacts=artifacts)
            (root/"summary.json").write_bytes(b.blob(p))
            with patch.object(b,"context",return_value=(parent,None,None,None,None,None,None,Factory,Audit)),patch.object(b,"PARENT_SHA",Audit.sha(root/"summary.json")),patch.object(b,"PARENT_ARTIFACTS",{x["file"]:x["sha256"] for x in artifacts}),patch.object(torch,"load",side_effect=AssertionError("no parent weights")):
                self.assertEqual(b.load_parent(root/"summary.json"),p)
                (root/"repeat-plan.json").write_bytes(b"changed")
                with self.assertRaises(ValueError): b.load_parent(root/"summary.json")

    def test_21_actual_run_saved_postcheck(self):
        def trained(model,seed,arm,data,tokens,targets,c260,trainer,base,orders,factory):
            r=copy.deepcopy(self.records[b.identities().index((seed,arm))]); r["initial_sha256"]=base.fingerprint(model)
            with torch.no_grad(): model.read.weight.add_(.01)
            r.update(final_sha256=base.fingerprint(model),raw=trainer.evaluate(model,data["original"],data["extra"],base,orders,factory))
            return r,copy.deepcopy(model.state_dict())
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(None,Scorer,Trainer,Base,Orders,None,None,Factory,Audit)),patch.object(b,"precheck",return_value=protection()) as pre,patch.object(b,"train_one",side_effect=trained) as train:
            out=Path(d)/"out"
            with contextlib.redirect_stdout(io.StringIO()): p=b.run(c261_summary=Path(d)/"parent.json",output_dir=out,expected_head="fixture-head")
            self.assertEqual(train.call_count,10); self.assertEqual(pre.call_count,2)
            with patch.object(Factory,"new_model",side_effect=AssertionError("no postcheck model")),patch.object(b,"load_bundle",side_effect=AssertionError("no postcheck weights")):
                self.assertEqual(b.verify_artifacts(out,"fixture-head")[0],p)
            with self.assertRaisesRegex(ValueError,"saved HEAD"): b.verify_artifacts(out,"wrong")
            (out/"measurements.json").write_bytes(b"[]")
            with self.assertRaises(ValueError): b.verify_artifacts(out,"fixture-head")

    def test_22_semantic_own_count_and_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self)); self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name): super().__init__(); self.name=name
            def id(self): return self.name
        source=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture-{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_23_cli_parser_and_source_call_order(self):
        import inspect
        root=Path(__file__).resolve().parents[1]; runner=(root/"tools/run_c262.ps1").read_text(encoding="utf-8"); launcher=(root/"tools/invoke_c262.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3); indices=[]
        for block in blocks:
            compile(block,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(block)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"})
        self.assertEqual(indices,[{1},set(),{1,2,3}]); failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher)
        self.assertIsNotNone(failure); self.assertLess(launcher.index("::ParseFile"),failure.start()); self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        self.assertIn("66e5eb87a146491e833bbd2f32ce6989",launcher)
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first=lambda name:min(i for i,n in calls if n==name)
        for left,right in (("precheck","training_tables"),("train_one","load_bundle"),("replay_one","analyze")): self.assertLess(first(left),first(right))
        self.assertIn("load_parent",inspect.getsource(b.precheck))

    def test_24_bundle_and_scope_contract(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"models.pt"; value=dict(schema="fold-c262-batch-models-v1",identities=[list(x) for x in b.identities()],states=[{}]*10)
            torch.save(value,path); self.assertEqual(len(b.load_bundle(path)),10)
            value["identities"].reverse(); torch.save(value,path)
            with self.assertRaises(ValueError): b.load_bundle(path)
        _,s=b.analyze(self.records,self.data,Scorer,Base,Orders); pins,protected=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",source_blobs=pins,input_sha256=protected,
            artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,production_adoption=False,gate_f_candidate=False,initialization_only_cause_claim=False,core_superiority_claim=False,general_language_claim=False,network_calls=0)
        b.validate_result(p)
        with self.assertRaises(ValueError): b.validate_result(dict(p,initialization_only_cause_claim=True))
        p["validation_summary"]["seed_pass_counts"][b.ARMS[0]]=4
        with self.assertRaises(ValueError): b.validate_result(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
