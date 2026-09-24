# V5-B residual token readout pilot v0.1 — C248

## Question and scope

Can an experimental residual token readout reach the original C244 normal-input recombination
criteria, compared with an equal-parameter EOS-only residual adapter?
This is a bounded architectural experiment motivated by the user's candidate discussion, not
adoption of a new FOLD production design. Do not modify accepted core/front-end/runtime files.
No fact slots, entity parser, key-value database, auxiliary loss or working memory is added.

C247 did not establish uniform TRAIN sufficiency at200 normal updates. It nevertheless showed
control-only TRAIN passes for Full234002, so reduced ordinary exposure alone does not explain
those C246 failures. Other cells remain ambiguous. Stop tuning the erasure mixture for now;
do not infer that the core alone or readout alone is the established cause.

## Candidate and matched control

Both arms privately copy the same original initial backbone and add exactly768 trainable scalars.
All original backbone parameters are trained as before; the backbone is not frozen.

Candidate token_read:
- H is the actual final post-core per-token state in Full, or the GRU sequence output in GRU-only.
- h is the actual EOS pooled state used by the existing readout.
- q=Wq*h, k_i=Wk*H_i, alpha=softmax(k_i dot q / sqrt(16)) over nonPAD slots.
- z=h+Wo*sum_i(alpha_i*H_i); the original LayerNorm and256-byte decoder receive z.
Wq,Wk,Wo are bias-free16x16 matrices:3x256=768 parameters. Values have no separate projection.

Control eos_adapter:
- z=h+W2*GELU(W1*h), with bias-free16->24->16 matrices:384+384=768 parameters.
- It never accesses non-EOS states. It increases readout capacity without adding token retrieval.

Both output matrices are initialized to zero, making initial outputs exactly equal to the original
backbone. Other head matrices use fixed seed+248000 under a private RNG context; head construction
does not perturb the backbone RNG. No favorable initialization or arm is chosen after results.
Total Full parameters14256;GRU-only10928. Capacity matches within each family, not between families.

The query comes from the entire EOS context, not an externally identified queried entity. Reading
all real tokens includes BOS/EOS and the question bytes. No gold location, row ID, entity label or
true value is supplied. The pilot can still learn shortcuts; attention is not proof of binding.
It does not claim sequence-order invariance or general-purpose fact extraction.

## Actual forward path and isolation

ReadoutPilot invokes the unchanged original model.forward. For token_read it temporarily captures
the final NEXT-route core output (Full) or GRU output (baseline) with per-call hooks, retaining the
normal autograd graph. A pre-hook on the existing readout_norm inserts the residual. It verifies
that the captured EOS equals the actual original pooled input and that the readout is invoked once.
All temporary hooks are removed in a finally block, including on an exception. States are local to
one forward; no cross-example/cross-model cache or learned persistent state is introduced.

This experiment is CPU/NEXT-only as in the accepted task. PAD slots have exactly zero attention
weight. Both arms retain original readout norm/decoder and route/core behavior. They use separate
model copies, not simultaneously installed hooks on a shared model. Production files stay intact.

## Data, training and comparisons

Keep original C244 TRAIN64/HOLDOUT32 and all row bytes/order/targets/provenance. Use the C247
saved split as its exact hash-matched copy. Restore the established C244400-normal-update recipe
for BOTH new arms, rather than comparing architectures under the often-insufficient200-update
control budget. This is not a C247 retry or an extension of its accepted run.

Create common Full/GRU backbones for each seed234001/234002/234003 before either is trained;
copy each family into its two arms. Common initial fingerprints must match C247.initial_sha256.
Zero-head initial TRAIN metrics must match C247.initial_train within1e-9. C247.final is not reused
as training initialization. The twelve checkpoints are newly trained from those common initial states.

Same AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32,float64,CPU,threads2,
deterministic algorithms. Alternate old32/added32 for200 cycles. No erasure or special input aid.
Fit executable AST is the C244 normal fit except its progress tag. Actual batch tokens are checked.
Only TRAIN is scored initially;HOLDOUT is first evaluated after step400 and during checkpoint replay.
No early stopping,holdout-driven tuning,seed replacement or best-checkpoint selection.

Compare newly trained token_read vs newly trained eos_adapter within the same seed/family/language.
The two arms have equal added capacity,not equal FLOPs,latency,memory or architectural function.
Extra per-token work and Python hooks make speed claims inappropriate. A difference does not
uniquely identify attention versus gradient routing or nonlinear parametrization as its cause.

## Gate and workload

Primary:every token_read Full seed/language cell meets BOTH TRAIN/HOLDOUT original criteria:
normal accuracy>=0.90;fact/query/order paired both-correct>=0.80;both mask drops>=0.35.
TRAIN32 rows/language and16 pairs:type minima29/32 and13/16. HOLDOUT16 rows/8 pairs:minima15/16,7/8.
Other family/arm gates are reported independently. Control success cannot substitute for reader
success. A reader PASS with a matching control is not evidence of reader superiority.

Twelve models=3 seeds x2 families x2 arms. Each receives400 updates,12800 training presentations.
Totals4800 updates/153600 training presentations. Per model15 scoring forwards/768 scoring rows,
including initial TRAIN,final both splits,and reload both splits. Totals4980 full-model forwards/
162816 row presentations. One saved bundle contains12 ordered states. No parent-model rerun.
The wrapper's one backbone execution is its one full-model forward,not two independent inferences.
Serialized sizes and fit seconds are recorded;peak memory and FLOPs are not measured here.

Any integrity fault is INVALID / RETRY SAME C248. A valid primary miss is ACCEPTED VALID NEGATIVE;
a pass supports only this internal bounded recombination fixture. It does not establish language
understanding,core superiority,unique mechanism,production adoption or Gate F completion.
Judge C248 before C249. Numeric-memory tuning remains paused.
