"""C236 authoring tests; synthetic fixtures are not scientific model results."""
import ast
from collections import Counter, defaultdict
import contextlib
import copy
import hashlib
import inspect
import io
import itertools
from pathlib import Path
import re
import tempfile
import unittest
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c236_minimal_binding as b


def fixture():
    names={"en":("box","book","ball","umbrella"),"ja":("箱","本","玉","傘")}
    rows=[]
    for a,c in itertools.combinations(range(4),2):
        for x,y in itertools.permutations(range(4),2):
            group=f"{a}-{c}-{x}-{y}"
            split="EVAL" if tuple(sorted((x,y))) in ((0,3),(1,2)) else "TRAIN"
            for language in names:
                for order,query in itertools.product((0,1),(a,c)):
                    row=dict(id=f"{language}-{group}-{order}-{query}",group=group,
                        objects=[a,c],values=[x,y],language=language,order=order,
                        query=query,split=split,target=ord(str(x if query==a else y)))
                    facts=[(a,x),(c,y)]
                    if order: facts.reverse()
                    row["prompt"]=";".join(names[language][k]+"="+str(v) for k,v in facts)+";"+names[language][query]+"="
                    rows.append(row)
    return rows


def perfect_metrics():
    return {lang:dict(rows=8,accuracy=1.0,answer_nll=.1,evidence_blind_accuracy=.5,
        query_blind_accuracy=.5,evidence_drop=.5,query_drop=.5,
        fact_pair_accuracy=1.0,query_pair_accuracy=1.0) for lang in ("en","ja")}


def records():
    return [dict(seed=seed,family=family,final_probe=perfect_metrics(),checkpoint_roundtrip=True,
        prediction_replayed=True,reload_max_error=0.0,replay_metric_error=0.0,weights_changed=True,
        fit=dict(steps=400,answer_presentations=12800),forward_calls=409,row_presentations=12944)
        for seed,family in b.identities()]


def payload(summary):
    pins={f"parent-{i}":"fixture" for i in range(256)};pins.update({x:"fixture" for x in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256={f"input-{i}":"fixture" for i in range(382)},
        artifacts=[dict(file=x) for x in b.OUTPUTS],validation_summary=summary,
        status="PASS" if summary["full_probe_gate"] else "FAIL",gate_f_candidate=False,network_calls=0)


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__();self.linear=torch.nn.Linear(4,256).double()
    def forward(self,tokens,tasks):
        return self.linear(tokens)


class Factory:
    @staticmethod
    def fingerprint(model):
        h=hashlib.sha256()
        for name,value in sorted(model.state_dict().items()):
            h.update(name.encode());h.update(value.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()


class Binding:
    """Instrumentation double; calls the real toy forward on all three views."""
    @staticmethod
    def evaluate(model,rows,views):
        training=model.training;model.eval()
        with torch.no_grad():
            logits=[model(x,torch.zeros(len(x),dtype=torch.int64)).detach() for x,_ in views]
        model.train(training)
        predictions=[x.argmax(-1).tolist() for x in logits];out={}
        for lang in ("en","ja"):
            ids=[i for i,r in enumerate(rows) if r["language"]==lang]
            accs=[sum(pred[i]==rows[i]["target"] for i in ids)/len(ids) for pred in predictions]
            pairs={kind:defaultdict(list) for kind in ("facts","query")}
            for i in ids:
                r=rows[i]
                pairs["facts"][(tuple(r["objects"]),tuple(sorted(r["values"])),r["order"],r["query"])].append(i)
                pairs["query"][(r["group"],r["order"])].append(i)
            paired={kind:sum(all(predictions[0][i]==rows[i]["target"] for i in g)
                    for g in groups.values())/len(groups) for kind,groups in pairs.items()}
            out[lang]=dict(rows=len(ids),accuracy=accs[0],answer_nll=float(F.cross_entropy(logits[0][ids],views[0][1][ids])),
                evidence_blind_accuracy=accs[1],query_blind_accuracy=accs[2],evidence_drop=accs[0]-accs[1],
                query_drop=accs[0]-accs[2],fact_pair_accuracy=paired["facts"],query_pair_accuracy=paired["query"])
        return out,logits


class C236Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.data=fixture();cls.train=[r for r in cls.data if r["split"]=="TRAIN"]

    def exercise(self):
        rows=b.select_probe(self.train)
        torch.manual_seed(9001);model=Toy()
        gen=torch.Generator().manual_seed(9002)
        x=torch.randn(16,4,dtype=torch.float64,generator=gen)
        y=torch.tensor([r["target"] for r in rows],dtype=torch.int64)
        views=[(x,y),(x*.5,y),(x*.25,y)]
        with contextlib.redirect_stdout(io.StringIO()):
            record,state,reference=b.train_one(model,binding=Binding,factory=Factory,rows=rows,views=views,
                seed=9003,family="full",expected_initial=Factory.fingerprint(model))
        return record,state,reference,rows,views

    def test_01_parent_fixture_matches_accepted_hash(self):
        self.assertEqual(b.digest(self.data),b.DATA_SHA)
        self.assertEqual((len(self.data),len(self.train)),(576,384))

    def test_02_manifest_hash_and_scope(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertFalse(b.manifest()["held_out_generalization_claim"])
        self.assertEqual(b.manifest()["held_out_evaluation_rows"],0)

    def test_03_probe_balance_and_identity(self):
        rows=b.select_probe(self.train)
        self.assertEqual((len(rows),b.digest(rows)),(16,b.PROBE_SHA))
        self.assertEqual(Counter(r["language"] for r in rows),{"en":8,"ja":8})
        self.assertEqual(Counter(r["target"] for r in rows),{48:8,49:8})
        self.assertEqual({r["split"] for r in rows},{"TRAIN"})
        self.assertEqual(len({r["id"] for r in rows}),16)

    def test_04_missing_parent_rows_rejected(self):
        with self.assertRaises(ValueError):b.select_probe(self.train[:-1])

    def test_05_probe_target_change_rejected(self):
        rows=copy.deepcopy(self.train);rows[0]["target"]=255
        with self.assertRaises(ValueError):b.select_probe(rows)

    def test_06_perfect_probe_passes(self):
        self.assertTrue(b.probe_pass(perfect_metrics()))

    def test_07_accuracy_failure_is_not_pass(self):
        m=perfect_metrics();m["en"].update(accuracy=.875,evidence_drop=.375,query_drop=.375)
        self.assertFalse(b.probe_pass(m))

    def test_08_mask_failure_is_not_pass(self):
        m=perfect_metrics();m["ja"].update(query_blind_accuracy=.75,query_drop=.25)
        self.assertFalse(b.probe_pass(m))

    def test_09_invalid_metrics_rejected(self):
        for key,value in (("rows",96),("accuracy",float("nan")),("query_drop",.25)):
            with self.subTest(key=key):
                m=perfect_metrics();m["en"][key]=value
                with self.assertRaises(ValueError):b.validate_metrics(m)

    def test_10_summary_fixed_workload(self):
        s=b.summarize(records())
        self.assertEqual((s["total_training_steps"],s["total_answer_presentations"],s["model_forward_calls"],s["total_row_presentations"]),
                         (2400,76800,2454,77664))
        b.validate_result(payload(s))

    def test_11_identity_order_rejected(self):
        with self.assertRaises(ValueError):b.summarize(list(reversed(records())))

    def test_12_valid_negative_keeps_baseline_separate(self):
        r=records();r[0]["final_probe"]["en"].update(accuracy=.5,evidence_drop=0.0,query_drop=0.0)
        s=b.summarize(r);self.assertFalse(s["full_probe_gate"]);self.assertTrue(s["gru_probe_gate"])
        p=payload(s);self.assertEqual(p["status"],"FAIL");b.validate_result(p)

    def test_13_bad_replay_is_invalid_not_negative(self):
        r=records();r[0]["reload_max_error"]=.1
        with self.assertRaises(ValueError):b.validate_result(payload(b.summarize(r)))

    def test_14_missing_protection_is_invalid(self):
        p=payload(b.summarize(records()));p["source_blobs"].pop(b.OWN[0])
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_15_fit_rejects_empty_or_bad_steps(self):
        x=torch.zeros(2,4,dtype=torch.float64);y=torch.zeros(2,dtype=torch.int64)
        for steps in (0,-1,True):
            with self.subTest(steps=steps):
                with self.assertRaises(ValueError):b.fit(Toy(),x,y,9000,steps=steps)

    def test_16_fit_deterministic_toy_updates(self):
        torch.manual_seed(9004);first=Toy();second=copy.deepcopy(first)
        before=Factory.fingerprint(first);x=torch.eye(4,dtype=torch.float64);y=torch.tensor([48,49,48,49])
        a=b.fit(first,x,y,9005,steps=2);b.fit(second,x,y,9005,steps=2)
        self.assertEqual(Factory.fingerprint(first),Factory.fingerprint(second))
        self.assertNotEqual(Factory.fingerprint(first),before)
        self.assertEqual((a["steps"],a["answer_presentations"]),(2,64))

    def test_17_fit_nonfinite_rejected(self):
        class Bad(Toy):
            def forward(self,tokens,tasks):return super().forward(tokens,tasks)*float("nan")
        with self.assertRaises(ValueError):b.fit(Bad(),torch.zeros(2,4,dtype=torch.float64),torch.tensor([48,49]),9006,steps=1)

    def test_18_actual_train_one_workload_path(self):
        record,state,reference,rows,views=self.exercise()
        self.assertEqual((record["forward_calls"],record["row_presentations"]),(406,12896))
        self.assertEqual(record["predictions"],b.prediction_record(reference))
        self.assertNotEqual(record["initial_sha256"],record["final_sha256"])
        self.assertEqual(len(state),2)

    def test_19_actual_replay_path(self):
        record,state,reference,rows,views=self.exercise()
        b.replay_one(Toy(),state,record,reference,binding=Binding,factory=Factory,rows=rows,views=views)
        self.assertEqual((record["forward_calls"],record["row_presentations"]),(409,12944))
        self.assertTrue(record["checkpoint_roundtrip"])

    def test_20_replay_rejects_changed_logits(self):
        record,state,reference,rows,views=self.exercise();reference[0]=reference[0]+.1
        with self.assertRaises(ValueError):
            b.replay_one(Toy(),state,record,reference,binding=Binding,factory=Factory,rows=rows,views=views)

    def test_21_checkpoint_schema_and_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"model.pt"
            value=dict(schema="fold-c236-minimal-binding-v1",identities=[list(x) for x in b.identities()],states=[{} for _ in range(6)])
            torch.save(value,path);self.assertEqual(len(b.load_bundle(path)),6)
            value["identities"].reverse();torch.save(value,path)
            with self.assertRaises(ValueError):b.load_bundle(path)

    def test_22_actual_run_dispatch_and_common_copy_order(self):
        tree=ast.parse(inspect.getsource(b.run))
        calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "")
               for n in ast.walk(tree) if isinstance(n,ast.Call)]
        line=lambda name:min(n for n,x in calls if x==name)
        self.assertLess(line("load_inputs"),line("train_one"))
        self.assertLess(line("new_baseline"),line("train_one"))
        self.assertLess(line("train_one"),line("save"))
        self.assertLess(line("save"),line("load_bundle"))
        self.assertLess(line("load_bundle"),line("replay_one"))
        pre=ast.parse(inspect.getsource(b.precheck))
        names={n.func.id for n in ast.walk(pre) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
        self.assertIn("audit_fit_contract",names)

    def test_23_runner_embedded_python_and_preflight(self):
        root=Path(__file__).resolve().parents[1]
        run=(root/"tools/run_c236.ps1").read_text(encoding="utf-8")
        launch=(root/"tools/invoke_c236.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",run,re.S)
        self.assertEqual(len(blocks),3)
        for block in blocks:compile(block,"embedded","exec")
        self.assertLess(launch.index("::ParseFile"),launch.index("$failure = $null"))
        self.assertIn("c235-v5b-frozen-binding-diagnostic-17d75b38b35249a297bde78cee0f1d43",launch)
        self.assertIn("c234-v5b-context-binding-fb381b067fc54cb3a46dbf3897ece200",launch)
        pre,reg,post=[ast.parse(block) for block in blocks]
        def argv_indices(tree):
            return {n.slice.value for n in ast.walk(tree) if isinstance(n,ast.Subscript)
                and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name)
                and n.value.value.id=="sys" and n.value.attr=="argv" and isinstance(n.slice,ast.Constant)}
        self.assertEqual(argv_indices(pre),{1,2})
        self.assertEqual(argv_indices(post),{1,2,3,4})

    def test_24_own_loader_count_semantic(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self))
        self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        ids=[t.id() for t in b.flatten(suite)]
        self.assertEqual(len(ids),len(set(ids)))
        m=b.manifest();self.assertEqual(m["loaded_tests"]-m["focused_tests"],1)
        self.assertEqual((len(b.OWN),len(b.OUTPUTS)),(6,5))


if __name__=="__main__":unittest.main(verbosity=2)
