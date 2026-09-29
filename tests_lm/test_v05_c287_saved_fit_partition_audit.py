"""C287 behavioral fixtures; real parent archives remain runtime gates."""
import ast
import contextlib
import copy
import hashlib
import io
import itertools
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock,patch
import torch
from fold_lm.v05_benchmarks import model_c287_saved_fit_partition_audit as b


def sync(metrics):
    for m in metrics:
        for task in b.PROFILES:
            tm=m[task]
            for r in tm['cells']:r['passed']=all(r[k]>=v for k,v in b.THRESHOLDS.items() if k!='two_order_accuracy')
            for r in tm['two_order']:r['passed']=r['accuracy']>=.8
            tm['passed']=all(r['passed'] for r in tm['cells']+tm['two_order'])
    return metrics


def fail(cell):
    n=cell['rows'];cell.update(correct=n-2,accuracy=(n-2)/n,query_pair_accuracy=(n-2)/n)


def fixtures(accepted=True):
    metrics=[];fits=[]
    for state in b.expected_results():
        m=dict(seed=state['seed'],arm=state['arm'])
        for task,profiles in b.PROFILES.items():
            cells=[];orders=[]
            for split,profile,lang,e in itertools.product(('TRAIN','HOLDOUT'),profiles,('en','ja'),((0,1),(0,2),(1,2))):
                n=16 if split=='TRAIN' else 8
                common=dict(split=split,profile=profile,language=lang,entities=list(e),accuracy=1.)
                for perm in (e,e[::-1]):
                    cells.append(dict(**common,permutation=list(perm),rows=n,correct=n,pairs=n//2,collapsed_pairs=0,
                                      query_pair_accuracy=1.,evidence_drop=.5,query_drop=.5,answer_nll=.02))
                orders.append(dict(**common,groups=n,both_correct=n))
            if accepted and not state[task+'_pass']:fail(cells[0])
            m[task]=dict(cells=cells,two_order=orders)
        metrics.append(m)
        losses=[1.]*400+([.2]*400 if state['arm']==b.ARMS[0] else [.1]*400)
        fits.append(dict(seed=m['seed'],arm=m['arm'],fit=dict(steps=800,last_ce=losses[-1],loss_history=losses,step400_sha256='a'*64)))
    return sync(metrics),fits


def first_cell(metrics,task='two_char',split='TRAIN'):
    return next(r for r in metrics[0][task]['cells'] if r['split']==split)


def parent_fixture():
    return dict(commit_sha=b.PARENT_EXECUTION,status='FAIL',source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
                artifacts=[dict(file=n,sha256=v[0],serialized_bytes=v[1]) for n,v in b.PARENT_ARTIFACTS.items()],
                validation_summary=dict(candidate_gate=False,seed_results=b.expected_results(),all_replays=True,
                                        all_pairs_matched=True,all_prefixes_matched=True))


def protection():
    pins={n:'b'*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<568:pins['fixture/'+str(len(pins))]='b'*40
    return pins,{'fixture/input/'+str(i):'a'*64 for i in range(1016)}


class Audit:
    @staticmethod
    def sha(path):
        p=Path(path);return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'a'*64
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding='utf-8'))
    @staticmethod
    def safe_child(root,name):return Path(root)/name
    @staticmethod
    def git(root,*args):
        if args[0]=='rev-parse':return b'ffffffffffffffffffffffffffffffffffffffff\n'
        if args[0]=='branch':return b'feat/sft-target-loss\n'
        return b''


def result_fixture():
    _,s=b.analyze(*fixtures());pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha='f'*40,status='PASS',diagnostic_execution_valid=True,
                source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,
                capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


class C287Tests(unittest.TestCase):
    def test_01_real_seal(self):
        b.validate_seal();self.assertEqual(b.MANIFEST_SHA,b.digest(b.manifest()))

    def test_02_bad_seals(self):
        for seal in ('UNSEALED','F'*64,'0'*64):
            with patch.object(b,'MANIFEST_SHA',seal),self.assertRaises(ValueError):b.validate_seal()

    def test_03_grid_and_flags(self):
        r,s=b.analyze(*fixtures());self.assertEqual(len(r['records']),3240)
        self.assertEqual(s['parent_results'],b.expected_results());self.assertEqual(len(s['split_partitions']),60)

    def test_04_duplicate_and_missing_grid(self):
        for mutate in (lambda m:m[0]['quad']['cells'].append(copy.deepcopy(m[0]['quad']['cells'][0])),lambda m:m[0]['quad']['two_order'].pop()):
            m,f=fixtures();mutate(m)
            with self.assertRaisesRegex(ValueError,'unique grid'):b.analyze(m,f)

    def test_05_cell_order_invariance(self):
        m,f=fixtures();expected=b.analyze(m,f)
        for model in m:
            for task in b.PROFILES:model[task]['cells'].reverse();model[task]['two_order'].reverse()
        self.assertEqual(b.analyze(m,f),expected)

    def test_06_nonfinite_nll_and_boolean_metrics(self):
        for key,value in (('answer_nll',float('nan')),('accuracy',True),('answer_nll',-.1)):
            m,f=fixtures();first_cell(m)[key]=value
            with self.assertRaises(ValueError):b.analyze(m,f)

    def test_07_counts_and_ratios(self):
        for key,value in (('correct',15),('pairs',True),('query_pair_accuracy',.31),('collapsed_pairs',1),('evidence_drop',.31)):
            m,f=fixtures(False);first_cell(m)[key]=value;sync(m)
            with self.assertRaises(ValueError):b.analyze(m,f)

    def test_08_flags_and_unknown_keys(self):
        for key,value in (('passed',False),('profile','unknown'),('entities',[0,3])):
            m,f=fixtures(False);first_cell(m)[key]=value
            with self.assertRaises(ValueError):b.analyze(m,f)
        m,f=fixtures(False);m[0]['two_char']['passed']=False
        with self.assertRaisesRegex(ValueError,'task pass'):b.analyze(m,f)

    def test_09_fitted_train_partition(self):
        m,f=fixtures(False);fail(first_cell(m));_,s=b.analyze(sync(m),f)
        self.assertEqual(s['model_partitions'][0]['first_direct_failure_partition'],'fitted_train')

    def test_10_seen_holdout_is_not_training_underfit(self):
        m,f=fixtures(False);fail(first_cell(m,split='HOLDOUT'));_,s=b.analyze(sync(m),f)
        p=s['model_partitions'][0];self.assertTrue(p['fitted_train_direct_pass'])
        self.assertEqual(p['first_direct_failure_partition'],'seen_length_holdout')

    def test_11_quad_train_is_untrained_length(self):
        m,f=fixtures(False);fail(first_cell(m,task='quad'));_,s=b.analyze(sync(m),f)
        self.assertEqual(s['model_partitions'][0]['first_direct_failure_partition'],'quad')
        self.assertTrue(s['model_partitions'][0]['fitted_train_direct_pass'])

    def test_12_mask_failure_separate(self):
        m,f=fixtures(False);first_cell(m)['evidence_drop']=0.;_,s=b.analyze(sync(m),f)
        row=s['split_partitions'][0];self.assertTrue(row['direct_pass']);self.assertFalse(row['full_pass'])
        self.assertEqual(row['mask_only_cells'],1);self.assertEqual(s['model_partitions'][0]['first_direct_failure_partition'],'none')

    def test_13_two_order_is_direct_failure(self):
        m,f=fixtures(False);r=m[0]['triple']['two_order'][0];r.update(accuracy=.5,both_correct=8)
        _,s=b.analyze(sync(m),f);self.assertEqual(s['model_partitions'][0]['first_direct_failure_partition'],'fitted_train')

    def test_14_final_nll_is_weighted_not_last_batch(self):
        m,f=fixtures(False);first_cell(m)['answer_nll']=.74;_,s=b.analyze(m,f)
        train=s['split_partitions'][0];self.assertAlmostEqual(train['final_normal_nll'],(.74+35*.02)/36)
        self.assertEqual(train['rows'],576);self.assertEqual(s['split_partitions'][1]['rows'],288)
        self.assertNotEqual(train['final_normal_nll'],f[0]['fit']['last_ce'])

    def test_15_loss_inventory(self):
        bins,paired=b.loss_bins(fixtures()[1]);self.assertEqual((len(bins),len(paired)),(180,90))
        for seed,arm in b.identities():
            self.assertEqual(sum(r['updates'] for r in bins if (r['seed'],r['arm'])==(seed,arm)),800)

    def test_16_loss_window_and_length_profile_indexing(self):
        _,f=fixtures()
        for r in f:r['fit'].update(loss_history=[float(i+1) for i in range(800)],last_ce=800.)
        bins,_=b.loss_bins(f)
        for row in bins:
            steps=[s for s in range(row['first_update'],row['last_update']+1) if ((s-1)//4)%2==row['length']-2 and ((s-1)//4)%3==row['profile_index']]
            self.assertEqual(row['updates'],len(steps));self.assertEqual(row['mean_ce'],sum(steps)/len(steps))

    def test_17_paired_loss_direction(self):
        _,pairs=b.loss_bins(fixtures()[1])
        for row in pairs:self.assertAlmostEqual(row['candidate_minus_control_mean_ce'],0. if row['first_update']==1 else -.1)

    def test_18_bad_loss_traces(self):
        for mutate in (lambda f:f[0]['fit']['loss_history'].pop(),lambda f:f[0]['fit']['loss_history'].__setitem__(0,float('nan')),
                       lambda f:f[0]['fit'].update(last_ce=2.),lambda f:f[0]['fit'].update(steps=True)):
            _,f=fixtures();mutate(f)
            with self.assertRaises(ValueError):b.loss_bins(f)

    def test_19_prefix_mismatch(self):
        for mutate in (lambda f:f[1]['fit']['loss_history'].__setitem__(399,.9),lambda f:f[1]['fit'].update(step400_sha256='b'*64)):
            _,f=fixtures();mutate(f)
            with self.assertRaisesRegex(ValueError,'common first400'):b.loss_bins(f)

    def test_20_all_models_required(self):
        m,f=fixtures();f.reverse()
        with self.assertRaises(ValueError):b.analyze(m,f)
        m,f=fixtures();m.pop()
        with self.assertRaises(ValueError):b.analyze(m,f)

    def test_21_exact_parent_identity(self):
        b.validate_parent(parent_fixture())
        for mutate in (lambda p:p.update(status='PASS'),lambda p:p['source_blobs'].clear(),
                       lambda p:p['artifacts'][0].update(serialized_bytes=0),lambda p:p['validation_summary'].update(all_prefixes_matched=False)):
            p=parent_fixture();mutate(p)
            with self.assertRaises(ValueError):b.validate_parent(p)

    def test_22_parent_loader_dispatch_and_all_hashes(self):
        paths=[Path('/c287-fixture')/str(i)/'summary.json' for i in range(13)]
        paths=[p.resolve() for p in paths];mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True));m,f=fixtures()
        parent=NS(verify_artifacts=Mock(return_value=(parent_fixture(),m)),validate_result=Mock())
        c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        with patch.object(b,'context',return_value=(parent,c)),patch.object(torch,'load',return_value=dict(schema='fold-c286-cosine-tail-eval-v1',records=f)) as load:
            got=b.load_parent(paths);self.assertEqual(got[1:],(m,f));load.assert_called_once()
            parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]='0'*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_23_forbidden_operations_and_restore(self):
        for action in (lambda:torch.nn.Identity()(torch.ones(1)),lambda:torch.nn.Linear(1,1).load_state_dict({}),lambda:torch.save({},'FORBIDDEN.pt')):
            with b.no_neural(),self.assertRaisesRegex(RuntimeError,'C287 forbids'):action()
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_24_scope_and_workload(self):
        p=result_fixture();b.validate_result(p)
        for k in b.ZERO_KEYS:
            q=copy.deepcopy(p);q['validation_summary'][k]=False
            with self.assertRaises(ValueError):b.validate_result(q)
        p['gate_f_candidate']=True
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_25_result_inventory_and_parent_flags(self):
        for mutate in (lambda p:p['validation_summary']['split_partitions'].pop(),lambda p:p['validation_summary']['loss_bins'].pop(),
                       lambda p:p['validation_summary']['parent_results'][0].update(quad_pass=False)):
            p=result_fixture();mutate(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    def test_26_run_roundtrip_and_no_overwrite(self):
        m,f=fixtures();events=[]
        def pc(*a):events.append('precheck');return protection()
        def lp(*a):events.append('parent');return parent_fixture(),m,f
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,'context',return_value=(None,NS(audit=Audit()))),\
             patch.object(b,'precheck',side_effect=pc),patch.object(b,'load_parent',side_effect=lp),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'audit';p=b.run(summaries=['x']*13,output_dir=out,expected_head='f'*40)
            self.assertEqual(events,['precheck','parent','precheck'])
            q,_=b.verify_artifacts(out,['x']*13,'f'*40);self.assertEqual(q,p)
            with self.assertRaises(FileExistsError):b.run(summaries=['x']*13,output_dir=out,expected_head='f'*40)

    def test_27_hash_and_semantic_tamper(self):
        m,f=fixtures()
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,'context',return_value=(None,NS(audit=Audit()))),\
             patch.object(b,'precheck',return_value=protection()),patch.object(b,'load_parent',return_value=(parent_fixture(),m,f)),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'audit';p=b.run(summaries=['x']*13,output_dir=out,expected_head='f'*40)
            path=out/'fit-partition-report.json';path.write_text('{}')
            with self.assertRaisesRegex(ValueError,'output bytes'):b.verify_artifacts(out,['x']*13,'f'*40)
            item=next(a for a in p['artifacts'] if a['file']==path.name);item.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size)
            (out/'summary.json').write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,'persisted'):b.verify_artifacts(out,['x']*13,'f'*40)

    def test_28_suite_real_construction(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=['fixture.'+str(i) for i in range(b.manifest()['loaded_tests']-1)]+[b.EXCLUDED]
        with patch.object(b,'regression_modules',return_value=[]),patch.object(unittest.defaultTestLoader,'loadTestsFromNames',return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),b.manifest()['focused_tests'])
            self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})

    def test_29_cli_order(self):
        argv=['prog','--summaries']+[str(i) for i in range(13)]+['--output-dir','out','--expected-head','f'*40]
        with patch.object(sys,'argv',argv),patch.object(b,'run') as run:
            b.main();self.assertEqual(run.call_args.kwargs['summaries'],[Path(str(i)) for i in range(13)])

    def test_30_runner_blocks_and_paths(self):
        root=Path(__file__).resolve().parents[1];r=(root/'tools/run_c287.ps1').read_text();l=(root/'tools/invoke_c287.ps1').read_text()
        blocks=re.findall(r"@'\n(.*?)\n'@",r,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn('sys.argv[2:15]',blocks[2]);self.assertIn('head = sys.argv[15]',blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',l)),13)
        self.assertLess(l.index('-Mode Validate'),l.index('-Mode Execute'))
        self.assertLess(l.index('AUTHORING_RUNTIME_PREFLIGHT_FAILED'),l.index('publish_experiment_log.ps1'))
        self.assertIn('Parser]::ParseFile',l)

    def test_31_immutable_inventory_and_binding(self):
        root=Path(__file__).resolve().parents[1];self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text())
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()['own_tests'])
        for n in b.OWN:self.assertTrue((root/n).is_file())
        tree=ast.parse(Path(b.__file__).read_text());imports=[n for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and (n.module or '').startswith('fold_lm')]
        self.assertEqual([n.names[0].name for n in imports],['model_c286_cosine_tail_stability'])
        self.assertEqual(b.manifest()['source_pins'],562+len(b.OWN));self.assertEqual(b.manifest()['protected_inputs'],1001+9+len(b.OWN))

    def test_32_context_dispatch_and_guard(self):
        import types
        package=types.ModuleType('fold_lm.v05_benchmarks');c=NS(audit=Audit());parent=NS(context=lambda:(0,1,2,3,c))
        package.model_c286_cosine_tail_stability=parent
        with patch.dict(sys.modules,{'fold_lm.v05_benchmarks':package}):self.assertEqual(b.context(),(parent,c))
        with patch.object(b,'context',return_value=(parent,c)):
            b.guard(Path.cwd(),'f'*40)
            with self.assertRaises(ValueError):b.guard(Path.cwd(),'e'*40)


if __name__=='__main__':unittest.main()
