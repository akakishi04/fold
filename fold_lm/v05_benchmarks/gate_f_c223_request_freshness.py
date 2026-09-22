"""C223: retained-request invalidation over the unchanged frozen C222 lifecycle."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import itertools
import json
from pathlib import Path
import unittest

import torch
from fold_lm.v05 import memory_request_lease as leases

EXPERIMENT_ID = "C223-v5f-retained-request-freshness"
STAGE = "V5-F-RETAINED-REQUEST-FRESHNESS"
BASE = "b2de4593777c23868738c04490aa1b68eb96f076"
PARENT_EXECUTION = "ae4286ac9b79cd34eb8bdfd1d72ae2e27c308889"
PARENT_SHA = "18321ace4ade112fe227d4836867223a5ec609761c89015b704e9e14b629c62e"
PARENT_VALIDATION_SHA = "9d6916dfcaec497680b94ae2b280dc9ab98f3da17aac7447a8b2e8b150d9b40b"
PARENT_PLAN_SHA = "1b94c0af7c1d828f54c5519dd9169a9e2a7985ddd91b155a72d312d39e26a828"
MANIFEST_SHA = "ef0d7db9c3ef24da2076c8811076e53c6d46abeff19b363163a0c352f0d0872d"
PLAN = (
    ("anchor_only",2,None), ("beta_hot",1,2), ("beta_committed",0,2),
    ("beta_replaced",0,0), ("beta_retracted",2,None), ("shadow_assumed",2,None),
    ("shadow_ended",2,None), ("project_ended",3,None),
)
# current snapshot, source of intentionally unguarded old beta request
REPLAYS = ((2,1),(3,2),(4,3),(7,4))
SEED_FAMILIES = ((218001,218002,218003),(219001,219002,219003),
                 (217001,217002,217003),(216001,216002,216003))
OWN = (
    "fold_lm/v05/memory_request_lease.py",
    "fold_lm/v05_benchmarks/gate_f_c223_request_freshness.py",
    "tests_lm/test_v05_c223_request_freshness.py",
    "tools/run_c223.ps1", "tools/invoke_c223.ps1",
    "docs/experiment-ledger-addendum-c223-preregistration.md",
    "docs/v5f-retained-request-freshness-v0.1.md",
)
OUTPUTS = {"freshness-plan.json", "fresh-decisions.json", "stale-decisions.json",
           "replay-controls.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import gate_f_c222_withdrawal_lifecycle as parent
    return parent


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,
                parent_validation_sha256=PARENT_VALIDATION_SHA,parent_plan_sha256=PARENT_PLAN_SHA,
                plan=[list(x) for x in PLAN],replays=[list(x) for x in REPLAYS],
                seed_families=[list(x) for x in SEED_FAMILIES],
                fresh_decisions=1296,stale_decisions=4536,same_generation_repeats=81,
                unguarded_replays=324,session_count=3,publications_per_session=7,
                fresh_calls=dict(coverage=1296,selector=891,provider=891,reader=891,bank_reads=891),
                stale_calls=dict(coverage=0,selector=0,provider=0,reader=0,bank_reads=0),
                repeat_calls=dict(coverage=81,selector=81,provider=81,reader=81,bank_reads=81),
                replay_calls=dict(coverage=324,selector=243,provider=243,reader=243,bank_reads=243),
                writer_forwards=3,successful_model_forwards=4134,new_training_steps=0,
                same_parent_parity_required=True,all_old_leases_rejected=True,
                publication_includes_representation_commit=True,
                monotonic_session_generation=True,answer_cache_added=False,
                concurrent_execution_tested=False,in_place_tensor_mutation_tested=False,
                production_runtime_modified=True,gate_f_candidate=False,
                device="cpu",threads=2,deterministic_algorithms=True)


def expected_result(label,query):
    _,cov,answer = next(row for row in PLAN if row[0] == label)
    if query == "alpha":
        cov,answer = 0,1
    elif query != "beta":
        raise ValueError("unknown query")
    action = "ANSWER" if answer is not None else (
        "SUPPRESS_OUT_OF_SCOPE" if cov == 3 else "SUPPRESS_MISSING")
    trace = ("coverage","selector","provider","reader") if answer is not None else ("coverage",)
    return dict(coverage=cov,answer=answer,action=action,trace=trace,
                bank_reads=1 if answer is not None else 0)


def matches(result,expected):
    return result is not None and all(getattr(result,key) == value for key,value in expected.items())


def parent_answers(rows):
    """Validate actual C222 decision fields; return a scorer-only parity map."""
    require(isinstance(rows,list) and len(rows) == 1296,"parent decision count")
    combinations = set(itertools.product(*SEED_FAMILIES))
    names = ("writer_seed","coverage_seed","selector_seed","reader_seed")
    result = {}
    for row in rows:
        seeds = tuple(row[name] for name in names)
        label,query = row["label"],row["query"]
        require(seeds in combinations,"parent seed identity")
        expected = expected_result(label,query)
        key = seeds+(label,query)
        require(key not in result and row["success"] is True,"parent duplicate/failed row")
        for field,value in expected.items():
            got = tuple(row[field]) if field == "trace" else row[field]
            require(got == value,"parent decision semantics:"+field)
        result[key] = expected
    require(len(result) == 1296,"incomplete parent matrix")
    return result


def counts(rows):
    counter = Counter()
    for row in rows:
        counter.update(row["trace"])
        counter["bank_reads"] += row["bank_reads"]
    return {key:counter[key] for key in ("coverage","selector","provider","reader","bank_reads")}


def evaluate(factory,models,snapshots,baseline):
    """Execute leases first. The parent labels/answers are used only by the following scorer."""
    fresh,stale,repeats,replays = [],[],[],[]
    names = ("writer_seed","coverage_seed","selector_seed","reader_seed")
    for ws in SEED_FAMILIES[0]:
        rows = snapshots[ws]
        require(len(rows) == 8 and [r[0] for r in rows] == [p[0] for p in PLAN],"timeline identity")
        session = leases.RequestSession(rows[0][1:],factory)
        retained = []
        for index,(label,bank,state) in enumerate(rows):
            if index:
                session.publish((bank,state))
            current = {query:session.bind(query) for query in ("alpha","beta")}
            for cs,ss,rs in itertools.product(*SEED_FAMILIES[1:]):
                seeds = (ws,cs,ss,rs)
                context = dict(zip(names,seeds,strict=True))
                components = (models["coverage"][cs],models["selector"][ss],models["reader"][rs])
                for query,ticket in current.items():
                    outcome = session.execute(ticket,*components)
                    expected = baseline[seeds+(label,query)]
                    ok = outcome.status == "CURRENT" and matches(outcome.result,expected)
                    fresh.append(dict(context,label=label,query=query,success=bool(ok),
                                      parent_parity=matches(outcome.result,expected),**asdict(outcome)))
                for old_index,old_tickets in enumerate(retained):
                    for query,ticket in old_tickets.items():
                        outcome = session.execute(ticket,*components)
                        ok = (outcome.status == "STALE_REQUEST" and outcome.result is None
                              and outcome.trace == ("freshness",) and outcome.bank_reads == 0)
                        stale.append(dict(context,label=label,source=PLAN[old_index][0],query=query,
                                          success=bool(ok),**asdict(outcome)))
                if index == 2:
                    outcome = session.execute(current["beta"],*components)
                    ok = outcome.status == "CURRENT" and matches(outcome.result,baseline[seeds+(label,"beta")])
                    repeats.append(dict(context,label=label,success=bool(ok),**asdict(outcome)))
                for current_index,old_index in REPLAYS:
                    if index != current_index:
                        continue
                    # Negative control bypasses only the new lease guard; uses real old provider closure.
                    result = leases.live.dispatch_query(retained[old_index]["beta"].request,*components)
                    old = baseline[seeds+(PLAN[old_index][0],"beta")]
                    now = baseline[seeds+(label,"beta")]
                    ok = matches(result,old) and not matches(result,now)
                    replays.append(dict(context,label=label,source=PLAN[old_index][0],
                                        reproduced_old=matches(result,old),differs_current=not matches(result,now),
                                        success=bool(ok),**asdict(result)))
            retained.append(current)
    return fresh,stale,repeats,replays


def summarize(fresh,stale,repeats,replays,writer_accuracy,unchanged):
    groups = dict(fresh=fresh,stale=stale,repeat=repeats,replay=replays)
    summary = dict(writer_target_accuracy=writer_accuracy,fingerprints_unchanged=unchanged,
                   new_training_steps=0,writer_forward_calls=3)
    for name,rows in groups.items():
        summary[name+"_decisions"] = len(rows)
        summary[name+"_success"] = sum(r["success"] for r in rows)
        summary[name+"_calls"] = counts(rows)
    summary["parent_parity"] = sum(r["parent_parity"] for r in fresh)
    summary["stale_result_exposures"] = sum(r["result"] is not None for r in stale)
    summary["model_forward_calls"] = 3+sum(summary[n+"_calls"][k]
        for n in groups for k in ("coverage","selector","reader"))
    return summary


def gate(s):
    return (all(s.get(n+"_decisions") == s.get(n+"_success") == count
                for n,count in (("fresh",1296),("stale",4536),("repeat",81),("replay",324)))
            and s.get("parent_parity") == 1296 and s.get("stale_result_exposures") == 0
            and all(s.get(n+"_calls") == manifest()[n+"_calls"]
                    for n in ("fresh","stale","repeat","replay"))
            and s.get("writer_target_accuracy") == 1.0 and s.get("fingerprints_unchanged") is True
            and s.get("model_forward_calls") == 4134 and s.get("new_training_steps") == 0)


def precheck(c222_summary,root):
    pmod = parent_module()
    base = pmod.parent_module().parent_module()
    a = base.audit
    root = Path(root)
    require(a.sha(c222_summary) == PARENT_SHA,"C222 summary changed")
    parent = a.read_json(c222_summary)
    pmod.validate_result(parent)
    require(parent["commit_sha"] == PARENT_EXECUTION and parent["status"] == "PASS"
            and pmod.gate(parent["validation_summary"]),"wrong accepted C222")
    require(tuple(row[:3] for row in pmod.PLAN) == PLAN and pmod.MANIFEST_SHA == PARENT_PLAN_SHA,
            "parent trajectory changed")
    require(len(parent["source_blobs"]) == 171 and len(parent["input_sha256"]) == 207,"parent coverage")
    pins,protected = dict(parent["source_blobs"]),dict(parent["input_sha256"])
    for path,wanted in protected.items():
        require(Path(path).is_file() and a.sha(path) == wanted,"changed inherited input:"+path)
    for path,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip() == wanted,"changed parent source:"+path)
    protected[str(Path(c222_summary).resolve())] = PARENT_SHA
    validation_seen = False
    for artifact in parent["artifacts"]:
        path = a.safe_child(Path(c222_summary).resolve().parent,artifact["file"])
        require(path.is_file() and a.sha(path) == artifact["sha256"]
                and path.stat().st_size == artifact["serialized_bytes"],"parent artifact changed")
        protected[str(path.resolve())] = artifact["sha256"]
        if artifact["file"] == "validation-summary.json":
            require(artifact["sha256"] == PARENT_VALIDATION_SHA,"parent validation changed")
            validation_seen = True
    require(validation_seen,"parent validation missing")
    for path in OWN:
        require(path not in pins,"OWN collides with accepted source")
        pins[path] = a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    dependencies = tuple(base.DIRECT_REPO_DEPENDENCIES)+(
        "fold_lm/v05_benchmarks/gate_f_c220_frozen_learned_stack.py",
        "fold_lm/v05/memory_dispatch.py",
        "fold_lm/v05_benchmarks/gate_f_c221_live_coverage_dispatch.py",
        "fold_lm/v05_benchmarks/gate_f_c222_withdrawal_lifecycle.py",OWN[0])
    require(len(dependencies) == 19 and all(path in pins for path in dependencies),"unpinned dependency")
    protected.update(a.protect_tree_files(root,pins))
    require(len(pins) == 178 and len(protected) == 220,"C223 protection counts")
    require(digest(manifest()) == MANIFEST_SHA,"C223 manifest drift")
    return parent,pins,protected


def regression_modules(root):
    names = parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 107,"parent module count")
    return names+["tests_lm.test_v05_c223_request_freshness"]


def regression_suite(root):
    helper = parent_module().parent_module().parent_module().c205
    loaded = unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))
    tests = list(helper._iter_tests(loaded))
    excluded = helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    ids = [test.id() for test in tests]
    require(all(ids.count(x) == 1 for x in excluded),"historical exclusion identity")
    kept = [test for test in tests if test.id() not in excluded]
    require(len(tests) == 2436 and len(kept) == 2435,"C223 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE
            and p["diagnostic_execution_valid"] is True,"C223 result identity")
    require(len(p["source_blobs"]) == 178 and len(p["input_sha256"]) == 220
            and len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS,"C223 coverage")
    s = p["validation_summary"]
    require(all(s[n+"_decisions"] == count for n,count in
                (("fresh",1296),("stale",4536),("repeat",81),("replay",324))),"incomplete C223")
    require(p["status"] == ("PASS" if gate(s) else "FAIL"),"C223 verdict drift")
    require(s["new_training_steps"] == 0 and p["gate_f_candidate"] is False
            and p["network_calls"] == 0,"scope drift")


def run(*,c222_summary,output_dir,expected_head):
    pmod = parent_module()
    dispatch = pmod.parent_module()
    base = dispatch.parent_module()
    a = base.audit
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard()
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    parent,pins,protected = precheck(c222_summary,root)
    baseline = parent_answers(a.read_json(Path(c222_summary).resolve().parent/"live-decisions.json"))
    coverage_parent = base.find_protected_input(parent,"summary.json",base.PARENT_C219_SHA)
    models = dict(writer=base.restore_writer_models(parent),
                  coverage=base.restore_coverage_models(parent,coverage_parent),
                  selector=base.restore_selector_models(parent),reader=base.restore_reader_models(parent))
    hashers = dict(writer=base.c218.model_sha,coverage=base.c219.model_sha,
                   selector=base.c217.model_sha,reader=base.c216.model_sha)
    def fingerprints():
        return {family:{str(seed):hashers[family](model) for seed,model in group.items()}
                for family,group in models.items()}
    before = fingerprints()
    predictions,forwards,writer_accuracy = base.frozen_writer_predictions(models["writer"])
    require(forwards == 3,"Writer forward count")
    snapshots = {seed:list(pmod.timeline(base,predictions[seed],seed)) for seed in SEED_FAMILIES[0]}
    def factory(pair,query):
        bank,state = pair
        return dispatch.request_for(base,bank,state,query)
    fresh,stale,repeats,replays = evaluate(factory,models,snapshots,baseline)
    after = fingerprints()
    summary = summarize(fresh,stale,repeats,replays,writer_accuracy,before == after)
    out = Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts = []
    for name,value in (("freshness-plan.json",manifest()),("fresh-decisions.json",fresh),
                       ("stale-decisions.json",stale),
                       ("replay-controls.json",dict(same_generation=repeats,unguarded=replays,
                                                   fingerprints_before=before,fingerprints_after=after)),
                       ("validation-summary.json",summary)):
        path = out/name
        path.write_bytes(blob(value))
        artifacts.append(dict(file=name,sha256=a.sha(path),serialized_bytes=path.stat().st_size))
    guard()
    precheck(c222_summary,root)
    for path,wanted in protected.items():
        require(a.sha(path) == wanted,"input modified:"+path)
    result = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
                  status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,
                  C222_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,
                  artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,network_calls=0,
                  limitations=["same synthetic C222 trajectory, not independent unseen tasks",
                               "state changes must use explicit session publication",
                               "no answer cache, concurrent safety, in-place tensor mutation or malicious bypass claim",
                               "oracle operations; frozen models; no acquisition or memory-cost comparison"])
    validate_result(result)
    (out/"summary.json").write_bytes(blob(result))
    print("=== C223 RESULT ===",flush=True)
    print(blob(result).decode(),flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("c222-summary","output-dir"):
        parser.add_argument("--"+arg,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
