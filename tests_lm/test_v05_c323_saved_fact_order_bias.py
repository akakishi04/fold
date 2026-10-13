"""C323 independent fixed-fact-order software controls, not actual saved evidence."""
from __future__ import annotations
import argparse
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
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c323_saved_fact_order_bias as b


def fixture_data():
    out={s:[] for s in b.SPLITS}
    for entities,values,language in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),b.LANGUAGES):
        split='HOLDOUT' if (values[1]-values[0])%4==2 else 'TRAIN'
        for order,query in itertools.product((entities,entities[::-1]),entities):
            out[split].append(dict(id=f'{language}:{entities}:{values}:{order}:{query}',
                entities=list(entities),values=list(values),language=language,permutation=list(order),
                query=query,target=48+values[entities.index(query)]))
    return out


def parent_pairs(data):
    rows=[]
    for seed,arm,condition,split,profile in itertools.product(b.SEEDS,b.ARMS,b.CONDITIONS,b.SPLITS,b.PROFILES):
        pairs={}
        for r in data[split]:
            k=(r['language'],tuple(r['entities']),tuple(r['values']),tuple(r['permutation']))
            pairs.setdefault(k,{})[r['query']]=r
        for (lang,entities,values,perm),group in pairs.items():
            first=48+values[entities.index(perm[0])]
            if condition=='old4': pa,pb=(group[e]['target'] for e in entities)
            else:
                chosen=48+values[entities.index(perm[-1] if arm=='last_only' and profile=='balanced' else perm[0])]
                pa=pb=chosen
            r=dict(seed=seed,arm=arm,condition=condition,split=split,profile=profile,language=lang,
                   source_profile=('repeat','shared_prefix','shared_suffix')[b.PROFILES.index(profile)] if condition=='old4' else profile,
                   row_A=group[entities[0]]['id'],row_B=group[entities[1]]['id'],
                   prediction_A=pa,prediction_B=pb,target_A=group[entities[0]]['target'],target_B=group[entities[1]]['target'],
                   correct_count=int(pa==group[entities[0]]['target'])+int(pb==group[entities[1]]['target']),
                   same_prediction=pa==pb)
            rows.append(r)
    return rows


def parent_summary(pairs):
    return dict(overall=[dict(arm=arm,condition=condition,
             answers=2*len(subset),correct=sum(r['correct_count'] for r in subset),
             pairs=len(subset),same_prediction=sum(r['same_prediction'] for r in subset))
             for arm,condition in itertools.product(b.ARMS,b.CONDITIONS)
             for subset in [[p for p in pairs if p['arm']==arm and p['condition']==condition]]])


class Audit:
    @staticmethod
    def sha(p):
        p=Path(p)
        return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'a'*64
    @staticmethod
    def read_json(p): return json.loads(Path(p).read_text(encoding='utf-8'))
    @staticmethod
    def safe_child(root,n): return Path(root)/n

@contextlib.contextmanager
def no_neural():
    with patch.object(torch.nn.Module,'_call_impl',side_effect=AssertionError('no model forward')), \
         patch.object(torch.nn.Module,'load_state_dict',side_effect=AssertionError('no model load')):
        yield


def pinned():
    pins={n:'a'*40 for n in b.OWN}
    pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<784: pins['f/'+str(len(pins))]='a'*40
    return pins,{'input/'+str(i):'a'*64 for i in range(1478)}


def result(summary):
    pins,inputs=pinned()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,status='PASS',commit_sha='f'*40,
                diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,
                artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,
                capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


class C323Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old_threads=torch.get_num_threads();torch.set_num_threads(2)
        cls.data=fixture_data(); cls.pairs=parent_pairs(cls.data)
        cls.parent=parent_summary(cls.pairs)
        cls.details,cls.groups,cls.summary=b.analyze(cls.data,cls.pairs,cls.parent)
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.old_threads)
    def test_01_manifest_self_hash(self):
        b.validate_seal(); self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
    def test_02_manifest_modification_fails(self):
        with patch.object(b,'MANIFEST_SHA','f'*64),self.assertRaises(ValueError):b.validate_seal()
    def test_03_canonical_data_count(self):
        ids=b.logical_index(self.data);self.assertEqual((len(ids['TRAIN']),len(ids['HOLDOUT'])),(192,96))
    def test_04_duplicate_source_rejected(self):
        d=copy.deepcopy(self.data);d['TRAIN'].append(d['TRAIN'][0]);
        with self.assertRaisesRegex(ValueError,'duplicate'):b.logical_index(d)
    def test_05_source_target_and_permutation_rejected(self):
        for field,value in [('target',70),('permutation',[0,0]),('values',[0,0])]:
            d=copy.deepcopy(self.data);d['TRAIN'][0][field]=value
            with self.assertRaises(ValueError):b.logical_index(d)
    def test_06_position_classification_independent(self):
        ids=b.logical_index(self.data)
        sample=next(z for z in self.pairs if z['condition']=='interior' and z['arm']=='mean_last')
        key=b.classify_pair(sample,ids);x=key[-1]
        self.assertTrue(x['both_first']);self.assertFalse(x['both_last']);self.assertEqual(x['correct'],1)
    def test_07_both_permutations_first_tracking(self):
        group=next(z for z in self.details if z['condition']=='interior' and z['arm']=='mean_last')
        self.assertTrue(group['first_fact_both_orders']);self.assertFalse(group['last_fact_both_orders'])
        self.assertEqual((group['correct'],group['first_fact_answers'],group['same_query_across_orders']),(2,4,0))
    def test_08_last_tracking(self):
        group=next(z for z in self.details if z['condition']=='interior' and z['arm']=='last_only' and z['profile']=='balanced')
        self.assertTrue(group['last_fact_both_orders']);self.assertFalse(group['first_fact_both_orders'])
    def test_09_query_correct_control(self):
        group=next(z for z in self.details if z['condition']=='old4')
        self.assertTrue(group['four_correct']);self.assertFalse(group['first_fact_both_orders']);self.assertEqual(group['correct'],4)
        self.assertEqual(group['same_query_across_orders'],2)
    def test_10_value_lock_is_distinct(self):
        key=(319001,'mean_last','interior','TRAIN','u_dominant','en',(0,1),(0,1))
        f=dict(prediction_A=48,prediction_B=48,first_value=48,last_value=49,both_first=True,both_last=False,both_correct=False,collapsed=True,correct=1,first_answers=2,last_answers=0,other_answers=0)
        g=dict(f,first_value=49,last_value=48,both_first=False,both_last=True,first_answers=0,last_answers=2)
        r=b.order_quad(f,g,key)
        self.assertTrue(r['same_value_all_four']);self.assertFalse(r['first_fact_both_orders']);self.assertFalse(r['last_fact_both_orders'])
        self.assertEqual(r['same_query_across_orders'],2)
    def test_11_full_inventory_conservation(self):
        self.assertEqual((len(self.pairs),len(self.details),len(self.groups),len(self.summary['reconciliations'])),(8640,4320,240,4))
        self.assertEqual(sum(r['answers'] for r in self.groups),17280)
        self.assertEqual(sum(r['query_pairs'] for r in self.groups),8640)
        b.validate_result(result(self.summary))
    def test_12_parent_reconciliation_detects_changes(self):
        s=copy.deepcopy(self.parent);s['overall'][0]['same_prediction']+=1
        with self.assertRaisesRegex(ValueError,'C322 aggregate'):b.analyze(self.data,self.pairs,s)
    def test_13_missing_or_duplicate_order_rejected(self):
        with self.assertRaisesRegex(ValueError,'query-pair count'):b.analyze(self.data,self.pairs[:-1],self.parent)
        pair=copy.deepcopy(self.pairs);pair[1]=pair[0]
        with self.assertRaises(ValueError):b.analyze(self.data,pair,self.parent)
    def test_14_pair_profile_target_tamper(self):
        ids=b.logical_index(self.data);p=copy.deepcopy(self.pairs[0])
        for field,value in [('source_profile','mismatch'),('target_A',70),('same_prediction',True)]:
            q=dict(p);q[field]=value if field!='same_prediction' else not p['same_prediction']
            with self.assertRaises(ValueError):b.classify_pair(q,ids)
    def test_15_scope_and_work_contract(self):
        for f in (lambda p:p.update(capability_gate_applicable=True),lambda p:p['validation_summary'].update(model_forward_calls=False),lambda p:p['validation_summary'].update(diagnostic_complete=False)):
            p=result(copy.deepcopy(self.summary));f(p)
            with self.assertRaises(ValueError):b.validate_result(p)
    def test_16_utf8_and_runner_contract(self):
        root=Path(__file__).resolve().parents[1]
        for n in b.OWN:self.assertTrue((root/n).read_text(encoding='utf-8'))
        launch=(root/b.OWN[3]).read_text(encoding='utf-8'); runner=(root/b.OWN[2]).read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'runs\\c(\d{3})-.*?\\summary.json',launch),[str(n) for n in range(322,273,-1)])
        self.assertEqual(len(re.findall(r"@'\n(.*?)\n'@",runner,re.S)),3)
        for code in re.findall(r"@'\n(.*?)\n'@",runner,re.S):compile(code,'runner','exec')
        self.assertIn('sys.argv[2:51]',runner);self.assertIn('head = sys.argv[51]',runner)
        self.assertLess(launch.index('-Mode Validate'),launch.index('-Mode Execute'))

    @contextlib.contextmanager
    def synthetic_parent(self):
        paths=[(Path('/c323-fixture')/str(i)/'summary.json').resolve() for i in range(49)]
        sha=[b.PARENT_SHA,'2'*64,'3'*64]+[str(i%10)*64 for i in range(46)]
        hashes=dict(zip(map(str,paths),sha,strict=True))
        evidence=dict(commit_sha=b.PARENT_EXECUTION,experiment_id='C322-v5b-saved-query-contrast',status='PASS',
                      capability_gate_applicable=False,source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
                      artifacts=[dict(file=n) for n in b.OUTPUTS],
                      validation_summary=dict(diagnostic_complete=True,overall=self.parent['overall']))
        p=NS(PARENT_SHA='2'*64,OUTPUTS=b.OUTPUTS,verify_artifacts=Mock(return_value=(evidence,[])),
             validate_result=Mock(),load_parent=Mock(return_value=({},self.data,[])))
        parent=NS(PARENT_SHA='3'*64);model=NS(parent_hashes=lambda owner:tuple(sha[3:]));owner=NS()
        x=NS(guarded=NS(no_neural=contextlib.nullcontext),c=NS(audit=NS(
            sha=lambda path:hashes[str(path)],read_json=lambda path:self.pairs)))
        with patch.object(b,'context',return_value=(p,parent,model,owner,x)):
            yield paths,hashes,p,evidence

    def test_17_all49_parent_hashes_before_dispatch(self):
        with self.synthetic_parent() as (paths,hashes,p,evidence):
            self.assertEqual(b.load_parent(paths)[0],evidence)
            p.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                saved=hashes[str(path)];hashes[str(path)]='f'*64;p.verify_artifacts.reset_mock()
                with self.assertRaisesRegex(ValueError,'49 parent hashes'):b.load_parent(paths)
                p.verify_artifacts.assert_not_called();hashes[str(path)]=saved

    def test_18_parent_status_protection_and_artifact_inventory(self):
        for mutate in (lambda e:e.update(status='FAIL'),lambda e:e.update(capability_gate_applicable=True),
                       lambda e:e['artifacts'].pop(),lambda e:e['validation_summary'].update(diagnostic_complete=False),
                       lambda e:e['source_blobs'].update({b.PARENT_SOURCE:'0'*40})):
            with self.synthetic_parent() as (paths,_,p,e):
                mutate(e)
                with self.assertRaises(ValueError):b.load_parent(paths)

    def test_19_source_protection_real_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);pins={b.PARENT_SOURCE:b.PARENT_BLOB}
            while len(pins)<778:pins['accepted/'+str(len(pins))]='a'*40
            for name in [*pins,*b.OWN]:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(name,encoding='utf-8')
            protected={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1467-len(protected)):
                path=root/('input'+str(i));path.write_text('value',encoding='utf-8');protected[str(path.resolve())]=Audit.sha(path)
            directory=root/'parent';directory.mkdir();summary=directory/'summary.json';summary.write_text('summary',encoding='utf-8')
            artifacts=[]
            for name in b.OUTPUTS:
                path=directory/name;path.write_text('data',encoding='utf-8');artifacts.append(dict(file=name,sha256=Audit.sha(path)))
            def sha(path):return b.PARENT_SHA if Path(path).resolve()==summary.resolve() else Audit.sha(path)
            p=types.ModuleType('p');p.__file__=str(root/b.PARENT_SOURCE)
            x=NS(parent=NS(context=lambda:()),p312=NS(context=lambda:()),wide=NS(context=lambda:()),
                 c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,safe_child=Audit.safe_child,
                 git=lambda root,*args:(pins.get(args[1][5:],'b'*40)+'\n').encode(),
                 protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp})))
            loaded=(dict(source_blobs=pins,input_sha256=protected,artifacts=artifacts),None,None)
            with patch.object(b,'context',return_value=(p,NS(),NS(),NS(context=lambda:()),x)), \
                 patch.object(b,'load_parent',return_value=loaded),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*49,root)[:2])),(784,1478))
                x.c.missing=types.ModuleType('missing');x.c.missing.__file__=str(root/'missing.py')
                with self.assertRaisesRegex(ValueError,'unprotected helper'):b.precheck([summary]*49,root)

    @contextlib.contextmanager
    def production_stub(self):
        evidence=dict(validation_summary=self.parent)
        loaded=(evidence,self.data,self.pairs)
        x=NS(guarded=NS(no_neural=no_neural),c=NS(audit=Audit()))
        with patch.object(b,'context',return_value=(None,None,None,NS(),x)), \
             patch.object(b,'guard'),patch.object(b,'precheck',return_value=(*pinned(),loaded)), \
             patch.object(b,'load_parent',return_value=loaded):yield

    def test_20_production_dispatch_and_roundtrip(self):
        with self.production_stub(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'run';r=b.run(summaries=['x']*49,output_dir=out,expected_head='f'*40)
            self.assertEqual({z.name for z in out.iterdir()},set(b.OUTPUTS)|{'summary.json'})
            saved,groups=b.verify_artifacts(out,['x']*49,'f'*40)
            self.assertEqual(saved,r);self.assertEqual(len(groups),240)

    def test_21_tamper_and_resealed_semantic_check(self):
        with self.production_stub(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'run';r=b.run(summaries=['x']*49,output_dir=out,expected_head='f'*40)
            path=out/'measurements.json';path.write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'output bytes'):b.verify_artifacts(out,['x']*49,'f'*40)
            descriptor=next(z for z in r['artifacts'] if z['file']==path.name)
            descriptor.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size)
            (out/'summary.json').write_bytes(b.blob(r))
            with self.assertRaisesRegex(ValueError,'persisted'):b.verify_artifacts(out,['x']*49,'f'*40)
            with self.assertRaises(FileExistsError):b.run(summaries=['x']*49,output_dir=out,expected_head='f'*40)

    def test_22_no_neural_optimizer_or_tensor_archive(self):
        with self.production_stub(),tempfile.TemporaryDirectory() as tmp,patch.object(torch,'save',side_effect=AssertionError('tensor checkpoint')), \
             patch.object(torch.optim,'AdamW',side_effect=AssertionError('optimizer')),contextlib.redirect_stdout(io.StringIO()):
            b.run(summaries=['x']*49,output_dir=Path(tmp)/'run',expected_head='f'*40)

    def test_23_cli_registration_and_context_schema(self):
        argv=['program','--summaries']+['x']*49+['--output-dir','out','--expected-head','f'*40]
        with patch.object(sys,'argv',argv),patch.object(b,'run') as fn:
            b.main();self.assertEqual(len(fn.call_args.kwargs['summaries']),49)
        self.assertEqual(len(b.OWN),6);self.assertEqual(b.manifest()['parents'],49)

    def test_24_semantic_regression_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def runTest(self):pass
            def id(self):return self.name
        ids=['f.'+str(i) for i in range(5293)]+[b.EXCLUDED]
        with patch.object(b,'regression_modules',return_value=[]), \
             patch.object(unittest.defaultTestLoader,'loadTestsFromNames',return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual([t.id() for t in b.flatten(b.regression_suite(Path.cwd()))],ids[:-1])
        with patch.object(b,'regression_modules',return_value=[]), \
             patch.object(unittest.defaultTestLoader,'loadTestsFromNames',return_value=unittest.TestSuite([Dummy('x'),Dummy('x')])), \
             self.assertRaises(ValueError):b.regression_suite(Path.cwd())


if __name__=='__main__':unittest.main()
