# V5-F memory operation contract v0.1

C213 begins V5-F after Gate E passed.

The changed variable is only the deterministic memory semantic bridge between relational memory
operations and the existing V5 EvidenceState provenance contract.

C213 does **not** introduce:

- learned Writer;
- learned Reader;
- Port Selector;
- Capsule Router;
- FOLD-R numeric response capsule;
- H1/H2 compiler;
- natural-language-to-operation parsing;
- model inference.

## Canonical operation vocabulary

```text
ASSERT(factor_id, scope, relation)
RETRACT(factor_id)
REPLACE(factor_id, new_relation)
ASSUME(scope_id, relation)
END_SCOPE(scope_id)
QUERY(read_request)
```

The implementation additionally carries exact expected memory revision and, for observed mutations,
source/evidence-time provenance.

## Two revision clocks

The bridge distinguishes:

```text
memory_revision
evidence_revision / evidence_time
```

Observed ASSERT/REPLACE/RETRACT advance both memory revision and evidence revision.

ASSUME/END_SCOPE advance memory revision only.

This prevents an internal hypothesis/scope operation from masquerading as new external evidence.

## Read states

C213 requires distinct statuses:

```text
SUPPORTED
MISSING
RETRACTED
OUT_OF_SCOPE
STALE_REVISION
```

These are not aliases.

In particular:

- a retracted factor is not ordinary MISSING;
- a query after END_SCOPE is OUT_OF_SCOPE;
- a query against an old memory revision is STALE_REVISION;
- a never-seen factor in a live scope is MISSING.

## Provenance boundary

Observed factors carry `ProvenanceKind.OBSERVED`.

ASSUME creates `ProvenanceKind.HYPOTHESIS`.

Hypotheses may be read inside a live assumption scope but `export_observed()` must never place them
inside authoritative `EvidenceState`.

The existing V5 EvidenceState invariant remains authoritative:

```text
hypothesis provenance cannot enter EvidenceState
```

## Factor identity and edit semantics

ASSERT requires a fresh `(scope_id, factor_id)`.

REPLACE requires a currently live observed factor and preserves its factor identity.

RETRACT removes the live record and leaves a tombstone so that a subsequent read is RETRACTED, not
MISSING.

A stale mutation is rejected before it can modify memory.

END_SCOPE cannot silently remove observed records. It is reserved here for scoped hypothesis state.

## Registered deterministic fixture

The C213 fixture executes six successful mutations:

1. ASSERT global alpha;
2. REPLACE global alpha;
3. ASSERT project beta;
4. RETRACT global alpha;
5. ASSUME sandbox temp;
6. END_SCOPE sandbox.

It executes eight reads with exact status totals:

```text
SUPPORTED       3
MISSING         2
RETRACTED       1
STALE_REVISION  1
OUT_OF_SCOPE    1
```

Final registered state:

```text
memory_revision   6
evidence_revision 4
evidence_time     3
live records      1
tombstones        1
ended scopes      1
exported observed 1
exported hypotheses 0
```

Additional required rejects:

- stale mutation rejected;
- END_SCOPE with observed record rejected;
- mutation into ended scope rejected.

## Interpretation boundary

PASS establishes only that the reference memory-operation/scope/revision/provenance semantics are
internally consistent and can export authoritative observations without hypothesis promotion.

PASS does not establish:

- FOLD-R numerical correction closure;
- H1/H2 memory compression;
- learned Writer/Reader accuracy;
- learned Port Selector coverage;
- natural-language memory extraction;
- Gate F.

The next V5-F experiment may bind this semantic layer to the existing FOLD-R numeric capsule only
after C213 is accepted.
