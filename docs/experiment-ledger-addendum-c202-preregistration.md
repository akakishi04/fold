# C202 preregistration — three-channel acquisition dispatch

**C201 ACCEPTED PASS. C202 ACTIVE / NOT YET JUDGED. C203 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

With accepted C199 phase-0 learned fact targets, C200 structured-v2 channel metadata and the C201
selected-fact mapper held fixed, does the real structured acquisition lifecycle execute the
matching RETRIEVE / OBSERVE / ASK_USER endpoint, publish exactly the selected fact's registered
coherent-world value, leave all nonselected facts untouched and preserve the exact resource
contract?

This is a reference integration diagnostic. It adds no training and does not claim learned
channel preference.

## Fixed target source

Accepted C199:

- execution HEAD:
  `48100f36f4f1acdf44d5cb1d508b907e19724c10`
- summary SHA256:
  `0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9`

Use only arm0 ALLOWED, phase0 target predictions.

Required target artifact schema:

```text
target_predictions (2,9,9536,3)
world_codes        (9536,)
```

All phase0 targets must be indices0..3.
No target inference or relabeling occurs in C202.

## Parent C201

Accepted C201:

- execution HEAD:
  `1ce0334e0d5ee76c7e5fac40082c19bd43576415`
- summary SHA256:
  `c27ff79f20811ce373d175617b2a556c3c847d631f096fb401cb0251ad4fca4c`

C202 reuses the accepted exactly-one-channel mapper unchanged.

## Registered workload

For every accepted target, execute three independent variants:

```text
RETRIEVE
OBSERVE
ASK_USER
```

Total:

```text
9 blocks x 9536 targets x 3 channels = 257472 acquisitions
```

Expected provider calls per channel:

```text
RETRIEVE = 85824
OBSERVE  = 85824
ASK_USER = 85824
```

## Initial state

Each independent acquisition starts from a registered post-decision state:

```text
internal_remaining      12
acquisitions_remaining  4
available               [true,true,true]
permitted               [true,true,true]
last_outcome            NONE
internal_step           8
evidence_time           1
revision                1
all four facts          UNOBSERVED
```

The selected fact alone declares exactly one semantic channel in structured-v2 metadata.

## Provider fixture

C202 uses in-memory coherent C190 world documents.

The fixture removes filesystem latency but does not bypass the acquisition lifecycle.
The real `AcquisitionOwner.dispatch()` still validates:

- SourceBinding identity;
- request/delivery binding;
- source document hash and schema;
- selected fact/value consistency;
- observation publication;
- receipt creation.

Each world has three distinct provider instances, one per registered channel.
Only the provider matching the typed proposal may be called.

This fixture is not a real sensor, user conversation or network provider.

## Per-case contract

Required action result:

```text
PENDING / ACQUISITION_RESERVED
internal_charged       1
acquisition_reserved   1
```

Required dispatch result:

```text
PUBLISHED / OBSERVATION_ADMITTED
provider_calls         1
fact_publications      1
```

Required provider routing:
- matching channel provider call delta =1;
- both nonmatching channel provider call deltas =0.

Required publication:
- selected fact becomes OBSERVED;
- selected value equals the registered C190 coherent-world bit;
- selected fact receives exactly one reference identity;
- every nonselected fact stays UNOBSERVED with no value/reference;
- receipt count=1;
- receipt action equals the selected channel;
- receipt fact_id/value match the selected fact/world.

Required final resources:

```text
internal_remaining      9
acquisitions_remaining  3
available               [true,true,true]
permitted               [true,true,true]
last_outcome            NONE
internal_step           11
pending                 none
runtime terminal        none
```

## Fixed PASS gate

Across 27 block/channel records:

```text
cases/record             9536
provider_calls/record    9536
publications/record      9536
receipts/record          9536
failed/record            0
```

Global:

```text
dispatch_cases                 257472
block_records                  27
failures                       0
route_errors                   0
action_errors                  0
dispatch_errors                0
provider_channel_errors        0
receipt_errors                 0
selected_value_errors          0
nonselected_mutation_errors    0
resource_errors                0
provider_calls                 257472
publications                   257472
receipts                       257472

channel provider calls:
RETRIEVE                       85824
OBSERVE                        85824
ASK_USER                       85824
```

A valid completed miss is **ACCEPTED VALID NEGATIVE**.

Source/hash/schema/parent-artifact/import/regression/incomplete/protection failure is
**INVALID EXECUTION / RETRY SAME C202**.

No result may change this workload or gate under C202.

## Scope / non-claims

C202 registers:
- training0;
- fresh seeds0;
- learned forward calls0;
- network calls0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

PASS establishes only typed three-channel acquisition dispatch and publication on bounded fixture
providers.

PASS does not establish:
- learned preference among multiple channels;
- real sensor OBSERVE;
- real user interaction ASK_USER;
- mixed-family answer correctness;
- final Gate E completion.

## Authoring quality gate

C202 OWN:
- `fold_lm/v05_benchmarks/gate_e_c202_three_channel_acquisition_dispatch.py`
- `tests_lm/test_v05_c202_three_channel_acquisition_dispatch.py`
- `tools/run_c202.ps1`
- `tools/invoke_c202.ps1`
- this preregistration
- `docs/three-channel-acquisition-dispatch-v0.1.md`

Historical runtime/source pins additionally include:
- structured action runtime;
- structured acquisition lifecycle;
- C185 fact identities;
- C190 coherent-world source generator.

Expected:
- source pins25;
- protected inputs39;
- output artifacts5;
- new tests26;
- focused regression **1785 =1759+26**;
- regression modules **87**.

Scientific manifest SHA256:

`24bd6b04647342e8114a6e8245af046cfdae242a06d65c0a46286f577267406e`

## Post-authoring review requirement

Before any execution command is issued, committed remote bytes for benchmark/tests/runner/launcher/
preregistration/docs must be re-fetched and independently reviewed.

Review completed against committed remote bytes at:

`8879022df0aa6c904399fea21d7187614378d557`

Reviewed: benchmark, 26 new tests, runner, launcher, preregistration, dispatch-boundary docs,
accepted C201/C200/C199 identities, C199 prediction artifact schema/path, four historical runtime/
source pins, 25 source pins /39 protected inputs, manifest identity, 87-module/1785-test runner
contract, py_compile inputs, three launcher parent run paths, ExpectedHead/log publication wiring,
provider-channel isolation, selected/nonselected fact postconditions, resource postcondition, stale
C-number/HEAD/path residue and C203 non-registration.

`post_authoring_review = PASS`

## Execution / stop

Use the final reviewed registration HEAD as `ExpectedHead`.

Expected progress:
- C202 repository preflight
- C202 authoring syntax preflight
- source_and_artifact_precheck PASS
- focused regression1785/1785
- 27 block/channel progress lines
- RESULT
- POSTCHECK
- remote log publication

Judge C202 before any C203 registration.
