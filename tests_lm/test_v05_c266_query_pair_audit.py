"""Synthetic saved logits test attribution; no learned model or historical suite is implied."""
import ast
from collections import defaultdict
import contextlib
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
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c266_query_pair_audit as b


def rows_fixture():
    rows = []
    for entities in ((0,1),(0,2),(1,2)):
        for values in itertools.permutations(range(4),2):
            for language in ("en","ja"):
                names = ("a","b","c") if language == "en" else ("甲","乙","丙")
                for permutation in (entities,entities[::-1]):
                    for query in entities:
                        rid = ":".join((language,"".join(map(str,entities)),"".join(map(str,values)),"".join(map(str,permutation)),str(query)))
                        r = dict(id=rid,entities=list(entities),values=list(values),language=language,permutation=list(permutation),query=query,target=48+values[entities.index(query)])
                        r["prompt"] = ";".join(names[i]+"="+str(values[entities.index(i)]) for i in permutation)+";"+names[query]+"="
                        rows.append(r)
    return rows


def raw_fixture(rows, strategy):
    x = torch.full((288,256), -10., dtype=torch.float64)
    for i,r in enumerate(rows):
        target = r["target"]
        if strategy == "swap": target = 48+r["values"][1-r["entities"].index(r["query"])]
        if strategy == "collapse": target = 48+r["values"][0]
        if strategy == "outside": target = 200
        x[i,target] = 10.
    return {"normal":x, "evidence_blind":x.clone(), "query_blind":x.clone()}


def expected_metrics(records, rows):
    result = []
    for r in records:
        profiles = {}
        for p,raw in r["renamed"].items():
            pred = raw["normal"].argmax(-1).tolist(); cells = []
            for language in ("en","ja"):
                for entities in ((0,1),(0,2),(1,2)):
                    for perm in (entities,entities[::-1]):
                        ids = [i for i,x in enumerate(rows) if (x["language"],tuple(x["entities"]),tuple(x["permutation"])) == (language,entities,perm)]
                        groups = defaultdict(list)
                        for i in ids: groups[tuple(rows[i]["values"])].append(i)
                        cells.append(dict(language=language,entities=list(entities),permutation=list(perm),
                            correct=sum(pred[i] == rows[i]["target"] for i in ids),
                            query_pair_accuracy=sum(all(pred[i] == rows[i]["target"] for i in g) for g in groups.values())/12))
            profiles[p] = dict(correct=sum(pred[i] == x["target"] for i,x in enumerate(rows)),rows=288,cells=cells)
        result.append(dict(seed=r["seed"],arm=r["arm"],profiles=profiles))
    return result


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("fixture-input-"): return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):
        child = (Path(root)/name).resolve(); b.require(child.parent == Path(root).resolve(),"unsafe path"); return child
    @staticmethod
    def git(root,*args):
        if args == ("rev-parse","HEAD"): return b"fixture-head"
        if args == ("branch","--show-current"): return b"feat/sft-target-loss"
        return b""


def protection():
    return ({**{f"old-{i}":"fixture" for i in range(436)},**{n:"fixture" for n in b.OWN}},
            {f"fixture-input-{i}":"0"*64 for i in range(748)})


class C266Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2); cls.rows = rows_fixture()
        raw = dict(zip(b.PROFILES,[raw_fixture(cls.rows,k) for k in ("correct","swap","collapse")]))
        cls.records = [dict(seed=s,arm=a,weights_preserved=True,renamed=raw) for s,a in b.identities()]
        cls.metrics = expected_metrics(cls.records,cls.rows)
        cls.outputs = b.analyze(cls.records,cls.rows,cls.metrics)

    def test_01_manifest_and_row_identities(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.rows),b.ROW_SHA)
        self.assertTrue(all(len(v) == 64 for v in b.PARENT_ARTIFACTS.values()))

    def test_02_six_exclusive_categories(self):
        examples = [((48,49),"both_correct"),((49,48),"swapped"),((48,48),"collapse_entity0"),
                    ((49,49),"collapse_entity1"),((200,200),"collapse_outside"),((48,200),"other_different")]
        for pred,expected in examples: self.assertEqual(b.pair_class(pred,(48,49)),expected)
        for pred in itertools.product((48,49,50,51,200),repeat=2): self.assertIn(b.pair_class(pred,(48,49)),b.CATEGORIES)

    def test_03_answer_classification(self):
        self.assertEqual([b.answer_class(v,48,49) for v in (48,49,50,200)],list(b.ANSWER_CLASSES))
        with self.assertRaises(ValueError): b.pair_class((48,49),(48,48))
        with self.assertRaises(ValueError): b.pair_class((256,49),(48,49))

    def test_04_query_group_coverage(self):
        groups = b.query_groups(self.rows)
        self.assertEqual(len(groups),144)
        self.assertEqual(sorted(i for _,ids in groups for i in ids),list(range(288)))

    def test_05_missing_or_corrupt_rows_rejected(self):
        for rows in (self.rows[:-1],list(reversed(self.rows))):
            with self.assertRaises(ValueError): b.query_groups(rows)
        bad = copy.deepcopy(self.rows); bad[0]["target"] = 200
        with self.assertRaises(ValueError): b.query_groups(bad)

    def test_06_exact_integer_accounting(self):
        pairs,cells,profiles,contrasts,s = self.outputs
        self.assertEqual((len(pairs),len(cells),len(profiles),len(contrasts)),(8640,720,120,80))
        self.assertEqual(sum(c["answers"] for c in cells),17280)
        self.assertEqual(s["profile_categories"]["doubled"]["both_correct"],2880)
        self.assertEqual(s["profile_categories"]["shared_prefix"]["swapped"],2880)
        self.assertEqual(s["profile_categories"]["shared_suffix"]["collapse_entity0"],2880)

    def test_07_collapse_not_always_first_presented(self):
        cells = [x for x in self.outputs[1] if x["profile"] == "shared_suffix"]
        self.assertEqual(sum(x["selected_first_fact"] for x in cells),1440)
        self.assertEqual(sum(x["selected_last_fact"] for x in cells),1440)
        self.assertTrue(all(x["correct_answers"] == 12 for x in cells))

    def test_08_same_argmax_does_not_mean_same_logits(self):
        rr = copy.deepcopy(self.records); rr[0]["renamed"]["shared_suffix"]["normal"][0,200] += 1
        pairs = b.analyze(rr,self.rows,expected_metrics(rr,self.rows))[0]
        target = next(p for p in pairs if p["seed"] == b.SEEDS[0] and p["arm"] == b.ARMS[0] and p["profile"] == "shared_suffix" and self.rows[0]["id"] in p["row_ids"])
        self.assertEqual(target["category"],"collapse_entity0"); self.assertFalse(target["same_logits"])
        self.assertEqual(target["query_logit_max_abs_difference"],1.)

    def test_09_matched_baseline_transitions(self):
        for c in self.outputs[3]:
            self.assertEqual(c["baseline_both_correct"],72)
            key = "swapped" if c["profile"] == "shared_prefix" else "collapsed"
            self.assertEqual(c["transitions"][key],72)

    def test_10_zero_eligible_baseline_is_null(self):
        rr = copy.deepcopy(self.records)
        for r in rr: r["renamed"]["doubled"] = raw_fixture(self.rows,"outside")
        contrasts = b.analyze(rr,self.rows,expected_metrics(rr,self.rows))[3]
        self.assertTrue(all(c["baseline_both_correct"] == 0 and c["collapse_fraction"] is None for c in contrasts))

    def test_11_absent_digit_and_other_bytes_are_not_discarded(self):
        rr = copy.deepcopy(self.records); x = rr[0]["renamed"]["doubled"]["normal"]
        x[0].fill_(-10); x[0,50] = 10
        x[1].fill_(-10); x[1,200] = 10
        pairs = b.analyze(rr,self.rows,expected_metrics(rr,self.rows))[0]
        q = next(p for p in pairs if p["seed"] == b.SEEDS[0] and p["arm"] == b.ARMS[0] and p["profile"] == "doubled" and self.rows[0]["id"] in p["row_ids"])
        self.assertEqual(q["category"],"other_different")
        self.assertEqual(q["answer_classes"],["absent_digit","other_byte"])

    def test_12_nonfinite_dtype_shape(self):
        x = self.records[0]["renamed"]["doubled"]["normal"]
        for bad in (x.float(),x[:-1],torch.full_like(x,float("nan"))):
            with self.assertRaises(ValueError): b.tensor_check(bad)

    def test_13_masks_validated_even_though_normal_answers_attributed(self):
        rr = copy.deepcopy(self.records); rr[0]["renamed"]["doubled"]["query_blind"][0,0] = float("nan")
        with self.assertRaises(ValueError): b.analyze(rr,self.rows,self.metrics)

    def test_14_parent_totals_and_cells_reconciled(self):
        for level in ("total","cell"):
            metrics = copy.deepcopy(self.metrics)
            if level == "total": metrics[0]["profiles"]["doubled"]["correct"] -= 1
            else: metrics[0]["profiles"]["doubled"]["cells"][0]["query_pair_accuracy"] = 0.
            with self.assertRaises(ValueError): b.analyze(self.records,self.rows,metrics)

    def test_15_no_state_or_profile_selection(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.rows,self.metrics)
        with self.assertRaises(ValueError): b.analyze(list(reversed(self.records)),self.rows,self.metrics)
        rr = copy.deepcopy(self.records); del rr[0]["renamed"]["shared_suffix"]
        with self.assertRaises(ValueError): b.analyze(rr,self.rows,self.metrics)

    def test_16_saved_only_guard_restores_model_calls(self):
        model = torch.nn.Linear(1,1)
        with b.saved_only():
            with self.assertRaises(RuntimeError): model(torch.zeros(1,1))
            with self.assertRaisesRegex(ValueError,"forbidden"): torch.load("trained-models.pt",map_location="cpu",weights_only=True)
            with self.assertRaisesRegex(ValueError,"safe archive"): torch.load("evaluations.pt",weights_only=False)
        self.assertEqual(model(torch.zeros(1,1)).shape,(1,1))

    @contextlib.contextmanager
    def runtime_fixture(self, root):
        p265,p264,p263 = [root/n for n in ("p265.json","p264.json","p263.json")]
        for path in (p265,p264,p263): path.write_bytes(b"synthetic parent")
        torch.save(dict(schema="fold-c265-identifiers-eval-v1",records=self.records),root/"eval-outputs.pt")
        torch.save({},root/"evaluations.pt")
        profile = dict(doubled=dict(zip(b.ARMS,(5,5,3,3))),shared_prefix=dict(zip(b.ARMS,(3,2,0,1))),shared_suffix={a:0 for a in b.ARMS})
        payload = dict(commit_sha=b.PARENT_EXECUTION,status="FAIL",validation_summary=dict(seed_pass_counts={a:0 for a in b.ARMS},profile_pass_counts=profile),artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        def verify(directory,old,source,head):
            self.assertEqual((directory,old,source,head),(root,p264,p263,b.PARENT_EXECUTION))
            # Five synthetic reads stand in for the documented parent's saved verification chain.
            for name in ("eval-outputs.pt",)*3+("evaluations.pt",)*2:
                torch.load(root/name,map_location="cpu",weights_only=True)
            return payload,self.metrics
        parent = SimpleNamespace(validate_result=lambda p:None,verify_artifacts=Mock(side_effect=verify))
        task = SimpleNamespace(dataset=lambda:self.rows)
        with patch.object(b,"context",return_value=(parent,task,Audit)),patch.object(b,"PARENT_SHA",Audit.sha(p265)),patch.object(b,"C264_SHA",Audit.sha(p264)),patch.object(b,"C263_SHA",Audit.sha(p263)):
            yield (p265,p264,p263),parent,payload

    def test_17_actual_four_argument_parent_loader(self):
        with tempfile.TemporaryDirectory() as d:
            with self.runtime_fixture(Path(d)) as (paths,parent,payload):
                with b.saved_only() as loads: records,rows,metrics = b.load_reference(*paths)
                self.assertEqual(len(loads),6); self.assertEqual(rows,self.rows); self.assertEqual(len(records),20)
                parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1],paths[2],b.PARENT_EXECUTION)
                payload["status"] = "PASS"
                with self.assertRaises(ValueError): b.load_reference(*paths)

    def test_18_actual_compute_checks_reference_read_budget(self):
        with tempfile.TemporaryDirectory() as d:
            with self.runtime_fixture(Path(d)) as (paths,parent,payload):
                out = b.compute(*paths); self.assertEqual(out[-1]["eval_archive_reads_per_pass"],6)
                parent.verify_artifacts.side_effect = lambda *a:(payload,self.metrics)
                with self.assertRaisesRegex(ValueError,"archive workload"): b.compute(*paths)

    def test_19_actual_run_and_persisted_recomputation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with self.runtime_fixture(root) as (paths,parent,payload),patch.object(b,"precheck",return_value=protection()) as pre:
                out = root/"out"
                with contextlib.redirect_stdout(io.StringIO()):
                    p = b.run(c265_summary=paths[0],c264_summary=paths[1],c263_summary=paths[2],output_dir=out,expected_head="fixture-head")
                self.assertEqual(pre.call_count,2)
                self.assertEqual(b.verify_artifacts(out,*paths,"fixture-head")[0],p)
                with self.assertRaisesRegex(ValueError,"saved HEAD"): b.verify_artifacts(out,*paths,"wrong")
                (out/"cells.json").write_bytes(b"[]")
                with self.assertRaises(ValueError): b.verify_artifacts(out,*paths,"fixture-head")

    def test_20_same_scores_with_no_collapse_still_diagnostic_pass(self):
        rr = copy.deepcopy(self.records)
        for r in rr:
            for profile in b.PROFILES: r["renamed"][profile] = raw_fixture(self.rows,"correct")
        result = b.analyze(rr,self.rows,expected_metrics(rr,self.rows))[-1]
        self.assertFalse(result["capability_pass_claim"])
        self.assertTrue(all(x["both_correct"] == 2880 for x in result["profile_categories"].values()))

    def test_21_scope_and_partition_guards(self):
        s = copy.deepcopy(self.outputs[-1]); s["eval_archive_reads_per_pass"] = 6
        pins,protected = protection()
        p = dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,status="PASS",diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,
                 artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,capability_pass_claim=False,causal_parser_claim=False,gate_f_candidate=False,production_adoption=False)
        b.validate_result(p)
        with self.assertRaises(ValueError): b.validate_result(dict(p,capability_pass_claim=True))
        s["profile_categories"]["doubled"]["both_correct"] -= 1
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_22_semantic_suite_count_and_exact_exclusion(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases(),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name): super().__init__(); self.name = name
            def id(self): return self.name
        suite = unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture-{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_23_cli_parser_and_source_dispatch(self):
        root = Path(__file__).resolve().parents[1]
        runner = (root/"tools/run_c266.ps1").read_text(encoding="utf-8")
        launcher = (root/"tools/invoke_c266.ps1").read_text(encoding="utf-8")
        blocks = re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3); indices = []
        for text in blocks:
            compile(text,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id == "sys" and n.value.attr == "argv"})
        self.assertEqual(indices,[{1,2,3},set(),{1,2,3,4,5}])
        failure = re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher); self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start()); self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        calls = [(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(b.run))) if isinstance(n,ast.Call)]
        first = lambda name:min(line for line,n in calls if n == name)
        self.assertLess(first("precheck"),first("compute")); self.assertIn("load_reference",inspect.getsource(b.compute))

    def test_24_dependency_range_and_no_training_call(self):
        tree = ast.parse(inspect.getsource(b.precheck))
        pattern = next(n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id == "pattern" for t in n.targets))
        names = ["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,266)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names)); self.assertEqual(5+len(names)+1,42)
        self.assertEqual(736+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),748)
        for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))):
            if isinstance(n,ast.Call):
                name = n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else ""
                self.assertNotIn(name,{"AdamW","backward","fit","train_one","step","load_state_dict","new_model"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
