"""C291 behavioral fixtures; no claims about user-local FOLD scientific outcomes."""
import ast
import contextlib
import copy
import hashlib
import io
import itertools
import json
import math
import re
import sys
import tempfile
import types
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock,patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c291_answer_margin as b


def dataset():
    data={}
    for split,count in (("TRAIN",8),("HOLDOUT",4)):
        rows=[]
        for lang,e in itertools.product(("en","ja"),((0,1),(0,2),(1,2))):
            for order,j in itertools.product((e,e[::-1]),range(count)):
                for q,target in zip(e,(48,49),strict=True):
                    rows.append(dict(language=lang,entities=list(e),values=[j+10,j+20],permutation=list(order),query=q,target=target))
        data[split]=rows
    return data


def tables(data):
    y=torch.tensor([r["target"] for r in data["TRAIN"]]);x=torch.zeros((2,3,192,48),dtype=torch.int64)
    x[:,:,:,0]=torch.arange(192)%2
    return x,y


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__();self.backbone=torch.nn.Embedding(2,4,dtype=torch.float64);self.read=torch.nn.Linear(4,256,dtype=torch.float64)
        self.calls=0;self.rows=0
    def forward(self,tokens,zeros):
        assert tokens.ndim==2 and tokens.shape[1]==48 and zeros.shape==(len(tokens),) and not bool(zeros.any())
        self.calls+=1;self.rows+=len(tokens)
        return self.read(self.backbone(tokens[:,0]))


def fingerprint(model):
    return b.digest({k:v.detach().tolist() for k,v in model.state_dict().items()})


def fit_fixture(seed,arm,data):
    aux=3. if arm==b.ARMS[1] else 4.;weight=0. if arm==b.ARMS[0] else .25
    return dict(steps=800,training_rows=38400,optimizer_creations=1,last_ce=2.,ce_history=[2.]*800,
                pair_history=[3.]*800,answer_history=[4.]*800,total_history=[2.+weight*aux]*800,
                applied_lr=[.005]*800,applied_weight=[weight]*800,**b.schedule(seed,data["TRAIN"])[3])


def records_fixture():
    data=dataset();records=[]
    for seed,arm in b.identities():
        raw={t:dict(passed=True,totals=[dict(split=s,profile=str(p),language=l,rows=n,pairs=n//2,correct=n,collapsed_pairs=0)
             for s,n in (("TRAIN",96),("HOLDOUT",48)) for p in range(3) for l in ("en","ja")]) for t in b.TASKS}
        records.append(dict(seed=seed,arm=arm,parameters=14256,weights_changed=True,checkpoint_roundtrip=True,reload_max_error=0.,
                            initial_sha256="a"*64,final_sha256="b"*64,fit=fit_fixture(seed,arm,data),raw=raw,
                            forward_calls=881,row_presentations=46176,core_forward_calls=3524,
                            replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    return records,data


def scorers():
    diagnostic=NS(normalize_task=lambda scored,*_:scored["totals"],partition=lambda rows:dict(direct_pass=all(r["correct"]==r["rows"] for r in rows)))
    transfer=NS(score_quad=lambda data,raw,c:raw)
    c=NS(p267=NS(score=lambda data,raw:raw),c270=NS(score=lambda data,raw,p:raw))
    return diagnostic,transfer,c


def parent_fixture(parent):
    return dict(experiment_id="C290-v5b-saved-pair-margin-audit",commit_sha=b.PARENT_EXECUTION,status="PASS",
                source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},artifacts=[dict(file=n,sha256=v[0],serialized_bytes=v[1]) for n,v in b.PARENT_ARTIFACTS.items()],
                validation_summary=dict(diagnostic_complete=True,capability_gate_applicable=False,parent_results=parent.expected_results(),pair_records=19440))


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<592:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1066)}


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
    z=torch.zeros((2,256),dtype=torch.float64);z[0,48]=2.;z[1,49]=2.
    return z,torch.tensor([48,49])


class C291Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.deterministic=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
        cls.data=dataset();cls.x,cls.y=tables(cls.data);torch.manual_seed(77);initial=Toy();cls.initial=copy.deepcopy(initial)
        cls.fits=[];cls.models=[]
        with contextlib.redirect_stdout(io.StringIO()):
            for arm in b.ARMS:
                m=copy.deepcopy(initial);cls.fits.append(b.fit(m,cls.data,cls.x,cls.y,b.SEEDS[0],arm));cls.models.append(m)
        cls.records,_=records_fixture();cls.metrics,cls.summary=b.analyze(cls.records,cls.data,*scorers())
    @classmethod
    def tearDownClass(cls):
        torch.set_num_threads(cls.threads);torch.use_deterministic_algorithms(cls.deterministic)

    def test_01_manifest_seal(self):
        b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seal(self):
        for value in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",value),self.assertRaises(ValueError):b.validate_seal()

    def test_03_zero_logits_closed_form(self):
        z=torch.zeros((2,256),dtype=torch.float64);y=torch.tensor([48,49])
        for arm in b.ARMS:
            total,ce,pair,answer=b.objective(z,y,arm)
            self.assertAlmostEqual(float(ce),math.log(256));self.assertAlmostEqual(float(pair),math.log1p(math.e))
            self.assertEqual(pair,answer);self.assertAlmostEqual(float(total),float(ce)+(0 if arm==b.ARMS[0] else .25*float(answer)))

    def test_04_ce_identity_and_gradient(self):
        z,y=example();z.requires_grad_();total=b.objective(z,y,"ce_only")[0];ce=F.cross_entropy(z,y)
        self.assertTrue(torch.equal(total,ce));self.assertTrue(torch.equal(torch.autograd.grad(total,z)[0],torch.autograd.grad(ce,z)[0]))

    def test_05_pair_sum_identity(self):
        z,y=example();total,ce,pair,_=b.objective(z,y,"pair_sum")
        self.assertAlmostEqual(float(pair),math.log1p(math.exp(-3.)));self.assertEqual(total,ce+.25*pair)

    def test_06_offsets(self):
        z,y=example();other=z+torch.tensor([[12.],[-9.]])
        for arm in b.ARMS:
            for a,c in zip(b.objective(z,y,arm),b.objective(other,y,arm),strict=True):self.assertAlmostEqual(float(a),float(c))

    def test_07_pair_compensation_witness(self):
        z,y=example();z[0,48]=20.;z[1,48]=10.;z[1,49]=0.
        _,_,pair,answer=b.objective(z,y,"answer_margin")
        self.assertLess(float(pair),.001);self.assertGreater(float(answer),5.)
        self.assertEqual(int((z.argmax(1)==y).sum()),1)

    def test_08_third_class_witness_and_gradient(self):
        z,y=example();z[:,70]=10.;z.requires_grad_();answer=b.objective(z,y,"answer_margin")[3]
        grad=torch.autograd.grad(answer,z)[0]
        self.assertGreater(float(answer.detach()),8.);self.assertTrue(bool((grad[:,70]>0).all()))
        self.assertTrue(bool((grad[torch.arange(2),y]<0).all()));self.assertEqual(int((grad!=0).sum()),4)

    def test_09_pair_and_class_permutations(self):
        z,y=example();a=b.objective(z,y,"answer_margin")
        c=b.objective(z.flip(0),y.flip(0),"answer_margin")
        for x,v in zip(a,c,strict=True):self.assertEqual(x,v)
        perm=torch.arange(255,-1,-1)
        for x,v in zip(a,b.objective(z[:,perm],255-y,"answer_margin"),strict=True):self.assertAlmostEqual(float(x),float(v))

    def test_10_finite_difference_and_ties(self):
        z,y=example();z[:,70]=3.;z.requires_grad_();loss=b.objective(z,y,"answer_margin")[0]
        grad=torch.autograd.grad(loss,z)[0]
        for i,j in ((0,48),(0,70),(1,49),(1,7)):
            plus=z.detach().clone();minus=plus.clone();plus[i,j]+=1e-6;minus[i,j]-=1e-6
            numeric=(b.objective(plus,y,"answer_margin")[0]-b.objective(minus,y,"answer_margin")[0])/(2e-6)
            self.assertAlmostEqual(float(numeric),float(grad[i,j]),places=7)
        z=torch.zeros((2,256),dtype=torch.float64,requires_grad=True)
        grad=torch.autograd.grad(b.objective(z,y,"answer_margin")[3],z)[0]
        self.assertTrue(bool(torch.isfinite(grad).all()));self.assertTrue(bool((grad[:,0]>0).all()))

    def test_11_nonfinite(self):
        for v in (float("inf"),float("nan")):
            z,y=example();z[0,1]=v
            with self.assertRaises(ValueError):b.objective(z,y,"answer_margin")

    def test_12_shape_dtype(self):
        z,y=example()
        for a,c in ((z.float(),y),(z[:,:255],y),(z[:1],y[:1]),(z,y.float())):
            with self.assertRaises(ValueError):b.objective(a,c,"ce_only")

    def test_13_invalid_labels(self):
        for y in (torch.tensor([-1,49]),torch.tensor([48,256]),torch.tensor([48,48])):
            with self.assertRaises(ValueError):b.objective(example()[0],y,"answer_margin")

    def test_14_unknown_arm(self):
        with self.assertRaises(ValueError):b.objective(*example(),"pair_early")

    def test_15_actual_schedule_counts(self):
        for seed in b.SEEDS:
            x,p,l,plan=b.schedule(seed,self.data["TRAIN"])
            self.assertEqual(x.shape,(800,48));self.assertEqual(plan["per_length_row_exposures"],[[100]*192]*2)
            self.assertEqual(plan["length_profile_updates"],[[136,132,132],[132,136,132]])

    def test_16_pair_integrity(self):
        x,_,_,_=b.schedule(b.SEEDS[0],self.data["TRAIN"])
        for ids in x.tolist():
            for i,j in zip(ids[::2],ids[1::2],strict=True):
                a,c=self.data["TRAIN"][i],self.data["TRAIN"][j]
                self.assertNotEqual(a["query"],c["query"])
                for k in ("language","entities","values","permutation"):self.assertEqual(a[k],c[k])

    def test_17_schedule_determinism(self):
        a=b.schedule(b.SEEDS[0],self.data["TRAIN"])[0];c=b.schedule(b.SEEDS[0],self.data["TRAIN"])[0]
        self.assertTrue(torch.equal(a,c));self.assertFalse(torch.equal(a,b.schedule(b.SEEDS[1],self.data["TRAIN"])[0]))

    def test_18_schedule_rejects_incomplete_pairs(self):
        for fn in (lambda r:r.pop(),lambda r:r[1].update(query=r[0]["query"])):
            rows=copy.deepcopy(self.data["TRAIN"]);fn(rows)
            with self.assertRaises(ValueError):b.schedule(b.SEEDS[0],rows)
        with self.assertRaises(ValueError):b.schedule(289001,self.data["TRAIN"])

    def test_19_real_model_factory_contract(self):
        class Fake(torch.nn.Module):
            def __init__(self,*_):super().__init__();self.weight=torch.nn.Parameter(torch.ones(14256,dtype=torch.float64))
        c=NS(c278=NS(MeanFinalDualReadout=Fake),factory=NS(new_model=lambda _:None),reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))
        models=b.make_models(b.SEEDS[0],c);self.assertEqual(list(models),list(b.ARMS))
        self.assertEqual(len({m.weight.data_ptr() for m in models.values()}),3)
        with self.assertRaises(ValueError):b.make_models(1,c)

    def test_20_factory_rejects_wrong_capacity(self):
        class Fake(torch.nn.Module):
            def __init__(self,*_):super().__init__();self.weight=torch.nn.Parameter(torch.ones(3,dtype=torch.float64))
        c=NS(c278=NS(MeanFinalDualReadout=Fake),factory=NS(new_model=lambda _:None),reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))
        with self.assertRaises(ValueError):b.make_models(b.SEEDS[0],c)

    def test_21_actual_800_updates_three_arms(self):
        for arm,f,m in zip(b.ARMS,self.fits,self.models,strict=True):
            b.check_fit(f,b.SEEDS[0],arm,self.data)
            self.assertEqual((m.calls,m.rows),(800,38400));self.assertFalse(m.training)
            self.assertLess(f["last_ce"],f["ce_history"][0]);self.assertNotEqual(fingerprint(m),fingerprint(self.initial))

    def test_22_fit_rng_replay(self):
        m=copy.deepcopy(self.initial)
        with contextlib.redirect_stdout(io.StringIO()):f=b.fit(m,self.data,self.x,self.y,b.SEEDS[0],b.ARMS[2])
        self.assertEqual(f,self.fits[2]);self.assertEqual(fingerprint(m),fingerprint(self.models[2]))

    def test_23_fit_tamper(self):
        for fn in (lambda f:f["applied_lr"].__setitem__(0,.01),lambda f:f["total_history"].__setitem__(10,99.),lambda f:f.update(optimizer_creations=2)):
            f=copy.deepcopy(self.fits[2]);fn(f)
            with self.assertRaises(ValueError):b.check_fit(f,b.SEEDS[0],b.ARMS[2],self.data)

    def test_24_actual_train_one_order_and_counts(self):
        m=copy.deepcopy(self.initial);events=[]
        @contextlib.contextmanager
        def counted(model,core):
            calls=[0,0];cores=[0]
            yield calls,cores
            calls[:]=[model.calls,model.rows];cores[0]=4*model.calls
        def evaluate(model,*_):
            events.append("frozen_evaluation");self.assertFalse(model.training)
            self.assertFalse(any(p.requires_grad for p in model.parameters()))
            with torch.no_grad():
                for _ in range(81):model(torch.zeros((96,48),dtype=torch.int64),torch.zeros(96,dtype=torch.int64))
            return {t:{} for t in b.TASKS}
        c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted),core=None)
        with contextlib.redirect_stdout(io.StringIO()):
            r,state=b.train_one(m,self.data,{}, {},self.x,self.y,b.SEEDS[0],b.ARMS[0],NS(evaluate=evaluate),None,c)
        self.assertEqual(events,["frozen_evaluation"]);self.assertEqual((r["forward_calls"],r["row_presentations"]),(881,46176))
        self.assertEqual(list(state),list(m.state_dict()))

    def test_25_target_alignment(self):
        y=self.y.clone();y[0]=50
        with self.assertRaises(ValueError):b.fit(copy.deepcopy(self.initial),self.data,self.x,y,b.SEEDS[0],b.ARMS[0])

    def test_26_matching_guards(self):
        group=copy.deepcopy(self.records[:3]);b.check_matched_group(group)
        for key in ("ce_history","pair_history","answer_history"):
            changed=copy.deepcopy(group);changed[1]["fit"][key][0]+=1.
            with self.assertRaises(ValueError):b.check_matched_group(changed)
        group[1]["initial_sha256"]="0"*64
        with self.assertRaises(ValueError):b.check_matched_group(group)

    def test_27_actual_analysis_inventory(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["contrasts"])),(15,90,360))
        self.assertEqual(self.summary["quad_pass_counts"],dict.fromkeys(b.ARMS,5));self.assertTrue(self.summary["candidate_gate"])

    def test_28_one_candidate_miss_stays_negative(self):
        records=copy.deepcopy(self.records);records[2]["raw"]["quad"]["passed"]=False
        _,s=b.analyze(records,self.data,*scorers());self.assertFalse(s["candidate_gate"])
        self.assertEqual(s["quad_pass_counts"][b.ARMS[2]],4);b.validate_result(result_fixture(s))

    def test_29_replay_and_workload_tamper(self):
        for key,value in (("reload_max_error",1e-3),("replay_forward_calls",80),("checkpoint_roundtrip",False),("parameters",1)):
            records=copy.deepcopy(self.records);records[0][key]=value
            with self.assertRaises(ValueError):b.analyze(records,self.data,*scorers())

    def test_30_result_contract(self):
        b.validate_result(result_fixture(self.summary))
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p["source_blobs"].pop(b.PARENT_SOURCE),lambda p:p["validation_summary"].update(train_steps=False),lambda p:p["validation_summary"]["final_partitions"].pop()):
            p=result_fixture(copy.deepcopy(self.summary));fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    def test_31_loader_hash_before_dispatch(self):
        paths=[(Path("/c291-fixture")/str(i)/"summary.json").resolve() for i in range(17)]
        parent=NS(PARENT_SHA="c"*64,expected_results=lambda:["fixed"],no_neural=contextlib.nullcontext,validate_result=Mock())
        legacy=NS(SUMMARY_SHAS=("d"*64,)*15);p=parent_fixture(parent);parent.verify_artifacts=Mock(return_value=(p,{}))
        wanted=[b.PARENT_SHA,parent.PARENT_SHA,*legacy.SUMMARY_SHAS];mapping=dict(zip(map(str,paths),wanted,strict=True))
        objects={n:{"fixture":n} for n in ("dataset.json","triple-dataset.json","quad-dataset.json")}
        c=NS(audit=NS(sha=lambda path:mapping[str(path)],read_json=lambda path:objects[path.name]))
        manifest=b.manifest();manifest.update({k:b.digest(objects[n]) for k,n in zip(("data_sha256","triple_sha256","quad_sha256"),objects,strict=True)})
        with patch.object(b,"context",return_value=(parent,legacy,None,None,None,None,c)),patch.object(b,"manifest",return_value=manifest):
            self.assertEqual(b.load_parent(paths)[0],p);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_32_parent_scope_and_artifacts(self):
        parent=NS(expected_results=lambda:[]);p=parent_fixture(parent);b.validate_parent(p,parent)
        for fn in (lambda p:p.update(status="FAIL"),lambda p:p["artifacts"][0].update(serialized_bytes=1),lambda p:p["validation_summary"].update(capability_gate_applicable=True)):
            q=copy.deepcopy(p);fn(q)
            with self.assertRaises(ValueError):b.validate_parent(q,parent)

    def test_33_actual_precheck_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);lm=[f"fold_lm/fixture{i}.py" for i in range(6)]
            names=[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,291)];names[-1]=b.PARENT_SOURCE
            names+=lm;names+=[f"accepted/{i}" for i in range(586-len(names))]
            pins={n:(b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40) for n in names}
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n)
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1056-len(inputs)):
                p=root/f"input{i}";p.write_text("input");inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();summary=directory/"summary.json";summary.write_text("summary")
            mapping={str(summary.resolve()):b.PARENT_SHA}
            for n,v in b.PARENT_ARTIFACTS.items():p=directory/n;p.write_text("parent");mapping[str(p.resolve())]=v[0]
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*args):return (pins.get(args[1][5:],"c"*40)+"\n").encode()
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}),factory=NS(LM_SOURCES=lm))
            p=dict(source_blobs=pins,input_sha256=inputs)
            with patch.object(b,"context",return_value=(None,None,None,None,None,None,c)),patch.object(b,"load_parent",return_value=(p,None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*17,root))),(592,1066))
                pins.pop(b.PARENT_SOURCE)
                with self.assertRaises(ValueError):b.precheck([summary]*17,root)

    def test_34_semantic_regression_inventory(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(4285)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),4285)
            self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("duplicate"),Dummy("duplicate")])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())

    def test_35_bundle_and_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"bundle.pt";v=dict(schema="fold-c291-answer-margin-models-v1",identities=[list(i) for i in b.identities()],states=[{} for _ in range(15)])
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),15)
            v["identities"].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)
        argv=["prog","--summaries"]+[str(i) for i in range(17)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),17)

    @contextlib.contextmanager
    def run_fixture(self):
        records=copy.deepcopy(self.records);events=[];lookup={(r["seed"],r["arm"]):r for r in records}
        diagnostic,transfer,c=scorers();c.audit=Audit();parent=NS(no_neural=contextlib.nullcontext)
        def replay(*args):events.append("replay")
        evaluation=NS(replay_one=replay);training=NS(training_tables=lambda *_:(self.x,self.y))
        def load(*_):events.append("load_parent");return {},self.data,{"triple":True},{"quad":True}
        def train(*args):events.append("train");return copy.deepcopy(lookup[(args[6],args[7])]),{}
        def precheck(*_):events.append("precheck");return protection()
        with patch.object(b,"context",return_value=(parent,None,diagnostic,evaluation,transfer,training,c)),patch.object(b,"precheck",side_effect=precheck),patch.object(b,"load_parent",side_effect=load),patch.object(b,"make_models",return_value=dict.fromkeys(b.ARMS,None)),patch.object(b,"train_one",side_effect=train):
            yield events

    def test_36_run_call_order_and_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*17,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[:2],["precheck","load_parent"]);self.assertEqual(events.count("train"),15)
            self.assertEqual(events.count("replay"),15);self.assertEqual(events[-1],"precheck")
            q,_=b.verify_artifacts(out,["x"]*17,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*17,output_dir=out,expected_head="f"*40)

    def test_37_hash_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*17,output_dir=out,expected_head="f"*40)
            path=out/"measurements.json";path.write_text("{}")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*17,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*17,"f"*40)

    def test_38_runtime_anchor_equivalence(self):
        def old(z,y,w):
            targets=y.reshape(-1,2);logits=z.reshape(-1,2,256);i=torch.arange(len(targets))
            correct=logits[i,0,targets[:,0]]+logits[i,1,targets[:,1]]
            swapped=logits[i,0,targets[:,1]]+logits[i,1,targets[:,0]]
            pair=F.softplus(1.-(correct-swapped)).mean();ce=F.cross_entropy(z,y)
            return ce if w==0. else ce+w*pair,ce,pair
        c=NS();legacy=NS(objective=old);training=NS(training_tables=lambda *_:(self.x,self.y))
        with patch.object(b,"context",return_value=(None,legacy,None,None,None,training,c)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,{},{})),patch.object(b,"make_models",return_value={}),contextlib.redirect_stdout(io.StringIO()):
            b.runtime_preflight(["x"]*17,Path.cwd())

    def test_39_runner_inventory_and_blocks(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/b.OWN[2]).read_text();launcher=(root/b.OWN[3]).read_text()
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:19]",blocks[2]);self.assertIn("head = sys.argv[19]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),17)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),40)
        for name in b.OWN:self.assertTrue((root/name).is_file())
        self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text())

    def test_40_context_import_and_guard(self):
        package=types.ModuleType("fold_lm.v05_benchmarks");c=NS(audit=Audit());legacy=NS(context=lambda:("unused",2,3,4,5,c))
        parent=NS(context=lambda:(legacy,c));package.model_c290_saved_pair_margin_audit=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):self.assertEqual(b.context(),(parent,legacy,2,3,4,5,c))
        b.guard(Path.cwd(),"f"*40,c)
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,c)
        imports=[n for n in ast.walk(ast.parse(Path(b.__file__).read_text())) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c290_saved_pair_margin_audit"])


if __name__=="__main__":unittest.main()
