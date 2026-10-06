# C308 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review and executed local software tests,not authoritative FOLD science.
Review target:22bbc839cb24bab585573d3c4838875b43eaa431.
Acceptance base:49bf2b96faa9afcee97bbce3840e1164b498fcd8.

## Committed-byte verification

After committing,the six OWN files were fetched from the immutable review target and reread.
Source481lines and test470lines were read in consecutive ranges covering the complete files;
runner,launcher,preregistration and design were read in full. Each returned whole-file Git blob
was compared with independently hashed local bytes before the two post-match test runs below.
All6 match:
- fold_lm/v05_benchmarks/model_c308_core_learning_rate.py:f4e41f0d37b1aa5cbba536e5da984ab556eea2c5;31880bytes.
- tests_lm/test_v05_c308_core_learning_rate.py:87a673fbd1695d56853c45cc72c728e3753d1bb9;31961bytes.
- tools/run_c308.ps1:9a03e0be71be6d995cf113703e4d6edfdadd28bf;4698bytes.
- tools/invoke_c308.ps1:49c559a7b14bd9e0ad7fab96451274f67f52aace;6807bytes.
- docs/experiment-ledger-addendum-c308-preregistration.md:f2c22ba9e88d08a3402cb678a072ecd22cb4fdb0;8918bytes.
- docs/v5b-core-learning-rate-v0.1.md:2c74106c4a4cc38707dba4c91783023781757ee5;1305bytes.

The remote acceptance-to-authoring diff contains exactly these6 additions. No accepted source,
test,preregistration,log or dispatcher changed. Activation must preserve all six reviewed blobs.

## Checks actually executed after all matches

python -m unittest tests_lm.test_v05_c308_core_learning_rate -v
Normal default:Ran32 tests in17.596s;OK.
Entire same suite with io.text_encoding default emulated as CP932:Ran32 in17.232s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. These are post-match runs.
All6 files UTF-8/no-NUL;both Python files and all3 embedded Python blocks compile.
Recursive symtable/import binding audit:0 unresolved global references.
Manifest self-hash:c13d8d4ed974f977840e7cc1d84d5d60e3bfc78bdbc9384ff1f5d4906f65210f.
PowerShell is unavailable here. Windows dispatcher/launcher/runner ParseFile remains mandatory.

The actual child fit loop performs1200 AdamW updates in each of three arms on a controlled toy
model. Full/frozen controls reproduce the extracted accepted C307 fit definitions exactly for
all1200 losses,gradient metadata and final weights. All5 schedules match the accepted algorithm
with the new seed lists in an isolated test namespace. No imported parent module is mutated.
An independently written candidate loop uses reversed optimizer-group order but original model
order for clipping;it reproduces all candidate losses and final weights. A repeated fit after
external RNG disturbance reproduces losses;one optimizer reaches step1200. This is software
control evidence on target-coded synthetic inputs,not FOLD generalization evidence.

Optimizer tests inspect disjoint parameter-group membership,core/noncore boundaries,constant LRs,
frozen exclusion and all trainable parameters covered exactly once. Invalid LR/group count and
wrong requires_grad policies are rejected. The actual first_batch_probe combines the accepted
C306 full/frozen gradient check with the new full/slow probe. Initial full/slow logits and all
preclip gradients match. One discarded step changes noncore parameters equally and core parameters
in the registered0.1ratio within1e-12. Original input models remain unchanged by the probe.
Candidate and full cores learn;frozen core does not. The probe does not assert later update ratios.

The real train_one function performs1200training+108evaluation calls on a toy model with actual
forward hooks measuring1308model calls,67968row presentations and5232toy core calls. These are
measured calls to the toy's four-core-call forward,not actual FOLD backend measurements.
Factory tests use a substitute LengthReadout and appropriately sized backend;they check matched
state,independent storage,64slots and14256/10928/14256 trainable counts. They do not execute the
actual C304 LengthReadout class in this review. C304 schedule_stats and C306 gradient-probe
function bodies are actual selected accepted definitions.

Other tests cover15results/120partitions/80contrasts,two paired-five contingencies,one candidate
failure retaining a negative gate,34 hash rejections BEFORE parent dispatch,wrong parent schema/
flags/data,694/1295 protection and missing-helper rejection. Production run tests use the actual
child run/bundle serializer/loader:all15 fit dispatches precede all15 replay dispatches,with one
bundle read. No-overwrite,JSON reconstruction,byte tamper and semantic tamper after descriptor
replacement are tested. Actual LR histories are validated,not inferred from requested settings.
Semantic suite fixtures construct4878unique IDs and retain4877 after the sole C204 exclusion,
including duplicate-ID rejection. This is not execution of the actual inherited4877-test suite.

Only OWN6 are byte-identical to remote. Local parent support is selected fetched C307 schedule/fit,
C306 first_batch_probe and C304 schedule_stats definitions,not full parent modules or a repo clone.
Parent archives,Git,legacy scorers and replay callbacks are substitutes where unavailable. CP932
emulation covers default Path text decoding,not the whole Windows environment. No user-local
scientific performance,actual FOLD training or full inherited-suite success is claimed here.

## Scientific and parent semantic review

The sole direct repository import is C307. Its context yields C306,C305 no-neural,C304 helpers,
pair builder,C287 normalizer,C283 transfer and backend. C307's actual writer/loader/verifier was
reread at the review ref:final frozen logits and1200-step traces are saved after training;
verify_artifacts returns(payload,metrics),reconstructs scores and checks source/artifact invariants.
C308 verifies34 ordered summary hashes before that exact verifier with33 ancestor paths and the
accepted execution HEAD. The summary seals all7 output descriptors;exact parent negative flags
and paired-five contingency are required. Only verified canonical dataset/prompts feed training.
No parent prediction is a new target and no learned checkpoint initializes a new model.

All688 inherited source pins and1281 inputs remain enforced,including actual context/core/factory
language modules and C304.PINNED. Add OWN6 plus8 parent files to obtain694/1295. C306's probe is
called through the actual returned context and is covered;no lazy helper pin is waived.

Only prospective optimizer policy differs across the three concurrent arms. Full/frozen preserve
one-group parameter ordering;slow uses noncore0.005/core0.0005 with disjoint groups. Global clipping
uses original model parameter order BEFORE optimizer.step. The code does not shrink core gradients
before AdamW,detach a path,modify the forward equation,add a gain or unfreeze adaptively. The frozen
arm retains input backward. Initial states/first CE/events match within each new seed.
Nominal LR ratios do not imply final update-size ratios after trajectories diverge. Freezing changes
trainable capacity/clipping/backward work. The chosen0.1ratio is not measured optimal or a causal
finding from C307. No new task-family or general-language capability claim follows.

## Workload and release boundary

15*1200=18000updates;864000training rows;15*(1200+108+108)=21240forwards;1175040total rows;
84960core calls. One15-state bundle write/read,15strict loads,network0. Operational probe copies
perform2 discarded updates outside science;no probe-trained state reaches the scientific run.
All original2/3/4/5 views and masked/local gates are reused. New candidate5/5 is not automatically
superiority if controls also succeed. All negative and control outcomes remain visible.

Runner contains3 compiled Python blocks;34 ordered parent paths;postcheck paths=sys.argv[2:36],
head=sys.argv[36],argc37. Validate failure returns before science/publication. Own32/modules193/
loaded4878/focused4877. Sole inherited exact C204 exclusion unchanged. The actual unchanged
invoke_active_v2 dispatcher was reread,blob e3923b6224959b442afefa02fafa967e2e6d462e;its parse
chain and legacy-pinned entry remain intact. No accepted operational entry is replaced.

Not executed here:Windows PowerShell ParseFile,all34 real parent archives/protected byte checks,
actual FOLD first-batch optimizer probes,the full4877regression suite,or15 actual FOLD fits and
strict replays. These remain mandatory local Validate/Execute gates. Review PASS authorizes the
guarded launcher only,not a scientific verdict. Integrity failure repairs SAME C308;valid all-five
miss is ACCEPTED VALID NEGATIVE. No after-result ratio/seed/budget/threshold retuning. C309 waits
for C308 formal judgment;C306/C307 negative verdicts and Gate F remain unchanged.
