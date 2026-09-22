# V5-F withdrawal and hypothesis lifecycle v0.1

## One scientific question

Can the frozen C221 live memory stack stop publishing a committed observation after its withdrawal,
including while a same-named hypothesis exists in a different scope, without losing unrelated
observed information?

C222 changes only the evaluation lifecycle. It adds no production module, no model update and no
training. Accepted memory semantics, Coverage-first dispatcher, provider preconditions, Reader,
Selector, Writer and Coverage checkpoints remain unchanged. Operation kinds remain oracle.

## Continuing trajectory

Create one bank per frozen Writer checkpoint and update the returned immutable state successively.
Do not reconstruct a new initial bank for every stage. At every snapshot query both alpha and beta;
alpha is the unrelated observed anchor with semantic class1 (value0).

| Snapshot | Change | Expected project/beta Coverage | Beta answer class | memory/evidence/time/epoch |
|---|---|---|---:|---|
| anchor_only | Learned ASSERT alpha class1; commit | MISSING | none | 1/1/1/1 |
| beta_hot | Learned ASSERT beta class2 | HOT_REQUIRED | 2 | 2/2/2/1 |
| beta_committed | Commit beta | SUPPORTED | 2 | 2/2/2/2 |
| beta_replaced | Learned factor+relation REPLACE beta class0 | SUPPORTED | 0 | 3/3/3/2 |
| beta_retracted | Oracle RETRACT project/beta | MISSING | none | 4/4/4/2 |
| shadow_assumed | ASSUME sandbox/beta with beta-class-2 | MISSING | none | 5/4/4/2 |
| shadow_ended | END_SCOPE sandbox | MISSING | none | 6/4/4/2 |
| project_ended | END_SCOPE project | OUT_OF_SCOPE | none | 7/4/4/2 |

The hypothesis deliberately carries the old pre-replacement beta semantic value and the same factor
name, but a different scope. It must not re-establish the withdrawn project observation. ASSUME
construction is oracle; this is not learned hypothetical writing or hypothetical question answering.

Alpha must remain SUPPORTED with answer class1 at all eight snapshots. This prevents an apparently
safe but useless implementation from passing merely by suppressing all answers or clearing memory.

## Symbolic provenance and numerical-state diagnostics

Diagnostics run outside the learned query path and are recorded separately. They must show:

- project/beta is RETRACTED after withdrawal, while its scope remains live;
- no relation/provenance is exposed by that tombstone read;
- sandbox/beta is readable as HYPOTHESIS only while its scope is live;
- sandbox/beta is OUT_OF_SCOPE after END_SCOPE;
- authoritative evidence export contains only current observed factors;
- after withdrawal, export retains global/alpha and never promotes sandbox/beta;
- ASSUME/END_SCOPE do not advance evidence revision/time;
- H2 W/b remain identical across the withdrawn, hypothesis-live, hypothesis-ended and project-ended
  snapshots.

Coverage MISSING here means no current authoritative support for the target. It does not assert
that the fact never existed. The richer MemoryRead RETRACTED status is retained and checked; it is
not silently replaced by MISSING in the memory-operation API.

## Fresh live requests, not retained closures

For each query, call the accepted C221 request builder with the current snapshot, then invoke the
accepted dispatcher. No teacher answer, expected Coverage or precomputed Reader output is supplied
to the dispatcher. The scorer checks those only after the call.

The benchmark retains snapshot references for reproducible evaluation of checkpoint combinations.
This is measurement storage, not a claim about production memory consumption. It does not replay
raw history to construct each snapshot.

Each query request is newly constructed. C222 does not exercise reuse of an old QueryRequest closure,
a session cache, stale answer-cache invalidation or arbitrary query revisions. Do not interpret PASS
as proof of those untested mechanisms.

## Forced-allow controls

At beta_retracted and shadow_assumed, override only the Coverage proposal to SUPPORTED, while still
calling and recording the original frozen Coverage prediction. The accepted provider must detect
that project/beta lacks an observed record and return BLOCKED_MISSING.

Required trace: coverage, selector, provider. No numeric bank read, Reader call or answer.
This distinguishes deterministic safety from the neural classifier's normal suppression behavior.

## Fixed matrix and counts

Three checkpoints each for Writer/Coverage/Selector/Reader give81 combinations. Each uses eight
snapshots and two queries, yielding1296 main decisions. These are not1296 independent unseen tasks.
There are648 alpha anchor decisions,243 readable beta decisions and405 suppressed beta decisions.

Main successful calls: Coverage1296, Selector891, provider891, bank reads891, Reader891.
Controls: 2 per combination =162; Coverage162, Selector162, provider162, bank reads0, Reader0.
Frozen Writer targets are batched exactly as in C220/C221:3 model forwards.
Total successful model forwards:3405. New training steps0.

## PASS and interpretation

Require1296/1296 main decisions,162/162 controls,648/648 alpha anchor answers,405/405 correct beta
suppressions, zero beta answers after RETRACT, zero downstream calls on normal suppression, three
passing symbolic/export/numerical-state trajectory audits and unchanged checkpoint fingerprints.
Model-dependent call totals are scored, not demanded as preconditions for serializing a complete
negative result.

A completed classification/answer/audit/call-pattern mismatch is FAIL. Source/artifact/schema errors
or an operation exception preventing a complete trajectory are INVALID; preserve the log and do
not move to the next C. No threshold relaxation after a run.

PASS supports this narrow continuing-state withdrawal/hypothesis-isolation trajectory only.
Gate F remains NOT PASSED: broader lifecycle cases, arbitrary old-request/cache freshness,
acquisition/clarification and total memory-cost comparison remain unestablished.
