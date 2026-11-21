"""C322 independent arithmetic and software-contract tests; no real parent archives here."""
import ast
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
from fold_lm.v05_benchmarks import model_c322_saved_query_contrast as b


def data_fixture():
    out={s:[] for s in b.SPLITS}
    for e,v,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),b.LANGUAGES):
        s='HOLDOUT' if (v[1]-v[0])%4==2 else 'TRAIN'
        for order,q in itertools.product((e,e[::-1]),e):
            out[s].append(dict(id=f'{lang}:{e}:{v}:{order}:{q}',entities=list(e),values=list(v),permutation=list(order),query=q,language=lang,target=48+v[e.index(q)]))
    return out


def check(z,n):
    b.require(z.shape==(n,256) and z.dtype==torch.float64 and z.device.type=='cpu' and bool(torch.isfinite(z).all()),'logits')


def score(data,raw,c):
    totals=[]
    for s in b.SPLITS:
        ys=[r['target'] for r in data[s]]; correct=collapsed=0
        for z in (v['normal'] for v in raw[s].values()):
            pred=z.argmax(1).tolist(); correct+=sum(a==v for a,v in zip(pred,ys,strict=True))
            collapsed+=sum(pred[i]==pred[i+1] for i in range(0,len(ys),2))
        totals.append(dict(split=s,rows=len(ys)*3,correct=correct,pairs=len(ys)*3//2,collapsed_pairs=collapsed,full_pass=correct==len(ys)*3))
    return dict(passed=all(t['full_pass'] for t in totals),totals=totals)


class Audit:
    @staticmethod
    def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).is_file() else 'a'*64
    @staticmethod
    def read_json(p): return json.loads(Path(p).read_text(encoding='utf-8'))
    @staticmethod
    def safe_child(root,n): return Path(root)/n


@contextlib.contextmanager
def no_neural():
    with torch.no_grad(),patch.object(torch.nn.Module,'_call_impl',side_effect=AssertionError('neural call forbidden')),patch.object(torch.nn.Module,'load_state_dict',side_effect=AssertionError('weights forbidden')): yield


def fixtures():
    data=data_fixture(); records=[]; parts=[]
    for seed,arm in b.identities():
        raw={}
        for condition in b.CONDITIONS:
            labels=b.OLD_PROFILES if condition=='old4' else b.PROFILES; raw[condition]={}
            for split in b.SPLITS:
                y=torch.tensor([r['target'] for r in data[split]]); z=torch.zeros((len(y),256),dtype=torch.float64)
                if condition=='old4': z[torch.arange(len(y)),y]=4.
                else: z[:,48]=4.
                raw[condition][split]={p:dict(normal=z) for p in labels}
        records.append(dict(seed=seed,arm=arm,readout_policy=arm,weights_preserved=True,hooks_restored=True,raw=dict(before={'4':raw['old4']},interior=raw['interior'])))
        parts.extend(dict(seed=seed,arm=arm,**r) for r in score(data,raw['interior'],None)['totals'])
    parent=NS(score_new=lambda raw,data,x:score(data,raw,x.c),OUTPUTS=('evaluation-plan.json','interior-prompts.json','evaluations.pt','measurements.json','validation-summary.json'),PARENT_SHA='b'*64)
    x=NS(wide=NS(score_length=score,context=lambda:()),diag=NS(normalize_task=lambda z,*_:z['totals'],partition=lambda v:{k:x for k,x in v[0].items() if k!='split'}),guarded=NS(no_neural=no_neural),c=NS(audit=Audit(),p267=NS(check_logits=check),factory=NS(language_module=lambda:None)),parent=NS(context=lambda:()),p312=NS(context=lambda:()))
    return data,records,dict(final_partitions=parts),parent,x


def protection():
    pins={n:'a'*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<778: pins['fixture/'+str(len(pins))]='a'*40
    return pins,{'fixture/input/'+str(i):'a'*64 for i in range(1467)}


def payload(s):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,status='PASS',commit_sha='f'*40,diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


class C322Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); torch.set_num_threads(2)
        cls.data,cls.records,cls.parent_summary,cls.p,cls.x=fixtures()
        cls.pairs,cls.groups,cls.summary=b.analyze(cls.records,cls.data,cls.p,cls.x,cls.parent_summary)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads)
    def logits(self,a=3.,d=-2.):
        x=torch.zeros(256,dtype=torch.float64); z=x.clone(); x[48]=a; z[48]=d; return x,z
    def test_01_manifest(self):
        b.validate_seal()
        with patch.object(b,'MANIFEST_SHA','0'*64),self.assertRaises(ValueError): b.validate_seal()
    def test_02_arithmetic_oracle(self):
        x,z=self.logits(); r=b.pair_measure(x,z,48,49)
        self.assertEqual((r['margin_A'],r['margin_B'],r['contrast'],r['raw_linf'],r['shift_invariant_linf']),(3.,-2.,5.,5.,5.))
        self.assertTrue(r['both_target_directions']); self.assertEqual(r['correct_count'],1)
    def test_03_scalar_shift_removed(self):
        x=torch.arange(256,dtype=torch.float64); r=b.pair_measure(x,x+16.,48,49)
        self.assertEqual((r['raw_linf'],r['shift_invariant_linf'],r['contrast']),(16.,0.,0.)); self.assertTrue(r['same_prediction'])
    def test_04_same_argmax_not_same_logits(self):
        x,z=self.logits(); x[70]=z[70]=10.; r=b.pair_measure(x,z,48,49)
        self.assertTrue(r['same_prediction']); self.assertGreater(r['contrast'],0); self.assertFalse(r['near_shift_invariant']); self.assertEqual(r['correct_count'],0)
    def test_05_reversed_and_zero_signs(self):
        x,z=self.logits(); self.assertEqual(b.pair_measure(z,x,48,49)['contrast_sign'],-1)
        self.assertEqual(b.pair_measure(x,x,48,49)['contrast_sign'],0)
    def test_06_ties_keep_original_decoder(self):
        x=torch.zeros(256,dtype=torch.float64); r=b.pair_measure(x,x,48,49)
        self.assertEqual((r['prediction_A'],r['prediction_B'],r['correct_count']),(0,0,0)); self.assertFalse(r['both_target_directions'])
    def test_07_nonfinite_shape_grad(self):
        x,z=self.logits()
        for bad in (x.float(),x[:255],x.clone().requires_grad_(),torch.full_like(x,float('nan'))):
            with self.assertRaises(ValueError): b.pair_measure(bad,z,48,49)
        with self.assertRaises(ValueError): b.pair_measure(x,z,48,48)
    def test_08_pairing_not_adjacency(self):
        rows=copy.deepcopy(self.data['HOLDOUT']); rows=rows[::2]+rows[1::2]
        indices=b.pair_rows(rows); self.assertEqual(len(indices),48)
        for i,j in indices: self.assertEqual((rows[i]['query'],rows[j]['query']),tuple(rows[i]['entities']))
    def test_09_bad_pair_id_target(self):
        rows=copy.deepcopy(self.data['TRAIN'])
        with self.assertRaises(ValueError): b.pair_rows(rows[:-1])
        with self.assertRaises(ValueError): b.pair_rows(rows+[rows[0]])
        rows[0]['target']=70
        with self.assertRaises(ValueError): b.pair_rows(rows)
    def test_10_aggregate_conservation(self):
        x,z=self.logits(); rows=[b.pair_measure(x,z,48,49),b.pair_measure(x,x,48,49)]
        a=b.aggregate(rows); self.assertEqual((a['pairs'],a['answers'],a['contrast_positive'],a['contrast_zero']),(2,4,1,1))
        with self.assertRaises(ValueError): b.aggregate([])
    def test_11_full_inventory(self):
        self.assertEqual((len(self.pairs),len(self.groups),len(self.summary['reconciliations'])),(8640,240,40)); b.validate_result(payload(self.summary))
        self.assertEqual(sum(g['pairs'] for g in self.groups),8640)
    def test_12_bad_cohort_provenance(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.data,self.p,self.x,self.parent_summary)
        rr=copy.deepcopy(self.records); rr[0]['readout_policy']='changed'
        with self.assertRaises(ValueError): b.analyze(rr,self.data,self.p,self.x,self.parent_summary)
    def test_13_parent_reconciliation(self):
        s=copy.deepcopy(self.parent_summary); s['final_partitions'][0]['correct']+=1
        with self.assertRaisesRegex(ValueError,'parent aggregate'): b.analyze(self.records,self.data,self.p,self.x,s)
    @contextlib.contextmanager
    def loader(self):
        paths=[(Path('/c322')/str(i)/'summary.json').resolve() for i in range(48)]
        hashes=dict(zip(map(str,paths),(b.PARENT_SHA,'b'*64,*[str(i%10)*64 for i in range(46)]),strict=True))
        e=dict(experiment_id='C321-v5b-frozen-interior-name-order',commit_sha=b.PARENT_EXECUTION,status='FAIL',source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},validation_summary=dict(self.parent_summary,pass_counts=dict.fromkeys(b.ARMS,0),primary_gate=False),artifacts=[dict(file=n) for n in self.p.OUTPUTS])
        p=NS(PARENT_SHA='b'*64,OUTPUTS=self.p.OUTPUTS,verify_artifacts=Mock(return_value=(e,[])),validate_result=Mock(),load_parent=Mock(return_value=({},self.data,{},[])))
        tail_hashes=tuple(list(hashes.values())[2:]); parent=NS(parent_hashes=lambda _:tail_hashes); x=copy.copy(self.x); x.c=NS(audit=NS(sha=lambda p:hashes[str(p)])); archive=dict(schema='fold-c321-interior-eval-v1',records=self.records)
        with patch.object(b,'context',return_value=(p,parent,None,x)),patch.object(torch,'load',return_value=archive): yield paths,hashes,p,e,archive
    def test_14_all48_hashes(self):
        with self.loader() as (paths,hashes,p,e,a):
            self.assertEqual(b.load_parent(paths)[0],e); p.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=hashes[str(path)]; hashes[str(path)]='f'*64; p.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                p.verify_artifacts.assert_not_called(); hashes[str(path)]=old
    def test_15_parent_status_and_archive(self):
        for fn in (lambda e,a:e.update(status='PASS'),lambda e,a:e['artifacts'].pop(),lambda e,a:a.update(schema='model-weights')):
            with self.loader() as (paths,_,p,e,a):
                fn(e,a)
                with self.assertRaises(ValueError): b.load_parent(paths)
    def test_16_protection_real_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins={b.PARENT_SOURCE:b.PARENT_BLOB}
            while len(pins)<772: pins['accepted/'+str(len(pins))]='a'*40
            for n in list(pins)+list(b.OWN): path=root/n; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(n,encoding='utf-8')
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1455-len(inputs)):
                path=root/('input'+str(i)); path.write_text('x',encoding='utf-8'); inputs[str(path)]=Audit.sha(path)
            folder=root/'parent'; folder.mkdir(); summary=folder/'summary.json'; summary.write_text('summary',encoding='utf-8'); artifacts=[]
            for n in self.p.OUTPUTS: path=folder/n; path.write_text('artifact',encoding='utf-8'); artifacts.append(dict(file=n,sha256=Audit.sha(path)))
            def sha(path): return b.PARENT_SHA if Path(path)==summary else Audit.sha(path)
            p=types.ModuleType('parent'); p.__file__=str(root/b.PARENT_SOURCE); owner=NS(context=lambda:()); x=copy.copy(self.x)
            x.c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,safe_child=Audit.safe_child,git=lambda root,*a:(pins.get(a[1][5:],'b'*40)+'\n').encode(),protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp}))
            loaded=(dict(source_blobs=pins,input_sha256=inputs,artifacts=artifacts),None,None)
            with patch.object(b,'context',return_value=(p,None,owner,x)),patch.object(b,'load_parent',return_value=loaded),contextlib.redirect_stdout(io.StringIO()):
                a,c,_=b.precheck([summary]*48,root); self.assertEqual((len(a),len(c)),(778,1467))
                x.c.missing=types.ModuleType('missing'); x.c.missing.__file__=str(root/'missing.py')
                with self.assertRaisesRegex(ValueError,'unprotected helper'): b.precheck([summary]*48,root)
    @contextlib.contextmanager
    def run_fixture(self):
        loaded=(dict(validation_summary=self.parent_summary),self.data,self.records); owner=NS(context=lambda:(None,NS(guard=lambda *a:None)))
        with patch.object(b,'context',return_value=(self.p,None,owner,self.x)),patch.object(b,'precheck',return_value=(*protection(),loaded)),patch.object(b,'load_parent',return_value=loaded): yield
    def test_17_production_run_and_json_only(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,patch.object(torch,'save',side_effect=AssertionError('no tensor save')),patch.object(torch.optim,'AdamW',side_effect=AssertionError('no training')),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'run'; p=b.run(summaries=['x']*48,output_dir=out,expected_head='f'*40)
            self.assertEqual({z.name for z in out.iterdir()},set(b.OUTPUTS)|{'summary.json'}); q,_=b.verify_artifacts(out,['x']*48,'f'*40); self.assertEqual(p,q)
    def test_18_tamper_and_no_overwrite(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'run'; p=b.run(summaries=['x']*48,output_dir=out,expected_head='f'*40); path=out/'measurements.json'; path.write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'output bytes'): b.verify_artifacts(out,['x']*48,'f'*40)
            a=next(a for a in p['artifacts'] if a['file']==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size); (out/'summary.json').write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,'persisted'): b.verify_artifacts(out,['x']*48,'f'*40)
            with self.assertRaises(FileExistsError): b.run(summaries=['x']*48,output_dir=out,expected_head='f'*40)
    def test_19_runtime_same_analyzer(self):
        with self.run_fixture(),contextlib.redirect_stdout(io.StringIO()): b.runtime_preflight(['x']*48,Path.cwd())
    def test_20_exact_suite_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=['f.'+str(i) for i in range(5269)]+[b.EXCLUDED]
        with patch.object(b,'regression_modules',return_value=[]),patch.object(unittest.defaultTestLoader,'loadTestsFromNames',return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual([t.id() for t in b.flatten(b.regression_suite(Path.cwd()))],ids[:-1])
        with patch.object(b,'regression_modules',return_value=[]),patch.object(unittest.defaultTestLoader,'loadTestsFromNames',return_value=unittest.TestSuite([Dummy('x'),Dummy('x')])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())
    def test_21_cli_and_import_binding(self):
        argv=['prog','--summaries']+['x']*48+['--output-dir','out','--expected-head','f'*40]
        with patch.object(sys,'argv',argv),patch.object(b,'run') as run: b.main(); self.assertEqual(len(run.call_args.kwargs['summaries']),48)
        p=NS(context=lambda:('parent','owner','x'),regression_modules=lambda root:['m'+str(i) for i in range(206)])
        package=types.ModuleType('fold_lm.v05_benchmarks'); package.model_c321_interior_name_order=p
        with patch.dict(sys.modules,{'fold_lm.v05_benchmarks':package}): self.assertEqual(b.context(),(p,'parent','owner','x')); self.assertEqual(len(b.regression_modules(Path.cwd())),207)
    def test_22_utf8(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,'text_encoding',side_effect=lambda encoding,stacklevel=2:'cp932' if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding='utf-8'))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding='utf-8'))
    def test_23_runner_contract(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding='utf-8'); launcher=(root/b.OWN[3]).read_text(encoding='utf-8')
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: compile(code,'embedded','exec')
        self.assertIn('sys.argv[2:50]',blocks[2]); self.assertIn('head = sys.argv[50]',blocks[2]); self.assertIn('len(sys.argv) == 51',blocks[2])
        self.assertEqual(re.findall(r'runs\\c(\d{3})-.*?\\summary.json',launcher),[str(n) for n in range(321,273,-1)])
        self.assertLess(launcher.index('-Mode Validate'),launcher.index('-Mode Execute')); self.assertIn('science_exit_hex',runner); self.assertIn('regression_exit_hex',runner)
    def test_24_scope_and_counts(self):
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),24)
        for fn in (lambda p:p.update(capability_gate_applicable=True),lambda p:p['validation_summary'].update(model_forward_calls=False),lambda p:p['validation_summary'].update(diagnostic_complete=False)):
            p=payload(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)

if __name__=='__main__': unittest.main()
