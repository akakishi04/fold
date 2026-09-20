# Three-channel acquisition dispatch v0.1

This document fixes the C202 reference integration boundary from a selected fact and exactly-one
semantic channel through the existing structured acquisition lifecycle.

## Input state

C202 begins after an already-accepted learned fact target has been selected. The trusted
RuntimeState uses:

```text
internal_remaining      12
acquisitions_remaining  4
available               RETRIEVE/OBSERVE/ASK_USER = true
permitted               RETRIEVE/OBSERVE/ASK_USER = true
last_outcome            NONE
internal_step           8
evidence_time/revision  1/1
```

The structured-v2 view declares exactly one semantic channel on the selected fact.

## Dispatch path

```text
selected fact_index
-> structured_action_channel.propose_selected()
-> structured_action_runtime.step()
-> ACQUISITION_RESERVED
-> AcquisitionOwner.dispatch()
-> matching channel Endpoint
-> bounded source/delivery validation
-> OBSERVATION_ADMITTED
```

All three endpoint names are registered simultaneously. Only the channel named by the typed
proposal may receive the request.

## Fixture boundary

C202 uses in-memory coherent C190 world documents. This removes filesystem latency from the
comparison, but it does not bypass lifecycle validation. The acquisition owner still validates:

- SourceBinding identity;
- request/delivery binding;
- source document hash/schema;
- fact/value consistency;
- observation publication;
- receipt creation.

The fixture is not a real sensor, user conversation or external network service.

## Expected postcondition

After one admitted acquisition:

```text
internal_remaining      9
acquisitions_remaining  3
last_outcome            NONE
internal_step           11
pending                 none
runtime terminal         none
selected fact           OBSERVED at coherent-world value
nonselected facts       unchanged UNOBSERVED
receipt count           1
```

## Scope

This boundary establishes typed three-channel dispatch and publication only. It does not establish
learned preference among channels, real OBSERVE sensing, real ASK_USER transport, answer quality,
or final Gate E completion.
