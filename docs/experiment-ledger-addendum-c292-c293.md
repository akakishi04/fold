# C292 formal acceptance — saved answer-role diagnostic

## Verdict and identity

C292 ACCEPTED PASS (diagnostic integrity only). C291 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C293 NOT REGISTERED in this acceptance commit.
Scientific execution HEAD:4e7d4468a103fa70dcfaee719fcf6daa75af5b7e.
Published log commit:513f820c494e067e67d1c3757af09cf7642b0b90.
Published log SHA256:5ef0c190eb49831b01e60fdcdf265a3183b1a0965147cf00ce66b4e50def9fdc;869232 bytes.
Summary:runs/c292-v5b-answer-roles-ba65b6ac20ac46e5b08fe96a5e5a8e74/summary.json.
Summary SHA256:44aa5ddbe5856ffdd7a62f63ac7574367527fab17c447c02ca68f7071e9ae513.
Manifest SHA256:f45b635e637d043d7b5dfeb2c65abed847a0b7d47ae3dd0cb4f0ce6c7f4f2869.

## Execution validity

Own32 and focused4317 PASS;the recorded full suite took554.722s.
Source598/protected1081. Parent reconstruction and the full role-audit dry-run passed before
scientific execution. The diagnostic reports PASS,diagnostic_complete=True and exact persisted
reconstruction. Final POSTCHECK:tracked tree clean,execution HEAD preserved,run_execution_valid=True.
Scientific training,model forwards,model-state loads,new checkpoint writes,row presentations,
core calls and network calls are0. The operational test suite is separate from this workload.
All15 parent states and38880 normal answers are retained. No C291 prediction or gate is changed.

## Accepted outputs

- audit-plan.json:1860 bytes;f45b635e637d043d7b5dfeb2c65abed847a0b7d47ae3dd0cb4f0ce6c7f4f2869.
- answer-role-report.json:10886453 bytes;fc63ace448c477ffc8e3cddb9e2a1f30c750fa6139dc271659d243a030148343.
- validation-summary.json:195492 bytes;638968211f717a444ebc4069e89cd694045e58ccecec96e7313103c67659c6b8.

## Deciding measurements

For seed291003,HOLDOUT,each partition contains288 normal answers.
Counts are errors / absent-known-value errors / other-fact errors / non-value errors:
- CE two_char:123 /112 /11 /0.
- CE triple:123 /110 /13 /0.
- CE quad:131 /113 /18 /0.
- answer_margin two_char:63 /62 /1 /0.
- answer_margin triple:72 /71 /1 /0.
- answer_margin quad:77 /72 /5 /0.
The candidate has212 errors across these three partitions;205 are known0..3 values absent from
both stated facts and7 are the other stated fact's value. These dependent partitions are not
independent experimental replicates. This concentration does not apply automatically to all seeds.
Both CE and answer_margin fit all two/three TRAIN normal rows on this seed. The error pattern
therefore cannot be described solely as selecting the wrong one of the two presented fact values.
Pair_sum fits the seen-length HOLDOUT of this seed and has8 quad HOLDOUT errors:5 absent,3 other.

## Interpretation boundary

An absent value is an observable unsupported output,not proof of memorization,a specific attention
route,or deficient model capacity. The diagnostic is not an intervention or independent replication.
Prior quad gates remain CE4/5,pair_sum2/5,answer_margin4/5. Do not replace full256-class decoding
with a restricted value decoder or silently promote the model based on these role labels.

## Next bounded question,not activation

Test whether reweighting the existing CE component that places probability on either stated fact
value improves transfer,without extra training examples,inference filtering or parameter changes.
For a paired TRAIN example with support S={y0,y1},CE decomposes into
Lsupport=-log(P(y0)+P(y1)) and Lchoice=-log(P(y)/(P(y0)+P(y1))).
A candidate CE+.25*Lsupport increases support pressure while keeping the conditional choice term
at its ordinary weight. Concurrent CE and1.25*CE controls distinguish this policy from merely
multiplying the whole loss;this does not perfectly match optimizer gradients or prove causation.
Only paired TRAIN labels may define S;no HOLDOUT/quad optimization or metadata in model.forward.
C293 requires separate preregistration,implementation,tests and committed-byte review.
