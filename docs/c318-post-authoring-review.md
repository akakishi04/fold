# C318 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review plus executed local software controls,NOT actual FOLD science.
Review target:06375ef01097beef25cfe7438310b9f9676f52ac.
Acceptance base:300dcb6ed45411cec6e646f732cb95ed664cf683.

## Committed bytes and scope

After committing all6 OWN files,each was refetched from the immutable target. Source291lines and
tests346lines were read in full consecutive ranges;the other4 were read in full. Git blob IDs
match independently hashed local bytes6/6. Remote comparison shows precisely these6 additions:

- fold_lm/v05_benchmarks/model_c318_readout_branch_isolation.py:5d48dd2866b8e10a286cb5d3991e6f3ea24f952d;21184bytes.
- tests_lm/test_v05_c318_readout_branch_isolation.py:aa9ab231023f3fad0ab33c34b27c188064a54331;26320bytes.
- tools/run_c318.ps1:3f778fc211f9edc202b0de4dd06f43e4bc9b2eba;4619bytes.
- tools/invoke_c318.ps1:869f4e83256e6725be145ba49a83d6b26ab8395c;7800bytes.
- docs/experiment-ledger-addendum-c318-preregistration.md:7843a4c9ef5798a07b6359f00517ef567ccd742a;7292bytes.
- docs/v5b-readout-branch-isolation-v0.1.md:5f3f1a2c46ac61b9c20ff7a23c14f14c98b63a63;1110bytes.

No accepted source,test,preregistration,log or dispatcher was changed. Activation must retain OWN6.

## Actually executed after all6 refetch matches

To stay within the local per-call execution limit,the unchanged24-test module was executed in
two nonoverlapping partitions01..12 and13..24 under each default-encoding mode:

- Normal:12/12 PASS13.126s,then12/12 PASS10.245s.
- CP932-default emulation:12/12 PASS19.953s,then12/12 PASS24.274s.

Each completed process returned0 with zero failures/errors. Log test IDs were programmatically
checked:all24 distinct IDs exactly once in each mode. CP932 patch covers imports,setup,tests and
teardown;only omitted encodings map to cp932. Pre-commit incomplete/failed runs are not counted.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. No PowerShell executable available. CP932 default
emulation is not full Windows emulation. Terminal cleanup messages after OK did not change exits.
All6 local hashes were checked again after testing against the fetched remote IDs. UTF8/noNUL,
both Python files and3 embedded runner blocks compile. Recursive symtable/import-binding audit
finds0 unresolved global references after accounting for module bindings,builtins,module globals.
Manifest seal:757879ae36418ab5b3973a18ea80902aef081c3e41b4a463f03cc841c2c3e4ad.

## Scientific path and behavioral controls

The actual accepted C304 forward/span function ASTs execute in the tests with controlled encoder,
core and readout components. Actual C315 evaluate/validate_raw/replay_error functions are reused.
Independent single-attention numerical references for BOTH mean_only and last_only match the
instrumented accepted forward within1e-14. Reference uses one full memory contribution,not half
of it. Original pass-through is bit-identical;single-byte query controls unchanged. Bad native
query-input provenance fails. Eval/no-grad/frozen restrictions,existing hook coexistence,repeated
calls,no optimizer,empty probe and exception cleanup are exercised.

Actual child infer_one evaluates all4 modes on the controlled model:576forwards/55296rows/
2304core calls per state. Each pass has144forwards,288query projections,4896single-byte query
rows;original logits restored exactly. Changed strict-loaded states are rejected. Analysis checks
original flags,all raw domains,10states/30scored conditions/300partitions/60single records and
1280groups/92160paired rows. Both changed conditions may fail all gates without converting the
diagnostic's status into a capability judgment. Incomplete cohorts,false preservation and
reproduction drift are rejected. Existing C317 paired accounting and one-byte helpers are reused.

All44 expected hash failures are exercised before parent verification. The real precheck function
uses754/1418 temporary file fixtures and rejects an unpinned helper. Production run-path tests
invoke the child run and verify one checkpoint-bundle read from C316 at summaries[1],not C317 at
summaries[0],then ten inference dispatches. Only evaluation tensors are written,not a new model
checkpoint. Persistence roundtrip,byte tampering,semantic tampering with updated descriptors,
existing-directory rejection,scope errors and real child runtime_preflight path are exercised.
Synthetic suite IDs test5174 loaded ->5173 exact retained IDs and duplicate rejection;this does
NOT mean the real inherited5173 tests ran here. CLI tests exercise main and context/module binding.

Local parent support files contain exact accepted function/helper slices,NOT complete parent
modules or a repository checkout. These support files are NOT committed. Tests on the user's
checkout read the full accepted C304/C315 sources and import the full accepted C317 module.
Substitute models/scorers/parent archives/Git interfaces are software controls,not actual FOLD
competence or tests of the user's saved checkpoints. Canonical input hashes match originals.

## Parent writer,loader and implementation audit

C317 run/verify implementations were reread at the immutable review ref and match blob
7ef1736df78b5dd883a331c434f5f82f1eb8ab92. C317 writes four diagnostic artifacts including
fold-c317-endpoint-eval-v1,not a model bundle. C318 verifies44 ordered hashes then calls exact
C317.verify_artifacts with43 ancestors and C317's scientific HEAD. Parent source/input protection,
original output reconstruction and all local/masked gates remain enforced. After that,C317's
actual load_parent on the43-path tail provides verified C316 data/prompts/final-output anchors.
C318 obtains actual C316 module and its context from C317.context,loads the C316 bundle through
C316.load_bundle from summaries[1],and uses C316.make_models with the original seeds/context.
All original ten checkpoints stay;strict full-state fingerprints match the old final records.

Sole direct science import C317. C316 factory/loader,C315 evaluator/replayer,C304 span/scorer,
C287 normalizer,C310 no-neural and backend are already inherited protected sources. Every748
parent source and1407 input is checked;actual repository-local context/factory helpers must be
in the source map. Add OWN6 plus5 C317 parent files yields754sources/1418inputs. No source waiver.

Native C304 read.query call1 sees span mean,call2 sees last-byte local state. C318 checks both
native arguments on every call before changing exactly one. Mean-only duplicates mean into the
second call;last-only duplicates last into the first. Both native attention computations and .5
average remain,with the rest of the real parent forward unchanged. Observer capture has no target
labels. Total coefficient1 is preserved,but vector norm/covariance is not matched. This is not
an independent causal decomposition or a trained alternative. All modes verify state/hook cleanup.

## Work,command and stop boundary

10states*4modes*144=5760forwards;552960rows;23040core calls.10strict state loads,one model-bundle
read,training0,new model checkpoints0. Raw logits1132462080bytes before overhead,not peak-memory
accounting. Ten discarded operational forwards and recursive checks/regression costs separate.
Three scored modes plus one restoration control do not mean40independent learned models.
No speedup claim:both query projections and all upstream computations still execute.

44fixed launcher paths ordered C317..C274;postcheck paths[2:46],head[46],argc47. Runner owns24tests
and full5173regression. The unique C318 ACTIVE guard and Validate-before-science/publication remain.
Dispatcher itself,selected launcher and runner all use the established ParseFile chain. Native
PowerShell parsing was not run here. Activation edits only documentation,not any reviewed OWN.

Mandatory user gates NOT executed here:44actual parent archives and Windows protected bytes,
PowerShell ParseFile,real bilingual frozen model probes,full5173 inherited regression,and actual
all10checkpoint inference. These remain Validate/Execute gates. This review authorizes only the
guarded launcher. Any integrity failure repairs SAME C318,without outcome-driven changes.
C318 PASS is diagnostic integrity only;C317/C316/earlier verdicts and Gate F remain unchanged.
