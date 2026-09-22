import hashlib
import inspect
import io
import math
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c232_bilingual_learning as b


class Toy(nn.Module):
    """Synthetic instrument only, deliberately not a V5-B replacement."""
    def __init__(self, seed=0):
        super().__init__()
        self.scores=nn.Parameter(torch.zeros(256,dtype=torch.float64))
        self.unused=nn.Parameter(torch.zeros(13232,dtype=torch.float64))
    def forward(self, tokens, tasks):
        return self.scores[None,:].expand(len(tokens),-1)


def prefix_rows(raw):
    x=torch.tensor([[257,*raw[:i],258,*([256]*(46-i))] for i in range(len(raw))])
    return x,torch.tensor(list(raw),dtype=torch.int64)


def fake_parent():
    def fingerprint(model):
        return hashlib.sha256(b''.join(x.detach().numpy().tobytes() for x in model.parameters())).hexdigest()
    def predict(model,x):
        with torch.no_grad():return model(x,torch.zeros(len(x),dtype=torch.int64))
    return SimpleNamespace(document_rows=prefix_rows,new_model=Toy,fingerprint=fingerprint,
                           predict=predict,generate=lambda model,prefix:b'test')


def good_record(seed):
    def scores(value):return {key:dict(bits_per_byte=value) for key in ('all','en','ja')}
    return dict(seed=seed,weights_changed=True,checkpoint_roundtrip=True,reload_max_error=0.,
        generation_replayed=True,initial_train=scores(8.),initial_eval=scores(8.),
        final_train=scores(3.),final_eval=scores(4.),unigram_eval=scores(6.),
        fit=dict(steps=400,byte_presentations=12800))


class C232Tests(unittest.TestCase):
    def test_01_manifest_and_dataset_hashes(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(b.dataset()),b.DATA_SHA)

    def test_02_document_split_counts(self):
        train,ev=b.validate_dataset(b.dataset())
        self.assertEqual((len(train),len(ev)),(48,16))
        self.assertEqual(len({r['id'] for r in b.dataset()}),64)

    def test_03_semantic_pairs_do_not_cross_splits(self):
        train,ev=b.validate_dataset(b.dataset())
        a={tuple(r['pair']) for r in train};z={tuple(r['pair']) for r in ev}
        self.assertFalse(a&z);self.assertEqual((len(a),len(z)),(12,4))

    def test_04_pair_holds_all_languages_and_templates_together(self):
        for i in range(4):
            for j in range(4):
                rows=[r for r in b.dataset() if r['pair']==[i,j]]
                self.assertEqual(len(rows),4)
                self.assertEqual(len({r['split'] for r in rows}),1)

    def test_05_all_words_seen_in_train(self):
        train,_=b.validate_dataset(b.dataset())
        for language in b.LANGUAGES:
            text=''.join(r['text'] for r in train if r['language']==language)
            self.assertTrue(all(w in text for w in b.NOUNS[language]+b.COLORS[language]))

    def test_06_byte_counts_and_slots(self):
        train,ev=b.validate_dataset(b.dataset())
        self.assertEqual([sum(len(r['text'].encode()) for r in rows) for rows in (train,ev)],[948,316])
        self.assertLessEqual(max(len(r['text'].encode()) for r in b.dataset()),47)

    def test_07_dataset_edits_rejected(self):
        rows=b.dataset();rows[0]['split']='TRAIN'
        with self.assertRaises(ValueError):b.validate_dataset(rows)

    def test_08_unigram_rejects_eval(self):
        with self.assertRaises(ValueError):b.unigram_tables(b.dataset())

    def test_09_unigram_normalized_and_smoothed(self):
        train,_=b.validate_dataset(b.dataset());p=b.unigram_tables(train).exp()
        torch.testing.assert_close(p.sum(1),torch.ones(2,dtype=torch.float64))
        self.assertTrue(bool((p>0).all()))

    def test_10_unigram_counts_are_language_specific(self):
        train,_=b.validate_dataset(b.dataset());p=b.unigram_tables(train).exp()
        for i,lang in enumerate(b.LANGUAGES):
            raw=b''.join(r['text'].encode() for r in train if r['language']==lang)
            self.assertAlmostEqual(float(p[i,10]),(raw.count(10)+1)/(len(raw)+256))

    def test_11_unigram_independent_of_eval_changes(self):
        train,ev=b.validate_dataset(b.dataset());old=b.unigram_tables(train)
        ev[0]['text']='different test data'
        torch.testing.assert_close(old,b.unigram_tables(train),rtol=0,atol=0)

    def test_12_tensor_rows_use_parent_prefix_adapter(self):
        with patch.object(b,'parent_module',return_value=fake_parent()):
            row=dict(text='箱\n',language='ja');x,y,g=b.tensor_rows([row])
        self.assertEqual(x.shape,(4,48));self.assertEqual(y.tolist(),list('箱\n'.encode()))
        self.assertEqual(x[0,:2].tolist(),[257,258]);self.assertEqual(g.tolist(),[1]*4)

    def test_13_empty_tensor_rows_rejected(self):
        with patch.object(b,'parent_module',return_value=fake_parent()):
            with self.assertRaises(ValueError):b.tensor_rows([])

    def test_14_scores_weight_bytes_not_documents(self):
        scores=b.metrics_from_nll(torch.tensor([1.,1.,4.],dtype=torch.float64),torch.tensor([0,0,1]))
        self.assertAlmostEqual(scores['all']['bits_per_byte'],2/math.log(2))
        self.assertEqual(scores['en']['bytes'],2)

    def test_15_empty_language_is_invalid(self):
        with self.assertRaises(ValueError):b.metrics_from_nll(torch.ones(2),torch.zeros(2,dtype=torch.int64))

    def test_16_nonfinite_scores_invalid(self):
        with self.assertRaises(ValueError):b.metrics_from_nll(torch.tensor([1.,float('nan')]),torch.tensor([0,1]))

    def test_17_uniform_reference_eight_bits(self):
        reference=torch.full((2,256),-math.log(256),dtype=torch.float64)
        out=b.reference_score(reference,(None,torch.tensor([1,2]),torch.tensor([0,1])))
        self.assertAlmostEqual(out['all']['bits_per_byte'],8)

    def test_18_evaluator_restores_training_state(self):
        model=Toy().train()
        with patch.object(b,'parent_module',return_value=fake_parent()):
            scores,_=b.evaluate(model,(torch.zeros((2,48),dtype=torch.int64),torch.tensor([0,1]),torch.tensor([0,1])))
        self.assertTrue(model.training);self.assertAlmostEqual(scores['all']['bits_per_byte'],8)

    def test_19_trainer_has_no_eval_inputs(self):
        self.assertEqual(tuple(inspect.signature(b.fit).parameters),('model','train_tokens','train_targets','seed','steps'))
        source=inspect.getsource(b.fit)
        self.assertNotIn('final_eval',source);self.assertNotIn('early_stop',source)

    def test_20_real_optimizer_changes_synthetic_weights(self):
        model=Toy();x=torch.zeros((4,48),dtype=torch.int64);y=torch.zeros(4,dtype=torch.int64)
        result=b.fit(model,x,y,232001,steps=2)
        self.assertEqual(result['byte_presentations'],64)
        self.assertGreater(float(model.scores.detach()[0]),0)

    def test_21_two_step_training_deterministic(self):
        x=torch.zeros((4,48),dtype=torch.int64);y=torch.tensor([0,1,2,3])
        a,z=Toy(),Toy();b.fit(a,x,y,123,steps=2);b.fit(z,x,y,123,steps=2)
        torch.testing.assert_close(a.scores,z.scores,rtol=0,atol=0)

    def test_22_gate_accepts_complete_relative_improvement(self):
        self.assertTrue(b.gate(b.summary_for([good_record(s) for s in b.SEEDS])))

    def test_23_no_improvement_is_valid_negative(self):
        row=good_record(b.SEEDS[0]);row['final_eval']['ja']['bits_per_byte']=7.
        self.assertFalse(b.learning_pass(row))

    def test_24_tie_does_not_pass(self):
        row=good_record(b.SEEDS[0]);row['final_eval']['en']['bits_per_byte']=6.
        self.assertFalse(b.learning_pass(row))

    def test_25_wrong_replay_does_not_pass(self):
        row=good_record(b.SEEDS[0]);row['reload_max_error']=1e-4
        self.assertFalse(b.learning_pass(row))

    def test_26_training_budget_is_fixed(self):
        m=b.manifest();self.assertEqual((m['steps_per_seed'],m['batch_size'],m['total_steps']),(400,32,1200))
        self.assertEqual(m['total_training_byte_presentations'],38400)
        self.assertEqual(m['validation_selection'],'none; final step400 only; no early stopping or checkpoint selection')

    def test_27_runner_cli_order_and_parser_guard(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/'tools/run_c232.ps1').read_text();launch=(root/'tools/invoke_c232.ps1').read_text()
        self.assertIn('expected_focused_tests = 2721',run)
        self.assertLess(run.index('authoring_selftest = PASS'),run.index('& $Python -u -c $Regression'))
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,'embedded','exec')
        self.assertIn('c231-v5b-byte-eval-9e4c4cd1513a4b3c97e598252f6300c5',launch)
        self.assertLess(launch.index('::ParseFile'),launch.index('$failure = $null'))

    def test_28_source_binding_and_parent_decoder_identity(self):
        self.assertIn('parent.new_model(seed)',inspect.getsource(b.run))
        self.assertIn('parent.document_rows(',inspect.getsource(b.tensor_rows))
        self.assertNotIn('new_model',inspect.getsource(b.fit))

    def test_29_real_output_validator_preserves_valid_negative(self):
        rows=[good_record(s) for s in b.SEEDS];rows[0]['weights_changed']=False
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
               source_blobs={**{x:'x' for x in b.OWN},**{str(i):'x' for i in range(232)}},
               input_sha256={str(i):'x' for i in range(334)},artifacts=[dict(file=x) for x in b.OUTPUTS],
               validation_summary=b.summary_for(rows),status='FAIL',gate_f_candidate=False,network_calls=0)
        b.validate_result(p)

    def test_30_synthetic_run_calls_train_and_publishes_valid_negative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'input';p.write_bytes(b'x')
            wanted=hashlib.sha256(b'x').hexdigest()
            pins={**{x:'x' for x in b.OWN},**{str(i):'x' for i in range(232)}}
            paths={str(root/f'input{i}'):wanted for i in range(334)}
            for path in paths:Path(path).write_bytes(b'x')
            audit=SimpleNamespace(sha=lambda path:hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                git=lambda root,*args:b'HEAD' if args[0]=='rev-parse' else b'feat/sft-target-loss' if args[0]=='branch' else b'')
            calls=[]
            def simulated_fit(model,x,y,seed):
                calls.append((len(y),seed))
                with torch.no_grad():model.scores[0]+=0.1
                return dict(steps=400,byte_presentations=12800,simulation_only=True)
            with patch.object(b,'audit_module',return_value=audit),patch.object(b,'parent_module',return_value=fake_parent()),patch.object(b,'precheck',return_value=({},pins,paths)),patch.object(b,'fit',side_effect=simulated_fit),patch('sys.stdout',new=io.StringIO()):
                result=b.run(c231_summary=p,output_dir=root/'out',expected_head='HEAD')
            self.assertEqual(calls,[(948,s) for s in b.SEEDS])
            self.assertEqual(result['status'],'FAIL')
            self.assertEqual(len(result['artifacts']),5)

    def test_31_actual_v5b_training_smoke_train_only(self):
        torch.set_num_threads(2)
        parent=b.parent_module();model=parent.new_model(b.SEEDS[0]);before=parent.fingerprint(model)
        train,_=b.validate_dataset(b.dataset());x,y,_=b.tensor_rows(train[:2])
        result=b.fit(model,x,y,b.SEEDS[0],steps=2)
        self.assertEqual(sum(p.numel() for p in model.parameters()),13488)
        self.assertNotEqual(parent.fingerprint(model),before)
        self.assertEqual(result['steps'],2)
        self.assertTrue(all(bool(torch.isfinite(p).all()) for p in model.parameters()))

    def test_32_actual_historical_suite_counts(self):
        root=Path(__file__).resolve().parents[1];names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(117,2722))
        self.assertEqual(b.regression_suite(root).countTestCases(),2721)


if __name__=='__main__':unittest.main(verbosity=2)
