"""C283 behavioral fixtures; real parent artifacts and neural path are runtime gates."""
import ast
import contextlib
import copy
import hashlib
import io
import itertools
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c283_frozen_four_character_transfer as b


def logical_data():
    out={s:[] for s in b.SPLITS}
    for entities,values,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if values in ((0,2),(1,3),(2,0),(3,1)) else "TRAIN"
        for perm,query in itertools.product((entities,entities[::-1]),entities):
            out[split].append(dict(id=f"{lang}:{entities}:{values}:{perm}:{query}",entities=list(entities),values=list(values),
                                   language=lang,permutation=list(perm),query=query,target=48+values[entities.index(query)]))
    return out


def old_render(length):
    def render(r,p,v="normal"):
        i,j=r["entities"];chars=("a","b","c") if r["language"]=="en" else ("甲","乙","丙");u,w=chars[i],chars[j]
        ns={i:u*length,j:w*length if p in ("doubled","tripled") else u*(length-1)+w if "prefix" in p else w+u*(length-1)}
        values=dict(zip(r["entities"],r["values"],strict=True))
        return ";".join(ns[k]+"="+("?" if v=="evidence_blind" else str(values[k])) for k in r["permutation"])+";"+("?" if v=="query_blind" else ns[r["query"]])+"="
    return render


def prefix(raw):
    if len(raw)>46: raise ValueError("overflow")
    return torch.tensor([257]+list(raw)+[258]+[256]*(46-len(raw)),dtype=torch.int64)


def check_logits(x,n):
    if x.shape!=(n,256) or x.dtype!=torch.float64 or not bool(torch.isfinite(x).all()): raise ValueError("logits")


def raw_fixture(data):
    raw={}
    for s in b.SPLITS:
        raw[s]={}
        for p in b.PROFILE_MAP:
            raw[s][p]={}
            for v in b.VIEWS:
                y=torch.zeros((len(data[s]),256),dtype=torch.float64)
                labels=[r["target"] if v=="normal" else 0 for r in data[s]]
                y[torch.arange(len(y)),torch.tensor(labels)]=1
                raw[s][p][v]=y
    return raw


def score_fixture(data,raw,p267):
    # An independent simple scorer fixture; production uses the pinned C270 scorer.
    totals=[];cells=[];orders=[];passed=True
    for s in b.SPLITS:
        for p,views in raw[s].items():
            for v,y in views.items(): check_logits(y,len(data[s]))
            pred=views["normal"].argmax(-1).tolist()
            for lang in ("en","ja"):
                ids=[i for i,r in enumerate(data[s]) if r["language"]==lang]
                correct=sum(pred[i]==data[s][i]["target"] for i in ids)
                good=correct==len(ids);passed &= good
                totals.append(dict(split=s,profile=p,language=lang,rows=len(ids),pairs=len(ids)//2,correct=correct,collapsed_pairs=0))
                cells.append(dict(split=s,profile=p,language=lang,passed=good))
                orders.append(dict(split=s,profile=p,language=lang,passed=good))
    return dict(cells=cells,two_order=orders,totals=totals,passed=bool(passed))


class Audit:
    @staticmethod
    def sha(p):
        p=Path(p); return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch": return b"feat/sft-target-loss\n"
        return b""
    @staticmethod
    def read_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n): return Path(root)/n


def fingerprint(model):
    return hashlib.sha256(b"".join(x.detach().cpu().numpy().tobytes() for x in model.state_dict().values())).hexdigest()


def fixture_context():
    def valid(data):
        if b.digest(data)!=b.PARENT_ARTIFACTS["dataset.json"][0]: raise ValueError("logical identity")
    p267=NS(validate_data=valid,render=old_render(2),PROFILES=("doubled","shared_prefix","shared_suffix"),
            check_logits=check_logits,dataset=logical_data)
    c270=NS(render=old_render(3),PROFILES=("tripled","shared_prefix2","shared_suffix2"),score=score_fixture,
            replay_old=lambda a,r,d,p:0.,validate_dataset=lambda *a:None)
    return NS(p267=p267,c270=c270,previous=NS(replay_triple=lambda *a:0.),factory=NS(prefix_tensor=prefix),
              base=NS(fingerprint=fingerprint),audit=Audit(),core=None)


def records_fixture():
    c=fixture_context();data=logical_data();raw=raw_fixture(data);anchor=dict(two_char={},triple={})
    refs=[dict(seed=s,arm=a,final_sha256="fixed",raw_two={},raw_triple={}) for s,a in b.identities()]
    rr=[dict(seed=s,arm=a,final_sha256="fixed",weights_preserved=True,model_forward_calls=135,row_presentations=12960,
             core_forward_calls=540,anchor_error=0.,restore_error=0.,anchor=anchor,restored=anchor,novel=raw) for s,a in b.identities()]
    return c,data,refs,rr


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<544:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(964)}


def result_fixture():
    c,d,refs,rr=records_fixture();_,s=b.analyze(rr,refs,d,c);pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
                source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,
                gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False)


class Model(torch.nn.Module):
    def __init__(self):super().__init__();self.weight=torch.nn.Parameter(torch.zeros(14256,dtype=torch.float64));self.calls=[]
    def forward(self,x,t):
        self.calls.append(len(x));return self.weight[:256].expand(len(x),-1)


class C283Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.threads=torch.get_num_threads();torch.set_num_threads(2)
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads)

    def test_01_real_seal_and_dataset_hash(self):
        b.validate_seal();self.assertEqual(b.digest(b.dataset(logical_data())),b.QUAD_SHA)

    def test_02_bad_seals_rejected(self):
        for seal in ("UNSEALED","F"*64,"0"*64):
            with patch.object(b,"MANIFEST_SHA",seal),self.assertRaises(ValueError):b.validate_seal()

    def test_03_all_names_four_characters_and_distinct(self):
        for rows in logical_data().values():
            for row in rows:
                for p in b.PROFILE_MAP:
                    names=list(b.names(row,p).values());self.assertEqual(list(map(len,names)),[4,4]);self.assertNotEqual(*names)

    def test_04_exact_prefix_and_suffix(self):
        row=logical_data()["TRAIN"][0]
        self.assertEqual(list(b.names(row,"shared_prefix3").values()),["aaaa","aaab"])
        self.assertEqual(list(b.names(row,"shared_suffix3").values()),["aaaa","baaa"])

    def test_05_normal_views_preserve_values_and_query(self):
        r=logical_data()["TRAIN"][0];ns=b.names(r,"quadrupled")
        self.assertTrue(b.render(r,"quadrupled").endswith(";"+ns[r["query"]]+"="))
        self.assertNotIn("?",b.render(r,"quadrupled"))

    def test_06_masks_and_unknown_view(self):
        r=logical_data()["TRAIN"][0]
        self.assertEqual(b.render(r,"quadrupled","evidence_blind").count("?"),2)
        self.assertTrue(b.render(r,"quadrupled","query_blind").endswith(";?="))
        with self.assertRaises(ValueError):b.render(r,"quadrupled","other")

    def test_07_real_logical_hash_and_no_overlap(self):
        c=fixture_context();d=logical_data();b.validate_dataset(b.dataset(d),d,c)
        self.assertEqual(b.digest(d),b.PARENT_ARTIFACTS["dataset.json"][0])

    def test_08_japanese_fits_without_truncation(self):
        q=b.dataset(logical_data());lengths=[]
        for split in q.values():
            for rows in split.values():
                for r in rows:
                    for text in r["views"].values():
                        x=prefix(text.encode());self.assertEqual(len(x),48)
                        lengths.append(len(text.encode()))
        self.assertEqual(max(lengths),43)

    def test_09_dataset_tampering_rejected(self):
        c=fixture_context();d=logical_data();q=b.dataset(d);q["TRAIN"]["quadrupled"][0]["target"]+=1
        with self.assertRaises(ValueError):b.validate_dataset(q,d,c)

    def test_10_adapter_roundtrip_profiles(self):
        c,d,_,rr=records_fixture();c.c270.score=Mock(wraps=score_fixture)
        result=b.score_quad(d,rr[0]["novel"],c)
        self.assertIs(c.c270.score.call_args.args[0],d)
        for split in b.SPLITS:
            for new,old in b.PROFILE_MAP.items():
                self.assertIs(c.c270.score.call_args.args[1][split][old],rr[0]["novel"][split][new])
        for field in ("cells","two_order","totals"):
            self.assertEqual({r["profile"] for r in result[field]},set(b.PROFILE_MAP))
        self.assertTrue(result["passed"])

    def test_11_adapter_does_not_mutate_source_scorer_result(self):
        c,d,_,rr=records_fixture();saved=score_fixture(d,{s:{v:rr[0]["novel"][s][k] for k,v in b.PROFILE_MAP.items()} for s in b.SPLITS},c.p267)
        orig=copy.deepcopy(saved);c.c270.score=lambda *a:saved;b.score_quad(d,rr[0]["novel"],c)
        self.assertEqual(saved,orig)

    def test_12_adapter_missing_profile_rejected(self):
        c,d,_,rr=records_fixture();r=copy.deepcopy(rr[0]["novel"]);r["TRAIN"].pop("quadrupled")
        with self.assertRaises(ValueError):b.score_quad(d,r,c)

    def test_13_evaluation_runs_exact_27_forwards(self):
        c=fixture_context();d=logical_data();m=Model();raw=b.evaluate_quad(m,b.dataset(d),d,c)
        self.assertEqual((len(m.calls),sum(m.calls)),(27,2592));self.assertEqual(set(raw),set(b.SPLITS))
        self.assertFalse(any(y.requires_grad for r in raw.values() for p in r.values() for y in p.values()))

    def test_14_probe_phase_order_and_frozen_guard(self):
        c,d,refs,_=records_fixture();m=Model().eval();m.requires_grad_(False);refs[0]["final_sha256"]=fingerprint(m);events=[]
        @contextlib.contextmanager
        def counted(*a):yield [135,12960],[540]
        c.p267.counted=counted
        with patch.object(b,"evaluate_anchor",side_effect=lambda *a:(events.append("anchor") or dict(two_char={},triple={}))),\
             patch.object(b,"evaluate_quad",side_effect=lambda *a:(events.append("quad") or {})):
            b.frozen_probe(m,refs[0],d,{}, {},c)
        self.assertEqual(events,["anchor","quad","anchor"])
        m.train()
        with self.assertRaisesRegex(ValueError,"frozen model"):b.frozen_probe(m,refs[0],d,{}, {},c)

    def test_15_analyze_all_states_and_contrasts(self):
        c,d,refs,rr=records_fixture();metrics,s=b.analyze(rr,refs,d,c)
        self.assertEqual((len(metrics),len(s["contrasts"])),(10,60));self.assertEqual(s["seed_pass_counts"],dict.fromkeys(b.ARMS,5))

    def test_16_no_seed_selection(self):
        c,d,refs,rr=records_fixture();rr.pop()
        with self.assertRaisesRegex(ValueError,"model identities"):b.analyze(rr,refs,d,c)

    def test_17_weight_and_count_mismatch_rejected(self):
        for key,value in (("weights_preserved",False),("final_sha256","bad"),("model_forward_calls",134)):
            c,d,refs,rr=records_fixture();rr[0][key]=value
            with self.assertRaises(ValueError):b.analyze(rr,refs,d,c)

    def test_18_replay_nonfinite_or_drift_rejected(self):
        for error in (float("nan"),float("inf"),1e-5):
            c,d,refs,rr=records_fixture();rr[0]["anchor_error"]=error
            with self.assertRaises(ValueError):b.analyze(rr,refs,d,c)

    def test_19_control_cannot_fail_candidate(self):
        p=result_fixture();s=p["validation_summary"];s["seed_results"][0]["passed"]=False;s["seed_pass_counts"][b.ARMS[0]]=4
        b.validate_result(p)

    def test_20_one_candidate_failure_requires_negative(self):
        p=result_fixture();s=p["validation_summary"];s["seed_results"][1]["passed"]=False;s["seed_pass_counts"][b.ARMS[1]]=4
        with self.assertRaises(ValueError):b.validate_result(p)
        s["candidate_gate"]=False;p["status"]="FAIL";b.validate_result(p)

    def test_21_no_training_or_gate_f_claim(self):
        for key in ("train_steps","new_checkpoint_writes"):
            p=result_fixture();p["validation_summary"][key]=1
            with self.assertRaises(ValueError):b.validate_result(p)
        p=result_fixture();p["gate_f_candidate"]=True
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_22_all_nine_hashes_checked_before_parent(self):
        paths=[Path(str(i)).resolve() for i in range(9)];mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        c=NS(audit=NS(sha=lambda p:mapping[str(p)]));parent=NS(verify_artifacts=Mock())
        for p in paths:
            old=mapping[str(p)];mapping[str(p)]="0"*64
            with patch.object(b,"context",return_value=(parent,c)),self.assertRaises(ValueError):b.load_parent(paths)
            parent.verify_artifacts.assert_not_called();mapping[str(p)]=old

    def test_23_parent_dispatch_and_neural_block(self):
        paths=[Path(str(i)).resolve() for i in range(9)];mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        c=NS(audit=NS(sha=lambda p:mapping[str(p)]));parent=NS(verify_artifacts=Mock(side_effect=lambda *a:torch.nn.Identity()(torch.ones(1))))
        with patch.object(b,"context",return_value=(parent,c)),self.assertRaisesRegex(RuntimeError,"forbids neural"):b.load_parent(paths)
        parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_24_missing_parent_pin_and_boolean_counts(self):
        p=result_fixture();del p["source_blobs"][b.PARENT_SOURCE]
        with self.assertRaises(ValueError):b.validate_result(p)
        p=result_fixture();p["validation_summary"]["new_checkpoint_writes"]=False
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_25_real_suite_filter(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
            self.assertEqual(suite.countTestCases(),b.manifest()["focused_tests"])

    def test_26_real_run_checkpoint_dispatch_and_persistence(self):
        c,d,refs,rr=records_fixture();events=[]
        parent=NS(load_bundle=Mock(return_value=[Model().state_dict() for _ in range(10)]),make_models=lambda *a:{arm:Model() for arm in b.ARMS})
        def probe(m,r,*a):
            self.assertFalse(m.training);self.assertFalse(any(p.requires_grad for p in m.parameters()));events.append(r["seed"])
            return rr[b.identities().index((r["seed"],r["arm"]))]
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(parent,c)),\
             patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},refs,d,{})),\
             patch.object(b,"frozen_probe",side_effect=probe),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*9,output_dir=out,expected_head="f"*40)
            parent.load_bundle.assert_called_once();self.assertEqual(events,[s for s,a in b.identities()])
            q,_=b.verify_artifacts(out,["x"]*9,"f"*40);self.assertEqual(q,p)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*9,output_dir=out,expected_head="f"*40)

    def test_27_artifact_tampering_rejected(self):
        c,d,refs,rr=records_fixture();parent=NS(load_bundle=lambda p:[Model().state_dict() for _ in range(10)],make_models=lambda *a:{arm:Model() for arm in b.ARMS})
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(parent,c)),patch.object(b,"precheck",return_value=protection()),\
             patch.object(b,"load_parent",return_value=({},refs,d,{})),patch.object(b,"frozen_probe",side_effect=rr),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";b.run(summaries=["x"]*9,output_dir=out,expected_head="f"*40)
            (out/"quad-dataset.json").write_text("{}")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*9,"f"*40)

    def test_28_cli_order(self):
        args=["prog","--summaries"]+[str(i) for i in range(9)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",args),patch.object(b,"run") as run:
            b.main();self.assertEqual(run.call_args.kwargs["summaries"],[Path(str(i)) for i in range(9)])

    def test_29_runner_blocks_and_publication_order(self):
        root=Path(__file__).resolve().parents[1];r=(root/"tools/run_c283.ps1").read_text(encoding="utf-8");l=(root/"tools/invoke_c283.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",r,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:11]",blocks[2]);self.assertIn("head = sys.argv[11]",blocks[2])
        self.assertLess(l.index("-Mode Validate"),l.index("-Mode Execute"));self.assertLess(l.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),l.index("publish_experiment_log.ps1"))
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',l)),9)

    def test_30_only_direct_parent_import_and_protection_counts(self):
        tree=ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        imports=[n for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c282_mixed_length_training"])
        self.assertEqual(b.manifest()["source_pins"],538+len(b.OWN));self.assertEqual(b.manifest()["protected_inputs"],950+8+len(b.OWN))

    def test_31_anchor_replay_is_not_optional(self):
        c,d,refs,rr=records_fixture();c.c270.replay_old=Mock(side_effect=ValueError("anchor changed"))
        with self.assertRaisesRegex(ValueError,"anchor changed"):b.analyze(rr,refs,d,c)

    def test_32_immutable_preregistration_inventory(self):
        root=Path(__file__).resolve().parents[1]
        self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])
        for n in b.OWN:self.assertTrue((root/n).is_file())


if __name__=="__main__":unittest.main()
