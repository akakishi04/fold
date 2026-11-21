# C221 preregistration — live Coverage dispatch

**C220 ACCEPTED PASS. C221 ACTIVE / NOT YET JUDGED. C222 NOT REGISTERED.**
Gate E PASSED. Gate F NOT PASSED.

## Scientific question and one changed condition

Can Coverage-first live dispatch preserve the same frozen C220 stack outcomes while actually
controlling downstream invocation, without receiving expected labels or precomputed Reader answers?

Change only deterministic dispatch/order and its explicit provider precondition boundary.
Keep all accepted checkpoints, all eight episode shapes and all81 checkpoint combinations fixed.
No training, new tasks, acquisition, RETRACT/ASSUME or cost optimization.

## Accepted parent

Scientific HEAD: `6bc455fa377ec9d3c70d6d1f0922c00680fd5a04`.
Published log commit: `e194716393249373a7d1f6ab552860e851ea84d0`.
Summary SHA256: `45821b372bf0108e667274e2facd73b1f0a84f515a7d036e73874d9238fff5f7`.
Validation artifact SHA256: `f17175ab1f914df65a28014fbc2571c32cbeeade583ad7f38093a17a24c458cd`.
Episode plan SHA256: `99f84e9d05327c8c483b45928676009f6be198e5d568a285d2e893e1279e144f`.

Local summary:
`runs/c220-v5f-frozen-learned-stack-5bc9d133c96348de81a24d19b3ef6f93/summary.json`.

Parent source pins158; inherited protected inputs182. Validate all parent outputs and protect the
parent combination-results artifact used only by the scorer. Resolve all four frozen checkpoint
families through the accepted parent's protected-input chain and reuse its fingerprint-checked
restoration helpers. No checkpoint files are committed to Git.

C220 acceptance and the identified offline-composition limitation:
`docs/experiment-ledger-addendum-c220-c221.md`.

## Fixed main test

Eight unchanged C220 episode shapes x81 checkpoint combinations =648 decisions.

Required:
- main success648;
- exact parent Coverage/answer parity648;
- readable success486;
- correct MISSING/OOS suppression162;
- downstream invocations on the162 suppressed queries0;
- actual readable trace `coverage,selector,provider,reader`;
- actual suppression trace `coverage`.

Successful main counters:
Coverage648; Selector486; provider486; bank reads486; Reader486.

The648 rows are not independent unseen tasks. They are a reused integration fixture crossed with
checkpoint seeds. No significance/generalization claim is made from the row count.

## Fixed causal interventions

For every checkpoint combination:

1. HOT alpha, force MISSING -> SUPPRESS_MISSING, Coverage-only trace.
2. SUPPORTED beta, force OUT_OF_SCOPE -> SUPPRESS_OUT_OF_SCOPE, Coverage-only trace.
3. MISSING alpha, force SUPPORTED -> Selector/provider reached, BLOCKED_MISSING, no bank/Reader.
4. OUT_OF_SCOPE beta, force HOT_REQUIRED -> Selector/provider reached, BLOCKED_OUT_OF_SCOPE, no bank/Reader.

The wrapper actually calls the frozen Coverage model before overriding its proposal and records the
original class. No weight is modified. Require324/324 correct intervention effects.
Successful control counters: Coverage324; Selector162; provider162; bank reads0; Reader0.

The provider's scope/observed-factor preconditions are deterministic runtime checks, not scorer
labels and not learned safety guarantees. A prevented invalid read does not turn a main Coverage
classification error into a correct prediction.

## Workload and fixed gate

Writer seeds218001/218002/218003; Coverage219001/219002/219003;
Selector217001/217002/217003; Reader216001/216002/216003.
All checkpoints frozen, no joint adaptation.

CPU, torch threads2, deterministic algorithms; float32 neural inputs and the inherited float64
numeric memory path.

At PASS, total model forwards2109 = Writer3 + Coverage972 + Selector648 + Reader486.
New training steps0. Fingerprints before/after must match exactly. Writer target accuracy1.0.
Construction retains18 learned Writer applications,12 oracle initialization writes,3 oracle
END_SCOPE operations and18 commits. These construction counts are inherited, not a cost benchmark.

PASS additionally requires exact main/control counter dictionaries, zero suppressed downstream
work and all parent parity/control criteria above.

Wrong predictions or invocation patterns in a complete run are scientific FAIL. The result validator
does not demand successful model-dependent downstream counts before serializing a valid negative.
Source/artifact/schema/malformed-output/incomplete-run defects are INVALID / RETRY SAME C221.

## Authoring registration

OWN7:
- `fold_lm/v05/memory_dispatch.py`
- `fold_lm/v05_benchmarks/gate_f_c221_live_coverage_dispatch.py`
- `tests_lm/test_v05_c221_live_coverage_dispatch.py`
- `tools/run_c221.ps1`
- `tools/invoke_c221.ps1`
- this preregistration
- `docs/v5f-live-coverage-dispatch-v0.1.md`

Source pins165. Protected inputs195 = inherited182 + parent summary/artifacts6 + OWN7.
Deciding dependencies16 = C220 direct dependency set14 + C220 benchmark + new dispatcher.
Output artifacts5: dispatch-plan, live-decisions, intervention-decisions, component-fingerprints,
validation-summary. All scientific outputs remain under ignored `runs/`.

C221 tests34; modules106; loaded2370; focused2369.
Only the inherited exact exclusion remains:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
No accepted historical source/test is modified, moved or removed.

Manifest SHA256:
`fb387b9c026ee852f4efbabab0c71cde93e03fea443f440f7b508b8fe3c3f4d8`.

## Post-authoring review

`post_authoring_review = PASS`

Review HEAD: `b5ee7fc81fc342152031859377260bb6f760486d`.
Review scope: committed-source review and targeted synthetic authoring tests, not formal science.

Remote files were fetched after all OWN files were committed. Git blob hashes of the five code/test/
PowerShell files matched the authoring copies exactly:

| File | Reviewed blob |
|---|---|
| memory_dispatch.py | da7efd7cf6c1c9a748ed35953df1a26a6e4c30fe |
| C221 benchmark | 0041f407622159b6ef26f232a2ed3183346c52b4 |
| C221 tests | 5bdea9b2dde65096a65be220da4782ad516d3c76 |
| run_c221.ps1 | 33eff61d19bd42978a56ed51aa09d88b0e7af230 |
| invoke_c221.ps1 | 03e420c395d14c9e66fc65110df45a14f1cbe7d3 |

On those identical copies,32 targeted tests were rerun:32 PASS,0 failures,0 errors in1.262 seconds
(Python3.13.5 / PyTorch2.10.0+cpu). Python source and all three embedded runner-Python blocks compiled.
The manifest hash was computed and matched. TestLoader enumerated34 new test methods.
Synthetic spy-model evaluation exercised648 main and324 intervention dispatches, with exact
registered traces/counters. A synthetic fixture of the actual parent artifact field schema passed
the648-row scorer adapter. These fixtures are not accepted-checkpoint scientific evidence.

Git comparison from published C220 log commit to the review HEAD changes only new C221/acceptance
files and the unpinned handoff. No accepted scientific source, historical test, log or dependency
was removed or edited. Parent artifact semantics, checkpoint-restoration call paths,16 dependency
coverage,165/195 accounting, argv[1]/postcheck argv[1..3], early-test ordering and launcher guards
were source-reviewed. C222 remains unregistered.

Not executed in the reviewing environment:
- `test_33_actual_historical_suite_counts`;
- `test_34_plan_matches_accepted_parent`;
- full2369-test historical regression;
- Windows PowerShell AST parsing;
- local-only accepted-checkpoint/artifact precheck or C221 science.

No synthetic or stub result is represented as a full historical-regression PASS. The authoritative
runner executes all34 new tests first, then2369 focused tests, and starts science only after those
gates pass. Dispatcher/launcher/runner AST checks remain on the Windows execution path. Failure
stops before science and preserves/publishes the log. Review PASS is not a claim those pending
execution checks have already run.

## Stop

Use `tools/invoke_active.ps1` with the final reviewed HEAD. Judge C221 before any C222 registration.
Gate F remains NOT PASSED. Actions-storage work remains separate.
