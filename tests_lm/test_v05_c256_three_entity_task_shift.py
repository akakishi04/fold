"""C256 authoring tests. Synthetic score fixtures are not capability evidence."""
import ast
import copy
import io
import re
from pathlib import Path
import unittest
from unittest.mock import patch
import torch
from fold_lm.v05_benchmarks import model_c256_three_entity_task_shift as b

def perfect_metric():
    return dict(rows=72,accuracy=1.0,answer_nll=.01,evidence_blind_accuracy=.25,query_blind_accuracy=.25,
        evidence_drop=.75,query_drop=.75,order_pair_accuracy=1.0,query_triplet_accuracy=1.0)

def perfect_final():
    return {s:{"en":perfect_metric(),"ja":perfect_metric()} for s in b.SPLITS}

def records():
    out=[]
    for seed,arm in b.identities():
        out.append(dict(seed=seed,arm=arm,parameters=14256,weights_changed=True,head_weights_changed=True,
            checkpoint_roundtrip=True,reload_max_error=0.0,fit=dict(steps=800,answer_presentations=38400),
            forward_calls=806,row_presentations=39264,replay_forward_calls=6,replay_row_presentations=864,
            final=perfect_final(),backbone_initial_sha256="a"*64,wrapper_initial_sha256="b"*64,
            head_initial_sha256="c"*64,final_sha256="d"*64))
    return out

def payload(summary):
    pins={f"old-{i}":"fixture" for i in range(376)}
    pins.update({x:"fixture" for x in b.OWN})
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256={f"input-{i}":"0"*64 for i in range(623)},
        artifacts=[dict(file=x) for x in b.OUTPUTS],validation_summary=summary,
        production_adoption=False,gate_f_candidate=False,network_calls=0)

class Case(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        cls.parent,cls.c252,cls.reader,cls.factory,cls.audit=b.context()
        cls.parts=b.dataset()

    def test_01_manifest_and_dataset_hash(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),b.TASK_SHA)
        with patch("sys.stdout",new=io.StringIO()):
            b.validate_registration(382,623)
            for counts in ((381,623),(382,622)):
                with self.assertRaisesRegex(ValueError,"source/input counts"):
                    b.validate_registration(*counts)
            with patch.object(b,"MANIFEST_SHA","0"*64):
                with self.assertRaisesRegex(ValueError,"manifest hash"):
                    b.validate_registration(382,623)

    def test_02_partition_shape_and_unique_ids(self):
        self.assertEqual({k:len(v) for k,v in self.parts.items()},b.ROWS)
        self.assertFalse({r["id"] for r in self.parts["TRAIN"]}&{r["id"] for r in self.parts["HOLDOUT"]})

    def test_03_assignment_marginals_balanced(self):
        for rows in self.parts.values():
            assignments={tuple(r["assignment"]) for r in rows}
            self.assertEqual(len(assignments),12)
            for pos in range(3):
                self.assertEqual({v:sum(a[pos]==v for a in assignments) for v in range(4)},{0:3,1:3,2:3,3:3})

    def test_04_exact_assignments_do_not_cross_split(self):
        train={tuple(r["assignment"]) for r in self.parts["TRAIN"]}
        held={tuple(r["assignment"]) for r in self.parts["HOLDOUT"]}
        self.assertFalse(train&held);self.assertEqual(len(train|held),24)

    def test_05_render_views_and_target_semantics(self):
        r=self.parts["TRAIN"][0]
        self.assertEqual(r["prompt"],b.render(r,"normal"))
        self.assertNotIn("?",b.render(r,"normal"))
        self.assertEqual(b.render(r,"evidence_blind").count("?"),3)
        self.assertTrue(b.render(r,"query_blind").endswith("?="))
        self.assertEqual(r["target"],48+r["assignment"][r["query"]])

    def test_06_tensor_contract_real_factory(self):
        x,y=b.tensors(self.parts["TRAIN"][:8],"normal",self.factory)
        self.assertEqual(tuple(x.shape),(8,48));self.assertEqual(tuple(y.shape),(8,))
        self.assertEqual(x.dtype,torch.int64);self.assertTrue((x[:,0]==257).all())

    def test_07_batch_schedule_covers_each_epoch(self):
        for seed in b.SEEDS[:2]:
            blocks=[b.batch_indices(seed,i) for i in range(3)]
            self.assertTrue(all(len(x)==48 for x in blocks))
            joined=torch.cat(blocks);self.assertEqual(len(set(joined.tolist())),144)
            self.assertEqual(set(joined.tolist()),set(range(144)))

    def test_08_batch_schedule_is_deterministic_and_seeded(self):
        self.assertTrue(torch.equal(b.batch_indices(b.SEEDS[0],17),b.batch_indices(b.SEEDS[0],17)))
        self.assertFalse(torch.equal(b.batch_indices(b.SEEDS[0],17),b.batch_indices(b.SEEDS[1],17)))

    def test_09_seed_batch_is_fresh(self):
        self.assertTrue(set(b.SEEDS).isdisjoint({250001,250002,250003,250004,250005}))
        self.assertEqual(len(set(b.SEEDS)),5)

    def test_10_candidate_control_capacity_and_common_backbone(self):
        source=self.factory.new_model(b.SEEDS[0]);h=b.fingerprint(source)
        a=b.make_model(copy.deepcopy(source),b.ARMS[0],b.SEEDS[0],self.c252,self.reader)
        c=b.make_model(copy.deepcopy(source),b.ARMS[1],b.SEEDS[0],self.c252,self.reader)
        self.assertEqual(sum(p.numel() for p in a.parameters()),14256)
        self.assertEqual(sum(p.numel() for p in c.parameters()),14256)
        self.assertEqual(b.fingerprint(a.backbone),h);self.assertEqual(b.fingerprint(c.backbone),h)

    def test_11_zero_output_heads_preserve_initial_backbone_logits(self):
        source=self.factory.new_model(b.SEEDS[0]).eval()
        x,_=b.tensors(self.parts["TRAIN"][:12],"normal",self.factory);task=torch.zeros(12,dtype=torch.int64)
        with torch.no_grad(): base=source(x,task)
        for arm in b.ARMS:
            model=b.make_model(copy.deepcopy(source),arm,b.SEEDS[0],self.c252,self.reader).eval()
            with torch.no_grad(): out=model(x,task)
            self.assertLessEqual(float((out-base).abs().max()),b.TOL)

    def test_12_candidate_gradient_reaches_reader_and_core(self):
        model=b.make_model(self.factory.new_model(b.SEEDS[0]),b.ARMS[0],b.SEEDS[0],self.c252,self.reader)
        ids=b.batch_indices(b.SEEDS[0],0);x,y=b.tensors(self.parts["TRAIN"],"normal",self.factory)
        torch.nn.functional.cross_entropy(model(x[ids],torch.zeros(48,dtype=torch.int64)),y[ids]).backward()
        self.assertGreater(float(model.read.output.weight.grad.abs().sum()),0)
        self.assertTrue(any(p.grad is not None and float(p.grad.abs().sum())>0 for p in model.backbone.core.parameters()))

    def test_13_control_gradient_reaches_adapter_and_core(self):
        model=b.make_model(self.factory.new_model(b.SEEDS[0]),b.ARMS[1],b.SEEDS[0],self.c252,self.reader)
        ids=b.batch_indices(b.SEEDS[0],0);x,y=b.tensors(self.parts["TRAIN"],"normal",self.factory)
        torch.nn.functional.cross_entropy(model(x[ids],torch.zeros(48,dtype=torch.int64)),y[ids]).backward()
        self.assertGreater(float(model.read.output.weight.grad.abs().sum()),0)
        self.assertTrue(any(p.grad is not None and float(p.grad.abs().sum())>0 for p in model.backbone.core.parameters()))

    def test_14_perfect_metric_contract_and_gate(self):
        rows=self.parts["TRAIN"];target=torch.tensor([r["target"] for r in rows])
        normal=torch.full((144,256),-20.,dtype=torch.float64);normal[torch.arange(144),target]=20
        blind=torch.full_like(normal,-20.);blind[:,48]=20
        m,p=b.metrics(rows,dict(normal=normal,evidence_blind=blind,query_blind=blind))
        b.validate_metrics(m)
        self.assertTrue(all(b.cell_pass(x) for x in m.values()))
        self.assertTrue(all(x["order_pair_accuracy"]==1 and x["query_triplet_accuracy"]==1 for x in m.values()))

    def test_15_query_triplet_and_order_group_counts(self):
        rows=self.parts["HOLDOUT"]
        for lang in ("en","ja"):
            subset=[r for r in rows if r["language"]==lang]
            order={(tuple(r["assignment"]),r["query"]) for r in subset}
            query={(tuple(r["assignment"]),r["order"]) for r in subset}
            self.assertEqual((len(order),len(query)),(36,24))

    def test_16_gate_requires_each_registered_dimension(self):
        for key,value in (("accuracy",.89),("order_pair_accuracy",.79),("query_triplet_accuracy",.79),
                          ("evidence_drop",.34),("query_drop",.34)):
            m=perfect_metric();m[key]=value
            self.assertFalse(b.cell_pass(m),key)

    def test_17_actual_evaluate_is_state_preserving(self):
        model=b.make_model(self.factory.new_model(b.SEEDS[0]),b.ARMS[0],b.SEEDS[0],self.c252,self.reader)
        before=b.fingerprint(model);final,pred,raw=b.evaluate(model,self.parts,self.factory)
        self.assertEqual(b.fingerprint(model),before);self.assertEqual(set(final),set(b.SPLITS))
        self.assertEqual(raw["TRAIN"]["normal"].shape,(144,256));self.assertEqual(len(pred["HOLDOUT"]["normal"]),144)

    def test_18_metric_error_tolerance(self):
        a=perfect_final();c=copy.deepcopy(a);c["HOLDOUT"]["en"]["answer_nll"]+=5e-10
        self.assertLessEqual(b.metric_error(a,c),b.TOL)
        c["HOLDOUT"]["en"]["answer_nll"]+=2e-9
        self.assertGreater(b.metric_error(a,c),b.TOL)

    def test_19_checkpoint_replay_actual_untrained_model(self):
        seed=b.SEEDS[0];model=b.make_model(self.factory.new_model(seed),b.ARMS[0],seed,self.c252,self.reader)
        final,pred,raw=b.evaluate(model,self.parts,self.factory)
        record=dict(final_sha256=b.fingerprint(model),final=final,predictions=pred)
        state={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
        fresh=b.make_model(self.factory.new_model(seed),b.ARMS[0],seed,self.c252,self.reader)
        b.replay_one(fresh,state,record,raw,self.parts,self.factory)
        self.assertTrue(record["checkpoint_roundtrip"]);self.assertLessEqual(record["reload_max_error"],b.TOL)

    def test_20_summary_perfect_candidate_passes(self):
        s=b.summarize(records());self.assertTrue(s["candidate_gate"])
        self.assertEqual(s["seed_pass_counts"],{b.ARMS[0]:5,b.ARMS[1]:5})
        self.assertEqual((s["model_forward_calls"],s["row_presentations"]),(8120,401280))

    def test_21_summary_one_candidate_miss_fails_primary(self):
        r=records();r[0]["final"]["HOLDOUT"]["en"]["accuracy"]=.5
        s=b.summarize(r);self.assertFalse(s["candidate_gate"]);self.assertEqual(s["seed_pass_counts"][b.ARMS[0]],4)

    def test_22_result_count_and_scope_guards(self):
        s=b.summarize(records());p=payload(s);b.validate_result(p)
        for key,val in (("model_forward_calls",8119),("candidate_gate",False)):
            bad=copy.deepcopy(p);bad["validation_summary"][key]=val
            if key=="candidate_gate": bad["status"]="PASS"
            with self.assertRaises(ValueError):b.validate_result(bad)

    def test_23_constructed_historical_filter(self):
        class Dummy(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        suite=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture{i}") for i in range(3313)])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),3313)

    def test_24_runner_cli_and_launcher_contract(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c256.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools/invoke_c256.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for x in blocks:compile(x,"embedded","exec")
        def argv(x):
            return {n.slice.value for n in ast.walk(ast.parse(x)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant)
                and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"}
        self.assertEqual(argv(blocks[0]),{1});self.assertEqual(argv(blocks[2]),{1,2,3})
        failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher)
        self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start())
        self.assertIn("c255-v5b-value-residual-8203653a07964d9bb549c272a8b9b943",launcher)

if __name__=="__main__":unittest.main(verbosity=2)
