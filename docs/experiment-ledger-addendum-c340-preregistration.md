# C340 preregistration -- original-length5 training boundary

Date: 2026-10-28 Japan time.
Experiment C340-v5b-length5-training; stage V5-B-LENGTH5-TRAINING.
Accepted scientific base aea1286c205e274611e63b14ddd26e5c99884f1f.
C339 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY); C338 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. No production adoption. Source publication is not activation.
Require independent committed-byte review PASS and a subsequent documentation-only
ACTIVE registration before giving the user an execution command. C341 NOT REGISTERED.

## One scientific question

At the same2400-update budget, does replacing only original-length4 TRAIN tokens
with canonical original-length5 TRAIN tokens improve transfer to never-trained
original6 while retaining the shorter-task and interior4 gates?

C339 reconciled the complete saved C338 cohort without new fitting or inference.
Normal HOLDOUT original6 correctness decreased1389->1375/1440 and absent-digit
errors increased27->49 under the support-loss arm. Pooled within-pair NLL improved
but support NLL worsened. The selected seed338004 example must not be generalized
to all seeds. These results motivate a TRAIN exposure intervention, not another
support coefficient sweep or an assertion that the mechanism is already known.

## Single changed variable and fixed controls

Arms are original4(control) and original5(candidate). Both use ordinary mean CE256
and native_before readout during training, evaluation and replay. No support loss,
extra labels, inference filtering, changed target, architecture, capacity, attention,
optimizer, model-selection rule or output repair is introduced.

Prepare both sets of tables from the canonical data and prompt writers. Keep the
original schedule indices2/3/4 and its family mask unchanged. Only the three
original-family slot4 tables are replaced by original5 normal TRAIN prompt tokens.
This preserves interior4 selection even when it shares a schedule slot with the
changed original family. Validate all192 source IDs and targets against the TRAIN
rows, the canonical prompt hash, table dtype/shape and the exact changed-key set.
HOLDOUT logical rows, masked controls and original6 never enter the fitting loop.

|Actual TRAIN domain|Control exposures/row|Candidate exposures/row|
|---|---:|---:|
|original2|200|200|
|original3|200|200|
|original4|100|0|
|original5|0|100|
|original6|0|0|
|interior4|100|100|

These counts are across both cycles,600presentations per logical TRAIN row.
The original5 candidate now sees its normal TRAIN templates/value combinations.
Its original5 HOLDOUT still uses held-out value combinations, and original6 remains
outside training in BOTH arms. Do not describe every evaluation domain as equally
unseen or interpret the intervention as universal arbitrary-length generalization.

## Paired cohort, data and learning

Seeds340001..340005; order seeds340101..340105; all five pairs are mandatory.
Construct both members of each pair before fitting either, require identical full
initial/core state hashes and disjoint parameter storage. Use fresh models only,
never accepted C338 weights. No seed removal or final/intermediate checkpoint choice.

Canonical192TRAIN/96HOLDOUT rows and SHA remain
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Values are two distinct members of0..3, encoded as byte classes48..51. HOLDOUT value
pairs stay(0,2),(1,3),(2,0),(3,1); preserve both languages and every registered profile.
Unchanged C332/C329/C326/C324 helpers supply canonical data, table construction,
schedule, family masks, native architecture and scoring.

Use the C326 batch4/two_to_four schedule,1200events repeated twice,48rows/update.
Paired targets/events/masks/order/rates/FIT_RNG612000 are identical. One core_slow
AdamW optimizer per model continues through the two cycles: noncoreLR.005/coreLR.0005,
betas.9/.999,eps1e-8,weight_decay0,globalgradientclip1. No restart or intermediate
evaluation. Compare post1200 and pre1201 weight/optimizer hashes for continuity.
The only loss is ordinary cross_entropy over all256classes and the correct target.

Architecture14256parameters/core3328,64slots/padded input positions,CPUfloat64,
2Torchthreads. Final states are detached deep copies. ALL10fitting runs finish
before scientific evaluation begins. Training input hashes differ between arms,
while logical row/target/event/mask hashes and initial weights must agree.

## Token and work accounting

Equal updates, rows and padded64 input shapes do not imply equal nonpadding exposure.
The actual fitting loop counts nonpadding tokens, including BOS/EOS, and saved
semantic reconstruction recomputes them from canonical tables and schedules.

|Arm|Updates/model|Rows/model|Nonpadding tokens/model|
|---|---:|---:|---:|
|original4|2400|115200|3110400|
|original5|2400|115200|3225600|

The candidate receives115200additional nonpadding tokens/model,576000across its
five models. These values also appear in seed_results for console-log inspection.
This is an exposure comparison at equal update budget, not a claim of equal
semantic byte exposure or measured wall-clock/FLOP equality.

Scientific cohort work:10training+10evaluation model instances,10final states,
24000gradient calls/optimizer steps,1152000TRAIN rows. Evaluation/replay adds3420
model forwards; totals27420model forwards,1480320row presentations,109680core
forwards,54840query projections,20state loads,1bundle load,1bundle write,0network
calls. Raw-logit payload672399360bytes is neither serialization total nor peakRAM.
Tests, parent evidence reconstruction and discarded preflight are separate work.

Preflight checks all5real schedules/both arm tables and actual exposure. A discarded
native model tests original/interior English/Japanese inputs in both arms:
8forwards/16rows/4backwards/0updates,with nonzero output weights and finite gradients.
It does not demand equal logits for the changed-length inputs. The probe weights
remain unchanged and are never reused as a scientific model.

## Evaluation and fixed gate

Each final model is loaded/evaluated/reloaded/replayed using native_before and
unchanged all256-class argmax. Retain all114views:original1..6/interior4,both logical
splits,all profiles/languages,normal and masked controls. Require raw replay drift
<=1e-9 AND exact argmax, immutable state/data/prompt fingerprints and matching receipts.
Original1 remains descriptive. The target or supplied pair never restricts inference.

Use unchanged original/interior scorers and paired query grouping. Existing local
thresholds remain accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,both_order.80.
Retain per-domain correct/both-query-correct counts and rescued/regressed answers/pairs.
C338.support_report/C337.audit_logits supply descriptive correct/wrong_observed/
absent_digit/outside_catalog partitions,288normal HOLDOUT answers/domain/state.
These partitions add neither a support-loss term nor an additional support-error gate.

C340 PASS requires ALL of the following, fixed before any new scientific result:
1. All5candidate states pass the complete original2..6 AND interior4 gates.
2. For EACH paired seed, original6 correct-answer and both-query-correct gains are
   nonnegative; pooled original2..5 gains and interior4 gains are also nonnegative
   for BOTH measures. Individual short-domain results remain reported; the retention
   contrast is explicitly pooled, so this does not assert zero local short-domain harm.
3. Summed over the5seeds, original6 correct-answer AND both-query-correct gains are
   strictly positive. Perfect-control ties do not waive this requirement.

This is the C332-style capability contrast applied to a fresh exposure experiment,
not a retrospective change to C338's support-loss gate. A valid tie, saturated cohort
or failure of any fixed criterion is ACCEPTED VALID NEGATIVE. It is not a reason to
retry with new seeds, larger capacity, more updates or a more favorable criterion.
PASS supports this fixed cohort/intervention only; Gate F completion, production
adoption, an optimal curriculum and a universal length mechanism remain unclaimed.

## Immediate C339 parent and complete evidence protection

Execution f58c22f83fe7c41c451d5d0bcf26c249ab21908b.
Publication71585b7eb2da7685915bb30b43376b1ea1ffec9b.
Folder runs/c339-support-transfer-38b97ac63a92445cb0b212d1fe9a73fe/.
Primary304dec1fcbb6532da968fd21c337f39079f4abb1cc305893722e466636ef4dbf.
Envelopedb81d2dba1bd8a1b2f850c3b5a7833a9b95b7a24d8cddc984fc1e3a5e1195be3.
Require fold-c339-diagnostic-v1/PASS,capability_gate_applicable=false,diagnostic valid,
parent_candidate_gate=false/eligible0,full6202receipt,895sources/5769inputs and all
5769final uncached rereads. This diagnostic parent is distinct from a trained parent.
Pin executor27c83c8b5a3af364475a73ffd1563607255607ad and benchmark
edde2009f4b8135199eea993d2a85aa987e87d4b before import; preserve the helper dictionary ABI.

Reconstruct inherited maps using unchanged C339.snapshot. Add ALL467C339outputs:
4science files+primary+envelope+461test proofs(3records+229receipt/log pairs).
Validate all parent test IDs,success/PID/log evidence and byte hashes. Add7OWN files:
benchmark,executor,2test modules,runner,launcher,this preregistration. Protection is
902sources=895+7 and6243inputs=5769+467+7. No source/input overlap or missing dependency.
Inspect actual direct/lazy deciding imports, including C338/C337/C332 and their
inherited canonical helpers. No execution-HEAD-only substitute for explicit pins.

Immediate parent reconstruction is the actual FIVE-argument call:
C339.semantic_recheck(C339science,C338science,C329data,C338validation_summary,read).
Load the C338validation_summary from its own protected primary file and check its
accepted SHA. Run this under no_neural,then validate canonical data/prompts. Do not
call a stale trained-parent signature or recursively rerun C338semantic/model code.
All ancestor bytes remain protected even though older semantic bodies are not rerun.

Native R4 read leases span checks/regression/science/reconstruction, with explicit
finite max_files=6243. Keep independent initial hashes and ALL6243final uncached
rereads. No default4096 capacity,eviction,unlocked fallback,omitted proofs or edited
accepted source/tests/contracts/logs/dispatchers. Publication-only repairs never
change scientific data, and this experiment does not edit accepted code.

## Regression, artifacts, launch and stop

Preserve all6202ordered parent test IDs, SHA
b5d92857cbb2c72d61a1e2a9af242f57e283fd7c26e5e6e86661d6cbdb35fbf4.
Append actual32science tests then24execution tests:6258selected/231modules,
6259before the sole inherited exact C204mutable-ACTIVE exclusion. No new exclusion,
skip,cached success,accepted-test edit or automatic retry. Build real loaders and
check ordered IDs/counts,not numeric source-string literals. Each module runs in a
fresh sequential process with accepted C330R1.2 direct/immediate-child PID validation
and canonical begin/end markers. Generic module ABI binds the NEWHEAD and test plan.
Own plan/evidence schemas fold-c340-regression-plan-v1/fold-c340-regression-v1.
All6258tests must pass before scientific fitting. Module-level OK is insufficient.

Six scientific outputs:experiment-plan.json,training-traces.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json. Bundle schemas are
fold-c340-trained-models-v1 and fold-c340-evaluations-v1. Primaryfold-c340-trained-v1
and envelopefold-c340-execution-envelope-v1 bind source/input maps and execution HEAD.
Hash/size-bind all6outputs around saved reconstruction and before final records.
Child saved reconstruction uses C340.semantic_recheck(out,data_out,cx,read),the
four-argument trained-child contract. The fresh verifier independently checks
proofs/persistence/metrics and actual token fingerprints; it does not independently
replay24000optimizer steps. A successor must preserve473C340outputs:
6science+primary+envelope+465proofs(3records+231receipt/log pairs).

Route:invoke_active_v2->invoke_c340->run_c340->c340_execution->native locks/parent
snapshot->immediate C339semantics->discarded native preflight->6258isolated tests
->10fresh fits->native evaluation/replay->saved reconstruction->6243final rereads
->independent fresh verifier->console-only c340/latest.log+latest.json publication.
Local prefix runs/c340-length5-training-<id>/. Native runtime remains Windows
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5 and PowerShell7; no environment reinstall.
Branch/tracked-tree/ExpectedHead/uniqueACTIVE/dependency/AST guards precede logging.
Stale requests skip without scientific execution or publication. The standard user
block parses active_v2; dispatcher parses invoke_c340; launcher parses itself/runner.

Progress prints every200updates,each seed/arm,all10state results,5paired contrasts,
regression module progress and verification heartbeats. Completion requires native
full regression,training/replay/reconstruction,6243rereads,fresh verifier,
run_execution_valid=true and successful log publication. StatusFAIL is scientifically
valid when those integrity checks pass. Source/input/regression/PID/nonfinite/
gradient/pairing/schema/replay/reconstruction failures are INVALID SAMEC340.
Publication-only failure repairs publication without retraining. C341 waits for
formal judgment. No CI,paid service,accepted model retraining or artifact deletion.

## Mandatory independent committed-byte review

After publishing all7files,reread remote bytes through EOF and compare Git blobs
with tested local content. Rerun56tests normally and under CP932-default-text-open
emulation. Audit UTF8/noNUL/compile/import/free names,actual6258test-ID inventory,
manifest/work/counts,source protection,parent5-argument/child4-argument dispatch,
all3profiles'actual token replacement,unchanged family masks/native readout/CE,
CLI/PowerShell ordering and prelogging skip guards. Review by someone other than
the source author must PASS before a separate documentation-only ACTIVE commit.

Author tests use the real canonical dataset/renderers/tokenizers/schedules/native
model preflight/scorers and saved archive reconstruction. The2400-update continuity
check uses a small Torch model,not a formal trained FOLD result. Worker/fresh-verifier
and full proof-map tests use explicitly synthetic parent/OS/scientific collaborators.
Record those limits; neither56author tests nor suite construction equals6258native
tests or the ten-model scientific run. Any review fixes require a renewed remote
reread before approval. Record review target HEAD and post_authoring_review=PASS.

Manifest SHA256:8016f388949a574a3609a563d1005c99b1c83455cd31148471f60a7c9b832914.
