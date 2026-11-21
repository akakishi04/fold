# V5-B directional boundary diagnostic v0.1 — C274

C273 validly failed its all-five capability gate. dual_boundary produced one fully passing state but
degraded shared-suffix behavior across the cohort. Before introducing another fusion rule,C274
directly measures the two directional boundary components.

Compare two fresh matched readers:
- first_boundary: read.query receives only the FIRST visible query-byte pre-core state.
- final_boundary: read.query receives only the FINAL visible query-byte pre-core state.

Both use C269.query_span_mask(tokens),the same14256 parameters,state_dict keys and matched initial
tensor values. No learned C273/C272 checkpoint initializes C274.

The scientific question is diagnostic,not a winner/capability gate:
How do first-only and final-only query-boundary states differ on shared-prefix versus shared-suffix
transfer under the exact paired CE policy?

Predeclare the main reported directional contrasts:
1. unseen three-character shared_prefix2: first_boundary versus final_boundary;
2. unseen three-character shared_suffix2: first_boundary versus final_boundary.

Also report tripled and the complete original two-character task for both arms. Use the existing
fixed cell gates as descriptive per-seed measurements,but do not turn pooled superiority into a
candidate PASS or Gate F claim.

Fresh seeds274001..274005. Train on the exact C267 two-character TRAIN split with96 paired query
groups,48 rows/update,800 updates,mean CE,AdamW lr0.005. Evaluate both original two-character and
C270 three-character tasks,strict checkpoint replay,and persisted metric reconstruction.

C274 formal PASS means diagnostic execution/integrity completed exactly as preregistered. It does
NOT mean either first_boundary or final_boundary is a capability winner. A valid directional result,
including no directional difference,will be accepted and used to design C275.
