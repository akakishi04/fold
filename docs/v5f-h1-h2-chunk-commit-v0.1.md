# V5-F H1/H2 chunk commit v0.1

C215 introduces only the deterministic H1 hot-memory / H2 capsule-bank boundary.

## Question

Can chunk commit preserve numeric readout and semantic clocks while moving supported observed
records from H1 into H2, and can post-commit REPLACE/RETRACT work from current protected-factor
descriptors without replaying operation history?

## Main fixture

Nine snapshots:

```text
initial                 SUPPORTED
ASSERT alpha            HOT_REQUIRED
commit alpha            SUPPORTED
REPLACE alpha           SUPPORTED
ASSERT beta             HOT_REQUIRED
commit beta             SUPPORTED
RETRACT alpha           SUPPORTED
ASSUME temp             SUPPORTED
END_SCOPE temp          SUPPORTED
```

Registered counts:

```text
H1 observed [0,1,0,0,1,0,0,0,0]
H2 factors   [0,0,1,1,1,2,1,1,1]
total obs    [0,1,1,1,2,2,1,1,1]
```

Two successful commits must:
- leave memory_revision/evidence_revision/evidence_time unchanged;
- increment storage_epoch only;
- change readout by exactly0.

Final:
- storage_epoch2;
- memory/evidence/time =6/4/3;
- H2 reflected evidence revision4;
- H2 factor beta only;
- no hot records;
- operation history entries0.

Controls:
- empty commit -> NOOP;
- unknown observed relation -> OUT_OF_SCOPE read/commit, unchanged state;
- SPD-destroying update -> NUMERIC_UNSAFE read/commit, unchanged state;
- non-supported reads expose no numeric value.

All main snapshot reads must match independent full-reference solves within1e-10.

No learned Writer/Reader/Port Selector/Coverage classifier, model forward, language parser or training.
PASS does not establish Gate F.
