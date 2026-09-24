# C249 preregistration — frozen read-path ablation

Experiment:C249-v5b-frozen-read-path-ablation.
Stage:V5-B-FROZEN-READ-PATH-ABLATION.
C248 ACCEPTED VALID NEGATIVE;C250 NOT REGISTERED. Gate E PASSED;Gate F NOT PASSED.
This registers a frozen diagnostic,not retraining,production adoption or a new capability gate.
Activation requires committed-byte post-authoring review recorded in the authoritative handoff.

## One scientific question

Does original-input performance of the accepted C248 final networks depend on their added residual
branch and,for the token reader,on learned nonuniform read weights rather than uniform pooling?
Include every seed/family/arm,not only the eight successful reader cells.

## Accepted parent identities and semantic adapter

Acceptance/base:812d8a0452962c569303bade157aa802de20ea65.
Acceptance record:docs/experiment-ledger-addendum-c248-c249.md.
C248 execution HEAD:23bcc949638ea3e927ec0bb3d846b9f42b552a56.
Published log commit:5a3e7e7ae371b5f5f384d1283d68dd434201e6ec.
Publisher log SHA256:7a1984dd55d93253ea3498503873c0cb41fa3667dfa4f467b7ca0994e3dea99c.
Summary SHA256:99778defedd9854815f94989567687c64930e3b505449a847dd030be5a47dab6.
Local summary:runs/c248-v5b-residual-token-read-f3cd1bdfb2cf4a068ed091ea75bf8b22/summary.json.
Require exact valid FAIL,token_read outcomes BOTH_PASS8/RECOMBINATION_MISS4,and eos_adapter
RECOMBINATION_MISS12. C248's primary all-seed gate must not be relaxed to accept its eight cells.

Required C248 artifact hashes:
- measurements.json:d2c7f99d79e6ac2ddc47e5d5d900ccaea4479b2325c0d0b35e7a9f05f587e382
- readout-plan.json:bfaafd5c699690553aa072ba74b9707853a2e627b22a6d3d488b646f27047593
- split-dataset.json:e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346
- trained-models.pt:35e39b16f5a30f9a55d7718427294d4bba6255772ad7fdf183ea0275e310cdc3
- validation-summary.json:7130fbc17973ea9189313c60df880ea5b9593c1e1e0871f5ddeb08898c0e0dff

Use C248.validate_result and C248.summarize(refs,C242) on the actual parent schema. The C249
loader reads C248's own split/measurements,not C248.load_inputs which expects its C247 parent.
C248 records contain seed,family,arm,final_sha256,final[split][language] and predictions[split][view].
final_sha256 is the fully trained wrapper/backbone/head identity after400 updates,not the original
backbone_initial_sha256 or wrapper initial_sha256. Use final weights for every C249 calculation.

Load the accepted bundle through actual C248.load_bundle:fold-c248-residual-read-v1,12 ordered
states. Order is seed234001/234002/234003,then family full/gru_only,then arm token_read/eos_adapter.
Instantiate actual C248.ReadoutPilot around the original family backbone,strictly load every state
key,eval(),requires_grad_(False),and verify the original final fingerprint before scoring.
Constructing model containers is not training;their random initial values are entirely overwritten.
No earlier checkpoint is selected,no successful seed is singled out,and no state is updated.

## Inputs,interventions and restoration

Keep exact TRAIN64/HOLDOUT32,all row bytes,targets,order,provenance and rendering. The neural input
remains only tokens and NEXT-only tasks,with256-way output. No entity IDs or target locations.
CPU float64,threads2,deterministic algorithms. All gradients must remain absent.

Per model use this fixed order:
1. Intact normal/evidence_blind/query_blind on TRAIN then HOLDOUT:6 forwards.
2. residual_off on normal TRAIN then normal HOLDOUT:2 forwards,for both arms.
3. uniform_read on normal TRAIN then normal HOLDOUT:2 forwards,reader arm only.
4. Remove intervention hooks and repeat intact three views/both splits:6 restoration forwards.

residual_off returns h,the original pooled input supplied to the trained ResidualHead,instead of
its usual output. The trained backbone,LayerNorm and decoder are preserved. This removes the added
branch's contribution but is NOT equivalent to the separately trained original backbone or EOS arm.

uniform_read returns h+Wo*mean(H_nonPAD) using the same trained per-token states and output matrix.
All originally eligible real positions,including BOS/EOS and question bytes,remain eligible.
PAD weights are zero. No entity parser or semantically selected subset is introduced.
It replaces learned query/key weighting with uniform averaging only in the returned representation.
The original head still computes before the overriding forward hook;an additional output projection
is executed for uniform mode. This is a functional intervention,not a FLOP-saving implementation.

The original C248 wrapper still calls actual backbone.forward and its scoped state-capture hooks.
C249 adds only a scoped hook on model.read. Parameters are never edited. Hooks are removed on
intervention exit,including exceptions. After the completed audit,no temporary hooks may remain.
Input-token tensors are checked unchanged and model fingerprints remain equal to accepted finals.

## Measurements and integrity gate

Intact predictions must match all original C248 saved arrays exactly. Recompute the complete
original metric schema including NLL and mask drops;max metric error<=1e-9. Parent record schema
and normal/pair count contracts are checked. Unlike saved-argmax-only audits,this diagnostic does
run the model and retain logits,so NLL can be recomputed from actual output scores.

For each ablation report normal-only rows,accuracy,NLL,fact/query/order paired both-correct scores,
accuracy drop,NLL change,answer flips,lost/gained correct answers and max raw-logit change.
Do NOT fabricate evidence/query mask drops for ablation modes scored only on normal input.
Keep raw-logit effects distinct from argmax changes. All output classes remain eligible.

After restoration,all original predictions must return exactly and raw logits must match the
initial intact pass within1e-9. These restore outputs are validated online;only errors/identity flags
are stored for restoration,not duplicate restored-logit arrays. Checks on frozen weights and
absence of gradients are mandatory throughout. A branch-performance drop is not required.

C249 status PASS means diagnostic integrity only:parent identity/replay,fixed interventions,
unchanged weights/inputs,restoration,counts and persisted artifact recomputation. Any source,
artifact,schema,nonfinite,replay,mutation,test or workload fault is INVALID / RETRY SAME C249.
Do not alter C248 or Gate F for any result. No production adoption.

## Exact workload,protection and artifacts

Six readers each16 model forwards/768 row presentations;six EOS controls each14/672.
Totals180 full-model forwards/8640 rows. The wrapper plus its single backbone execution counts
once,not twice. One accepted bundle is deserialized into12 states;new training0,checkpoint writes0,
scientific network calls0. Historical regression and authoring fixtures are separately scoped.

Store5184 logit rows:intact and intervened only. Restoration contributes3456 evaluated rows but
no duplicated raw arrays. Normal contrast cells72=6x2x2x2 reader cells+6x1x2x2 EOS cells.
Postcheck reconstructs tensors as float64,recomputes all retained metrics and contrasts,verifies
original parent predictions/metrics and final identities,and runs no further model forward.

Inherit C248334 source pins/526 protected inputs. Add its summary+five artifacts and OWN6:
340 source pins/538 inputs. Direct dependency union25:five C231 LM_SOURCES plus C230 through C249
helper/entry modules. All original model/core sources remain inherited and protected. No accepted
source/test/log is edited and no mutable control state is asserted in historical tests.

OWN6:the C249 benchmark,test,runner,launcher,this preregistration and docs/v5b-frozen-read-ablation-v0.1.md.
Own tests24;modules134;loaded3146/focused3145. Only inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Use actual loader counts and unique IDs;synthetic filter testing is not a historical regression PASS.

Five ignored artifacts:ablation-plan.json,logits.json,diagnostics.json,contrasts.json,validation-summary.json.
Summary includes execution,source/input hashes,artifact hashes/sizes and diagnostic integrity flags.
Only console log and receipt are published to docs/experiment-run-logs/c249/latest.*.
Manifest SHA256:9fd82672124ff0227174d7a9df894c67ca9f1958a36fad6cbc575e1179dfa414.

## Interpretation,review and stop

A drop under ablation is an effect of changing the computation of this frozen network,not proof
of a unique semantic mechanism or the cause of its training success. Jointly trained branches
can co-adapt;changing a branch shifts internal distributions and normalization. Uniform-read
results do not predict a model trained with uniform attention. A null effect does not rule out
a training-time benefit. This is not independent-seed replication,an external test set or a remedy
for the failing C248 seed. Report every model/split/language rather than selecting favorable cases.

Re-fetch all six completed files at fixed review HEAD,match code/script blobs to tested bytes,
compile/import,run24 own tests,audit globals,parent writer/load signatures,intervention equations,
PAD behavior,restoration,counts and CLI/parser order. Synthetic tests use real torch GRU but a
synthetic Full Core interface double;they do not validate the actual learned FOLD checkpoints.
Record exact performed/pending checks in authoritative handoff before issuing a command.

Dispatcher/launcher/runner ParseFile -> Python/source/parent precheck ->24 own tests ->3145 focused
tests ->C249 frozen diagnostic ->postcheck ->log publication. Branch/tree/HEAD/ACTIVE mismatches
skip before execution/publication. Transport-only failure does not justify repeating completed
model work. No training,threshold rescue,production change,paid API,external data,cleanup or history
rewrite. Numeric-memory/erasure-mixture tuning remains paused. Judge C249 before C250.
