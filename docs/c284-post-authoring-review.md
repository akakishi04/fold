# C284 committed-byte post-authoring review

Review target:19a678c1852977d22ae25a653b71bccd880d1aaa.
Acceptance base:255ad0ed293b5e6b29266f761c5e6b862a9fca37.
post_authoring_review=PASS (committed-byte/static plus local fixture own32).
Authoritative Windows runtime gate:PENDING.

## Remote identity and scope

GitHub compare shows exactly6 new OWN paths relative to acceptance;no accepted source/test,
protected dispatcher,prior log or scientific condition was edited. All6 committed files were
fetched after commit and compared with the locally compiled/tested bytes by complete Git blob SHA.
Result6/6 match. Python files were read in bounded consecutive ranges;the complete blob identities
match,not merely the displayed excerpts. No in-memory-only source was approved.

|file|Git blob|bytes|
|---|---|---:|
|fold_lm/v05_benchmarks/model_c284_max_length_matched_training.py|cc560842a4f2b4e9b0ba6ae9481c42e2f3bb1df1|26905|
|tests_lm/test_v05_c284_max_length_matched_training.py|6e97ed37a282749631f994fdbdfc4d96a1490cab|22115|
|tools/run_c284.ps1|be1005e1fd576ca48f32c47118ce2117308c8399|5400|
|tools/invoke_c284.ps1|0de71e862476da596c66a3a67e77e15f4e82daae|4443|
|docs/experiment-ledger-addendum-c284-preregistration.md|5bb2aff43084752e20c5f2e8d4d54914c5109a90|6950|
|docs/v5b-max-length-matched-training-v0.1.md|131ab0c72afc06dc32968b94747f180bf24cba9f|1765|

Manifest computed by executing manifest()/digest():
c835e2293c8a379b4173e4030cb687c0bb0bc549ef44298a0d8f8f39b2e6c080.
Only the MANIFEST_SHA assignment was sealed. Valid/malformed/mismatched seals are exercised through
validate_seal();no sentinel-wide string replacement was used.

## Executed reviewer checks

Environment:Linux,Python3.13.5,PyTorch2.10.0+cpu. After committed-byte identity comparison,
all32 own tests passed again:Ran32 tests in3.757s;OK. Both Python files and all3 embedded runner
Python blocks compile. Recursive symbol-table inspection finds0 unresolved global bindings.
All6 files are valid UTF-8 with no NUL bytes.

Behavioral checks cover exact paired batches/profile/exposure matrices,maximum length matching,
complete query-pair epochs,seed sensitivity,invalid pairs,independent initial state storage,
capacity errors,valid/bad seals,actual800-update toy-model fitting in BOTH arms,frozen evaluation
ordering,three-task dispatch,raw-logit drift,strict-state replay,all180 contrasts,primary versus
descriptive gates,parent hash dispatch and source pins,blocked neural calls/writes,synthetic suite
construction/exact exclusion,actual run-function ordering,output roundtrip,no overwrite,and output
hash/semantic tamper rejection. New tests use immutable preregistration/inventory,not ACTIVE state.

Parent archives,inherited model/scorer paths and Git context are mocked in relevant fixtures.
The toy fit verifies selection/update mechanics,not FOLD learning performance. The suite-filter test
constructs a synthetic4014-test suite;it does NOT execute the inherited4013 real tests.
No actual C284 scientific10-model training or real checkpoint evaluation was run by the reviewer.
No native PowerShell executable is available here;ParseFile is NOT claimed executed here.

## Parent and scientific path review

The directly imported repository module is C283. Its actual verify_artifacts signature is
(outdir,nine ancestor summaries,execution_HEAD). C284 passes the C283 directory,C282..C274 paths,
and24c4acd44905e1d3c4d2a019214eb588d72f9a93. All10 hashes are independently checked before dispatch;
all5 C283 artifact names/hashes/byte sizes and the C283 source blob are fixed. Parent reconstruction
blocks neural Module calls,load_state_dict and torch.save.

C283.context returns C282 and its underlying context. C284 uses C282.training_tables without its
seed-restricted model-construction helper. New284001..284005 models are made directly with the
pinned C278 class and factory,then independently deep-copied. C282 training tables use only normal
TRAIN renderings of lengths2/3. C284's own schedule selects three-only or alternating2/3 at identical
logical batches/800 updates. Four-character data is passed only to final frozen evaluation.
C267/C270 scorers and C283 quad adapter are unchanged. C284 owns its new task-keyed raw schema and
analysis;no C282/C283.analyze call receives C284 records. Replay checks every task/view/logit shape,
finite values,raw drift,argmax and unchanged state after strict loading.

Primary passed/candidate_gate means four-character gate only. Two/three/all-task flags are
separately reconstructed and descriptive. Candidate absolute PASS cannot be called superiority
without paired control evidence. The maximum trained length confound is removed,not all exposure/
curriculum confounds. Gate F and all prior verdicts are preserved.

Inherited source maps protect every reachable helper. Counts:544+6=550 source pins;
964+1 C283 summary+5 C283 artifacts+6 OWN=976 protected inputs;dependency-union60.
Workload arithmetic:10*(800+81+81)=9620 forwards;384000+2*77760=539520 rows;4*9620=38480 core calls.
One10-state bundle write/load and10 strict loads. Final raw payload159252480 bytes.

## Runner/activation boundary

CLI order is output_dir,ten summary paths,ExpectedHead at sys.argv[1],[2:12],[12];length13.
Launcher checks PowerShell host,branch,tracked tree,ExpectedHead and unique C284 ACTIVE,parses runner,
then Validate before Execute/log publication. Standard user block parses the protected v2 dispatcher.
Validate builds real TRAIN tables,checks maximum length/batches and real initial models,then runs
own32 and focused4013. Operational failure must skip scientific execution and publication.

Activation may update only handoff/review documentation,keeping the reviewed OWN6 and C272 legacy
compatibility seal intact. Full Windows parent reconstruction,PowerShell parsing,real initial model
construction,focused4013 and actual science remain required runtime gates.
