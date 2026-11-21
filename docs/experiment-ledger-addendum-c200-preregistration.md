# C200 preregistration — acquisition-channel input contract v2

**C199 ACCEPTED PASS. C200 ACTIVE / NOT YET JUDGED. C201 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can an opt-in structured task input v2 expose the missing **fact-specific acquisition-channel
eligibility** required by Gate E while preserving the entire canonical v1 policy packet exactly
and without leaking hidden values, answer labels, necessity labels, evaluator dependencies or
runtime authority?

This is an input-contract diagnostic only. It does not train or evaluate a learned tool selector.

## Changed interface

v1 remains unchanged.

C200 adds an opt-in v2 packet:

```text
features[0:72]  = exact canonical structured-task-input-v1 packet
features[72:84] = 4 fact slots x 3 visible eligibility bits

per fact:
[ RETRIEVE, OBSERVE, ASK_USER ]
```

Unused fact-slot tail padding must be zero.

A channel bit means only that the channel is **semantically applicable to that fact**.
It does not grant permission, assert provider availability, consume budget, authorize an action
or imply acquisition success.

The existing v1 resource masks remain the separate runtime availability/permission layer.

## Parent identity

Accepted C199:

- scientific execution HEAD:
  `48100f36f4f1acdf44d5cb1d508b907e19724c10`
- summary:
  `runs/c199-v5e-attempt-limit-886ac50bbbe046ebba61316e6bf97268/summary.json`
- summary SHA256:
  `0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9`

C200 additionally pins the canonical v1 source blob at the accepted C199 execution identity and
requires the current v1 blob to be byte-identical. Historical C170-C199 behavior is not modified.

## Fixed diagnostic groups

### 1. Channel-mask roundtrip

**32 cases**:

```text
4 fact slots x all 8 three-bit channel masks
```

Every case must:
- round-trip exactly through v2 encode/decode;
- retain the exact v1 72-feature prefix;
- retain the exact v1 binding object.

### 2. Runtime authority cross

**448 cases**:

```text
7 nonempty semantic channel masks
x 8 runtime availability masks
x 8 runtime permission masks
```

For every case:
- declared channel eligibility remains unchanged by authority masks;
- policy-visible usable channels equal the explicit intersection of
  semantic eligibility × availability × permission;
- the canonical v1 prefix remains exact.

This is feature inspection only. Runtime execution remains authoritative.

### 3. Hidden-completion pairs

**12 paired visible cases**:

```text
3 one-hot channels
x AND/OR
x observed A bit 0/1
```

For each pair, hidden B=0 and B=1 may produce different evaluator conclusions, but the
policy packet must remain identical because B is still unobserved.

Required:
- 12 packet-equality checks;
- 6 answer-changing hidden-completion pairs;
- no hidden value carried in the packet.

These evaluator outputs are diagnostic metadata only and never become model input.

### 4. Malformed / noncanonical inputs

**18 cases** must all be rejected, including:
- wrong schema;
- short/long feature arrays;
- non-Boolean channel integers;
- bool masquerading as integer channel feature;
- negative/out-of-range values;
- nonzero unused channel padding;
- mutable feature/binding shapes;
- v1 prefix corruption;
- hidden payload disguised in the v1 fact region;
- invalid channel tuple/count/type.

## Fixed gate

C200 PASS requires all of the following:

```text
mask_roundtrips            = 32
runtime_cross              = 448
hidden_pairs               = 12
malformed_cases            = 18

roundtrip_failures         = 0
runtime_cross_failures     = 0
hidden_packet_mismatches   = 0
hidden_answer_diff_pairs   = 6
malformed_rejected         = 18

v1_feature_width           = 72
v2_feature_width           = 84
v1_prefix_preserved        = true
channel_classes            = 8
```

A valid complete miss is **ACCEPTED VALID NEGATIVE**.

Source/hash/schema/manifest/import/regression/incomplete/protection failures are
**INVALID EXECUTION / RETRY SAME C200**.

No result may change these counts or the gate under C200.

## Scope / non-claims

C200 includes:
- zero training steps;
- zero fresh seeds;
- zero learned forward calls;
- zero provider/tool/network calls;
- zero evidence writes;
- no production runtime change.

A PASS means only that the missing visible acquisition-channel input boundary exists as a
strict, lossless, backward-preserving contract.

A PASS does **not** establish:
- learned selection among RETRIEVE / OBSERVE / ASK_USER;
- correct tool execution;
- Gate E nine-family quality;
- final Gate E completion;
- language or answer/proof generation.

## Authoring quality gate

C200 source files:
- `fold_lm/v05/structured_task_input_v2.py`
- `fold_lm/v05_benchmarks/gate_e_c200_acquisition_channel_input.py`
- `tests_lm/test_v05_c200_acquisition_channel_input.py`
- `tools/run_c200.ps1`
- `tools/invoke_c200.ps1`
- this preregistration
- `docs/structured-task-interface-v0.2.md`

Pinned source/protected counts:
- source pins: **8**
- protected inputs: **9**
- output artifacts: **5**

Regression:
- expected modules: **85**
- expected focused tests: **1731 = 1701 + 30**

The runner performs Python `py_compile` before source/artifact precheck, then the complete
1731-test focused regression before the diagnostic.

Scientific manifest SHA256:

`af65cbab8b4e9d594fc4ffad5709acee07a5c85bc91a9148771c1dfe64de13bb`

## Execution / stop

Use the final registration HEAD as `ExpectedHead`.

Expected progress:
- C200 repository preflight
- C200 authoring syntax preflight
- source_and_artifact_precheck PASS
- focused regression 1731/1731
- C200 diagnostic collection
- RESULT
- POSTCHECK
- remote log publication

Judge C200 before any C201 registration.
