# C282 committed-byte post-authoring review

Final review target:7f6432bb2d40bc7ec19561b561c1b9f0fd9db5f2.
Initial OWN6 commit:3cbb0f3ba3874f4ab1bb4ebbe396c441f83cbefa.
Acceptance base:d54a8d5a775949ccb54dae6ebc9e934c7579c8f5.
Result:PASS for committed-byte/static review and local fixture-based own32 execution.
Authoritative Windows runtime gate:PENDING. No C282 scientific training result exists yet.

## Committed identity

Compare acceptance->initial OWN6 reports exactly six added files,no accepted source/test edits.
Compare initial->final target reports only10 added runner lines:actual training-table construction,
real paired initial model construction and logical schedule checks in operational Validate.
All initial OWN6 files were fetched after commit;the final runner was fetched after its last commit.
The unchanged five blobs plus final runner match the local tested bytes exactly (6/6).

|file|Git blob|bytes|
|---|---|---:|
|fold_lm/v05_benchmarks/model_c282_mixed_length_training.py|fdf35a6c0c18e0c0da4b1f592cef73be156de481|25105|
|tests_lm/test_v05_c282_mixed_length_training.py|b16a6a59b7049be1a372ccf7fd08f775f02b6c1f|19317|
|tools/run_c282.ps1|5e941e6ecc888e489ddae8fbadc64b4e408e5cbc|5345|
|tools/invoke_c282.ps1|432a79a97e25a57ec3774109cb3b1e8bb28a05d8|4248|
|docs/experiment-ledger-addendum-c282-preregistration.md|56fb7113f31a498836f73d463a8acc0b2f451b36|7098|
|docs/v5b-mixed-length-training-v0.1.md|bda243604a786bb81f66faf3b5554f883fb6d33b|2056|

Manifest was calculated by executing manifest():
291ed152bec43b222e54851c5e4699776e220d60937a733599c37f617ed400de.
Only the assignment was sealed. The seal-shape and digest-equality checks are executed in tests
with valid,malformed and mismatched seals. Negative-test UNSEALED literals are intentional.

## Executed local checks and limits

Linux/Python3.13.5/PyTorch2.10.0+cpu. Final own32 run:Ran32 tests in3.802s;OK.
All32 passed after final committed-byte comparison. Both Python files and all three embedded
runner Python blocks compile. Recursive symbol-table checks find0 unresolved globals,allowing
normal module-injected __file__/__name__/__package__/__builtins__.

Behavioral tests cover actual800-step schedule selection and100/100 versus200/0 row exposures,
complete query pairs and epochs,paired logical batch equality,reproducibility,fresh seed identity,
TRAIN-only normal rendering,independent model storage/capacity checks,all-eight parent hashes,
parent loader dispatch,neural-call blocking,artifact sizes,source pin rejection,table hashes,
replay and record identities,candidate-versus-control gate semantics,and rejection of unseen-length
or Gate F claims. The suite test constructs3950 synthetic unique IDs and filters the exact C204 ID.
It does not claim that the real inherited3949-test suite ran locally.

The fit smoke test executes800 AdamW updates on a tiny bias-only test model to verify actual batch
length selection and update count. This is NOT the real C278 backbone and NOT C282 science.
The run/persistence roundtrip uses mocked parent archives,scorers,training and replay;it verifies
call ordering,all output files,serialization/reconstruction and refusal to overwrite an existing run.
The lifecycle test uses an ACTIVE-C282 handoff fixture. These fixtures do not replace native validation.

Native PowerShell is unavailable here;ParseFile was NOT executed locally. Real parent archives,
actual model construction/training tensors and full focused3949 remain required in user-local Validate.
Actual ten-model training/evaluation/checkpoint replay remains required in Execute.

## Parent contract, dispatch and dependency coverage

The sole direct repository import in child source is C281. C281.context()[0] is C280;
C280.context provides C278,C270,C269,C267,core,base,reader,factory,audit in the inherited order.
C281.verify_artifacts receives parent_dir,list of seven C280..C274 summaries,and accepted C281 HEAD.
Its source blob is explicitly checked against2e06703af5e187febc12dbf65f33e3a6a773e612.

Actual C278 MeanFinalDualReadout is used in BOTH arms,not C280 EvidenceOnlyDualReadout.
C267/C270 renderers receive normal TRAIN rows only. C267/C270 scorers and every evaluation split
remain unchanged. C280.replay_one is reused only for its model/state/raw_two/raw_triple contract;
it does not call the old C280 seed schedule or C280.analyze. The child owns its new schedule validation.

Deciding calls use inherited C281 verification,C280 replay,C278 readout,C269 span mask,C267 dataset/
counting/evaluation/scoring,C270 rendering/evaluation/scoring and inherited factory/base/core/reader/
audit helpers. These already-pinned paths are retained and rechecked;no new unpinned helper is used.
Source count532+6=538;protected count940+4 parent inputs+6 OWN=950;dependency-union58.
The58 is an inherited source-union cardinality,not58 newly imported modules.

## Changed variable and interpretation audit

Only TRAIN length coverage changes. Models,initial states,logical minibatches,optimizer,800 updates,
200 logical-row exposures,scorers and thresholds are fixed. Candidate alternates length by epoch;
profile=epoch%3. Exact length/profile matrices are [[268,268,264],[0,0,0]] versus
[[136,132,132],[132,136,132]]. Both total800 updates;candidate has100 complete epochs per length.

Candidate learns three-character TRAIN names. A candidate PASS is explicitly seen-length/held-out-
value-combination learning,NOT success on the original unseen-length extrapolation condition.
The control retains the two-character-only transfer condition. Gate F remains NOT PASSED.
No seed exclusion,training extension,checkpoint selection or threshold retuning is permitted.

## Runner and activation

Eight summary paths are C281,C280,C279,C278,C277,C276,C275,C274 in that order.
Postcheck argv is output_dir,8 summaries,ExpectedHead:indices1,[2:10],10;total argv length11.
Validate checks parent integrity,builds real training tables and initial paired models without
training/forwards,then executes own32 and the actual focused3949 suite before scientific logging.
Launcher parses runner,checks host/branch/tree/HEAD/unique ACTIVE C282,and publishes only C282.
Dispatcher parsing is required in the user command;selected launcher parsing remains in dispatcher.

Activation may change only handoff/review documentation and must retain all reviewed OWN6 blobs,
C272 compatibility seal,accepted evidence and protected dispatchers. No authoritative runtime PASS
is claimed until the user's actual Validate/Execute output is published and judged.
