# C248 preregistration — residual token readout pilot

Experiment:C248-v5b-residual-token-read-pilot.
Stage:V5-B-RESIDUAL-TOKEN-READ-PILOT.
C247 ACCEPTED VALID NEGATIVE;C249 NOT REGISTERED. Gate E PASSED;Gate F NOT PASSED.
This registers an experiment-only candidate,not adoption of a new production design. No accepted
runtime/core/front-end/test source is edited. Authoritative handoff activation requires review.

## One question

Can a residual reader that revisits actual token states meet the original normal-input binding
criteria,compared with an equal-parameter EOS-only adapter? The primary gate is bounded capability;
the paired comparison limits capacity confounding. It does not presume attention is the cause or
that the earlier core has been shown deficient. Erasure-recipe tuning is paused.

## Accepted parent and semantics

Acceptance/base:521eff1865cd13224ff5a2a247c466a6ba330d3e.
Acceptance record:docs/experiment-ledger-addendum-c247-c248.md.
C247 scientific execution:6705aa76bf70ec2685100c47e1abe9cec3625523.
Published log commit:539bdb7860f1a9a5d59046c43d006c9989b636d9.
Publisher log SHA256:65402c6ffeb4147e71b3ca1228b4a761e391676d550aef2c7e0cf3908e06150c.
C247 summary SHA256:2f77f23ee7b77016ad44e1900b7396bbe07855e13429adc32cded0d0276ce404.
Local summary:runs/c247-v5b-normal-exposure-a3cec4a219a14360bac90cf8d7303da5/summary.json.
Require exact execution-valid FAIL and comparison_counts BOTH_TRAIN_PASS2,CONTROL_TRAIN_PASS_ONLY2,
NEITHER_TRAIN_PASS8. Do not reinterpret secondary HOLDOUT as the deciding C247 primary gate.

Required parent artifacts:
- control-plan.json:f9558bfead121a605f8cc2dd776eed5db6db981c1c20b675d44d49d4b95a502c
- measurements.json:14d37a60a23db8475a0161c70cc7bc3c92e034b7f1329012746ebbd9349c62a1
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346
- trained-models.pt:809d248f31f56f7c07c2e53637277a3fd0c62edbaa409d6c47e565421cf7d79f
- validation-summary.json:2301115ce19ca0422858054bd29de9b92f2ca2335e7e8e7d586006bb860a61b2

Context roles:C247 parent,C244 base,C242 fitting,C234 binding,C231 factory,accepted audit helper.
Validate actual C247 result and reproduce its measurement summary with C247.summarize(refs,C242).
The C248 loader reads C247 files directly;do not call C247.load_inputs with the wrong parent schema.
initial_sha256 is the pretraining backbone fingerprint;initial_train is its original TRAIN64 score.
final/predictions are after200 control updates and are used only to validate accepted evidence.
C248 initializes no weights from trained parent state dictionaries. Their bytes remain protected.

## Data and initial states

Keep byte-identical original C244 TRAIN64/HOLDOUT32 as saved by C247. Preserve all row order,IDs,
prompts,targets,provenance and the normal/evidence_blind/query_blind evaluator inputs. No auxiliary
labels,entity IDs,answer-location oracle,parser or row IDs enter the neural model.

For each seed234001/234002/234003,construct original Full and its common-weight GRU-only copy before
training either family. For each family,deep-copy the fresh backbone for arms token_read and
 eos_adapter. All backbone fingerprints must match C247.initial_sha256. The added heads are
initialized under private RNG seed+248000 without altering global state. Zero output projections
make both arms initially identical to the original function. Verify initial TRAIN metrics against
C247.initial_train within1e-9 before learning;authoring tests separately compare raw initial logits.

## Two arms, matched capacity

Original backbone sizes:Full13488,GRU-only10160. Each arm adds768 independent scalars:
Full14256,GRU-only10928. No discarded/dormant production core is counted as a new learned reader.

Token reader:actual final token states H and EOS state h. Use three bias-free16x16 matrices:
q=Wq*h;k_i=Wk*H_i;alpha=softmax(k_i dot q /4),masked exactly on PAD;z=h+Wo*sum(alpha_i*H_i).
Wo starts zero. There is no separately learned value projection. All nonPAD slots,including BOS,
EOS and question bytes,are eligible. The query is a learned transform of the whole EOS context,
not a separately parsed queried noun or a gold semantic key. No fact slots are constructed.

EOS control:z=h+W2*GELU(W1*h),bias-free16->24->16,with W2 initially zero.384+384=768 parameters.
It only sees the existing EOS state. All backbone and head parameters are trained jointly in both
arms;this is not a frozen-encoder linear probe. Equal parameter count is not equal compute or
identical optimization geometry;do not attribute a difference to one internal mechanism.

ReadoutPilot calls the actual original backbone.forward. The reader obtains the real final NEXT
core output in Full through a scoped core forward hook,and actual GRU output in GRU-only.
The original readout_norm input is replaced by the residual representation through one pre-hook.
Require captured EOS to equal the actual pooled input,expected capture count and one readout call.
Temporary hooks are always removed in finally and no state persists between calls. Preserve the
original autograd graph;do not detach captured states during training. No accepted source rewrite.
Only CPU/NEXT tasks are supported by this bounded pilot,as in the existing task. No latency claim.

## Training and endpoint

Both new arms use C244's400 NORMAL updates,not C247's200-step diagnostic-control budget.
Same alternating old32/added32 schedule for200 cycles,batch32,AdamW lr0.005,betas(0.9,0.999),
eps1e-8,weight_decay0,clip1,float64,CPU,threads2,deterministic algorithms. The exact fit AST is
C244.fit except its progress label. Audit all400 row-index selections. No erasure or added loss.
The 400-step choice is fixed before results,not a continuation of C247 or a rescue of its gate.

Each model is evaluated initially on TRAIN only. HOLDOUT first reaches evaluation after step400,
then checkpoint replay. No tuning,early stop,best-checkpoint choice or favorable seed selection.
Use C242.evaluate/validate_metrics/cell_pass and C234 renderer/paired metrics. Original256-byte
argmax is unconstrained. Every normal and control-view score is retained per arm/family/seed/language.

Primary:all token_read Full cells must meet BOTH TRAIN and HOLDOUT original criteria:
normal accuracy>=0.90;fact/query/order paired both-correct>=0.80;both mask drops>=0.35.
TRAIN32 rows/language,16 pairs/type:minima29/32 and13/16. HOLDOUT16 rows/8 pairs:minima15/16,7/8.
Other family/arm gates are reported separately. status PASS iff gates.token_read.full is True.
A control PASS cannot substitute for a candidate PASS. A candidate PASS with equal control success
does not establish an advantage for rereading. Report all12 paired HOLDOUT accuracy deltas.
A valid primary miss is ACCEPTED VALID NEGATIVE. No threshold changes or automatic architecture adoption.

## Workload and integrity

Twelve new models in seed,family,arm order;arms token_read then eos_adapter.
12x400=4800 updates/153600 training presentations. Per model initial TRAIN3 forwards/192 rows,
final TRAIN3+HOLDOUT3/288 rows,and reload6/288. Totals180 evaluation forwards/9216 scoring rows,
4980 full-model forwards/162816 total rows. Before reload409 calls/13280 rows/model;after415/13568.
One new checkpoint bundle contains12 state dicts. Wrapper+its one backbone call is one full-model
execution,not two independent inferences. Extra readout work is not concealed by that call count.
No parent model rerun or scientific network call. Tests run separately on synthetic data/models.

Require common-backbone identity,zero-residual initial metric replay,head and whole-model weight
updates,non-mutating evaluation,actual update/row counts,strict bundle schema/order/fingerprint,
exact final prediction replay and raw-logit/metric error<=1e-9. Reuse C244.replay_one with C242 fitting;
its per-model replay is independent of the collection's12-model count. Never use a six-model
parent collection summarizer for these new records. Schema:fold-c248-residual-read-v1.

Parent328 source pins/514 inputs plus its summary+five artifacts and OWN6 gives334 pins/526 inputs.
Direct dependency union24:five C231 LM_SOURCES plus C230 through C248 helper/entry modules.
All actual lazy helper imports and original language/core source remain inherited and protected.
OWN6:the benchmark,test,runner,launcher,this preregistration and docs/v5b-residual-token-read-v0.1.md.
Own tests24;modules133;loaded3122/focused3121 with only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Enforce actual suite counts and unique IDs;synthetic filter tests are not historical regression passes.

Five ignored outputs:readout-plan.json,split-dataset.json,trained-models.pt,measurements.json,
validation-summary.json. Records contain arm,backbone_initial_sha256,initial/final fingerprints,
initial_train,initial_metric_error,final,predictions,parameters,head update flag and measured counters.
Postcheck validates hashes/sizes,plan,split,paired summary,common initial identities and saved
discrete metrics via C243. Fit time and artifact bytes are recorded;peak RAM/FLOPs are not measured.
Only console log/receipt are published. Manifest SHA256:
bfaafd5c699690553aa072ba74b9707853a2e627b22a6d3d488b646f27047593.

## Review and stop

Re-fetch all six completed files at immutable review HEAD;match code/script blobs to tested bytes,
compile/import,run24 own tests,inspect parent schema/loader/summary/replay signatures and actual
Full/GRU forward implementation. Test raw zero-head identity,gradients,non-EOS access,PAD exclusion,
RNG preservation,hook cleanup,capacity,initial mismatch,full12-model run/replay/postcheck and controls.
Audit free globals,fit AST,CLI arguments,counts and parser/publication order. Record performed and
pending checks. Synthetic CheapCore/CheapGRU are interface doubles,not real FOLD model validation.

Dispatcher/launcher/runner ParseFile -> Python/source/parent precheck ->24 own tests ->3121 focused
regression ->paired pilot ->postcheck ->log push. Operational branch/tree/HEAD/ACTIVE mismatches
skip before execution/publication. Integrity faults are INVALID / RETRY SAME C248;transport-only
failures do not justify retraining. Preserve accepted evidence and tools/run_c167.ps1.
No production change,external corpus,paid API,cleanup/history rewrite,Gate F promotion or automatic
C249. This adaptive internal task does not establish general language or unique mechanisms.
