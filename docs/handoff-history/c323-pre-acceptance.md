# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C322 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C323 ACTIVE / NOT YET JUDGED. C324 NOT REGISTERED.**
C323 is the sole ACTIVE saved-response fact-order bias diagnostic;no C323 science yet.
C321 remains ACCEPTED VALID NEGATIVE (interior-order 0/5),C320 bounded ACCEPTED PASS
(unequal lengths 5/5 mean_last);all earlier verdicts unchanged.
Latest accepted execution:b7943ab4435d68d2716e6137b596042b777f2efb.
Latest accepted publication:278e883bd5b6555aa2bef8a43e1634dc5e44e6f0. Do not rerun C322.

## C322 accepted evidence

Acceptance:docs/experiment-ledger-addendum-c322-c323.md.
Acceptance commit:a0e2221eb8f12b5a2cc8f325876a8752ed1b9eb1.
Summary:runs/c322-v5b-query-contrast-f164844010f04c24bcfda4a743b44a72/summary.json.
Summary SHA256:fdcf1f2ac893a46c900e50db93740004926c70765ca269ba0cfe7474bf4c5796.
Log SHA256:eb081b5f0f3b421dc987c1605b21efca5312438cdcad9d70865fc0fc4f7f8e85;
1173665bytes,independently verified reconstructed CRLF byte stream.
Own24/full5269 PASS;one-process regression1245.157s,failures0/errors0,exit0.
Source778/protected1467,run_execution_valid=True,tracked tree preserved.
Old4 botharms4320/4320 correct and0/2160 equal-query predictions.
Interior mean_last2211/4320 correct,1996/2160 same argmax,107/2160 both correct,
118/2160 preferred both target values,mean direction contrast0.6438573484898602.
Interior last_only2292/4320,1951/2160 same argmax,171/2160 both correct,
190/2160 preferred both targets,mean contrast0.9952475930687953.
No numerically near constant-shift differences at1e-9 across2,160pairs per interior arm.
Same argmax≠same output vector and positive relative direction≠correct256-way decoding.
C322 is diagnostic integrity PASS only,not model improvement/Gate F success.

## Active C323 — fixed fact-order counterfactuals on saved logits

Experiment:C323-v5b-saved-fact-order-bias. Stage:V5-B-SAVED-FACT-ORDER-BIAS.
Registration:docs/experiment-ledger-addendum-c323-preregistration.md.
Design:docs/v5b-saved-fact-order-bias-v0.1.md.
Review:docs/c323-post-authoring-review.md.
Acceptance base:a0e2221eb8f12b5a2cc8f325876a8752ed1b9eb1.
Authoring/review target:c2a9812ce53564aefd602c18e96af11e047745da.

Question:do C321's collapsed responses track the value written in the FIRST or LAST
fact position,when both fact permutations present exactly the same entities and values?
No new model inference or learning. Read all10 C319 checkpoint output records (via
the accepted C322 JSON analysis),both original4/interior conditions,three profiles,
English/Japanese,TRAIN/HOLDOUT value splits. Require canonical logical row IDs and targets.
For every logical facts/values/query pair,match exactly the2 opposite fact permutations
without choosing order by outcomes. This creates4320 four-answer counterfactual groups.
Per group: correctness0..4;both queries collapsed per order;first-both/last-both order
following;all-four-value lock;per-query response stability across order swap;
first/last/other answer-class accounting. Report240 locality groups,4 overall arms/conditions
and reconcile17280 answers and8640 original C322 pairs.
Original4 is a matched positive control;C321 interior remains untrained input.
This is NOT a causal demonstration of attention to first/last positions or a new gate.
No restricted candidate selection,score modification,checkpoint loading,new forward or training.

## Parent contract/protection

Verify49 ordered ancestor hashes BEFORE exact C322.verify_artifacts(C322dir,48 ancestors,
accepted execution HEAD),then C322.load_parent() for canonical data and C322 sealed
query-pairs.json. C322's4 outputs are JSON diagnostics,not model bundles.
Parent source blob:c93fb85922c5907c424698897de4af2888f81f77;
parent summary SHA256:fdcf1f2ac893a46c900e50db93740004926c70765ca269ba0cfe7474bf4c5796.
Preserve all778 parent source pins/1467 protected inputs;OWN6 plus5 parent outputs
and newsource protection =>784 pins/1478 protected. No protected path waiver,
accepted-file edits or new historical-test exclusions.

C323 work:10 saved models;8640 parent query pairs;4320 counterfactuals;17280
original normal answers;240 reported groups;4 overall reconciliations.
model_forward_calls=0,train_steps=0,model_state_loads=0,new_checkpoint_writes=0,
network_calls=0 in C323 science. Recursive verification/tests remain nontrivial CPU work.
Outputs:audit-plan.json,order-counterfactuals.json,measurements.json,
validation-summary.json and summary.json. Exact numerical/logical reconstruction from
reverified parent JSON,full hashes/sizes/no-overwrite enforced.
OWN24/modules208/loaded5294/focused5293;one inherited C204 exclusion only.
Manifest:8c4e9152cb11d1492cd7d88cf7caafef40a901de6c68aa44e404c1c46ff7c5de.

## Post-authoring review and performance boundary

post_authoring_review=PASS;all6 OWN reread remotely at
c2a9812ce53564aefd602c18e96af11e047745da;independent Git blob match6/6,
then full own24 normalPASS0.978s and CP932default-emulatedPASS1.030s,both exit0.
Linux/Python3.13.5/PyTorch2.10.0+cpu;synthetic parent/model/data controls.
Both Python AST and3 runner Python here-strings compile. 49 launcher fixed paths
C322..C274/postcheck argv[2:51],HEAD[51],argc52 checked.
Local tests cover counterfactual categories,49 wrong hash rejections,
784/1478 temporary-file guard,real run dispatch,JSON no-neural persistence/tamper,
semantic loaded/focused suite test IDs,CLI and no neural/training operations.
These are NOT actual Windows parent-archive validation or full5293 regression success.

C322 full5269 ordered tests actually took1245.157s;large previous suites
(c182,c304,c315,c316,c309) each accounted for~45-51s.
C323 preserves the ordered one-process full5293 regression,prior direct UTF8 progress
logs,fixture boundary timing,science stderr,fatal traces,immediate decimal/hex exits and
previous preflight-log retention. No promised runtime reduction,test bypass or retry.
Mandatory local gates:49 real ancestors/Windows pins,PowerShell ParseFile,own24/full5293,
then C323 JSON diagnostic and exact saved reconstruction. If failure,repair SAME C323.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after ff-only pull.
Expected:legacy_dispatcher_pin PASS -> active_experiment C323 ->
Validate(49parents,784/1478,actual saved query/fact-order reconciliation,
own24,full5293 ordered regression) -> authoring_runtime_preflight PASS ->
Execute(JSON-only fixed order counterfactuals,4 reconciliations,persistence) ->
published latest.log/latest.json. No auto retries or test skipping.
C324 NOT REGISTERED until formal C323 verdict;C322 diagnosis,C321 negative,
C320 bounded PASS and Gate F NOT PASSED remain distinct.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

## Historical state

Pre-activation:docs/handoff-history/c323-pre-activation.md.
Git blob:3043571b333cdcb2822a7fbaada31e6b1d826ffe.
Pre-acceptance:docs/handoff-history/c322-pre-acceptance.md.
Git blob:2a0591d6a25b64d7bf7a779ad67c076a1a6ed407.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
