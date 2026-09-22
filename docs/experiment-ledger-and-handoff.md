# FOLD Experiment Ledger and Handoff

> Authoritative current state. Follow `AGENTS.md` and
> `docs/experiment-conversation-handoff-protocol.md` (Current response format v2).

Repository: `akakishi04/fold`  
Branch: `feat/sft-target-loss`  
Local repository: `M:\asobiba\fold`  
Authoritative runtime: Python 3.13.15 / PyTorch 2.10.0+cu130 / NumPy 2.3.5.

## Formal state

Gate A/B PASSED; Gate C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C220 ACCEPTED PASS. C221 NOT REGISTERED.**

No C experiment is ACTIVE while C221 is being authored.

## Accepted C220

Experiment: `C220-v5f-frozen-learned-stack-integration`  
Stage: `V5-F-FROZEN-LEARNED-STACK-INTEGRATION`.

Scientific execution HEAD: `6bc455fa377ec9d3c70d6d1f0922c00680fd5a04`  
Published log commit: `e194716393249373a7d1f6ab552860e851ea84d0`  
Log SHA256: `dd9e8753ac48b74e369c2c87efdb0987da81c1b9379bab674af86252c8b7eed2`  
Summary SHA256: `45821b372bf0108e667274e2facd73b1f0a84f515a7d036e73874d9238fff5f7`.

Accepted local summary:
`runs/c220-v5f-frozen-learned-stack-5bc9d133c96348de81a24d19b3ef6f93/summary.json`.

Execution validity: 2335/2335 regression OK; prechecks/postchecks PASS;
protected inputs preserved; tracked tree clean; `run_execution_valid = True`.

Deciding results: 81 checkpoint combinations, 648 decision rows (486 readable /162 non-readable),
integration/expected-coverage/readable-answer/non-readable-suppression accuracy1.0;
MISSING/OOS confusions0, placement mismatches0, operation failures0, training0.
All four checkpoint-family roundtrips passed. Total model forwards42.

Complete verdict, identities, artifact hashes and interpretation:
`docs/experiment-ledger-addendum-c220-c221.md`.

### Interpretation boundary

C220 passed its registered **offline composition** check. These are eight synthetic episode shapes
crossed with81 checkpoint combinations, not648 independent unseen tasks.

The executed source precomputes readable Reader outputs and combines them with Coverage in the
scorer. It does not yet prove that learned Coverage controls actual downstream calls.
C221 must test this causal dispatch boundary before adding task breadth.

No learned operation-kind selection, natural-language inputs, acquisition integration,
RETRACT/ASSUME integration, memory-cost superiority or Gate F completion is established.

## Accepted V5-F chain

| Experiment | Accepted measured scope |
|---|---|
| C213 | Deterministic MemoryOp / factor / scope / revision / provenance contract |
| C214 | Fixed-port numeric response agrees with full solve on registered edits |
| C215 | H1/H2 representation-only commit, post-commit REPLACE/RETRACT reference |
| C216 | Isolated three-value Reader with oracle port selection |
| C217 | Two-port Selector with frozen C216 Readers |
| C218 | Structured factor+relation Writer with oracle ASSERT/REPLACE kind |
| C219 | Four-class structured Coverage pilot, numeric safety excluded |
| C220 | Frozen four-component offline composition |

The frozen learned components exist and passed these narrow pilots. They are not general
natural-language memory components and have not demonstrated large-scale memory-cost advantages.

## Gate E checkpoint

C212 is ACCEPTED PASS / GATE_E_PASSED.
Scientific HEAD: `4d1436c1ba12721b1c802fb5d76e359b3a62841f`.
Summary SHA256: `3685c37dd6e2c7fea92723548446b86f4ee8d068f7dd00afe3e2337f8bca8bce`.
Independent144-episode holdout /432 policy-episode evaluations; candidate128 correct,
noninferiority to FIXED_ACQUISITION and registered superiority to INTERNAL_ONLY passed.
Full decisive log: `docs/experiment-run-logs/c212/latest.log`.

## Historical evidence and maintenance

Earlier detailed handoff is recoverable at
`e194716393249373a7d1f6ab552860e851ea84d0:docs/experiment-ledger-and-handoff.md`.
This compact handoff does not replace any historical preregistration or accepted source pin.

Keep all current accepted source/protection dependencies unchanged. In particular,
`tools/run_c167.ps1` is historical regression-construction infrastructure and must not be deleted.
Its exact blob is `7c5d6e9838d4ce7bd2bfec0e43458eb749fd1789`.

Policies: `tools/README-experiment-harness.md`, `docs/experiment-run-logs/README.md`.
No cleanup, source moves, history rewrite, CI addition or Actions-storage work is authorized by the
next experiment. Actions storage is being handled separately by the user.

## Next boundary

C221 proposed question: can Coverage-first live dispatch preserve the same frozen-stack decisions
while actually preventing downstream calls on suppression, with no expected labels supplied to the
dispatcher? Include separate causal intervention controls and call traces.

Hold checkpoints, episode shapes, operation-kind oracle and Gate F interpretation fixed.
Do not add retraining, new semantic tasks, RETRACT/ASSUME, acquisition or cost optimization here.

## Stop condition

C220 is closed as ACCEPTED PASS.
C221 remains NOT REGISTERED until its authoring and post-authoring review are complete.
Gate F remains NOT PASSED.
