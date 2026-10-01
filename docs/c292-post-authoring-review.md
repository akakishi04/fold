# C292 independent post-authoring review

post_authoring_review = PASS
Scope:committed-byte/static review plus local behavioral fixtures;not user-local science.
Review target:6e6bf264beaecb33cdfaa9c7ed7c2591b53d4a02.
Acceptance base:842e32a59bb5e3ef3f475554fb238c693139377e.

## Committed-byte match

After commit,all six OWN files were fetched from the immutable review target. Python source and
its test were read in consecutive ranges;other files were read in full. Returned whole-file Git
blob SHAs match independently hashed local bytes6/6:
- fold_lm/v05_benchmarks/model_c292_saved_answer_roles.py:715ef24d73bc023ac8ed6fd7363b32bc0321b708;19144 bytes.
- tests_lm/test_v05_c292_saved_answer_roles.py:477b6fbfff1ed1517dc6e278922d50e4f15c1b03;19673 bytes.
- tools/run_c292.ps1:66c0066bac6946ec9e99be015f6eb893b150c586;4686 bytes.
- tools/invoke_c292.ps1:0c153620fcefafc0cc0247436342cbfb66b3aefa;5238 bytes.
- docs/experiment-ledger-addendum-c292-preregistration.md:7e18074bb5f14a2e81c2e7d4c97c7ab5906300aa;6511 bytes.
- docs/v5b-saved-answer-roles-v0.1.md:c9c4ddaeb93f2dccdedcdbb9a54a860173c1cd4a;1148 bytes.

The remote acceptance-to-authoring comparison contains exactly these six additions. Accepted
sources/tests/logs/preregistrations and protected dispatchers have not changed. Activation must
preserve these six reviewed blobs. The C291 recovery test is now accepted and stays immutable.

## Verification actually executed after matching

python -m unittest tests_lm.test_v05_c292_saved_answer_roles -v
Normal local default:Ran32 in2.763s;OK.
Entire same suite under an io.text_encoding CP932-default emulation:Ran32 in2.796s;OK.
Linux/Python3.13.5/PyTorch2.10.0+cpu. This is not an actual Windows runtime.
All6 files UTF-8/no-NUL. Both Python files and all3 embedded Python blocks compile.
Symbol-table review found0 unresolved custom globals,allowing standard module __file__/__name__.
Manifest recomputation matches f45b635e637d043d7b5dfeb2c65abed847a0b7d47ae3dd0cb4f0ce6c7f4f2869.

Fixtures exercise the complete38880-row/90-partition/540-value-pair/540-profile-language analysis
on synthetic data with valid original domain structure. Tests cover every256 output class,query
and fact-order mapping,in-context versus absent value cases,collapse,pair coverage,exact prediction
changes within the same role,18 hash rejections before dispatch,and parent normal-total mismatch.
Other checks exercise full protection maps and a missing context-module rejection,semantic test
ID filtering,forbidden neural/state/save operations with restoration,run phase order,roundtrip,
no-overwrite,hash and semantic tampering,CLI indexing and compact receipts. CP932 checks read all
six actual files explicitly as UTF-8. AST checks reject implicit source/test read_text calls.

Some parent files,Git/scorers and suite members are fixtures. The actual parent archives are not
available in this review runtime;no real C292 findings are claimed. The full4317 inherited suite
has not been run here. Its actual loader/count/ID filtering remains mandatory on the user's PC.

## Parent semantics and direct dependency review

C291's writer stores frozen final logits under raw[task][split][profile][view] in the
fold-c291-answer-margin-eval-v1 archive. Its verifier reconstructs all original gates,loss histories,
matching and file identities. C292 calls that exact verifier with17 ancestor paths and C291's
accepted execution HEAD,after verifying18 summary hashes. No parent checkpoint is loaded into
a model;torch.load only reads saved numerical results. C292 blocks Module calls,load_state_dict
and torch.save under no_grad while reconstructing parent data and the new audit.

C267 dataset/render source was inspected:values are distinct integers0..3,target is48 plus the
value attached to the queried entity,fact order does not change that binding. C270 triple source
preserves these values and source IDs. C291's sealed data and parent verifier enforce the inherited
quad prompt/target contract. The source labels all256 classes without restricted decoding.
C292's direct repository import is C291. Its context returns C290/C289 and the inherited scorer
bundle. C282.context was inspected and returns a SimpleNamespace of repository modules,so vars(c)
and module-file coverage checks match the real object contract rather than only a test stand-in.
All592 inherited pins are retained and checked;context modules are additionally required to be
pinned,including C291 itself at4257586769ffd9e810fd41d5bc0debea86dd087f. Add6 OWN and9 parent
inputs to obtain598/1081. No accepted dependency or protection failure is waived.

## Review boundaries

Original gates,model weights,cohort,profiles and value splits are unchanged. All15 C291 models
remain,including failures. Counts are dependent observations,not independent extra trials.
Emitting an absent value does not prove memorization;emitting the other value does not prove a
specific attention failure. PASS means diagnostic integrity only. No C291 verdict or Gate F change.
Source/test contain no active-C hardcoding in accepted lifecycle tests;only the new launcher
resolves C292 in the authoritative Formal state. No historical regression test is weakened.

Runner Validate precedes Execute. All3 Python blocks compile;18 inputs;postcheck paths[2:20],
head[20],argc21. Launcher contains18 fixed ordered paths and returns before publish on Validate
failure. Existing dispatcher remains unchanged and must be parsed in the user command;it parses
the selected launcher and that launcher parses the runner.

Not executed here:PowerShell ParseFile on Windows,actual18 ancestor archives,the real4317-test
regression suite,and actual saved-output diagnosis. These remain mandatory Validate/Execute gates.
An integrity failure retries SAME C292. C293 stays unregistered until C292 is formally judged.
