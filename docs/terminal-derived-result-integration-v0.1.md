# Terminal derived-result integration v0.1

C206 connects the accepted mixed-channel terminal state to the existing production
`structured_derived_result.verify` contract.

## Boundary

The task conclusion is **derived**, not observed.

```text
accepted saved learned trace
-> real mixed-channel acquisition lifecycle
-> terminal SUFFICIENT TaskView
-> benchmark-only C171 proof fixture
-> production structured_derived_result.verify
-> VERIFIED_DERIVED
```

The C171 proof fixture is a reference candidate producer only. It is not production answer logic,
not learned reasoning, and not evidence acquisition.

## Terminal workload

Across9 accepted blocks:

```text
episodes              85824
decisions            214948
acquisitions         129124
terminal SUFFICIENT   85824
correct candidates     85824
opposite controls      85824
verifier calls        171648

RETRIEVE               88918
OBSERVE                 21252
ASK_USER                18954
channel switches         32564
```

## Correct candidate contract

At every terminal state:

1. C171 independent completion evaluator must return exactly one Boolean conclusion;
2. that conclusion must equal the actual coherent-world root value;
3. C171 benchmark proof fixture binds only actually OBSERVED fact references;
4. production verifier must return:
   - schema `fold-structured-derived-result-v1`;
   - status `VERIFIED_DERIVED`;
   - reason `VALID_LOCAL_PROOF`;
   - derivation kind `BOOLEAN_LOCAL_PROOF`;
   - exact candidate value/support/proof;
5. checked proof steps must be1..7;
6. the trusted TaskView must be byte-for-byte unchanged by verification.

## Negative control

Using the same proof/support with the opposite conclusion must return `REJECTED` with:
- no output value;
- no supporting references;
- no proof payload.

## Observation boundary

Verification must not:
- change any fact status/value/reference;
- replenish/debit resources;
- create an OBSERVED result;
- commit the logical conclusion into evidence.

The derived result is a separate output object bound to the current expression/evidence digests.

## Scope

C206 does not test learned proof generation or natural-language answer generation. It does not add a
new learned head, training data, external provider family, durable memory, or final Gate E
evaluation.

It establishes only whether the accepted terminal acquisition trajectory can be consumed by the
already-existing bounded production derived-result verifier without crossing the observation /
derivation boundary.
