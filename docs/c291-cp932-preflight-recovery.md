# C291 operational preflight recovery — explicit UTF-8 test reads

## Formal disposition

C291 remains ACTIVE / NOT YET JUDGED. Retry SAME C291.
This was an operational authoring-preflight failure,not a completed scientific execution.
C290 remains ACCEPTED PASS (diagnostic integrity only). C292 NOT REGISTERED. Gate F NOT PASSED.
Failed invocation HEAD:57ef469ed23950f37eb17f788f582bf1a35eb3f1.
Recovery code/review target:02ba39b039d6d85b04c5a536f1fc44b6058351c9.
The execution command must use the later branch HEAD that includes this review and handoff update.

## Failure evidence and cause

The user supplied the Windows own-test traceback:
UnicodeDecodeError: 'cp932' codec can't decode byte 0x94 in position 25: illegal multibyte sequence.
Ran40 tests;FAILED(errors=1);invocation_skipped=AUTHORING_RUNTIME_PREFLIGHT_FAILED;
detail=C291 own tests failed;experiment_executed=False;execution_log_publish_attempted=False.
The runner stopped in Validate before focused4285 and before the15-model scientific Execute.
Operational output belongs to runs/c291-preflight-last.log;no scientific latest log was published
by this skipped invocation. No new scientific result or failed capability measurement is inferred.

The failing test39 called Path.read_text() on the UTF-8 preregistration without an encoding.
Its title contains an em dash whose UTF-8 bytes fail the Japanese Windows CP932 default decoder.
The test also left its runner/launcher reads implicit;test40 left its Python-source read implicit.
The original test39 itself was executed locally with io.text_encoding's default emulated as CP932,
and reproduced the SAME byte0x94/position25 error. This is not corruption of the model or dataset.
The original Linux-only authoring review missed this locale dependency. Environment changes on the
user's machine are not the remedy;the repository-owned reads must specify their file encoding.

## Minimal recovery and scientific immutability

The code commit changes ONLY tests_lm/test_v05_c291_answer_margin.py.
Old test blob:63e2bfd2c3be8aa4811b91b868877913f45a6c90.
Repaired test blob:f9d14c3228bb0ab55c95f4998b7b9c293909be93;28159 bytes.
Four formerly implicit reads now use encoding="utf-8":runner,launcher,preregistration and source.
Test39 now performs its actual inventory checks under a scoped CP932-default emulation and verifies
that decoding the actual preregistration bytes as CP932 fails. Explicit UTF-8 reading must succeed.
Test40 checks the C291 source/test AST and rejects locale-dependent read_text calls.
The temporary emulation is restored on exit;no process-wide locale setting,errors="ignore",
replacement decoding,skipped test,threshold relaxation or UTF-8-mode workaround is introduced.

The40 test IDs are unchanged;AST comparison confirms tests01..38 are unchanged.
Scientific source,losses,models,parameters,seeds,optimizer,training schedule,evaluation data,
thresholds,runner,launcher and preregistration remain byte-identical to the failed invocation.
Own40/modules176/loaded4286/focused4285 and source592/protected1066/dependency-union67 are unchanged.
Manifest content and SHA256 remain:
99916916817da709aead967aaae85052dfb3b049b1bc3ed7356a94abb7781d12.
No accepted parent source/test/log,dispatcher or prior experiment is modified.

## Committed-byte review and actual verification

Recovery post-authoring review = PASS (committed-byte/static plus local behavioral tests).
The committed repaired test was fetched back at02ba39b039d6d85b04c5a536f1fc44b6058351c9.
Its whole-file Git blob matches the locally tested bytes. The remote commit diff confirms only
tests39/40 changed and only this test file differs from57ef469ed23950f37eb17f788f582bf1a35eb3f1.
The other five OWN files retain their previously fetched and independently verified Git blobs:
- source:4257586769ffd9e810fd41d5bc0debea86dd087f;
- runner:02ea9b07d85d4eba3c300ddd4cbde56c18f26d43;
- launcher:5b258e79c352f03cda57e2a8488b473470b1144c;
- preregistration:ef6488f7dcfeed36d98daf091f9fb5a353b03d19;
- design:5c1230253684ece2be44976e97e1adc73a03d2d3.

After remote-byte matching,the COMPLETE40-test module was rerun in both modes:
- normal local default:Ran40 in6.705s;OK;
- io.text_encoding default emulated as CP932 for the full suite:Ran40 in6.461s;OK.
Both Python files and all3 runner-embedded Python blocks compile;unresolved-global audit0;
manifest recomputation matches;all C291 source/test read_text calls explicitly use UTF-8.
The pre-fix actual test39 fails under the same emulation;the fixed tests39/40 pass.

Local runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. The full C291 test module includes its existing
small-model training fixtures and mocked parent artifacts/scorers. This is NOT Windows execution,
not the full4285 inherited regression suite,and not actual FOLD15-model science.
The CP932 exercise emulates default Path text decoding only,not an entire Windows environment.

## Current execution boundary

The earlier docs/c291-post-authoring-review.md remains a historical record for its original target.
This recovery review supersedes its test-blob approval;unchanged scientific-source review remains
applicable. Do not present the old test blob as current or claim original approval covered CP932.
Run the existing invoke_active_v2 dispatcher via explicit PowerShell7 with the new recovery HEAD.
Mandatory local Validate still checks parent data/source protection,real initial models/objectives,
own40 and focused4285. Only after its PASS may scientific Execute and publication begin.
Retain the dispatcher/launcher/runner ParseFile chain. Do not bypass or weaken any preflight.
If another integrity issue occurs,repair SAME C291. C292 stays unregistered;Gate F remains unchanged.
