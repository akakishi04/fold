# C343 independent post-authoring review

Date: 2026-11-02 Japan time.
**post_authoring_review = PASS**
Review target HEAD: `10a4cc6e69e52bfd657cd119b4c85f46cd14e761`.
Tree: `fec7ad0fa2494bad01a3350196d89ee36c6b3b81`.
Sole parent: C342 acceptance `50c277fff5242244dd82a87d392e543dc8c3594f`.
Manifest: `7e5de7e3040acd3d7aff1a748e8b7b97d36461badaa0c65c612b3f3a5e3c12d6`.

## Independent committed-byte review

A separate reviewer retrieved all seven files from the exact GitHub commit after
source/tests/launchers/preregistration were complete, read each through EOF and
independently computed UTF8 Git blob hashes from the complete remote responses.
Remote response, commit tree and actual local bytes agree. The source commit has
seven additions only. Accepted sources/tests/contracts/dispatchers remain unchanged.

|File|Bytes|Git blob|
|---|---:|---|
|fold_lm/v05_benchmarks/model_c343_saved_mixed_length_localization.py|35398|e9b8ee752422c93a29fefbb4b8ef0f48b5b776be|
|tools/c343_execution.py|27639|8ec24e0b5c10ee653a445209f7caf9961d5c872c|
|tests_lm/test_v05_c343_saved_mixed_length_localization.py|30944|c95c805f82f2c90b1c92e5df43ef2b04e05f4cfc|
|tests_lm/test_v05_c343_execution.py|28733|26bb4499fa004056b3f5b24ab4f504bc55b3f5b7|
|tools/run_c343.ps1|966|f436a1afa134744800fe003a048dbb0bbefa8f7b|
|tools/invoke_c343.ps1|3181|21133b227e6af146edc9faea61d1344149d5b7e9|
|docs/experiment-ledger-addendum-c343-preregistration.md|17110|ae6a92a614655f68800319e93087ca6c635b40ce|

No blocking discrepancy or source correction was found during this formal review.
The six source/test/launcher files had earlier local static checks; those were not
substituted for this separate committed-remote-byte review.

## Authoring evidence and precise scope

Combined64own tests passed normally in37.910s and with CP932-default text I/O
emulation in38.200s. Both have failures/errors/skips/expected failures/unexpected
successes all0. Explicit UTF8 and binary I/O remained unchanged in CP932 emulation.
Reports record acceptance HEAD50c277fff5242244dd82a87d392e543dc8c3594f: the tests ran
on the final sealed files before publication. Those exact bytes match the reviewed
commit. This is not described as a test rerun after the source commit.

Additional constituent checks: sealed science40PASS35.806s, infrastructure24PASS
1.708s normally/1.640s CP932. Author environment is Python3.12.14 / Torch2.10.0+cpu /
NumPy2.3.5. Native user runtime remains Python3.13.15 / Torch2.10.0+cu130 / NumPy2.3.5.

At the committed source HEAD, the four Python files passed UTF8/noNUL,compile,
import and pyflakes (0findings). Recursive bytecode audit covered277code objects,
1672LOAD_GLOBAL instructions and found0unbound globals. This checks global binding,
not a proof of all dynamic attributes/branches.

Actual loaders/build_plan produce6443tests before the sole inherited exclusion,
6442selected tests/237modules,own40+24. Parent6378IDs/235groups are an identical
ordered prefix. Full ordered-ID SHA:
`0581297af93ba5c06494f1e41627de8a2f574ee2ef62a46147225a55755ad7f5`.
Parent ID SHA:
`76dfa4fd2952bdffd80250e57880d58cda72e7f7c16402c1817fed39ff294460`.
Excluded exact inherited ID is
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
No additional skip/exclusion or mutable-current-state historical test was introduced.
The inventory audit loaded suites without executing the full native test bodies.

PowerShell7.5.4 actual Parser.ParseFile returned0errors for invoke_active_v2.ps1,
invoke_c343.ps1 and run_c343.ps1. These scripts were parsed, not launched.
CLI help and git diff --check passed. Source-string assertions target the actual
functions; numeric count contracts use constructed loaders/test IDs rather than
numeric literals found by inspect.getsource.

## Parent semantics and complete diagnostic accounting

The reviewer checked actual C342 writer schemas, its eight-field seed result and
13-field paired comparison, full preserved summary and trained-negative primary/
envelope. Exact parent execution/folder/primary/envelope pins match accepted C342.
The parent ABI is four arguments; child run/recheck five; report three. Canonical
data explicitly comes from the accepted C329 source via C330 helper context.

All114raw views/state and replay are checked; saved logits reconstruct scalar
measurements and local gate counts. All4320local/2160both-order cells,144strata and
30criterion summaries remain. The new normal path covers51840observations,
25920paired answers,12960query pairs,120support summaries and60transition summaries.
It binds raw/scalar/parent support and all30HOLDOUT answer/pair rescue/regression
counts, retains all4x4kind transitions and wrong-to-wrong prediction changes.
Non-symmetric matrix tests detect reversed control/candidate direction.

Query-pair identities include seed/domain/split/profile/language/entities/values/
fact-order and both queries. Query pairs, both-order gates, criterion transitions
and individual-answer transitions remain different units. Reporter publishes every
failed gate cell and all120/60normal summaries, verified against saved inventory.

Exposure counts are explicitly per logical TRAIN row across all profiles. They
are not repetitions of one literal prompt. original5 has4/5exposures0/100; mixed45
has50/50; original2/3=200each/interior4=100 in both. Original6 and HOLDOUT rows have
0actual presentations; masked views were never fitted. Child record copies replace
obsolete annotations without changing immutable helper global state or numeric gates.

C342 candidatefalse/eligible2 is preserved. No filter, repaired argmax, selected
checkpoint, new prompt, forward or fit enters the diagnostic. Complete accounting
can pass without establishing capability improvement, causation or Gate F.

## Protection, call ordering and launcher

Actual helper/context alias audit covered68repository files with0uncovered direct/
lazy dependencies. Twenty explicit bootstrap/fixed pins matched committed blobs;
immutable OWN/EXTRA and other pin declarations cover inherited helper paths.
Source923=916+7;inputs7693=7205+481+7. All481parent outputs include473regression proofs.
Finite leases explicitly allow7693 and require all7693final uncached rereads.
Future successor retains all483C343 outputs including477proofs.

The actual production sequence verifies immediate parent, executes full isolated
regression, runs child diagnosis/reconstruction under no_neural, rereads every
input, writes/report outputs and performs separate fresh verification. Failed
regression/reconstruction/verification cannot produce run_execution_valid=true.
Historical ancestor bytes/proofs remain protected without recursive science reruns.

Branch/clean tree/ExpectedHead/uniqueACTIVE/dependency/AST checks precede logging.
Stale invocation skips without science or publication. Standard user block parses
the dispatcher; dispatcher parses chosen launcher; launcher parses itself/runner.
C343 names,paths,CLI indices and terminal transition-count marker are correct.

## Limits and activation authorization

No native full6442regression,7693Windows leases or actual C342 archive diagnostic
was run in this author checkout. Scientific tests use canonical data,real scorers
and synthetic saved logits. Parent916source-map/7205input files are local to the
user and were not rehashed here. Full native protection relies on immutable
declarations plus accepted C342 fresh verification and C343 snapshot/recheck.

PASS authorizes a documentation-only activation containing this review and a
unique C343 ACTIVE handoff, with all seven reviewed files unchanged. Final user
command must use that activation HEAD, not this source-only HEAD. C343 remains
NOT YET JUDGED until its published native result is independently checked.
