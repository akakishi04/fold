"""C260 authoring tests: explicit synthetic fixtures, not learned-capability evidence."""
import ast
from collections import defaultdict
import contextlib
import copy
import hashlib
import io
import itertools
import json
from pathlib import Path
import re
import tempfile
import textwrap
from types import SimpleNamespace
import unittest
from unittest.mock import Mock,patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c260_core_free_training as b


class Backbone(nn.Module):
    def __init__(self):
        super().__init__()
        self.byte_embedding=nn.Embedding(259,16,padding_idx=256)
        self.local_encoder=nn.GRU(16,16,batch_first=True)
        self.readout_norm=nn.LayerNorm(16);self.decoder=nn.Linear(16,256)
        self.core=FixtureCore()
    def _validate(self,tokens,tasks):
        b.require(tokens.dtype==tasks.dtype==torch.int64 and tokens.shape[1:]==(48,) and tasks.shape==(len(tokens),),'token contract')
    def encode_local(self,tokens):
        value,_=self.local_encoder(self.byte_embedding(tokens))
        return value*(tokens!=256).unsqueeze(-1)


class FixtureCore(nn.Module):
    """3328 synthetic parameters for branch accounting, not the FOLD core computation."""
    def __init__(self):
        super().__init__();self.weight=nn.Parameter(torch.zeros(3328))
    def forward(self,value):
        return value+torch.tanh(self.weight[:16])


class Template(nn.Module):
    def __init__(self,seed):
        super().__init__();torch.manual_seed(seed)
        self.backbone=Backbone();self.read=nn.Module()
        for name in ('query','key','output'):setattr(self.read,name,nn.Linear(16,16,bias=False))
        self.double().eval()
    def forward(self,tokens,tasks):
        self.backbone._validate(tokens,tasks)
        local=self.backbone.encode_local(tokens);valid=tokens!=256;eos=valid.sum(1)-1
        pre=local[torch.arange(len(tokens)),eos];post=pre
        for _ in range(4):post=self.backbone.core(post)
        q=self.read.query(pre);scores=(self.read.key(local)*q.unsqueeze(1)).sum(-1)/4
        weights=scores.masked_fill(~valid,float('-inf')).softmax(-1)
        read=self.read.output((weights.unsqueeze(-1)*local).sum(1))
        return self.backbone.decoder(self.backbone.readout_norm(post+read))


class Factory:
    @staticmethod
    def prefix_tensor(raw):
        b.require(len(raw)<=46,'prefix');return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))],dtype=torch.int64)
    @staticmethod
    def new_model(seed):return Template(seed)


class Base:
    @staticmethod
    def fingerprint(model):return hashlib.sha256(b''.join(k.encode()+v.detach().cpu().numpy().tobytes() for k,v in sorted(model.state_dict().items()))).hexdigest()
    @staticmethod
    def make_model(model,arm,seed,aligned,reader):return model
    @staticmethod
    def dataset():
        train={(0,1,2),(0,1,3),(0,2,1),(1,0,2),(1,0,3),(1,3,0),(2,0,3),(2,3,0),(2,3,1),(3,1,2),(3,2,0),(3,2,1)}
        parts={s:[] for s in b.SPLITS}
        for a in itertools.permutations(range(4),3):
            split='TRAIN' if a in train else 'HOLDOUT'
            for lang in ('en','ja'):
                for order in (0,1):
                    for q in range(3):
                        r=dict(id=f'{lang}-{a[0]}{a[1]}{a[2]}-{order}-{q}',assignment=list(a),language=lang,order=order,query=q,target=48+a[q])
                        r['prompt']=Orders.render(dict(r,permutation=list(Orders.ORDERS[order])),'normal');parts[split].append(r)
        return parts
    @staticmethod
    def metrics(rows,raw):
        pred=Orders.predictions(raw,len(rows));out={}
        for lang in ('en','ja'):
            ids=[i for i,r in enumerate(rows) if r['language']==lang];order=defaultdict(list);queries=defaultdict(list)
            for i in ids:
                r=rows[i];order[(tuple(r['assignment']),r['query'])].append(i);queries[(tuple(r['assignment']),r['order'])].append(i)
            c=Orders.cell(rows,pred,ids,queries);c['order_pair_accuracy']=sum(all(pred['normal'][i]==rows[i]['target'] for i in g) for g in order.values())/36
            out[lang]=c
        return out,pred
    @staticmethod
    def cell_pass(c):return Orders.new_cell_pass(c) and c['order_pair_accuracy']>=.8


class Orders:
    ORDERS=((0,1,2),(2,1,0),(0,2,1),(1,0,2),(1,2,0),(2,0,1))
    @staticmethod
    def render(r,view):
        names=('a','b','c') if r['language']=='en' else ('甲','乙','丙')
        return ';'.join(names[i]+'='+('?' if view=='evidence_blind' else str(r['assignment'][i])) for i in r['permutation'])+';'+('?' if view=='query_blind' else names[r['query']])+'='
    @staticmethod
    def novel_dataset(parts):
        result={s:[] for s in b.SPLITS}
        for s,rows in parts.items():
            for old in rows:
                if old['order']!=0:continue
                for p in Orders.ORDERS[2:]:
                    r=dict(source_id=old['id'],id=old['id']+':'+''.join(map(str,p)),assignment=list(old['assignment']),language=old['language'],query=old['query'],target=old['target'],permutation=list(p))
                    r['prompt']=Orders.render(r,'normal');result[s].append(r)
        return result
    @staticmethod
    def predictions(raw,n):
        b.require(set(raw)==set(b.VIEWS),'views')
        for x in raw.values():b.require(x.shape==(n,256) and x.dtype==torch.float64 and bool(torch.isfinite(x).all()),'finite logits')
        return {k:v.argmax(-1).tolist() for k,v in raw.items()}
    @staticmethod
    def cell(rows,pred,ids,groups):
        acc={v:sum(pred[v][i]==rows[i]['target'] for i in ids)/len(ids) for v in b.VIEWS}
        return dict(rows=len(ids),accuracy=acc['normal'],query_triplet_accuracy=sum(all(pred['normal'][i]==rows[i]['target'] for i in g) for g in groups.values())/len(groups),evidence_drop=acc['normal']-acc['evidence_blind'],query_drop=acc['normal']-acc['query_blind'])
    @staticmethod
    def new_metrics(rows,raw):
        pred=Orders.predictions(raw,288);out=[]
        for lang in ('en','ja'):
            for p in Orders.ORDERS[2:]:
                ids=[i for i,r in enumerate(rows) if r['language']==lang and tuple(r['permutation'])==p];groups=defaultdict(list)
                for i in ids:groups[tuple(rows[i]['assignment'])].append(i)
                out.append(dict(language=lang,permutation=list(p),**Orders.cell(rows,pred,ids,groups)))
        return out,pred
    @staticmethod
    def new_cell_pass(c):return c['accuracy']>=.9 and c['query_triplet_accuracy']>=.8 and c['evidence_drop']>=.35 and c['query_drop']>=.35
    @staticmethod
    def six_order_metrics(old,new,op,np):
        groups=defaultdict(list)
        for rows,pred in ((old,op),(new,np)):
            for r,p in zip(rows,pred,strict=True):groups[(r['language'],tuple(r['assignment']),r['query'])].append(p==r['target'])
        b.require(len(groups)==72 and all(len(v)==6 for v in groups.values()),'six groups')
        return {l:dict(groups=36,all_six_correct=sum(all(v) for k,v in groups.items() if k[0]==l),accuracy=sum(all(v) for k,v in groups.items() if k[0]==l)/36) for l in ('en','ja')}


class Parent:
    @staticmethod
    def training_tables(parts,factory,orders):
        rows=parts['TRAIN'];tables=[]
        for pair in range(3):tables.append(torch.stack([factory.prefix_tensor(orders.render(dict(r,permutation=list(orders.ORDERS[2*pair+r['order']])),'normal').encode()) for r in rows]))
        return torch.stack(tables),torch.tensor([r['target'] for r in rows])
    @staticmethod
    def evaluate(model,parts,extra,base,orders,factory):
        raw={};before=base.fingerprint(model);model.eval()
        with torch.no_grad():
            for name,data in (('original',parts),('extra',extra)):
                raw[name]={}
                for split,rows in data.items():
                    raw[name][split]={}
                    for view in b.VIEWS:
                        converted=[dict(r,permutation=list(orders.ORDERS[r['order']])) if name=='original' else r for r in rows]
                        tokens=torch.stack([factory.prefix_tensor(orders.render(r,view).encode()) for r in converted])
                        raw[name][split][view]=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
        b.require(base.fingerprint(model)==before,'mutation');return raw
    @staticmethod
    def replay_one(model,state,r,parts,extra,base,orders,factory):
        model.load_state_dict(state,strict=True);model.eval();b.require(base.fingerprint(model)==r['final_sha256'],'checkpoint')
        raw=Parent.evaluate(model,parts,extra,base,orders,factory);err=0.
        for stage in raw:
            for split in b.SPLITS:
                for v in b.VIEWS:
                    x,y=raw[stage][split][v],r['raw'][stage][split][v];err=max(err,float((x-y).abs().max()))
                    b.require(torch.equal(x.argmax(-1),y.argmax(-1)),'argmax')
        b.require(err<=b.TOL,'replay');r.update(checkpoint_roundtrip=True,reload_max_error=err,replay_forward_calls=12,replay_row_presentations=2592)


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith('fixture-input-'):return '0'*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding='utf-8'))
    @staticmethod
    def safe_child(root,name):
        child=(Path(root)/name).resolve();b.require(child.parent==Path(root).resolve(),'safe child');return child
    @staticmethod
    def git(root,*args):
        if args==('rev-parse','HEAD'):return b'fixture-head'
        if args==('branch','--show-current'):return b'feat/sft-target-loss'
        return b''


def protection():
    return {**{f'old-{i}':'fixture' for i in range(400)},**{n:'fixture' for n in b.OWN}},{f'fixture-input-{i}':'0'*64 for i in range(672)}


def perfect_records(parts,extra):
    raw={}
    for name,data in (('original',parts),('extra',extra)):
        raw[name]={}
        for split,rows in data.items():
            raw[name][split]={}
            for view in b.VIEWS:
                x=torch.full((len(rows),256),-10.,dtype=torch.float64)
                for i,r in enumerate(rows):x[i,r['target'] if view=='normal' else 48]=10.
                raw[name][split][view]=x
    return [dict(seed=s,arm=a,parameters=b.PARAMETERS[a],common_initial_sha256=str(s),final_sha256='fixture',weights_changed=True,common_changed=True,head_changed=True,checkpoint_roundtrip=True,
        forward_calls=812,row_presentations=40992,core_forward_calls=3248 if a=='with_core' else 0,replay_core_forward_calls=48 if a=='with_core' else 0,replay_forward_calls=12,replay_row_presentations=2592,reload_max_error=0.,
        fit=dict(steps=800,answer_presentations=38400,logical_batch_sha256='fixture',order_pair_updates=[267,267,266]),raw=copy.deepcopy(raw)) for s,a in b.identities()]


class C260Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.parts=Base.dataset();cls.extra=Orders.novel_dataset(cls.parts)
        cls.tokens,cls.targets=Parent.training_tables(cls.parts,Factory,Orders);cls.records=perfect_records(cls.parts,cls.extra)

    def test_01_manifest_and_hash_contract(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),b.manifest()['original_dataset_sha256']);self.assertEqual(b.digest(self.extra),b.manifest()['extra_dataset_sha256'])
        with contextlib.redirect_stdout(io.StringIO()):
            b.validate_registration(406,672)
            with self.assertRaises(ValueError):b.validate_registration(405,672)
            with patch.object(b,'MANIFEST_SHA','bad'),self.assertRaises(ValueError):b.validate_registration(406,672)

    def test_02_pair_capacity_and_surviving_state(self):
        full,free=b.make_pair(b.SEEDS[0],Base,None,None,Factory)
        self.assertEqual([sum(p.numel() for p in m.parameters()) for m in (full,free)],[14256,10928])
        self.assertEqual(b.common_fingerprint(full),b.common_fingerprint(free));self.assertIsNone(free.backbone.core)
        self.assertFalse(any(k.startswith('backbone.core.') for k in free.state_dict()))

    def test_03_no_template_mutation_or_alias(self):
        t=Template(b.SEEDS[0]);before=Base.fingerprint(t);free=b.CoreFreeReadout(t)
        self.assertEqual(before,Base.fingerprint(t));self.assertIsNotNone(t.backbone.core)
        with torch.no_grad():free.read.output.weight.add_(1)
        self.assertEqual(before,Base.fingerprint(t))

    def test_04_free_forward_matches_explicit_formula(self):
        m=b.CoreFreeReadout(Template(b.SEEDS[0]));x=self.tokens[0,:4];valid=x!=256;pre=m.backbone.encode_local(x);q=pre[torch.arange(4),valid.sum(1)-1]
        alpha=((m.read.key(pre)*m.read.query(q)[:,None]).sum(-1)/4).masked_fill(~valid,float('-inf')).softmax(-1)
        want=m.backbone.decoder(m.backbone.readout_norm(q+m.read.output((alpha[:,:,None]*pre).sum(1))))
        self.assertTrue(torch.equal(m(x,torch.zeros(4,dtype=torch.int64)),want))

    def test_05_free_path_never_calls_full_backbone(self):
        m=b.CoreFreeReadout(Template(b.SEEDS[0]));x=self.tokens[0,:2]
        with patch.object(m.backbone,'forward',side_effect=AssertionError('no backbone forward')):
            self.assertEqual(m(x,torch.zeros(2,dtype=torch.int64)).shape,(2,256))

    def test_06_gradients_reach_encoder_reader_decoder(self):
        m=b.CoreFreeReadout(Template(b.SEEDS[0]));m(self.tokens[0,:4],torch.zeros(4,dtype=torch.int64)).square().mean().backward()
        for p in (m.read.query.weight,m.read.key.weight,m.read.output.weight,m.backbone.local_encoder.weight_ih_l0,m.backbone.decoder.weight):
            self.assertIsNotNone(p.grad);self.assertTrue(torch.isfinite(p.grad).all());self.assertGreater(float(p.grad.abs().sum()),0.)

    def test_07_invalid_task_and_eos(self):
        m=b.CoreFreeReadout(Template(b.SEEDS[0]));x=self.tokens[0,:2].clone()
        with self.assertRaises(ValueError):m(x,torch.ones(2,dtype=torch.int64))
        x[x==258]=0
        with self.assertRaises(ValueError):m(x,torch.zeros(2,dtype=torch.int64))

    def test_08_all800_step_schedule_and_tail(self):
        counts=[0,0,0]
        for i in range(800):
            a,p=b.batch_plan(b.SEEDS[0],i);c,q=b.batch_plan(b.SEEDS[0],i)
            self.assertTrue(torch.equal(a,c));self.assertEqual(p,q);counts[p]+=1
        self.assertEqual(counts,[267,267,266])
        with self.assertRaises(ValueError):b.batch_plan(259002,0)

    def test_09_nine_step_coverage_and_no_holdout(self):
        seen=defaultdict(list)
        for step in range(9):
            ids,pair=b.batch_plan(b.SEEDS[0],step)
            for i in ids.tolist():
                r=self.parts['TRAIN'][i];seen[(tuple(r['assignment']),r['language'],r['query'])].append(Orders.ORDERS[2*pair+r['order']])
        self.assertEqual(len(seen),72)
        for orders in seen.values():self.assertEqual(sorted(orders),sorted(Orders.ORDERS))
        altered=dict(self.parts,HOLDOUT=[]);x,y=Parent.training_tables(altered,Factory,Orders)
        self.assertTrue(torch.equal(x,self.tokens));self.assertTrue(torch.equal(y,self.targets))

    def test_10_actual_fit_loop_three_step_fixture(self):
        m=b.CoreFreeReadout(Template(b.SEEDS[0]));before=Base.fingerprint(m)
        with patch.object(b,'STEPS',3):r=b.fit(m,self.tokens,self.targets,b.SEEDS[0])
        self.assertEqual(r['steps'],3);self.assertNotEqual(before,Base.fingerprint(m))

    def test_11_actual_800_step_free_training_and_replay(self):
        m=b.CoreFreeReadout(Template(b.SEEDS[0]))
        with contextlib.redirect_stdout(io.StringIO()):r,state=b.train_one(m,self.parts,self.extra,self.tokens,self.targets,b.SEEDS[0],'without_core',Parent,Base,Orders,Factory)
        b.replay_one(b.CoreFreeReadout(Template(b.SEEDS[0])),state,r,self.parts,self.extra,Parent,Base,Orders,Factory)
        self.assertEqual((r['core_forward_calls'],r['replay_core_forward_calls']),(0,0));self.assertEqual(r['reload_max_error'],0.)
        self.assertEqual((r['forward_calls'],r['row_presentations']),(812,40992))

    def test_12_core_counter_and_hook_cleanup(self):
        m=Template(b.SEEDS[0]);calls,h=b.core_counter(m);m(self.tokens[0,:2],torch.zeros(2,dtype=torch.int64));h.remove()
        self.assertEqual(calls,[4]);self.assertFalse(m.backbone.core._forward_hooks)

    def test_13_perfect_gate_and_paired_comparisons(self):
        _,s=b.analyze(self.records,self.parts,self.extra,Base,Orders)
        self.assertTrue(s['candidate_gate']);self.assertEqual(s['seed_pass_counts'],{'with_core':5,'without_core':5})
        self.assertTrue(all(c['accuracy_delta']==0 for c in s['comparisons']))

    def test_14_control_cannot_rescue_or_fail_candidate(self):
        r=copy.deepcopy(self.records);r[0]['raw']['extra']['HOLDOUT']['normal'][:]=0
        self.assertTrue(b.analyze(r,self.parts,self.extra,Base,Orders)[1]['candidate_gate'])
        r=copy.deepcopy(self.records);r[1]['raw']['extra']['HOLDOUT']['normal'][:]=0
        self.assertFalse(b.analyze(r,self.parts,self.extra,Base,Orders)[1]['candidate_gate'])

    def test_15_original_and_per_order_gates(self):
        for stage,reason in (('original','ORIGINAL_CRITERIA_MISS'),('extra','EXTRA_ORDER_MISS')):
            r=copy.deepcopy(self.records);r[1]['raw'][stage]['TRAIN']['normal'][:]=0
            self.assertEqual(b.analyze(r,self.parts,self.extra,Base,Orders)[0][1]['outcome'],reason)

    def test_16_six_order_gate_not_mean(self):
        r=copy.deepcopy(self.records);rows=self.extra['TRAIN'];a=sorted({tuple(x['assignment']) for x in rows})
        for j,p in enumerate(Orders.ORDERS[2:]):
            ids=[i for i,x in enumerate(rows) if x['language']=='en' and tuple(x['permutation'])==p and x['query']==0 and tuple(x['assignment']) in a[2*j:2*j+2]]
            r[1]['raw']['extra']['TRAIN']['normal'][ids]=0
        self.assertEqual(b.analyze(r,self.parts,self.extra,Base,Orders)[0][1]['outcome'],'SIX_ORDER_MISS')

    def test_17_identity_counts_nonfinite_and_pairs(self):
        for key,val in (('parameters',14256),('core_forward_calls',1),('reload_max_error',2e-9),('common_initial_sha256','bad')):
            r=copy.deepcopy(self.records);r[1][key]=val
            with self.assertRaises(ValueError):b.analyze(r,self.parts,self.extra,Base,Orders)
        r=copy.deepcopy(self.records);r[1]['raw']['extra']['TRAIN']['normal'][0,0]=float('nan')
        with self.assertRaises(ValueError):b.analyze(r,self.parts,self.extra,Base,Orders)

    def test_18_parent_valid_negative_loader_dispatch(self):
        p=dict(status='FAIL',validation_summary={'seed_pass_counts':{'two_order':2,'six_order':4}},artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        parent=SimpleNamespace(verify_artifacts=Mock(return_value=(p,[{}]*10)))
        a=SimpleNamespace(sha=lambda path:b.PARENT_SHA)
        with patch.object(b,'context',return_value=(parent,None,None,None,None,None,a)):
            path=Path(tempfile.gettempdir())/'c260-review'/'summary.json'
            self.assertEqual(b.load_parent(path),p)
            parent.verify_artifacts.assert_called_once_with(path.resolve().parent,b.PARENT_EXECUTION)
            p['status']='PASS'
            with self.assertRaises(ValueError):b.load_parent(path)

    def test_19_actual_run_persisted_postcheck(self):
        def trained(model,parts,extra,tokens,targets,seed,arm,parent,base,orders,factory):
            r=copy.deepcopy(self.records[b.identities().index((seed,arm))]);r['common_initial_sha256']=b.common_fingerprint(model)
            with torch.no_grad():model.read.output.weight.add_(.01)
            r.update(final_sha256=base.fingerprint(model),raw=Parent.evaluate(model,parts,extra,base,orders,factory))
            return r,copy.deepcopy(model.state_dict())
        with tempfile.TemporaryDirectory() as d,patch.object(b,'context',return_value=(Parent,Base,Orders,None,None,Factory,Audit)),patch.object(b,'precheck',return_value=protection()),patch.object(b,'train_one',side_effect=trained) as train:
            out=Path(d)/'out'
            with contextlib.redirect_stdout(io.StringIO()):p=b.run(c259_summary=Path(d)/'parent.json',output_dir=out,expected_head='fixture-head')
            self.assertEqual(train.call_count,10)
            with patch.object(b,'make_pair',side_effect=AssertionError('no new model in postcheck')):
                self.assertEqual(b.verify_artifacts(out,'fixture-head')[0],p)
            with self.assertRaisesRegex(ValueError,'saved HEAD'):b.verify_artifacts(out,'wrong')
            (out/'measurements.json').write_bytes(b'[]')
            with self.assertRaises(ValueError):b.verify_artifacts(out,'fixture-head')

    def test_20_saved_bundle_schema(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'models.pt';v=dict(schema='fold-c260-core-models-v1',identities=[list(x) for x in b.identities()],states=[{}]*10)
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),10)
            v['identities'].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)

    def test_21_semantic_own_count_and_inherited_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));self.assertEqual(suite.countTestCases(),b.manifest()['own_tests'])
        class Dummy(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        s=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f'fixture-{i}') for i in range(b.manifest()['focused_tests'])])
        with patch.object(b,'regression_modules',return_value=[]),patch.object(unittest.defaultTestLoader,'loadTestsFromNames',return_value=s):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()['focused_tests'])

    def test_22_runner_cli_and_parser_order(self):
        root=Path(__file__).resolve().parents[1];runner=(root/'tools/run_c260.ps1').read_text(encoding='utf-8');launcher=(root/'tools/invoke_c260.ps1').read_text(encoding='utf-8')
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3);indices=[]
        for block in blocks:
            compile(block,'embedded','exec')
            indices.append({n.slice.value for n in ast.walk(ast.parse(block)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=='sys' and n.value.attr=='argv'})
        self.assertEqual(indices,[{1},set(),{1,2,3}]);failure=re.search(r'(?m)^\s*\$failure\s*=\s*\$null\s*$',launcher)
        self.assertIsNotNone(failure);self.assertLess(launcher.index('::ParseFile'),failure.start());self.assertLess(launcher.index('STALE_EXPECTED_HEAD'),failure.start())
        self.assertIn('7042b90d1ed54cc0858291e661d329e8',launcher)

    def test_23_source_scientific_dispatch_and_no_full_forward(self):
        import inspect
        def calls(f):return [(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else '') for n in ast.walk(ast.parse(textwrap.dedent(inspect.getsource(f)))) if isinstance(n,ast.Call)]
        seq=calls(b.run);first=lambda name:min(i for i,n in seq if n==name)
        for l,r in (('precheck','make_pair'),('make_pair','train_one'),('train_one','load_bundle'),('load_bundle','replay_one'),('replay_one','analyze')):self.assertLess(first(l),first(r))
        self.assertIn('load_parent',[n for _,n in calls(b.precheck)])
        self.assertNotIn('core',[n for _,n in calls(b.CoreFreeReadout.forward)])

    def test_24_result_scope_and_resource_guards(self):
        _,s=b.analyze(self.records,self.parts,self.extra,Base,Orders);pins,protected=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status='PASS',source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False,core_superiority_claim=False,unseen_order_transfer_claim=False,network_calls=0)
        b.validate_result(p)
        with self.assertRaises(ValueError):b.validate_result(dict(p,core_superiority_claim=True))
        p['validation_summary']['core_forward_calls']=0
        with self.assertRaises(ValueError):b.validate_result(p)


if __name__=='__main__':
    unittest.main(verbosity=2)
