"""C265 tests use the real C264 scorer and an explicitly synthetic parser oracle."""
import ast
import contextlib
import copy
import hashlib
import inspect
import io
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock,patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c264_two_fact_deletion as parent
from fold_lm.v05_benchmarks import model_c265_compound_identifiers as b


class Oracle(nn.Module):
    """String parsing with placeholder parameters is NOT a learned FOLD model."""
    def __init__(self,seed,arm=0,strategy="exact"):
        super().__init__(); self.marker=nn.Parameter(torch.zeros(14256,dtype=torch.float64))
        with torch.no_grad(): self.marker[0]=seed+arm/10
        self.backbone=nn.Module(); self.backbone.core=nn.Identity(); self.strategy=strategy
        self.eval().requires_grad_(False)
    def forward(self,tokens,tasks):
        logits=torch.full((len(tokens),256),-10.,dtype=torch.float64)
        for i,token_row in enumerate(tokens.tolist()):
            fields=bytes(x for x in token_row if x<256).decode().split(";")
            pairs=[x.split("=") for x in fields[:-1]]; query=fields[-1][:-1]
            convert=lambda name:name[:1] if self.strategy=="first" else name[-1:] if self.strategy=="last" else name
            facts={convert(k):v for k,v in pairs}
            value=facts.get(convert(query),pairs[0][1]); value="0" if value=="?" else value
            logits[i,ord(value)]=10.
        for _ in range(4): logits=self.backbone.core(logits)
        return logits+self.marker[0]*0


class Factory:
    @staticmethod
    def new_model(seed): return Oracle(seed)
    @staticmethod
    def prefix_tensor(raw):
        b.require(len(raw)<=46,"prefix length")
        return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)


class Base:
    @staticmethod
    def make_model(model,arm,seed,aligned,reader):
        b.require(arm=="aligned_precore_read","architecture"); return model
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for k,v in sorted(model.state_dict().items()): h.update(k.encode()); h.update(v.detach().cpu().numpy().tobytes())
        return h.hexdigest()


class CoreCounter:
    @staticmethod
    def core_counter(model):
        count=[0]
        def hook(module,args,output): count[0]+=1
        return count,model.backbone.core.register_forward_hook(hook)


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("fixture-input-"): return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path): return __import__("json").loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):
        child=(Path(root)/name).resolve(); b.require(child.parent==Path(root).resolve(),"unsafe child"); return child
    @staticmethod
    def git(root,*args):
        if args==("rev-parse","HEAD"): return b"fixture-head"
        if args==("branch","--show-current"): return b"feat/sft-target-loss"
        return b""


def protection():
    return {**{f"old-{i}":"fixture" for i in range(430)},**{n:"fixture" for n in b.OWN}},{f"fixture-input-{i}":"0"*64 for i in range(736)}


class C265Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2); cls.rows=parent.dataset(); cls.data=b.dataset(cls.rows,parent)
        cls.models=[Oracle(s,b.ARMS.index(a)) for s,a in b.identities()]
        anchor=parent.evaluate_new(cls.models[0],cls.rows,Factory)
        renamed={p:b.evaluate_profile(cls.models[0],cls.data[p],Factory,parent) for p in b.PROFILES}
        cls.refs=[dict(seed=s,arm=a,final_sha256=Base.fingerprint(m),reduced=anchor) for (s,a),m in zip(b.identities(),cls.models,strict=True)]
        cls.records=[dict(seed=r["seed"],arm=r["arm"],final_sha256=r["final_sha256"],weights_preserved=True,
            model_forward_calls=30,row_presentations=4320,core_forward_calls=120,anchor_error=0.,restore_error=0.,
            anchor=anchor,renamed=renamed,restored=anchor) for r in cls.refs]

    def test_01_hash_and_registration(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA); self.assertEqual(b.digest(self.data),b.DATA_SHA)
        with contextlib.redirect_stdout(io.StringIO()):
            b.validate_registration(436,736)
            with self.assertRaises(ValueError): b.validate_registration(436,735)
            with patch.object(b,"MANIFEST_SHA","bad"),self.assertRaises(ValueError): b.validate_registration(436,736)

    def test_02_complete_unique_dataset_and_known_bytes(self):
        b.validate_dataset(self.data,self.rows,parent)
        self.assertEqual(sum(len(x) for x in self.data.values()),864)
        chars=set("abc甲乙丙=;?0123".encode())
        for items in self.data.values():
            for r in items:
                for text in r["views"].values(): self.assertTrue(set(text.encode())<=chars)

    def test_03_equal_lengths_and_profile_collisions(self):
        for r in self.rows:
            maps=[b.name_map(r,p) for p in b.PROFILES]; i,j=r["entities"]
            self.assertEqual(maps[1][i][0],maps[1][j][0]); self.assertNotEqual(maps[1][i][-1],maps[1][j][-1])
            self.assertEqual(maps[2][i][-1],maps[2][j][-1]); self.assertNotEqual(maps[2][i][0],maps[2][j][0])
            self.assertEqual(len({len(b.render(r,p).encode()) for p in b.PROFILES}),1)
            self.assertLessEqual(len(b.render(r,"shared_prefix").encode()),46)

    def test_04_consistent_fact_and_query_renaming(self):
        for r in self.rows:
            for p in b.PROFILES:
                parts=b.render(r,p).split(";"); facts=dict(x.split("=") for x in parts[:-1])
                self.assertEqual(ord(facts[parts[-1][:-1]]),r["target"])
                self.assertEqual(b.render(r,p,"evidence_blind").count("?"),2)
                self.assertTrue(b.render(r,p,"query_blind").endswith(";?="))

    def test_05_changed_metadata_or_bad_profile_rejected(self):
        data=copy.deepcopy(self.data); data["doubled"][0]["target"]=200
        with self.assertRaises(ValueError): b.validate_dataset(data,self.rows,parent)
        with self.assertRaises(ValueError): b.name_map(self.rows[0],"other")
        with self.assertRaises(ValueError): b.render(self.rows[0],"doubled","other")

    def test_06_actual_parent_scoring_perfect_profiles(self):
        m,s=b.analyze(self.records,self.refs,self.rows,parent)
        self.assertTrue(s["joint_gate"])
        self.assertEqual(s["profile_pass_counts"],{p:{a:5 for a in b.ARMS} for p in b.PROFILES})
        for score in m[0]["profiles"].values(): self.assertEqual((score["correct"],len(score["cells"]),len(score["two_order"])),(288,12,6))

    def test_07_first_character_shortcut_fails_shared_prefix(self):
        m=Oracle(b.SEEDS[0],strategy="first")
        doubled=b.evaluate_profile(m,self.data["doubled"],Factory,parent)
        prefix=b.evaluate_profile(m,self.data["shared_prefix"],Factory,parent)
        self.assertTrue(parent.score(self.rows,doubled)["passed"])
        self.assertFalse(parent.score(self.rows,prefix)["passed"])
        self.assertEqual(parent.score(self.rows,prefix)["correct"],144)

    def test_08_last_character_shortcut_fails_shared_suffix(self):
        m=Oracle(b.SEEDS[0],strategy="last")
        suffix=b.evaluate_profile(m,self.data["shared_suffix"],Factory,parent)
        self.assertFalse(parent.score(self.rows,suffix)["passed"])
        self.assertEqual(parent.score(self.rows,suffix)["correct"],144)

    def test_09_each_profile_and_each_arm_is_required(self):
        for profile in b.PROFILES:
            rr=list(self.records); r=dict(rr[3]); r["renamed"]=dict(r["renamed"])
            r["renamed"][profile]=dict(r["renamed"][profile],normal=torch.zeros_like(r["renamed"][profile]["normal"])); rr[3]=r
            _,s=b.analyze(rr,self.refs,self.rows,parent)
            self.assertFalse(s["joint_gate"]); self.assertEqual(s["profile_pass_counts"][profile][b.ARMS[3]],4)

    def test_10_parent_per_cell_threshold_not_pooled(self):
        raw={k:v.clone() for k,v in self.records[0]["renamed"]["doubled"].items()}
        ids=[i for i,r in enumerate(self.rows) if r["language"]=="en" and r["entities"]==[0,1] and r["permutation"]==[0,1]][:3]
        raw["normal"][ids]=0; m=parent.score(self.rows,raw)
        self.assertGreater(m["correct"]/288,.98); self.assertFalse(m["passed"])

    def test_11_mask_gates_retained(self):
        for view in ("evidence_blind","query_blind"):
            raw=dict(self.records[0]["renamed"]["doubled"]); raw[view]=raw["normal"]
            self.assertFalse(parent.score(self.rows,raw)["passed"])

    def test_12_raw_replay_tolerance_argmax_and_nonfinite(self):
        ref=self.refs[0]["reduced"]; raw={k:v.clone() for k,v in ref.items()}; raw["normal"]+=5e-10
        self.assertLessEqual(b.replay(raw,ref,parent),b.TOL)
        raw["normal"]+=2e-9
        with self.assertRaises(ValueError): b.replay(raw,ref,parent)
        raw={k:v.clone() for k,v in ref.items()}; raw["normal"][0,0]=float("nan")
        with self.assertRaises(ValueError): b.replay(raw,ref,parent)
        a={k:torch.zeros_like(v) for k,v in ref.items()}; c=copy.deepcopy(a); c["normal"][:,1]=5e-10
        with self.assertRaises(ValueError): b.replay(a,c,parent)

    def test_13_actual_probe_counts_and_checkpoint_identity(self):
        r=b.probe(self.models[2],self.refs[2],self.rows,self.data,parent,CoreCounter,Base,Factory)
        self.assertEqual((r["model_forward_calls"],r["row_presentations"],r["core_forward_calls"]),(30,4320,120))
        self.assertEqual(r["restore_error"],0.); self.assertEqual(r["final_sha256"],self.refs[2]["final_sha256"])

    def test_14_anchor_barrier_and_hook_cleanup(self):
        ref=copy.deepcopy(self.refs[0]); ref["reduced"]["normal"]+=1.
        with patch.object(b,"evaluate_profile") as new,self.assertRaisesRegex(ValueError,"replay"):
            b.probe(self.models[0],ref,self.rows,self.data,parent,CoreCounter,Base,Factory)
        new.assert_not_called(); self.assertFalse(self.models[0]._forward_hooks); self.assertFalse(self.models[0].backbone.core._forward_hooks)

    def test_15_frozen_mode_and_mutation_guard(self):
        m=copy.deepcopy(self.models[0]).train()
        with self.assertRaisesRegex(ValueError,"frozen"): b.probe(m,self.refs[0],self.rows,self.data,parent,CoreCounter,Base,Factory)
        m.eval()
        def mutate(module,args,out):
            with torch.no_grad(): module.marker[0]+=1
        h=m.register_forward_hook(mutate)
        try:
            with self.assertRaisesRegex(ValueError,"mutation"): b.probe(m,self.refs[0],self.rows,self.data,parent,CoreCounter,Base,Factory)
        finally: h.remove()

    def test_16_saved_identity_count_and_restoration_guards(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.refs,self.rows,parent)
        for k,v in (("weights_preserved",False),("core_forward_calls",0),("restore_error",float("nan"))):
            rr=list(self.records); rr[0]=dict(rr[0],**{k:v})
            with self.assertRaises(ValueError): b.analyze(rr,self.refs,self.rows,parent)

    def test_17_reference_loader_three_argument_dispatch(self):
        p=dict(commit_sha=b.PARENT_EXECUTION,status="PASS",validation_summary={"seed_pass_counts":{a:5 for a in b.ARMS}},artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        metrics=[dict(seed=r["seed"],arm=r["arm"],**parent.score(self.rows,r["reduced"])) for r in self.refs]
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); s=root/"summary.json"; ms=root/"model-source.json"; s.write_bytes(b"parent"); ms.write_bytes(b"source")
            (root/"two-fact-dataset.json").write_bytes(b.blob(self.rows)); torch.save(dict(schema="fold-c264-deletion-eval-v1",records=self.refs),root/"eval-outputs.pt")
            with patch.object(b,"context",return_value=(parent,None,None,None,None,None,Factory,Audit)),patch.object(b,"PARENT_SHA",Audit.sha(s)),patch.object(b,"MODEL_SOURCE_SHA",Audit.sha(ms)),patch.object(parent,"validate_result"),patch.object(parent,"verify_artifacts",return_value=(p,metrics)) as verify:
                rows,refs=b.load_reference(s,ms); self.assertEqual(rows,self.rows); self.assertEqual(len(refs),20)
                verify.assert_called_once_with(root,ms,b.PARENT_EXECUTION)
                p["status"]="FAIL"
                with self.assertRaises(ValueError): b.load_reference(s,ms)

    def test_18_saved_reference_metrics_semantics(self):
        source=inspect.getsource(b.load_reference)
        self.assertIn('r["reduced"]',source); self.assertIn('parent.score(rows',source)
        self.assertNotIn('r["anchor"]',source)
        self.assertEqual(list(inspect.signature(parent.verify_artifacts).parameters),["output_dir","c263_summary","expected_head"])

    def test_19_actual_twenty_state_run_and_saved_postcheck(self):
        source=SimpleNamespace(load_bundle=Mock(return_value=[m.state_dict() for m in self.models]))
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(parent,source,CoreCounter,Base,None,None,Factory,Audit)),patch.object(b,"precheck",return_value=protection()) as pre,patch.object(b,"load_reference",return_value=(self.rows,self.refs)) as load:
            root=Path(d); out=root/"out"
            with contextlib.redirect_stdout(io.StringIO()): p=b.run(c264_summary=root/"p264",c263_summary=root/"p263",output_dir=out,expected_head="fixture-head")
            self.assertEqual(pre.call_count,2); self.assertEqual(load.call_count,1); source.load_bundle.assert_called_once()
            with patch.object(Factory,"new_model",side_effect=AssertionError("no saved-postcheck model")),patch.object(b,"probe",side_effect=AssertionError("no saved-postcheck inference")):
                self.assertEqual(b.verify_artifacts(out,root/"p264",root/"p263","fixture-head")[0],p)
            self.assertEqual(load.call_count,2); source.load_bundle.assert_called_once()
            with self.assertRaisesRegex(ValueError,"saved HEAD"): b.verify_artifacts(out,root/"p264",root/"p263","bad")
            (out/"identifier-dataset.json").write_bytes(b"{}")
            with self.assertRaises(ValueError): b.verify_artifacts(out,root/"p264",root/"p263","fixture-head")

    def test_20_source_no_training_and_real_call_order(self):
        source=ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        for n in ast.walk(source):
            if isinstance(n,ast.Call):
                name=n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else ""
                self.assertNotIn(name,{"AdamW","backward","fit","train_one","step"})
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first=lambda name:min(line for line,n in calls if n==name)
        for a,c in (("precheck","load_reference"),("load_reference","load_bundle"),("load_bundle","probe"),("probe","analyze")): self.assertLess(first(a),first(c))

    def test_21_runner_cli_indices_and_parser_order(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/"tools/run_c265.ps1").read_text(encoding="utf-8"); launcher=(root/"tools/invoke_c265.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3); indices=[]
        for text in blocks:
            compile(text,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"})
        self.assertEqual(indices,[{1,2},set(),{1,2,3,4}]); failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher)
        self.assertIsNotNone(failure); self.assertLess(launcher.index("::ParseFile"),failure.start()); self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        self.assertIn("46c2297b66ba41a9b8f66f7bfca48935",launcher); self.assertIn("638f26dfee354c9cb3aa5fa174d3e9f6",launcher)

    def test_22_semantic_own_count_and_exact_exclusion(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases(),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name): super().__init__(); self.name=name
            def id(self): return self.name
        suite=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture-{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_23_dependency_and_model_source_protection(self):
        tree=ast.parse(inspect.getsource(b.precheck)); pattern=next(n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="pattern" for t in n.targets))
        names=["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,265)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names)); self.assertEqual(5+len(names)+1,b.manifest()["direct_dependencies"])
        self.assertIn('protected.get(str(source)) == MODEL_SOURCE_SHA',inspect.getsource(b.precheck))
        self.assertEqual(723+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),736)

    def test_24_resource_and_gate_accounting(self):
        _,s=b.analyze(self.records,self.refs,self.rows,parent); pins,protected=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",source_blobs=pins,input_sha256=protected,
            artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False,arbitrary_name_claim=False,causal_parser_claim=False,network_calls=0)
        b.validate_result(p); self.assertEqual(86400*256*8,b.manifest()["logit_payload_bytes"])
        with self.assertRaises(ValueError): b.validate_result(dict(p,causal_parser_claim=True))
        s["profile_pass_counts"]["doubled"][b.ARMS[0]]=4
        with self.assertRaises(ValueError): b.validate_result(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
