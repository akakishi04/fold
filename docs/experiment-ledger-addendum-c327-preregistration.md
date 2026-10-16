# C327 preregistration -- frozen checkpoint gradient alignment

Authoring date:2026-10-17 Japan time.
Experiment:C327-v5b-frozen-gradient-alignment;stage:V5-B-FROZEN-GRADIENT-ALIGNMENT.
Acceptance base:c3aff2fe3a6067860d19e76903b8f50677984467.
C326 remains ACCEPTED VALID NEGATIVE;Gate F NOT PASSED;C328 NOT REGISTERED.
This contract is immutable after acceptance. Activation requires a separate
committed-remote-byte post-authoring review and authoritative handoff update.

## One scientific question

At all ten fixed C326 final checkpoints, are ordinary TRAIN loss gradients for
original four-character names and interior-order four-character names opposed,
when logical rows, profile slot and language are matched?

This is a diagnostic, not another fitting run. It measures terminal local geometry,
not the entire training trajectory, a proof of causal interference, the actual
AdamW/preconditioned/clipped update, or the effect of a finite parameter step.
It cannot directly explain failure on original length-six or other unmeasured tasks.

## Fixed cohort, objectives and state

Reuse ALL C326 seeds326001..326005 and both epoch4/batch4 final states. Do not select
successful checkpoints, add seeds, initialize fitting from them or update weights.
For each model, separately use three original profile slots (repeat, shared_prefix,
shared_suffix) and both languages(en,ja):six pairs/model,60 objective pairs total.
Only TRAIN logical rows enter the objectives. Each objective contains all96 TRAIN
rows of its language, in unchanged dataset order. Both families use the same targets
and intact source query pairs. No HOLDOUT row or label is used to form a gradient.
The interior profile is the corresponding fixed C324 template slot, not a relabeling
chosen from model output. Models use native mean_last in eval mode, CPUfloat64,
2threads,deterministic algorithms,14256 parameters including3328 core,64 slots.

Temporarily enable autograd on ephemeral loaded models, not learning/optimizer steps.
Compute ordinary mean cross-entropy gradients with torch.autograd.grad over the
complete named-parameter inventory. Retain connectivity bits for each tensor;
unused tensors are explicitly represented by zeros, not silently dropped. Connected
zero gradients remain distinguishable from unused tensors. No param.grad accumulation.
Check every model state fingerprint and hooks before/after, and after each objective
pair. No checkpoint is written. The protected parent files remain read-locked.

For each pair measure original then interior, and repeat interior then original.
Require repeat maxabs error<=1e-9, identical connectivity and loss difference<=1e-9.
Every one of the four forwards must match the corresponding protected C326 saved
TRAIN logits with maxabs<=1e-9 and identical argmax. The stored losses are independently
reconciled to CE of those parent logits during saved-result reconstruction.
These repeats test measurement reproducibility; they do not refit/replay C326 training.

## Quantities and partition

Persist the first original/interior gradient vectors for all60pairs and the reverse
repeat receipts, native parameter layout, row-ID hashes and per-model work receipts.
Report raw dot product, both norms, cosine and zero-gradient cases. Do not insert an
epsilon denominator; cosine is null when either norm is zero. No desired sign is
required. Raw cosine is checked within floating tolerance, not silently clamped.

Partition named parameters into backbone.core.* (core), read.* (Reader), and all
remaining parameters (other). The all group is their disjoint union. Verify the
core count3328 and total14256, unique layout and sum-of-partitions dot/squared-norm
conservation. Reader is the read.* module, NOT a claim to include all output-head
parameters. Record the same statistics for all four groups.

For g_old and g_inside also report the first-order directional derivatives along
-(g_old+g_inside)/2. A negative raw dot alone need not make this mean direction
harm either objective. This is Euclidean unpreconditioned geometry, not actual AdamW
motion, and a first-order sign is not proof about a finite update.

All60pair records and240partition measurements remain in measurements.json.
Console reports40 seed/arm/group aggregates:6 profile-language pairs each, negative
dot count, defined cosine count, min/median/max cosine, and joint-descent count.
Do not average away failed measurement integrity or call repeated seeds independent.

## Work and fixed gate

Scientific cohort:10 fixed loaded models;60 gradient pairs;240 objective forwards
and240 autograd gradient evaluations;23040row presentations;960internal core forwards;
10 model state loads;one model bundle read andone evaluation bundle read.
0training updates,0optimizer steps,0new checkpoints,0network calls.
Saved raw gradient payload:13685760bytes(60*2*14256*8), separate from metadata,
connectivity,serialized bytes and peak process RSS.

A fixed native preflight before regression probes seed326001/epoch4, first profile,
English TRAIN rows:4forwards/4gradient evaluations,384rows,16core forwards,0updates,
one separately scoped checkpoint state load. The cohort still measures every state.
Parent semantic reconstruction, saved reconstruction, preflight and software tests
are explicitly outside the scientific cohort counters; they are not free work.

PASS means complete diagnostic integrity:all inputs/identities,240 measurements,
reverse repeats, unchanged states, finite vectors, valid null cosines, partition
conservation, saved reconstruction and envelope verification. There is NO conflict
sign/frequency or capability gate. A zero/positive/negative alignment is reported as
measured, not turned into an execution failure. C326/Gate F verdicts stay unchanged.
Integrity failure means INVALID/RETRY SAME C327, not a capability negative.

## Mandatory parent and source/input inheritance

Parent execution:dbef3dbc1566ff2c8c30405e9c8d207f5e79f460.
Parent publication:4b94198f36af10ee319cd00c5a908b95426d8464.
Parent folder:runs/c326-mixing-bbd9cd8f43db45f18b2370f2c3337dfa/.
Primary science/summary.json SHA256:
0dd7af1c69774f5d00b1ee654284c38731f4233b2b858aedcf1bf0aaa77656aa.
Mandatory execution-envelope.json SHA256:
d379e907d3d9668f47b9690cb097398005b6c0c6c349ac30082ac3590d7dc62a.

Validate BOTH fixed parent records, C326 identity/FAIL, original manifest/work,
full5610-test receipt, semantic completion and final1533 input rereads. Both records
must carry the identical full814source/1533input union. Verify every inherited source
Git blob and input byte. Validate the8immediate outputs,summary and envelope.
Use unchanged C326.semantic_recheck under no_neural to reconstruct all fixed parent
metrics/plan/summary from its saved checkpoint/evaluation bundles. No parent forward
or recursive older semantic reexecution is claimed by this parent verification.
Diagnostic model forwards afterward are explicitly counted new work.

C327 protects820sources=814inherited+6own;
1549inputs=1533inherited+10parent files+6own.
Own files:benchmark,execution helper,test module,runner,launcher,this contract.
Every direct/lazy repository dependency and inherited supplemental test is protected.
No accepted module global/function or source is patched. Use unchanged native R4
Windows read leases through the entire worker, independent first-read reference
hashes and final uncached rereads of ALL1549inputs. No unlocked/cross-run fallback.

## Execution, artifacts and review

48own tests;5610inherited+48=5658selected tests;216modules;
5659before the sole inherited C204 exclusion. No additional exclusion or skip.
Actual suite identities/counts are checked;ordered-ID digest is printed. Full
regression runs in a separate ordinary interpreter with no science wrappers.
Only native gradient preflight and ALL5658success permit the diagnostic cohort.

Route:explicit PowerShell7 ->invoke_active_v2 ->invoke_c327 ->run_c327 ->c327_execution
controller ->worker ->parent verification ->native gradient preflight ->ordinary
regression ->60gradient pairs/reverse repeats ->saved gradient/geometry reconstruction
->1549final input rereads ->primary result/envelope ->fresh byte-verifier ->log publish.

Local-only outputs under runs/c327-gradient-<id>/science/:
diagnostic-plan.json,gradients.pt,measurements.json,validation-summary.json,summary.json.
The enclosing folder also contains execution-envelope.json,regression-result.json
and science/regression/verify process logs. Never publish gradient/checkpoint tensors.
Only console text goes to docs/experiment-run-logs/c327/latest.log and latest.json.

Hash/size-bind all4outputs immediately before/after saved semantic reconstruction,
then require the same hashes before summary/envelope creation. A fresh process checks
complete parent/child unions, all source/input/output bytes and sizes, full regression,
manifest/cohort/gate bindings. It is a byte verifier,not additional gradient recomputation.
Retain10second heartbeats,test progress and one completion line per measured model.

Manifest SHA256:
36fca7e0b0baea3b51adcaad167caa551033e0f802ab3f883d4f4f846cbc22ee.
After writing all6files,commit and reread their complete remote bytes. Compare Git
blob IDs to locally tested bytes; compile/UTF8/noNUL/free-global audits;rerun all48
tests plus CP932-default-text-open emulation. Toy finite differences, saved-vector
fixtures and worker-control fixtures are not native full FOLD execution. Record
review PASS separately before activation. Mandatory PowerShell AST chain remains.

Authoritative runtime is unchanged Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
No CI,package reinstall,paid service,artifact deletion or scientific refit.
Stale branch/HEAD/ACTIVE/dirtytree/missing dependency/AST failure is operational
SKIPPED before scientific logging/publication. Source/input/test/nonfinite/logit/
gradient/state/semantic/envelope failure stops SAME C327 without automatic retry.
Repair publication alone without redoing measurements. C328 remains unregistered.
