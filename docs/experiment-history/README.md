# FOLD experiment history — thematic index

Report cut: 2026-09-20 JST  
Scientific branch snapshot: `feat/sft-target-loss@5a2605a9bac234a605b9f35394520fff2175db82`

## Current authoritative state at this cut

- Gate A/B: PASSED
- Gate C/D: PASSED in measured scope
- Gate E: **NOT PASSED**
- C195: **ACCEPTED PASS**
- C196: **ACTIVE / NOT YET JUDGED**
- C197: NOT REGISTERED

This directory summarizes completed experiments **by scientific subject**, not merely by C-number.
It is intended to preserve the reasoning history before old experiment scripts are archived or
removed from the working tree.

The experiment ledger, preregistrations, accepted summaries, protected artifacts and historical
Git commits remain authoritative for exact reproduction.

## Reports

1. [Shared-Basis and adaptive routing — C78-C96](01-shared-basis-and-adaptive-routing-c78-c96.md)
2. [Information sufficiency, authority and recovery — C97-C132](02-information-sufficiency-authority-recovery-c97-c132.md)
3. [Retrieval, ranking and composition — C133-C151](03-retrieval-ranking-composition-c133-c151.md)
4. [Evidence lifecycle and live terminal path — C152-C167](04-evidence-lifecycle-live-terminal-c152-c167.md)
5. [Structured interface and runtime contracts — C168-C173](05-structured-interface-contracts-c168-c173.md)
6. [Learned necessity and semantic representation — C174-C184](06-learned-necessity-semantics-c174-c184.md)
7. [Learned acquisition and generic loop — C185-C195](07-learned-acquisition-loop-c185-c195.md)
8. [Execution-invalid / harness recovery history](08-execution-invalid-recovery-history.md)

## Reading rule

A PASS means the preregistered question passed **within its registered scope**.
A VALID NEGATIVE means the experiment executed correctly and the registered hypothesis/gate failed.
An INVALID EXECUTION is not scientific evidence.

## Cleanup rule

Do not delete an old file merely because its C-number is old. Before cleanup classify it as:

- **active dependency** — imported, replayed, hashed or regression-loaded by current experiments;
- **historical reproduction only** — not needed by the current head but needed to rerun an old experiment;
- **archive candidate** — useful only as historical implementation after its result is summarized and Git history preserves it;
- **safe working-tree deletion candidate** — no current dependency, no protected identity requirement, and replacement/summary is established.

C196 is active at this report cut, so cleanup must not move the scientific branch HEAD or invalidate
its source/protected-file union.
