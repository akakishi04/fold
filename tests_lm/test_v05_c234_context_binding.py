import copy
import hashlib
import inspect
import io
import itertools
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c234_context_binding as b


def prefix(raw):
    if len(raw)>46:raise ValueError('too long')
    return torch.tensor([257,*raw,258,*([256]*(46-len(raw)))])


class Source(nn.Module):
    """Synthetic parent interface with real GRU layers, not the actual FOLD core."""
    def __init__(self,seed):
        super().__init__();torch.manual_seed(seed)
        self.byte_embedding=nn.Embedding(259,16,padding_idx=256)
        self.local_encoder=nn.GRU(16,16,batch_first=True)
        self.readout_norm=nn.LayerNorm(16);self.decoder=nn.Linear(16,256)
        self.core=nn.Parameter(torch.zeros(3328));self.double().eval()
    def forward(self,tokens,tasks):
        encoded,_=self.local_encoder(self.byte_embedding(tokens))
        last=(tokens!=256).sum(1)-1
        return self.decoder(self.readout_norm(encoded[torch.arange(len(tokens)),last]))


def baseline(source):
    result=copy.deepcopy(source);del result.core;return result


def fingerprint(model):
    h=hashlib.sha256()
    for name,value in sorted(model.state_dict().items()):
        h.update(name.encode());h.update(value.detach().numpy().tobytes())
    return h.hexdigest()


def good_records():
    rows=[]
    for seed,family in itertools.product(b.SEEDS,b.FAMILIES):
        rows.append(dict(seed=seed,family=family,final_eval={lang:dict(rows=96,accuracy=1.,answer_nll=.1,
            evidence_blind_accuracy=.25,query_blind_accuracy=.5,evidence_drop=.75,query_drop=.5,
            fact_pair_accuracy=1.,query_pair_accuracy=1.) for lang in b.OBJECTS},
            weights_changed=True,checkpoint_roundtrip=True,prediction_replayed=True,reload_max_error=0.,
            fit=dict(steps=400,answer_presentations=12800)))
    return rows


def payload(summary):
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
        source_blobs=dict({x:'fixture' for x in b.OWN},**{str(i):'fixture' for i in range(244)}),
        input_sha256={str(i):'fixture' for i in range(358)},
        artifacts=[dict(file=x) for x in b.OUTPUTS],validation_summary=summary,
        status='PASS' if b.gate(summary) else 'FAIL',gate_f_candidate=False,network_calls=0)


class C234Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.data=b.dataset();cls.train,cls.ev=b.validate_dataset(cls.data)

    def test_01_fixed_hashes(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.data),b.DATA_SHA)

    def test_02_sizes_and_group_disjointness(self):
        self.assertEqual((len(self.data),len(self.train),len(self.ev)),(576,384,192))
        self.assertFalse({x['group'] for x in self.train}&{x['group'] for x in self.ev})

    def test_03_holdout_values_only(self):
        self.assertTrue(all(tuple(sorted(r['values'])) in b.EVAL_PAIRS for r in self.ev))
        self.assertTrue(all(tuple(sorted(r['values'])) not in b.EVAL_PAIRS for r in self.train))

    def test_04_all_nouns_values_seen_in_train(self):
        for noun in range(4):
            seen={r['values'][r['objects'].index(noun)] for r in self.train if noun in r['objects']}
            self.assertEqual(seen,set(range(4)))

    def test_05_all_renderings_group_together(self):
        for group in {r['group'] for r in self.data}:
            rows=[r for r in self.data if r['group']==group]
            self.assertEqual((len(rows),len({r['split'] for r in rows})),(8,1))

    def test_06_english_and_japanese_prompts(self):
        row=dict(language='en',objects=[0,1],values=[0,3],order=0,query=0)
        self.assertEqual(b.render(row),'box=0;book=3;box=')
        row['language']='ja';self.assertEqual(b.render(row),'箱=0;本=3;箱=')

    def test_07_target_is_requested_value(self):
        for row in self.data:
            self.assertEqual(row['target'],48+row['values'][row['objects'].index(row['query'])])

    def test_08_order_does_not_change_target(self):
        by={r['id']:r for r in self.data}
        for row in self.ev:
            changed=by[f"{row['language']}-{row['group']}-{1-row['order']}-{row['query']}"]
            self.assertEqual(row['target'],changed['target']);self.assertNotEqual(row['prompt'],changed['prompt'])

    def test_09_evidence_blind_removes_values(self):
        for row in self.ev:
            text=b.render(row,'evidence_blind')
            self.assertEqual(text.count('=?'),2)
            self.assertFalse(any(str(v) in text for v in range(4)))

    def test_10_query_blind_keeps_facts(self):
        for row in self.ev:
            self.assertEqual(b.render(row,'query_blind').rsplit(';',1)[0],row['prompt'].rsplit(';',1)[0])
            self.assertTrue(b.render(row,'query_blind').endswith(';?='))

    def test_11_dataset_edit_is_rejected(self):
        rows=copy.deepcopy(self.data);rows[0]['target']=49
        with self.assertRaises(ValueError):b.validate_dataset(rows)

    def test_12_baselines_first_last_constant(self):
        for lang in b.OBJECTS:
            rows=[r for r in self.ev if r['language']==lang]
            first=[48+r['values'][r['order']] for r in rows]
            last=[48+r['values'][1-r['order']] for r in rows]
            for pred,want in ((first,.5),(last,.5),([48]*len(rows),.25)):
                self.assertEqual(sum(p==r['target'] for p,r in zip(pred,rows))/len(rows),want)

    def test_13_perfect_fact_and_query_pairs(self):
        pred=[r['target'] for r in self.ev]
        for kind in ('facts','query'):self.assertEqual(b.paired_accuracy(self.ev,pred,kind),1.)

    def test_14_constant_cannot_pass_paired_test(self):
        for kind in ('facts','query'):self.assertEqual(b.paired_accuracy(self.ev,[48]*192,kind),0.)

    def test_15_broken_pairs_rejected(self):
        with self.assertRaises(ValueError):b.paired_accuracy(self.ev[:-1],[48]*191,'facts')
        with self.assertRaises(ValueError):b.paired_accuracy(self.ev,[48]*192,'unknown')

    def test_16_prefix_targets_are_separate(self):
        with patch.object(b,'factory_module',return_value=SimpleNamespace(prefix_tensor=prefix)):
            x,y=b.tensors(self.ev[:2])
        self.assertEqual(tuple(x.shape),(2,48));self.assertEqual(y.tolist(),[r['target'] for r in self.ev[:2]])
        raw=self.ev[0]['prompt'].encode();self.assertEqual(x[0,:len(raw)+2].tolist(),[257,*raw,258])

    def test_17_metrics_use_exact_unconstrained_byte(self):
        rows=self.ev;targets=torch.tensor([r['target'] for r in rows]);logits=torch.zeros((192,256))
        logits[torch.arange(192),targets]=10
        m=b.metrics(rows,targets.tolist(),[0]*192,[255]*192,logits,targets)
        for item in m.values():
            self.assertEqual((item['accuracy'],item['evidence_blind_accuracy'],item['query_blind_accuracy']),(1.,0.,0.))

    def test_18_evaluator_restores_training_and_no_weight_changes(self):
        with patch.object(b,'factory_module',return_value=SimpleNamespace(prefix_tensor=prefix)):
            views=[b.tensors(self.ev,mode) for mode in ('normal','evidence_blind','query_blind')]
        model=Source(1);model.train();before=fingerprint(model);b.evaluate(model,self.ev,views)
        self.assertTrue(model.training);self.assertEqual(fingerprint(model),before)

    def test_19_train_only_signature(self):
        self.assertEqual(tuple(inspect.signature(b.fit).parameters),('model','train_tokens','train_targets','seed','steps'))
        self.assertNotIn('final_eval',inspect.getsource(b.fit))

    def test_20_optimizer_and_paired_samples(self):
        x=torch.stack([prefix(b'A=0;A='),prefix(b'A=1;A=')]);y=torch.tensor([48,49])
        models=[Source(2),Source(2)];seen=[];original=torch.randint
        def capture(*args,**kwargs):
            value=original(*args,**kwargs);seen.append(value.clone());return value
        with patch.object(torch,'randint',side_effect=capture):
            before=fingerprint(models[0])
            for model in models:b.fit(model,x,y,234001,steps=2)
        self.assertNotEqual(fingerprint(models[0]),before);self.assertEqual(fingerprint(models[0]),fingerprint(models[1]))
        self.assertTrue(torch.equal(seen[0],seen[2]));self.assertTrue(torch.equal(seen[1],seen[3]))

    def test_21_primary_and_baseline_gates_independent(self):
        rows=good_records();rows[1]['final_eval']['en']['accuracy']=.5
        s=b.summarize(rows);self.assertTrue(b.gate(s));self.assertFalse(s['gru_binding_gate'])

    def test_22_full_failure_is_valid_negative(self):
        rows=good_records();rows[0]['final_eval']['en']['accuracy']=.5
        s=b.summarize(rows);self.assertFalse(b.gate(s));b.validate_result(payload(s))

    def test_23_paired_or_control_miss_fails_ability(self):
        for field in ('fact_pair_accuracy','query_pair_accuracy','evidence_drop','query_drop'):
            row=good_records()[0];row['final_eval']['ja'][field]=0.
            self.assertFalse(b.binding_pass(row))
        row=good_records()[0];row['final_eval'].pop('en')
        with self.assertRaises(ValueError):b.binding_pass(row)

    def test_24_replay_failure_is_invalid(self):
        rows=good_records();rows[0]['reload_max_error']=1.
        with self.assertRaises(ValueError):b.validate_result(payload(b.summarize(rows)))

    def test_25_workload_and_scope(self):
        m=b.manifest();self.assertEqual((m['total_training_steps'],m['total_answer_presentations']),(2400,76800))
        self.assertFalse(m['learned_memory_used']);self.assertFalse(m['general_language_claim'])

    def test_26_runner_cli_and_ast_preflight_path(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/'tools/run_c234.ps1').read_text();launch=(root/'tools/invoke_c234.ps1').read_text()
        self.assertIn('expected_focused_tests = 2785',run)
        self.assertLess(run.index('authoring_selftest = PASS'),run.index('& $Python -u -c $Regression'))
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,'embedded','exec')
        self.assertIn('c233-v5b-core-ablation-f73f95f4afa44668a64b953f1bbad723',launch)
        self.assertLess(launch.index('::ParseFile'),launch.index('$failure = $null'))

    def test_27_existing_negative_parent_is_not_required_to_pass(self):
        source=inspect.getsource(b.precheck)
        self.assertIn('p["status"]=="FAIL"',source)
        self.assertIn('parent.validate_result(p)',source)
        self.assertIn('deps<=set(pins)',source)

    def test_28_fresh_common_copy_before_either_training(self):
        source=inspect.getsource(b.run)
        self.assertLess(source.index('baseline=parent.new_baseline(full)'),source.index('trained=fit('))
        self.assertNotIn('load_parent_states',source)

    def test_29_serialized_order_and_invalid_view(self):
        rows=good_records();rows.reverse()
        with self.assertRaises(ValueError):b.summarize(rows)
        with self.assertRaises(ValueError):b.render(self.ev[0],'unknown')
        self.assertFalse(re.findall(r'\bc\d{3}\.',inspect.getsource(b)))

    def test_30_full_run_adapter_preserves_valid_negative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'parent.json';path.write_text('{}')
            a=SimpleNamespace(sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest(),
                git=lambda root,*args:b'HEAD' if args[0]=='rev-parse' else b'feat/sft-target-loss' if args[0]=='branch' else b'')
            parent=SimpleNamespace(parent_module=lambda:SimpleNamespace(audit_module=lambda:a),new_baseline=baseline)
            factory=SimpleNamespace(new_model=Source,fingerprint=fingerprint,prefix_tensor=prefix)
            prot={}
            for i in range(358):
                p=root/f'input{i}';p.write_bytes(b'x');prot[str(p)]=a.sha(p)
            pins=payload(b.summarize(good_records()))['source_blobs'];seen=[]
            def simulate(model,x,y,seed,**kwargs):
                self.assertEqual(len(x),384);self.assertEqual(len(y),384);seen.append(seed)
                with torch.no_grad():model.decoder.bias.add_(.001)
                return dict(steps=400,answer_presentations=12800,synthetic=True)
            with patch.object(b,'parent_module',return_value=parent),patch.object(b,'factory_module',return_value=factory),patch.object(b,'precheck',return_value=({},pins,prot)),patch.object(b,'fit',side_effect=simulate),patch('sys.stdout',new=io.StringIO()):
                result=b.run(c233_summary=path,output_dir=root/'out',expected_head='HEAD')
            self.assertEqual(seen,[s for s in b.SEEDS for _ in b.FAMILIES])
            self.assertEqual(result['status'],'FAIL');self.assertTrue(result['validation_summary']['all_replays'])
            self.assertEqual(len(result['artifacts']),5)

    def test_31_actual_parent_train_only_smoke(self):
        factory=b.factory_module();full=factory.new_model(b.SEEDS[0]);gru=b.parent_module().new_baseline(full)
        x,y=b.tensors(self.train[:4])
        for model,count in ((full,13488),(gru,10160)):
            before=factory.fingerprint(model);b.fit(model,x,y,b.SEEDS[0],steps=2)
            self.assertNotEqual(factory.fingerprint(model),before)
            self.assertEqual(sum(v.numel() for v in model.parameters()),count)

    def test_32_actual_historical_suite(self):
        root=Path(__file__).resolve().parents[1];names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(119,2786))
        self.assertEqual(b.regression_suite(root).countTestCases(),2785)


if __name__=='__main__':unittest.main(verbosity=2)
