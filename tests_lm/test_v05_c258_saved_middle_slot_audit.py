"""Synthetic saved-output fixtures validate C258 authoring, not learned capability."""
import ast
import contextlib
import copy
import hashlib
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
from fold_lm.v05_benchmarks import model_c258_saved_middle_slot_audit as b


def dataset():
    train = {(0,1,2),(0,1,3),(0,2,1),(1,0,2),(1,0,3),(1,3,0),(2,0,3),(2,3,0),(2,3,1),(3,1,2),(3,2,0),(3,2,1)}
    parts = {s:[] for s in b.SPLITS}
    for assignment in itertools.permutations(range(4),3):
        split = "TRAIN" if assignment in train else "HOLDOUT"
        for lang,names in (("en",("a","b","c")),("ja",("甲","乙","丙"))):
            for order,perm in enumerate(b.KNOWN):
                for query in range(3):
                    parts[split].append(dict(id=f"{lang}-{assignment[0]}{assignment[1]}{assignment[2]}-{order}-{query}",
                        assignment=list(assignment),language=lang,order=order,query=query,target=48+assignment[query],
                        prompt=";".join(names[i]+"="+str(assignment[i]) for i in perm)+";"+names[query]+"="))
    return parts


class Parent:
    @staticmethod
    def novel_dataset(parts):
        result={s:[] for s in b.SPLITS}
        for split in b.SPLITS:
            for old in parts[split]:
                if old["order"] != 0:continue
                for perm in b.NOVEL:
                    row=dict(source_id=old["id"],id=old["id"]+":"+"".join(map(str,perm)),
                        assignment=list(old["assignment"]),language=old["language"],query=old["query"],target=old["target"],permutation=list(perm))
                    names=("a","b","c") if row["language"]=="en" else ("甲","乙","丙")
                    row["prompt"]=";".join(names[i]+"="+str(row["assignment"][i]) for i in perm)+";"+names[row["query"]]+"="
                    result[split].append(row)
        return result
    @staticmethod
    def check_logits(value,rows):
        b.require(value.shape==(rows,256) and value.dtype==torch.float64 and value.device.type=="cpu" and bool(torch.isfinite(value).all()),"logits")
    @staticmethod
    def validate_result(value):
        b.require(value["experiment_id"]=="C257-v5b-unseen-fact-order-transfer","parent identity")


class Audit:
    @staticmethod
    def sha(path):
        if str(path).startswith("synthetic-input-"):return "0"*64
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):
        path=(Path(root)/name).resolve()
        b.require(path.parent==Path(root).resolve(),"unsafe child")
        return path
    @staticmethod
    def git(root,*args):
        if args==("rev-parse","HEAD"):return b"synthetic-head"
        if args==("branch","--show-current"):return b"feat/sft-target-loss"
        return b""


def records(parts,novel,mode="perfect"):
    out=[]
    for seed,arm in b.identities():
        values={stage:{} for stage in ("anchor","novel")}
        for split in b.SPLITS:
            for stage,rows in (("anchor",parts[split]),("novel",novel[split])):
                logits=torch.full((len(rows),256),-10.,dtype=torch.float64)
                for i,r in enumerate(rows):
                    prediction=r["target"]
                    if stage=="novel" and r["query"]==1:
                        if mode=="middle":prediction=48+r["assignment"][r["permutation"][1]]
                        if mode=="other":prediction=48+r["assignment"][next(x for x in r["permutation"] if x not in (1,r["permutation"][1]))]
                    logits[i,prediction]=10.
                values[stage][split]={"normal":logits}
        out.append(dict(seed=seed,arm=arm,outputs=values))
    return out


def protection():
    return ({**{f"old-{i}":"fixture" for i in range(388)},**{n:"fixture" for n in b.OWN}},
            {f"synthetic-input-{i}":"0"*64 for i in range(647)})


class C258Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2);cls.parts=dataset();cls.novel=Parent.novel_dataset(cls.parts)
        cls.records=records(cls.parts,cls.novel)
        cls.perfect=b.attribution(cls.parts,cls.novel,cls.records,Parent)

    def test_01_hashes(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.digest(self.parts),"ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b")
        self.assertEqual(b.digest(self.novel),b.PARENT_ARTIFACTS["order-dataset.json"])
        with contextlib.redirect_stdout(io.StringIO()):
            b.validate_registration(394,647)
            with self.assertRaises(ValueError):b.validate_registration(393,647)
            with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError):b.validate_registration(394,647)

    def test_02_correct_classification(self):
        for a in itertools.permutations(range(4),3):
            for perm in b.KNOWN+b.NOVEL:
                for q in range(3):
                    v=b.classify(list(a),q,perm,48+a[q]);self.assertEqual(v["kind"],"correct")
                    self.assertEqual(v["predicted_entity"],q);self.assertEqual(v["query_position"],perm.index(q))
                    self.assertFalse(v["middle_wrong"])

    def test_03_wrong_displayed_entity(self):
        value=b.classify([2,0,3],1,(0,2,1),51)
        self.assertEqual((value["kind"],value["predicted_entity"],value["predicted_position"]),("other_entity",2,1))
        self.assertTrue(value["middle_wrong"])

    def test_04_absent_value_and_other_byte(self):
        a=b.classify([2,0,3],1,(0,2,1),49);c=b.classify([2,0,3],1,(0,2,1),97)
        self.assertEqual(a["kind"],"absent_value");self.assertIsNone(a["predicted_entity"])
        self.assertEqual(c["kind"],"other_byte");self.assertIsNone(c["predicted_position"])

    def test_05_bad_row_inputs(self):
        for args in (([0,0,1],1,(0,1,2),48),([0,1,2],3,(0,1,2),48),([0,1,2],1,(0,0,2),48),([0,1,2],1,(0,1,2),True)):
            with self.assertRaises(ValueError):b.classify(*args)

    def test_06_complete_cells_and_counts(self):
        out=self.perfect;self.assertEqual(len(out["row-attribution.json"]),8640)
        self.assertEqual(len(out["query-position-cells.json"]["order_query"]),720)
        for c in out["query-position-cells.json"]["order_query"]:
            self.assertEqual((c["rows"],c["correct"]),(12,12));self.assertEqual(sum(c[k] for k in b.KINDS),12)
        self.assertEqual(len(out["query-position-cells.json"]["query"]),120)

    def test_07_zero_denominator_is_null(self):
        for s in self.perfect["signature-summary.json"]:
            self.assertIsNone(s["middle_share_of_b_errors"]);self.assertIsNone(s["middle_share_of_in_assignment_b_errors"])
            self.assertEqual(s["b_errors"],0)
        self.assertEqual(json.loads(b.blob({"ratio":b.ratio(0,0)})),{"ratio":None})

    def test_08_middle_shortcut_signature(self):
        result=b.attribution(self.parts,self.novel,records(self.parts,self.novel,"middle"),Parent)
        for s in result["signature-summary.json"]:
            self.assertEqual((s["b_error_rate"],s["ac_error_rate"],s["middle_distractor_errors"]),(1.,0.,48))
            self.assertEqual(s["other_distractor_errors"],0);self.assertEqual(s["middle_share_of_b_errors"],1.)
            self.assertEqual(s["known_both_correct_to_wrong"],48)

    def test_09_other_distractor_not_middle(self):
        result=b.attribution(self.parts,self.novel,records(self.parts,self.novel,"other"),Parent)
        for s in result["signature-summary.json"]:
            self.assertEqual((s["middle_distractor_errors"],s["other_distractor_errors"]),(0,48))
            self.assertEqual(s["middle_minus_other"],-48)

    def test_10_external_byte_not_displayed_entity(self):
        copied=copy.deepcopy(self.records);rows=self.novel["TRAIN"]
        i=next(i for i,r in enumerate(rows) if r["query"]==1 and r["language"]=="en")
        copied[0]["outputs"]["novel"]["TRAIN"]["normal"][i]=-10.
        copied[0]["outputs"]["novel"]["TRAIN"]["normal"][i,200]=10.
        s=b.attribution(self.parts,self.novel,copied,Parent)["signature-summary.json"][0]
        self.assertEqual((s["b_errors"],s["other_byte_errors"],s["middle_distractor_errors"]),(1,1,0))
        self.assertIsNone(s["middle_share_of_in_assignment_b_errors"])

    def test_11_known_pair_baseline(self):
        copied=copy.deepcopy(self.records);row=self.parts["TRAIN"][0]
        copied[0]["outputs"]["anchor"]["TRAIN"]["normal"][0]=-10.;copied[0]["outputs"]["anchor"]["TRAIN"]["normal"][0,200]=10.
        values=b.attribution(self.parts,self.novel,copied,Parent)["row-attribution.json"]
        matched=[r for r in values if r["seed"]==b.SEEDS[0] and r["arm"]==b.ARMS[0] and r["split"]=="TRAIN" and r["phase"]=="novel" and r["language"]==row["language"] and r["assignment"]==row["assignment"] and r["query"]==row["query"]]
        self.assertEqual(len(matched),4);self.assertTrue(all(r["known_both_correct"] is False for r in matched))

    def test_12_identity_and_nonfinite_guards(self):
        with self.assertRaises(ValueError):b.attribution(self.parts,self.novel,self.records[:-1],Parent)
        copied=copy.deepcopy(self.records);copied[0]["outputs"]["novel"]["TRAIN"]["normal"][0,0]=float("nan")
        with self.assertRaises(ValueError):b.attribution(self.parts,self.novel,copied,Parent)
        altered=copy.deepcopy(self.novel);altered["TRAIN"][0]["target"]=200
        with self.assertRaises(ValueError):b.attribution(self.parts,altered,self.records,Parent)

    def test_13_accepts_negative_parent_not_pass(self):
        p=dict(experiment_id="C257-v5b-unseen-fact-order-transfer",commit_sha=b.PARENT_EXECUTION,status="FAIL",
               validation_summary={"seed_pass_counts":{b.ARMS[0]:2,b.ARMS[1]:0}},artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        b.validate_parent(p,Parent)
        with self.assertRaises(ValueError):b.validate_parent(dict(p,status="PASS"),Parent)
        with self.assertRaises(ValueError):b.validate_parent(dict(p,commit_sha="wrong"),Parent)

    def loader_fixture(self,d):
        root=Path(d);summary={"seed_pass_counts":{b.ARMS[0]:2,b.ARMS[1]:0}};measurements=[{"synthetic":True}]
        parent=SimpleNamespace(validate_result=Parent.validate_result,load_inputs=Mock(return_value=(self.parts,[])),
            analyze=Mock(return_value=(measurements,summary)),manifest=lambda:{"synthetic":True})
        for name,value in (("order-dataset.json",self.novel),("measurements.json",measurements),("validation-summary.json",summary),("order-plan.json",parent.manifest())):
            (root/name).write_bytes(b.blob(value))
        torch.save(dict(schema="fold-c257-order-eval-v1",records=self.records),root/"eval-outputs.pt")
        artifacts=[dict(file=n,sha256=Audit.sha(root/n),serialized_bytes=(root/n).stat().st_size) for n in b.PARENT_ARTIFACTS]
        payload=dict(experiment_id="C257-v5b-unseen-fact-order-transfer",commit_sha=b.PARENT_EXECUTION,status="FAIL",validation_summary=summary,artifacts=artifacts)
        (root/"summary.json").write_bytes(b.blob(payload))
        return root,parent,payload

    def test_14_loader_replays_actual_interface_once(self):
        with tempfile.TemporaryDirectory() as d:
            root,parent,payload=self.loader_fixture(d)
            with patch.object(b,"context",return_value=(parent,"previous",None,Audit)),patch.object(b,"PARENT_SHA",Audit.sha(root/"summary.json")),patch.object(b,"PARENT_ARTIFACTS",{a["file"]:a["sha256"] for a in payload["artifacts"]}),patch.object(torch,"load",wraps=torch.load) as load:
                parts,novel,result=b.load_saved(root/"summary.json",root/"c256.json")
                self.assertEqual((parts,novel),(self.parts,self.novel));self.assertEqual(len(result),10)
                load.assert_called_once_with(root/"eval-outputs.pt",map_location="cpu",weights_only=True)
                parent.load_inputs.assert_called_once_with(root/"c256.json")
                self.assertEqual(parent.analyze.call_args.args[4],"previous")

    def test_15_loader_rejects_replay_and_schema(self):
        with tempfile.TemporaryDirectory() as d:
            root,parent,payload=self.loader_fixture(d)
            with patch.object(b,"context",return_value=(parent,"previous",None,Audit)),patch.object(b,"PARENT_SHA",Audit.sha(root/"summary.json")),patch.object(b,"PARENT_ARTIFACTS",{a["file"]:a["sha256"] for a in payload["artifacts"]}):
                parent.analyze.return_value=([],{})
                with self.assertRaisesRegex(ValueError,"parent summary replay"):b.load_saved(root/"summary.json",root/"c256.json")
                with patch.object(torch,"load",return_value={"schema":"wrong","records":[]}),self.assertRaisesRegex(ValueError,"archive schema"):
                    b.load_saved(root/"summary.json",root/"c256.json")

    def test_16_no_model_calls_guard_restored(self):
        model=torch.nn.Linear(1,1);x=torch.zeros(1,1)
        with b.no_model_calls():
            with self.assertRaisesRegex(RuntimeError,"forbids model"):model(x)
        self.assertEqual(tuple(model(x).shape),(1,1))

    def test_17_actual_run_saved_postcheck_and_scope(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,"context",return_value=(Parent,None,None,Audit)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_saved",return_value=(self.parts,self.novel,self.records)) as load:
            root=Path(d);out=root/"output"
            with contextlib.redirect_stdout(io.StringIO()):p=b.run(c257_summary=root/"c257.json",c256_summary=root/"c256.json",output_dir=out,expected_head="synthetic-head")
            self.assertEqual(load.call_count,1)
            got,s=b.verify_artifacts(out,root/"c257.json",root/"c256.json","synthetic-head")
            self.assertEqual(got,p);self.assertEqual(load.call_count,2);self.assertEqual(len(s),40)
            with self.assertRaisesRegex(ValueError,"saved HEAD"):b.verify_artifacts(out,root/"c257.json",root/"c256.json","wrong")
            with self.assertRaises(ValueError):b.validate_result(dict(p,causal_mechanism_claim=True))
            (out/"row-attribution.json").write_bytes(b"[]")
            with self.assertRaises(ValueError):b.verify_artifacts(out,root/"c257.json",root/"c256.json","synthetic-head")

    def test_18_semantic_test_count_and_historical_filter(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(type(self));self.assertEqual(suite.countTestCases(),b.manifest()["own_tests"])
        class Dummy(unittest.TestCase):
            def __init__(self,name):super().__init__();self.name=name
            def id(self):return self.name
        source=unittest.TestSuite([Dummy(b.EXCLUDED)]+[Dummy(f"fixture{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=source):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),b.manifest()["focused_tests"])

    def test_19_runner_indices_and_launcher_order(self):
        root=Path(__file__).resolve().parents[1];runner=(root/"tools/run_c258.ps1").read_text();launcher=(root/"tools/invoke_c258.ps1").read_text()
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        indices=[]
        for block in blocks:
            compile(block,"embedded","exec")
            indices.append({n.slice.value for n in ast.walk(ast.parse(block)) if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Name) and n.value.value.id=="sys" and n.value.attr=="argv"})
        self.assertEqual(indices,[{1,2},set(),{1,2,3,4}])
        failure=re.search(r"(?m)^\s*\$failure\s*=\s*\$null\s*$",launcher);self.assertIsNotNone(failure)
        self.assertLess(launcher.index("::ParseFile"),failure.start());self.assertLess(launcher.index("STALE_EXPECTED_HEAD"),failure.start())
        self.assertIn("705d486739b44a56bbed34fae66ace89",launcher);self.assertIn("3f95a0d190e4424f91634cb8813d7987",launcher)

    def test_20_source_call_order_no_training(self):
        import inspect
        for function in (b.run,b.verify_artifacts):
            calls=[(n.lineno,n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else "") for n in ast.walk(ast.parse(inspect.getsource(function))) if isinstance(n,ast.Call)]
            first=lambda name:min(line for line,n in calls if n==name)
            self.assertLess(first("load_saved"),first("attribution"))
            self.assertLess(first("no_model_calls"),first("load_saved"))
        source=ast.parse(Path(b.__file__).read_text())
        for n in ast.walk(source):
            if isinstance(n,ast.Call):
                name=n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else ""
                self.assertNotIn(name,{"new_model","make_model","fit","train_one","backward","AdamW","load_state_dict","load_bundle"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
