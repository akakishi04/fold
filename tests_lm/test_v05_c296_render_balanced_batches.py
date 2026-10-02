"""C296 behavioral fixtures; synthetic control tests are not FOLD capability results."""
import ast
from collections import Counter
import contextlib
import copy
import hashlib
import io
import itertools
import json
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
from fold_lm.v05_benchmarks import model_c296_render_balanced_batches as b


def dataset():
    d={"TRAIN":[],"HOLDOUT":[]}
    for e,v,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for order,q in itertools.product((e,e[::-1]),e):
            d[split].append(dict(id=str((lang,e,v,order,q)),language=lang,entities=list(e),values=list(v),permutation=list(order),query=q,target=48+v[e.index(q)]))
    return d


def tables(data):
    y=torch.tensor([r["target"] for r in data["TRAIN"]]);x=torch.zeros((2,3,192,48),dtype=torch.int64)
    for length,profile in itertools.product(range(2),range(3)):
        x[length,profile,:,0]=y-48;x[length,profile,:,1]=length;x[length,profile,:,2]=profile
    return x,y


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__();self.backbone=torch.nn.Embedding(4,4,dtype=torch.float64);self.read=torch.nn.Linear(4,256,dtype=torch.float64)
        self.calls=0;self.rows=0
    def forward(self,tokens,tasks):
        assert tokens.shape==(len(tokens),48) and tasks.shape==(len(tokens),) and not bool(tasks.any())
        self.calls+=1;self.rows+=len(tokens)
        return self.read(self.backbone(tokens[:,0]))


def fingerprint(m):return b.digest({k:v.detach().tolist() for k,v in m.state_dict().items()})


def fixtures():
    data=dataset();z={}
    for split,rows in data.items():
        z[split]=torch.zeros((len(rows),256),dtype=torch.float64)
        z[split][torch.arange(len(rows)),torch.tensor([r["target"] for r in rows])]=4.
    records=[]
    for seed in b.SEEDS:
        plans,shared=b.schedules(seed,data["TRAIN"])
        for arm in b.ARMS:
            raw={t:{s:{str(p):{v:z[s] for v in ("normal","evidence_blind","query_blind")} for p in range(3)} for s in data} for t in b.TASKS}
            fit=dict(steps=800,training_rows=38400,optimizer_creations=1,ce_history=[1.]*800,last_ce=1.,
                schedule_events=plans[arm].clone(),event_sha256=b.digest(plans[arm].tolist()),**shared)
            records.append(dict(seed=seed,arm=arm,parameters=14256,weights_changed=True,initial_sha256="a"*64,final_sha256="b"*64,fit=fit,raw=raw,
                forward_calls=881,row_presentations=46176,core_forward_calls=3524,checkpoint_roundtrip=True,reload_max_error=0.,
                replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    return records,data


def scorers():
    def score(data,raw):
        totals=[]
        for split,profiles in raw.items():
            for profile,views in profiles.items():
                pred=views["normal"].argmax(1).tolist()
                for lang in ("en","ja"):
                    ii=[i for i,r in enumerate(data[split]) if r["language"]==lang]
                    n=sum(pred[i]==data[split][i]["target"] for i in ii)
                    totals.append(dict(split=split,profile=profile,language=lang,rows=len(ii),pairs=len(ii)//2,correct=n,collapsed_pairs=0))
        return dict(passed=all(t["correct"]==t["rows"] for t in totals),totals=totals)
    def measure(z,rows):return [dict(correct=int(p)==r["target"]) for p,r in zip(z.argmax(1).tolist(),rows,strict=True)]
    def aggregate(rows):
        n=sum(r["correct"] for r in rows)
        return dict(rows=len(rows),correct=n,conditional_correct=n,output_role_counts=dict(target=n,other_fact=len(rows)-n,absent_known_value=0,non_value_byte=0))
    audit=NS(measure=measure,aggregate=aggregate,no_neural=contextlib.nullcontext)
    diag=NS(normalize_task=lambda s,*_:s["totals"],partition=lambda rr:dict(rows=sum(r["rows"] for r in rr),correct=sum(r["correct"] for r in rr),direct_pass=all(r["rows"]==r["correct"] for r in rr)))
    transfer=NS(score_quad=lambda data,raw,c:score(data,raw));c=NS(p267=NS(score=score),c270=NS(score=lambda data,raw,p:score(data,raw)))
    return audit,diag,transfer,c


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<622:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1131)}


class Audit:
    @staticmethod
    def sha(p):
        p=Path(p);return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(p):return json.loads(Path(p).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n):return Path(root)/n
    @staticmethod
    def git(root,*a):
        if a[0]=="rev-parse":return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if a[0]=="branch":return b"feat/sft-target-loss\n"
        return b""


def result_fixture(summary):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if summary["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,gate_f_candidate=False,production_adoption=False)


class C296Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.det=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
        cls.data=dataset();cls.x,cls.y=tables(cls.data);cls.plans,cls.shared=b.schedules(b.SEEDS[0],cls.data["TRAIN"])
        torch.manual_seed(296);cls.initial=Toy();cls.models=[];cls.fits=[]
        with contextlib.redirect_stdout(io.StringIO()):
            for arm in b.ARMS:
                model=copy.deepcopy(cls.initial);cls.fits.append(b.fit(model,cls.data,cls.x,cls.y,b.SEEDS[0],arm));cls.models.append(model)
        cls.records,_=fixtures();cls.metrics,cls.summary=b.analyze(cls.records,cls.data,*scorers())
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads);torch.use_deterministic_algorithms(cls.det)

    def test_01_seal(self):b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seal(self):
        for h in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",h),self.assertRaises(ValueError):b.validate_seal()

    def test_03_blocked_schedule_reference(self):
        pairs=b.pairs_from_rows(self.data["TRAIN"]);plan=self.plans["blocked"]
        for epoch in (0,1,5,198,199):
            order=torch.randperm(96,generator=torch.Generator().manual_seed(b.SEEDS[0]+296000+epoch))
            self.assertTrue(torch.equal(plan[epoch*4:epoch*4+4,:,2:].reshape(96,2),pairs[order]))
            self.assertTrue(bool((plan[epoch*4:epoch*4+4,:,0]==epoch%2).all()))
            self.assertTrue(bool((plan[epoch*4:epoch*4+4,:,1]==epoch%3).all()))

    def test_04_all_balanced_batches(self):
        expected=dict.fromkeys(itertools.product(range(2),range(3)),4)
        for batch in self.plans["balanced"][:792]:self.assertEqual(Counter(map(tuple,batch[:,:2].tolist())),expected)

    def test_05_exact_block_multisets_all_seeds(self):
        for seed in b.SEEDS:
            p,s=b.schedules(seed,self.data["TRAIN"])
            self.assertEqual(b.event_counter(p["blocked"]),b.event_counter(p["balanced"]))
            self.assertEqual(len(s["block_multiset_sha256"]),33)

    def test_06_identical_final_eight(self):
        self.assertTrue(torch.equal(self.plans["blocked"][792:],self.plans["balanced"][792:]))
        self.assertFalse(torch.equal(self.plans["blocked"][:792],self.plans["balanced"][:792]))

    def test_07_exposure_counts(self):
        self.assertEqual(self.shared["per_length_row_exposures"],[[100]*192]*2)
        for plan in self.plans.values():
            for row in range(192):
                self.assertEqual(int((plan[:,:,2:]==row).sum()),200)

    def test_08_intact_query_pairs(self):
        valid=set(map(tuple,b.pairs_from_rows(self.data["TRAIN"]).tolist()))
        for plan in self.plans.values():self.assertEqual(set(map(tuple,plan[:,:,2:].reshape(-1,2).tolist())),valid)

    def test_09_determinism_and_fresh_seed(self):
        p,_=b.schedules(b.SEEDS[0],self.data["TRAIN"]);q,_=b.schedules(b.SEEDS[1],self.data["TRAIN"])
        self.assertTrue(torch.equal(p["balanced"],self.plans["balanced"]));self.assertFalse(torch.equal(p["balanced"],q["balanced"]))

    def test_10_bad_pair_data(self):
        for fn in (lambda r:r.pop(),lambda r:r[1].update(query=r[0]["query"]),lambda r:r[0].update(target=88)):
            rows=copy.deepcopy(self.data["TRAIN"]);fn(rows)
            with self.assertRaises(ValueError):b.schedules(b.SEEDS[0],rows)
        with self.assertRaises(ValueError):b.schedules(295001,self.data["TRAIN"])

    def test_11_missing_event_is_rejected(self):
        wrong=self.plans["balanced"].clone();wrong[0,0]=wrong[0,1]
        with self.assertRaises(ValueError):b.verify_plan_pair(self.plans["blocked"],wrong)

    def test_12_tail_reordering_is_rejected(self):
        wrong=self.plans["balanced"].clone();wrong[792]=wrong[792].flip(0)
        with self.assertRaisesRegex(ValueError,"shared tail"):b.verify_plan_pair(self.plans["blocked"],wrong)

    def test_13_bad_schedule_shape_or_bounds(self):
        for wrong in (self.plans["balanced"].float(),self.plans["balanced"][:799]):
            with self.assertRaises(ValueError):b.verify_plan_pair(self.plans["blocked"],wrong)
        wrong=self.plans["balanced"].clone();wrong[0,0,2]=192
        with self.assertRaises(ValueError):b.verify_plan_pair(self.plans["blocked"],wrong)

    def test_14_render_batch_reference(self):
        for plan in self.plans.values():
            events=plan[0];x,y=b.render_batch(self.x,self.y,events)
            expected=torch.stack([self.x[l,p,r] for l,p,i,j in events.tolist() for r in (i,j)])
            yy=torch.tensor([self.data["TRAIN"][r]["target"] for _,_,i,j in events.tolist() for r in (i,j)])
            self.assertTrue(torch.equal(x,expected));self.assertTrue(torch.equal(y,yy))

    def test_15_same_rendered_examples(self):
        a=self.plans["blocked"][:24];c=self.plans["balanced"][:24]
        def rendered(plan):
            return Counter((tuple(x),y) for batch in plan for xx,yy in [b.render_batch(self.x,self.y,batch)] for x,y in zip(xx.tolist(),yy.tolist(),strict=True))
        self.assertEqual(rendered(a),rendered(c))

    def test_16_real_800_step_loops(self):
        for arm,f,m in zip(b.ARMS,self.fits,self.models,strict=True):
            b.check_fit(f,b.SEEDS[0],arm,self.data);self.assertEqual((m.calls,m.rows),(800,38400))
            self.assertFalse(m.training);self.assertLess(f["last_ce"],f["ce_history"][0]);self.assertNotEqual(fingerprint(m),fingerprint(self.initial))

    def test_17_fit_determinism_and_optimizer(self):
        real=torch.optim.AdamW;made=[]
        def factory(*a,**kw):opt=real(*a,**kw);made.append(opt);return opt
        m=copy.deepcopy(self.initial)
        with patch.object(torch.optim,"AdamW",side_effect=factory),contextlib.redirect_stdout(io.StringIO()):f=b.fit(m,self.data,self.x,self.y,b.SEEDS[0],"balanced")
        self.assertEqual(len(made),1);self.assertEqual({int(v["step"]) for v in made[0].state.values()},{800})
        self.assertEqual(f["ce_history"],self.fits[1]["ce_history"]);self.assertEqual(fingerprint(m),fingerprint(self.models[1]))

    def test_18_plain_ce_first_update(self):
        for arm,f in zip(b.ARMS,self.fits,strict=True):
            m=copy.deepcopy(self.initial);x,y=b.render_batch(self.x,self.y,self.plans[arm][0])
            z=m(x,torch.zeros(48,dtype=torch.int64));loss=F.cross_entropy(z,y)
            self.assertEqual(float(loss.detach()),f["ce_history"][0])

    def test_19_target_alignment(self):
        y=self.y.clone();y[0]=100
        with self.assertRaises(ValueError):b.fit(copy.deepcopy(self.initial),self.data,self.x,y,b.SEEDS[0],"balanced")

    def test_20_persisted_fit_tamper(self):
        for fn in (lambda f:f["schedule_events"].__setitem__((0,0,0),3),lambda f:f["ce_history"].__setitem__(1,float("nan")),lambda f:f.update(optimizer_creations=2)):
            f=copy.deepcopy(self.fits[1]);fn(f)
            with self.assertRaises(ValueError):b.check_fit(f,b.SEEDS[0],"balanced",self.data)

    def test_21_factory_identity_and_storage(self):
        class Fake(torch.nn.Module):
            def __init__(self,*_):super().__init__();self.weight=torch.nn.Parameter(torch.ones(14256,dtype=torch.float64))
        c=NS(c278=NS(MeanFinalDualReadout=Fake),factory=NS(new_model=lambda _:None),reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))
        models=b.make_models(b.SEEDS[0],c);self.assertNotEqual(models["blocked"].weight.data_ptr(),models["balanced"].weight.data_ptr())
        self.assertEqual(fingerprint(models["blocked"]),fingerprint(models["balanced"]))

    def test_22_train_one_freezes_and_counts(self):
        m=copy.deepcopy(self.initial)
        @contextlib.contextmanager
        def counted(model,core):
            calls=[0,0];cores=[0];yield calls,cores;calls[:]=[model.calls,model.rows];cores[0]=4*model.calls
        def evaluate(model,*args):
            self.assertFalse(model.training);self.assertFalse(any(p.requires_grad for p in model.parameters()))
            with torch.no_grad():
                for _ in range(81):model(torch.zeros((96,48),dtype=torch.int64),torch.zeros(96,dtype=torch.int64))
            return {t:{} for t in b.TASKS}
        c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted),core=None)
        with contextlib.redirect_stdout(io.StringIO()):r,state=b.train_one(m,self.data,{},{},self.x,self.y,b.SEEDS[0],"balanced",NS(evaluate=evaluate),None,c)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(881,46176));self.assertEqual(set(state),set(m.state_dict()))

    def test_23_analysis_inventory(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["contrasts"])),(10,60,180))
        self.assertEqual(self.summary["quad_pass_counts"],dict.fromkeys(b.ARMS,5))

    def test_24_one_candidate_miss(self):
        records=copy.deepcopy(self.records);views=records[1]["raw"]["quad"]["HOLDOUT"]["0"]
        views["normal"]=views["normal"].clone();views["normal"][0,88]=20.
        _,s=b.analyze(records,self.data,*scorers());self.assertFalse(s["candidate_gate"]);self.assertEqual(s["quad_pass_counts"]["balanced"],4)
        b.validate_result(result_fixture(s))

    def test_25_integrity_and_matching(self):
        for field,value in (("reload_max_error",.1),("forward_calls",800),("initial_sha256","e"*64)):
            records=copy.deepcopy(self.records);records[1][field]=value
            with self.assertRaises(ValueError):b.analyze(records,self.data,*scorers())

    def test_26_roles_reconcile(self):
        audit,diag,transfer,c=scorers();audit.aggregate=lambda rows:dict(rows=len(rows),correct=0)
        with self.assertRaisesRegex(ValueError,"roles match scores"):b.analyze(self.records,self.data,audit,diag,transfer,c)

    def test_27_result_contract(self):
        b.validate_result(result_fixture(self.summary))
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(train_steps=16000),lambda p:p["validation_summary"]["final_partitions"].pop()):
            p=result_fixture(copy.deepcopy(self.summary));fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c296-fixture")/str(i)/"summary.json").resolve() for i in range(22)]
        old=(NS(PARENT_SHA="7"*64),NS(SUMMARY_SHAS=("8"*64,)*15));p291=NS(PARENT_SHA="6"*64,context=lambda:old)
        p292=NS(PARENT_SHA="5"*64);p293=NS(PARENT_SHA="4"*64,context=lambda:(p292,p291))
        audit_parent=NS(PARENT_SHA="3"*64,no_neural=contextlib.nullcontext)
        parent=NS(PARENT_SHA="2"*64,context=lambda:(audit_parent,p293),validate_result=Mock(),verify_artifacts=Mock())
        payload=dict(experiment_id="C295-v5b-ce-training-budget",commit_sha=b.PARENT_EXECUTION,status="FAIL",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
            artifacts=[dict(file=n,sha256="a"*64) for n in b.OUTPUTS],validation_summary=dict(seed_results=b.expected_parent_results(),candidate_gate=False,common_trajectory=True,all_replays=True))
        parent.verify_artifacts.return_value=(payload,{})
        mapping=dict(zip(map(str,paths),[b.PARENT_SHA,"2"*64,"3"*64,"4"*64,"5"*64,"6"*64,"7"*64]+["8"*64]*15,strict=True))
        objects={n:{"fixture":n} for n in ("dataset.json","triple-dataset.json","quad-dataset.json")};manifest=b.manifest()
        for k,n in zip(("data_sha256","triple_sha256","quad_sha256"),objects,strict=True):manifest[k]=b.digest(objects[n])
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:objects[p.name]))
        with patch.object(b,"context",return_value=(parent,audit_parent,None,None,None,None,c)),patch.object(b,"manifest",return_value=manifest):yield paths,mapping,parent,payload

    def test_28_twenty_two_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,payload):
            self.assertEqual(b.load_parent(paths)[0],payload);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_29_parent_status_and_cohort(self):
        for fn in (lambda p:p.update(status="PASS"),lambda p:p["artifacts"].pop(),lambda p:p["validation_summary"]["seed_results"].pop()):
            with self.loader_fixture() as (paths,_,_,p):
                fn(p)
                with self.assertRaises(ValueError):b.load_parent(paths)

    def test_30_actual_protection_and_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);names=[b.PARENT_SOURCE]+[f"accepted/{i}" for i in range(615)];pins={n:b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40 for n in names}
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1116-len(inputs)):
                p=root/f"input{i}";p.write_text("input",encoding="utf-8");inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();s=directory/"summary.json";s.write_text("summary",encoding="utf-8");mapping={str(s.resolve()):b.PARENT_SHA};artifacts=[]
            for n in b.OUTPUTS:p=directory/n;p.write_text("parent",encoding="utf-8");mapping[str(p.resolve())]="a"*64;artifacts.append(dict(file=n,sha256="a"*64))
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*a):return (pins.get(a[1][5:],"c"*40)+"\n").encode()
            parent=types.ModuleType("parent");parent.__file__=str(root/b.PARENT_SOURCE);parent.context=lambda:()
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            with patch.object(b,"context",return_value=(parent,None,None,None,None,None,c)),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=inputs,artifacts=artifacts),None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([s]*22,root))),(622,1131))
                c.missing=types.ModuleType("missing");c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"):b.precheck([s]*22,root)

    def test_31_semantic_suite_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(4461)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            s=b.regression_suite(Path.cwd());self.assertEqual(s.countTestCases(),4461);self.assertEqual({t.id() for t in b.flatten(s)},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())

    def test_32_bundle_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"models.pt";v=dict(schema="fold-c296-render-models-v1",identities=[list(i) for i in b.identities()],states=[{} for _ in range(10)])
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),10);v["identities"].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)

    @contextlib.contextmanager
    def run_fixture(self):
        records=copy.deepcopy(self.records);audit,diag,transfer,c=scorers();c.audit=Audit();events=[]
        def train(*args):events.append("train");return copy.deepcopy(records[b.identities().index((args[6],args[7]))]),{}
        def replay(*args):events.append("replay")
        def load(*a):events.append("load_parent");return {},self.data,{"triple":1},{"quad":1}
        def precheck(*a):events.append("precheck");return protection()
        with patch.object(b,"context",return_value=(None,audit,diag,NS(replay_one=replay),transfer,NS(training_tables=lambda *_:(self.x,self.y)),c)),patch.object(b,"precheck",side_effect=precheck),patch.object(b,"load_parent",side_effect=load),patch.object(b,"make_models",return_value=dict.fromkeys(b.ARMS,None)),patch.object(b,"train_one",side_effect=train):yield events

    def test_33_actual_run_order_and_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*22,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[:2],["precheck","load_parent"]);self.assertEqual(events.count("train"),10);self.assertEqual(events.count("replay"),10)
            self.assertLess(max(i for i,x in enumerate(events) if x=="train"),events.index("replay"))
            q,_=b.verify_artifacts(out,["x"]*22,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*22,output_dir=out,expected_head="f"*40)

    def test_34_byte_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*22,output_dir=out,expected_head="f"*40);path=out/"measurements.json";path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*22,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size);(out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*22,"f"*40)

    def test_35_runtime_preflight(self):
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"context",return_value=(None,None,None,None,None,NS(training_tables=lambda *_:(self.x,self.y)),None)),patch.object(b,"load_parent",return_value=({},self.data,{},{})),patch.object(b,"make_models") as make,contextlib.redirect_stdout(io.StringIO()):
            b.runtime_preflight(["x"]*22,Path.cwd());make.assert_called_once()

    def test_36_cli(self):
        argv=["prog","--summaries"]+[str(i) for i in range(22)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),22)

    def test_37_cp932_actual_files(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))

    def test_38_explicit_utf8_and_direct_import(self):
        for path in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in n.keywords))
        tree=ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        imports=[n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c295_ce_budget"])

    def test_39_runner_blocks_and_paths(self):
        root=Path(__file__).resolve().parents[1];runner=(root/b.OWN[2]).read_text(encoding="utf-8");launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:24]",blocks[2]);self.assertIn("head = sys.argv[24]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),22)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"));self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_40_context_guard_and_test_count(self):
        c=NS(audit=Audit());parent=NS(context=lambda:(1,2,3,4,5,6,c),regression_modules=lambda root:["f"+str(i) for i in range(180)])
        package=types.ModuleType("fold_lm.v05_benchmarks");package.model_c295_ce_budget=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):self.assertEqual(b.context(),(parent,1,3,4,5,6,c));self.assertEqual(len(b.regression_modules(Path.cwd())),181)
        b.guard(Path.cwd(),"f"*40,c)
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,c)
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),40)


if __name__=="__main__":unittest.main()
