# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted code/tests/preregistrations/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C308 ACCEPTED PASS. C309 NOT REGISTERED.**
C308 PASS is bounded capability,not merely diagnostic integrity. No ACTIVE experiment yet.
Scientific execution:2fc902e8c7f57579087a61e25e7c1e88f8c66090.
Published log:045de9e384e6d19f35b48722a55b3fac1062ddbd. Do not rerun C308.
C306/C307 valid-negative verdicts remain unchanged.

## Latest accepted evidence — C308

Acceptance:docs/experiment-ledger-addendum-c308-c309.md.
Summary:runs/c308-v5b-core-lr-02b24ac7b9da4a36a14a5545bd42aab6/summary.json.
SHA256:42a2dbc75c6bf958bff26315f918fc999728196eac7fe890eee28aa392f63c8a.
Own32/focused4877 PASS;source694/protected1295;all_groups_matched=True;run_execution_valid=True.
Manifestc13d8d4ed974f977840e7cc1d84d5d60e3bfc78bdbc9384ff1f5d4906f65210f.
Every length2/3/4/5:full_train4/5,core_frozen5/5,core_slow5/5;all-length likewise4/5,5/5,5/5.
Fitted TRAIN direct5/5 in all arms;trained-length HOLDOUT direct4/5,5/5,5/5.
Full_train308002 fits TRAIN but HOLDOUT2/3/4/5=77/79/80/81 out288;frozen/slow each288/288.
Candidate meets its absolute all-five gate but has no pass-count superiority over frozen.
No broad reliability,optimal-ratio,arbitrary-length or Gate F claim is authorized.

## Next registration boundary

Repeat all three fixed policies on fresh paired initialization/order seeds. Keep ratio0.1,
1200 updates,old data/templates/thresholds and complete cohort. No post-hoc policy/seed selection.
C309 command requires separate committed-byte review and activation.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Preserve accepted seals;historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c308-pre-acceptance.md.
Git blob:528b2ed36503065cf218377cd353669c24ab2396.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
