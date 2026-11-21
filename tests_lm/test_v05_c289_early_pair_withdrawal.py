"""C289 behavioral fixtures; real inherited archives and models remain runtime gates."""
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
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock,patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c289_early_pair_withdrawal as b


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
    def normalize(tm,task,seed,arm):return [dict(split=s,passed=tm["passed"],direct_pass=tm["passed"]) for s in ("TRAIN","HOLDOUT")]
    def partition(rr):return dict(direct_pass=all(r["direct_pass"] for r in rr),full_pass=all(r["passed"] for r in rr))
    diagnostic=NS(normalize_task=normalize,partition=partition)
    c=NS(audit=Audit(),p267=NS(dataset=data_fixture,validate_data=lambda d:None,score=lambda d,r:r),
         c270=NS(prompt_dataset=lambda *a:{"triple":True},validate_dataset=lambda *a:None,score=lambda d,r,p:r),
         c278=NS(MeanFinalDualReadout=Readout),c269=NS(query_span_mask=None),factory=NS(new_model=lambda s:Weights()),
         reader=None,base=NS(fingerprint=fingerprint),core=None)
    transfer=NS(dataset=lambda d:{"quad":True},validate_dataset=lambda *a:None,score_quad=lambda d,r,c:r)
    training=NS(training_tables=lambda d,c:(torch.zeros((2,3,192,48),dtype=torch.int64),torch.tensor([48,49]*96)))
    return NS(),diagnostic,NS(replay_one=Mock()),transfer,training,c


def records_fixture():
    ctx=fixture_context();data=data_fixture();records=[]
    for seed,arm in b.identities():
        weights=b.weight_schedule(arm)
        fit=dict(steps=800,training_rows=38400,optimizer_creations=1,step400_sha256="c"*64,
                 ce_history=[.1]*800,pair_history=[.5]*800,total_history=[.1+w*.5 for w in weights],
                 applied_lr=[.005]*800,applied_weight=weights,last_ce=.1,**b.schedule(seed,data["TRAIN"])[3])
        records.append(dict(seed=seed,arm=arm,parameters=14256,weights_changed=True,checkpoint_roundtrip=True,
                            initial_sha256="a"*64,final_sha256="b"*64,reload_max_error=0.,fit=fit,raw={t:scored(t) for t in b.TASKS},
                            forward_calls=881,row_presentations=46176,core_forward_calls=3524,
                            replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    return ctx,data,records


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<580:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1041)}


def result_fixture():
    ctx,d,rr=records_fixture();_,s=b.analyze(rr,d,ctx[1],ctx[3],ctx[5]);pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
                gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False,
                source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s)


def recount(p):
    s=p["validation_summary"];rr=s["seed_results"]
    for r in rr:r["passed"]=r["quad_pass"];r["all_tasks_pass"]=all(r[t+"_pass"] for t in b.TASKS)
    for name,field in b.COUNT_FIELDS:s[name]={a:sum(r[field] for r in rr if r["arm"]==a) for a in b.ARMS}
    return p


def parent_fixture():
    return dict(commit_sha=b.PARENT_EXECUTION,status="FAIL",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
                artifacts=[dict(file=n,sha256=v[0],serialized_bytes=v[1]) for n,v in b.PARENT_ARTIFACTS.items()],
                validation_summary=dict(seed_results=b.expected_parent_results(),candidate_gate=False,all_replays=True,
                    all_pairs_matched=True,quad_pass_counts={"ce_only":3,"ce_pair_assignment":1},
                    fitted_train_pass_counts={"ce_only":3,"ce_pair_assignment":5}))


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__();self.bias=torch.nn.Parameter(torch.zeros(256,dtype=torch.float64))
        self.query=torch.nn.Parameter(torch.zeros(256,dtype=torch.float64));self.seen=[]
    def forward(self,x,t):
        assert len(x)==48 and t.shape==(48,) and bool((t==0).all())
        self.seen.append(int(x[0,1]))
        return self.bias[None,:]+(2*x[:,0].to(torch.float64)-1)[:,None]*self.query[None,:]


class C289Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.rng=torch.random.get_rng_state()
        cls.deterministic=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
        cls.fits={};cls.models={};cls.optimizer_calls={};cls.lr_steps={};cls.optimizer_steps={}
        tokens=torch.zeros((2,3,192,48),dtype=torch.int64);tokens[:,:,:,0]=torch.tensor([0,1]*96);tokens[1,:,:,1]=1
        targets=torch.tensor([48,49]*96);original=torch.optim.AdamW
        for arm in b.ARMS:
            made=[];rates=[];steps=[]
            class Recorder(original):
                def __init__(self,*a,**kw):
                    super().__init__(*a,**kw);made.append(self)
                def step(self,*a,**kw):
                    rates.append(float(self.param_groups[0]["lr"]));answer=super().step(*a,**kw)
                    p=self.param_groups[0]["params"][0];steps.append(int(self.state[p]["step"]));return answer
            model=Toy()
            with patch.object(torch.optim,"AdamW",Recorder),contextlib.redirect_stdout(io.StringIO()):
                cls.fits[arm]=b.fit(model,data_fixture(),tokens,targets,b.SEEDS[0],arm,NS(base=NS(fingerprint=fingerprint)))
            cls.models[arm]=model;cls.optimizer_calls[arm]=len(made);cls.lr_steps[arm]=rates;cls.optimizer_steps[arm]=steps
    @classmethod
    def tearDownClass(cls):
        torch.set_num_threads(cls.threads);torch.random.set_rng_state(cls.rng);torch.use_deterministic_algorithms(cls.deterministic)

    def test_01_real_seal(self):
        b.validate_seal();self.assertEqual(b.MANIFEST_SHA,b.digest(b.manifest()))

    def test_02_bad_seals(self):
        for sha in ("UNSEALED","0"*64,"F"*64):
            with patch.object(b,"MANIFEST_SHA",sha),self.assertRaises(ValueError):b.validate_seal()

    def test_03_three_schedules_and_switch_boundary(self):
        self.assertEqual(b.weight_schedule("ce_only"),[0.]*800)
        self.assertEqual(b.weight_schedule("pair_always"),[.25]*800)
        w=b.weight_schedule("pair_early");self.assertEqual(w,[.25]*400+[0.]*400)
        self.assertEqual((w[399],w[400]),(.25,0.))

    def test_04_bad_arm_and_objective_weight(self):
        with self.assertRaises(ValueError):b.weight_schedule("ce_pair_assignment")
        for w in (.1,True):
            with self.assertRaises(ValueError):b.objective(torch.zeros((2,256),dtype=torch.float64),torch.tensor([1,2]),w)

    def test_05_objective_zero_logits(self):
        t,ce,pair=b.objective(torch.zeros((2,256),dtype=torch.float64),torch.tensor([1,2]),.25)
        self.assertAlmostEqual(float(ce),math.log(256));self.assertAlmostEqual(float(pair),math.log1p(math.e))
        self.assertAlmostEqual(float(t),math.log(256)+.25*math.log1p(math.e))

    def test_06_disabled_aux_exact_ce_value_and_gradient(self):
        z=torch.linspace(-1,1,512,dtype=torch.float64).reshape(2,256).requires_grad_();y=torch.tensor([1,2])
        total,_,_=b.objective(z,y,0.);ref=F.cross_entropy(z,y)
        self.assertTrue(torch.equal(total,ref));self.assertTrue(torch.equal(torch.autograd.grad(total,z)[0],torch.autograd.grad(ref,z)[0]))

    def test_07_enabled_objective_finite_difference(self):
        mask=torch.zeros((2,2,256),dtype=torch.float64);mask[0,0,1]=1.;mask[1,1,2]=1.
        def fn(x):return b.objective((x[:,None,None]*mask).sum(0),torch.tensor([1,2]),.25)[0]
        self.assertTrue(torch.autograd.gradcheck(fn,(torch.tensor([.2,-.1],dtype=torch.float64,requires_grad=True),)))

    def test_08_pair_margin_semantics(self):
        z=torch.zeros((2,256),dtype=torch.float64);z[0,1]=2.;z[1,2]=2.;y=torch.tensor([1,2])
        good=b.objective(z,y,.25)[2];bad=b.objective(z.flip(0),y,.25)[2]
        self.assertLess(float(good),float(bad));self.assertEqual(float(good),float(b.objective(z.flip(0),y.flip(0),.25)[2]))

    def test_09_identical_queries_and_no_individual_accuracy_guarantee(self):
        z=torch.zeros((2,256),dtype=torch.float64);z[:,1]=100.;y=torch.tensor([1,2])
        self.assertAlmostEqual(float(b.objective(z,y,.25)[2]),math.log1p(math.e))
        z.zero_();z[0,1]=20.;z[1,1]=1.;_,ce,pair=b.objective(z,y,.25)
        self.assertLess(float(pair),1e-6);self.assertGreater(float(ce),1.)

    def test_10_bad_objective_shapes_targets_and_nonfinite(self):
        for z,y in ((torch.zeros((3,256),dtype=torch.float64),torch.tensor([1,2,3])),
                    (torch.zeros((2,255),dtype=torch.float64),torch.tensor([1,2])),
                    (torch.zeros((2,256),dtype=torch.float64),torch.tensor([1,1])),
                    (torch.zeros((2,256),dtype=torch.float64),torch.tensor([-1,2])),
                    (torch.full((2,256),float("nan"),dtype=torch.float64),torch.tensor([1,2])),
                    (torch.zeros((2,256)),torch.tensor([1,2]))):
            with self.assertRaises(ValueError):b.objective(z,y,.25)

    def test_11_schedule_coverage_and_shape(self):
        x,p,l,plan=b.schedule(b.SEEDS[0],data_fixture()["TRAIN"])
        self.assertEqual(tuple(x.shape),(800,48));self.assertEqual(int(l.sum()),400)
        self.assertEqual(plan["per_length_row_exposures"],[[100]*192]*2)
        self.assertEqual(plan["length_profile_updates"],[[136,132,132],[132,136,132]])

    def test_12_pairs_complete_each_epoch(self):
        x,_,_,_=b.schedule(b.SEEDS[0],data_fixture()["TRAIN"])
        for e in range(200):self.assertEqual(sorted(x[4*e:4*e+4].flatten().tolist()),list(range(192)))
        self.assertTrue(bool((x[:,1::2]==x[:,::2]+1).all()))

    def test_13_schedule_reproducible_fresh_seed(self):
        rows=data_fixture()["TRAIN"];a=b.schedule(b.SEEDS[0],rows)[3]
        self.assertEqual(a,b.schedule(b.SEEDS[0],rows)[3]);self.assertNotEqual(a,b.schedule(b.SEEDS[1],rows)[3])
        with self.assertRaises(ValueError):b.schedule(288001,rows)

    def test_14_bad_pair_rejected(self):
        rows=data_fixture()["TRAIN"];rows[1]["query"]=0
        with self.assertRaisesRegex(ValueError,"complete query pair"):b.schedule(b.SEEDS[0],rows)

    def test_15_three_initial_models_match(self):
        c=fixture_context()[5];models=b.make_models(b.SEEDS[0],c)
        self.assertEqual(list(models),list(b.ARMS));self.assertEqual(len({fingerprint(m) for m in models.values()}),1)
        for a,d in itertools.combinations(models.values(),2):
            self.assertTrue(all(x.data_ptr()!=y.data_ptr() for x,y in zip(a.parameters(),d.parameters(),strict=True)))

    def test_16_capacity_precision_and_mutation_isolation(self):
        c=fixture_context()[5];models=b.make_models(b.SEEDS[0],c)
        with torch.no_grad():next(models[b.ARMS[2]].parameters()).add_(1.)
        self.assertEqual(fingerprint(models[b.ARMS[0]]),fingerprint(models[b.ARMS[1]]))
        self.assertNotEqual(fingerprint(models[b.ARMS[0]]),fingerprint(models[b.ARMS[2]]))
        for fn in (lambda s:Weights(13489),lambda s:Weights().float()):
            c.factory.new_model=fn
            with self.assertRaises(ValueError):b.make_models(b.SEEDS[0],c)

    def test_17_real_fit_all800_steps_and_data(self):
        for arm in b.ARMS:
            self.assertEqual(self.lr_steps[arm],[.005]*800)
            self.assertEqual(self.models[arm].seen,[e%2 for e in range(200) for _ in range(4)])
            self.assertFalse(self.models[arm].training);b.check_fit(self.fits[arm],b.SEEDS[0],arm,data_fixture())

    def test_18_optimizer_never_recreated_or_reset(self):
        for arm in b.ARMS:
            self.assertEqual(self.optimizer_calls[arm],1);self.assertEqual(self.optimizer_steps[arm],list(range(1,801)))
            self.assertEqual(self.fits[arm]["optimizer_creations"],1)

    def test_19_real_common_prefix_and_later_divergence(self):
        a,c=(self.fits[x] for x in b.ARMS[1:])
        self.assertEqual(a["step400_sha256"],c["step400_sha256"])
        for k in ("ce_history","pair_history","total_history"):self.assertEqual(a[k][:400],c[k][:400])
        self.assertNotEqual(fingerprint(self.models[b.ARMS[1]]),fingerprint(self.models[b.ARMS[2]]))

    def test_20_weight_trace_applied_at_correct_update(self):
        for arm in b.ARMS:self.assertEqual(self.fits[arm]["applied_weight"],b.weight_schedule(arm))
        f=self.fits["pair_early"]
        self.assertTrue(all(t==ce for t,ce in zip(f["total_history"][400:],f["ce_history"][400:],strict=True)))

    def test_21_bad_fit_alignment_before_optimizer(self):
        with patch.object(torch.optim,"AdamW") as opt,self.assertRaisesRegex(ValueError,"alignment"):
            b.fit(None,data_fixture(),torch.zeros((2,3,192,48),dtype=torch.int64),torch.tensor([49,48]*96),b.SEEDS[0],b.ARMS[0],None)
        opt.assert_not_called()

    def test_22_nonfinite_fit_fails(self):
        model=Toy()
        with torch.no_grad():model.bias.fill_(float("nan"))
        with self.assertRaisesRegex(ValueError,"objective finite"):
            b.fit(model,data_fixture(),torch.zeros((2,3,192,48),dtype=torch.int64),torch.tensor([48,49]*96),b.SEEDS[0],b.ARMS[0],NS())

    def test_23_check_fit_rejects_loss_and_weight_tamper(self):
        for fn in (lambda f:f["total_history"].__setitem__(500,9.),lambda f:f["applied_weight"].__setitem__(400,.25),
                   lambda f:f.update(optimizer_creations=2),lambda f:f["ce_history"].__setitem__(0,float("nan"))):
            f=copy.deepcopy(self.fits["pair_early"]);fn(f)
            with self.assertRaises(ValueError):b.check_fit(f,b.SEEDS[0],"pair_early",data_fixture())

    def test_24_matched_group_rejects_prefix_or_initial_mismatch(self):
        for fn in (lambda r:r[2]["fit"].update(step400_sha256="d"*64),lambda r:r[2]["fit"]["pair_history"].__setitem__(399,.51),
                   lambda r:r[0].update(initial_sha256="e"*64)):
            _,_,r=records_fixture();fn(r)
            with self.assertRaises(ValueError):b.check_matched_group(r[:3])

    def test_25_primary_and_comparator_inventory(self):
        ctx,d,r=records_fixture();m,s=b.analyze(r,d,ctx[1],ctx[3],ctx[5])
        self.assertEqual((len(m),len(s["final_partitions"]),len(s["contrasts"])),(15,90,360))
        self.assertEqual({x["comparator"] for x in s["contrasts"]},set(b.ARMS[:2]))
        self.assertTrue(s["all_auxiliary_prefixes_matched"])
        self.assertEqual(s["quad_pass_counts"],dict.fromkeys(b.ARMS,5))

    def test_26_comparator_failure_cannot_fail_candidate(self):
        for i in (0,1):
            p=result_fixture();p["validation_summary"]["seed_results"][i]["quad_pass"]=False;b.validate_result(recount(p))

    def test_27_candidate_single_miss_must_be_negative(self):
        p=result_fixture();p["validation_summary"]["seed_results"][2]["quad_pass"]=False;recount(p)
        with self.assertRaisesRegex(ValueError,"candidate gate"):b.validate_result(p)
        p["status"]="FAIL";p["validation_summary"]["candidate_gate"]=False;b.validate_result(p)

    def test_28_seen_task_is_descriptive_not_primary(self):
        p=result_fixture();p["validation_summary"]["seed_results"][2]["triple_pass"]=False;b.validate_result(recount(p))

    def test_29_matching_scope_counts_and_roles_rejected(self):
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(all_auxiliary_prefixes_matched=False),
                   lambda p:p["validation_summary"].update(models=True),lambda p:p["source_blobs"].pop(b.PARENT_SOURCE),
                   lambda p:p["validation_summary"]["contrasts"][0].update(candidate="pair_always")):
            p=result_fixture();fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    def test_30_analyze_missing_state_and_replay_mismatch(self):
        for fn in (lambda r:r.pop(),lambda r:r[0].update(reload_max_error=1e-3)):
            ctx,d,r=records_fixture();fn(r)
            with self.assertRaises(ValueError):b.analyze(r,d,ctx[1],ctx[3],ctx[5])

    def test_31_parent_exact_flags_and_artifacts(self):
        b.validate_parent(parent_fixture())
        for fn in (lambda p:p.update(status="PASS"),lambda p:p["source_blobs"].clear(),
                   lambda p:p["artifacts"][0].update(serialized_bytes=0),lambda p:p["validation_summary"]["seed_results"][1].update(quad_pass=True)):
            p=parent_fixture();fn(p)
            with self.assertRaises(ValueError):b.validate_parent(p)

    def test_32_all_fifteen_hashes_and_loader_dispatch(self):
        paths=[(Path("/c289-fixture")/str(i)/"summary.json").resolve() for i in range(15)]
        mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True));p=parent_fixture()
        parent=NS(verify_artifacts=Mock(return_value=(p,[])),validate_result=Mock());c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        with patch.object(b,"context",return_value=(parent,None,None,None,None,c)):
            b.load_parent(paths);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_33_parent_forbidden_operations(self):
        paths=[Path(str(i)).resolve() for i in range(15)];mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        for action in (lambda *a:torch.nn.Identity()(torch.ones(1)),lambda *a:torch.nn.Linear(1,1).load_state_dict({}),lambda *a:torch.save({},"FORBIDDEN.pt")):
            parent=NS(verify_artifacts=Mock(side_effect=action))
            with patch.object(b,"context",return_value=(parent,None,None,None,None,c)),self.assertRaisesRegex(RuntimeError,"C289 parent forbids"):b.load_parent(paths)
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_34_context_chain(self):
        import types
        package=types.ModuleType("fold_lm.v05_benchmarks");d,e,t,tr,c=(NS() for _ in range(5))
        parent=NS(context=lambda:(d,e,t,tr,c));package.model_c288_query_pair_assignment_loss=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):self.assertEqual(b.context(),(parent,d,e,t,tr,c))

    def test_35_actual_precheck_maps_and_dependency_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);lm=[f"fold_lm/fixture{i}.py" for i in range(6)]
            names=[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,289)]
            names[-1]=b.PARENT_SOURCE;names+=lm;names += [f"accepted/{i}.txt" for i in range(574-len(names))]
            pins={n:(b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40) for n in names}
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n)
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1026-len(inputs)):
                p=root/f"input{i}";p.write_text("input");inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();summary=directory/"summary.json";summary.write_text("summary")
            mapping={str(summary.resolve()):b.SUMMARY_SHAS[0]}
            for n,(sha,size) in b.PARENT_ARTIFACTS.items():p=directory/n;p.write_text("parent");mapping[str(p.resolve())]=sha
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*a):return (pins.get(a[1][5:],"c"*40)+"\n").encode()
            def protect(root,ps):return {str((root/n).resolve()):sha(root/n) for n in ps}
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=protect),factory=NS(LM_SOURCES=lm))
            with patch.object(b,"context",return_value=(None,None,None,None,None,c)),patch.object(b,"load_parent",return_value=dict(source_blobs=pins,input_sha256=inputs)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*15,root))),(580,1041))
                pins.pop(b.PARENT_SOURCE)
                with self.assertRaises(ValueError):b.precheck([summary]*15,root)

    def test_36_real_suite_filter(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
            self.assertEqual(suite.countTestCases(),b.manifest()["focused_tests"])

    def test_37_duplicate_suite_rejected(self):
        class Dummy(unittest.TestCase):
            def runTest(self):pass
            def id(self):return "duplicate"
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy(),Dummy()])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())

    def test_38_train_freeze_evaluate_order(self):
        _,_,ev,tr,_,c=fixture_context();m=b.make_models(b.SEEDS[0],c)[b.ARMS[0]];events=[]
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

    def test_39_run_roundtrip_and_order(self):
        ctx,d,rr=records_fixture();events=[]
        def train(m,data,t,q,x,y,s,a,*args):events.append("train");return copy.deepcopy(rr[b.identities().index((s,a))]),{"x":torch.ones(1)}
        def pc(*a):events.append("precheck");return protection()
        ctx[2].replay_one.side_effect=lambda *a:events.append("replay")
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=ctx),patch.object(b,"precheck",side_effect=pc),patch.object(b,"load_parent",return_value=parent_fixture()),patch.object(b,"train_one",side_effect=train),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*15,output_dir=out,expected_head="f"*40)
            self.assertEqual(events,["precheck"]+["train"]*15+["replay"]*15+["precheck"])
            q,_=b.verify_artifacts(out,["x"]*15,"f"*40);self.assertEqual(q,p)
            self.assertEqual({x.name for x in out.iterdir()},set(b.OUTPUTS)|{"summary.json"})
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*15,output_dir=out,expected_head="f"*40)

    def test_40_output_hash_and_semantic_tamper(self):
        ctx,d,rr=records_fixture()
        def train(m,data,t,q,x,y,s,a,*args):return copy.deepcopy(rr[b.identities().index((s,a))]),{"x":torch.ones(1)}
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=ctx),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=parent_fixture()),patch.object(b,"train_one",side_effect=train),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*15,output_dir=out,expected_head="f"*40)
            f=out/"measurements.json";f.write_text("[]")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*15,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==f.name);a.update(sha256=Audit.sha(f),serialized_bytes=f.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*15,"f"*40)

    def test_41_checkpoint_wrong_count_or_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"bad.pt"
            for v in (dict(schema="wrong"),dict(schema="fold-c289-early-pair-models-v1",identities=[list(i) for i in b.identities()],states=[{}]*14)):
                torch.save(v,p)
                with self.assertRaises(ValueError):b.load_bundle(p)

    def test_42_cli_fifteen_paths(self):
        argv=["prog","--summaries"]+[str(i) for i in range(15)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:
            b.main();self.assertEqual(run.call_args.kwargs["summaries"],[Path(str(i)) for i in range(15)])

    def test_43_runner_blocks_cli_and_publication(self):
        root=Path(__file__).resolve().parents[1];r=(root/"tools/run_c289.ps1").read_text(encoding="utf-8");l=(root/"tools/invoke_c289.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",r,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:17]",blocks[2]);self.assertIn("head = sys.argv[17]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',l)),15)
        self.assertLess(l.index("-Mode Validate"),l.index("-Mode Execute"));self.assertLess(l.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),l.index("publish_experiment_log.ps1"))
        self.assertIn("Parser]::ParseFile",l)

    def test_44_immutable_inventory_and_direct_import(self):
        root=Path(__file__).resolve().parents[1];self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])
        for n in b.OWN:self.assertTrue((root/n).is_file())
        imports=[n for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c288_query_pair_assignment_loss"])
        self.assertEqual(b.manifest()["source_pins"],574+len(b.OWN));self.assertEqual(b.manifest()["protected_inputs"],1026+9+len(b.OWN))

    def test_45_repository_guards(self):
        c=NS(audit=Audit());b.guard(Path.cwd(),"f"*40,c)
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,c)
        def git(root,*a):return b"dirty" if a[0]=="status" else Audit.git(root,*a)
        c.audit=NS(git=git)
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"f"*40,c)

    def test_46_group_wrong_order_rejected(self):
        _,_,r=records_fixture();b.check_matched_group(r[:3]);r[0],r[1]=r[1],r[0]
        with self.assertRaises(ValueError):b.check_matched_group(r[:3])

    def test_47_contrast_identity_mismatch_rejected(self):
        ctx,d,r=records_fixture();r[2]["raw"]["quad"]["totals"][0]["language"]="other"
        with self.assertRaisesRegex(ValueError,"contrast identity"):b.analyze(r,d,ctx[1],ctx[3],ctx[5])

    def test_48_all_three_counts_and_no_old_primary(self):
        p=result_fixture();self.assertEqual(p["validation_summary"]["models"],15)
        self.assertEqual(p["validation_summary"]["train_steps"],15*800)
        self.assertEqual(p["validation_summary"]["model_forward_calls"],15*(800+81+81))
        p["validation_summary"]["quad_pass_counts"].pop("ce_only")
        with self.assertRaises(ValueError):b.validate_result(p)


if __name__=="__main__":unittest.main()
