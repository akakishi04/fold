# C321 post-authoring review

post_authoring_review = PASS
Scope: committed-byte/static review and executed local software controls,NOT real FOLD science.
Review target:672a96440ec779d7f440685bb0c856da0e7e41c5.
Acceptance base:8785a88b70a14a4b8d632ff520a03977eb73f129.

## Committed-byte identity

All6 OWN files were refetched from the immutable authoring commit. Source285lines and tests326lines
were reread in consecutive ranges,including the complete test tail;other4files fetched in full.
Returned Git blob identities were compared to independently computed local blob hashes,6/6:

- fold_lm/v05_benchmarks/model_c321_interior_name_order.py:6c55bedbfb0373ce809e3bd62a73260adaf65212;20657bytes.
- tests_lm/test_v05_c321_interior_name_order.py:5cec8df1901600a5a80e5a30ee33a5359a7bef4f;26363bytes.
- tools/run_c321.ps1:3e06070df3d0fb76b788b49b664c164fd02a2737;9095bytes.
- tools/invoke_c321.ps1:c5e5719f3d9db8bce4ff9ddd004d3a2d1d56f78a;8419bytes.
- docs/experiment-ledger-addendum-c321-preregistration.md:6d7d49cd06c28e81945eb7c56ffd0b07b2c4a17e;7770bytes.
- docs/v5b-interior-name-order-v0.1.md:9cd3d9ed2b06aee5281661048fe2908151645824;1078bytes.

Remote compare against acceptance shows exactly these6 additions,no accepted source/test/log/
preregistration/dispatcher modifications. Activation must preserve all6 reviewed OWN blobs.

## Actually executed AFTER all6 refetch matches

Normal:python -u -m unittest tests_lm.test_v05_c321_interior_name_order -v
Ran24 tests in11.511s;OK;process exit0.

Entire module imported and run under default-CP932 emulation through io.text_encoding:
Ran24 tests in10.902s;OK;process exit0. Patch covers import,setup,alltests and teardown;explicit
UTF8 remains UTF8. This is not complete Windows emulation. Both runs uninterrupted and full.
The logs were checked for exactly24distinct test IDs and OK in each mode. No omissions.
Pre-commit development failures/successes are not counted as post-authoring evidence.
Local runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No PowerShell executable available.
Terminal cleanup messages after OK did not change process exits.

All6 hashes rechecked after testing;UTF8/noNUL. Both Python files and all3 embedded runner Python
blocks compile. Recursive symtable/import-binding checks found0 unresolved global references
in the two new Python files after accounting for module bindings and Python builtins/globals.
Manifest self-hash813f7283535086c9b7ebd416da1fb1d50b5240ece9d58e364173b4cb4d433fea matches.
47launcher paths ordered C320..C274. Postcheckpaths=sys.argv[2:49],head=sys.argv[49],argc50.

## Scientific behavior and independent controls

Independent prompt parser checks names/values/query answers without using the model. Canonical
dataset and original1..6 prompt hashes match. For every entity/language/family,the two distinct
names have length4,equal first/last characters and equal character counters. No mutation/RNG use.
Each question pair keeps the same facts but changes queried entity and correct answer. All864
normal inputs distinct/disjoint from old inputs;vocabulary subset,max Japanese43bodybytes/45tokens.
Exact token bytes/BOS/EOS/padding and actual accepted C304 query span are checked for every view.

The actual accepted C304 forward/span/scorer-adapter functions,C315 evaluate/validate_raw/replay,
and C319 trained_readout/hook_snapshot functions execute in local tests using controlled encoder,
core and model components. Both trained policies run the actual child315forward pipeline and
restore original outputs exactly. Strict state/policy/frozen-mode violations are rejected.
The actual scorer adapter maps new family keys through old profile slots without copying or
altering tensors/rows. C270 is a controlled scorer in this local adapter test,not the real scorer.

All47hash failures are checked before parent dispatch. The actual child precheck validates
772/1455 temporary file fixtures and rejects a missing repository-local helper. Parent status,
artifact inventory,complete cohort,original flags and scope are checked. A failing primary is
not rescued by five comparator successes. Diagnostic validity is not substituted for capability.

Production run-path fixtures verify one C319 model-bundle read from summaries[1],ten inference
dispatches,and evaluation tensors only. No optimizer or trained-model archive. Persistence
roundtrip uses no-neural guards;byte tampering and semantic tampering with updated descriptors
are rejected. Existing run directories cannot be overwritten. Runtime preflight executes both
policy branches on controlled bilingual original/new inputs. Semantic suite tests exercise5246
unique loaded IDs,5245retained IDs and duplicate rejection,NOT actual inherited regression.

Local support files contain exact accepted function slices,NOT full parent modules/repository;
these supports were not committed. On the user's checkout,tests extract those functions from
full accepted source files. Synthetic models/scores/archives and substitute Git interfaces are
software-control evidence,not actual checkpoint competence or evidence that real5245tests pass.

## Source-level parent writer and deciding-path audit

C320 run/verify source was inspected:its five artifacts include unequal prompts and before/new/
after logits,not a dataset/model bundle. C321 first verifies47summary hashes then exact
C320.verify_artifacts(C320dir,46ancestors,C320executionHEAD). Require acceptedPASS and exact
C320 layout flags. Actual C320.load_parent on paths[1:] returns verified C319 dataset,original
prompts and final same-policy output anchors. C319's own load_bundle reads trained-models.pt
at summaries[1].parent;actual make_models uses original seed/context. Strict state/policy identity
checked per checkpoint. No C320 predictions used as weights,new teacher data or newly inferred outputs.

C319 context/readout policy,C315 evaluator and C304 forward/span/profile scorer adapter were
inspected at immutable accepted refs. Model policy wraps ALL old/new passes;last_only is not
silently replayed under mean_last. New evaluator uses same96row chunks/all256classes. Every old
view must reproduce C319<=1e-9 and exact argmax,with original2..6 gates unchanged. State/hook
checks cover each pass. New names,not model structure/readout,are the intervention.

Sole direct science import C320;C319 owner and inherited context supply all remaining helpers.
All766accepted source pins and1443inputs are checked,including local lazy/context/factory-language
module coverage. Add OWN6 plus6C320parentfiles ->772sources/1455inputs. No unpinned dependency
waiver,accepted file mutation or new exclusion. The original exact C204 exclusion stays fixed.

## Runtime,interpretation and stop boundary

10states*(144+27+144)=3150forwards,302400rows,12600core calls,10strict state loads,one C319bundle
read,training0,new checkpoints0. Six discarded smoke forwards and recursive checks/regression
are separate costs. Raw logits619315200bytes before metadata/serialization,not peak-RAM estimate.
Same states and template-based task,not fresh-seed replication. Equal input character counts do
not guarantee equal hidden span means because the learned encoder may encode context/order.
A PASS is finite new name-order capability,not arbitrary identity matching or Gate F completion.

Runner retains recovered C320 one-interpreter ordered-suite observation,unique direct UTF8 logs,
fatal handler,fixture-boundary messages,exact child exit decimal/hex and previous-log preservation.
No automatic retries or test splitting/exclusion. C320's original interruption cause remains
unconfirmed despite successful completion. This instrumentation is not an environmental fix.

Not executed here:47actual parent archives/Windows protected bytes,native PowerShell ParseFile,
actual full5245regression or inference on10actual C319 checkpoints. These remain mandatory local
Validate/Execute gates. Source/scorer/model integrity failure repairs SAME C321 without retuning.
Valid primary failure is ACCEPTED VALID NEGATIVE. C322 waits for formal judgment;Gate F unchanged.
