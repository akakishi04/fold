# C182 preregistration — frozen fact-index renaming

V5-E. Registered AFTER C181 acceptance bd3117087e2a1aefd99c3e07e54269015c0099fa.
Repository akakishi04/fold; branch feat/sft-target-loss; use final registration HEAD.
**C182 ACTIVE / NOT YET JUDGED. C183 NOT REGISTERED. Gate E NOT PASSED.**
C181 remains ACCEPTED PASS and all historical negatives remain unchanged.

## One scientific question

Do ALL three frozen C181 INTERNAL_SEMANTICS base models preserve their zero-error
necessity decisions when fact indices and their complete fact records are consistently
renamed, while formula connectivity, operators, negation and visible meaning stay fixed?

C181 saturated the repeatedly inspected four development groups. Its supplied syntaxes
always order leaf fact references1,2,3,4. Perfect original scores do not establish
robustness to another reference-index convention. C182 tests this specific limitation,
not another loss, larger model, new seed or more training on the saturated pilot set.

## Frozen model and integrity boundary

Use all six C181 FINAL checkpoints, seeds181001/181002/181003 and both FINAL_ONLY and
INTERNAL_SEMANTICS. No selection, fine-tuning, ensemble or checkpoint replacement.
Hash all eleven C181 artifacts and validate the complete checkpoint metadata and
full25921parameter fingerprint against the accepted summary's per-model fingerprint.
Deserialize each of the six checkpoints ONCE with weights_only=True. Construct ONLY
the original C179 SharedGraphProbe TREE_LINKS base, load its25726parameters, disable
gradients and use original graph.predict, batch1024. The auxiliary head is not
constructed or called. Its stored tensors are checked for fingerprint/shape integrity
but are not used in prediction. No SemanticProbe.restore, teacher_targets, optimizer,
proof checker, teacher-forced state or auxiliary inference call is used.
Temporary initialization is overwritten by frozen weights with RNG state restored;
there is no new training seed. No new model checkpoints are saved.

Before new tests, replay all six models' C181 TRAIN and PILOT inputs. Require EXACT
raw-argmax decisions and logit absolute differences <=1e-6, relative tolerance0,
against saved logits. Reaggregate saved logits/decisions and C181 metric tables.
A replay/source/schema/nonfinite disagreement invalidates this execution; it is NOT
silently repaired or counted as new-condition scientific failure. No tolerance change.
The test process is a fresh benchmark invocation, not the previous training process.

## Changed variable: consistent old-index -> new-index renaming

Enumerate all24permutations of zero-based indices(0,1,2,3) lexicographically. Identity
is the source replay. For EACH of the remaining23permutations, transform every one
of the9396C174 PILOT rows, preserving its original row identity and label:
- a FACT reference to old index i becomes p[i];
- move the ENTIRE old fact record to new slot p[i];
- retain every operator, child link, leaf negation, header and runtime field.

Then apply the unchanged C178 visible-leaf binding preparation. The bound presence
and visible bit at every formula leaf must be identical to the original. No Boolean
expression evaluation or new teacher labels are generated. UNKNOWN remains UNKNOWN;
observed zero is never confused with absence. The transform has no label argument.

Example: rename A->C and C->A while moving their records together. The naming and
fact-table positions change, but each formula leaf reads the same visible information.
This is NOT an independent shuffle of values that would change the logical problem.

Novelty check: all51840original rows have canonical leaf naming1,2,3,4 and PILOT9396
raw rows are unique. Bijective transformations have23distinct noncanonical leaf naming
orders, so216108transformed raw inputs are unique and none equals an original numeric
input. Semantic groups and logical problems are STILL the old reused development tasks.
This is a metamorphic naming robustness test, not independent semantic generalization.
Variable count/depth, repeated-variable reasoning, language and live policy are not tested.

## Fixed workload

|Quantity|Registered|
|---|---:|
|Source checkpoints / source seeds|6 / 3 reused|
|Fresh seeds / training updates|0 / 0|
|Original identity replay predictions|311040|
|New numeric inputs|216108 = 9396 x 23|
|New-condition predictions, all six models|1296648|
|New-condition candidate predictions, three internal models|648324|
|Total main inference predictions|1607688|
|Forward batches / shared-cell calls|1692 / 11844|
|Teacher / auxiliary-head forward calls|0 / 0|
|Acquisition / proof / evidence / network calls|0 / 0 / 0 / 0|

CPUfloat32,2threads,deterministic algorithms,batch1024,original7cell applications/row.
Same frozen weights, decision rule and logical inputs; ONLY reference-index convention
changes within each model. No claim of equal total work to the original C181 experiment.
Pairs/rows/permutations overlap semantically and are not independent observations.
Control FINAL_ONLY models are included for descriptive comparison, not discarded for
poor accuracy and not required to become perfect.

## Fixed deciding gate

For EACH INTERNAL_SEMANTICS checkpoint, EACH nonidentity permutation and EVERY9396
row, require raw main argmax correct and identical to the original correct decision.
That is zero errors and zero decision flips in all69candidate model/permutation cells.
All138model/permutation cells must complete; all six identity replays must first pass.
A single finite new-condition candidate error produces VALID NEGATIVE. No majority
vote, average-score rescue, case dropping, threshold adjustment or logits correction.
FINAL_ONLY errors are reported but are not a gate condition. Exact logit invariance
under renaming is NOT required: confidence values may change without a decision error.

PASS supports frozen main-decision robustness to these23reference renamings.
VALID NEGATIVE establishes a limitation under renamed inputs; C181's original PASS
remains unchanged. Freeze and retain every outcome. No retraining or case/seed changes.
INVALID covers source/artifact/schema/transform/replay/nonfinite/incomplete/protection
errors; restore validity of the SAME C182 without changing scientific conditions.
Neither result is final Gate E or proof of general learned symbolic semantics.

## Diagnostics, outputs and protection

Save raw float32 logits/int8 decisions for all new-condition rows. Save model/permutation
metrics, group/count confusion, errors, decision flips and rescued/regressed decisions
relative to original output. Aggregates are descriptive; they cannot hide one failure.
No further unchanged-score-only diagnostic is needed to find error strata.

Outputs:renaming-plan.json,transform-audit.json,frozen-replay.json,
renaming-results.json,renamed-predictions.npz,complete summary.json. Five artifacts
excluding summary; no transformed dataset or source checkpoints are rewritten.
The NPZ uses model6 x permutation23 x row9396 order and contains permutation mappings,
source row indices, model seeds and arm indices. Details remain in an artifact instead
of dumping every large confusion table into the terminal.

Reuse C181.precheck over all earlier sources, then protect accepted C181 summary and
its11artifacts. Historicalsourcepins76+4ownfiles;151unique protected input paths,
plus outer C37/composition-fixture guards. Standalone paths only.
Parent summary bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98;
source execution HEAD3ec4cd8f2afc664799f1e6bfecfce457dd255ad4.
Manifest SHA2564aa37d094447417e466048f92d2b4949296078ab77d00f5d7d4b24ec46ff55d5.
Production runtime, old sources/checkpoints/preregistrations and Gate E contract unchanged.

## Implementation review and execution limits

32/32new helper tests passed using actual new code with locally transcribed fetched
C179model/predict and C178/C174preparation definitions. NOT a full Git-blob-identical
checkout. Local Git network resolution failed; no complete source/artifact integration
or deciding checkpoint execution was possible here. Test data and checkpoints are
synthetic, with no training or experiment-score evaluation.
Independent Boolean completion enumeration checks9720synthetic renamed rows
(5tree shapes x81partial assignments x24permutations). Other tests cover inverse and
composition, whole-record binding, visible-bit preservation, hidden-payload rejection,
base-only restore, full fingerprints including unused head, frozen parameters,
RNG preservation, numerical parity, replay tolerance and strict all-case gate.
Historical regression-list test mocks predecessor;formalrunner resolvesREALlist.
New module/test compile;three embedded runner Python blocks parse.
Full1185tests,WindowsPowerShell,all151inputs and official1607688prediction batch
remain UNEXECUTED. No C182 scientific result has been measured by the reviewer.

**1185expected=1153+32;66modules**,one regression then one frozen batch.
Run tools/run_c182.ps1 with C181/C180/C179/C178/C177/C176/C174 summaries and expectedHEAD.
Progress:precheck/regression;311040identityreplay;permutation1/23..23/23withcandidateerrors;
1296648newpredictions;RESULT/POSTCHECK. Judge C182 ->ledger/handoff->next;no C183 yet.
