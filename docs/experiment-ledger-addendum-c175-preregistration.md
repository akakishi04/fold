# C175 preregistration — frozen prediction frequency reference

Registered after C174 acceptance commit `b5c670932c9614f3a892e9ddff697520b12e6926`.
Repository `akakishi04/fold`, branch `feat/sft-target-loss`. V5-E.
**C175 ACTIVE / NOT YET JUDGED. C174 remains ACCEPTED PASS. C176 NOT REGISTERED. Gate E NOT PASSED.**
Use the final C175 registration commit as ExpectedHead. Read the conversation protocol,
C174 acceptance addendum and unchanged C174/Gate E evaluation contracts.

## One question / scope

Does EACH frozen C174 syntax-visible model exceed a syntax-blind reference that uses
all TRAIN rows to tabulate the majority class for each visible-fact/resource state?
Changed scientific variable: the comparator, not the candidate or its predictions.
Hold all C174 checkpoints, final argmax decisions, 72 fields, rows, split, labels,
semantic groups and primary scoring definition fixed. No candidate postprocessing.

This is a development analysis designed AFTER seeing C174's complete summary. It reuses
the same 4 pilot groups, not an independent replication or a new final Gate E holdout.
A C175 negative does not revoke C174's correctly preregistered positive result. No new
capacity/steps/threshold/split/seed search is allowed inside this analysis.

The rationale is C174's small aggregate syntax gains and imperfect training fit;
one pilot group deteriorated in all seeds and the blind models were already nontrivial.
The new reference removes optimizer quality from the syntax-free comparator by using
exact counts. It is NOT claimed optimal for held-out group-macro balanced accuracy.

## Frozen sources / work

C174 execution HEAD: `d011b13952abc10093d8d8d2b418ecc3d39f5fc3` (standalone runner fix).
Parent: `runs/c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410/summary.json`.
Parent SHA256: `3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36`.
Canonical data SHA256: `eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65`.
Manifest SHA256: `51c7b72eb8496118185ec9ab370f068902f312b332855abc479be00a5ffc9478`.

Verify all11 parent artifacts against exact names/hashes/sizes. Six checkpoint files
are hashed only, NEVER deserialized or run. Read pilot-data.npz without pickle,
templates-and-splits.json, pilot-predictions.json and training-predictions.npz.
Reconstruct the exact canonical dataset fingerprint, model/row alignment, raw pilot
argmax versus saved logits, all six train/pilot confusion aggregates and 3 C174 baselines.
No C174 dataset regeneration, optimizer, inference, acquisition or proof checker.
C174 row predictions are the data under analysis, not a substitute for a newly claimed live run.

| Work | Fixed count |
|---|---:|
| Existing models / initializations |6 / 3 reused, no new models|
| TRAIN rows / groups / templates |42444 / 36 / 524|
| PILOT_EVAL rows / groups / templates |9396 / 4 / 116|
| Saved model decisions reaggregated |311040 = 6 x 51840|
| TRAIN-only blind keys |81, each with524 training rows|
| Reference classifications |51840, split results kept separate|
| New training steps / learned forward calls / fresh seeds |0 / 0 / 0|
| Checkpoint deserializations / actual acquisitions / evidence writes |0 / 0 / 0|

Regression's historical toy training tests are outside these benchmark counts.

## Reference fixed before measuring its pilot score

Key = raw integer fields0..3 concatenated with46..71, exactly the information retained
by C174 syntax ablation before fixed positive scaling. AST fields4..45 are excluded.
Do not use function IDs, template IDs, split labels, unknown values or pilot teacher labels
as key features. All templates have the same shape bounds/resources outside AST, yielding
81 distinct visible assignments. Gather class counts ONLY from the 42444 TRAIN rows.
Each row contributes one vote, as under C174's uniform row sampling, not group reweighting.
Predict1 iff TRAIN count1 is strictly greater than TRAIN count0, otherwise predict0.
Ties choose0. No smoothing, tuning, fitted decision threshold or PILOT_EVAL-based selection.
An unseen key is an execution error, not a fallback prediction.
The table represents TRAIN empirical ordinary-accuracy majority, not a held-out oracle.

## Deciding endpoint / verdict

Primary = equal mean of per-group balanced accuracies across ALL4 existing PILOT_EVAL
groups. Retain the full/ablated C174 metrics and the new reference separately.
**PASS**: valid complete analysis AND for EACH seed174001/174002/174003, the frozen
TASK_VISIBLE primary strictly exceeds the reference primary and its two aggregate class
recalls remain >0.5. Ties or failure in any seed => **ACCEPTED VALID NEGATIVE**.
Do not average away a failed seed. This is a directional development criterion,
not statistical significance, practical quality, proof of systematic reasoning or Gate E.

**INVALID / RETRY SAME C175**: source/hash/schema/canonical data drift, missing artifacts,
row/model mismatch, raw-logit/argmax mismatch, failure to reproduce the accepted summary,
missing workload or protection failure. These are not new behavioral negative outcomes.
No historical output is changed; finite scientific FAIL saves its result and exits0.

## Batched secondary measurements (not additional success gates)

For all6 frozen models, separately for TRAIN_RESUBSTITUTION and PILOT_EVAL:
- per-group confusion, both recalls, ordinary and balanced accuracy;
- confusion stratified by missing-fact count0..4; absent-class recall/BA is null, not
  silently called0 or1, and no stratum is dropped from the main endpoint;
- at each identical blind key, pair opposite-label rows and count pairs where BOTH are
  correctly classified. Sum n0*n1 candidate pairs and correct0*correct1 successes without
  materializing the Cartesian product. Empty denominator => null. Pair counts follow the
  fixed hash-bound dataset, with no case selection. These correlated comparisons are
  not independent trials or single-operator interventions and do not alter the verdict.
Save all81 reference table keys/counts/predictions for review. Neither labels nor these
secondary analyses repair a candidate decision or select a different checkpoint.

## Source protection / migration handling

48 historical paths = parent42 source_blobs + six C174-owned files pinned at d011b139.
Four C175-owned files checked against execution HEAD. Use standalone `HEAD:<path>`
without `fold/`, and retain original parent artifact hashes/provenance.
No monkey-patch of old modules. No changes to old runners, model, input decoder or
preregistrations. Root-local canonical checkout bytes or LF/CRLF equivalent only.
C37/composition fixture and C174 summary remain outer protected files.

Fresh UUID output: audit-plan.json before measurements, audit-details.json for complete
secondary tables and full summary.json. Hash/size protections, final tree/HEAD checks.

## Verification / execution / stop

20/20 new actual-module tests passed with NumPy and real temporary standalone Git source
checks, including LF/CRLF equivalence and tamper rejection. Toy reference/predictions only;
no C175 score on registered data has been computed by the reviewer. New Python code compiled.
Three embedded runner Python scripts parsed. Full973 tests, Windows PowerShell and the
artifact-backed complete audit have NOT been executed by reviewer.
**973 focused tests expected =953+20,59 modules**, once, then one CPU audit.
Runner: `tools/run_c175.ps1 -C174Summary ... -ExpectedHead ...`, authoritative Python
`.venv-py31315/Scripts/python.exe`. Progress 1/3 replay,2/3 reference/strata,3/3 protection.
No C174 retraining. Collect the log even if scientific_status=FAIL with valid execution.
Judge C175 -> ledger/handoff -> next design. No C176 before formal judgment.
