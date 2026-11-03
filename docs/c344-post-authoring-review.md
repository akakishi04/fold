# C344 independent post-authoring review

Date: 2026-11-04 Japan time.
**post_authoring_review = PASS**
Review target HEAD: `d97d1286f47ee06745083aa5e146c2d9349db3dc`.
Tree: `eabee60fc0ebc56f767d7a93c1544b6d4e10b1e7`.
Sole parent: accepted-result base `345830ca6cd256abfb33d2d220db06e8f83e2859`.
Manifest: `a663ebb0b09671c6d277b5abec6d09604a49a194d5d61409a1a5bf5018785ad8`.

## Independent committed-byte review

A reviewer independent of the source/test authors retrieved all seven complete
files from the exact GitHub commit, read them through EOF and independently
recomputed their UTF8 Git blob hashes. Remote response, commit tree and local
bytes agree. The source commit has exactly seven additions. Accepted sources,
tests, contracts, logs and dispatchers are unchanged.

|File|Bytes|Git blob|
|---|---:|---|
|fold_lm/v05_benchmarks/model_c344_pair_max_training.py|42806|6261a0c267df027835093c7ce53958f8f0034186|
|tools/c344_execution.py|27582|3dbe61736df3a0855db1e37e3f24c6cbecd49f87|
|tests_lm/test_v05_c344_pair_max_training.py|43790|95238b223fc88e7436a7fa8253b1c4324fd60a11|
|tests_lm/test_v05_c344_execution.py|29413|69af274e0738e6fab08e7e6032a686061a3987bb|
|tools/run_c344.ps1|966|d479b15b6f5bf1ccb5bd8a99b45d181df1ca9f18|
|tools/invoke_c344.ps1|3150|dafe28b0befa4b9f2a7d65ab2665e0e0140cebd2|
|docs/experiment-ledger-addendum-c344-preregistration.md|18517|097826f7b303422b1d2c1f475804b1baf097e044|

No blocking discrepancy or source correction was found during this formal review.
Earlier local core reviews were not substituted for this committed-byte pass.

## Author software validation and actual inventory

Final combined72 own tests passed normally in91.885s and with CP932-default text
open emulation in92.115s. Failures/errors/skips/expected failures/unexpected successes
are all0. Explicit UTF8 and binary I/O were preserved in the emulation.
Reports identify acceptance HEAD345830ca6cd256abfb33d2d220db06e8f83e2859; these final
sealed local bytes were tested before local adoption of the source commit. All six
reported code/test/launcher SHA256 values match the complete remote files. This
is not represented as a test run begun after publication.

Constituent checks: science48 PASS89.524s; infra24 PASS2.822s normally/2.534s CP932.
The initial science author run found two test-contract mistakes: tuple-key banks
were passed to a state serializer that accepts only string keys, and a table
shape/cross-bank validator was incorrectly expected to verify canonical hashes.
Tests were corrected to use training_fingerprint and the actual cross-bank
boundary. The actual stream-tamper test remains. Core,manifest,cohort and scientific
gate did not change. Both final full72 runs include these corrections.

Author runtime: Python3.12.14 / Torch2.10.0+cpu / NumPy2.3.5. User native runtime
remains Python3.13.15 / Torch2.10.0+cu130 / NumPy2.3.5. No runtime replacement.
Four new Python files pass UTF8/noNUL,compile,import and pyflakes with0 findings.
Recursive compiled-code audit covers289 code objects and2029 LOAD_GLOBAL
instructions with0 unbound globals. This establishes global binding, not arbitrary
dynamic-attribute or branch correctness.

Actual production helpers/build_plan and all239 raw unittest loaders yield6515
tests before exclusion and6514 selected tests. Own modules contain48 science and
24 infrastructure tests. Parent6442 IDs/237 groups are an identical ordered prefix.
Full ordered-ID SHA256:
`c5d7db147680f739c62bbbc2f12be324c66ba16ea108dc04beb3071f56abaaa3`.
Parent ordered-ID SHA256:
`0581297af93ba5c06494f1e41627de8a2f574ee2ef62a46147225a55755ad7f5`.
Sole inherited excluded ID:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
No extra exclusions,skips or current-ACTIVE assertions were introduced in historical
tests. Count contracts use actual loaders/IDs,not numeric source-string literals.
Inventory construction does not execute the native6514 test bodies.

PowerShell7.5.4 actual Parser.ParseFile returned0 errors for invoke_active_v2.ps1,
invoke_c344.ps1 and run_c344.ps1,with864/494/142 tokens respectively. These were
parsed,not launched. CLI help/argument positions and git diff --check passed.
The standard block template also passed with99 tokens/0 errors. Its40-hex
ExpectedHead is replaced and reparsed once the activation HEAD is known.

## Scientific isolation and writer/reconstruction semantics

The control retains the ordinary full256 F.cross_entropy mean path. Candidate
uses the mean of torch.maximum over24 complete query pairs. Both arms compute
and report both losses; only the selected tensor is differentiated. Independent
logsumexp/softmax gradient references verify the value identity and ordinary
baseline,non-tie harder-query gradients,symmetric exact ties,non-compensation by
an easier query and continued competition from outside-catalog classes.

Canonical row identities,language/entities/values/fact order,distinct queries and
target counterparts are checked before optimizer creation and every forward.
The actual selected indices match the schedule's paired row order. Both arms use
the same immutable C342 mixed45 banks,allocator,cycle complement,events,targets,
family masks,length masks and actual token/target stream. All five actual fresh
schedules are checked. Per model2400 updates/115200 rows/3168000 nonpadding tokens.
Actual exposure per logical row is200/200/50/50/0/100 for original2/3/4/5/6/interior4.

Continuous core_slow optimizer and weight hashes agree across the1200/1201 boundary.
Two fixed small Torch fixtures exercise both2400-update paths; separate first-four
update optimizer references agree exactly. Detached checkpoints have independent
storage. A production orchestration test establishes all10 fits before20 evaluation/
replay passes. Discarded native preflight measures16forwards/64rows/8backwards/0updates.
Scientific WORK remains24000updates/27420forwards/1480320row presentations.

Saved raw logits reconstruct every native scalar gate and support/normal count.
All120 normal state/domain/split summaries and60 matched contrasts are present;
the existing C324 contrast writer accepts canonical TRAIN as well as HOLDOUT rows.
The writer key sets,normal support partition,zero/one/both-correct and collapse
arithmetic,answer/pair rescue-regression direction and per-row exposure fields
were checked against actual functions and non-symmetric fixtures.

The fixed gate requires all5 full candidates,every one of120 nonnegative gain
inequalities across60 contrasts,and4 separately strict aggregate interior endpoints.
Tests independently break every inequality and strict endpoint. Perfect-control
saturation and ties remain valid negatives. No support filter,selected subgroup,
seed omission,extra update or changed inference path enters the comparison.
Unchanged threshold scorers,full256 argmax,114 views/state,raw replay<=1e-9 and exact
argmax are mandatory. No-neural saved reconstruction binds output schemas,states,
traces,receipts,actual input streams,metrics and summary. It does not replay every
optimizer update. Loss histories allow finite nonnegative values; preflight must
be nontrivial. Valid numerical CE zero is not an artificial execution failure.

## Exact parent and dependency protection

Immediate parent is C343 diagnostic PASS with nested C342 negativefalse/eligible2.
The actual parent writer and verifier fields match the child adapter. Parent source
and executor blobs,execution HEAD,folder,primary,envelope and manifest match the
accepted C343 evidence. Child calls the C343 benchmark directly with five arguments
under no_neural. Calling its executor.parent_semantics alone would only check C342.
C344 preflight/training/recheck/report have5/6/4/2 arguments. previous()->C332 and
reference()->C342 preserve canonical C329 data via the C330 folder bridge.

Source930=923+7;input8183=7693+483+7. All483 parent outputs include477 proofs:
three regression records plus237 receipt/log pairs. The immediate parent6442 tests
are reconstructed from complete ordered IDs,PID topology and log markers. Every
inherited source and input remains bound. Finite leases explicitly permit8183
inputs and require all8183 uncached final rereads; no default4096 truncation or
unlocked fallback. A future successor must retain489 outputs,including481 proofs.

Source audit resolves65 actual helper/context/explicit-lazy files and a conservative
221-file import closure,which includes dormant older routes. Declaration gaps0.
Sixty-eight unique explicit pins (33 map entries/43 path-blob pairs with overlap)
match current committed bytes; conflicts0/mismatches0. Capsule source is explicitly
pinned by the C214 producer,while other inherited files are covered by OWN/EXTRA/
PARENT_OWN declarations. No new pin or accepted-file edit was needed. This is
source/declaration evidence,not a substitute for rehashing native artifact maps.

## Process ordering, launcher and activation boundary

Actual worker order is locks/snapshot,immediate parent reconstruction,discarded
native preflight,full isolated regression,training,evaluation/replay,saved
reconstruction,all final rereads,then a separate fresh verifier. Regression,
reconstruction or verification failure cannot yield run_execution_valid=true.
All old bytes/proofs remain protected without ancestor neural reruns.

Branch/clean tracked tree/ExpectedHead/uniqueACTIVE/dependency/AST guards precede
logging. Stale invocation skips without science or publication. Standard block
parses dispatcher;dispatcher parses selected launcher;launcher parses itself and
runner. Run prefix,CLI indices,native Python path,C344 log publication and complete
normal-result reporting are correct. C272 compatibility seal and legacy dispatchers
remain unchanged. No source/comment false match was used as proof of a code path.

No formal native6514 regression,8183 Windows leases or ten-model C344 scientific
run was performed in this author checkout. Tests explicitly distinguish canonical
helpers/native preflight from synthetic logits,small optimizer fixtures and mock
parent/OS collaborators. User-side parent artifacts were not copied here.

PASS authorizes only a separate documentation-only activation with this review,
pre-activation history and a unique C344 ACTIVE handoff. All seven reviewed files
must stay unchanged. The user's ExpectedHead is that later activation commit.
C344 remains NOT YET JUDGED until published native evidence is independently judged.
