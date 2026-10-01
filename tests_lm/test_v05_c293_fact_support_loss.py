"""Behavioral C293 fixtures; authoritative FOLD execution is a separate runtime gate."""
import ast
from collections import Counter
import contextlib
import copy
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import re
import sys
import tempfile
import types
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock,patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c293_fact_support_loss as b


def dataset():
    data={"TRAIN":[],"HOLDOUT":[]}
    for e,v,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for order,q in itertools.product((e,e[::-1]),e):
            data[split].append(dict(id=str((lang,e,v,order,q)),language=lang,entities=list(e),values=list(v),permutation=list(order),query=q,target=48+v[e.index(q)]))
    return data


def tables(data):
    y=torch.tensor([r["target"] for r in data["TRAIN"]]);x=torch.zeros((2,3,192,48),dtype=torch.int64)
    x[:,:,:,0]=y-48
    return x,y


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__();self.backbone=torch.nn.Embedding(4,4,dtype=torch.float64);self.read=torch.nn.Linear(4,256,dtype=torch.float64)
        self.calls=self.rows=0
    def forward(self,tokens,tasks):
        assert tokens.shape==(len(tokens),48) and tasks.shape==(len(tokens),) and not bool(tasks.any())
        self.calls+=1;self.rows+=len(tokens)
        return self.read(self.backbone(tokens[:,0]))


def fingerprint(m):return b.digest({k:v.detach().tolist() for k,v in m.state_dict().items()})


def fit_fixture(seed,arm,data):
    total=2. if arm==b.ARMS[0] else 2.5 if arm==b.ARMS[1] else 2.25
    return dict(steps=800,training_rows=38400,optimizer_creations=1,last_ce=2.,ce_history=[2.]*800,support_history=[1.]*800,
                choice_history=[1.]*800,total_history=[total]*800,applied_lr=[.005]*800,**b.schedule(seed,data["TRAIN"])[3])


def records_fixture():
    data=dataset();zs={}
    for split,rows in data.items():
        z=torch.zeros((len(rows),256),dtype=torch.float64);z[torch.arange(len(rows)),torch.tensor([r["target"] for r in rows])]=4.;zs[split]=z
    records=[]
    for seed,arm in b.identities():
        raw={t:{s:{str(p):{v:zs[s] for v in ("normal","evidence_blind","query_blind")} for p in range(3)} for s in data} for t in b.TASKS}
        records.append(dict(seed=seed,arm=arm,parameters=14256,initial_sha256="a"*64,final_sha256="b"*64,weights_changed=True,checkpoint_roundtrip=True,reload_max_error=0.,
                            fit=fit_fixture(seed,arm,data),raw=raw,forward_calls=881,row_presentations=46176,core_forward_calls=3524,
                            replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    return records,data


def role(row,p):
    target=row["target"];other=48+row["values"][1-row["entities"].index(row["query"])]
    return dict(role="target" if p==target else "other_fact" if p==other else "absent_known_value" if 48<=p<=51 else "non_value_byte")


def tally(rows):
    counts=Counter(r["role"] for r in rows)
    return dict(rows=len(rows),correct=counts["target"],role_counts={k:counts[k] for k in ("target","other_fact","absent_known_value","non_value_byte")})


def scorers(data):
    def score(data,raw):
        totals=[]
        for split,profiles in raw.items():
            for profile,views in profiles.items():
                preds=views["normal"].argmax(1).tolist()
                for lang in ("en","ja"):
                    ii=[i for i,r in enumerate(data[split]) if r["language"]==lang]
                    correct=sum(preds[i]==data[split][i]["target"] for i in ii)
                    totals.append(dict(split=split,profile=profile,language=lang,rows=len(ii),pairs=len(ii)//2,correct=correct,collapsed_pairs=0))
        return dict(passed=all(r["correct"]==r["rows"] for r in totals),totals=totals)
    parent=NS(answer_role=role,tally=tally,no_neural=contextlib.nullcontext)
    diagnostic=NS(normalize_task=lambda s,*_:s["totals"],partition=lambda rows:dict(rows=sum(r["rows"] for r in rows),correct=sum(r["correct"] for r in rows),direct_pass=all(r["correct"]==r["rows"] for r in rows)))
    transfer=NS(score_quad=lambda data,raw,c:score(data,raw))
    c=NS(p267=NS(score=score),c270=NS(score=lambda data,raw,p:score(data,raw)))
    return parent,diagnostic,transfer,c


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<604:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1091)}


class Audit:
    @staticmethod
    def sha(p):
        p=Path(p);return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(p):return json.loads(Path(p).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n):return Path(root)/n
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse":return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch":return b"feat/sft-target-loss\n"
        return b""


def result_fixture(summary):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if summary["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
                source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,
                gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False)


def example():
    z=torch.zeros((2,256),dtype=torch.float64);z[0,48]=2.;z[1,49]=3.
    return z,torch.tensor([48,49])


class C293Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.det=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
        cls.data=dataset();cls.x,cls.y=tables(cls.data);torch.manual_seed(73);cls.initial=Toy();cls.models=[];cls.fits=[]
        with contextlib.redirect_stdout(io.StringIO()):
            for arm in b.ARMS:
                m=copy.deepcopy(cls.initial);cls.fits.append(b.fit(m,cls.data,cls.x,cls.y,b.SEEDS[0],arm));cls.models.append(m)
        cls.records,_=records_fixture();cls.metrics,cls.summary=b.analyze(cls.records,cls.data,*scorers(cls.data))
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads);torch.use_deterministic_algorithms(cls.det)

    def test_01_real_seal(self):b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seals(self):
        for h in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",h),self.assertRaises(ValueError):b.validate_seal()

    def test_03_uniform_closed_form(self):
        z=torch.zeros((2,256),dtype=torch.float64);y=torch.tensor([48,49])
        _,ce,s,q=b.objective(z,y,b.ARMS[0])
        self.assertAlmostEqual(float(ce),math.log(256));self.assertAlmostEqual(float(s),math.log(128));self.assertAlmostEqual(float(q),math.log(2))

    def test_04_ce_and_scaled_gradients(self):
        z,y=example();z.requires_grad_()
        for arm,scale in ((b.ARMS[0],1.),(b.ARMS[1],1.25)):
            v=b.objective(z,y,arm)[0];ref=scale*F.cross_entropy(z,y)
            self.assertTrue(torch.equal(v,ref));self.assertTrue(torch.equal(torch.autograd.grad(v,z)[0],torch.autograd.grad(ref,z)[0]))

    def test_05_candidate_decomposition_gradient(self):
        z,y=example();z.requires_grad_();v,ce,s,q=b.objective(z,y,b.ARMS[2])
        self.assertAlmostEqual(float(v.detach()),float((1.25*s+q).detach()))
        self.assertTrue(torch.allclose(torch.autograd.grad(v,z,retain_graph=True)[0],torch.autograd.grad(1.25*s+q,z)[0],atol=1e-12,rtol=1e-12))

    def test_06_support_does_not_choose_correct_fact(self):
        z,y=example();z[:]=-10.;z[0,49]=20.;z[1,48]=20.
        _,ce,s,q=b.objective(z,y,b.ARMS[2]);self.assertLess(float(s),1e-8);self.assertGreater(float(q),29.);self.assertGreater(float(ce),29.)

    def test_07_unsupported_winner_gradient(self):
        z,y=example();z[:,70]=8.;z.requires_grad_();s=b.objective(z,y,b.ARMS[2])[2];g=torch.autograd.grad(s,z)[0]
        self.assertTrue(bool((g[:,70]>0).all()));self.assertTrue(bool((g[:,[48,49]]<0).all()))

    def test_08_offsets_and_class_permutation(self):
        z,y=example()
        for a,c in zip(b.objective(z,y,b.ARMS[2]),b.objective(z+torch.tensor([[20.],[-10.]]),y,b.ARMS[2]),strict=True):self.assertAlmostEqual(float(a),float(c))
        perm=torch.arange(255,-1,-1)
        for a,c in zip(b.objective(z,y,b.ARMS[2]),b.objective(z[:,perm],255-y,b.ARMS[2]),strict=True):self.assertAlmostEqual(float(a),float(c))

    def test_09_pair_order_symmetry(self):
        z,y=example()
        for a,c in zip(b.objective(z,y,b.ARMS[2]),b.objective(z.flip(0),y.flip(0),b.ARMS[2]),strict=True):self.assertEqual(a,c)

    def test_10_finite_differences(self):
        z,y=example();z.requires_grad_();g=torch.autograd.grad(b.objective(z,y,b.ARMS[2])[0],z)[0]
        for i,j in ((0,48),(0,49),(0,70),(1,48),(1,49)):
            plus=z.detach().clone();minus=plus.clone();plus[i,j]+=1e-6;minus[i,j]-=1e-6
            v=(b.objective(plus,y,b.ARMS[2])[0]-b.objective(minus,y,b.ARMS[2])[0])/(2e-6)
            self.assertAlmostEqual(float(v),float(g[i,j]),places=7)

    def test_11_nonfinite_rejected(self):
        for v in (float("nan"),float("inf")):
            z,y=example();z[0,0]=v
            with self.assertRaises(ValueError):b.objective(z,y,b.ARMS[0])

    def test_12_shapes_and_labels(self):
        z,y=example()
        for a,c in ((z.float(),y),(z[:1],y[:1]),(z[:,:255],y),(z,y.float()),(z,torch.tensor([48,48])),(z,torch.tensor([-1,49]))):
            with self.assertRaises(ValueError):b.objective(a,c,b.ARMS[0])
        with self.assertRaises(ValueError):b.objective(z,y,"answer_margin")

    def test_13_exposure_and_seed_schedules(self):
        hashes=[]
        for seed in b.SEEDS:
            x,p,l,plan=b.schedule(seed,self.data["TRAIN"])
            self.assertEqual(x.shape,(800,48));self.assertEqual(plan["per_length_row_exposures"],[[100]*192]*2);hashes.append(plan["logical_batch_sha256"])
        self.assertEqual(len(set(hashes)),5)

    def test_14_pair_fact_support_exact(self):
        x,*_=b.schedule(b.SEEDS[0],self.data["TRAIN"])
        for ids in x.tolist():
            for i,j in zip(ids[::2],ids[1::2],strict=True):
                a,c=self.data["TRAIN"][i],self.data["TRAIN"][j]
                self.assertEqual({a["target"],c["target"]},{48+v for v in a["values"]})
                for k in ("language","entities","values","permutation"):self.assertEqual(a[k],c[k])

    def test_15_schedule_rejects_wrong_pairing(self):
        for fn in (lambda r:r.pop(),lambda r:r[1].update(query=r[0]["query"]),lambda r:r[1].update(target=88)):
            rows=copy.deepcopy(self.data["TRAIN"]);fn(rows)
            with self.assertRaises(ValueError):b.schedule(b.SEEDS[0],rows)

    def test_16_real_800_step_fixture(self):
        for arm,m,f in zip(b.ARMS,self.models,self.fits,strict=True):
            b.check_fit(f,b.SEEDS[0],arm,self.data);self.assertEqual((m.calls,m.rows),(800,38400))
            self.assertFalse(m.training);self.assertLess(f["last_ce"],f["ce_history"][0]);self.assertNotEqual(fingerprint(m),fingerprint(self.initial))

    def test_17_fit_reproducibility(self):
        m=copy.deepcopy(self.initial)
        with contextlib.redirect_stdout(io.StringIO()):f=b.fit(m,self.data,self.x,self.y,b.SEEDS[0],b.ARMS[2])
        self.assertEqual(f,self.fits[2]);self.assertEqual(fingerprint(m),fingerprint(self.models[2]))

    def test_18_trace_tampering(self):
        for fn in (lambda f:f["support_history"].__setitem__(0,99.),lambda f:f["total_history"].__setitem__(3,9.),lambda f:f["applied_lr"].__setitem__(1,.01),lambda f:f.update(optimizer_creations=2)):
            f=copy.deepcopy(self.fits[2]);fn(f)
            with self.assertRaises(ValueError):b.check_fit(f,b.SEEDS[0],b.ARMS[2],self.data)

    def test_19_target_alignment(self):
        y=self.y.clone();y[0]=90
        with self.assertRaises(ValueError):b.fit(copy.deepcopy(self.initial),self.data,self.x,y,b.SEEDS[0],b.ARMS[0])

    def test_20_model_factory(self):
        class Fake(torch.nn.Module):
            def __init__(self,*_):super().__init__();self.weight=torch.nn.Parameter(torch.ones(14256,dtype=torch.float64))
        c=NS(c278=NS(MeanFinalDualReadout=Fake),factory=NS(new_model=lambda _:None),reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))
        models=b.make_models(b.SEEDS[0],c);self.assertEqual(len({m.weight.data_ptr() for m in models.values()}),3)
        with self.assertRaises(ValueError):b.make_models(1,c)

    def test_21_train_one_frozen_order_and_workload(self):
        m=copy.deepcopy(self.initial)
        @contextlib.contextmanager
        def counted(model,core):
            calls=[0,0];cores=[0];yield calls,cores;calls[:]=[model.calls,model.rows];cores[0]=model.calls*4
        def evaluate(model,*_):
            self.assertFalse(model.training);self.assertFalse(any(p.requires_grad for p in model.parameters()))
            with torch.no_grad():
                for _ in range(81):model(torch.zeros((96,48),dtype=torch.int64),torch.zeros(96,dtype=torch.int64))
            return {}
        c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted),core=None)
        with contextlib.redirect_stdout(io.StringIO()):r,_=b.train_one(m,self.data,{},{},self.x,self.y,b.SEEDS[0],b.ARMS[0],NS(evaluate=evaluate),None,c)
        self.assertEqual((r["forward_calls"],r["row_presentations"],r["core_forward_calls"]),(881,46176,3524))

    def test_22_group_guards(self):
        g=copy.deepcopy(self.records[:3]);b.check_group(g);g[1]["fit"]["support_history"][0]+=1
        with self.assertRaises(ValueError):b.check_group(g)

    def test_23_complete_analysis(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["contrasts"])),(15,90,360))
        self.assertTrue(self.summary["candidate_gate"])
        for p in self.summary["final_partitions"]:self.assertEqual(p["output_role_counts"]["target"],p["rows"])

    def test_24_one_candidate_miss_is_negative(self):
        r=copy.deepcopy(self.records);view=r[2]["raw"]["quad"]["HOLDOUT"]["0"];view["normal"]=view["normal"].clone();view["normal"][0,88]=20.
        _,s=b.analyze(r,self.data,*scorers(self.data));self.assertFalse(s["candidate_gate"]);self.assertEqual(s["quad_pass_counts"][b.ARMS[2]],4)
        b.validate_result(result_fixture(s))

    def test_25_replay_and_roles_reconstruction(self):
        r=copy.deepcopy(self.records);r[0]["reload_max_error"]=.1
        with self.assertRaises(ValueError):b.analyze(r,self.data,*scorers(self.data))
        parent,diag,transfer,c=scorers(self.data);parent.tally=lambda obs:dict(rows=len(obs),correct=0,role_counts={})
        with self.assertRaisesRegex(ValueError,"role/score"):b.analyze(self.records,self.data,parent,diag,transfer,c)

    def test_26_result_contract(self):
        b.validate_result(result_fixture(self.summary))
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p["source_blobs"].pop(b.PARENT_SOURCE),lambda p:p["validation_summary"].update(train_steps=False),lambda p:p["validation_summary"]["final_partitions"].pop()):
            p=result_fixture(copy.deepcopy(self.summary));fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    @contextlib.contextmanager
    def parent_fixture(self):
        paths=[(Path("/c293-fixture")/str(i)/"summary.json").resolve() for i in range(19)]
        old=(NS(PARENT_SHA="d"*64),NS(SUMMARY_SHAS=("e"*64,)*15))
        p291=NS(PARENT_SHA="c"*64,context=lambda:old)
        parent=NS(PARENT_SHA="b"*64,no_neural=contextlib.nullcontext,validate_result=Mock(),verify_artifacts=Mock())
        payload=dict(commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},artifacts=[dict(file=n,sha256=v[0],serialized_bytes=v[1]) for n,v in b.PARENT_ARTIFACTS.items()],validation_summary=dict(diagnostic_complete=True,capability_gate_applicable=False))
        parent.verify_artifacts.return_value=(payload,{})
        wanted=[b.PARENT_SHA,"b"*64,"c"*64,"d"*64]+["e"*64]*15;mapping=dict(zip(map(str,paths),wanted,strict=True))
        objects={n:{"fixture":n} for n in ("dataset.json","triple-dataset.json","quad-dataset.json")}
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:objects[p.name]));m=b.manifest()
        for k,n in zip(("data_sha256","triple_sha256","quad_sha256"),objects,strict=True):m[k]=b.digest(objects[n])
        with patch.object(b,"context",return_value=(parent,p291,None,None,None,None,c)),patch.object(b,"manifest",return_value=m):yield paths,mapping,parent,payload

    def test_27_nineteen_hashes_before_dispatch(self):
        with self.parent_fixture() as (paths,mapping,parent,payload):
            self.assertEqual(b.load_parent(paths)[0],payload);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_28_parent_scope_and_descriptor(self):
        for fn in (lambda p:p.update(status="FAIL"),lambda p:p["artifacts"][0].update(serialized_bytes=1),lambda p:p["validation_summary"].update(capability_gate_applicable=True)):
            with self.parent_fixture() as (paths,_,_,payload):
                fn(payload)
                with self.assertRaises(ValueError):b.load_parent(paths)

    def test_29_actual_protection_and_helper_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);names=[b.PARENT_SOURCE]+[f"accepted/{i}" for i in range(597)];pins={n:(b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40) for n in names}
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1081-len(inputs)):
                p=root/f"input{i}";p.write_text("input",encoding="utf-8");inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();s=directory/"summary.json";s.write_text("summary",encoding="utf-8");mapping={str(s.resolve()):b.PARENT_SHA}
            for n,v in b.PARENT_ARTIFACTS.items():p=directory/n;p.write_text("parent",encoding="utf-8");mapping[str(p.resolve())]=v[0]
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*a):return (pins.get(a[1][5:],"c"*40)+"\n").encode()
            parent=types.ModuleType("parent");parent.__file__=str(root/b.PARENT_SOURCE);p291=NS(context=lambda:())
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            with patch.object(b,"context",return_value=(parent,p291,None,None,None,None,c)),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=inputs),None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([s]*19,root))),(604,1091))
                missing=types.ModuleType("missing");missing.__file__=str(root/"missing.py");c.missing=missing
                with self.assertRaisesRegex(ValueError,"unprotected helper"):b.precheck([s]*19,root)

    def test_30_semantic_suite_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            s=b.regression_suite(Path.cwd());self.assertEqual(s.countTestCases(),b.manifest()["focused_tests"]);self.assertEqual({t.id() for t in b.flatten(s)},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())

    def test_31_bundle_schema_and_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"bundle.pt";v=dict(schema="fold-c293-support-models-v1",identities=[list(i) for i in b.identities()],states=[{} for _ in range(15)])
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),15);v["identities"].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)
        with patch.object(sys,"argv",["prog","--summaries"]+[str(i) for i in range(19)]+["--output-dir","out","--expected-head","f"*40]),patch.object(b,"run") as run:
            b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),19)

    @contextlib.contextmanager
    def run_fixture(self):
        records=copy.deepcopy(self.records);lookup={(r["seed"],r["arm"]):r for r in records};events=[]
        parent,diag,transfer,c=scorers(self.data);c.audit=Audit();training=NS(training_tables=lambda *_:(self.x,self.y))
        def pc(*_):events.append("precheck");return protection()
        def load(*_):events.append("load_parent");return {},self.data,{"triple":True},{"quad":True}
        def train(*args):events.append("train");return copy.deepcopy(lookup[(args[6],args[7])]),{}
        def replay(*_):events.append("replay")
        with patch.object(b,"context",return_value=(parent,None,diag,NS(replay_one=replay),transfer,training,c)),patch.object(b,"precheck",side_effect=pc),patch.object(b,"load_parent",side_effect=load),patch.object(b,"make_models",return_value=dict.fromkeys(b.ARMS,None)),patch.object(b,"train_one",side_effect=train):yield events

    def test_32_production_run_order_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*19,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[:2],["precheck","load_parent"]);self.assertEqual(events.count("train"),15);self.assertEqual(events.count("replay"),15);self.assertEqual(events[-1],"precheck")
            q,_=b.verify_artifacts(out,["x"]*19,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*19,output_dir=out,expected_head="f"*40)

    def test_33_hash_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*19,output_dir=out,expected_head="f"*40);path=out/"measurements.json";path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*19,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size);(out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*19,"f"*40)

    def test_34_runtime_preflight(self):
        with patch.object(b,"context",return_value=(None,None,None,None,None,NS(training_tables=lambda *_:(self.x,self.y)),None)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,{},{})),patch.object(b,"make_models",return_value={}),contextlib.redirect_stdout(io.StringIO()):b.runtime_preflight(["x"]*19,Path.cwd())

    def test_35_cp932_read_independence(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))

    def test_36_no_implicit_text_reads(self):
        for path in (Path(b.__file__),Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in node.keywords))

    def test_37_runner_blocks_and_paths(self):
        root=Path(__file__).resolve().parents[1];runner=(root/b.OWN[2]).read_text(encoding="utf-8");launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:21]",blocks[2]);self.assertIn("head = sys.argv[21]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),19)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"));self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_38_context_and_module_count(self):
        c=NS(audit=Audit());p291=NS(context=lambda:(0,1,2,3,4,5,c));parent=NS(context=lambda:(p291,c),regression_modules=lambda root:["fixture"+str(i) for i in range(177)])
        package=types.ModuleType("fold_lm.v05_benchmarks");package.model_c292_saved_answer_roles=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):self.assertEqual(b.context(),(parent,p291,2,3,4,5,c));self.assertEqual(len(b.regression_modules(Path.cwd())),178)
        imports=[n for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c292_saved_answer_roles"])

    def test_39_guard_and_count(self):
        b.guard(Path.cwd(),"f"*40,NS(audit=Audit()))
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])

    def test_40_record_role_counts_without_decoder_filter(self):
        parent,_,_,_=scorers(self.data);raw={"0":{"normal":torch.zeros((192,256),dtype=torch.float64)}};raw["0"]["normal"][:,88]=10.
        counts=b.role_counts(raw,self.data["TRAIN"],parent);self.assertEqual(counts["correct"],0);self.assertEqual(counts["role_counts"]["non_value_byte"],192)


if __name__=="__main__":unittest.main()
