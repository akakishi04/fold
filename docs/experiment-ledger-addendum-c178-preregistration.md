# C178 preregistration — visible-fact binding at syntax leaves

V5-E. Registered after C177 acceptance commit ca8e3cf35e310372bf293327f28314d6f2d1f9fc.
Repository akakishi04/fold; branch feat/sft-target-loss; use final registration HEAD.
**C178 ACTIVE / NOT YET JUDGED. C179 NOT REGISTERED. Gate E NOT PASSED.**
C177 remains ACCEPTED PASS under its narrow ordering gate; C176 remains ACCEPTED VALID
NEGATIVE. C174/C175 and all older results/checkpoints/preregistrations stay unchanged.

## One scientific question

Does explicitly binding ALREADY VISIBLE facts to the FACT leaves that refer to them
improve necessity classification, under the same small MLP, training data and workload?

C177 ordering gains were small, same-visible-key AUC improved in only one seed, and raw
classification regressions still exceeded rescues. Do not continue unchanged-logit audits
merely to find another favorable endpoint, and do not calibrate a threshold to rescue C176.
Source inspection shows the original MLP receives fact indices in syntax nodes and a
separate fact table. It must learn that indirection as well as Boolean composition. This
is a candidate bottleneck, NOT an experimentally established cause of past errors.

Changed variable: scaled input representation only. Compare INDIRECT_FACTS with
BOUND_VISIBLE_FACTS. Both retain the full original syntax, fact table, resources, indices
and all already-visible information. Loss is ordinary UNWEIGHTED cross entropy in BOTH
arms. Conditional weighting from C176 is NOT carried forward. Same unchanged C174 MLP
class, dimension72, 26114parameters, initial weights within seed, row-index sequence,
optimizer and 2000updates/model. This is a new experiment, not repair/retraining of C176.

## Exact input transformation; no solver or hidden value

The frozen C174 data has four facts and seven ordered read-once syntax nodes per row.
Each node's six original fields are active-mask, kind, fact-index, left-child-index,
right-child-index, negate. A FACT leaf's two child-index fields are canonically zero.

1. INDIRECT_FACTS is exactly original api.prepare(raw,TASK_VISIBLE).
2. BOUND_VISIBLE_FACTS starts from that same scaled vector.
3. At FACT leaves only, replace the two zero child-index coordinates with the referenced
   fact's observed-presence and raw observed bit, each represented as float32 0/1.
4. For an unobserved/unusable fact, these are 0/0; observed zero is 1/0 and one is 1/1.
5. Do not apply leaf negation, AND, OR, truth-table evaluation, dependency inference,
   proof checking or expected-label-based features. A negated observed-one leaf is still
   annotated with raw observed-one; the model must learn how negation affects the task.
6. All internal-node child pointers and their original scales stay exact. Leaf fact IDs,
   negation flags, original fact table, statuses and resource fields are unchanged.

Only the eight leaf placeholder coordinates per row are used for the copied fields.
Zeroing those coordinates exactly recovers the original scaled input. The information
was present already; this reorganizes/duplicates it rather than injecting unknown facts.
The transform has NO label/group/expected-action argument and uses no TRAIN/EVAL statistics.
Numeric guards reject invalid masks, links, fact IDs, hidden payloads and unsupported shapes.
It is restricted to this read-once C174 family, not a universal C170 input adapter.

The transformed vector is NOT a C170 PolicyInput: it has a different explicit diagnostic
representation version. Both modes bind that representation string in checkpoint metadata
and roundtrip checks. The old model class is reused only as the same numeric MLP. No old
packet schema, consumer contract, historical checkpoint or production runtime is modified.
Handwritten index lookup is part of this candidate front end, NOT learned binding.
This intervention also activates previously zero input coordinates; unchanged parameter
count is not a proof that all effective expressivity/conditioning is identical. A gain
supports this representation package, not a unique internal mechanism or reasoning claim.

## Frozen workload, baseline and outputs

New seeds178001/178002/178003; two new models per seed, six total. No historical weight
initialization or continuation. Both use unchanged C174 api.fit: Adam lr0.001,
betas(.9,.999),eps1e-8,weight_decay0,amsgradFalse,foreachFalse; batch256,2000updates.
Private uniform-with-replacement row RNG=seed+1000000. Same initial and schedule hashes
required within each pair. CPUfloat32/two threads/deterministic algorithms.

Reuse original C174 NPZ/metadata and split without regenerating or selecting cases:
TRAIN36groups/524templates/42444rows; PILOT_EVAL4groups/116templates/9396rows.
Data SHA256 eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65.
All transforms are deterministic visible-field operations; only TRAIN rows/labels enter fit.
All six FINAL checkpoints must be saved/reloaded before ANY model score is produced.
No early stopping, best-checkpoint choice, extra updates, new seeds or threshold fitting.

|Work|Registered total|
|---|---:|
|Prepared original rows, each with two representations|51840|
|Visible leaf-to-fact lookups|207360=4x51840|
|Copied numeric fields|414720=8x51840|
|New models / initialization seeds|6 / 3|
|Training forward / optimizer updates|12000|
|Sampled training rows|3072000|
|Pilot predictions|56376|
|TRAIN resubstitution predictions|254664|
|Inference batches|312|
|New checkpoint roundtrip loads / historical loads|6 / 0|
|Actual acquisition / proof checking / evidence writes / network|0 / 0 / 0 / 0|

Preprocessing is performed once before training, not called a free learned computation.
Its lookup/copy counts and benchmark wall clock are recorded. No production speed or
VRAM saving claim follows from the fixed input width or parameter count. Tiny training
inside regression is separate from the registered batch totals.

## Primary and exact decision

Primary: equal arithmetic mean BA within missing counts1,2,3 on reused PILOT_EVAL.
Use the same joint improvement conditions as C176, now comparing bound versus indirect:
For EACH of three paired seeds, require ALL:
1. bound primary > indirect primary;
2. bound original four-semantic-group macro BA >= indirect (no decline tolerated);
3. bound count1 NEEDS recall > indirect count1 NEEDS recall;
4. bound count3 SUFFICIENT recall > indirect count3 SUFFICIENT recall;
5. both bound aggregate class recalls >0.5.

No seed average can hide a failure. Same score fails conditions1/3/4; equality is allowed
only by condition2. These are preregistered directional DEVELOPMENT criteria, not a
practical reliability threshold, statistical-significance test or Gate E final gate.
C178 does not retroactively alter C174-C177 metrics or adoption decisions.

PASS: valid complete batch satisfying the joint gate. It supports this representation
under this model/data/budget, NOT a proof of learned binding, general logical reasoning,
FOLD shared-core performance, target/tool selection, proof generation or safe live control.
VALID NEGATIVE: finite valid complete batch missing any gate condition. Preserve all models
and errors. Do not change weights, input coordinates, seed list, steps or thresholds to pass.
INVALID / RETRY SAME C178: source/hash/schema/lineage drift, unpaired fitting, malformed
input or output, nonfinite numerical state, unexpected exception, incomplete workload or
protection failure. Restore validity, not scientific settings. Preserve invalid.json and
completed fit records. Finite scientific FAIL saves complete outputs and exits0.

## Batched secondary analysis, not additional success gates

Save original group/count confusion matrices and both recalls, ordinary accuracy, raw
logits and predictions on BOTH splits. Also compute within-count and same-visible-key
AUC, and paired error rescues/regressions/flip directions by count on TRAIN and PILOT.
TRAIN logits are saved this time, rather than silently requiring a later model rerun.
Missing counts0/4 have a pure class: BA and pair AUC are null, while accuracy is retained.
Pair combinations overlap; never count them as independent samples. No calibration or
threshold is selected from any table. Do not replace the classification gate with AUC.
New seeds do not make the four repeatedly inspected pilot groups an independent holdout.

## Lineage, source protection and files

Parent C177 runs/c177-v5e-score-order-c18e0ed086f34e0aada4635e907e470f/summary.json;
SHA25699f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4.
Also require original C176 and C174 summaries and all their artifacts via unchanged C177
precheck. Verify the two C177 artifacts; old checkpoints are hashed but never loaded.
Historical pins60=56C177source pins+4C177own paths at691b6df851525469889fe3640e638411ea284b58.
Four new own files pinned to current execution HEAD; 90 unique input paths protected.
All paths are standalone. C37 and composition fixture receive additional runner guards.

Fresh UUID output: leaf-binding-plan.json BEFORE learning, input-binding-audit.json,
six checkpoint files, pilot-predictions.json, training-predictions.npz, summary.json.
TRAIN NPZ additionally carries logits and explicit seed/arm identities, without pickle.
Ten listed artifacts (excluding summary itself), hash/byte sizes retained; no old artifact
is overwritten. Old C174-C177 source and preregistrations are unchanged.
Scientific manifest SHA2564393da528c6193cd2d8762cfea081e102e02537148299578806b0f3dcb9facc0.

## Verification and run

32/32 new tests passed using the actual new module and Git-blob-identical copies of
original C170 structured_task_input and C174 structured_necessity_probe. PyTorch2.10CPU /
NumPy2.3.5. Tests cover exact control preparation, masked known-zero, pointer binding,
non-computation of negation, unchanged syntax/resources, input immutability, malformed
inputs, paired toy fitting, representation-bound weight roundtrip and strict gate.
Toy fitting uses two synthetic rows and TWO updates, not the registered learning run.
Two new Python files compiled; all three embedded runner Python blocks parsed.
Full historical regression/dependency/artifact integration, Windows PowerShell, the1057
tests and the formal six-model2000-update experiment have NOT been executed by reviewer.

**1057 focused tests expected=1025+32,62modules**,one regression then one CPU paired batch.
Run tools/run_c178.ps1 -C177Summary ... -C176Summary ... -C174Summary ... -ExpectedHead ... .
Progress:source/artifact precheck,regression,plan,seed/arm every500updates,three paired BA
lines,RESULT/POSTCHECK. Return full log even when scientific_status=FAIL.
Judge C178 -> ledger/handoff -> next design. **No C179 before formal judgment.**
