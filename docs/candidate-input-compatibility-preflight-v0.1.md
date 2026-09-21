# Candidate input compatibility preflight v0.1

C208 tests whether the current frozen C181/C188 inference interface can consume the frozen C207
development packets **as-is**.

No model forward, adapter, candidate score or baseline score is produced.

## Frozen input

Parent C207 visible artifact:

```text
SHA256 c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543
episodes 144
families 9
```

Only `development-visible.json` is loaded. The scorer artifact is not loaded.

## Current candidate contracts

### Necessity representation

The accepted frozen necessity path uses C178 `prepare_pair`, whose validator requires:

- canonical CPU int32 [N,72];
- exactly7 nodes;
- exactly4 facts;
- four FACT leaves;
- one connected read-once tree;
- canonical visible fact/runtime fields.

C178 accepts registered structured-v1 fact statuses generally as long as non-OBSERVED facts carry no
payload.

### Target representation

The frozen C188 target selector additionally requires:

- exactly4 active fact slots;
- fact status only UNOBSERVED or OBSERVED;
- presence bit exactly equivalent to OBSERVED;
- four FACT leaves mapped one-to-one to fact IDs1..4.

The selector therefore does not natively accept STALE/CONFLICT rows.

## Diagnostic

For every frozen C207 visible case C208 records:

- header 7-node/4-fact compatibility;
- active fact-slot count;
- active FACT-leaf count;
- target-status compatibility;
- actual C178 validator result/rejection;
- actual C188 missing-mask + leaf-position validator result/rejection;
- combined as-is compatibility.

Expected validator rejection is scientific evidence, not execution invalidity.

## Verdict

C208 scientific PASS requires all144 frozen development rows to be accepted as-is by both current
candidate input contracts.

A complete valid FAIL is retained as **ACCEPTED VALID NEGATIVE** and establishes the exact
representation surface that must be addressed before baseline-development measurement.

Execution validity requires only complete classification of all144 rows with no unexpected harness
error, no model forward, no adapter and no scorer use.
