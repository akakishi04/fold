# C344 acceptance and C345 saved-objective audit boundary

Date: 2026-11-22 Japan time.
**C344 ACCEPTED VALID NEGATIVE.** Execution revision C344-R1 completed validly;
the registered pair-max candidate gate is false, eligible_seed_count=2.
Attempt01 remains INVALID EXECUTION. Gate F remains NOT PASSED. No production
adoption. This acceptance does not activate C345.

## Execution identity and evidence

Scientific execution HEAD: `8d1e1170cd614503deab1e09474fe82de4bba561`.
Log publication: `9d163289775373aaf62028a7b8aeacbfb41593a6`, sole parent execution.
The publication changes only docs/experiment-run-logs/c344/latest.log and
latest.json. The seven OWN files reviewed at source
`ca6df52fb72ed0020df7e3d027d738d28870464f` remain unchanged through execution and
publication. The original attempt01 log archive remains byte-identical.

Original Windows log: 355860 bytes; SHA256
`aba71fc3bba513a3dab51a34b46b06641b1b0f5c2fa713c201c3491643867b49`.
Git LF: 352156 bytes, 3704 LF; SHA256
`3b95943f9ae648a09af420c359a084e6718e67449345e24b9177e1eaa83780a1`.
LF-to-CRLF reconstruction exactly matches the published metadata. Git log blob:
`b1a7229297b364ccedf677ce844b168b522bf36a`; metadata blob:
`f10685544698e2a11ed310987845a79aa4997958`.

Run folder:
`runs/c344-pair-max-training-76ae8eb6e3bf4d08ac577c5fde9e0caa/`.
Primary summary SHA256:
`610398ced893ff1d1885faf9bd02ffef57779ca2bd96bfa995b6929e6d8f20d7`.
Execution envelope SHA256:
`c77f0fcf5fcbbf59d3961894713dbf8dcb30ae89841df0325b980a07d8913562`.
Manifest SHA256:
`a663ebb0b09671c6d277b5abec6d09604a49a194d5d61409a1a5bf5018785ad8`.

## Execution validity

The six native R1 timeout-cleanup cases passed, with six cleanup barriers and no
failure, error, skip, expected failure or unexpected success. Their exact receipt,
source pins, execution HEAD and order match the accepted R1 contract. Native read
locks passed the write/delete-denial and read-compatibility probe.

Full regression: **6514 tests / 239 isolated modules PASS**, 3208.100 seconds,
zero failures/errors/skips. All 239 module begin/end records match the production
loader's actual ordered modules and counts. All 242 module/regression/science/
fresh-verifier process exits are zero. Ordered test-ID SHA256:
`c5d7db147680f739c62bbbc2f12be324c66ba16ea108dc04beb3071f56abaaa3`.
The only inherited exclusion remains the exact C204 mutable-ACTIVE test; no new
exclusion or accepted-test modification was used.

All 930 source pins / 8183 protected inputs were registered. Immediate C343
semantics and its 6442-test proof were reconstructed without ancestor neural
reruns. The discarded numerical preflight preceded the full regression; all ten
2400-update fits finished before any final evaluation/replay. Formal science
completed 24000 updates, 27420 model forwards and 1480320 row presentations.
Saved-state roundtrip, exact-argmax/raw-logit replay and saved arithmetic/stream
reconstruction passed. All 8183 inputs received final uncached rereads. The
separate fresh verifier completed and `run_execution_valid = true`.

Independent review reconstructed the complete published summary from 10 seed
records, 120 normal summaries, five paired summaries and 60 normal contrasts,
then passed the original immutable check_summary and fixed_gate functions.
The author-side review used the fetched log, committed writer/verifier source
and completion evidence. It did not transfer or rerun all native checkpoints or
the user's protected inputs on the author machine.

The successor must retain **all 489 C344 outputs**: six science artifacts,
primary summary, execution envelope and 481 regression proofs (three records
plus 239 module JSON/log pairs). With seven new OWN files this yields 937 source
pins and 8679 protected inputs, before any further preregistered additions.

## Preregistered decision

C344 changed only the TRAIN reduction from ordinary mean full256 CE to the mean
of each complete query pair's maximum CE, at identical paired initial weights,
mixed45 token/target streams, architecture, rates and 2400-update budget.

PASS required all five candidates to pass every original2..6/interior4 native
gate; all 60 seed/domain/split contrasts to have nonnegative answer AND query-pair
gains; and all four aggregate interior TRAIN/HOLDOUT answer/pair gains to be
strictly positive. No condition was changed after observing the run.

Only seeds 344001 and 344005 satisfy the candidate eligibility conditions: **2/5**.
Control full-pass seeds are 344004 and 344005, also 2/5. These are different passing seed sets;
the equal full-pass count does not mean the two arms behave identically.
Seven of 60 matched contrasts regress on both endpoints: **14/120 inequalities
fail**. All four strict interior gains are negative.

|Interior4 endpoint|mean_ce|pair_max|Candidate minus control|
|---|---:|---:|---:|
|TRAIN correct answers /2880|2864|2728|-136|
|TRAIN both-query-correct pairs /1440|1424|1293|-131|
|HOLDOUT correct answers /1440|1430|1331|-99|
|HOLDOUT both-query-correct pairs /720|712|640|-72|

## Deciding measurements

|Seed|Interior TRAIN control /576|Candidate /576|Interior HOLDOUT control /288|Candidate /288|Control full pass|Candidate full pass|
|---|---:|---:|---:|---:|---|---|
|344001|576|576|288|288|false|true|
|344002|560|562|278|280|false|false|
|344003|576|552|288|275|false|false|
|344004|576|462|288|200|true|false|
|344005|576|576|288|288|true|true|

|Domain / split|Control correct|Candidate correct|Rescued answers|New regressions|
|---|---:|---:|---:|---:|
|interior4 TRAIN /2880|2864|2728|16|152|
|interior4 HOLDOUT /1440|1430|1331|10|109|
|original6 TRAIN /2880|2875|2877|5|3|
|original6 HOLDOUT /1440|1431|1438|9|2|
|original5 TRAIN /2880|2880|2879|0|1|

Original2/3/4 are perfect in both arms on normal TRAIN and HOLDOUT views.
Original5 HOLDOUT is also perfect in both. Original6 improves in aggregate but
regresses on both splits for seed344004. Its names were never fitted; its TRAIN
label means familiar logical value combinations, not trained six-character names.

Every candidate interior TRAIN error is a new error relative to its paired control:
all 16 control errors were rescued, while 152 previously correct answers became
wrong. All 152 candidate TRAIN errors select the other observed value. Among 1440
candidate TRAIN query pairs, 1293 are both correct, 142 have exactly one correct
answer and five have neither correct. The 142 single-error pairs collapse to one
displayed value; the five double-error pairs swap the two displayed values.

The same disjoint-error pattern holds for interior HOLDOUT: all ten control errors
were rescued and 109 new errors appeared. Those 109 errors comprise 50
wrong_observed and 59 absent_digit, with zero outside_catalog. Candidate HOLDOUT
has 640 both-correct, 51 one-correct and 29 zero-correct pairs. Answer and pair
transition units differ and must not be added together.

The largest deterioration is seed344004: interior TRAIN576->462 and
HOLDOUT288->200. Seed344003 also deteriorates; seed344002 improves slightly but
still fails the interior gate. No seed or subgroup is excluded from the result.

## Interpretation and boundaries

At this fixed training budget and cohort, pair-max is not an effective remedy for
the fitted binding failures motivating C344. The failure is not only transfer to
unseen value combinations: actually fitted interior TRAIN answers also worsen.
The result does not support adopting this candidate or declaring Gate F passed.

The intervention changes within-pair gradient weighting and its interaction with
global clipping. Zero direct gradient for the easier partner, switching of the
harder partner, optimization difficulty and a mismatch between the surrogate loss
and exact-answer metrics are possible explanations, not measured causal findings.
The terminal logits and training traces were saved, but their matched loss-level
diagnosis has not yet been formally performed. No capacity or pooling cause is
established. Cross-experiment raw scores with different seeds are not paired
comparisons.

## Next one question: C345 saved-objective and trajectory audit

Does pair-max's worse binding accompany a higher terminal pair-max objective on
the same fitted prompts, or a lower surrogate objective despite worse exact
answers? C345 will audit the existing C344 artifacts, without new model forwards,
training updates, coefficient searches, checkpoint selection or altered inference.

Compute both ordinary CE and pair-max from the saved full256 normal logits for
every seed, arm, domain and logical split, bind exact-answer/pair counts back to
C344, and describe the matching objective-versus-answer contrasts. Inspect every
saved preupdate loss and preclip norm using all fixed 200-step blocks and both
cycles' canonical slot/profile groups. Slot4 is a mixture of original4, original5
and interior4, and must not be reported as a pure-family loss.

Preupdate minibatch traces are not intermediate full-cohort evaluations; they
cannot establish that exact-answer capability was learned and later forgotten.
Norm>1 counts are a descriptive clipping-threshold diagnostic, not proof that
clipping caused the failures. A lower final objective would not establish a global
optimum. The diagnostic must preserve C344's valid-negative capability judgment
whatever the signs of the measured differences. Registration, tests and an
independent committed-remote-byte review remain separate prerequisites.
