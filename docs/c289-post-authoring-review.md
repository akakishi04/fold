# C289 committed-byte post-authoring review

Review target:2058969f7f37ef63e117f17939dbd75c729776d7.
Acceptance base:4acd3873a4f524ceb3080aab10653cd13caaa1c4.
post_authoring_review=PASS (committed-byte/static plus executed local fixture own48).
Authoritative Windows runtime gate:PENDING.

## Remote identity and mutation boundary

GitHub compare from the acceptance base to the review target reports exactly6 added OWN files.
No accepted source,test,preregistration,dispatcher or published log was changed by C289 authoring.
All6 committed files were fetched back. The source and tests were read in successive complete
ranges;whole-file Git blob identities were compared with the complete local UTF-8 files used
for compilation and tests. All6 identities match. No NUL bytes were found.

|file|Git blob|bytes|
|---|---|---:|
|fold_lm/v05_benchmarks/model_c289_early_pair_withdrawal.py|d5e2231d1d1a1e39b5628129f3ca2ef9838c9951|29639|
|tests_lm/test_v05_c289_early_pair_withdrawal.py|e4359955704165382dc23e435933a61900bc7364|29807|
|tools/run_c289.ps1|b56af787f4646cb3885ea6cda969dd56fecb23b3|5687|
|tools/invoke_c289.ps1|56e3055ac81fbe0baffe3b6c8a3f29f01715f0fe|4940|
|docs/experiment-ledger-addendum-c289-preregistration.md|8b558fbffa4de3f3bcbfff4a10e9d2eeb96719e6|8703|
|docs/v5b-early-pair-withdrawal-v0.1.md|cf4ed27913aaa293a9ee925ba2fa8fe220d6eabd|1971|

Manifest recomputed from manifest():48b33a7ed29cf9ded858753d5f64210006f559ef428c167e912621a71896ae21.
Valid,malformed and mismatched seal execution tests pass. Only the manifest assignment was sealed;
no global sentinel replacement was used. Both Python files and3 embedded runner Python blocks
compile. Recursive Python symbol-table analysis found0 unresolved referenced global names in each
new Python file. The benchmark's only direct repository import is the pinned C288 module.

## Executed local behavioral tests

Environment:Linux,Python3.13.5,PyTorch2.10.0+cpu.
Initial local own48:Ran48 tests in9.143s;OK.
After matching all6 remote identities:Ran48 tests in8.483s;OK.

The test class executes the actual C289.fit loop for800 AdamW updates on a small query-conditioned
toy model for EACH of the3 arms. Instrumented AdamW creations and internal step counters confirm
one optimizer per arm and uninterrupted steps1..800,including400/401. Actual LR histories remain
.005. Actual auxiliary weight history is0 throughout,always.25,or.25 for400 then0 for400.
Always/early first400 CE,pair,total histories and step400 state fingerprints match exactly;their
final toy states diverge. This is not actual FOLD training or a C289 scientific result.

Further executed checks cover analytic objective values,autograd versus finite differences,
disabled auxiliary exact CE value/gradient,correct-versus-swapped score behavior,absence of an
individual-accuracy guarantee,intact query pairs and complete epoch coverage,per-length exposures,
fresh-seed reproducibility,three matched independent initial states,precision/capacity failures,
target alignment before optimizer construction,nonfinite rejection,trace tampering,group and
prefix mismatches,absolute candidate versus comparator gate semantics,90 partitions/360 contrasts,
all15 independent parent hashes,exact parent verifier dispatch and forbidden parent neural/state/
write operations,temporary source/input protection maps and missing-dependency rejection,
real suite construction/filtering,train-freeze-evaluate ordering,15-state run/persistence/replay
ordering,no overwrite,output hash and semantic tampering,checkpoint schemas,CLI parsing and guards.

Tests use mocked ancestral archives,Git,full-size models and scorers outside the toy optimizer
checks. They do not establish real inherited runtime compatibility or actual C289 performance.

## Parent contract and deciding-path dependency audit

C289.load_parent dispatches C288.verify_artifacts(parent_dir,fourteen ancestor paths,accepted
execution HEAD). C288 is an8-artifact capability experiment,not a diagnostic/checkpoint adapter.
The saved raw archive is task-keyed two_char/triple/quad. C288 owns reconstruction of its original
objective histories and matched initial/data/LR;C289 separately validates the exact published
10 parent seed records,quad3/1 and TRAIN direct3/5,FAIL and successful replay flags.
All15 summary hashes and all8 artifact hashes/sizes match the published C288 evidence and acceptance.
The parent source pin is f7f9c73565828e23533efd188f25009e5e4b3d50. Parent verification blocks
Module calls,load_state_dict and torch.save. No parent weights are used to initialize new models.

C288.context provides C287.normalize_task/partition,C284.evaluate/replay_one,C283.score_quad and
C282.training_tables plus C278/C269/C267/core/base/reader/factory/audit helpers. C289 does not call
an inherited identity-bound analyze on its new records. New schedule,objective weights,common-prefix
checks,15-state bundle schemas and result validation are owned by C289. Reachable helpers stay
covered by inherited source/protection maps. dependency-union65;source580=574+6;protected1041=
1026+9 new parent inputs+6 OWN. The dependency test rejects a missing direct parent pin.

## Scientific and operational consistency

Three fresh arms per seed are ce_only,pair_always,pair_early. All models retain14256 parameters,
48-token context,normal mixed2/3 examples,800 updates and constantLR.005. Only always/early have a
common first400 objective;the CE anchor is not incorrectly required to match their midpoint.
Switch applies before update401. AdamW is not recreated. No intermediate checkpoint or extra
forward is introduced. The objective preserves C288's correct-minus-swapped operation grouping;
authoritative Validate additionally compares both objectives on identical synthetic logits.

Per model881 training/evaluation forwards and81 replay;15 models yield14430 forwards,809280 row
presentations,57720 core calls,12000 updates and576000 training rows. One15-state bundle write/load,
15 strict state loads. Candidate absolute gate uses only all5 pair_early quad results. All3 arms'
full task and fitting/HOLDOUT counts and both named comparator contrasts remain visible.
Postcheck reconstructs all scores,objective traces,schedules and exact auxiliary prefixes.

Runner has15 summary arguments. Postcheck uses paths=sys.argv[2:17],head=sys.argv[17],len(argv)=18.
There are exactly3 embedded Python blocks and15 concrete ancestor summary paths in the launcher.
Own48;modules174;loaded4206;focused4205;sole inherited exact C204 exclusion unchanged. Suite tests
construct actual synthetic suites and compare IDs;counts are not inferred from source literals.
Launcher guards branch,tracked tree,ExpectedHead and unique ACTIVE C289 before logging/publish.
Validate precedes Execute;Validate failure returns before publisher. Dispatcher parses itself and
selected launcher;selected launcher parses the runner. C289 publication path/ID is explicit.

## Runtime boundary and activation

PowerShell is not installed in the review environment,so actual ParseFile is NOT claimed executed.
Actual inherited archives,real initial model/table construction,objective-equivalence preflight,
full focused4205,Windows PowerShell parsing and15-model science remain user-local mandatory gates.
Do not describe local fixture success as any of these completed runtime steps.

Activate only through a documentation-only commit containing this review and the authoritative
handoff. Do not change the reviewed OWN6 at activation. Gate F stays NOT PASSED;C290 is unregistered.
