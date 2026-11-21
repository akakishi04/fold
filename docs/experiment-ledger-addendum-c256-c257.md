# C256 acceptance and C257 unseen-order boundary

## Formal verdict

**C256 ACCEPTED PASS — bounded three-entity task-shift capability.**
This is a capability PASS, not merely a diagnostic-integrity PASS. It does not promote Gate F,
prove general language skill, establish core superiority, or authorize production adoption.
C252 remains ACCEPTED VALID NEGATIVE; C255 remains diagnostic PASS.

Scientific execution HEAD: db9f3cb90d9268066c34fc91300193058301f06c.
Published log commit: 5695706c6306156fa079ce092581270ca781af71.
Publisher log SHA256: 4f21d18bec9eb3ae937c42be9d8af3091d67a241a53a85820afd3e6694110ce6.
Log bytes: 654496.
Summary SHA256: 56c9c4e46800aadfb3c1a125522a66c6c2014721eceac0ab29ccd08c005bd184.
Local summary: runs/c256-v5b-three-entity-3f95a0d190e4424f91634cb8813d7987/summary.json.
Publication follows execution by one commit and changes only c256/latest.log/latest.json.
Acceptance uses retrieved immutable log ranges, publication metadata and recorded local postchecks,
not independent rerunning of learned checkpoints or a complete-log byte rehash by the reviewer.
The earlier precheck failure remains INVALID in the C256 execution-recovery addendum and Git history.

## Execution validity

24 own tests PASS in 0.832s; 3313 focused tests PASS in 207.503s.
382 source pins and 623 protected inputs verified. All ten models completed 800 updates:
8000 updates, 384000 training presentations, 8120 model forwards, 401280 total row presentations.
Changed full/head weights, strict checkpoint state loading, saved predictions, metrics and logit
replay passed. Final protected inputs, clean tracked tree and scientific HEAD checks passed.
run_execution_valid=True; candidate_gate=True; scientific_status=PASS.

## Deciding metrics

Every candidate seed passes both languages and both TRAIN/HOLDOUT under the original registered
accuracy, order-pair, query-triplet and mask-drop criteria. Candidate TRAIN: 720/720 correct.
HOLDOUT correct counts below are per language, denominator 72:

| Seed | Candidate EN | Candidate JA | EOS control EN | EOS control JA |
|---:|---:|---:|---:|---:|
|256001|72|72|29|25|
|256002|72|72|29|28|
|256003|72|72|26|24|
|256004|72|72|21|24|
|256005|70|72|20|22|

Candidate HOLDOUT: 718/720 (99.7222%); control: 248/720 (34.4444%).
Candidate beats its same-seed control in every one of ten HOLDOUT language comparisons.
Whole-seed joint passes: candidate 5/5; EOS adapter 0/5.
Candidate outcome counts: BOTH_PASS=10.
Control outcome counts: TASK_SHIFT_MISS=9; TRAIN_CRITERIA_MISS=1.
The control seed256001 JA misses its TRAIN query-triplet criterion (19/24), even though its
normal TRAIN accuracy is 66/72. Do not describe all control TRAIN cells as passing.

Candidate seed256005 EN HOLDOUT: 70/72 answers, 34/36 order pairs, 22/24 query triplets,
evidence_drop=0.722222..., query_drop=0.638888...; it legitimately passes the unchanged gate.
Other candidate HOLDOUT cells: 72/72, 36/36 order pairs and 24/24 query triplets.

## Interpretation and remaining boundary

The selected aligned reader architecture can learn withheld three-way value assignments on five
new initializations, while the parameter-matched EOS-only control does not reach that result.
The difference is bounded to this authored task and budget. It is not a compute-matched comparison
or proof that the FOLD core is superior to a properly matched core-free attention model.

Compared with C252, C256 also changed names, assignment split, sampling, batch size and training
budget. Consequently this is not evidence that three entities are inherently easier or that the
architecture's general initialization robustness has been solved. Languages are symbolic identifier
spellings, not evidence of natural-language proficiency. Five seeds are not a population guarantee.

C256 only trained/evaluated fact orders (a,b,c) and (c,b,a), or their Japanese equivalents.
The middle entity b/乙 therefore never changes its middle position. Generalization over value
assignments does not establish generalization over all six fact orders.

## Accepted artifact identities

- dataset.json: ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b (34296 bytes)
- measurements.json: f7d11d7592769e54824d3d7dccc4e481029dc5157b6c35c333831408d7b032c8 (45697 bytes)
- task-plan.json: 43948ceb676d536301d4e3a63a7ee1407f8bec44034db59f8b4f6e4872ae53b1 (2691 bytes)
- trained-models.pt: 72d9ada52e48395290200c1c6918d7eef091aebd44a3d2a6176dc1dd442dae3a (1236574 bytes)
- validation-summary.json: a25fe29ed2deb33ceab64c0f7d7e450e6a143ea5c0bc428eea20b9d45dff8bc2 (2313 bytes)

## Next question, not registration

Freeze all ten C256 final models. Without further training, can the candidate answer the same
assignments under the four fact orders never used in C256: acb, bac, bca, cab?
Keep the TRAIN/HOLDOUT assignment boundary, languages, queried entities, target values and model
weights. Replay the original two orders first, then evaluate the new four, then restore/replay the
original inputs. Score each new order separately and all-six-order consistency, not only a pooled
average. Retain all controls and all seeds. This is a new order-transfer capability evaluation,
not another internal-activation intervention and not a C256 retry. Separate preregistration and
committed-byte authoring review control C257 activation; C258 is not registered.
