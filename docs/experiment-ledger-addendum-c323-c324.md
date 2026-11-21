# C323 acceptance / C324 boundary

## Formal verdict

C323 ACCEPTED PASS (DIAGNOSTIC INTEGRITY).
C324 NOT REGISTERED. No ACTIVE experiment after this acceptance.
C321 remains ACCEPTED VALID NEGATIVE; C320 and all earlier verdicts remain unchanged.
Gate A/B PASSED; C/D PASSED in their measured scope; Gate E PASSED; Gate F NOT PASSED.
C323 is not a model-capability PASS, a model improvement, or a production adoption.

## Execution identity and evidence

Repository: akakishi04/fold; branch: feat/sft-target-loss.
Scientific execution HEAD: 1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4.
Published log commit: e434a7ac6dd867e32f8135fc1b4c395e1644ffb9.
The publication commit has the scientific execution HEAD as its parent.
Console evidence: docs/experiment-run-logs/c323/latest.log and latest.json.
Log SHA256: ba9f788c326b6c4bc3a86a9d6bde542410fffa73d50c0d961707fd2a3980b8f8.
Log size: 1072473 bytes; 7280 physical text lines in the uploaded copy.
Saved summary: runs/c323-v5b-fact-order-f1b710e74fbe495aba6410d0d9530248/summary.json.
Summary SHA256: fcc87597395300e45eacabaa94b87b6910093669532279f9ed6c67ec3f84af1f.

The user supplied the two published console files after the earlier connector read
of the large log was incomplete. The uploaded raw bytes were independently hashed;
both size and SHA256 exactly match the publication metadata. No experiment rerun.
The current remote handoff, execution source and runner were read before acceptance.

## Execution validity

- Own tests: 24/24; 9.389 seconds.
- Ordered one-process full regression: 5293 run, 0 failures, 0 errors;
  unittest elapsed 1214.580 seconds; exit 0 / 0x00000000.
- authoring_runtime_preflight = PASS.
- Scientific process exit 0 / 0x00000000.
- Source pins 784; protected inputs 1478; registered manifest unchanged:
  8c4e9152cb11d1492cd7d88cf7caafef40a901de6c68aa44e404c1c46ff7c5de.
- Runner invokes C323.precheck, then C323.verify_artifacts, before printing
  the summary hash, overall groups and diagnostic-complete receipt.
- persisted_fact_order = PASS; diagnostic_complete = True;
  tracked tree clean; execution HEAD preserved; run_execution_valid = True.
- Scientific model forward calls = 0; no scientific learning or checkpoint loading.

Independent reviewer-side processing of the uploaded console verified 240 unique
(seed,arm,condition,split,profile,language) groups, re-summed every integer field into
all four printed overall records, and reconciled 4320 counterfactual groups / 8640
question pairs / 17280 normal answers. This is a console-evidence reaggregation,
not a claim that the reviewer independently reran the user's local-only archives.

A runpy RuntimeWarning appears in the science stderr excerpt because the module
was already imported before run_module. It was not an exception: the process
returned 0 and the separate persisted-result reconstruction completed. Retain this
warning in the historical log; do not claim a warning-free run or edit accepted files.
The preflight's scientific_execution_started=False precedes the Execute phase and
is not a declaration that the later scientific diagnostic failed to execute.

## Deciding results

The preregistered PASS gate is diagnostic integrity and exact parent reconciliation,
not a minimum frequency of any bias category. The following are descriptive results.
All counts aggregate five seeds, English/Japanese, three profiles, TRAIN/HOLDOUT.
Each arm/condition has 1080 four-answer counterfactual groups and 4320 answers.

| Arm / condition | Correct answers | First-fact tracking in both orders | Last-fact tracking in both orders | Same output class in all four cases | All four correct |
|---|---:|---:|---:|---:|---:|
| mean_last / old4 | 4320/4320 | 0/1080 | 0/1080 | 0/1080 | 1080/1080 |
| mean_last / interior | 2211/4320 | 15/1080 | 113/1080 | 814/1080 | 29/1080 |
| last_only / old4 | 4320/4320 | 0/1080 | 0/1080 | 0/1080 | 1080/1080 |
| last_only / interior | 2292/4320 | 29/1080 | 95/1080 | 809/1080 | 62/1080 |

Interior question-pair collapse remains 1996/2160 (mean_last) and 1951/2160
(last_only), exactly reconciling C322. Per-query argmax stability under fact-order
swap is 1779/2160 and 1822/2160, respectively. Counts of answers classified as
first / last / other are 1908/2326/86 and 1991/2246/83, summing to 4320 per arm.

## Interpretation and non-claims

Interior names are four-character strings with equal first and last characters and
equal character multisets, but different internal order. This is a name-binding
challenge, NOT a change in the location of the query in the prompt.

In this saved cohort, always choosing the first or last written fact is not a
sufficient description of the dominant failure. Same-output-class lock across both
query identities and both fact orders is much more common (814/1080 and 809/1080)
than consistent first- or last-position following. This does not identify the
internal mechanism or prove that query information is absent: C322 already showed
that identical argmax results need not imply identical logit vectors. The lock
category may include an output class other than either supplied value.

The old4 positive controls remain perfect. The interior prompts were not included
in the C319 training distribution. Therefore this result alone cannot distinguish
insufficient training coverage from a structural representation/readout limitation.
No checkpoint, threshold, source prediction or previous result was changed.

## Next one-question direction — not executable registration

Candidate C324 question: at fixed architecture, optimizer, logical TRAIN rows and
training budget, does explicit exposure to the interior-order name distinction
improve held-out binding while retaining the original name-task performance?

Prefer a paired training intervention over another descriptive saved-output audit.
Use native mean_last in both arms so readout changes are not confounded with training
coverage. A candidate comparison replaces only the length-four TRAIN name templates
with the three fixed C321 interior templates; the control keeps the original
length-two/three/four templates. Preserve logical identities, targets, per-row
exposures, value split, permutations, languages, step count and paired initialization.
Use fresh preregistered seeds rather than selecting an existing successful state.

This direction is NOT a frozen unseen-name generalization claim: interior-order
patterns would now be seen during training. Original-task retention, HOLDOUT query
pair correctness, masked controls and both fact orders must remain separate gates.
Exact seed list, workload, thresholds, artifact schema, complete implementation,
regression registration, launcher and independent remote-byte post-authoring review
must be fixed before C324 can become ACTIVE. No C324 execution command is authorized
by this document. Do not rerun accepted C323.
