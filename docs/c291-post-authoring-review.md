# C291 independent post-authoring review

post_authoring_review = PASS
Scope:committed-byte/static review plus local behavioral fixtures;NOT authoritative FOLD science.
Review target:cc76905645ab60a650389e15456057088def6006.
Acceptance base:8f3158ea7f61c87bf674794755c8c36ccb0b27fe.

## Remote-byte verification

After the authoring commit,all six OWN files were fetched from the immutable target commit and
reread. Their returned whole-file Git blob identities match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c291_answer_margin.py:4257586769ffd9e810fd41d5bc0debea86dd087f;28482 bytes.
- tests_lm/test_v05_c291_answer_margin.py:63e2bfd2c3be8aa4811b91b868877913f45a6c90;27003 bytes.
- tools/run_c291.ps1:02ea9b07d85d4eba3c300ddd4cbde56c18f26d43;4651 bytes.
- tools/invoke_c291.ps1:5b258e79c352f03cda57e2a8488b473470b1144c;5133 bytes.
- docs/experiment-ledger-addendum-c291-preregistration.md:ef6488f7dcfeed36d98daf091f9fb5a353b03d19;7637 bytes.
- docs/v5b-answer-margin-v0.1.md:5c1230253684ece2be44976e97e1adc73a03d2d3;1435 bytes.

Comparison from acceptance to authoring shows exactly these six additions;no accepted source,
test,preregistration,log,or dispatcher changed. Activation must preserve all six reviewed blobs.

## Post-match checks actually executed

After matching the remote blobs,the new test module was rerun locally:
python -m unittest tests_lm.test_v05_c291_answer_margin -v
Ran40 tests in11.563s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. This is not the Windows authoritative runtime.
Both Python files and all three runner-embedded Python blocks compile. UTF-8/no-NUL checks PASS.
Symbol-table global/import-binding audit:unresolved globals0.
Manifest self-hash matches99916916817da709aead967aaae85052dfb3b049b1bc3ed7356a94abb7781d12.

Fixtures execute the real C291 fit loop for800 AdamW updates on each of three small query-conditioned
toy models,then repeat the candidate for determinism. A separate train_one fixture performs800
training calls plus81 frozen evaluation calls and checks881/46176/3524 accounting. These are not
actual C278/FOLD models. Factory capacity/storage rejection tests use stand-ins.
Loss tests cover closed forms,exact CE values/gradients,an independent literal pair-sum reference,
per-row offsets,pair/class permutations,cross-answer compensation,third-class competitors,
finite differences away from ties,and deterministic finite tie gradients. Nonfinite,shape,labels
and unsupported arms fail closed. All-five gate fixture remains FAIL when one candidate misses.
All five actual C291 schedules are constructed from synthetic valid pairs;exposures are100/100.
Other fixtures cover17 hash rejections before parent dispatch,592/1066 map accounting,matching,
replay/workload rejection,15-record analysis,90 partitions/360 contrasts,run call ordering,
checkpoint schema,persisted reconstruction,hash tampering and semantic tampering.

## Scientific path and parent contract review

C291 imports C290 only. C290.context yields C289;C289.context yields C287 diagnostic,C284 evaluator,
C283 quad scorer,C282 TRAIN table builder,and the inherited core bundle. These exact parent paths
were read;C287.normalize_task and partition accept seed/arm as metadata without old identity gates.
C284 replay remains strict-state/fingerprint plus full-view logit tolerance1e-9 and exact argmax.
C290 is loaded as a diagnostic,never as a training-state bundle. Verify17 ordered summary hashes,
then call C290.verify_artifacts with16 ancestor paths and its accepted execution HEAD. The C290
summary and all three output descriptors are pinned from the published receipt. C289 input data
are read only after recursive parent reconstruction and checked against canonical data hashes.
The only new neural path is C291 training from fresh independent initial models. No parent source
monkeypatching is used in the scientific code. Tests mock parent inputs where user-local archives
are unavailable;these mocks are not evidence that real parent reconstruction already passed here.

Source592=586+OWN6;protected1066=1056+4 C290 inputs+OWN6. Dependency-union67 includes the C290
module and the inherited scorer/model/helper sources. Runtime checks require the exact parent
blob and union cardinality. No missing direct dependency is waived.

## Objective,runner and count review

Normal TRAIN lengths2/3 only;HOLDOUT/quad/ablated examples never enter optimization.
The supervised hardest-rival loss masks only the target class from255 alternatives. Labels and
rival identities are never model inputs. CE and old pair-sum remain concurrent anchors.
800 updates/arm;constant LR.005;coefficient.25;margin1. Gradient scales are NOT matched.
Candidate all-five quad gate and all original masked criteria remain fixed. No threshold tuning.
All three penalties are computed from one model forward;only the registered total is differentiated.
Work14430 forwards/809280 presentations/57720 core calls matches15*(800+81+81) and4 core calls/forward.

Own40,module176,loaded4286,focused4285. The semantic suite-filter fixture checks actual test ID
sets;the real inherited suite must still be constructed/executed on Windows. Sole existing C204
exact exclusion retained. No inspect.getsource numeric-count assertion is introduced.
Runner has three Python blocks;postcheck paths=sys.argv[2:19],head=sys.argv[19],argc20.
Launcher has17 fixed ordered summary paths. Validate precedes Execute;Validate failure returns
before scientific log publication. The existing invoke_active_v2 dispatcher was re-fetched:
Git blob e3923b6224959b442afefa02fafa967e2e6d462e. It resolves the unique ACTIVE token and parses the
selected launcher;the child parses its runner. The user block must parse the dispatcher too.

## Mandatory authoritative runtime boundary

Not executed here:Windows PowerShell ParseFile,real local parent artifacts and Windows protected
byte hashes,the full4285 regression suite,actual FOLD15-model training and final strict replay.
These remain mandatory Validate/Execute gates. PASS here authorizes the guarded launcher only,
not a scientific verdict. Invalid execution retries SAME C291 without altered conditions.
C292 remains unregistered until C291 formal judgment. Gate F NOT PASSED.
