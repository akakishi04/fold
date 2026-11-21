"""C288 behavioral authoring tests; real archives/models remain runtime gates."""
import ast
import contextlib
import copy
import hashlib
import io
import json
import math
import re
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock,patch

import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c288_query_pair_assignment_loss as b


def data_fixture():
    return dict(TRAIN=[dict(language="en",entities=[0,1],values=[i,i+1],permutation=[0,1],query=q,target=48+q)
                       for i in range(96) for q in (0,1)],HOLDOUT=[])


def fingerprint(model):
    return hashlib.sha256(b"".join(v.detach().cpu().numpy().tobytes() for v in model.state_dict().values())).hexdigest()


class Weights(torch.nn.Module):
    def __init__(self,n=13488):
        super().__init__();self.weight=torch.nn.Parameter(torch.ones(n,dtype=torch.float64))


class Readout(torch.nn.Module):
    def __init__(self,backbone,seed,reader,span):
        super().__init__();self.backbone=backbone;self.read=Weights(768)


class Audit:
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse":return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch":return b"feat/sft-target-loss\n"
        return b""
    @staticmethod
    def sha(path):
        p=Path(path);return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n):return Path(root)/n


def scored(task):
    ps={"two_char":("doubled","shared_prefix","shared_suffix"),"triple":("tripled","shared_prefix2","shared_suffix2"),
        "quad":("quadrupled","shared_prefix3","shared_suffix3")}[task]
    totals=[dict(split=s,profile=p,language=l,rows=n,pairs=n//2,correct=n,collapsed_pairs=0)
            for s,n in (("TRAIN",96),("HOLDOUT",48)) for p in ps for l in ("en","ja")]
    return dict(passed=True,totals=totals)


def fixture_context():
    def normalized(tm,task,seed,arm):
        return [dict(split=s,passed=tm["passed"],direct_pass=tm["passed"]) for s in ("TRAIN","HOLDOUT")]
    def part(rr):
        return dict(direct_pass=all(r["direct_pass"] for r in rr),full_pass=all(r["passed"] for r in rr))
    parent=NS(normalize_task=normalized,partition=part)
    c=NS(audit=Audit(),p267=NS(dataset=data_fixture,validate_data=lambda d:None,score=lambda d,r:r),
         c270=NS(prompt_dataset=lambda *a:{"triple":True},validate_dataset=lambda *a:None,score=lambda d,r,p:r),
         c278=NS(MeanFinalDualReadout=Readout),c269=NS(query_span_mask=None),factory=NS(new_model=lambda s:Weights()),
         reader=None,base=NS(fingerprint=fingerprint),core=None)
    transfer=NS(dataset=lambda d:{"quad":True},validate_dataset=lambda *a:None,score_quad=lambda d,r,c:r)
    training=NS(training_tables=lambda d,c:(torch.zeros((2,3,192,48),dtype=torch.int64),torch.tensor([48,49]*96)))
    return parent,NS(replay_one=Mock()),transfer,training,c


def records_fixture():
    ctx=fixture_context();data=data_fixture();records=[]
    for seed,arm in b.identities():
        total=.1 if arm==b.ARMS[0] else .1+b.PAIR_WEIGHT*.5
        f=dict(steps=800,training_rows=38400,ce_history=[.1]*800,pair_history=[.5]*800,total_history=[total]*800,
               applied_lr=[.005]*800,last_ce=.1,**b.schedule(seed,data["TRAIN"])[3])
        records.append(dict(seed=seed,arm=arm,parameters=14256,weights_changed=True,checkpoint_roundtrip=True,
                            initial_sha256="a"*64,final_sha256="b"*64,reload_max_error=0.,fit=f,raw={t:scored(t) for t in b.TASKS},
                            forward_calls=881,row_presentations=46176,core_forward_calls=3524,
                            replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    return ctx,data,records


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<574:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1026)}


def result_fixture():
    ctx,data,records=records_fixture();_,s=b.analyze(records,data,ctx[0],ctx[2],ctx[4]);pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
                gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False,
                source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s)


def recount(p):
    s=p["validation_summary"];rr=s["seed_results"]
    for r in rr:r["passed"]=r["quad_pass"];r["all_tasks_pass"]=all(r[t+"_pass"] for t in b.TASKS)
    for name,field in (("seed_pass_counts","passed"),("two_char_pass_counts","two_char_pass"),("triple_pass_counts","triple_pass"),
                       ("quad_pass_counts","quad_pass"),("all_tasks_pass_counts","all_tasks_pass"),
                       ("fitted_train_pass_counts","fitted_train_direct_pass"),("seen_holdout_pass_counts","seen_holdout_direct_pass")):
        s[name]={a:sum(r[field] for r in rr if r["arm"]==a) for a in b.ARMS}
    return p


def parent_fixture():
    parts=[]
    for seed in range(286001,286006):
        for arm in ("constant_lr","cosine_tail"):
            fail=seed in (286002,286003);quad_only=seed==286005 and arm=="constant_lr"
            parts.append(dict(seed=seed,arm=arm,first_direct_failure_partition="fitted_train" if fail else "quad" if quad_only else "none",
                              fitted_train_direct_pass=not fail,seen_length_holdout_direct_pass=not fail,quad_direct_pass=not(fail or quad_only)))
    return dict(commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
                artifacts=[dict(file=n,sha256=v[0],serialized_bytes=v[1]) for n,v in b.PARENT_ARTIFACTS.items()],
                validation_summary=dict(diagnostic_complete=True,capability_gate_applicable=False,model_forward_calls=0,model_partitions=parts))


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__();self.bias=torch.nn.Parameter(torch.zeros(256,dtype=torch.float64))
        self.query=torch.nn.Parameter(torch.zeros(256,dtype=torch.float64));self.seen=[]
    def forward(self,x,t):
        assert len(x)==48 and t.shape==(48,) and bool((t==0).all())
        self.seen.append((int(x[0,1]),tuple(x[:,0].tolist())))
        return self.bias[None,:]+(2*x[:,0].to(torch.float64)-1)[:,None]*self.query[None,:]


class C288Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.rng=torch.random.get_rng_state()
        cls.deterministic=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
    @classmethod
    def tearDownClass(cls):
        torch.set_num_threads(cls.threads);torch.random.set_rng_state(cls.rng)
        torch.use_deterministic_algorithms(cls.deterministic)

    def test_01_seal_executes(self):
        b.validate_seal();self.assertEqual(b.MANIFEST_SHA,b.digest(b.manifest()))

    def test_02_bad_seals(self):
        for sha in ("UNSEALED","0"*64,"F"*64):
            with patch.object(b,"MANIFEST_SHA",sha),self.assertRaises(ValueError):b.validate_seal()

    def test_03_zero_logits_closed_form(self):
        z=torch.zeros((2,256),dtype=torch.float64);y=torch.tensor([1,2])
        total,ce,pair=b.objective(z,y,b.ARMS[1])
        self.assertAlmostEqual(float(ce),math.log(256));self.assertAlmostEqual(float(pair),math.log1p(math.e))
        self.assertAlmostEqual(float(total),math.log(256)+.25*math.log1p(math.e))

    def test_04_correct_assignment_better_than_swap(self):
        z=torch.zeros((2,256),dtype=torch.float64);z[0,1]=2.;z[1,2]=2.;y=torch.tensor([1,2])
        good=b.objective(z,y,b.ARMS[1])[2];bad=b.objective(z.flip(0),y,b.ARMS[1])[2]
        self.assertLess(float(good),float(bad))

    def test_05_pair_row_swap_invariance(self):
        z=torch.arange(512,dtype=torch.float64).reshape(2,256)/100;y=torch.tensor([1,2])
        self.assertEqual(float(b.objective(z,y,b.ARMS[1])[2]),float(b.objective(z.flip(0),y.flip(0),b.ARMS[1])[2]))

    def test_06_per_row_offset_invariance(self):
        z=torch.zeros((2,256),dtype=torch.float64);z[0,1]=2.;z[1,2]=2.;y=torch.tensor([1,2])
        a=b.objective(z,y,b.ARMS[1])[2];c=b.objective(z+torch.tensor([[10.],[-30.]]),y,b.ARMS[1])[2]
        self.assertAlmostEqual(float(a),float(c))

    def test_07_query_independent_scores_cannot_win_assignment(self):
        z=torch.zeros((2,256),dtype=torch.float64);z[:,1]=100.;y=torch.tensor([1,2])
        self.assertAlmostEqual(float(b.objective(z,y,b.ARMS[1])[2]),math.log1p(math.e))

    def test_08_autograd_matches_finite_difference(self):
        mask=torch.zeros((2,2,256),dtype=torch.float64);mask[0,0,1]=1.;mask[1,1,2]=1.
        def f(x):return b.objective((x[:,None,None]*mask).sum(0),torch.tensor([1,2]),b.ARMS[1])[0]
        self.assertTrue(torch.autograd.gradcheck(f,(torch.tensor([.2,-.1],dtype=torch.float64,requires_grad=True),)))

    def test_09_ce_control_exact_value_and_gradient(self):
        z=torch.linspace(-1,1,512,dtype=torch.float64).reshape(2,256).requires_grad_();y=torch.tensor([1,2])
        total,_,_=b.objective(z,y,b.ARMS[0]);ref=F.cross_entropy(z,y)
        self.assertEqual(float(total),float(ref))
        self.assertTrue(torch.equal(torch.autograd.grad(total,z)[0],torch.autograd.grad(ref,z)[0]))

    def test_10_pair_gradient_breaks_wrong_assignment(self):
        z=torch.zeros((2,256),dtype=torch.float64,requires_grad=True)
        b.objective(z,torch.tensor([1,2]),b.ARMS[1])[2].backward()
        self.assertLess(float(z.grad[0,1]),0);self.assertGreater(float(z.grad[0,2]),0)
        self.assertLess(float(z.grad[1,2]),0);self.assertGreater(float(z.grad[1,1]),0)
        self.assertEqual(float(z.grad[:,3:].abs().sum()),0.)

    def test_11_auxiliary_margin_is_not_individual_accuracy(self):
        z=torch.zeros((2,256),dtype=torch.float64);z[0,1]=20.;z[1,1]=1.
        _,ce,pair=b.objective(z,torch.tensor([1,2]),b.ARMS[1])
        self.assertLess(float(pair),1e-6);self.assertGreater(float(ce),1.)

    def test_12_invalid_shapes_and_targets_rejected(self):
        for z,y in ((torch.zeros((3,256),dtype=torch.float64),torch.tensor([1,2,3])),
                    (torch.zeros((2,255),dtype=torch.float64),torch.tensor([1,2])),
                    (torch.zeros((2,256),dtype=torch.float64),torch.tensor([1,1])),
                    (torch.zeros((2,256),dtype=torch.float64),torch.tensor([-1,2]))):
            with self.assertRaises(ValueError):b.objective(z,y,b.ARMS[1])

    def test_13_nonfinite_precision_and_unknown_arm_rejected(self):
        for z,y,arm in ((torch.zeros((2,256)),torch.tensor([1,2]),b.ARMS[0]),
                        (torch.full((2,256),float("nan"),dtype=torch.float64),torch.tensor([1,2]),b.ARMS[1]),
                        (torch.zeros((2,256),dtype=torch.float64),torch.tensor([1,2]),"unknown")):
            with self.assertRaises(ValueError):b.objective(z,y,arm)

    def test_14_schedule_exposure_shape(self):
        x,p,l,plan=b.schedule(b.SEEDS[0],data_fixture()["TRAIN"])
        self.assertEqual(tuple(x.shape),(800,48));self.assertEqual(plan["per_length_row_exposures"],[[100]*192]*2)
        self.assertEqual(plan["length_profile_updates"],[[136,132,132],[132,136,132]]);self.assertEqual(int(l.sum()),400)

    def test_15_complete_pairs_and_epochs(self):
        x,_,_,_=b.schedule(b.SEEDS[0],data_fixture()["TRAIN"])
        for e in range(200):self.assertEqual(sorted(x[4*e:4*e+4].flatten().tolist()),list(range(192)))
        self.assertTrue(bool((x[:,1::2]==x[:,::2]+1).all()))

    def test_16_reproducibility_and_seed_change(self):
        r=data_fixture()["TRAIN"];a=b.schedule(b.SEEDS[0],r)[3]
        self.assertEqual(a,b.schedule(b.SEEDS[0],r)[3]);self.assertNotEqual(a,b.schedule(b.SEEDS[1],r)[3])

    def test_17_bad_pair_and_stale_seed(self):
        rows=data_fixture()["TRAIN"];rows[1]["query"]=0
        with self.assertRaises(ValueError):b.schedule(b.SEEDS[0],rows)
        with self.assertRaises(ValueError):b.schedule(286002,data_fixture()["TRAIN"])

    def test_18_initial_models_independent_and_matched(self):
        c=fixture_context()[4];m=b.make_models(b.SEEDS[0],c)
        self.assertEqual(fingerprint(m[b.ARMS[0]]),fingerprint(m[b.ARMS[1]]))
        with torch.no_grad():next(m[b.ARMS[1]].parameters()).add_(1.)
        self.assertNotEqual(fingerprint(m[b.ARMS[0]]),fingerprint(m[b.ARMS[1]]))

    def test_19_capacity_and_precision_rejected(self):
        c=fixture_context()[4];c.factory.new_model=lambda s:Weights(13489)
        with self.assertRaisesRegex(ValueError,"capacity"):b.make_models(b.SEEDS[0],c)
        c.factory.new_model=lambda s:Weights().float()
        with self.assertRaisesRegex(ValueError,"precision"):b.make_models(b.SEEDS[0],c)

    def test_20_real_fit_800_updates_and_applied_objective(self):
        tokens=torch.zeros((2,3,192,48),dtype=torch.int64);tokens[:,:,:,0]=torch.tensor([0,1]*96);tokens[1,:,:,1]=1
        targets=torch.tensor([48,49]*96);original=torch.optim.AdamW
        for arm in b.ARMS:
            observed=[]
            class Recorder(original):
                def step(self,*a,**kw):observed.append(self.param_groups[0]["lr"]);return super().step(*a,**kw)
            m=Toy()
            with patch.object(torch.optim,"AdamW",Recorder),contextlib.redirect_stdout(io.StringIO()):
                f=b.fit(m,data_fixture(),tokens,targets,b.SEEDS[0],arm)
            self.assertEqual(observed,[.005]*800);self.assertEqual(len(m.seen),800)
            self.assertEqual([p[0] for p in m.seen],[e%2 for e in range(200) for _ in range(4)])
            self.assertTrue(all(p[1]==tuple([0,1]*24) for p in m.seen));b.check_fit(f,b.SEEDS[0],arm,data_fixture())
            self.assertLess(f["last_ce"],f["ce_history"][0]);self.assertFalse(m.training)

    def test_21_fit_wrong_target_alignment_before_optimizer(self):
        with patch.object(torch.optim,"AdamW") as opt,self.assertRaisesRegex(ValueError,"alignment"):
            b.fit(None,data_fixture(),torch.zeros((2,3,192,48),dtype=torch.int64),torch.tensor([49,48]*96),b.SEEDS[0],b.ARMS[0])
        opt.assert_not_called()

    def test_22_train_then_freeze_evaluate(self):
        _,ev,tr,_,c=fixture_context();m=b.make_models(b.SEEDS[0],c)[b.ARMS[0]];events=[]
        @contextlib.contextmanager
        def counted(*a):yield [881,46176],[3524]
        c.p267.counted=counted
        def fit(model,*a):
            events.append("fit")
            with torch.no_grad():
                for p in model.parameters():p.add_(1.)
            model.eval();return {}
        def evaluate(model,*a):
            events.append("evaluate");self.assertFalse(any(p.requires_grad for p in model.parameters()));self.assertFalse(model.training);return {}
        ev.evaluate=evaluate
        with patch.object(b,"fit",side_effect=fit):b.train_one(m,{}, {}, {},None,None,b.SEEDS[0],b.ARMS[0],ev,tr,c)
        self.assertEqual(events,["fit","evaluate"])

    def test_23_objective_trace_tampering_rejected(self):
        _,d,rr=records_fixture();f=rr[1]["fit"];f["total_history"][400]+=.1
        with self.assertRaisesRegex(ValueError,"objective reconstruction"):b.check_fit(f,b.SEEDS[0],b.ARMS[1],d)
        f["total_history"][400]-=.1;f["applied_lr"][799]=.0005
        with self.assertRaisesRegex(ValueError,"schedule/LR"):b.check_fit(f,b.SEEDS[0],b.ARMS[1],d)

    def test_24_analyze_inventory_and_fitting_partitions(self):
        ctx,d,rr=records_fixture();m,s=b.analyze(rr,d,ctx[0],ctx[2],ctx[4])
        self.assertEqual((len(m),len(s["contrasts"]),len(s["final_partitions"])),(10,180,60))
        self.assertEqual(s["fitted_train_pass_counts"],dict.fromkeys(b.ARMS,5))

    def test_25_missing_nonfinite_and_mismatched_pairs_rejected(self):
        for mutate in (lambda rr:rr.pop(),lambda rr:rr[0].update(reload_max_error=float("nan")),
                       lambda rr:rr[1].update(initial_sha256="c"*64),lambda rr:rr[0]["fit"]["ce_history"].__setitem__(0,float("nan"))):
            ctx,d,rr=records_fixture();mutate(rr)
            with self.assertRaises(ValueError):b.analyze(rr,d,ctx[0],ctx[2],ctx[4])

    def test_26_control_failure_does_not_fail_candidate(self):
        p=result_fixture();p["validation_summary"]["seed_results"][0]["quad_pass"]=False;b.validate_result(recount(p))

    def test_27_candidate_failure_requires_negative_seen_gate_descriptive(self):
        p=result_fixture();p["validation_summary"]["seed_results"][1]["triple_pass"]=False;b.validate_result(recount(p))
        p["validation_summary"]["seed_results"][1]["quad_pass"]=False;recount(p)
        with self.assertRaises(ValueError):b.validate_result(p)
        p["status"]="FAIL";p["validation_summary"]["candidate_gate"]=False;b.validate_result(p)

    def test_28_scope_counts_and_missing_parent_pin(self):
        for mutate in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(new_checkpoint_writes=True),
                       lambda p:p["source_blobs"].pop(b.PARENT_SOURCE)):
            p=result_fixture();mutate(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    def test_29_parent_fourteen_hashes_and_loader_dispatch(self):
        paths=[(Path("/c288-fixture")/str(i)/"summary.json").resolve() for i in range(14)]
        mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True));payload=parent_fixture()
        parent=NS(verify_artifacts=Mock(return_value=(payload,{})),validate_result=Mock());c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        with patch.object(b,"context",return_value=(parent,None,None,None,c)):
            b.load_parent(paths);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_30_parent_scope_partitions_and_forbidden_operations(self):
        b.validate_parent(parent_fixture());p=parent_fixture();p["validation_summary"]["model_partitions"][2]["fitted_train_direct_pass"]=True
        with self.assertRaisesRegex(ValueError,"deciding partitions"):b.validate_parent(p)
        paths=[Path(str(i)).resolve() for i in range(14)];mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        for action in (lambda *a:torch.nn.Identity()(torch.ones(1)),lambda *a:torch.nn.Linear(1,1).load_state_dict({}),lambda *a:torch.save({},"FORBIDDEN.pt")):
            parent=NS(verify_artifacts=Mock(side_effect=action));c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
            with patch.object(b,"context",return_value=(parent,None,None,None,c)),self.assertRaisesRegex(RuntimeError,"C288 parent forbids"):b.load_parent(paths)
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_31_precheck_real_file_maps_and_missing_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);lm=[f"fold_lm/fixture{i}.py" for i in range(6)]
            names=[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,288)]
            names[-1]=b.PARENT_SOURCE;names+=lm;names += [f"accepted/{i}.txt" for i in range(568-len(names))]
            pins={n:(b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40) for n in names}
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n)
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1016-len(inputs)):
                p=root/f"input{i}";p.write_text("input");inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();summary=directory/"summary.json";summary.write_text("summary")
            mapping={str(summary.resolve()):b.SUMMARY_SHAS[0]}
            for n,(sha,size) in b.PARENT_ARTIFACTS.items():p=directory/n;p.write_text("parent");mapping[str(p.resolve())]=sha
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*a):return (pins.get(a[1][5:],"c"*40)+"\n").encode()
            def protect(root,ps):return {str((root/n).resolve()):sha(root/n) for n in ps}
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=protect),factory=NS(LM_SOURCES=lm))
            with patch.object(b,"context",return_value=(None,None,None,None,c)),patch.object(b,"load_parent",return_value=dict(source_blobs=pins,input_sha256=inputs)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*14,root))),(574,1026))
                pins.pop(b.PARENT_SOURCE)
                with self.assertRaises(ValueError):b.precheck([summary]*14,root)

    def test_32_suite_actual_construction_and_duplicate_rejection(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
            self.assertEqual(suite.countTestCases(),b.manifest()["focused_tests"])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())

    def test_33_context_dispatch(self):
        import types
        package=types.ModuleType("fold_lm.v05_benchmarks");c=NS();evaluation=NS();transfer=NS();training=NS()
        c286=NS(context=lambda:(None,evaluation,transfer,training,c));parent=NS(context=lambda:(c286,c))
        package.model_c287_saved_fit_partition_audit=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):self.assertEqual(b.context(),(parent,evaluation,transfer,training,c))

    def test_34_actual_run_roundtrip_order_and_no_overwrite(self):
        ctx,d,rr=records_fixture();events=[]
        def train(m,data,t,q,x,y,seed,arm,*a):events.append("train");return copy.deepcopy(rr[b.identities().index((seed,arm))]),{"x":torch.ones(1)}
        def pc(*a):events.append("precheck");return protection()
        ctx[1].replay_one.side_effect=lambda *a:events.append("replay")
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=ctx),patch.object(b,"precheck",side_effect=pc),patch.object(b,"load_parent",return_value=parent_fixture()),patch.object(b,"train_one",side_effect=train),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*14,output_dir=out,expected_head="f"*40)
            self.assertEqual(events,["precheck"]+["train"]*10+["replay"]*10+["precheck"])
            q,_=b.verify_artifacts(out,["x"]*14,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*14,output_dir=out,expected_head="f"*40)

    def test_35_hash_and_semantic_artifact_tampering(self):
        ctx,d,rr=records_fixture()
        def train(m,data,t,q,x,y,s,a,*args):return copy.deepcopy(rr[b.identities().index((s,a))]),{"x":torch.ones(1)}
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=ctx),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=parent_fixture()),patch.object(b,"train_one",side_effect=train),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*14,output_dir=out,expected_head="f"*40)
            f=out/"measurements.json";f.write_text("[]")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*14,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==f.name);a.update(sha256=Audit.sha(f),serialized_bytes=f.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*14,"f"*40)

    def test_36_bad_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"bad.pt";torch.save(dict(schema="wrong",identities=[],states=[]),p)
            with self.assertRaises(ValueError):b.load_bundle(p)

    def test_37_cli_fourteen_paths(self):
        argv=["prog","--summaries"]+[str(i) for i in range(14)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:
            b.main();self.assertEqual(run.call_args.kwargs["summaries"],[Path(str(i)) for i in range(14)])

    def test_38_runner_python_blocks_and_publication_order(self):
        root=Path(__file__).resolve().parents[1];r=(root/"tools/run_c288.ps1").read_text(encoding="utf-8");l=(root/"tools/invoke_c288.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",r,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:16]",blocks[2]);self.assertIn("head = sys.argv[16]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',l)),14)
        self.assertLess(l.index("-Mode Validate"),l.index("-Mode Execute"));self.assertLess(l.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),l.index("publish_experiment_log.ps1"))
        self.assertIn("Parser]::ParseFile",l)

    def test_39_immutable_inventory_and_only_direct_parent_import(self):
        root=Path(__file__).resolve().parents[1];self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])
        for n in b.OWN:self.assertTrue((root/n).is_file())
        imports=[n for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c287_saved_fit_partition_audit"])
        self.assertEqual(b.manifest()["source_pins"],568+len(b.OWN));self.assertEqual(b.manifest()["protected_inputs"],1016+4+len(b.OWN))

    def test_40_repository_guards(self):
        c=NS(audit=Audit());b.guard(Path.cwd(),"f"*40,c)
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,c)
        def git(root,*a):return b"dirty" if a[0]=="status" else Audit.git(root,*a)
        c.audit=NS(git=git)
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"f"*40,c)


if __name__=="__main__":unittest.main()
