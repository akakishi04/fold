# V5-B dual-boundary attention v0.1 — C273

C272 validly failed its whole-state gate, but boundary_pair substantially reduced collapse and
improved shared-prefix transfer relative to mean_span. The remaining candidate weakness is strongest
on shared-suffix transfer, and one fresh seed still shows broad instability.

C272 combines first and final query-boundary states BEFORE the query projection/attention softmax:
q = query(0.5*(first_state+last_state)).
Because query is linear, the two boundary signals are blended into one score field before memory
selection.

C273 tests one structural alternative with no added parameters:
- boundary_pair: the accepted C272 architecture;
- dual_boundary: compute q_first=query(first_state) and q_last=query(last_state) separately, produce
  two independently masked attention softmaxes over the same pre-core memory, retrieve two memories,
  then average the retrieved memories before the shared read.output projection.

Thus the distinction is where the two boundary signals are combined: pre-softmax query space versus
post-softmax retrieved-memory space. The same query/key/output parameters are reused for both
dual-boundary attentions. For one-byte query-blind "?", first==last and the two attention paths are
identical.

Fresh seeds273001..273005. Both arms have exactly14256 parameters, identical state_dict keys and
matched initial tensor values with disjoint storage. Train only on the exact C267 two-character
TRAIN split using paired48-row batches, ordinary CE, AdamW lr0.005 and800 updates. No accepted learned
checkpoint initializes C273.

Evaluate every final state on both the original C267 two-character task and the C270 unseen
three-character task. Primary PASS requires all five dual_boundary states to pass every fixed
criterion on BOTH tasks. boundary_pair is a matched control and cannot rescue the candidate.

A PASS would support keeping boundary signals separate through attention in this bounded byte-level
binding task. It would not prove a general parser, arbitrary-name understanding, unbounded length or
Gate F completion. A valid miss is accepted without retuning seeds,weights,boundaries,data,steps or
thresholds.
