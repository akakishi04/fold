# V5-F memory capsule closure v0.1

C214 connects the accepted C213 memory-operation semantics to the existing fixed-port FOLD-R
response capsule.

## Scientific question

For supported observed edit sequences, does the capsule readout equal an independent full-memory
solve within registered float64 tolerance?

## Changed variable

Only the semantic-to-numeric bridge is added:

```text
C213 MemoryState
  -> observed live records only
  -> registered relation-to-port updates
  -> existing ResponseCapsule
  -> readout
```

The reference comparator is:

```text
same live observed records
  -> reconstruct J + U W U^T and eta + U b
  -> full torch.linalg.solve
  -> Q readout
```

## Held constant / absent

No learned Writer, learned Reader, Port Selector, H1/H2 compiler, language parser, model forward,
training or new capsule algebra is introduced.

The existing capsule implementation is pinned by source identity.

## Registered numeric fixture

Base dimensions:

```text
variables 4
update rank 2
readout dim 2
float64
```

Safe relation registry:

```text
rel-alpha-v1
rel-alpha-v2
rel-beta-v1
```

A fourth registered relation `rel-unsafe` is used only for the numeric-safety control.

The main C213-compatible state sequence has seven read snapshots:

1. initial;
2. after ASSERT alpha/v1;
3. after REPLACE alpha/v2;
4. after ASSERT beta;
5. after RETRACT alpha;
6. after ASSUME temp;
7. after END_SCOPE sandbox.

Expected observed-factor counts:

```text
[0,1,1,2,1,1,1]
```

All seven must be SUPPORTED by both capsule and full reference.

Maximum capsule-vs-full absolute error:

```text
<= 1e-10
```

ASSUME and END_SCOPE are hypothesis/scope-only operations, so their capsule readout must be
bit-identical to the preceding observed-only beta state.

## Capability controls

Unknown observed relation:

```text
OUT_OF_SCOPE
```

Registered update that destroys positive definiteness:

```text
NUMERIC_UNSAFE
```

Neither control may expose a numeric value.

These states must remain distinct.

## Semantic preservation

The final main sequence must still have:

```text
memory revision   6
evidence revision 4
evidence time     3
exported observed factor beta only
```

Hypothesis records are ignored by the authoritative numeric capsule bridge.

## Interpretation boundary

PASS supports only the deterministic semantic-to-fixed-port numeric closure:
- C213 edit semantics remain intact;
- supported capsule reads match full solves;
- unsupported capability and unsafe numerics remain explicit.

PASS does not establish:
- learned Port Selector;
- H1/H2 chunk commit;
- compression advantage;
- natural-language memory writing;
- learned Writer/Reader;
- Gate F.

A later C may introduce one of those components only after C214 is accepted.
