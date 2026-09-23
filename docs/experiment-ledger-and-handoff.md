# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C240 ACCEPTED PASS (diagnostic integrity only). C241 NOT REGISTERED. C242 NOT REGISTERED.**
No active experiment during acceptance-to-registration transition.
C239 remains ACCEPTED VALID NEGATIVE; C238 remains minimal seen-TRAIN fitting PASS.

## Latest accepted evidence — C240

Scientific execution HEAD:7bf66561cfb151a6ba2562791a1645b760ad6f1f.
Published log commit:24141d62cdb58be0d11ae3b57e35b5f0593c7e50.
Log SHA256:48066d34eee74c201dae7660fd32dd8b04bebedefd73547e745cfa51f8b24315.
Summary SHA256:3551a5da3346381fdeb81b80a7cd297822ee51f64e80f9d966158ecf4c36b8b0.
Local summary:runs/c240-v5b-saved-position-audit-4b604be67f5b47f0b18cabdb2513d12d/summary.json.

24 own tests PASS in0.104s;2929 focused tests PASS in112.356s.
286 source pins/430 protected inputs. Zero new training/model forwards/checkpoint loads/writes.
288 saved predictions,96 normal rows,576 rule comparisons,48 order pairs,24 diagnostic cells.
All discrete C239 metric replay and persisted audit recomputation PASS.
Protected inputs/tracked tree/execution HEAD preserved;run_execution_valid=True.
diagnostic_status=PASS;capability_pass_claim=False;causal_claim=False;nll_recomputed=False.

TRAIN normal rows:48/48 correct and48/48 query_fixed_position matches.
HOLDOUT normal rows:4/48 correct,44/48 other_entity,44/48 query_fixed_position,0 outside-supplied.
Matched order pairs:4/48 same answer,4/48 both correct,44/48 both query_fixed_position.
This is strong behavioral consistency with the preregistered positional shortcut,not proof of
an internal algorithm or unique cause. TRAIN entity=fixed-position and HOLDOUT fixed-position=
other entity in this binary fixture, so the identifiability limitation is explicit.

Acceptance/artifacts:docs/experiment-ledger-addendum-c240-c241.md.
Acceptance record commit:dc75a8defc0d21d70d1c7ec06914914468e0bd77.
No C239 verdict reversal,answer correction,NLL reconstruction,core ranking or Gate F promotion.

## Preserved earlier evidence

C239:all12 TRAIN cells pass but all12 reversed-order HOLDOUT cells miss;valid negative.
C238:all12 seen-TRAIN cells pass after complete-cohort sampling.
C237:diagnostic PASS with numerical sensitivity without correct answer switching.
C236:valid negative under random replacement sampling.
C235 diagnostic PASS;C234/C233 valid negatives;C232 bounded template-byte learning only.

## Next boundary

Prepare C241 as a fresh assignment holdout with both positions represented in TRAIN:
TRAIN uses value assignment[0,1] across both orders,queries and languages;HOLDOUT uses swapped
assignment[1,0] across both orders,queries and languages. Exact prompts/IDs are disjoint.
This breaks C239's query-to-fixed-position shortcut inside TRAIN. A fixed entity-value lookup can
still fit TRAIN but must fail HOLDOUT, so a HOLDOUT pass would rule out both simple behaviors on
this bounded fixture without proving a unique internal mechanism.

Keep fresh initial states,models,optimizer,batch32,400 steps and complete-cohort8x4 policy.
Use exact accuracy,query-pair and order-pair both-correct scores,plus evidence/query mask drops.
Do not invent fact-swap pairs inside assignment-fixed splits. HOLDOUT first reaches evaluation
after the training endpoint. Separate preregistration and remote-readback review are required.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve accepted sources/tests/logs and
tools/run_c167.ps1. No cleanup/history rewrite,paid API,external corpus,larger model or production
runtime change. Judge each active C before its successor.
