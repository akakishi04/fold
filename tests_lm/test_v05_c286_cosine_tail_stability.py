"""C286 behavioral fixtures; actual parent archives and inherited models are runtime gates."""
import ast
import contextlib
import copy
import hashlib
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c286_cosine_tail_stability as b


def data_fixture():
    return dict(TRAIN=[dict(language="en",entities=[0,1],values=[i,i+1],permutation=[0,1],query=q,
                           target=48+q,id=f"{i}:{q}") for i in range(96) for q in range(2)],HOLDOUT=[])


def fingerprint(model):
    return hashlib.sha256(b"".join(v.detach().cpu().numpy().tobytes() for v in model.state_dict().values())).hexdigest()


class Weights(torch.nn.Module):
    def __init__(self,n=13488):
        super().__init__(); self.weight=torch.nn.Parameter(torch.ones(n,dtype=torch.float64))


class Readout(torch.nn.Module):
    def __init__(self,backbone,seed,reader,span):
        super().__init__(); self.backbone=backbone; self.read=Weights(768)


class Audit:
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch": return b"feat/sft-target-loss\n"
        return b""
    @staticmethod
    def sha(p):
        p=Path(p); return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n): return Path(root)/n


def fixture_context():
    c=NS(audit=Audit(),p267=NS(dataset=data_fixture,validate_data=lambda d:None,score=lambda d,r:r),
         c270=NS(prompt_dataset=lambda *a:{"triple":True},validate_dataset=lambda *a:None,score=lambda d,r,p:r),
         c278=NS(MeanFinalDualReadout=Readout),c269=NS(query_span_mask=None),
         factory=NS(new_model=lambda s:Weights()),reader=None,base=NS(fingerprint=fingerprint),core=None)
    transfer=NS(dataset=lambda d:{"quad":True},validate_dataset=lambda *a:None,score_quad=lambda d,r,c:r)
    training=NS(training_tables=lambda d,c:(torch.zeros((2,3,192,48),dtype=torch.int64),torch.tensor([48,49]*96)))
    return NS(),NS(replay_one=Mock()),transfer,training,c


def scored(task):
    profiles={"two_char":("doubled","shared_prefix","shared_suffix"),
              "triple":("tripled","shared_prefix2","shared_suffix2"),
              "quad":("quadrupled","shared_prefix3","shared_suffix3")}[task]
    totals=[dict(split=s,profile=p,language=l,rows=n,pairs=n//2,correct=n,collapsed_pairs=0)
            for s,n in (("TRAIN",96),("HOLDOUT",48)) for p in profiles for l in ("en","ja")]
    return dict(passed=True,totals=totals)


def records_fixture():
    context=fixture_context(); data=data_fixture(); rr=[]
    for seed,arm in b.identities():
        rates=b.learning_rates(arm)
        fit=dict(steps=800,training_rows=38400,step400_sha256="a"*64,applied_lr=rates,
                 lr_sha256=b.digest(rates),loss_history=[.01]*800,last_ce=.01,**b.schedule(seed,data["TRAIN"])[3])
        rr.append(dict(seed=seed,arm=arm,parameters=14256,initial_sha256="initial",final_sha256="final",weights_changed=True,
                       checkpoint_roundtrip=True,reload_max_error=0.,fit=fit,raw={t:scored(t) for t in b.TASKS},
                       forward_calls=881,row_presentations=46176,core_forward_calls=3524,
                       replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    return context,data,rr


def protection():
    pins={n:"b"*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<562: pins["fixture/source/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1001)}


def result_fixture():
    ctx,d,rr=records_fixture(); _,summary=b.analyze(rr,d,ctx[2],ctx[4]); pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
                gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False,source_blobs=pins,input_sha256=inputs,
                artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary)


def recount(p):
    s=p["validation_summary"]; rr=s["seed_results"]
    for r in rr: r["passed"]=r["quad_pass"]; r["all_tasks_pass"]=all(r[t+"_pass"] for t in b.TASKS)
    for out,field in (("seed_pass_counts","passed"),("two_char_pass_counts","two_char_pass"),("triple_pass_counts","triple_pass"),
                      ("quad_pass_counts","quad_pass"),("all_tasks_pass_counts","all_tasks_pass")):
        s[out]={a:sum(r[field] for r in rr if r["arm"]==a) for a in b.ARMS}
    return p


def parent_fixture():
    return dict(commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
                artifacts=[dict(file=n,sha256=v[0],serialized_bytes=v[1]) for n,v in b.PARENT_ARTIFACTS.items()],
                validation_summary=dict(diagnostic_complete=True,capability_gate_applicable=False,model_forward_calls=0,
                  primary=dict(triple_to_quad=dict(mixed_length=dict(criteria=dict(accuracy=dict(both_fail=37,left_pass_right_fail=6,right_fail=43)))))))


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.bias=torch.nn.Parameter(torch.zeros(256,dtype=torch.float64)); self.seen=[]
    def forward(self,x,t):
        self.seen.append(int(x[0,0])); assert len(x)==48 and bool((t==0).all())
        return self.bias.expand(len(x),-1)


class C286Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.deterministic=torch.are_deterministic_algorithms_enabled()
        cls.rng=torch.random.get_rng_state();torch.set_num_threads(2)
        cls.fits={};cls.lr_steps={};cls.toys={}
        x=torch.zeros((2,3,192,48),dtype=torch.int64);x[1]=1;y=torch.tensor([48,49]*96)
        original=torch.optim.AdamW
        for arm in b.ARMS:
            observed=[]
            class Recorder(original):
                def step(self,*args,**kwargs):
                    observed.append(float(self.param_groups[0]["lr"]));return super().step(*args,**kwargs)
            model=Toy()
            with patch.object(torch.optim,"AdamW",Recorder),contextlib.redirect_stdout(io.StringIO()):
                cls.fits[arm]=b.fit(model,data_fixture(),x,y,b.SEEDS[0],arm,NS(base=NS(fingerprint=fingerprint)))
            cls.lr_steps[arm]=observed;cls.toys[arm]=model
    @classmethod
    def tearDownClass(cls):
        torch.set_num_threads(cls.threads);torch.use_deterministic_algorithms(cls.deterministic);torch.random.set_rng_state(cls.rng)

    def test_01_seal_executes(self):
        b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_invalid_seals_rejected(self):
        for seal in ("UNSEALED","F"*64,"0"*64):
            with patch.object(b,"MANIFEST_SHA",seal),self.assertRaises(ValueError):b.validate_seal()

    def test_03_first400_learning_rates_identical(self):
        a,c=map(b.learning_rates,b.ARMS);self.assertEqual(a[:400],c[:400]);self.assertEqual(c[:400],[.005]*400)

    def test_04_lr_endpoints_and_indexing(self):
        a,c=map(b.learning_rates,b.ARMS);self.assertEqual(a,[.005]*800)
        self.assertEqual(c[399],.005);self.assertLess(c[400],.005)
        self.assertAlmostEqual(c[599],.00275);self.assertEqual(c[799],.0005)

    def test_05_tail_monotone_and_finite(self):
        rates=b.learning_rates(b.ARMS[1]);self.assertTrue(all(.0005<=x<=.005 for x in rates))
        self.assertTrue(all(a>b for a,b in zip(rates[399:-1],rates[400:],strict=True)))

    def test_06_unknown_lr_arm_rejected(self):
        with self.assertRaises(ValueError):b.learning_rates("other")

    def test_07_exposure_and_shape(self):
        x,p,l,plan=b.schedule(b.SEEDS[0],data_fixture()["TRAIN"])
        self.assertEqual(tuple(x.shape),(800,48));self.assertEqual(plan["per_length_row_exposures"],[[100]*192]*2)
        self.assertEqual(plan["length_profile_updates"],[[136,132,132],[132,136,132]])
        self.assertEqual(int(l.sum()),400)

    def test_08_complete_query_pairs_every_epoch(self):
        x,_,_,_=b.schedule(b.SEEDS[0],data_fixture()["TRAIN"])
        for e in range(200):self.assertEqual(sorted(x[e*4:(e+1)*4].flatten().tolist()),list(range(192)))
        self.assertTrue(bool((x[:,1::2]==x[:,::2]+1).all()))

    def test_09_seed_reproducibility(self):
        rows=data_fixture()["TRAIN"];a=b.schedule(b.SEEDS[0],rows)[3]
        self.assertEqual(a,b.schedule(b.SEEDS[0],rows)[3]);self.assertNotEqual(a,b.schedule(b.SEEDS[1],rows)[3])

    def test_10_bad_pairs_or_seed(self):
        rows=data_fixture()["TRAIN"];rows[1]["query"]=0
        with self.assertRaises(ValueError):b.schedule(b.SEEDS[0],rows)
        with self.assertRaises(ValueError):b.schedule(284002,data_fixture()["TRAIN"])

    def test_11_model_capacity_and_independent_storage(self):
        c=fixture_context()[4];models=b.make_models(b.SEEDS[0],c)
        self.assertEqual(fingerprint(models[b.ARMS[0]]),fingerprint(models[b.ARMS[1]]))
        with torch.no_grad():next(models[b.ARMS[1]].parameters()).add_(1.)
        self.assertNotEqual(fingerprint(models[b.ARMS[0]]),fingerprint(models[b.ARMS[1]]))

    def test_12_bad_capacity_or_dtype(self):
        c=fixture_context()[4];c.factory.new_model=lambda s:Weights(13489)
        with self.assertRaisesRegex(ValueError,"capacity"):b.make_models(b.SEEDS[0],c)
        c.factory.new_model=lambda s:Weights().float()
        with self.assertRaisesRegex(ValueError,"precision"):b.make_models(b.SEEDS[0],c)

    def test_13_real_optimizer_steps_receive_exact_lr(self):
        for arm in b.ARMS:
            self.assertEqual(self.lr_steps[arm],b.learning_rates(arm))
            self.assertEqual(self.fits[arm]["applied_lr"],self.lr_steps[arm])
            self.assertEqual(self.toys[arm].seen,[e%2 for e in range(200) for _ in range(4)])

    def test_14_real_fit_prefix_identity_and_final_difference(self):
        a,c=(self.fits[x] for x in b.ARMS)
        self.assertEqual(a["step400_sha256"],c["step400_sha256"]);self.assertEqual(a["loss_history"][:400],c["loss_history"][:400])
        self.assertNotEqual(fingerprint(self.toys[b.ARMS[0]]),fingerprint(self.toys[b.ARMS[1]]))
        self.assertEqual(len(a["loss_history"]),800);self.assertFalse(self.toys[b.ARMS[1]].training)

    def test_15_fit_bad_shape_before_optimizer(self):
        with patch.object(torch.optim,"AdamW") as opt,self.assertRaises(ValueError):
            b.fit(None,{},torch.zeros(1),torch.zeros(1),b.SEEDS[0],b.ARMS[0],None)
        opt.assert_not_called()

    def test_16_nonfinite_loss_fails(self):
        model=Toy()
        with torch.no_grad():model.bias.fill_(float("nan"))
        with self.assertRaisesRegex(ValueError,"nonfinite loss"):
            b.fit(model,data_fixture(),torch.zeros((2,3,192,48),dtype=torch.int64),torch.tensor([48,49]*96),b.SEEDS[0],b.ARMS[0],NS())

    def test_17_train_freeze_evaluate_order(self):
        _,previous,transfer,_,c=fixture_context();m=b.make_models(b.SEEDS[0],c)[b.ARMS[0]];events=[]
        @contextlib.contextmanager
        def counted(*a):yield [881,46176],[3524]
        c.p267.counted=counted
        def fit(model,*a):
            events.append("fit")
            with torch.no_grad():
                for p in model.parameters():p.add_(1.)
            model.eval();return {}
        def ev(model,*a):
            events.append("evaluate");self.assertFalse(any(p.requires_grad for p in model.parameters()));return {}
        previous.evaluate=ev
        with patch.object(b,"fit",side_effect=fit):b.train_one(m,{}, {}, {},None,None,b.SEEDS[0],b.ARMS[0],previous,transfer,c)
        self.assertEqual(events,["fit","evaluate"])

    def test_18_analyze_all_tasks_and_prefixes(self):
        ctx,d,rr=records_fixture();metrics,s=b.analyze(rr,d,ctx[2],ctx[4])
        self.assertEqual((len(metrics),len(s["contrasts"])),(10,180));self.assertTrue(s["all_prefixes_matched"])
        self.assertEqual(s["quad_pass_counts"],dict.fromkeys(b.ARMS,5))

    def test_19_control_failure_cannot_fail_candidate(self):
        p=result_fixture();p["validation_summary"]["seed_results"][0]["quad_pass"]=False;b.validate_result(recount(p))

    def test_20_one_candidate_miss_is_negative(self):
        p=result_fixture();p["validation_summary"]["seed_results"][1]["quad_pass"]=False;recount(p)
        with self.assertRaises(ValueError):b.validate_result(p)
        p["status"]="FAIL";p["validation_summary"]["candidate_gate"]=False;b.validate_result(p)

    def test_21_seen_task_failure_is_descriptive(self):
        p=result_fixture();p["validation_summary"]["seed_results"][1]["triple_pass"]=False;b.validate_result(recount(p))

    def test_22_false_prefix_attestation_rejected(self):
        p=result_fixture();p["validation_summary"]["all_prefixes_matched"]=False
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_23_applied_lr_tamper_even_with_new_hash_rejected(self):
        ctx,d,rr=records_fixture();rr[1]["fit"]["applied_lr"][500]=.005
        rr[1]["fit"]["lr_sha256"]=b.digest(rr[1]["fit"]["applied_lr"])
        with self.assertRaisesRegex(ValueError,"LR history"):b.analyze(rr,d,ctx[2],ctx[4])

    def test_24_midpoint_mismatch_rejected(self):
        ctx,d,rr=records_fixture();rr[1]["fit"]["step400_sha256"]="b"*64
        with self.assertRaisesRegex(ValueError,"common first400"):b.analyze(rr,d,ctx[2],ctx[4])

    def test_25_prefix_loss_mismatch_rejected(self):
        ctx,d,rr=records_fixture();rr[1]["fit"]["loss_history"][399]=.011
        with self.assertRaisesRegex(ValueError,"common first400"):b.analyze(rr,d,ctx[2],ctx[4])

    def test_26_nonfinite_loss_or_replay_and_missing_model(self):
        ctx,d,rr=records_fixture();rr[0]["fit"]["loss_history"][500]=float("nan")
        with self.assertRaises(ValueError):b.analyze(rr,d,ctx[2],ctx[4])
        rr[0]["fit"]["loss_history"][500]=.01;rr[0]["reload_max_error"]=1e-3
        with self.assertRaises(ValueError):b.analyze(rr,d,ctx[2],ctx[4])
        rr.pop()
        with self.assertRaises(ValueError):b.analyze(rr,d,ctx[2],ctx[4])

    def test_27_scope_counts_and_source_pin(self):
        for mutation in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(train_steps=8001),
                         lambda p:p["validation_summary"].update(new_checkpoint_writes=True),lambda p:p["source_blobs"].pop(b.PARENT_SOURCE)):
            p=result_fixture();mutation(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    def test_28_context_dispatch_chain(self):
        import types
        package=types.ModuleType("fold_lm.v05_benchmarks")
        parent=NS();previous=NS();transfer=NS();training=NS();c=NS()
        previous.context=lambda:(transfer,training,c);parent.context=lambda:(previous,c)
        package.model_c285_saved_length_transfer_audit=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):
            self.assertEqual(b.context(),(parent,previous,transfer,training,c))

    def test_29_all_twelve_hashes_and_parent_call(self):
        paths=[(Path("/c286-fixture")/str(i)/"summary.json").resolve() for i in range(12)]
        mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True));payload=parent_fixture()
        parent=NS(verify_artifacts=Mock(return_value=(payload,{})),validate_result=Mock());c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        with patch.object(b,"context",return_value=(parent,None,None,None,c)):
            b.load_parent(paths);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for p in paths:
                old=mapping[str(p)];mapping[str(p)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(p)]=old

    def test_30_parent_source_artifacts_and_metric_rejected(self):
        paths=[Path(str(i)).resolve() for i in range(12)];mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        payload=parent_fixture();parent=NS(verify_artifacts=Mock(return_value=(payload,{})),validate_result=Mock())
        c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        with patch.object(b,"context",return_value=(parent,None,None,None,c)):
            for mutation in (lambda p:p["source_blobs"].clear(),lambda p:p["artifacts"][0].update(serialized_bytes=0),
                             lambda p:p["validation_summary"]["primary"]["triple_to_quad"]["mixed_length"]["criteria"]["accuracy"].update(right_fail=42)):
                altered=copy.deepcopy(payload);mutation(altered);parent.verify_artifacts.return_value=(altered,{})
                with self.assertRaises(ValueError):b.load_parent(paths)

    def test_31_forbidden_parent_operations(self):
        paths=[Path(str(i)).resolve() for i in range(12)];mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        parent=NS(verify_artifacts=Mock());c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        for action in (lambda *a:torch.nn.Identity()(torch.ones(1)),lambda *a:torch.nn.Linear(1,1).load_state_dict({}),lambda *a:torch.save({},"FORBIDDEN.pt")):
            parent.verify_artifacts.side_effect=action
            with patch.object(b,"context",return_value=(parent,None,None,None,c)),self.assertRaisesRegex(RuntimeError,"C286 parent forbids"):
                b.load_parent(paths)
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_32_precheck_real_file_maps_and_pin_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);lm=[f"fold_lm/fixture_{i}.py" for i in range(6)]
            names=[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,286)]
            names[-1]=b.PARENT_SOURCE;names+=lm
            names += [f"accepted/{i}.txt" for i in range(556-len(names))]
            pins={n:(b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40) for n in names}
            for n in names+list(b.OWN):
                f=root/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(n)
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(991-len(inputs)):
                p=root/f"input{i}";p.write_text("input");inputs[str(p.resolve())]=Audit.sha(p)
            parent_dir=root/"parent";parent_dir.mkdir();summary=parent_dir/"summary.json";summary.write_text("summary")
            mapping={str(summary.resolve()):b.SUMMARY_SHAS[0]}
            for n,(sha,size) in b.PARENT_ARTIFACTS.items():
                p=parent_dir/n;p.write_text("parent");mapping[str(p.resolve())]=sha
            payload=dict(source_blobs=pins,input_sha256=inputs)
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*args):return (pins.get(args[1][5:],"c"*40)+"\n").encode()
            def protect(root,ps):return {str((root/n).resolve()):sha(root/n) for n in ps}
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=protect),factory=NS(LM_SOURCES=lm))
            with patch.object(b,"context",return_value=(None,None,None,None,c)),patch.object(b,"load_parent",return_value=payload),contextlib.redirect_stdout(io.StringIO()):
                got=b.precheck([summary]*12,root);self.assertEqual(tuple(map(len,got)),(562,1001))
                pins.pop(b.PARENT_SOURCE)
                with self.assertRaises(ValueError):b.precheck([summary]*12,root)

    def test_33_actual_suite_filter(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
            self.assertEqual(suite.countTestCases(),4085)

    def test_34_duplicate_suite_ids_rejected(self):
        class Dummy(unittest.TestCase):
            def runTest(self):pass
            def id(self):return "duplicate"
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy(),Dummy()])),self.assertRaises(ValueError):
            b.regression_suite(Path.cwd())

    def test_35_real_run_dispatch_and_persistence(self):
        ctx,d,rr=records_fixture();events=[]
        def train(m,data,triple,quad,x,y,seed,arm,*a):
            events.append("train");return copy.deepcopy(rr[b.identities().index((seed,arm))]),{"x":torch.ones(1)}
        def pc(*a):events.append("precheck");return protection()
        ctx[1].replay_one.side_effect=lambda *a:events.append("replay")
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=ctx),patch.object(b,"precheck",side_effect=pc),\
             patch.object(b,"load_parent",return_value=parent_fixture()),patch.object(b,"train_one",side_effect=train),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*12,output_dir=out,expected_head="f"*40)
            self.assertEqual(events,["precheck"]+["train"]*10+["replay"]*10+["precheck"])
            q,_=b.verify_artifacts(out,["x"]*12,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*12,output_dir=out,expected_head="f"*40)

    def test_36_artifact_tampering_and_bad_checkpoint(self):
        ctx,d,rr=records_fixture()
        def train(m,data,triple,quad,x,y,s,a,*rest):return copy.deepcopy(rr[b.identities().index((s,a))]),{"x":torch.ones(1)}
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=ctx),patch.object(b,"precheck",return_value=protection()),\
             patch.object(b,"load_parent",return_value=parent_fixture()),patch.object(b,"train_one",side_effect=train),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*12,output_dir=out,expected_head="f"*40)
            f=out/"measurements.json";f.write_text("[]")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*12,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==f.name);a.update(sha256=Audit.sha(f),serialized_bytes=f.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*12,"f"*40)
            bad=Path(tmp)/"bad.pt";torch.save(dict(schema="wrong"),bad)
            with self.assertRaises(ValueError):b.load_bundle(bad)

    def test_37_cli_twelve_paths(self):
        argv=["prog","--summaries"]+[str(i) for i in range(12)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:
            b.main();self.assertEqual(run.call_args.kwargs["summaries"],[Path(str(i)) for i in range(12)])

    def test_38_runner_blocks_and_phase_order(self):
        root=Path(__file__).resolve().parents[1];r=(root/"tools/run_c286.ps1").read_text(encoding="utf-8");l=(root/"tools/invoke_c286.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",r,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:14]",blocks[2]);self.assertIn("head = sys.argv[14]",blocks[2])
        self.assertLess(l.index("-Mode Validate"),l.index("-Mode Execute"));self.assertLess(l.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),l.index("publish_experiment_log.ps1"))
        self.assertIn("Parser]::ParseFile",l);self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',l)),12)

    def test_39_immutable_inventory_and_direct_import(self):
        root=Path(__file__).resolve().parents[1];self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])
        for n in b.OWN:self.assertTrue((root/n).is_file())
        imports=[n for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c285_saved_length_transfer_audit"])
        self.assertEqual(b.manifest()["source_pins"],556+len(b.OWN));self.assertEqual(b.manifest()["protected_inputs"],991+4+len(b.OWN))

    def test_40_repository_guards(self):
        c=NS(audit=Audit());b.guard(Path.cwd(),"f"*40,c)
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,c)
        def git(root,*a):return b"dirty" if a[0]=="status" else Audit.git(root,*a)
        c.audit=NS(git=git)
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"f"*40,c)


if __name__=="__main__":unittest.main()
