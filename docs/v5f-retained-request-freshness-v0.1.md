# V5-F retained request freshness v0.1

## One question

With the same C222 trajectory and frozen learned checkpoints, does a session-owned request lease
reject old requests after a state publication, before any model/provider call, while fresh requests
preserve the accepted answers and Coverage decisions?

C222 rebuilt requests from each current state. Its success did not establish reuse safety of the old
C221 QueryRequest closures, which retain their original state. C223 changes only this request
freshness boundary. It is not a new training, answer-cache or memory-cost experiment.

## New boundary

`fold_lm/v05/memory_request_lease.py` adds RequestSession / RequestLease / LeaseResult.
A session owns a state and a request factory. `bind(query)` builds the request from that session's
current state; callers do not attach an arbitrary old request to a fresh generation through this API.

A lease records session identity, monotonic publication generation and the original QueryRequest.
`publish(new_state)` advances generation on every publication, even a representation-only commit or
an identical-state publication. It is conservative: unrelated old requests also become stale.

```text
execute(lease):
    wrong session -> WRONG_SESSION, no downstream calls
    old generation -> STALE_REQUEST, no downstream calls
    current -> accepted C221 Coverage-first dispatcher
```

The session also checks after synchronous dispatch and withholds an answer if a callback published
another state during that call. This is not a claim of thread-safe linearizability.

There is no answer cache. No truth labels or expected answers enter RequestSession. The benchmark
scorer retains them separately and checks the returned result afterward.

## Held fixed

Use the exact C222 timeline function, accepted memory semantics, operation kinds and frozen
Writer/Coverage/Selector/Reader restoration helpers. No parent production source or test is edited.
The same anchor_only / beta_hot / beta_committed / beta_replaced / beta_retracted / shadow_assumed /
shadow_ended / project_ended sequence runs once per Writer and is evaluated across81 combinations.

Each current alpha/beta query is compared with the accepted C222 live-decisions artifact through a
schema/identity/semantic adapter. This map is scorer-only, not an input to session or dispatcher.

## Main and stale tests

Fresh:8 snapshots x2 queries x81 combinations =1296 decisions. Require1296 successes and exact
parent Coverage/answer/action/trace/bank-read parity.

At every publication, retain and attempt both requests from every earlier snapshot:
(0+1+2+3+4+5+6+7) x2 x81 =4536 old-request attempts. All must return STALE_REQUEST with no result,
trace exactly `freshness`, and zero Coverage/Selector/provider/bank/Reader calls.

The HOT -> COMMITTED transition is included: memory_revision is unchanged in the parent, but
storage_epoch changes. The new generation must invalidate that old HOT request without pretending
commit introduced semantic evidence.

Repeat a current beta_committed lease without publishing a new state:81 positive controls must still
answer correctly. This rules out rejecting all retained requests unconditionally.

## Explicit unguarded replay controls

Four controls per checkpoint combination intentionally bypass only the new lease check and execute
the old QueryRequest through the unchanged C221 dispatcher:

| Current stage | Old beta request | Expected obsolete behavior |
|---|---|---|
| beta_committed | beta_hot | HOT coverage instead of SUPPORTED, same answer |
| beta_replaced | beta_committed | old class2 answer instead of class0 |
| beta_retracted | beta_replaced | withdrawn class0 still returned |
| project_ended | beta_retracted | MISSING suppression instead of OUT_OF_SCOPE |

Require324/324 controls to reproduce the registered old response and differ from the current
response. These deliberate bypasses are diagnostic controls, not allowed use of the guarded API.
The matching guarded requests are rejected in the4536-attempt matrix.

## Fixed successful invocation counts

| Group | Coverage | Selector | Provider | Bank reads | Reader |
|---|---:|---:|---:|---:|---:|
| Fresh | 1296 | 891 | 891 | 891 | 891 |
| Stale guarded | 0 | 0 | 0 | 0 | 0 |
| Same-generation repeat | 81 | 81 | 81 | 81 | 81 |
| Unguarded replay controls | 324 | 243 | 243 | 243 | 243 |

Frozen Writer forwards3; total model forwards4134 at PASS. Training0; fingerprints unchanged.
Counts are invocation evidence, not a throughput comparison. Model-dependent count differences in
a complete run are scientific failures, not automatically invalid executions.

## Limits

State changes must use explicit session publication. The state object is trusted and treated as
immutable. In-place tensor mutation, skipped publications, maliciously forged/bypassed leases,
concurrent access, cross-process serialization, model-version changes and answer-cache invalidation
are not established. Session identity is an in-process correctness check, not a security sandbox.

These decisions are the same small synthetic trajectory crossed with checkpoint combinations, not
thousands of independent unseen tasks. Keeping old snapshots/requests for evaluation is not a
production storage-cost claim. Operation selection remains oracle; no new acquisition, indexing,
training or full-history cost comparison. Gate F remains NOT PASSED.
