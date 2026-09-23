"""C237 authoring tests: synthetic instrumentation, not accepted-model evidence."""
import ast
from collections import defaultdict
import copy
import contextlib
import io
import hashlib
import inspect
import itertools
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c237_frozen_signal_audit as b


def fixture():
    rows=[]
    names={"en":("box","book"),"ja":("箱","本")}
    for x,y in ((0,1),(1,0)):
        group=f"0-1-{x}-{y}"
        for language in names:
            for order,query in itertools.product((0,1),(0,1)):
                facts=[(0,x),(1,y)]
                if order: facts.reverse()
                prompt=";".join(names[language][k]+"="+str(v) for k,v in facts)+";"+names[language][query]+"="
                rows.append(dict(id=f"{language}-{group}-{order}-{query}",group=group,objects=[0,1],
                    values=[x,y],language=language,order=order,query=query,split="TRAIN",
                    target=ord(str(x if query==0 else y)),prompt=prompt))
    return rows


def views_for(rows):
    names={"en":("box","book"),"ja":("箱","本")}
    views=[]
    for mode in b.VIEWS:
        encoded=[]
        for row in rows:
            facts=list(zip(row["objects"],row["values"],strict=True))
            if row["order"]: facts.reverse()
            text=";".join(names[row["language"]][k]+"="+("?" if mode=="evidence_blind" else str(v)) for k,v in facts)
            text+=";"+("?" if mode=="query_blind" else names[row["language"]][row["query"]])+"="
            ids=[b.BOS,*text.encode(),b.EOS];ids.extend([b.PAD]*(48-len(ids)))
            encoded.append(ids)
        views.append((torch.tensor(encoded),torch.tensor([r["target"] for r in rows])))
    return views


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.byte_embedding=torch.nn.Embedding(259,16,padding_idx=256).double()
        self.local_encoder=torch.nn.GRU(16,16,batch_first=True).double()
        self.readout_norm=torch.nn.LayerNorm(16).double()
        self.decoder=torch.nn.Linear(16,256).double()
    def forward(self,tokens,tasks):
        encoded,_=self.local_encoder(self.byte_embedding(tokens))
        index=(tokens!=b.PAD).sum(1)-1
        pooled=encoded[torch.arange(len(tokens)),index]
        return self.decoder(self.readout_norm(pooled))


def fingerprint(model):
    h=hashlib.sha256()
    for name,value in sorted(model.state_dict().items()):
        h.update(name.encode());h.update(value.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def make_model(seed=9010):
    torch.manual_seed(seed)
    return Toy().eval().requires_grad_(False)


class Binding:
    @staticmethod
    def evaluate(model,rows,views):
        with torch.no_grad():
            logits=[model(tokens,torch.zeros(len(tokens),dtype=torch.int64)).detach() for tokens,_ in views]
        preds=[x.argmax(-1).tolist() for x in logits];metrics={}
        for lang in ("en","ja"):
            ids=[i for i,r in enumerate(rows) if r["language"]==lang]
            acc=[sum(p[i]==rows[i]["target"] for i in ids)/len(ids) for p in preds]
            paired={kind:sum(preds[0][i]==rows[i]["target"] and preds[0][j]==rows[j]["target"]
                for i,j in b.paired_indices(rows,kind,lang))/4 for kind in ("facts","query")}
            metrics[lang]=dict(rows=8,accuracy=acc[0],answer_nll=float(F.cross_entropy(logits[0][ids],views[0][1][ids])),
                evidence_blind_accuracy=acc[1],query_blind_accuracy=acc[2],evidence_drop=acc[0]-acc[1],
                query_drop=acc[0]-acc[2],fact_pair_accuracy=paired["facts"],query_pair_accuracy=paired["query"])
        return metrics,logits
    @staticmethod
    def tensors(rows,mode): return views_for(rows)[b.VIEWS.index(mode)]
    @staticmethod
    def parent_module(): return SimpleNamespace(new_baseline=lambda model:model)


def payload(summary):
    pins={f"parent-source-{i}":"synthetic" for i in range(262)}
    pins.update({p:"synthetic" for p in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256={f"synthetic-input-{i}":"0"*64 for i in range(394)},
        artifacts=[dict(file=p) for p in b.OUTPUTS],validation_summary=summary,gate_f_candidate=False,network_calls=0)


def complete_records(record,traces,rows):
    cells,_=b.analyze(rows,traces)
    return [dict(copy.deepcopy(record),seed=seed,family=family,parent_metric_error=0.0,
        parent_predictions_equal=True,cells=copy.deepcopy(cells)) for seed,family in b.identities()]


class C237Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.rows=fixture();cls.views=views_for(cls.rows)
        cls.record,cls.traces=b.capture_model(make_model(),cls.rows,cls.views,binding=Binding,fingerprint=fingerprint)

    def test_01_manifest_hash_and_scope(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        m=b.manifest();self.assertEqual((m["new_training_steps"],m["optimizer_steps"],m["checkpoint_writes"]),(0,0,0))
        self.assertFalse(m["causal_claim"]);self.assertFalse(m["gate_f_candidate"])

    def test_02_fixture_exact_accepted_cohort(self):
        self.assertEqual(b.digest(self.rows),b.PARENT_ARTIFACTS["probe-dataset.json"])
        self.assertEqual({r["split"] for r in self.rows},{"TRAIN"})

    def test_03_query_pairs_change_target(self):
        for lang in ("en","ja"):
            pairs=b.paired_indices(self.rows,"query",lang);self.assertEqual(len(pairs),4)
            self.assertTrue(all(self.rows[i]["target"]!=self.rows[j]["target"] for i,j in pairs))

    def test_04_fact_and_order_pairs_separate(self):
        for lang in ("en","ja"):
            for kind in ("facts","order"):
                for i,j in b.paired_indices(self.rows,kind,lang):
                    self.assertEqual(self.rows[i]["target"]==self.rows[j]["target"],kind=="order")

    def test_05_broken_pair_rejected(self):
        rows=copy.deepcopy(self.rows);rows[0]["target"]=rows[1]["target"]
        with self.assertRaises(ValueError):b.paired_indices(rows,"query","en")
        with self.assertRaises(ValueError):b.paired_indices(self.rows[:-1],"query","ja")

    def test_06_eos_is_last_real_byte_boundary(self):
        tokens=self.views[0][0];ids=b.eos_indices(tokens)
        self.assertTrue(torch.equal(tokens[torch.arange(16),ids],torch.full((16,),b.EOS)))
        self.assertEqual(ids.tolist(),[len(r["prompt"].encode())+1 for r in self.rows])

    def test_07_malformed_prefix_rejected(self):
        for bad in (b.PAD,b.EOS,-1,300):
            tokens=self.views[0][0].clone();tokens[0,2]=bad
            with self.subTest(token=bad):
                with self.assertRaises(ValueError):b.eos_indices(tokens)

    def test_08_exact_equality_not_tolerance_threshold(self):
        a=torch.zeros(16,dtype=torch.float64);c=a.clone();c[0]=1e-12
        d=b.difference(a,c);self.assertFalse(d["exact_equal"]);self.assertEqual(d["linf"],1e-12)
        self.assertTrue(b.difference(a,a)["exact_equal"])

    def test_09_zero_scale_is_defined(self):
        a=torch.zeros(16,dtype=torch.float64)
        self.assertEqual(b.difference(a,a)["relative_l2"],0.0)

    def test_10_nonfinite_tensor_rejected(self):
        for value in (float("nan"),float("inf")):
            x=torch.zeros(16,dtype=torch.float64);x[0]=value
            with self.assertRaises(ValueError):b.difference(x,x)

    def test_11_argmax_not_restricted_to_supplied_digits(self):
        x=torch.zeros(256,dtype=torch.float64);x[255]=10
        out=b.row_output(x,48);self.assertEqual(out["prediction"],255);self.assertFalse(out["correct"])

    def test_12_logit_change_and_same_answer_are_separate(self):
        a={k:v.clone() for k,v in self.traces["normal"].items()};c={k:v.clone() for k,v in a.items()}
        c["logits"][0]+=0.25
        item=b.contrast(a,c,0,0,self.rows,"synthetic-common-shift")
        self.assertEqual(item["first"]["prediction"],item["second"]["prediction"])
        self.assertGreater(item["differences"]["logits"]["linf"],0)

    def test_13_analysis_pair_and_mask_counts(self):
        cells,details=b.analyze(self.rows,self.traces);self.assertEqual(len(details),56)
        for lang in cells:
            self.assertEqual([cells[lang][k]["count"] for k in b.PAIR_KINDS],[4,4,4])
            self.assertEqual([cells[lang][k]["count"] for k in b.VIEWS[1:]],[8,8])

    def test_14_passive_capture_matches_and_removes_hooks(self):
        model=make_model();before=fingerprint(model)
        record,traces=b.capture_model(model,self.rows,self.views,binding=Binding,fingerprint=fingerprint)
        self.assertEqual((record["forward_calls"],record["row_presentations"]),(6,96))
        self.assertEqual(record["passive_error"],0.0);self.assertEqual(before,fingerprint(model))
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()))
        self.assertEqual(set(traces),set(b.VIEWS))

    def test_15_error_cleanup_does_not_leave_hooks(self):
        model=make_model();calls=[0]
        class Broken:
            @staticmethod
            def evaluate(*args):
                calls[0]+=1
                if calls[0]==2:raise ValueError("synthetic evaluator fault")
                return Binding.evaluate(*args)
        with self.assertRaises(ValueError):b.capture_model(model,self.rows,self.views,binding=Broken,fingerprint=fingerprint)
        self.assertTrue(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()))

    def test_16_trainable_model_is_rejected(self):
        model=make_model().requires_grad_(True)
        with self.assertRaises(ValueError):b.capture_model(model,self.rows,self.views,binding=Binding,fingerprint=fingerprint)

    def test_17_decoder_reconstruction_detects_hidden_postprocessing(self):
        class Shifted(Toy):
            def forward(self,tokens,tasks):return super().forward(tokens,tasks)+1.0
        model=Shifted().eval().requires_grad_(False)
        with self.assertRaisesRegex(ValueError,"reconstruction"):
            b.capture_model(model,self.rows,self.views,binding=Binding,fingerprint=fingerprint)

    def test_18_metric_key_and_nonfinite_contract(self):
        metrics=self.record["metrics"];self.assertEqual(b.metric_error(metrics,metrics),0)
        for mutation in ("key","nonfinite"):
            other=copy.deepcopy(metrics)
            if mutation=="key":other["en"]["unexpected"]=0
            else:other["en"]["answer_nll"]=float("nan")
            with self.assertRaises(ValueError):b.metric_error(metrics,other)

    def test_19_parent_adapter_uses_final_probe_and_final_fingerprint(self):
        records=[]
        for seed,family in b.identities():
            records.append(dict(seed=seed,family=family,final_probe=copy.deepcopy(self.record["metrics"]),
                final_sha256="a"*64,checkpoint_roundtrip=True,prediction_replayed=True,weights_changed=True,
                reload_max_error=0.0,replay_metric_error=0.0,predictions=copy.deepcopy(self.record["predictions"])))
        parent=SimpleNamespace(validate_metrics=lambda m:b.metric_error(m,m))
        self.assertEqual(len(b.validate_parent_records(records,parent)),6)
        bad=copy.deepcopy(records);bad[0]["prediction_replayed"]=False
        with self.assertRaises(ValueError):b.validate_parent_records(bad,parent)
        with self.assertRaises(ValueError):b.validate_parent_records(list(reversed(records)),parent)

    def test_20_integrity_gate_independent_of_accuracy(self):
        records=complete_records(self.record,self.traces,self.rows)
        summary=b.summarize(records);b.validate_result(payload(summary))
        self.assertFalse(summary["capability_pass_claim"])
        self.assertEqual((summary["model_forward_calls"],summary["row_presentations"]),(36,576))

    def test_21_mutation_missing_work_or_replay_rejected(self):
        for key,value in (("after_sha256","b"*64),("forward_calls",5),("parent_predictions_equal",False),("passive_error",1.0)):
            records=complete_records(self.record,self.traces,self.rows);records[0][key]=value
            with self.subTest(key=key):
                with self.assertRaises(ValueError):b.validate_result(payload(b.summarize(records)))

    def test_22_synthetic_full_run_uses_loader_and_frozen_capture(self):
        rows=self.rows;views=self.views;parent_records=[];states=[]
        for seed,family in b.identities():
            model=make_model(seed);metrics,logits=Binding.evaluate(model,rows,views)
            states.append(copy.deepcopy(model.state_dict()))
            parent_records.append(dict(final_sha256=fingerprint(model),final_probe=metrics,predictions=b.prediction_record(logits)))
        base=payload(b.summarize(complete_records(self.record,self.traces,rows)))
        class Audit:
            @staticmethod
            def git(root,*args):
                if args[:2]==("rev-parse","HEAD"):return b"synthetic-head"
                if args[:2]==("branch","--show-current"):return b"feat/sft-target-loss"
                return b""
            @staticmethod
            def sha(path):
                if str(path).startswith("synthetic-input-"):return "0"*64
                return hashlib.sha256(Path(path).read_bytes()).hexdigest()
            @staticmethod
            def read_json(path):return json.loads(Path(path).read_text())
            @staticmethod
            def safe_child(root,name):
                path=(Path(root)/name).resolve()
                if path.parent!=Path(root).resolve():raise ValueError("unsafe artifact path")
                return path
        factory=SimpleNamespace(new_model=make_model,fingerprint=fingerprint)
        with tempfile.TemporaryDirectory() as tmp, patch.object(b,"context",return_value=(None,Binding,factory,Audit)), \
            patch.object(b,"precheck",return_value=(base["source_blobs"],base["input_sha256"])) as pre, \
            patch.object(b,"load_inputs",return_value=(rows,parent_records,states)) as loader:
            (Path(tmp)/"probe-dataset.json").write_bytes(b.blob(rows))
            with contextlib.redirect_stdout(io.StringIO()):
                result=b.run(c236_summary=Path(tmp)/"parent.json",output_dir=Path(tmp)/"out",expected_head="synthetic-head")
            loader.assert_called_once();self.assertEqual(pre.call_count,2)
            b.validate_result(result)
            verified,recs=b.verify_artifacts(Path(tmp)/"out",Path(tmp)/"parent.json","synthetic-head")
            self.assertEqual(verified,result);self.assertEqual(len(recs),6)
            with self.assertRaises(ValueError):b.verify_artifacts(Path(tmp)/"out",Path(tmp)/"parent.json","wrong-head")
            self.assertEqual(result["validation_summary"]["model_forward_calls"],36)
            self.assertEqual({p.name for p in (Path(tmp)/"out").iterdir()},b.OUTPUTS|{"summary.json"})
        tree=ast.parse(inspect.getsource(b.run))
        called={n.func.id for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
        self.assertTrue({"load_inputs","capture_model","analyze"}<=called)

    def test_23_runner_python_cli_and_launcher_parser(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c237.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools/invoke_c237.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        def argv(text):
            return {n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript)
                and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name)
                and n.value.value.id=="sys" and n.value.attr=="argv" and isinstance(n.slice,ast.Constant)}
        self.assertEqual(argv(blocks[0]),{1});self.assertEqual(argv(blocks[2]),{1,2,3})
        self.assertLess(launcher.index("::ParseFile"),launcher.index("$failure = $null"))
        self.assertIn("c236-v5b-minimal-binding-9cc3975f1c304ea893b8b53104ee8f71",launcher)

    def test_24_own_count_and_forbidden_execution_ast(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self))
        ids=[t.id() for t in b.flatten(suite)]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        tree=ast.parse(inspect.getsource(b))
        for node in ast.walk(tree):
            if isinstance(node,ast.Call):
                name=node.func.id if isinstance(node.func,ast.Name) else node.func.attr if isinstance(node.func,ast.Attribute) else ""
                self.assertNotIn(name,{"fit","backward","step","zero_grad"})
            if isinstance(node,ast.Attribute) and isinstance(node.value,ast.Name):
                self.assertFalse(node.value.id=="torch" and node.attr in {"save","optim"})


if __name__=="__main__":unittest.main(verbosity=2)
