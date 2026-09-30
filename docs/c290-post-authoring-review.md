# C290 committed-byte post-authoring review

Review target:9ad25da5fef6b8458f14a45a61e453ceea9551e8.
Acceptance base:4ffae6420500e0233c1b19df07f6f0cfac73c16d.
post_authoring_review=PASS (committed-byte/static plus local fixture own40).
Authoritative Windows runtime gate:PENDING.

## Mutation boundary and byte identities

GitHub compare shows exactly six added OWN files after acceptance. No accepted source,test,
preregistration,log or dispatcher was changed. After commit,all six files were fetched again;
source and test were read in consecutive complete ranges. Returned whole-file Git blob hashes
were compared with the complete UTF-8 bytes compiled and tested locally:6/6 match.

|file|Git blob|bytes|
|---|---|---:|
|fold_lm/v05_benchmarks/model_c290_saved_pair_margin_audit.py|43cbbd346f8d6f8b1b57bf9bc026a995ed52786d|19805|
|tests_lm/test_v05_c290_saved_pair_margin_audit.py|83721c4322578affa18b0b2798f1c605ac10d91d|20711|
|tools/run_c290.ps1|4f5eec6c246605576309c97c69785b297682e70d|4912|
|tools/invoke_c290.ps1|617d2627ac850326cd09ff4c84282e2bb60b123f|5042|
|docs/experiment-ledger-addendum-c290-preregistration.md|18dd05fc3c850b84f83c1b8f380600d5439a4dff|6571|
|docs/v5b-saved-pair-margin-audit-v0.1.md|d3042bf150a4ec8f6af6bb94b39baae06f410523|1513|

The final identity-matched test run completed40 tests in4.844s,OK,on Linux,
Python3.13.5,PyTorch2.10.0+cpu. Both Python modules and three embedded runner Python blocks
compile. No NUL bytes. Symbol-table audit found zero unresolved custom globals;Python-provided
__file__/__name__/__package__ are allowed bindings,not missing imports.
Manifest recomputation matches123a8805343a6c7704ff6042d83928d3069aa43fe79e213e2b5798811d35b6f3.

## Scientific and parent semantic review

C290 reads final saved normal logits,not a new inference or step400 checkpoint. The C289 writer
and verifier were checked at the accepted source blob. Exact C289 summary SHA commits all eight
artifact descriptors;its15 immutable ancestor summary hashes are obtained from the source-pinned
parent vector. All16 hashes are checked before dispatch to the exact C289 verifier,which reconstructs
old objectives,matching and all masked/full gates. Archive schema is fold-c289-early-pair-eval-v1.
Only its saved evaluation archive is deserialized;no training state is loaded into a model.

The pair margin computes(correct0+correct1)-(swapped0+swapped1),preserving the parent's arithmetic
association. A pre-commit authoring check added a cancellation-sensitive test for that association.
There were no post-commit source changes. Pair identities include language,entities,values and fact
order;query order/labels are verified. Counts/collapse must match the exact parent normal totals.
All3arms/all5seeds/all3tasks/all splits remain. Margin1 is descriptive,never a replacement gate.
Per-pair predictions distinguish a met margin with wrong answers and the reverse case. Comparisons
name both anchors and align identical examples rather than infer equal outputs from equal gate counts.

Module calls,load_state_dict and torch.save are blocked during the diagnostic path,with no_grad.
Output serialization preserves full local source/input maps and per-pair records. The compact console
receipt omits repeated large maps but includes artifact hashes/sizes,counts and summary hash;the full
local payload still undergoes exact reconstruction and hash checks. No old publisher is modified.

## Executed fixture checks and remaining gates

Executed checks include valid/malformed/mismatched seals;closed-form margin/CE,offset and pair-order
invariance;met margins with one/two wrong answers;correct pairs below margin;finite/shape/dtype/grad
rejections;complete pairing;19440-record analysis and parent-total mismatch detection;90 partitions;
60 paired comparisons/12960 pairs;rescue/regression directions;16 hash failures before dispatch;
forbidden operations and restoration;actual temporary source/input-map cardinalities586/1056 and
missing-parent-pin rejection;semantic4246-loaded/4245-filtered suite construction with synthetic
test IDs;CLI16-path ordering;run-precheck/analysis/persistence ordering;actual temporary output roundtrip,
no overwrite,and both hash and semantic tampering. The console receipt size check also executes.

Parent archives,Git and inherited scorers are mocked where required. The synthetic all-correct logits
are fixture inputs,not C289/C290 findings. No actual user-local C290 science was run by the reviewer.
Real C289 artifacts,real pair grouping/full analysis schema,all4245 inherited regression tests,
PowerShell ParseFile and actual saved-output reconstruction remain mandatory Windows runtime gates.
The two new PowerShell files are checked for phase/CLI/path ordering;PowerShell is unavailable in
this Linux review environment,so no successful parser execution is claimed here. The dispatcher,
selected launcher and runner are parsed on the user's explicit PowerShell7 invocation path.

## Activation constraint

Activation may add this review and update the authoritative handoff only. It must not change the
reviewed OWN6 or any accepted files. C291 remains unregistered. A C290 integrity failure retries
SAME C290;diagnostic PASS never revises C289's negative verdict or promotes Gate F.
