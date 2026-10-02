# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C296 ACCEPTED VALID NEGATIVE. C297 NOT REGISTERED.**
No ACTIVE experiment until the next authoring and committed-byte review are complete.
Scientific execution:3d52da4b565d05727b604560bbf60710dd9536e2.
Published log:16d3800de33edda84b88904b805029912de4ddc0.
Do not rerun C296 or change its fixed gates.

## Latest accepted evidence

Acceptance:docs/experiment-ledger-addendum-c296-c297.md.
Summary:runs/c296-v5b-render-batches-653d5ee53ab747f69da1611a8fc69630/summary.json.
Summary SHA256:d48c4c6725cecdf9e15034448186fe39b7e8b86b45f7a6418c839e2536f1093b.
Own40/focused4461 PASS;source622/protected1131;run_execution_valid=True.
Quad blocked2/5,balanced3/5;seen tasks4/4;TRAIN direct5/4;HOLDOUT direct4/4.
Two quad rescues and one regression;balanced worsens296005. No robust adoption claim.
Next proposed diagnostic separates fresh initialization and shuffle streams in a full3x3 grid,
with all cells retained and old full/masked gates measured descriptively. No automatic capability PASS.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

## Historical state

Full prior handoff:docs/handoff-history/c296-pre-acceptance.md.
Git blob5f738326b55e649d0d8014e12734fdb6a115dadf. Accepted sources/tests/logs remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
