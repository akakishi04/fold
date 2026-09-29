# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C282 ACCEPTED VALID NEGATIVE. C283 ACTIVE / NOT YET JUDGED. C284 NOT REGISTERED.**
C282 scientific execution HEAD:aef5aecfc438679641e59b337d7a9eb615c619a3.
C282 published log commit:b8c0462a27246cf6ff9d9024b614dbca244be2b1.
C282 mixed_length:whole4/5,two_char4/5,triple4/5;two_char_only:whole0/5,two_char4/5,triple0/5.
C283 is the unique ACTIVE frozen four-character transfer probe. No C282 rerun,threshold relaxation,
seed replacement or Gate F promotion. All10 C282 states remain in scope.

## Latest accepted science — C282

Acceptance:docs/experiment-ledger-addendum-c282-c283.md.
Acceptance commit:b597180933fcc464395ad62cc0e915e01c796871.
Summary:runs/c282-v5b-mixed-length-5ad726e62dfa4eacada5a8cda8c4c27f/summary.json.
Summary SHA256:075cb7399f62d048310bdfb1c31c93ac39ab8b3dc400578d60e062ebfdacf3d1.
Manifest SHA256:291ed152bec43b222e54851c5e4699776e220d60937a733599c37f617ed400de.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Own32/focused3949 and persisted reconstruction PASS. Registered10-model workload completed.
Mixed seed282001 fails both tasks;other mixed seeds pass both. Control seed282005 fails two-char;
all control seeds fail triple. This is substantial seen-length learning improvement,not unseen-length
success and not the fixed five-seed gate. All seeds must remain in subsequent comparison.

## Active C283 — frozen four-character transfer

Experiment:C283-v5b-frozen-four-character-transfer.
Stage:V5-B-FROZEN-FOUR-CHARACTER-TRANSFER.
Registration:docs/experiment-ledger-addendum-c283-preregistration.md.
Design:docs/v5b-frozen-four-character-transfer-v0.1.md.
Review:docs/c283-post-authoring-review.md.
Authoring/review target:cc4d71ee7edc4ae917d3535f1cd31c809da066ee.
Acceptance base:b597180933fcc464395ad62cc0e915e01c796871.

One question:do frozen C282 mixed_length states transfer better to completely unseen four-character
identifiers than their matched two_char_only states,without further training or seed selection?

Keep all10 states,seeds282001..282005,two_char_only/mixed_length,including known failed states.
Actual C278 MeanFinalDualReadout remains unchanged,14256 parameters,48-token context.
Profiles:quadrupled/shared_prefix3/shared_suffix3. Normal prompts864/model;English and Japanese,
maximum43 UTF-8 bytes. No truncation,new bytes,position-table extension or new factual entity count.
Quad dataset SHA256:86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.
Use the unchanged C270 raw-logit scorer through an explicit reversible profile-label adapter.

Each strict-loaded frozen model:original two+three anchor -> four-character probe -> original
 two+three restore. Raw/argmax replay tolerance1e-9;weights must remain identical. Replay preserves
known wrong answers instead of requiring old capability PASS. Primary four-character candidate
PASS iff all5 mixed_length states pass all fixed criteria on both value splits/all profiles.
Report every state and paired row/collapse contrasts. C282 verdict and Gate F are unchanged even
if C283 passes. A relative benefit does not isolate diversity from larger maximum training length.

Workload:zero training/optimizer updates/new checkpoint writes;existing checkpoint bundle load1;
model-state loads10;model forwards1350;row presentations129600;core calls5400.
Raw evaluation logits payload265420800 bytes before archive overhead.
Registration:source544;protected964;dependency-union59;own32;modules168;loaded3982;focused3981.
Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:e88244fe1acc677d629e3b0400dc4926be9b26560c05a782122ae1e5042213a4.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own32).
Review target:cc4d71ee7edc4ae917d3535f1cd31c809da066ee. All OWN6 fetched after commit;
6/6 Git blob identities match tested bytes. Local Linux/Python3.13.5/PyTorch2.10.0+cpu:
own32 PASS,final run1.089s;both Python files and3 embedded blocks compile;unresolved global names0.
Parent archives/scorers/model probes are mocked in relevant fixtures. No actual frozen C283
scientific result is claimed. Actual Windows parent validation,real tokens/scorer/model construction,
full focused3981,PowerShell ParseFile and scientific frozen evaluation remain runtime gates.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after ParseFile on dispatcher.
Expected order:legacy_dispatcher_pin=PASS -> active_experiment=C283 -> Validate(parent/source/artifact
544/964,real quad tokens/scorer adapter,own32,focused3981) -> authoring_runtime_preflight=PASS ->
Execute(all10 frozen states,anchor/probe/restore,persisted postcheck) -> log publication.

Validate failure skips science and scientific publication. Scientific integrity failure retries
SAME C283. Valid candidate gate miss is ACCEPTED VALID NEGATIVE. No seed selection,extra training,
new profiles,threshold changes or C284 registration before formal judgment. Gate F NOT PASSED.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads mutable handoff. Preserve this seal.
Later lifecycle-aware tests use immutable acceptance addenda after acceptance.

## Historical state and recovery

Previous full handoffs:docs/handoff-history/c280-pre-acceptance.md,
docs/handoff-history/c281-pre-acceptance.md,and docs/handoff-history/c282-pre-acceptance.md.
The last file preserves pre-acceptance Git blob d5df20dd7ca7f8350244b05fb4f754b3a581c67e.
Their ACTIVE instructions are historical only;only this Formal state is authoritative.
C281/C279 remain ACCEPTED PASS (diagnostic integrity only);C280/C278 remain ACCEPTED VALID NEGATIVE.
All accepted source/tests,preregistrations,logs and protected dispatchers are unchanged.
