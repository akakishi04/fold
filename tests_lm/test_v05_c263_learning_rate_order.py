"""C263 authoring tests reuse explicit synthetic C262 fixtures, not learned models."""
import ast
import contextlib
import copy
import io
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c263_learning_rate_order as b
from fold_lm.v05_benchmarks import model_c262_minibatch_order as parent
from tests_lm.test_v05_c262_minibatch_order import Tiny, Factory, Base, Orders, Trainer, Scorer, Audit


def protection():
    return ({**{f"old-{i}":"fixture" for i in range(418)}, **{n:"fixture" for n in b.OWN}},
            {f"fixture-input-{i}":"0"*64 for i in range(710)})


def records(data):
    raw = {}
    for stage, parts in data.items():
        raw[stage] = {}
        for split, rows in parts.items():
            raw[stage][split] = {}
            for view in b.VIEWS:
                x = torch.full((len(rows),256), -10., dtype=torch.float64)
                for i,r in enumerate(rows):
                    x[i, r["target"] if view == "normal" else 48] = 10.
                raw[stage][split][view] = x
    out = []
    for seed,arm in b.identities():
        _, order, lr = b.arm_config(arm)
        out.append(dict(seed=seed,arm=arm,parameters=14256,initial_sha256=str(seed),final_sha256="fixture",
            weights_changed=True,backbone_changed=True,head_changed=True,checkpoint_roundtrip=True,reload_max_error=0.,
            forward_calls=812,row_presentations=40992,core_forward_calls=3248,
            replay_forward_calls=12,replay_row_presentations=2592,replay_core_forward_calls=48,
            fit=dict(steps=800,training_rows=38400,lr=lr,order=order,last_loss=0.,**b.schedule(seed,order)[2]),raw=copy.deepcopy(raw)))
    return out


class C263Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        parts = Base.dataset(); cls.data = dict(original=parts,extra=Orders.novel_dataset(parts))
        cls.tokens,cls.targets = Trainer.training_tables(parts,Factory,Orders)
        cls.records = records(cls.data)

    def analyze(self, value):
        return b.analyze(value,self.data,parent,Scorer,Base,Orders)

    def test_01_fixed_manifest_and_registration(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        with contextlib.redirect_stdout(io.StringIO()):
            b.validate_registration(424,710)
            with self.assertRaisesRegex(ValueError,"counts"): b.validate_registration(423,710)
            with patch.object(b,"MANIFEST_SHA","wrong"),self.assertRaisesRegex(ValueError,"manifest"):
                b.validate_registration(424,710)

    def test_02_four_arm_identity_and_fresh_seeds(self):
        self.assertEqual(len(b.identities()),20)
        self.assertEqual(b.ARMS,("standard_forward","standard_reverse","lower_forward","lower_reverse"))
        self.assertTrue(set(b.SEEDS).isdisjoint(range(262001,262006)))
        self.assertEqual([b.arm_config(a)[2] for a in b.ARMS],[.005,.005,.001,.001])
        with self.assertRaises(ValueError): b.arm_config("unknown")

    def test_03_same_exposures_and_reversed_epoch_blocks(self):
        for seed in b.SEEDS:
            f,fp,fm = b.schedule(seed,"forward"); r,rp,rm = b.schedule(seed,"reverse")
            self.assertTrue(torch.equal(fp,rp))
            self.assertEqual(fm["exposure_counts"],rm["exposure_counts"])
            self.assertNotEqual(fm["chronology_sha256"],rm["chronology_sha256"])
            self.assertEqual(sum(fm["exposure_counts"]),38400)
            for epoch in range(266):
                self.assertTrue(torch.equal(f[epoch*3:epoch*3+3],r[epoch*3:epoch*3+3].flip(0)))

    def test_04_fixed_incomplete_tail(self):
        for seed in b.SEEDS:
            f,_,fm = b.schedule(seed,"forward"); r,_,_ = b.schedule(seed,"reverse")
            self.assertTrue(torch.equal(f[798],r[799]) and torch.equal(f[799],r[798]))
            self.assertEqual(fm["order_pair_updates"],[267,267,266])
        with self.assertRaises(ValueError): b.schedule(262001,"forward")

    def test_05_exact_data_no_holdout_training(self):
        for key in self.data:
            self.assertEqual(b.digest(self.data[key]),b.manifest()[key+"_dataset_sha256"])
        x,y = Trainer.training_tables(dict(self.data["original"],HOLDOUT=[]),Factory,Orders)
        self.assertTrue(torch.equal(x,self.tokens) and torch.equal(y,self.targets))

    def test_06_actual_optimizer_rate_dispatch(self):
        original = torch.optim.AdamW
        for arm in b.ARMS:
            model = Tiny(b.SEEDS[0]); before = Base.fingerprint(model)
            with patch.object(b,"STEPS",3),patch.object(torch.optim,"AdamW",wraps=original) as opt:
                value = b.fit(model,self.tokens,self.targets,b.SEEDS[0],arm)
            self.assertEqual(opt.call_args.kwargs["lr"],b.arm_config(arm)[2])
            self.assertEqual(value["steps"],3); self.assertNotEqual(before,Base.fingerprint(model))

    def test_07_actual_800_update_loop_and_parent_replay(self):
        model = Tiny(b.SEEDS[0])
        with contextlib.redirect_stdout(io.StringIO()):
            r,state = b.train_one(model,b.SEEDS[0],b.ARMS[2],self.data,self.tokens,self.targets,Scorer,Trainer,Base,Orders,Factory)
        parent.replay_one(Tiny(b.SEEDS[0]),state,r,self.data,Scorer,Trainer,Base,Orders,Factory)
        self.assertEqual((r["forward_calls"],r["core_forward_calls"],r["replay_core_forward_calls"]),(812,3248,48))
        self.assertEqual(r["fit"]["lr"],.001); self.assertEqual(r["reload_max_error"],0.)

    def test_08_exception_cleans_hooks(self):
        model = Tiny(b.SEEDS[0])
        with patch.object(b,"fit",side_effect=RuntimeError("fixture")),self.assertRaises(RuntimeError):
            b.train_one(model,b.SEEDS[0],b.ARMS[0],self.data,self.tokens,self.targets,Scorer,Trainer,Base,Orders,Factory)
        self.assertFalse(model._forward_hooks); self.assertFalse(model.backbone.core._forward_hooks)

    def test_09_complete_initial_state_no_shared_storage(self):
        model = Tiny(b.SEEDS[0]); copies = [copy.deepcopy(model) for _ in b.ARMS]
        self.assertEqual(len({Base.fingerprint(m) for m in copies}),1)
        self.assertEqual(sum(p.numel() for p in model.parameters()),14256)
        with torch.no_grad(): copies[0].read.weight.add_(1.)
        self.assertEqual(Base.fingerprint(copies[1]),Base.fingerprint(model))

    def test_10_perfect_candidate_and_comparison_counts(self):
        _,s = self.analyze(self.records)
        self.assertTrue(s["candidate_gate"]); self.assertEqual(s["rate_joint_pass"],{"standard":True,"lower":True})
        self.assertEqual((len(s["rate_contrasts"]),len(s["order_contrasts"]),len(s["interactions"])),(20,20,10))

    def test_11_one_lower_state_miss_fails_candidate(self):
        r = copy.deepcopy(self.records); r[2]["raw"]["original"]["TRAIN"]["normal"][:]=0
        _,s = self.analyze(r)
        self.assertFalse(s["candidate_gate"]); self.assertTrue(s["rate_joint_pass"]["standard"])
        self.assertEqual(s["seed_pass_counts"]["lower_forward"],4)

    def test_12_standard_miss_does_not_fail_lower_candidate(self):
        r = copy.deepcopy(self.records); r[0]["raw"]["original"]["TRAIN"]["normal"][:]=0
        _,s = self.analyze(r)
        self.assertTrue(s["candidate_gate"]); self.assertFalse(s["rate_joint_pass"]["standard"])

    def test_13_rate_and_exposure_contracts(self):
        for key,value in (("lr",.002),("order","reverse"),("exposure_sha256","wrong")):
            r = copy.deepcopy(self.records); r[2]["fit"][key]=value
            with self.assertRaises(ValueError): self.analyze(r)

    def test_14_initial_state_mismatch(self):
        r = copy.deepcopy(self.records); r[3]["initial_sha256"]="different"
        with self.assertRaisesRegex(ValueError,"initial state"): self.analyze(r)

    def test_15_rate_order_interaction_and_flips(self):
        r = copy.deepcopy(self.records); r[1]["raw"]["original"]["HOLDOUT"]["normal"][0]=0
        _,s = self.analyze(r)
        x = next(x for x in s["interactions"] if x["seed"]==b.SEEDS[0] and x["language"]=="en")
        self.assertEqual((x["standard_disagreements"],x["lower_disagreements"],x["disagreement_delta"]),(1,0,-1))
        rate = next(x for x in s["rate_contrasts"] if x["seed"]==b.SEEDS[0] and x["language"]=="en" and x["left_arm"]=="standard_reverse")
        self.assertEqual(rate["wrong_to_correct"],1)

    def test_16_identical_bad_answers_are_not_robust_capability(self):
        r = copy.deepcopy(self.records)
        for entry in r:
            if entry["arm"].startswith("lower_"):
                for stage in entry["raw"].values():
                    for split in stage.values(): split["normal"][:]=0
        _,s = self.analyze(r)
        self.assertTrue(all(x["lower_disagreements"]==0 for x in s["interactions"]))
        self.assertFalse(s["candidate_gate"])

    def test_17_per_order_and_six_order_gates(self):
        r = copy.deepcopy(self.records); rows = self.data["extra"]["TRAIN"]
        ids=[i for i,x in enumerate(rows) if x["language"]=="en" and tuple(x["permutation"])==Orders.ALL[2]][:4]
        r[2]["raw"]["extra"]["TRAIN"]["normal"][ids]=0
        self.assertEqual(self.analyze(r)[0][2]["outcome"],"EXTRA_ORDER_MISS")
        r = copy.deepcopy(self.records); assignments=sorted({tuple(x["assignment"]) for x in rows})
        for j,perm in enumerate(Orders.ALL[2:]):
            ids=[i for i,x in enumerate(rows) if x["language"]=="en" and tuple(x["permutation"])==perm and x["query"]==0 and tuple(x["assignment"]) in assignments[2*j:2*j+2]]
            r[2]["raw"]["extra"]["TRAIN"]["normal"][ids]=0
        self.assertEqual(self.analyze(r)[0][2]["outcome"],"SIX_ORDER_MISS")

    def test_18_nonfinite_identity_and_replay_errors(self):
        with self.assertRaises(ValueError): self.analyze(self.records[:-1])
        for key,value in (("reload_max_error",2e-9),("core_forward_calls",0)):
            r=copy.deepcopy(self.records); r[2][key]=value
            with self.assertRaises(ValueError): self.analyze(r)
        r=copy.deepcopy(self.records); r[2]["raw"]["extra"]["TRAIN"]["normal"][0,0]=float("nan")
        with self.assertRaises(ValueError): self.analyze(r)

    def test_19_actual_negative_parent_loader_dispatch(self):
        p=dict(commit_sha=b.PARENT_EXECUTION,status="FAIL",validation_summary={"seed_pass_counts":{"forward_blocks":0,"reverse_blocks":2}},
               artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        fake=SimpleNamespace(verify_artifacts=Mock(return_value=(p,[{}]*10)))
        audit=SimpleNamespace(sha=lambda path:b.PARENT_SHA)
        with patch.object(b,"context",return_value=(fake,None,None,None,None,None,None,None,audit)):
            path=(Path(tempfile.gettempdir())/"c263-parent"/"summary.json").resolve()
            self.assertEqual(b.load_parent(path),p)
            fake.verify_artifacts.assert_called_once_with(path.parent,b.PARENT_EXECUTION)
            p["status"]="PASS"
            with self.assertRaises(ValueError): b.load_parent(path)

    def test_20_actual_twenty_state_run_and_persisted_postcheck(self):
        def trained(model,seed,arm,data,tokens,targets,c260,trainer,base,orders,factory):
            r=copy.deepcopy(self.records[b.identities().index((seed,arm))]); r["initial_sha256"]=base.fingerprint(model)
            with torch.no_grad(): model.read.weight.add_(.01)
            r.update(final_sha256=base.fingerprint(model),raw=trainer.evaluate(model,data["original"],data["extra"],base,orders,factory))
            return r,copy.deepcopy(model.state_dict())
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,Scorer,Trainer,Base,Orders,None,None,Factory,Audit)),patch.object(b,"precheck",return_value=protection()) as pre,patch.object(b,"train_one",side_effect=trained) as train:
            out=Path(d)/"out"
            with contextlib.redirect_stdout(io.StringIO()): p=b.run(c262_summary=Path(d)/"parent.json",output_dir=out,expected_head="fixture-head")
            self.assertEqual(train.call_count,20); self.assertEqual(pre.call_count,2)
            with patch.object(Factory,"new_model",side_effect=AssertionError("no model in postcheck")),patch.object(b,"load_bundle",side_effect=AssertionError("no weights in postcheck")):
                self.assertEqual(b.verify_artifacts(out,"fixture-head")[0],p)
            with self.assertRaisesRegex(ValueError,"saved HEAD"): b.verify_artifacts(out,"wrong")
            (out/"measurements.json").write_bytes(b"[]")
            with self.assertRaises(ValueError): b.verify_artifacts(out,"fixture-head")

    def test_21_bundle_and_result_scope(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"states.pt"; v=dict(schema="fold-c263-rate-models-v1",identities=[list(x) for x in b.identities()],states=[{}]*20)
            torch.save(v,path); self.assertEqual(len(b.load_bundle(path)),20)
            v["identities"].reverse(); torch.save(v,path)
            with self.assertRaises(ValueError): b.load_bundle(path)
        _,s=self.analyze(self.records); pins,protected=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",source_blobs=pins,input_sha256=protected,
               artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,production_adoption=False,gate_f_candidate=False,
               learning_rate_benefit_claim=False,core_superiority_claim=False,general_language_claim=False,network_calls=0)
        b.validate_result(p)
        with self.assertRaises(ValueError): b.validate_result(dict(p,learning_rate_benefit_claim=True))
        s["seed_pass_counts"][b.ARMS[2]]=4
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_22_semantic_own_count_and_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self))
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name): super().__init__(); self.name=name
            def id(self): return self.name
        source=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture-{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_23_cli_parser_and_real_function_order(self):
        import inspect
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c263.ps1").read_text(encoding="utf-8"); launcher=(root/"tools/invoke_c263.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3); indices=[]
        for block in blocks:
            compile(block,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(block)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"})
        self.assertEqual(indices,[{1},set(),{1,2,3}])
        failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher); self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start()); self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        self.assertIn("b955446fc91846aa9fea770cd36b9276",launcher)
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first=lambda name:min(i for i,n in calls if n==name)
        for left,right in (("precheck","training_tables"),("train_one","load_bundle"),("replay_one","analyze")):
            self.assertLess(first(left),first(right))
        self.assertIn("load_parent",inspect.getsource(b.precheck))

    def test_24_dependency_range_and_count_arithmetic(self):
        import inspect
        source=ast.parse(inspect.getsource(b.precheck))
        pattern=next(n.value.value for n in ast.walk(source) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="pattern" for t in n.targets))
        names=["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,263)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names))
        self.assertFalse(re.fullmatch(pattern,"fold_lm/v05_benchmarks/model_c263_future.py"))
        self.assertEqual(5+len(names)+1,b.manifest()["direct_dependencies"])
        self.assertEqual(418+len(b.OWN),b.manifest()["source_pins"])
        self.assertEqual(697+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),b.manifest()["protected_inputs"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
