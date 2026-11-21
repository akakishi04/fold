# C313 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review plus executed local software tests,NOT actual FOLD science.
Review target:f6ca577c8c4280032fc31462c42a89342c7d3cd8.
Acceptance base:0c4dfe291010f90d7b444c36fd49d3accf64158c.

## Committed-byte verification

All6 OWN files were fetched from the immutable authoring commit after commit. Source348lines and
test409lines were reread in complete consecutive ranges;the other4 files were fetched in full.
Returned Git blob identities match independently hashed local tested bytes6/6:

- fold_lm/v05_benchmarks/model_c313_frozen_six_transfer.py:bf514ad80f85140e81b834d00aceb3379f4bfd80;23417bytes.
- tests_lm/test_v05_c313_frozen_six_transfer.py:0bcb1d3cc1c0209639d7f7fdba3cbe35ee2a4238;26012bytes.
- tools/run_c313.ps1:07c576f25e99855580f78b444a99b90c8c584faf;4610bytes.
- tools/invoke_c313.ps1:0669d03c6439ca02a622ade312ab718a00fbadd6;7309bytes.
- docs/experiment-ledger-addendum-c313-preregistration.md:3f674d855fcf1caa7974b3314af7c4e56e07fddb;7206bytes.
- docs/v5b-frozen-six-transfer-v0.1.md:ba5330fdd0409eda524f234aaae4647e545ea555;1268bytes.

Remote acceptance-to-authoring comparison contains exactly these6 additions. No accepted source,
test,log,preregistration or dispatcher changed. Activation must preserve all6 reviewed blobs.

## Tests actually rerun after all6 matches

Normal:python -u -m unittest tests_lm.test_v05_c313_frozen_six_transfer -v
Ran32 tests in4.970s;OK,zero failures/errors.

Entire same module imported and executed under io.text_encoding default-CP932 emulation:
Ran32 tests in5.032s;OK,zero failures/errors. Patch covered import,setup,all tests and teardown;
only omitted encoding is mapped to cp932. Both were uninterrupted complete unittest runs.
These post-refetch runs,not pre-commit results,are the executed review evidence.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. PowerShell is not installed locally.

All6 files UTF-8/noNUL;both Python files and all3 embedded runner Python blocks compile.
Recursive symbol-table/import-binding audit:0 unresolved globals in the two new Python files.
Manifest self-hash:f6e02599e4704457781f1ac49272a0a8d50d9c40524d66d4bcfb173e1cf86cca.
Launcher39paths ordered C312..C274;postcheck paths=sys.argv[2:41],head[41],argc42. C313-only ACTIVE
check,Validate before Execute/publication,and dispatcher/launcher/runner ParseFile path retained.

## Software and scientific-path checks

The independent logical fixture matches the canonical dataset SHA;old2..5 rendered prompt bytes
match the accepted prompt SHA. Test30 executes accepted C304 render/name_map/prefix_tensor ASTs:
all old prompts match,and every new six input fits64slots with maximum61UTF8bytes/63encoded tokens.
All864 normal six inputs distinct and disjoint from old normal prompts;no new byte vocabulary.
Masked input semantics,BOS/EOS,padding,exact token bytes,and overflow rejection are exercised.

Independent small transition examples distinguish new error,recovery,both wrong,and same wrong.
All10 parent states/flags remain. Tests reject primary failure despite secondary5/5,allow the
registered primary to pass with a failing secondary,and keep all original five flags unchanged.
This is prospective six capability testing,not post-hoc relabeling of C312's balanced negative.

Actual infer_one executes old108/new27/old108 forwards on a controlled model,checks243 forwards,
23328 rows,972 core calls,strict parent fingerprint and original-output reconstruction. A model
that changes its own weights is rejected. Actual runtime_preflight is exercised with controlled
bilingual inputs and both arms. Production run-path tests verify one bundle load,ten inference
dispatches,evaluation-tensor save only,persisted reconstruction and overwrite prevention.
Byte tampering and semantic tampering even with a resealed descriptor are both rejected.
All39 hash failures are tested before parent verifier dispatch;actual precheck exercises724/1357
file fixtures and rejects a missing repository helper. Semantic suite tests construct5030 IDs,
retain5029 exact IDs and reject duplicates;this is NOT running the actual inherited suite.

Test31 executes accepted C304.score_length's actual profile adapter with a controlled scorer.
Local C304 support contains fetched exact function slices,not a full module or model clone,and is
NOT committed. On the user checkout the tests extract those functions from full accepted source.
Scorers,parent archives,Git and some backend interfaces are substituted in local fixtures where
unavailable. Synthetic success is software-control evidence,not real FOLD six-character ability.

## Parent writer,model and dependency audit

C312's writer stores frozen FINAL raw length/split/profile/view logits in
fold-c312-value-batches-eval-v1 and ordered checkpoint states in fold-c312-value-batches-models-v1.
C313 verifies39 summary hashes before exact C312.verify_artifacts with38 ancestors and accepted
scientific HEAD. The fixed C312 summary seals all7 artifact descriptors. It reconstructs C312
plans,optimizer/gain policies,original masked/local scores and replay invariants. Its outputs are
not guessed from C311's diagnostic schema. The child reads verified C312 dataset and old prompts.

Use actual C312.make_models/load_bundle then strict-load the correct ordered state exactly once.
No checkpoint splicing,trained scalar edits,new parameters,optimizer,training or seed selection.
Every state including balanced312002 is retained. All inherited source pins718 and inputs1343
remain checked;C312.PINNED,C304.PINNED and actual repository-local context/factory-language helper
coverage enforced. OWN6 plus8 parent files gives724/1357. No dependency waiver or accepted edit.

Actual C304 LengthReadout.forward and span_mask were inspected:64slots and query/EOS positions
are dynamic;the model path does not hard-code a five-character identifier limit. Only child
rendering permits6;the original class,weights and all core/reader computations remain untouched.
New evaluation uses the same chunk96 and all three views/profile/split layout. C304.score_length
has no identifier-length input and delegates the same original logical gates through its profile
adapter. It is reused rather than patching the old four-length cohort analyzer. Old2..5 before
and after must reproduce every archived view<=1e-9 and exact argmax,plus original per-state gates.
Full model fingerprint and hook registries are checked after every pass.

## Work and interpretation boundary

10saved states*(108+27+108)=2430 forwards,233280 row presentations,9720 core calls;10strict state
loads,one parent bundle read,training0,new checkpoint0,network0. Six bilingual operational smoke
forwards,recursive old-artifact verification and software tests are separate costs. Raw logit
payload477757440bytes excludes serialization overhead and is not peak-memory accounting.

Prospective primary:all5 retained random baseline states pass six local/masked gates. Balanced
states are fully reported but cannot substitute for a failed primary. Choice is fixed before six
results,not before earlier five results;therefore this is not independent model selection or a
fresh-seed test. Same templates/value split mean success is bounded length transfer,not arbitrary
names,arbitrary lengths or general model competence. C312 stays negative and Gate F NOT PASSED.

Not executed here:actual39 parent archives and Windows protected bytes,Windows PowerShell ParseFile,
the real5029 inherited regression tests,or inference on the ten actual C312 checkpoints. These
remain mandatory user-side Validate/Execute gates. This review authorizes only the guarded launcher.
Any integrity/reproduction failure repairs SAME C313;valid primary failure is a valid negative.
C314 remains unregistered until formal C313 judgment.
