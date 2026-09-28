# V5-B boundary-pair query v0.1 — C272

C271 validly failed its whole-state gate. Endpoint query sharply improved unseen three-character
shared-prefix names but degraded shared-suffix names and the trained two-character family. Mean-span
showed the complementary pattern. This motivates one symmetric structural question rather than
another loss or seed retune.

C272 compares:
- mean_span: the accepted C269 arithmetic mean over all visible query-byte pre-core states;
- boundary_pair: the arithmetic mean of only the FIRST and FINAL visible query-byte pre-core states.

Both use the same C269.query_span_mask(tokens). For one-byte query-blind "?", first==last and the
state is not double-counted semantically; averaging identical positions returns that single state.
For multibyte Japanese identifiers, positions are bytes, not assumed Unicode characters.

The hypothesis is bounded: shared-prefix names differ near the end while shared-suffix names differ
near the beginning, so exposing both boundaries may preserve both distinctions without adding
parameters. This does not assert a causal parser or guarantee success.

Fresh seeds272001..272005. Both arms start from exactly matched14256-parameter states with disjoint
storage. Train only on the exact C267 two-character TRAIN split using the same paired48-row CE-only
policy as C271:800 updates,AdamW lr.005,200 exposures per TRAIN row,profile updates268/268/264.
No C271 learned checkpoint initializes C272.

Evaluate every final model on both the original two-character C267 task and the C270 unseen
three-character task. Primary PASS requires all five boundary_pair states to satisfy every fixed
criterion on BOTH tasks. mean_span is a matched control and cannot rescue the candidate.

A PASS would establish only that this fixed boundary summary improves this authored byte-level
binding family under the registered policy. It would not prove arbitrary names,natural language,
unbounded length or Gate F completion. A valid miss is accepted without changing boundaries,
weights,seeds,steps,data or thresholds.
