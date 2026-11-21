# C307 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review and executed local software tests,not authoritative Windows science.
Review target:b1394c51ad6a451c808eb16d57397595c1f30cb6.
Acceptance base:0012e1fb0d293cf2082c545c92ee2d7f5a6f8e01.

## Remote-byte verification

After the authoring commit,all six OWN files were fetched from that immutable commit. Source477
lines and test571 lines were read in consecutive ranges covering their complete contents;the
other four files were fetched in full. Returned whole-file Git blob identities match locally
hashed bytes6/6. This match was checked before either post-match test run below.

- fold_lm/v05_benchmarks/model_c307_core_freeze_replication.py:02cb0d743391ef1424b537159c824c5e2bc5209b;29689bytes.
- tests_lm/test_v05_c307_core_freeze_replication.py:eb40987445a083c1d08201af7c7fb386a2133afd;33875bytes.
- tools/run_c307.ps1:56493cf0b5f25e6719c55dac0f960a808be2c4d6;4765bytes.
- tools/invoke_c307.ps1:dc4c2f47197740da357a831235211618795fcc86;6707bytes.
- docs/experiment-ledger-addendum-c307-preregistration.md:aa534d6cee60f9ed5a23662a39fd5a12f2f5b0ee;8704bytes.
- docs/v5b-core-freeze-replication-v0.1.md:8655f8f9c4260ebfc19dd7b2bdcdafd1fec2ca64;1187bytes.

Remote acceptance-to-authoring comparison contains exactly those six additions. No accepted
source,test,preregistration,log or dispatcher changed. Activation must preserve these six blobs.

## Post-match checks actually executed

python -m unittest tests_lm.test_v05_c307_core_freeze_replication -v
Normal default:Ran32 tests in11.677s;OK.
Entire same suite with io.text_encoding default emulated as CP932:Ran32 in10.652s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Pre-commit results are not substituted.
Both Python files and all3 embedded runner Python blocks compile;all OWN files UTF-8/no-NUL.
Recursive symbol-table/global-import binding audit found0 unresolved globals.
Manifest self-hash matches9662b7d5763768a09c75c961dc8f8453c40506eadcbb44639bbd50f7dca2ab8b.
PowerShell is unavailable in this local runtime;the guarded Windows ParseFile chain remains mandatory.

The actual child fit executes1200 AdamW steps in both arms on small target-coded toy inputs.
The actual accepted C306 schedule/fit definitions are extracted into an isolated TEST namespace,
with only seed lists configured for the new cohort. They produce exactly the same all1200 CE
values,gradient-receiving counts/names,schedule tensors and final weights as the child for each
arm. This verifies software equivalence on controlled inputs,not real FOLD generalization.
The imported accepted parent module is never modified by the scientific path. The test-only
namespace does not alter parent files or bypass runtime source protection.

All5 schedules match the accepted scheduling algorithm;each TRAIN row receives100 exposures
at each length2/3/4 and each profile gets400 updates. Private-generator checks preserve global
RNG state. FIT_RNG612000 and SHUFFLE_OFFSET306000 are intentionally unchanged from C306.
A repeated frozen fit after disturbing external RNG reproduces losses. Optimizer instrumentation
finds one optimizer at step1200 with frozen core excluded. Frozen core stays unchanged;full core
changes. Configured trainable counts and actual receiving counts are tested separately.

Integration fixtures execute accepted C304 LengthReadout/span_mask/schedule_stats definitions
with substitute correctly sized backbone/core/reader components. The factory checks common
initial state,64-slot configs,14256 stored parameters,14256/10928 trainable counts and independent
parameter storage. The actual C306 first_batch_probe verifies initial logits/noncore preclip
parameter gradients agree,core gradients are absent in the frozen arm,and encoder signal remains.
The actual child train_one executes1200 training+108 evaluation calls and checks1308/67968/5232
accounting on a controlled toy model. Its four-core-calls accounting is a test stand-in,not a
measurement of the actual FOLD backend's core internals.

Other tests cover80 partitions/40 contrasts,new-cohort paired contingency,core/replay mismatch,
all33 hash failures BEFORE parent dispatch,wrong parent status/artifacts/data,and688/1281 maps
with a missing-helper rejection. The actual child run path performs all10 fit dispatches before
all10 replay dispatches and invokes its actual bundle serializer/loader once. It verifies JSON
roundtrip/no overwrite,byte tampering and semantic tampering even with updated output descriptors.
One failing new candidate remains a valid negative. No old success is added to the new gate.
Semantic suite fixtures build4846 unique IDs and retain4845 after the sole inherited C204
exclusion,also rejecting duplicate IDs. This is not execution of the actual inherited suite.

Local parent support consists of selected fetched C306/C304 definitions,not full byte-identical
parent modules or a repository clone. Only OWN6 are asserted byte-identical to remote. On the
user's checkout the test extracts those definitions from full accepted files. Parent archives,
Git,legacy scorer totals,actual replay callbacks and full-suite entries are substituted where
unavailable. No user-local training,evaluation or scientific performance is claimed from fixtures.
The CP932 test emulates Path decoding defaults only,not Windows itself.

## Scientific and parent semantic review

The child directly imports only C306. Its context returns C305 no-neural,C304 length helpers,
logical pair helper,C287 normalizer,C283 transfer helpers and the original core bundle. All
repository-local context/factory-language helpers and C304.PINNED must be protected. The child
retains all682 inherited sources/1267 inputs and adds OWN6 plus8 C306 summary/artifacts=688/1281.
No missing direct pin is waived. Compatible configure/first_batch_probe are reused from C306;
seed-sensitive parent make_models/fit/analyze are not called with new-cohort IDs or monkeypatched.

The actual C306 run/load_bundle/verify_artifacts writer path was inspected. Final raw evaluation
logits,1200-step losses/events and freeze/replay metadata are sealed in seven artifacts. Its
verifier returns(payload,metrics),unlike C305's single dict. C307 verifies33 ordered summary
hashes before dispatching the exact C306 verifier with32 ancestors and accepted execution HEAD.
Require its valid-negative status,exact10 original seed results,all_pairs_matched/all_replays
and candidate_gateFalse. Its summary hash seals every artifact descriptor. The new loader reads
only the already-verified C306 dataset/prompts for learning,rechecks both canonical hashes and
regenerates/validates prompts with C304. It does not read learned model states as initializers.

C304 evaluate(model,prompts,data,c),score_length(data,raw,c),and
replay_one(model,state,record,prompts,data,c) retain their accepted semantics. The child uses the
same full/masked scorer,not a simplified toy scorer in production. New schemas are
fold-c307-replication-models-v1 and fold-c307-replication-eval-v1;the child loader checks new IDs.
The model bundle schema intentionally omits the parent's redundant slots field;64slots remain
fixed in every model record and manifest. No parent loader is incorrectly dispatched on it.
Numeric reconstruction uses the parent's no-neural guard and reconstructs all scores from final
saved logits. Original C306 results are not repurposed as new candidate successes.

## Replication,workload and execution boundary

Only initialization/order seed pairs change versus C306. Both policies use ordinaryCE,1200steps,
lr.005,64slots,identical2/3/4 training data and exposure schedule with the same offsets. The core
remains in forward and backward-to-input calculation. Its weights freeze only in the candidate.
Fewer trainable weights/global clipping/backward work remain confounds of that whole policy.
No new hyperparameter,gain,loss,seed donor,additional length,checkpoint choice or best-of decoder.
Five fresh random pairs test seed-cohort sensitivity,not external replication or new task coverage.
C306 remains negative;C307 gets its own all-five gate. Do not repeat seed hunting until success.

10*1200=12000updates;576000 training rows;10*(1200+108+108)=14160 forwards;
783360 total rows;56640 core calls;10 strict state loads;one model bundle write/read;network0.
Operational probes and recursive parent verification are separate. Primary all5 new core_frozen
five-character gates at unchanged accuracy.90/query_pair.80/evidence_drop.35/query_drop.35/
two_order.80. Show full control results and paired wins/losses. No automatic Gate F promotion.

Runner3 embedded blocks compile;33 fixed paths;postcheck slice[2:35],HEAD[35],argc36. Launcher
Validate failure returns before science/log publication. Preserve dispatcher/selected-launcher/
runner ParseFile chain. Own32/modules192/loaded4846/focused4845;sole C204 exclusion unchanged.

Not executed here:Windows PowerShell ParseFile,33 actual parent archives/Windows protected
bytes,the full4845 inherited tests,and10 actual FOLD model fits/evaluations/replays. These are
mandatory local Validate/Execute gates. Review authorizes only the guarded launcher,not a
scientific result. Integrity failure repairs SAME C307;C308 waits for C307 formal judgment.
