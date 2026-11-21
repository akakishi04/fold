# V5-B normal-exposure control v0.1 — C247

## One question

Is the amount of ordinary training in C246 sufficient to fit the original TRAIN task when
its masked updates are removed? This is the missing normal-exposure control, not another attempt
to tune the same failed augmentation or a claim to solve generalization.

C244 had400 normal updates per model. C246 had200 normal plus200 other-value-hidden updates,
with the same total presentation budget. C246 lost full TRAIN criteria in10/12 cells. That cannot
yet be assigned to mixed-task interference:ordinary exposures were also halved.

C247 supplies200 NORMAL updates only, matching the count and relative order of C246's normal
examples. Compare all three records on the same input rows, retaining every seed and language.
Do not erase the accepted C246 result, rerun C244 or turn a control PASS into a HOLDOUT claim.

## Exact intervention and fixed quantities

Keep C244/C246 TRAIN64 and HOLDOUT32 byte-identical. Use only TRAIN normal tensors for optimization.
There is no additional masked training form, new row, changed target, architecture change or
inference correction. Parent checkpoints remain protected files but are never deserialized.

Create fresh Full13488/GRU-only10160 models with seeds234001/234002/234003,width16,48 slots.
Match C246.initial_sha256, inherited from C244's before-training state. Make the independent
common-weight GRU-only copy before either paired model learns. Never continue a trained checkpoint.

Normal row blocks alternate old32 then added32 for100 cycles. Each original TRAIN row appears
100 times, exactly as in C246's normal portion. Zero-based control step j corresponds to original
C246 step 4*(j//2)+2+(j%2). The mapped original view must be normal and its row indices identical.
C247 has no placeholder/zero-loss optimizer updates for the removed200 masked updates.

AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,CPU float64,threads2,
deterministic algorithms are fixed. The normal fit executable AST is equal to C244's except its
progress tag; STEPS is deliberately200 instead of400. No learning-rate schedule, gradient reuse,
checkpoint/seed selection, added budget or early stopping is introduced.

Normal-example exposure is matched, total optimizer steps are NOT. Removing the masked updates
changes Adam's step index and moments as well as the gradients it sees. This is a control for the
sufficiency of the normal budget, not unique identification of gradient conflict or a module fault.

## Primary and secondary outcomes

Primary:all Full seed/language cells pass the original full TRAIN criteria at200 normal updates:
accuracy>=0.90;fact/query/order paired both-correct>=0.80;both evidence/query mask drops>=0.35.
With32 rows/language and16 pairs per kind, this means at least29/32 correct and13/16 pairs.
GRU-only's TRAIN gate is reported independently. A primary pass is normal-budget TRAIN sufficiency.
A primary miss with valid execution is ACCEPTED VALID NEGATIVE for that limited question.

HOLDOUT is evaluated and fully reported using the same inherited criteria, but it is secondary
and does not decide the primary PASS. Report secondary joint TRAIN+HOLDOUT family gates explicitly.
This is an intentional newly registered control endpoint, not a relaxed C246 generalization gate.
C246/C244 remain valid negatives and Gate F remains NOT PASSED for either C247 primary outcome.

Comparison labels per seed/family/language are BOTH_TRAIN_PASS,CONTROL_TRAIN_PASS_ONLY,
C246_TRAIN_PASS_ONLY,NEITHER_TRAIN_PASS. A control-only TRAIN pass shows that reduced normal
presentation count alone is insufficient to explain the corresponding C246 miss. A control miss
is compatible with normal-budget insufficiency but does not exclude an additional mixed-training
effect. No pooled significance claim or family-wide mechanism conclusion is preregistered.

## Evaluation, accounting and protection

Only TRAIN is scored initially. Final original TRAIN/HOLDOUT views are scored after step200 and
again after checkpoint reload. C242.evaluate and its C234 renderer/metrics are reused, with
normal/evidence_blind/query_blind views only. No held-out result changes subsequent optimization.

6x200=1200 updates/38400 ordinary training presentations. Per model192 initial scoring rows plus
288 final and288 reloaded scoring rows. Totals90 evaluation forwards/4608 scoring rows;
1290 model forwards/43008 total row presentations. Before reload209 calls/6880 rows per model;
after215/7168. One new six-state checkpoint bundle, no parent model inference or network call.

Reuse C244.replay_one, whose six-forward/288-row replay contract is independent of training length.
Do NOT use C244.summarize for the child because it requires200 updates per block; the child has100.
Use C246.summarize(records,C244,C242) only for the actual parent measurements. Validate that schema,
parent discrete metrics, child counts, original comparator metrics and all file identities.

Postcheck verifies plan,partition,hashes/sizes,initial fingerprints, both unchanged comparators,
summary and discrete metrics reconstructed from child predictions. Exact argmax and1e-9 logit/
metric replay are required. Any execution/integrity fault is INVALID / RETRY SAME C247.
No full-checkout or real-model validation is implied by synthetic authoring tests.

Preserve all accepted sources/tests/logs. No larger model, paid API, external corpus, cleanup,
history rewrite or production modification. Numeric-memory tuning remains paused. Judge C247 before C248.
