# C235 acceptance and C236 minimal-binding boundary

## Formal verdict

**C235 ACCEPTED PASS — diagnostic integrity only.**
C234 remains ACCEPTED VALID NEGATIVE. Gate E PASSED; Gate F NOT PASSED.
No binding capability, general-language quality or core superiority is accepted by C235.

Scientific execution HEAD: `fc3311955c3dcda87b67c2ee8dd58a59fb256d6f`.
Published log commit: `71dd1bb48978a1bd0a6b71448f1ceb29011696c4`.
Log SHA256: `fb2811d896606c07bd3d6cbd28a036d30f905dfce0295ade1fde582cde14b40a`.
Log bytes: 521326.
Summary SHA256: `a9d6daa76bab38488ec3634d186ba81a2d61ae878df80202f3084057e917b1b5`.
Local summary: `runs/c235-v5b-frozen-binding-diagnostic-17d75b38b35249a297bde78cee0f1d43/summary.json`.

Evidence: `docs/experiment-run-logs/c235/latest.json` and `latest.log` at the published log commit.
The log commit is exactly one commit after the execution HEAD and changes only these two files.
Acceptance relies on published execution evidence and its local-artifact postcheck, not a reviewer
rerun of the six user-local checkpoints. The metadata SHA is the publisher's recorded digest.

## Execution validity

The repaired own suite passed all24 tests in0.334s. Focused regression passed2809 tests in65.332s.
Source/artifact precheck:256 source pins /370 protected inputs.
All six accepted C234 step400 models were evaluated on complete TRAIN384 and EVAL192 under three
views:36 model forwards /10368 row presentations /zero new training steps.
All parent EVAL predictions and metrics replayed. All model fingerprints remained unchanged.
All12 diagnostic cells were present. Protected inputs, clean tracked tree and execution HEAD were
preserved; `run_execution_valid = True`. `diagnostic_status = PASS` and
`capability_pass_claim = False`.

The initial invalid attempt remains recorded at log commit
`1615b5ce54afed8bde44ac9d326cace6c6e674d0` and in
`docs/experiment-ledger-addendum-c235-execution-recovery.md`.
It was an authoring-test false positive, not a scientific negative. The successful retry does not
erase that failed attempt or retrospectively label its execution valid.

## Deciding measurements

Every seed/family/language cell is `TRAIN_ACCURACY_BELOW_90` (12/12).
Each language has192 TRAIN rows. Exact correct counts below are recovered from the logged
six-decimal rates and the fixed integer denominator; the rounding interval identifies one count.

| Seed | Full EN TRAIN | Full JA TRAIN | GRU-only EN TRAIN | GRU-only JA TRAIN |
|---:|---:|---:|---:|---:|
|234001|102/192|95/192|96/192|96/192|
|234002|97/192|96/192|95/192|101/192|
|234003|96/192|100/192|99/192|92/192|

Overall TRAIN accuracy ranges from47.9167% to53.125%, far below the inherited90% reference.
Supplied-value selection on TRAIN is100% in all12 cells: each answer is one of the two values
present in the prompt. Yet changing the queried object leaves the answer unchanged in78.125% to
94.7917% of TRAIN query pairs. TRAIN both-correct query pairs range from2/96 to12/96.

EVAL reproduces C234: Full19/96 to25/96 correct; GRU-only30/96 to39/96 correct.
EVAL query-pair both-correct is0/48 throughout except Full seed234001 JA at2/48.

## Scientific interpretation and non-claims

The registered recipe failed already on its training binding set; failure is not confined to
held-out value-pair contexts. The output behavior is consistent with selecting a supplied value
without reliably binding it to the queried object. This is a behavioral description, not proof of
a particular internal algorithm, ignored-query mechanism or causal fault in a named module.

A low final sampled TRAIN-batch NLL in C234 was not proof of learning the TRAIN task. C235 now
measures that missing quantity. It does not isolate architecture, optimizer, dataset breadth,
training budget or representation as the cause. It is not a significance test or a full/GRU ranking.
C233/C234 verdicts remain unchanged; useful general-language/reasoning is not demonstrated.

## Accepted artifact identities

- diagnostic-plan.json: `2e8bb701b3a6d512479c7118ac0973784617e1243639ef00c3903caed1a0f6c3` (1732 bytes)
- diagnostics.json: `a93f73fb6cb17d9a3a8067f8a4d522cafe68acad56d02200ce95de521f5a989c` (16249 bytes)
- model-fingerprints.json: `28c26fa0d6ecf84db469b6ee3a945bd956489802cd4795d39b3a28c15fd7d71c` (1112 bytes)
- predictions.json: `10f477d42f1b53a250c34e77616a81f17f3e92e008f9ae1619fe572a055c44d3` (32072 bytes)
- validation-summary.json: `30ac8dcbe92b826e9d2f69384204ade6e6fb9fb6e07b660713325c9640385023` (261 bytes)

## Next question — minimal binding learnability

Before enlarging the model or extending training, ask whether the unchanged model/training recipe
can fit one balanced minimal binding set: two objects, two distinct values, both assignments,
both fact orders, both queried objects and both languages (16 existing C234 TRAIN rows).

This changes training-cohort breadth only relative to C234. Initialize fresh models using the same
predeclared seeds; retain architectures, answer-only objective, unconstrained256-byte output,
optimizer, batch size and400-step budget. This is a separate minimal TRAIN-fit probe, not a rerun
or rescue of C234, and no held-out-generalization claim follows from fitting16 seen rows.
More exposure per unique row and smaller vocabulary are consequences of this single cohort
restriction; they are not separately identified causal variables.

This acceptance document does not register C236. See the separate preregistration and current
handoff for activation/readiness. Do not run a new experiment until post-authoring review passes.
