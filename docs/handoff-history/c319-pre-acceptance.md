# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C318 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C319 ACTIVE / NOT YET JUDGED. C320 NOT REGISTERED.**
C319 is the unique ACTIVE from-scratch mean-plus-last versus last-only comparison;no result yet.
C317 diagnostic PASS,C316/C315 negatives,C308 bounded PASS and other old verdicts unchanged.
Latest accepted execution:f4624509c4311b3e7b04b3d861cfcb3e9d58bfd0.
Latest accepted publication:3444c11cb68c85e35202f65f26ba258aaadc2c1a. Do not rerun C318.

## Latest accepted evidence — C318

Acceptance:docs/experiment-ledger-addendum-c318-c319.md.
Acceptance commit:b43b820b94346be08646f8f5a0d499fb7824fb27.
Summary:runs/c318-v5b-readout-branches-bb278106ee824f26996434d7d895726a/summary.json.
SHA256:5b838ca1420dc36b146ba4afa548d889f16172bd1d1705e4f5df97a5664c5203.
Own24/focused5173 PASS;754sources/1418inputs;run_execution_valid=True.
All10 states restored original outputs with0.0 drift;single-byte controls held.
Pass counts by2/3/4/5/6:
Original,both cohorts:[5,5,5,5,4].
Mean-only,two_to_four:[4,0,0,0,0];one_to_four:[2,0,0,0,0].
Last-only,two_to_four:[5,5,5,3,2];one_to_four:[5,4,5,4,0].
Neither frozen isolation improves six reliability. Zero passing models is not zero accuracy.
Example only:one_to_four316005 six HOLDOUT English shared-suffix48/48->42/48 in last_only,
six regressions/no rescues. Do not extrapolate this group to all languages/profiles/models.
Diagnostic PASS is not capability PASS. All prior scientific judgments stay separate.

## Active C319 — trained last-only readout

Experiment:C319-v5b-trained-last-readout. Stage:V5-B-TRAINED-LAST-READOUT.
Registration:docs/experiment-ledger-addendum-c319-preregistration.md.
Design:docs/v5b-trained-last-readout-v0.1.md.
Review:docs/c319-post-authoring-review.md.
Authoring/review target:97a3baccfa4ab1d48a7ca4d98d2ead91f4fa8cbe.
Acceptance base:b43b820b94346be08646f8f5a0d499fb7824fb27.

One question:can last-only trained from initialization attain unseen-six reliability relative
to native mean-plus-last? Fresh initial seeds319001..319005/orderseeds319101..319105. Arms
mean_last control and last_only candidate. All10 models start anew;no saved C316 state or good
core is reused. No old prediction becomes a target. Primary:ALL5 NEW last_only states pass SIX
local/masked gates. Native control cannot replace the candidate primary after results.

Both arms use unchanged two_to_four allocation:each original TRAIN row100times at2,3,4,
zero at1,5,6.1200updates,48rows/update,57600training rows/model. Actual C315.plan_for_order with
original C312 pair inventory produces identical rendered batches and intact paired questions
within each seed. No value balancing or one-character mixture is added in this comparison.
Both share independent copies of identical initial weight tensors. Since functions differ,
initial logits/losses need not match. No artificial loss calibration is authorized.

Model is actual C304 LengthReadout/C278factory,14256stored/configured-trainable parameters,
3328core,64slots. Actual C308 core_slow optimizer:coreLR.0005/noncore.005,ordinary meanCE,AdamW
betas.9/.999/eps1e-8/decay0,globalgradientclip1,FIT_RNG612000,CPUfloat64,threads2,deterministic.
No new weights,gain,auxiliaryloss,teacher,freeze,stop-gradient,earlystop or seed/budget search.

Actual C304 forward still computes two native query attentions and their .5 average. Child hooks
validate native call1=span-mean and call2=last-byte local state. Candidate substitutes last-byte
state for call1 only;control leaves both unchanged. Thus candidate uses .5*(last-memory+last-memory)
with total coefficient1,not a half-strength term. The actual vector norm/covariance/functional
flexibility are not equalized. Both attention calculations remain;no compute-saving claim.
Last BYTE is literal,not a whole Unicode character. Inputs and full256-class argmax unchanged.

Unlike C318's frozen probes,the selected representation is NOT detached;autograd reaches the
encoder/query/reader and existing core/residual path. Training forward requires grad-connected
local tensors. Validate one capture/two native queries,finite CPUfloat64 Bx64x16 intermediates.
Capture references clear after every call while returned output retains its graph. All hooks
clean up on normal/exception paths. No accepted method/global/source is monkeypatched.

The SAME child readout policy wraps all1200updates,final1..6 evaluation and strict checkpoint
replay. Save policy tags/receipts;wrong policy is INVALID. Per fit+eval1344forwards/71424rows/
5376core calls,2688query calls,1200grad-enabled forwards. Replay144forwards/13824rows/576core,
288query calls,zero grad-enabled forwards. Full/core weights change during learning and remain
fixed during evaluation. All final outputs replay<=1e-9 and exact argmax. No inference-policy swap.

Evaluate original1..6 prompts,normal/evidence-blind/query-blind,English/Japanese and original
TRAIN/HOLDOUT values.1 has one canonical profile,untrained/descriptive in both arms;2..6 have3.
Same C304/C270 local gatesaccuracy.90/query_pair.80/evidence_drop.35/query_drop.35/two_order.80.
Report100state/length/split partitions,20single diagnostics,all10flags and5paired-six outcomes.
C319 candidate5/5 is bounded capability PASS,not diagnostic-only PASS,superiority or Gate F.
Same repeated task is not new-data validation;no universal branch-necessity conclusion.

## Parent contract,protection and workload

Verify45 ordered summary hashes BEFORE exact C318.verify_artifacts(parentdir,44ancestors,
accepted execution HEAD). Require diagnosticPASS,four actual output descriptors and exact C318
outcome table. C318 owns no model/dataset bundle. Its load_parent on paths[1:] returns verified
canonical C316 data/prompts. Recheck DATA/PROMPTS SHA values;ignore ancestor learned states for
scientific initialization. Child model factory creates all fresh states normally.

Sole direct import C318. Context supplies C317/C316,C315schedule/evaluate/replay,C304model/span/
scorer,C308optimizer,C287normalizer,C312/C296pairing,C310no-neural/backend. Retain all754sources/
1418inputs and actual local helper/factory-language coverage. Add OWN6+5C318files:760/1429.
No accepted file changes,new regression exclusion or source-protection waiver.

Science10new models,12000updates,576000training rows,14880forwards,852480row presentations,
59520core calls,10strict state loads,one10-state model bundle write/read,network0. Final evaluation
and replay included;operational probes,regression and recursive parent reconstruction separate.
Seven artifacts plus summary:architecture-plan.json,dataset.json,length-datasets.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Schemas:
fold-c319-trained-readout-models-v1 and fold-c319-trained-readout-eval-v1. Ordered seed/arm IDs,
policy tags,loss/LR/gradient traces,actual schedule,full/core hashes and final logits retained.
No overwrite. No-neural postcheck reconstructs every score,fit policy and JSON;all tensor/JSON
hashes/sizes verified. Full arrays local/ignored. Own24/modules204/loaded5198/focused5197.
Manifest:61d98e2b6289a9e11ac0bd915df26e7e07a932895d13b2730e2d675f3b6e0a7e.

## Post-authoring review and runtime boundary

post_authoring_review=PASS. All6 OWN refetched at97a3baccfa4ab1d48a7ca4d98d2ead91f4fa8cbe,
independent Git-blob matches6/6 and rechecked after tests. Post-match uninterrupted full runs:
normal24/24 PASS17.675s;CP932-default-emulated24/24 PASS18.501s;zero failures/errors,exit0.
Encoding patch covers import/setup/tests/teardown. Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5;
PowerShell unavailable. BothPython+3embeddedblocks compile,UTF8/noNUL,unresolvedglobals0,manifest
seal matches,45paths/CLI[2:47]/head47/argc48 checked. Accepted sources/tests/dispatchers unchanged.

Tests execute actual C304forward/span and C315 fit/eval/replay function ASTs with controlled
components. Controloutputs+gradients exactlynative;candidate independent formula outputs<=1e-13/
parametergradients<=1e-12;nonzeroencoder/querygradients. Actualcandidate1200steps+eval/replay and
control1200loop-equivalence tested,plus45hashguards,760/1429protection,loader/policy/run ordering,
semantic suite IDs,persistence/tamper/scope and no graph-retention checks. Support files are exact
function slices,NOT complete modules/repository and NOT committed. Synthetic models/scorers/
pairing/optimizer/Git/parent substitutes are software controls,not actual FOLD capability or
full5197 regression evidence. Review details every limitation including runtimeprobe substitution.

Mandatory user Validate still requires45real archives/Windows pins,PowerShellParseFile,real paired
factories and native/last-only forward/backward probes,own24/full5197regression. Only discarded
probe copies use fixed nonzero read.output to avoid a vacuous zero-head check;scientific initial
weights untouched. All10actual fits and strict same-policy replays remain pending Execute.
Activation preserves all6 reviewed OWN and every accepted source/test/log/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C319 -> Validate(45parents,760/1429,
all5fixed schedules,real readoutgradientprobes,own24,focused5197) -> authoring_runtime_preflight=PASS
-> Execute(10freshmodels*1200updates,same training/eval/replay policy,all1..6scores,strictreplay,
pairedsixresults,persistedreconstruction) -> log publication. Validate failure skips science/publish.
Integrity failures repair SAME C319 without changing science. Valid candidate six<5/5 is ACCEPTED
VALID NEGATIVE. No post-result seed/readout/gate/budget adjustment. C320 waits for formal C319
judgment;old verdicts and Gate F remain unchanged. Scientific HEAD differs from log-publicationHEAD.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted seals and immutable historical tests.

## Historical state

Pre-activation:docs/handoff-history/c319-pre-activation.md.
Git blob:2c4ca2bf62f819c34999943b72bdfa7278e339a2.
Previous:docs/handoff-history/c318-pre-acceptance.md.
Git blob:fe5fd87ac49999cc298e666d9dd887acfe7666fd.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
