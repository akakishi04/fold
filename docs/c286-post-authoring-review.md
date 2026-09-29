# C286 committed-byte post-authoring review

Review target:041087eb0bfc4baf5c9816515659196d351c7345.
Acceptance base:100ac28eca9015269fd69104edf36645c4f1bf9a.
post_authoring_review=PASS (committed-byte/static plus local fixture own40).
Authoritative Windows runtime gate:PENDING.

## Remote identity and mutation boundary

GitHub compare reports exactly6 added OWN files after acceptance. No accepted source/test,
preregistration,protected dispatcher or published log was changed by authoring. All6 files were
fetched after commit;the complete source/test were inspected in successive ranges. Returned whole
Git blob identities were compared with the complete locally compiled/tested UTF-8 bytes:6/6 match.

|file|Git blob|bytes|
|---|---|---:|
|fold_lm/v05_benchmarks/model_c286_cosine_tail_stability.py|332452219fe1a0b5472abb4a64be2827e6751b9f|25776|
|tests_lm/test_v05_c286_cosine_tail_stability.py|1a897da1f6d0249abc6adac36acb0ce61c3396d3|25365|
|tools/run_c286.ps1|2aaf9885aca0615a36ce01c9aa621d4460d51d55|5348|
|tools/invoke_c286.ps1|c9cb6526ff4dc67f8a3f121ce9a599b7f99bd8b6|4643|
|docs/experiment-ledger-addendum-c286-preregistration.md|a0a7a4f769c0bd015e273a098dd60bdece117608|7104|
|docs/v5b-cosine-tail-stability-v0.1.md|f477eb75669d450e739e8fb50ab3738566c00b39|1943|

Manifest computed from manifest():3d0ecd3f4785967a88e8b84597d9615be79eb7e609c348bf2ca1cdead8cbe94e.
Only the MANIFEST_SHA assignment was sealed;no global sentinel replacement. Valid,malformed and
mismatched seal execution tests pass. No NUL bytes or unresolved Python global bindings were found.
Both Python files and all3 embedded runner Python blocks compile.

## Executed fixture checks

Environment:Linux,Python3.13.5,PyTorch2.10.0+cpu. Post-commit identity-matched own40 run:
Ran40 tests in4.715s;OK. The initial run also passed;no authoring recovery was needed.
Tests13/14 execute actual800-update fits on a256-bias toy model for EACH arm and instrument actual
AdamW.step learning rates. They check all800 values,common first400 losses/state fingerprint and
subsequent final-state divergence. This is not real FOLD training or a C286 scientific result.

Other checks execute complete paired schedules,per-row exposure,shape/seed/pair rejection,
independent initial storage/precision/capacity,train-freeze-evaluate ordering,all3 task summaries,
primary versus descriptive gates,LR-history tampering even after hash replacement,step400/loss
prefix mismatch,nonfinite/replay failures,all12 parent hashes and exact loader arguments,forbidden
neural/state/write calls,actual temporary source/input map cardinalities and missing-pin rejection,
run/checkpoint/replay/persistence ordering,no overwrite,output hash plus semantic tampering,
CLI ordering,repository guards and immutable OWN inventory.

The suite-filter test constructs a synthetic4086-test suite and verifies the exact inherited
excluded ID and4085 remaining IDs. It does NOT claim the full inherited4085-test suite ran here.
Relevant fixtures replace real parent archives,Git and inherited models/scorers. Test fixtures
restore thread count,deterministic setting and RNG state after execution.

## Scientific scope and LR indexing

Actual C278 all-token mean/final readout,14256 parameters,48-token context and mixed2/3 coverage
are unchanged. Both800-update schedules have identical logical pairs/profiles/lengths. First400
LR values are exactly.005. Candidate update401 begins cosine decay;update600 is.00275;update800
is.0005. Each LR is assigned before the optimizer update. Control is.005 for all800 updates.
The code records actual applied values and checks them against the sealed rule on reconstruction.
No hidden warmup,additional training/evaluation,checkpoint selection or quadruple optimization.
Step400 fingerprinting does not write an intermediate checkpoint or perform a model forward.
Both first400 losses and step400 model fingerprints must match across a pair before acceptance.

The four-character all-five gate is the primary absolute gate,as in C284. Two/three/all-task
scores and comparative superiority are reported separately. C285 does not prove an optimizer
cause;smaller late LR may also hurt. Neither result automatically promotes Gate F.

## Parent schema,helper dispatch and dependency coverage

C285 source blob383b4156351c601a26b1f58c2ccdea59206f8538 was rechecked. C285.context returns
C284 plus its inherited context;C284.context returns C283,C282 and context. C286.context binds
(parent,previous,transfer,training,c)=(C285,C284,C283,C282,context),tested by actual dispatch.
C285.verify_artifacts(parent_dir,eleven ancestor paths,accepted HEAD) returns a diagnostic report,
not models. It is invoked with neural calls,load_state_dict and torch.save blocked.

C284 source blobcc560842a4f2b4e9b0ba6ae9481c42e2f3bb1df1 and its evaluate/replay_one writer-side
contracts were rechecked. They use raw={two_char,triple,quad},final_sha256 and schema-independent
replay fields without C284 seed/arm gating. C286 uses these helpers but never C284.analyze.
C286.analyze validates new identities,fit plans,LR traces,prefix match and pass semantics.
C282.training_tables remains the normal TRAIN-only2/3 renderer. C283 supplies the quad dataset
and scoring adapter. Reachable C278/C269/C267,core,base,reader,factory and audit helpers remain
covered by inherited source/input maps. C286 directly imports only C285;OWN source adds one to
the inherited dependency-union:62. Source562=556+6;protected1001=991+4 parent inputs+6 OWN.

## Launcher and outstanding runtime gates

Twelve summaries ordered C285..C274. Main CLI uses nargs12. Postcheck uses output argv1,paths
argv[2:14],HEAD argv14 and total argv length15. All3 embedded Python blocks parse/compile.
Launcher verifies PowerShell7.3+,branch,tracked tree,ExpectedHead and unique C286 ACTIVE,then
parses the runner and runs Validate before Execute. Validate failures skip science/log publication.
Scientific execution failures publish evidence and remain SAME C286. No runtime guard is weakened.

No PowerShell executable is available here;native ParseFile is NOT claimed executed. The standard
user command must parse the dispatcher,and dispatcher/launcher must parse selected scripts.
Real Windows parent artifact verification,all562/1001 pins/inputs,real TRAIN tables/paired initial
models,full focused4085 and actual10-model science remain PENDING authoritative runtime gates.
Activation may add only review/handoff documentation,not change the reviewed OWN6 blobs.
