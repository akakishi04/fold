# C315 formal acceptance — valid negative

C315 ACCEPTED VALID NEGATIVE. Candidate one_to_four six gate4/5,not registered5/5;
two_to_four control3/5. Gate F NOT PASSED. C316 NOT REGISTERED in this acceptance commit.
No C315 rerun is justified. Earlier bounded PASS and negative judgments remain unchanged.

## Evidence and validity

Scientific execution:5708562420e530749a8f63b1f4baf3c7e0f28029.
Published log:0b4ce1c953d2ccf0eea04747b1194c6dd70729ee.
Log SHA256:f9d269f451e296d9c8ce9b3f084816d9407d9717f6d5a488cb1909ccc64cb7f9;812040 bytes.
Summary:runs/c315-v5b-single-mix-dbdffe0b88094f729d1dbfbcdba520f0/summary.json.
Summary SHA256:aceda00cebf61b49e5f923bf7c426e2f4522dcac68444fc2e07b27a17b63dd66.
Own32/focused5085 PASS;source736/protected1379;all_pairs_matched=True.
All10 fits/final evaluations/strict replays completed;persisted_single_mix=PASS;
run_execution_valid=True;tracked tree clean;scientific HEAD preserved.
Publication changes only C315 latest.json/latest.log. FAIL is capability,not execution failure.

## Deciding outcomes

Lengths2,3,4,5:both arms5/5. Six:control3/5,candidate4/5.
Paired six:both_pass3,candidate_only1,control_only0,both_fail1.
315004 changes from control six573/576 TRAIN and284/288 HOLDOUT to candidate576/576 and288/288.
315002 still fails both:control566/576,283/288;candidate574/576,286/288.
The other three seeds have perfect normal six outputs in both arms.
Thus six normal errors fall22->4 in this cohort. No per-row rescue/regression count is inferred
from these aggregate correct counts. Every normal length2..5 partition is perfect in both arms.
Candidate length1 diagnostics:all5 perfect192/192 TRAIN,96/96 HOLDOUT. The untrained-single
control misses one HOLDOUT question at315001 and one TRAIN question at315004. Length1 remains
diagnostic-only and cannot substitute for the six gate.

## Interpretation and next boundary

Short examples were not useless in this cohort:one additional six pass and fewer total errors.
This is not proof of general superiority or abstract-rule discovery. Only five paired seeds;
candidate replaces25 percent of long-length exposures with short examples and alters timing.
Do not increase budget or tune the mixture to fix the remaining four questions.
Proposed C316:one preregistered fresh-seed replication of the exact C315 two-arm policies,
including1200updates,100 vs75 per-length exposures,canonical length1,core_slow and all old gates.
No old checkpoint reuse or pooled C315 success to rescue new failure. Separate authoring/review
and activation must finish before the new launcher is issued.
