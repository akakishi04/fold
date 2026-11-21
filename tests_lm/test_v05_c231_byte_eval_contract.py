import ast
import hashlib
import inspect
import io
import json
import math
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c231_byte_eval_contract as b


class Toy(nn.Module):
    """Synthetic prefix-dependent instrument; not the language model under test."""
    def __init__(self, seed=0):
        super().__init__()
        self.offset=nn.Parameter(torch.tensor(float(seed % 5),dtype=torch.float64))
    def forward(self, tokens, tasks):
        index=(tokens.sum(-1)%256).double()+self.offset
        return -(torch.arange(256,dtype=torch.float64)[None,:]-index[:,None]).square()/100


class C231Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_fixture_counts(self):
        self.assertEqual([len(x.encode()) for x in b.TEXTS],[16,22,16,28])
        self.assertEqual(b.digest(list(b.TEXTS)), '5dcdbd8223c0e40df8d9e3fb5c98e50873a0a014ce9a3c2e003fe74d3911ce23')

    def test_03_prefix_is_observed_bytes_only(self):
        tokens,y=b.document_rows(b'ABC')
        self.assertEqual(tokens[0,:3].tolist(),[b.BOS,b.EOS,b.PAD])
        self.assertEqual(tokens[2,:5].tolist(),[b.BOS,65,66,b.EOS,b.PAD])
        self.assertEqual(y.tolist(),[65,66,67])

    def test_04_partial_utf8_prefix_is_not_decoded(self):
        raw='箱'.encode();tokens,y=b.document_rows(raw)
        self.assertEqual(tokens[1,1].item(),raw[0])
        self.assertEqual(y.tolist(),list(raw))

    def test_05_empty_and_overlong_documents_rejected(self):
        for raw in (b'',b'x'*b.SLOTS,'text'):
            with self.assertRaises(ValueError):b.document_rows(raw)

    def test_06_no_truncation(self):
        with self.assertRaises(ValueError):b.prefix_tensor(b'x'*(b.SLOTS-1))
        self.assertEqual(b.prefix_tensor(b'x'*(b.SLOTS-2)).shape,(b.SLOTS,))

    def test_07_uniform_eight_bits_per_byte(self):
        m=b.likelihood(torch.zeros((3,256),dtype=torch.float64),torch.tensor([0,128,255]))
        self.assertAlmostEqual(m['bits_per_byte'],8,places=12)
        self.assertLess(m['scoring_error'],b.TOLERANCE)

    def test_08_special_ids_never_scored(self):
        for value in (-1,256,257,258):
            with self.assertRaises(ValueError):b.likelihood(torch.zeros((1,256)),torch.tensor([value]))

    def test_09_nonfinite_logits_rejected(self):
        x=torch.zeros((1,256));x[0,1]=float('nan')
        with self.assertRaises(ValueError):b.likelihood(x,torch.tensor([1]))

    def test_10_likelihood_shape_errors(self):
        with self.assertRaises(ValueError):b.likelihood(torch.zeros((1,10)),torch.tensor([1]))
        with self.assertRaises(ValueError):b.likelihood(torch.zeros((1,256)),torch.tensor([1.]))

    def test_11_model_interface_has_no_target(self):
        self.assertEqual(tuple(inspect.signature(b.predict).parameters),('model','tokens'))
        self.assertNotIn('targets',inspect.getsource(b.predict))

    def test_12_batch_single_suffix_controls_execute(self):
        r,_=b.score_document(Toy(),b'abcdef')
        for k in ('scoring_error','batch_single_error','suffix_error'):self.assertLessEqual(r[k],b.TOLERANCE)

    def test_13_generation_uses_own_previous_bytes(self):
        seen=[]
        class Inspect(nn.Module):
            def forward(self,tokens,tasks):
                seen.append(tokens[0].tolist());out=torch.zeros((1,256),dtype=torch.float64)
                out[0,65+len(seen)]=1;return out
        generated=b.generate(Inspect(),b'X')
        self.assertEqual(generated,b'BCDE')
        self.assertEqual(seen[1][:4],[b.BOS,88,66,b.EOS])
        self.assertEqual(seen[-1][:6],[b.BOS,88,66,67,68,b.EOS])

    def test_14_predict_requires_full_vocabulary(self):
        class Wrong(nn.Module):
            def forward(self,*args):return torch.zeros((1,2))
        with self.assertRaises(ValueError):b.predict(Wrong(),b.prefix_tensor(b'X')[None,:])

    def test_15_weights_not_changed(self):
        model=Toy();before=b.fingerprint(model)
        b.score_document(model,b'xyz')
        self.assertEqual(b.fingerprint(model),before)

    def test_16_gate_not_based_on_language_score(self):
        s=dict(seeds=list(b.SEEDS),all_contract_checks=True,scored_bytes=246,
            model_forward_calls=378,new_training_steps=0,meaningful_language_score=False)
        self.assertTrue(b.gate(s))
        s['meaningful_language_score']=True;self.assertFalse(b.gate(s))

    def test_17_nonfinite_score_and_bad_replay_fail_row(self):
        docs=[]
        for text in b.TEXTS:
            row,_=b.score_document(Toy(),text.encode())
            row.update(reload_error=0.,generation_replayed=True);docs.append(row)
        r=dict(documents=docs,checkpoint_roundtrip=True,weights_unchanged=True,forward_calls=126)
        self.assertTrue(b.row_gate(r))
        docs[0]['bits_per_byte']=float('inf');self.assertFalse(b.row_gate(r))
        docs[0]['bits_per_byte']=8.;docs[0]['generation_replayed']=False;self.assertFalse(b.row_gate(r))

    def test_18_union_preserves_parent_and_checks_conflicts(self):
        parent={'preserved.py':'x'}
        self.assertEqual(b.pin_union(parent),set(parent)|set(b.OWN)|set(b.LM_SOURCES))
        with self.assertRaises(ValueError):b.pin_union({next(iter(b.LM_SOURCES)):'wrong'})

    def test_19_runner_order_and_cli_blocks(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/'tools/run_c231.ps1').read_text(encoding='utf-8')
        launch=(root/'tools/invoke_c231.ps1').read_text(encoding='utf-8')
        self.assertIn('expected_focused_tests = 2689',run)
        self.assertLess(run.index('authoring_selftest = PASS'),run.index('& $Python -u -c $Regression'))
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,'embedded','exec')
        self.assertIn('c230-v5f-prepared-capsule-42695282c3e6402f9fe7616ba3641099',launch)
        self.assertLess(launch.index('::ParseFile'),launch.index('$failure = $null'))
        self.assertIn('RUNNER_PARSE_ERROR',launch)

    def test_20_no_training_or_memory_candidate_in_run(self):
        source=inspect.getsource(b.run)
        self.assertNotIn('optim.',source);self.assertNotIn('.backward(',source)
        self.assertNotIn('prepared_capsule',inspect.getsource(b.new_model))
        self.assertFalse(b.manifest()['meaningful_language_score'])

    def test_21_module_alias_bindings(self):
        tree=ast.parse(inspect.getsource(b))
        refs={n.value.id for n in ast.walk(tree) if isinstance(n,ast.Attribute)
              and isinstance(n.value,ast.Name) and re.fullmatch(r'c\d+',n.value.id)}
        self.assertFalse(refs)

    def test_22_synthetic_run_serialization_and_postchecks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'parent.json';path.write_text('{}')
            pins=dict(b.LM_SOURCES)
            pins.update({name:'x' for name in b.OWN})
            pins.update({f'parent{i}':'x' for i in range(221)})
            protected={}
            for i in range(305+6+len(pins)-221):
                p=root/f'input{i}';p.write_bytes(b'x');protected[str(p)]=hashlib.sha256(b'x').hexdigest()
            a=SimpleNamespace(sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest(),
                git=lambda root,*args:b'HEAD' if args[0]=='rev-parse' else b'feat/sft-target-loss' if args[0]=='branch' else b'')
            parent=SimpleNamespace(parent_module=lambda:None,context=lambda p:SimpleNamespace(audit=a));seen=[]
            def check(*args):seen.append('check');return {},pins,protected
            with patch.object(b,'parent_module',return_value=parent),patch.object(b,'precheck',side_effect=check),patch.object(b,'new_model',side_effect=Toy),patch('sys.stdout',new=io.StringIO()):
                result=b.run(c230_summary=path,output_dir=root/'out',expected_head='HEAD')
            self.assertEqual(result['status'],'PASS');self.assertEqual(seen,['check','check'])
            self.assertEqual(result['validation_summary']['model_forward_calls'],378)
            self.assertEqual(len(result['artifacts']),5)

    def test_23_actual_v5b_model_contract(self):
        torch.set_num_threads(2)
        model=b.new_model(b.SEEDS[0]);before=b.fingerprint(model)
        self.assertEqual(sum(p.numel() for p in model.parameters()),13488)
        for text in b.TEXTS:
            row,_=b.score_document(model,text.encode())
            for key in ('scoring_error','batch_single_error','suffix_error'):
                self.assertLessEqual(row[key],b.TOLERANCE)
        self.assertEqual(b.fingerprint(model),before)

    def test_24_actual_historical_suite(self):
        root=Path(__file__).resolve().parents[1]
        names=b.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        self.assertEqual((len(names),loaded.countTestCases()),(116,2690))
        self.assertEqual(b.regression_suite(root).countTestCases(),2689)


if __name__=='__main__':unittest.main(verbosity=2)
