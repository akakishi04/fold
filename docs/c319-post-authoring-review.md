# C319 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review plus executed local software tests,NOT actual FOLD science.
Review target:97a3baccfa4ab1d48a7ca4d98d2ead91f4fa8cbe.
Acceptance base:b43b820b94346be08646f8f5a0d499fb7824fb27.

## Committed bytes and scope

All6 OWN files were refetched after commit at the immutable target. Source412lines and tests443lines
were reread in consecutive ranges;the truncated source response was expanded again through its end.
The other4 files were read in full. Returned whole-file Git blob IDs match independently hashed
local bytes6/6. Acceptance-to-authoring comparison contains exactly these six additions:

- fold_lm/v05_benchmarks/model_c319_trained_last_readout.py:8222ddc165464b8acb84380f47d397504308a9df;28281bytes.
- tests_lm/test_v05_c319_trained_last_readout.py:a769c63d492a5b34809f825a9c46b9014661a161;31925bytes.
- tools/run_c319.ps1:529f06d2d0b266af9b3fedeeed471b6a101534b0;4694bytes.
- tools/invoke_c319.ps1:a553641927716e81eb90a4844521b336fe820e97;7901bytes.
- docs/experiment-ledger-addendum-c319-preregistration.md:833d01dfaac46c8ba10d4a01bb354ec717253e63;9709bytes.
- docs/v5b-trained-last-readout-v0.1.md:990ec1bf9cb0353252e209b1936386f7dc465e94;988bytes.

No accepted code,test,preregistration,log or dispatcher changed. Activation must retain OWN6.

## Actually executed after all6 remote/local matches

Normal:python -u -m unittest tests_lm.test_v05_c319_trained_last_readout -v
Ran24 tests in17.675s;OK;zero failures/errors;process exit0.

Complete unchanged24-test module under io.text_encoding default-CP932 emulation:
Ran24 tests in18.501s;OK;zero failures/errors;process exit0. Patch covered module import,setup,
all tests and teardown,only mapping an omitted encoding to cp932. Both were uninterrupted full
suite runs. Each log was checked for exactly24 unique test IDs. Earlier pre-commit tests are not
substituted for this evidence. CP932 emulation is not full Windows or console emulation.

After both runs all6 hashes were checked again. Both Python files and all3 embedded runner blocks
compile;UTF8/noNUL. Recursive symtable/import-binding audit finds0 unresolved globals after
accounting for module bindings,builtins and normal module globals. Manifest self-hash matches:
61d98e2b6289a9e11ac0bd915df26e7e07a932895d13b2730e2d675f3b6e0a7e.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5;PowerShell unavailable locally.
Terminal cleanup messages after OK did not change successful exits.

## Behavioral checks and numerical meaning

The tests execute the actual accepted C304 forward/span ASTs with controlled encoder/core/readout
components. Control mean_last exactly matches native forward outputs AND every parameter gradient.
An independent single-attention last-only formula matches candidate outputs within1e-13 and every
parameter gradient within1e-12. Encoder and query-projection gradients are explicitly nonzero.
This tests the differentiable intervention,not only forward equality under no-grad. One-byte
query controls remain unchanged. Consecutive optimizer steps show no retained-graph dependency.
Detached encoder states,changed native query inputs and exceptions reject/clean up as specified.

The actual C315 fit/scheduler functions execute on a small loop fixture for all1200updates.
Child optimize matches every loss,optimizer-rate trace,gradient-receiver trace,schedule and final
weight fingerprint. A separate actual child candidate train_one performs1200updates,final144
forwards and policy-specific144-forward replay on the controlled C304-forward model. Replay
logit error is0.0. Wrong checkpoint fingerprints and wrong recorded readout policies fail.
This validates consistent training/evaluation/replay,not actual FOLD learning or transfer quality.

Canonical synthetic dataset and full1..6 prompt hashes match the accepted values. All5 schedules
retain0/100/100/100 row exposures and complete paired epochs. Factory tests check equal initial
fingerprints,independent storage and14256configured parameters;controlled toys use padding for
capacity-contract tests,so their unused padding is not real FOLD active-capacity evidence.

Analysis tests keep all10 identities,100partitions and20one-character diagnostics. A failing
candidate cannot be rescued by a successful control. Recorded gradient-enabled call counts,
policy tags,fit traces and replay-policy mismatches are checked. All45 bad parent hashes fail
before verifier dispatch. Parent diagnostic schema/count checks and actual precheck760/1429
temporary-file coverage reject missing helpers. Actual run-path tests use substituted train/replay
functions to verify10fits before10replays,one child checkpoint-bundle load and policy-tagged
serialization. Persisted roundtrip,byte tampering,semantic tampering after descriptor resealing,
no overwrite,wrong bundle order and invalid training-length tables are tested.

Semantic suite tests construct5198 IDs and retain the exact5197 after the one inherited exclusion;
they do NOT run the actual inherited regression suite. CLI45args/context bindings,UTF8 reads,
all45 launcher paths and embedded postcheck indices[2:47]/head47/argc48 are checked.

## Local limitations

The local C304 support file contains3276bytes of exact fetched function/class-forward slices;
C315 support contains5982bytes of exact fetched function slices. They are NOT complete parent
modules or a full repository clone,and are NOT committed. User-checkout tests extract these ASTs
from the full accepted files. Production uses normal imports of the full accepted modules.

Local scorer,factory,optimizer,pair inventory,Git and parent-artifact interfaces are substituted
where unavailable. Test17 exercises the real runtime_preflight function with an independent
reference-last implementation standing in for the C318 frozen probe;the user runtime invokes
actual C318.branch_probe. These distinctions are not hidden behind a claim of full integration.
No actual FOLD checkpoint inference,real scientific training,or full5197 regression ran here.

## Parent writer and deciding-path dependency audit

C318 run/verify source was reread at the immutable review ref and matches its pinned blob.
It writes four diagnostic artifacts,including fold-c318-branches-eval-v1,not a training dataset
or model bundle. C319 verifies45 hashes then calls exact C318.verify_artifacts with44 ancestors
and C318's scientific execution HEAD. The C318 summary seals every artifact descriptor. Child
checks diagnostic PASS and the exact native/mean-only/last-only original outcome table.
C318.load_parent on the44-path tail then provides verified canonical C316 data/prompts. C319
ignores inherited checkpoint states and predictions for initialization and training targets.

Sole direct science import is C318. Its real context supplies C317/C316 plus C315 plan/tables/
evaluator/replay,C304 model/span/scorer,C308 optimizer,C287 normalization,C312/C296 pairing and
C310 no-neural/backend. Every inherited754 source and1418 input is checked;actual repository-local
helpers and factory-language module must be pinned. OWN6 plus5 C318 parent files yields760/1429.
No deciding-path source waiver,new regression exclusion or accepted-file alteration.

The training hook keeps the selected local representation attached to autograd. It checks native
call1=mean/call2=last before replacing only call1 in last_only. It never mutates accepted source,
methods,globals or stored parameters. Returned tensors retain their graph after capture-dictionary
cleanup. Both native attentions still execute and .5 averaging is unchanged. The same child policy
wraps optimizer updates,final evaluation and C315 strict replay. Model-bundle identities include
fresh seed and arm;replay requires the saved readout_policy to equal the arm. Full/core weights
must change during learning,then remain fixed during evaluation. No post-training policy swap.

## Scientific and execution boundaries

Fresh5pairedseeds,10models,1200updates/model;only readout policy differs within a pair. Both use
original2/3/4 training100exposures/row/length,not the one-character mixture. Initial weights/order
match,not necessarily initial logits or losses. Stored parameters14256/core3328/64slots,coreLR
.0005/noncore.005 and all optimizer settings fixed. Same repeated benchmark is not fresh-task
validation. The total memory coefficient1 is preserved,not vector norm or functional flexibility.
Both attention calculations remain;no speed/memory-saving claim.

Science12000updates,576000training rows,14880forwards,852480row presentations,59520core calls,
10strict state loads and one10-state checkpoint bundle write/read. Operational probes,recursive
artifact verification and software tests are separate costs. Only discarded runtime probe copies
receive the fixed nonzero read.output setting to avoid a vacuous zero-head comparison;scientific
initial states remain untouched. User probe compares actual C318/native and child forward paths,
then checks backward/finite query gradients. No scientific evaluation result has been observed.

Mandatory user gates remain:45actual parent archives/protected Windows bytes,PowerShell ParseFile,
real paired factories and readout probes,own24/full5197regression,all10actual scientific fits and
strict replays. Dispatcher/selected-launcher/runner ParseFile chain and Validate-before-science/
publication remain intact. This review authorizes only the guarded launcher. Integrity failure
repairs SAME C319. Valid candidate six<5/5 is a valid negative;do not tune seeds/gates after results.
C320 waits for formal judgment. C318 diagnostic PASS,old capability verdicts and Gate F stay distinct.
