# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C288 ACCEPTED VALID NEGATIVE. C289 NOT REGISTERED.**
Scientific execution:f43618b6bb6fcc1ad4a4a4b928992adce29f4e41.
Published log:eb9f27224460ad614e80b5feb23a5411d8ea42d6.
C287 remains ACCEPTED PASS (diagnostic integrity only). No C288 rerun or seed filtering.
No ACTIVE experiment until next preregistration and committed-byte review are complete.

## Latest accepted science — C288

Acceptance:docs/experiment-ledger-addendum-c288-c289.md.
Summary:runs/c288-v5b-pair-assignment-f6a7427e94c44fc7b818f8cd18626562/summary.json.
Summary SHA256:2a15fbf6c5e697d5e226bdae5a5b2f243f43625b29255839100d2f05ce24fbc0.
Manifest SHA256:44b114f22e06b214f3567baea16cc8771da55566e128c3c2d35b47023ba313d5.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False. Own40/focused4157 PASS.
Source574/protected1026. Work:10 models,8000 updates,384000 training rows,9620 forwards,
539520 row presentations,38480 core calls. Strict replay and persisted reconstruction PASS.

Quad primary ce_only3/5,ce_pair_assignment1/5;two3/3;triple3/3;all tasks3/1.
Trained-length TRAIN direct3/5 versus5/5;seen-length HOLDOUT direct3/5 versus3/5.
Candidate fits all TRAIN examples at both lengths2/3 exactly with no collapse,but288002/288003
still fail seen-length HOLDOUT. Candidate loses quad-only gates288001/288004;only288005 passes.
Pooled quad correct3902->4011 of4320;collapse175->90 of2160. Pooled improvement does not undo
reliable-gate regression. Do not claim universal transfer degradation or an adopted solution.

## Next question pending registration

Test early-only versus always-on pair auxiliary at fixed800-update budget,with a concurrent CE-only
anchor. All three arms should use matched fresh seeds,data,LR and capacity. Switch at update401;
no optimizer reset. Common first400 state/loss identity must be verified for always/early arms.
This is a bounded policy test,not a diagnosed late-pressure cause. C289 remains unregistered here.
No execution command before separate next-C preregistration,committed-byte review and activation.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Later lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoffs remain under docs/handoff-history/c280-pre-acceptance.md through
c288-pre-acceptance.md. The latest preserves Git blob2b3efa437e7fb91d35dc59894329904a00055646.
Only this Formal state is authoritative. Accepted source/tests,preregistrations,logs and protected
dispatchers remain unchanged. Earlier C287 chat claims are superseded by its acceptance addendum.
