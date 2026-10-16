# C324 R6 acceptance and C325 handoff

Reviewed: 2026-10-16 (Japan time).

## Formal verdict

C324 = **ACCEPTED VALID NEGATIVE**.
Scientific status = FAIL; candidate_gate = false; execution validity = true.
C323 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY). Gate F remains NOT PASSED.
The original attempt at 47ccd303f4382b7938db639e86aeb151e1f83af1 remains INVALID.
This acceptance applies only to the completed R6 scientific attempt below.
C325 is NOT REGISTERED. There is no authorization to rerun C324 or to execute C325.

## Evidence identity and independent review scope

- Scientific execution HEAD: fcef3d5833c31d51e261ce578209bd5acd73f59c.
- Published log commit: c67be12c1a08dda49f218699ecb8896ef1cf2061.
- Publication parent: fcef3d5833c31d51e261ce578209bd5acd73f59c, confirmed from Git commit metadata.
- Console paths: docs/experiment-run-logs/c324/latest.log and latest.json.
- Complete uploaded console bytes: 2615255; SHA256 aa179e9f8a4d0b19bf0c5e55226731162e23cab63d2110158f8119c8742d4149.
- Primary summary SHA256 reported by the run: 21e752a51809a9b400c798b24c4ff405105458965b54610cfa16f71a349fbbdd.
- Execution-envelope SHA256 reported by the run: 2c6013d9b4f33fb20e79e68946ad8596d756d23694d7d04508fcd0ca0e3040c3.
- Local scientific folder: runs/c324-scientific-r6-6b241e7f98c94ee3846a852f39456a7f/.

The reviewer independently read and hashed the entire uploaded log, not only its
terminal excerpt. Its metadata hash and byte count match exactly. The uploaded log
has 5994 CRLF line endings. Complete CRLF-to-LF normalization produces 2609261
bytes, SHA256 140343d12cbd2dead7f54d1dc85ba1bee4b95746fd12ba28e22335ad44024d82
and Git blob e992984130d23dfd3c393368d268ed8f93499d11, matching the published
log blob. Do not confuse the original Windows-byte digest with the normalized Git
object digest or treat their different values as a scientific mismatch.

The independent review checked emitted receipts, exact test IDs, all ten emitted
measurement records, arithmetic, aggregate conservation and fixed gate decisions.
It did NOT independently open the user's raw checkpoint/evaluation bundles,
science/summary.json or execution-envelope.json. Their hashes and their local
semantic/byte verification are evidenced by the completed registered R6 execution.
Do not describe this review as a second independent model replay or a second
independent rehash of all 1501 original inputs.

## Execution validity

The following completed in order in the registered native R6 route:

1. Native read-lock probe PASS; seven C316..C322 verifier bodies COMPLETED once
   each, with nine exact same-session reuses and no reported verifier failure.
2. Native TRAIN/schedule/gradient preflight PASS before scientific fitting.
3. Unmodified separate-process regression: 5490 tests, 213 modules, zero failures,
   errors or skips. The reviewer counted 5490 distinct test IDs in the log itself.
   The inherited single C204 exclusion is unchanged. Regression time: 922.503 s.
4. All ten registered models reached step 1200/1200. Every paired seed and both
   original/interior4 arms are present; no partial cohort or successful-seed selection.
5. Ten checkpoint replays PASS, followed by saved checkpoint/measurement semantic
   verification and all 1501 final uncached input rereads.
6. Execution envelope emitted with 802 source pins, 1501 protected inputs and the
   full 5490-test receipt. Fresh-process execution_envelope_verified confirms this
   composite inventory. Regression, science and verify subprocesses all exit 0.
7. Terminal run_execution_valid = true. The scientific FAIL is not an execution
   exception and is not authorization to train again.

The reviewer independently recalculated 4320 local cell gates and 2160 two-order
gates from the emitted measurements. All cell/count/total/domain/seed/pair flags
agree with the original fixed thresholds and the terminal negative verdict.
Pair-level rescue/regression totals were checked arithmetically; case-level rescue
identities were not independently reconstructed without the raw evaluation bundle.

Parent snapshot timing was 192.0192500000121 s. The final hash receipt reports
61780 requests, 60279 cache hits, 1501 unique inputs and 1501 final reference
rereads. These operational figures are not a controlled speedup experiment.
The original native crash cause remains unidentified.

## Deciding scientific measurements

Both arms use native mean_last, 14256 parameters, 64 slots, CPU float64, two threads,
1200 updates per model and 48 rows per update. Only length-four TRAIN templates
change. The candidate replaces the old length-four templates with interior-order
templates; this is not an increase in training budget.
Seeds: 324001..324005. Registered child work remains 12000 updates, 576000 training
rows, 15420 model forwards, 904320 row presentations and 61680 core forwards.

Interior HOLDOUT totals per paired seed (288 answers and 144 query pairs each):

| Seed | Control answers | Candidate answers | Control both-query-correct | Candidate both-query-correct | Candidate interior gate | Candidate retention gate |
|---|---:|---:|---:|---:|---|---|
| 324001 | 148 | 288 | 5 | 144 | PASS | FAIL |
| 324002 | 133 | 267 | 4 | 128 | FAIL | FAIL |
| 324003 | 136 | 288 | 0 | 144 | PASS | FAIL |
| 324004 | 151 | 288 | 8 | 144 | PASS | FAIL |
| 324005 | 148 | 265 | 5 | 125 | FAIL | FAIL |

All five paired interior answer gains are positive: 140,134,152,137,117.
All five paired query-pair gains are positive: 139,124,144,136,120.
Across five seeds: answers 716/1440 -> 1396/1440 (49.72% -> 96.94%);
both-query-correct 22/720 -> 685/720 (3.06% -> 95.14%).
Answer rescues=697, regressions=17, net gain=680.
Query-pair rescues=663, regressions=0, net gain=663.
These are pooled repeated-seed summaries, not 1440 independent logical tasks or
a statistical-significance claim.

Original-task HOLDOUT accuracy and full fixed-domain seed pass counts:

| Domain | Control HOLDOUT correct / 1440 | Candidate HOLDOUT correct / 1440 | Control gate passes / 5 | Candidate gate passes / 5 |
|---|---:|---:|---:|---:|
| Original length 2 | 1440 (100.00%) | 1440 (100.00%) | 5 | 5 |
| Original length 3 | 1440 (100.00%) | 1433 (99.51%) | 5 | 4 |
| Original length 4 | 1440 (100.00%) | 1352 (93.89%) | 5 | 1 |
| Original length 5 | 1440 (100.00%) | 1246 (86.53%) | 5 | 0 |
| Original length 6 | 1427 (99.10%) | 1195 (82.99%) | 2 | 0 |

The full gates also require every registered TRAIN/HOLDOUT cell, masked-view
control and fact-order criterion; pooled HOLDOUT accuracy is not a replacement.
Candidate original2..6 retention is 0/5; control retention is 2/5.
Candidate interior gate is 3/5; control interior gate is 0/5.
The all-five composite C324 gate therefore fails, with no threshold changes.

## Interpretation and non-claims

Explicit interior-order exposure substantially improves binding on the registered
held-out logical combinations. It does not preserve all original tasks at the
fixed architecture and budget, and is not robust across all five initializations.
The candidate cannot be adopted as satisfying the C324 replacement criterion.

This is evidence of a coverage/retention tradeoff in this comparison, not proof of
architectural impossibility. Candidate interior templates were seen during fitting;
this is not unseen-template generalization. Both arms were trained from fresh paired
initial states: the result does not establish sequential catastrophic forgetting.
Control original6 also fails in three seeds; do not present the control as uniformly
perfect, and do not hide this by choosing only its successful seeds.
Gate F, general language capability and MinePilot readiness are not established.

## Next scientific direction -- NOT REGISTERED

A useful next question is whether retaining original length-four exposure alongside
interior exposure can recover original-task retention without losing the interior
improvement at the same total training budget. A paired interior4 versus mixed4
comparison is a candidate direction; the exact mixture schedule and scientific
success rule must be frozen before any new fitting.

Do not spend a new scientific run merely reproducing the aggregate arithmetic above.
No C325 source, test suite, runner, launcher or post-authoring review is established
by this acceptance document. C325 is NOT REGISTERED and has no execution HEAD.
Keep acceptance separate from any later C325 preregistration/activation commit.

Any C325 MUST validate BOTH the accepted primary summary and R6 envelope, inherit
all 802 combined source pins (not only the primary summary's 792), and protect all
new direct dependencies and supplemental regression inputs. Preserve accepted
sources/tests/logs/contracts. Extend the complete 5490-test inventory without new
historical exclusions. No CI addition, seed search, outcome-dependent thresholds,
retraining of accepted C324 or reuse of a selected checkpoint for fresh paired fitting.
