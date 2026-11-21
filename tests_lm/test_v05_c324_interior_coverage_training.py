"""C324 authoring tests; synthetic dependencies are explicit and never capability evidence."""
from contextlib import contextmanager, nullcontext
import copy
import io
import itertools
from pathlib import Path
import re
import tempfile
from types import ModuleType, SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c324_interior_coverage_training as b
from tests_lm.test_v05_c324_training_templates import fixture

ROOT = Path(__file__).resolve().parents[1]


def parent_result():
    return dict(experiment_id='C323-v5b-saved-fact-order-bias',commit_sha=b.PARENT_EXECUTION,status='PASS',
        diagnostic_execution_valid=True,capability_gate_applicable=False,
        source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB,**{f'parent-{i}':'0'*40 for i in range(783)}},
        input_sha256={f'input-{i}':'0'*64 for i in range(1478)},
        artifacts=[dict(file=n,sha256='0'*64) for n in ('audit-plan.json','order-counterfactuals.json','measurements.json','validation-summary.json')],
        validation_summary=dict(diagnostic_complete=True,overall=[dict(arm=a,condition=c,correct=n,same_value_all_four=k)
            for a,c,n,k in [('mean_last','old4',4320,0),('last_only','old4',4320,0),
                            ('mean_last','interior',2211,814),('last_only','interior',2292,809)]]))


def summaries(gate=True):
    rr=[dict(seed=s,arm=a,original_pass={str(n):True for n in range(2,7)},retention_pass=True,interior_pass=a=='interior4') for s,a in b.identities()]
    pp=[dict(seed=s,candidate_interior_pass=True,candidate_retention_pass=True,
             answer_gain=1 if gate else 0,query_pair_gain=1,paired_success=gate) for s in b.SEEDS]
    return dict(candidate_gate=gate,paired_success_count=5 if gate else 0,seed_results=rr,paired_comparisons=pp,
                all_pairs_matched=True,all_replays=True,**b.WORK)


def result(gate=True):
    p=parent_result()
    pins={**p['source_blobs'],**{n:'a'*40 for n in b.OWN}}
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha='d'*40,status='PASS' if gate else 'FAIL',
                diagnostic_execution_valid=True,gate_f_candidate=False,production_adoption=False,
                source_blobs=pins,input_sha256={f'input-{i}':'0'*64 for i in range(1491)},
                artifacts=[dict(file=n,sha256='0'*64,serialized_bytes=1) for n in b.OUTPUTS],validation_summary=summaries(gate))


def simple_logits(rows, correct=True):
    target=torch.tensor([r['target'] for r in rows])
    z=torch.full((len(rows),256),-2.,dtype=torch.float64)
    z[torch.arange(len(rows)),target if correct else torch.full_like(target,48)]=2.
    return {p:{'normal':z.clone()} for p in b.templates.INTERIOR_PROFILES}


def events():
    e=torch.empty((1200,24,4),dtype=torch.int64)
    for epoch in range(300):
        block=e[epoch*4:epoch*4+4]
        block[:,:,0]=2+epoch%3;block[:,:,1]=(epoch//3+epoch%3)%3
        block[:,:,2:]=torch.arange(192).reshape(4,24,2)
    return e


def event_stats(e):
    return dict(event_sha256=b.digest(e.tolist()),logical_pair_sha256=b.digest(e[:,:,2:].tolist()),
        per_length_row_exposures=[torch.bincount(e[e[:,:,0]==n][:,2:].flatten(),minlength=192).tolist() for n in range(1,5)],
        length_profile_updates=[[int(((e[:,0,0]==n)&(e[:,0,1]==p)).sum()) for p in range(3)] for n in range(1,5)])


def check_logits(z,n):
    b.require(z.shape==(n,256) and z.dtype==torch.float64 and z.device.type=='cpu' and bool(torch.isfinite(z).all()),'finite logits')


class TinyModel(torch.nn.Module):
    """A software-only neural fixture, NOT the FOLD model."""
    def __init__(self):
        super().__init__()
        self.core=torch.nn.Linear(2,2,bias=False,dtype=torch.float64)
        self.output=torch.nn.Linear(2,256,dtype=torch.float64)
    def forward(self,tokens,tasks):
        return self.output(self.core(tokens[:,:2].double()/100.))


def optimizer_context():
    def optimizer(model,policy):
        return torch.optim.AdamW([dict(params=list(model.output.parameters()),lr=.005),
                                 dict(params=list(model.core.parameters()),lr=.0005)],betas=(.9,.999),eps=1e-8,weight_decay=0)
    return NS(policy=NS(optimizer_for=optimizer,verify_optimizer=lambda *a:None),
              c=NS(p267=NS(check_logits=check_logits)),parent=NS(schedule_stats=event_stats))


@contextmanager
def run_fixture(folder):
    """Exercise the actual writer/loader dispatch with synthetic training/model dependencies."""
    p=result(False);data={'TRAIN':[dict(target=48)],'HOLDOUT':[dict(target=48)]}
    old={str(n):{'TRAIN':{}} for n in (2,3,4)};new={'TRAIN':{}}
    cx=(NS(),NS(),NS(),NS(),NS(),NS(wide=NS(),guarded=NS(no_neural=nullcontext)))
    calls=[]
    def train(*args):
        seed,arm=args[-3:-1];calls.append(('train',seed,arm))
        return dict(seed=seed,arm=arm),{'fixture':torch.tensor([1.],dtype=torch.float64)}
    def replay(*args):
        calls.append(('replay',args[2]['seed'],args[2]['arm']))
    with patch.object(b,'context',return_value=cx),patch.object(b,'guard'),\
         patch.object(b,'precheck',return_value=(p['source_blobs'],p['input_sha256'],(data,old,new))),\
         patch.object(b,'training_views',return_value={a:object() for a in b.ARMS}),\
         patch.object(b,'tensor_tables',return_value=({},torch.tensor([48]))),\
         patch.object(b,'make_models',side_effect=lambda *a:{k:object() for k in b.ARMS}),\
         patch.object(b,'schedule',return_value=object()),patch.object(b,'check_dependencies'),\
         patch.object(b,'train_one',side_effect=train),patch.object(b,'replay',side_effect=replay),\
         patch.object(b,'analyze',return_value=([],summaries(False))),patch.object(b,'verify_inputs'):
        yield calls,cx,data,old,new


class C324Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)

    def test_01_manifest_seal_and_counts(self):
        b.validate_seal();m=b.manifest()
        self.assertEqual(m['models'],len(b.identities()))
        self.assertEqual(m['raw_logit_payload_bytes'],16416*256*8*10)
        self.assertEqual(m['model_forward_calls'],12000+2*171*10)
        self.assertEqual(len(b.OWN),8)

    def test_02_manifest_tamper_rejected(self):
        with patch.object(b,'STEPS',1201),self.assertRaisesRegex(ValueError,'seal'):b.validate_seal()

    def test_03_parent_hash_chain_dispatch(self):
        p=NS(parent_ordered_hashes=Mock(return_value=tuple(str(i) for i in range(49))))
        cx=(p,1,2,3,4,5)
        self.assertEqual(len(b.parent_hashes(cx)),50);p.parent_ordered_hashes.assert_called_once_with(1,2,3,4)

    def test_04_all_parent_hashes_precede_loader(self):
        with tempfile.TemporaryDirectory() as d:
            paths=[]
            for i in range(50):
                p=Path(d)/str(i);p.write_text(str(i));paths.append(p)
            hashes=tuple(map(b.sha,paths));loader=Mock()
            cx=(NS(verify_artifacts=loader),None,None,None,None,NS())
            for i in range(50):
                h=list(hashes);h[i]='f'*64
                with patch.object(b,'context',return_value=cx),patch.object(b,'parent_hashes',return_value=h),self.assertRaisesRegex(ValueError,'parent hashes'):
                    b.load_parent(paths)
            loader.assert_not_called()

    def test_05_parent_identity_and_source(self):
        p=parent_result();b.validate_parent(p)
        for k,v in [('commit_sha','bad'),('status','FAIL'),('capability_gate_applicable',True)]:
            q=copy.deepcopy(p);q[k]=v
            with self.assertRaises(ValueError):b.validate_parent(q)
        p['source_blobs'][b.PARENT_SOURCE]='bad'
        with self.assertRaises(ValueError):b.validate_parent(p)

    def test_06_parent_artifact_inventory(self):
        p=parent_result();p['artifacts'][0]['file']='trained-models.pt'
        with self.assertRaisesRegex(ValueError,'artifacts'):b.validate_parent(p)

    def test_07_parent_outcome_semantics(self):
        p=parent_result();p['validation_summary']['overall'][2]['same_value_all_four']+=1
        with self.assertRaisesRegex(ValueError,'outcomes'):b.validate_parent(p)

    def test_08_precheck_actual_files_and_protection_counts(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);folder=root/'parent';folder.mkdir();p=parent_result()
            for a in p['artifacts']:
                q=folder/a['file'];q.write_text(a['file']);a['sha256']=b.sha(q)
            summary=folder/'summary.json';summary.write_bytes(b.blob(p))
            inputs={}
            for i in range(1478):
                f=root/f'input-{i}';f.write_text(str(i));inputs[str(f)]=b.sha(f)
            p['input_sha256']=inputs
            fresh={}
            for name in b.OWN:
                f=root/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(name);fresh[str(f)]=b.sha(f)
            cx=(None,None,None,None,None,NS(c=NS(audit=NS(protect_tree_files=lambda *a:fresh)),policy=NS(CORE_LR=.0005,BASE_LR=.005)))
            with patch.object(b,'context',return_value=cx),patch.object(b,'load_parent',return_value=(p,{}, {}, {})),\
                 patch.object(b,'git',side_effect=lambda root,op,path:p['source_blobs'].get(path[5:],'a'*40)),\
                 patch.object(b,'check_dependencies'),patch.object(b,'PARENT_SHA',b.sha(summary)),patch.object(b,'validate_seal'):
                pins,protected,_=b.precheck([summary],root)
                self.assertEqual((len(pins),len(protected)),(792,1491))
                next(iter(root.glob('input-*'))).write_text('changed')
                with self.assertRaisesRegex(ValueError,'protected input'):b.precheck([summary],root)

    def test_09_missing_direct_dependency_rejected(self):
        mod=ModuleType('unprotected');mod.__file__=str(ROOT/'unprotected.py')
        x=NS(parent=mod,wide=None,policy=None,p312=None,pairs=None,diag=None,c=NS(factory=NS(language_module=lambda:None)))
        with self.assertRaisesRegex(ValueError,'unprotected direct'):b.check_dependencies(ROOT,{},(None,None,None,None,None,x))

        # Windows-style in-repository virtualenv, distinct from a directory that
        # merely happens to be named .venv/site-packages. No filesystem is read.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();site=root/'.venv-py31315'/'Lib'/'site-packages'
            alternate=root/'.venv-py31315'/'plat-packages'
            cases=[
                ('runtime-torch',site/'torch/nn/modules/sparse.py','torch.nn.modules.sparse',True),
                ('runtime-numpy',site/'numpy/__init__.py','numpy',True),
                ('runtime-platlib',alternate/'torch/nn/modules/linear.py','torch.nn.modules.linear',True),
                ('unrelated-venv',root/'.venv-other/Lib/site-packages/torch/nn/modules/sparse.py','torch.nn.modules.sparse',False),
                ('fake-site-name',root/'fold_lm/site-packages/torch/layer.py','torch.layer',False),
                ('local-torch-shadow',root/'torch/nn/modules/sparse.py','torch.nn.modules.sparse',False),
                ('first-party-in-site',site/'fold_lm/layer.py','fold_lm.layer',False),
                ('namespace-mismatch',site/'torch/layer.py','fold_lm.layer',False),
                ('unknown-runtime-package',site/'other/layer.py','other.layer',False),
                ('prefix-not-directory',Path(str(site)+'-other')/'torch/layer.py','torch.layer',False),
                ('namespace-prefix',site/'torch/layer.py','torchish.layer',False),
                ('path-escape',site/'torch/../fold_lm/layer.py','torch.layer',False),
            ]
            configured=lambda name: str(site if name=='purelib' else alternate)
            with patch.object(b.sysconfig,'get_path',side_effect=configured):
                for label,path,namespace,external in cases:
                    with self.subTest(dependency_case=label):
                        if external:
                            b.check_dependency_file(root,{},path,namespace,'direct dependency')
                        else:
                            with self.assertRaisesRegex(ValueError,'unprotected direct'):
                                b.check_dependency_file(root,{},path,namespace,'direct dependency')
                local=root/'fold_lm/layer.py'
                b.check_dependency_file(root,{'fold_lm/layer.py':'a'*40},local,'fold_lm.layer','model class')
                # Both direct-module and model-class callers use the same rule.
                runtime=ModuleType('torch.nn.modules.sparse');runtime.__file__=str(site/'torch/nn/modules/sparse.py')
                x=NS(parent=runtime,wide=None,policy=None,p312=None,pairs=None,diag=None,c=NS(factory=NS(language_module=lambda:None)))
                b.check_dependencies(root,{},(None,None,None,None,None,x))
                runtime.__name__='fold_lm.unprotected'
                with self.assertRaisesRegex(ValueError,'unprotected direct'):
                    b.check_dependencies(root,{},(None,None,None,None,None,x))
                with patch.object(b.sysconfig,'get_path',return_value=None),self.assertRaisesRegex(ValueError,'unprotected model'):
                    b.check_dependency_file(root,{},site/'torch/nn/modules/sparse.py','torch.nn.modules.sparse','model class')

    def test_10_template_intervention_and_teacher_identity(self):
        rows,old,new=fixture();views=b.training_views(rows,old,new)
        self.assertEqual(views['original'].targets,views['interior4'].targets)
        self.assertEqual({k for k in views['original'].tables if views['original'].tables[k]!=views['interior4'].tables[k]}, {(4,p) for p in b.PROFILES})

    def test_11_tensor_builder_uses_only_returned_normals(self):
        view=b.templates.TrainingViews({k:tuple(['text']*192) for k in itertools.product((2,3,4),b.PROFILES)},tuple(range(192)),tuple([48]*192))
        token=Mock(return_value=torch.zeros(64,dtype=torch.int64))
        tables,y=b.tensor_tables(view,NS(prefix_tensor=token));self.assertEqual(token.call_count,9*192)
        self.assertEqual(y.tolist(),[48]*192);self.assertEqual(len(tables),9)

    def test_12_tensor_builder_rejects_bad_frame(self):
        view=b.templates.TrainingViews({k:tuple(['x']*192) for k in itertools.product((2,3,4),b.PROFILES)},tuple(range(192)),tuple([48]*192))
        with self.assertRaisesRegex(ValueError,'TRAIN tensors'):b.tensor_tables(view,NS(prefix_tensor=lambda _:torch.zeros(48,dtype=torch.int64)))

    def test_13_fresh_schedule_uses_fixed_order_and_exposures(self):
        e=events();planner=Mock(return_value=e);x=NS(parent=NS(plan_for_order=planner,schedule_stats=event_stats),p312=object(),pairs=object())
        for seed,order in zip(b.SEEDS,b.ORDERS):
            self.assertTrue(torch.equal(b.schedule(seed,[0]*192,x),e));self.assertEqual(planner.call_args.args[0],order)
        with self.assertRaises(ValueError):b.schedule(319001,[0]*192,x)

    def test_14_changed_row_exposure_rejected(self):
        x=NS(parent=NS(plan_for_order=lambda *a:events(),schedule_stats=lambda _:dict(per_length_row_exposures=[[1]*192]*4)),p312=None,pairs=None)
        with self.assertRaisesRegex(ValueError,'row exposures'):b.schedule(b.SEEDS[0],[0]*192,x)

    def test_15_model_constructor_is_native_and_paired(self):
        # Source-level contract complements the mandatory real-model runtime preflight.
        import inspect
        source=inspect.getsource(b.make_models)
        for term in ('MeanFinalDualReadout','LengthReadout','copy.deepcopy(template)','core_slow','independent'):
            if term=='independent':continue
            self.assertIn(term,source)
        self.assertNotIn('load_state_dict',source)
        with self.assertRaisesRegex(ValueError,'fresh model seed'):b.make_models(319001,NS())

        # Exercise real torch classes with unmocked inspect.getfile/sysconfig.
        # Treat an ancestor of the installed package as the repository root:
        # the same containment relation as M:/asobiba/fold/.venv-py31315.
        import sysconfig
        site=Path(sysconfig.get_path('purelib')).resolve()
        x=NS(parent=None,wide=None,policy=None,p312=None,pairs=None,diag=None,c=NS(factory=NS(language_module=lambda:None)))
        with torch.random.fork_rng(devices=[]):
            model=torch.nn.Sequential(torch.nn.Embedding(4,2),torch.nn.Linear(2,2))
        state={k:v.clone() for k,v in model.state_dict().items()}
        rng=torch.random.get_rng_state().clone()
        b.check_dependencies(site.parent,{},(None,None,None,None,None,x),model)
        self.assertTrue(torch.equal(rng,torch.random.get_rng_state()))
        self.assertTrue(all(torch.equal(state[k],v) for k,v in model.state_dict().items()))
        # Production caller under an emulated Windows install path; a FOLD
        # class in the same graph still needs an explicit pin.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();runtime=root/'.venv-py31315/Lib/site-packages'
            local=type('LocalLayer',(torch.nn.Module,),{'__module__':'fold_lm.local_layer'})
            model=torch.nn.Sequential(torch.nn.Embedding(4,2),local())
            def origin(cls):
                return str(root/'fold_lm/local_layer.py' if cls is local else runtime/'torch/nn/modules/sparse.py')
            with patch.object(b.sysconfig,'get_path',return_value=str(runtime)),patch.object(b.inspect,'getfile',side_effect=origin):
                with self.assertRaisesRegex(ValueError,'unprotected model class:'):
                    b.check_dependencies(root,{},(None,None,None,None,None,x),model)
                b.check_dependencies(root,{'fold_lm/local_layer.py':'a'*40},(None,None,None,None,None,x),model)

    def test_16_checkpoint_state_digest_covers_tensor_bytes(self):
        a={'x':torch.tensor([1.,2.],dtype=torch.float64)};c=copy.deepcopy(a);c['x'][0]+=1
        self.assertNotEqual(b.state_digest(a),b.state_digest(c))
        c['x'][0]=float('nan')
        with self.assertRaisesRegex(ValueError,'checkpoint tensor'):b.state_digest(c)

    def test_17_real_torch_fit_matches_explicit_reference(self):
        torch.manual_seed(900);a=TinyModel();ref=copy.deepcopy(a);x=optimizer_context()
        table=torch.arange(192*64).reshape(192,64)%30
        tables={k:table for k in itertools.product((2,3,4),b.PROFILES)};y=torch.arange(192)%4+48;e=events()[:2]
        with patch.object(b,'STEPS',2):got=b.fit(a,tables,y,e,x,'software-fixture')
        torch.manual_seed(b.FIT_RNG);opt=x.policy.optimizer_for(ref,'core_slow')
        for event in e:
            opt.zero_grad(set_to_none=True);ids=event[:,2:].flatten()
            loss=torch.nn.functional.cross_entropy(ref(table[ids],torch.zeros(48,dtype=torch.int64)),y[ids]);loss.backward()
            torch.nn.utils.clip_grad_norm_(list(ref.parameters()),1.,error_if_nonfinite=True);opt.step()
        self.assertTrue(all(torch.equal(a.state_dict()[k],v) for k,v in ref.state_dict().items()))
        self.assertEqual(len(got['ce_history']),2)

    def test_18_fit_nonfinite_stops_before_optimizer_step(self):
        a=TinyModel();a.output.weight.data.fill_(float('nan'));x=optimizer_context()
        t={k:torch.zeros(192,64,dtype=torch.int64) for k in itertools.product((2,3,4),b.PROFILES)}
        with patch.object(b,'STEPS',2),self.assertRaisesRegex(ValueError,'finite logits'):b.fit(a,t,torch.zeros(192,dtype=torch.int64),events()[:2],x,'bad')

    def test_19_fit_metadata_and_schedule_validation(self):
        e=events();f=dict(steps=1200,training_rows=57600,fit_rng=b.FIT_RNG,optimizer_creations=1,trainable_parameters=14256,
            schedule_events=e,ce_history=[1.]*1200,optimizer_group_lrs=[[.005,.0005]]*1200,
            gradient_union={'x':1},gradient_parameter_counts=[1]*1200,**event_stats(e))
        x=NS(parent=NS(schedule_stats=event_stats))
        with patch.object(b,'schedule',return_value=e):
            b.check_fit(f,b.SEEDS[0],[0]*192,x);f['fit_rng']+=1
            with self.assertRaisesRegex(ValueError,'fit metadata'):b.check_fit(f,b.SEEDS[0],[0]*192,x)

    def test_20_fit_schedule_tamper_rejected(self):
        e=events();f=dict(steps=1200,training_rows=57600,fit_rng=b.FIT_RNG,optimizer_creations=1,trainable_parameters=14256,schedule_events=e+1)
        with patch.object(b,'schedule',return_value=e),self.assertRaisesRegex(ValueError,'saved schedule'):b.check_fit(f,b.SEEDS[0],[0]*192,NS())

    def test_21_query_pairs_follow_identity_not_adjacency(self):
        rows=fixture()[0];rows=rows[::2]+rows[1::2]
        pairs=b.query_pairs(rows);self.assertEqual(len(pairs),4)
        self.assertTrue(all(rows[a]['query']==0 and rows[z]['query']==1 for a,z in pairs))
        with self.assertRaises(ValueError):b.query_pairs(rows[:-1])
        with self.assertRaises(ValueError):b.query_pairs([])

    def test_22_heldout_gain_and_rescue_accounting(self):
        rows=fixture()[0];r=b.heldout_contrast(simple_logits(rows,False),simple_logits(rows,True),rows)
        self.assertEqual((r['answer_gain'],r['query_pair_gain'],r['rescued'],r['regressed']),(12,12,12,0))

    def test_23_new_errors_are_not_hidden(self):
        rows=fixture()[0];r=b.heldout_contrast(simple_logits(rows,True),simple_logits(rows,False),rows)
        self.assertEqual(r['answer_gain'],-12);self.assertEqual(r['regressed'],12)

    def test_24_contrast_keeps_full256_argmax(self):
        rows=fixture()[0];a=simple_logits(rows,True);z=copy.deepcopy(a)
        for views in z.values():views['normal'][:,255]=9.
        r=b.heldout_contrast(a,z,rows);self.assertEqual(r['candidate_correct'],0)
        z[b.templates.INTERIOR_PROFILES[0]]['normal'][0,0]=float('nan')
        with self.assertRaisesRegex(ValueError,'contrast logits'):b.heldout_contrast(a,z,rows)

    def test_25_fixed_gate_all_five_and_retention(self):
        pp=summaries()['paired_comparisons'];self.assertTrue(b.fixed_gate(pp)[0])
        for key in ('candidate_interior_pass','candidate_retention_pass'):
            p=copy.deepcopy(pp);p[2][key]=False;self.assertFalse(b.fixed_gate(p)[0])
        with self.assertRaises(ValueError):b.fixed_gate(pp[:-1])

    def test_26_zero_or_negative_gain_not_success(self):
        for key in ('answer_gain','query_pair_gain'):
            for value in (0,-1):
                p=summaries()['paired_comparisons'];p[0][key]=value;self.assertFalse(b.fixed_gate(p)[0])

    def test_27_gate_nonfinite_bool_and_wrong_order_rejected(self):
        for value in (True,float('nan'),1.):
            pp=summaries()['paired_comparisons'];pp[0]['answer_gain']=value
            with self.assertRaises(ValueError):b.fixed_gate(pp)
        with self.assertRaises(ValueError):b.fixed_gate(list(reversed(summaries()['paired_comparisons'])))

    def test_28_raw_domain_inventory_rejected_before_parent(self):
        with self.assertRaisesRegex(ValueError,'domain'):b.validate_raw({}, {}, ())

    def test_29_replay_tolerance_and_argmax(self):
        a=dict(original={},interior={s:{p:{v:torch.zeros(2,256,dtype=torch.float64) for v in b.VIEWS} for p in b.templates.INTERIOR_PROFILES} for s in b.SPLITS})
        cx=(None,None,None,None,None,NS(parent=NS(replay_error=lambda *a:0.),c=None))
        with patch.object(b,'validate_raw'):
            self.assertEqual(b.replay_error(a,copy.deepcopy(a),{},cx),0.)
            z=copy.deepcopy(a);z['interior']['TRAIN']['balanced']['normal'][0,0]=1e-8
            with self.assertRaisesRegex(ValueError,'strict replay'):b.replay_error(a,z,{},cx)

    def test_30_argmax_flip_below_tolerance_is_rejected(self):
        a=dict(original={},interior={s:{p:{v:torch.zeros(2,256,dtype=torch.float64) for v in b.VIEWS} for p in b.templates.INTERIOR_PROFILES} for s in b.SPLITS})
        z=copy.deepcopy(a);z['interior']['TRAIN']['balanced']['normal'][0,1]=1e-10
        cx=(None,None,None,None,None,NS(parent=NS(replay_error=lambda *a:0.),c=None))
        with patch.object(b,'validate_raw'),self.assertRaisesRegex(ValueError,'strict replay'):b.replay_error(a,z,{},cx)

    def test_31_training_path_uses_native_policy_and_counts(self):
        import inspect
        source=inspect.getsource(b.train_one)
        self.assertIn("trained_readout(model, x.wide, 'mean_last')",source)
        self.assertLess(source.index('trained = fit('),source.index('raw = evaluate('))
        self.assertIn('calls == [1371, 74016]',source)
        self.assertNotIn("trained_readout(model, x.wide, arm)",source)

    def test_32_evaluator_dispatches_both_domains(self):
        old=Mock(return_value='old');new=Mock(return_value='new')
        x=NS(parent=NS(evaluate=old),wide='wide',c='c');cx=(None,None,NS(evaluate_new=new),None,None,x)
        r=b.evaluate('m','d','o','n',cx)
        self.assertEqual(r,dict(original='old',interior='new'));old.assert_called_once_with('m','o','d','wide','c');new.assert_called_once_with('m','n','d',x)

    def test_33_replay_tensor_schema_rejects_before_load(self):
        m=TinyModel();state={k:v.clone().float() for k,v in m.state_dict().items()}
        with self.assertRaisesRegex(ValueError,'tensor schema'):b.replay(m,state,{},None,None,None,(None,None))

    def test_34_checkpoint_bundle_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'m.pt';states=[{'x':torch.zeros(1,dtype=torch.float64)} for _ in b.identities()]
            torch.save(dict(schema='fold-c324-interior-coverage-models-v1',identities=[list(v) for v in b.identities()],readout_policy='mean_last',states=states),path)
            self.assertEqual(len(b.load_bundle(path)),10)

    def test_35_checkpoint_wrong_policy_and_identity(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'m.pt'
            for policy in ('last_only',None):
                torch.save(dict(schema='fold-c324-interior-coverage-models-v1',identities=[list(v) for v in b.identities()],readout_policy=policy,states=[{}]*10),path)
                with self.assertRaisesRegex(ValueError,'checkpoint schema'):b.load_bundle(path)

    def test_36_valid_scientific_negative_is_retained(self):
        b.validate_result(result(False));b.validate_result(result(True))

    def test_37_result_work_and_gate_tamper_rejected(self):
        p=result();p['validation_summary']['model_forward_calls']+=1
        with self.assertRaises(ValueError):b.validate_result(p)
        p=result(False);p['status']='PASS'
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_38_actual_run_writer_and_child_loader_dispatch(self):
        with tempfile.TemporaryDirectory() as d,run_fixture(d) as (calls,*_):
            out=Path(d)/'output'
            with patch.object(b,'load_bundle',wraps=b.load_bundle) as loader,redirect_stdout():
                r=b.run(summaries=['synthetic'],output_dir=out,expected_head='d'*40)
            self.assertEqual(loader.call_count,1);self.assertEqual([x[0] for x in calls],['train']*10+['replay']*10)
            self.assertEqual([(x[1],x[2]) for x in calls[:10]],b.identities())
            self.assertEqual({p.name for p in out.iterdir()},set(b.OUTPUTS)|{'summary.json'})
            self.assertEqual(r['status'],'FAIL');self.assertTrue(r['diagnostic_execution_valid'])

    def test_39_output_directory_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d,run_fixture(d),self.assertRaises(FileExistsError):
            b.run(summaries=['synthetic'],output_dir=d,expected_head='d'*40)

    def test_40_actual_saved_reconstruction_and_checkpoint_digest(self):
        with tempfile.TemporaryDirectory() as d,run_fixture(d) as (_,cx,data,old,new),redirect_stdout():
            out=Path(d)/'out';b.run(summaries=['synthetic'],output_dir=out,expected_head='d'*40)
            with patch.object(b,'load_parent',return_value=(None,data,old,new)):
                r,_=b.verify_artifacts(out,['synthetic'],'d'*40);self.assertEqual(r['status'],'FAIL')
                p=b.read_json(out/'summary.json');state=torch.load(out/'trained-models.pt',weights_only=True);state['states'][0]['fixture']+=1;torch.save(state,out/'trained-models.pt')
                for a in p['artifacts']:
                    if a['file']=='trained-models.pt':a.update(sha256=b.sha(out/a['file']),serialized_bytes=(out/a['file']).stat().st_size)
                (out/'summary.json').write_bytes(b.blob(p))
                with self.assertRaisesRegex(ValueError,'checkpoint tensors'):b.verify_artifacts(out,['synthetic'],'d'*40)

    def test_41_artifact_bytes_and_json_safety(self):
        with tempfile.TemporaryDirectory() as d,run_fixture(d),redirect_stdout():
            out=Path(d)/'out';b.run(summaries=['synthetic'],output_dir=out,expected_head='d'*40)
            (out/'measurements.json').write_text('changed')
            with self.assertRaisesRegex(ValueError,'artifact bytes'):b.verify_artifacts(out,['synthetic'],'d'*40)
            for text in ('{"x":1,"x":2}','{"x":NaN}'):
                p=Path(d)/'bad.json';p.write_text(text)
                with self.assertRaises(ValueError):b.read_json(p)
            with self.assertRaises(ValueError):b.child(out,'../summary.json')

    def test_42_cli_argument_contract(self):
        paths=[f'p{i}' for i in range(50)]
        with patch.object(b,'run') as run,patch('sys.argv',['module','--summaries',*paths,'--output-dir','out','--expected-head','d'*40]):b.main()
        self.assertEqual(run.call_args.kwargs['summaries'],list(map(Path,paths)))
        self.assertEqual(run.call_args.kwargs['expected_head'],'d'*40)

    def test_43_runner_launcher_and_embedded_python(self):
        launcher=(ROOT/'tools/invoke_c324.ps1').read_text(encoding='utf-8');runner=(ROOT/'tools/run_c324.ps1').read_text(encoding='utf-8')
        self.assertIn('ParseFile',launcher);self.assertIn("-ne '324'",launcher)
        self.assertLess(launcher.index('STALE_EXPECTED_HEAD'),launcher.index('$preflightLog ='))
        self.assertEqual(len(re.findall(r'Join-Path \$Root "runs\\c\d+-.*?\\summary.json"',launcher)),50)
        self.assertIn('c323-v5b-fact-order-f1b710e74fbe495aba6410d0d9530248',launcher)
        for code in re.findall(r"@'\n(.*?)\n'@",runner,re.S):compile(code,'runner-python','exec')
        self.assertIn('b.verify_artifacts',runner);self.assertIn('regression_suite',runner);self.assertNotIn('runpy.run_module',runner)
        self.assertLess(runner.index('=== C324 preflight:'),runner.index('& $Python -m py_compile'))

    def test_44_semantic_regression_extension_and_exact_exclusion(self):
        class Case(unittest.TestCase):
            def __init__(self,name):super().__init__('runTest');self.name=name
            def runTest(self):pass
            def id(self):return self.name
        names=[f'parent_module_{i}' for i in range(208)]
        cx=(NS(regression_modules=lambda root:names),)
        cases=[Case(b.EXCLUDED)]+[Case(f'synthetic-parent-and-child-id-{i}') for i in range(b.manifest()['loaded_tests']-1)]
        with patch.object(b,'context',return_value=cx):
            self.assertEqual(b.regression_modules(ROOT),names+list(b.OWN_MODULES))
            with patch.object(unittest.defaultTestLoader,'loadTestsFromNames',return_value=unittest.TestSuite(cases)):
                suite=b.regression_suite(ROOT)
                self.assertEqual(suite.countTestCases(),b.manifest()['focused_tests'])
                self.assertEqual([t.id() for t in b.flatten(suite)],[t.id() for t in cases[1:]])
        own=unittest.defaultTestLoader.loadTestsFromNames(list(b.OWN_MODULES))
        self.assertEqual(own.countTestCases(),b.manifest()['own_tests'])


@contextmanager
def redirect_stdout():
    from contextlib import redirect_stdout as redirect
    with redirect(io.StringIO()):yield


if __name__=='__main__':unittest.main()
