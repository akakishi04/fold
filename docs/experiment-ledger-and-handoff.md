# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C292 ACCEPTED PASS (diagnostic integrity only). C293 NOT REGISTERED.**
Scientific execution:4e7d4468a103fa70dcfaee719fcf6daa75af5b7e.
Published log:513f820c494e067e67d1c3757af09cf7642b0b90.
C291 remains ACCEPTED VALID NEGATIVE. No rerun or Gate F promotion.
No ACTIVE experiment until C293 is preregistered,committed and independently reviewed.

## Latest accepted evidence — C292

Acceptance:docs/experiment-ledger-addendum-c292-c293.md.
Summary:runs/c292-v5b-answer-roles-ba65b6ac20ac46e5b08fe96a5e5a8e74/summary.json.
Summary SHA256:44aa5ddbe5856ffdd7a62f63ac7574367527fab17c447c02ca68f7071e9ae513.
Manifest:f45b635e637d043d7b5dfeb2c65abed847a0b7d47ae3dd0cb4f0ce6c7f4f2869.
Own32/focused4317 PASS;source598/protected1081;run_execution_valid=True.
38880 saved normal answers classified;scientific neural calls/training0.
Candidate291003 HOLDOUT errors at lengths2/3/4:63/72/77;absent known values62/71/72;
other-fact values1/1/5;non-value bytes0/0/0. Of212 errors across these partitions,205 are absent.
This does not prove memorization or hidden retrieval failure. Parent gates stay CE4/pair2/answer4.

## Next registration boundary

Potential next comparison:CE versus1.25*CE versus CE+.25*unordered-fact-support NLL.
No new model input,inference restriction,training data,length or budget is authorized by this
acceptance alone. C293 must use a separate preregistration and committed-byte review.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c292-pre-acceptance.md.
Its Git blob is43e27532c735595d9a2c1c8b5f189093f4a595ba. Older handoffs remain unchanged.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
Accepted source/tests/logs/preregistrations and protected dispatchers remain immutable.
