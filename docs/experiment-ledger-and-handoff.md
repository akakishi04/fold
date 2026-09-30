# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C289 ACCEPTED VALID NEGATIVE. C290 NOT REGISTERED. C291 NOT REGISTERED.**
Scientific execution:b5026f48e0c8b39bbfb9069f34271d7b6ba9d50f.
Published log:b96ab8b01ec9c9eb876fada8339c8c0e0d0a8e12.
C288 remains ACCEPTED VALID NEGATIVE. C287 remains diagnostic ACCEPTED PASS.
No C289 rerun,seed exclusion,threshold relaxation or Gate F promotion.

## Latest accepted science — C289

Acceptance:docs/experiment-ledger-addendum-c289-c290.md.
Summary:runs/c289-v5b-early-pair-ac332442137243e68d4ec3bd754ba717/summary.json.
Summary SHA256:151117fcd43177b8e393eeee6935222e54f01caecf8a17b4656149aec5058897.
Manifest SHA256:48b33a7ed29cf9ded858753d5f64210006f559ef428c167e912621a71896ae21.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False;
all_auxiliary_prefixes_matched=True;persisted reconstruction PASS.
Own48/focused4205 PASS;source580/protected1041;15 models and12000 updates.
Quad ce_only3/5,pair_always0/5,pair_early0/5.
Two/three full3/4/4;fitted TRAIN direct4/5/4;seen HOLDOUT direct3/4/4.
CE passes quad289003..289005;both auxiliary arms fail quad for every seed.
On289002 both auxiliary arms pass seen tasks but miss one quad HOLDOUT answer.
On289001 early withdrawal loses the trained-length TRAIN direct pass retained by always-on.
Equal full-gate counts do not imply identical individual outputs. No further loss/switch tuning
is registered. See acceptance for the proposed saved margin-versus-answer diagnostic.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoffs are preserved under docs/handoff-history/c280-pre-acceptance.md through
c289-pre-acceptance.md. The latest preserves Git blob c8aef6cc095ecfc40e096be53000add62c5c552d.
Only this Formal state is authoritative;historical ACTIVE instructions are not executable.
Accepted source/tests/preregistrations/logs and protected dispatchers remain unchanged.
