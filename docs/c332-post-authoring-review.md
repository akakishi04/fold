# C332 post-authoring review

Review date:2026-10-19 Japan time.
post_authoring_review = PASS
Committed source/preregistration review target:
c2826b5d66db72b8d63c6f6cca2ef726e2e3b1a7.
Acceptance base:bb7a025db8eb32c9de76646fc13a223e933ca155.
This approves authoring,not native Windows/full5946 regression or the C332 scientific
outcome. Use the subsequent documentation-only final activation HEAD in the command.

## Complete committed-byte reread

All six committed files were fetched again at that exact source commit and read
through EOF. Benchmark ranges1..120,121..240,241..330,331..389;executor1..120,
121..230,231..330,331..408;tests1..100,101..195,196..280,281..360,361..440,
441..515,516..571;both complete PowerShell files;contract1..105,106..205.
The returned Git blobs match independently calculated hashes of the local raw bytes
used for the post-reread checks below:

|File|Git blob|
|---|---|
|fold_lm/v05_benchmarks/model_c332_trained_first_mean_query.py|25406e1e644d49041ece9daa8a467ec5a91c76f9|
|tools/c332_execution.py|b590cd71fab98cae8ba2388b23345dad5156d44d|
|tests_lm/test_v05_c332_trained_first_mean_query.py|9a2655ab0e4862be886c7106a351d7c8165bb560|
|tools/run_c332.ps1|a1a7cdb87e155acbb5234064d718185b71834ac9|
|tools/invoke_c332.ps1|40e93a805908a4b73dc7105b7200f8cfab93aae4|
|docs/experiment-ledger-addendum-c332-preregistration.md|dd86e2acc488267458c635386477c8eedfb4aaa6|

Remote comparison against acceptance confirms exactly these six additions and no
modified/deleted accepted source,test,contract,log,runner or dispatcher. C331
acceptance and C332 source registration are separate commits. This review and the
ACTIVE handoff are a later documentation-only change,not edits to the six files.

## Actual checks after the remote reread

Normal own suite:48/48 PASS;failures/errors/skips0;6.634seconds.
CP932-default-text-open emulation:48/48 PASS;failures/errors/skips0;7.016seconds.
Harness elapsed times were6.634861/7.016536seconds. Both builtins.open and io.open
supply CP932 only for unspecified text encoding;binary and explicit UTF8 opens are
unchanged. This is not a native Windows locale test.

All six files decode as UTF8 without NUL;all three Python files compile/import.
Recursive LOAD_GLOBAL inspection of233function/method/nested code objects found
zero undefined names. Actual own loader contains48unique test IDs;ordered ID SHA:
2e11011852d4ca29c9783932a20f9411ec401808a96eec7f4729c9b0270292a2.
Manifest self-hash verified:
2a216840891fcc13c98890d525a23054e074d88464cf546223dd693f4cb50874.
The accepted C331 benchmark used by numerical tests matches its exact blob
15fc732df683e421648545acfa3ea5e7a8f3ddfd.

Author environment:LinuxPython3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5,2Torch threads.
This is a targeted reconstructed source/test tree,not a full repository checkout.
No Windows/full5946 historical regression,actual C329/C331 artifact reconstruction,
actual ten-model FOLD training or native PowerShell AST execution is claimed. Legacy
factory/scorer/schedule,parent-proof,lease/runtime and historical-suite collaborators
are explicitly synthetic where the tests replace them. Native user checks remain
mandatory. No package installation or external compute was used.

Mutation control replaces first_mean by native_before in memory through the accepted
readout collaborator. Both test08(independent candidate update formula) and test09
(paired policies change final updates) fail assertions:2tests/2expected failures,
0errors/skips. These are expected mutant failures,not failures of the reviewed files.
All six source files and the accepted C331 benchmark retain their original hashes
after the mutation test;the manifest still validates.

## Training variable and numerical-path audit

The actual C304 LengthReadout.forward,C329 factory/optimizer loop,C326 schedule and
batch4 allocator,C325 training table loader,and accepted C331 readout hook were read.
The native mean/last query path and first_mean/last path differ only in the first
query-projection representation. C332 calls that SAME policy during fitting and
same-policy evaluation/replay. The last-byte branch,weights/capacity at initialization,
attention operations,core and residual path remain native. Coefficient.5 is fixed.
The first endpoint is a UTF8 byte,not a decoded Japanese character.

Both fresh models in each pair are constructed before either is trained. Their full
initial hashes agree and nonempty parameter storage is disjoint. No accepted trained
checkpoint initializes either arm. Each model gets2400updates,one unchanged C308
core_slow AdamW factory call,one FIT_RNG seed call,constant.005/.0005rates,ordinary
mean CE and global norm1 clipping. The exact1200schedule/mask repeats once. Model and
optimizer hashes are equal across the1200/1201boundary. All ten fits finish before
scientific evaluation;there is no checkpoint selection or intermediate evaluation.

Real Torch fixtures execute the production optimize loop with the exact accepted
C331 hooks. Native four-update final weights match an independent plain-forward/
CE/backward/clip/AdamW reference. Candidate four-update final weights match an
independent explicit first/mean representation formula and the same optimizer
arithmetic. The actual2400-update candidate toy run verifies one optimizer,the two
full event cycles,continuation hashes and2400gradient-enabled forwards. That fixture
has2rows/update and is not the native48-row FOLD workload. Gradient connectivity,
hook cleanup,nonfinite/rate/reset rejection and detached nonaliased final copies are
checked. No gradients are detached from the candidate representation during training.

TRAIN tensor/label/event/mask fingerprints detect mutation and must match within
pairs. The accepted C325 loader enforces original/interior target equality. New
schedules use332101..332105 and unchanged C326 allocation. Per-row exposure remains
200/200/100/100 for original2/3/4/interior4;original5/6 are not added to training.
Saved traces reconstruct policy,exposure,counts and hashes,not all historical
intermediate optimizer updates. This evidence limit is explicitly preregistered.

## Gate, saved writer and accounting

The new C332 primary gate requires all five candidate models to pass all existing
original2..6/interior local/masked/order gates. Each seed must have nonnegative
original6,pooled original2..5,and interior answer AND pair gains. Aggregate original6
answer AND pair gains must be strictly positive. Per-seed ties allow saturated
controls but never eliminate strict cohort improvement. This new preregistered gate
does not retrospectively relax C329 or change C331's negative intervention finding.
A complete scientific FAIL is valid negative evidence,not an execution error.

Production orchestration tests use synthetic scientific callbacks plus real safe
Torch/JSON writers to verify ten fits before twenty evaluation/replay passes and
all six registered outputs. Production analyze is exercised on the full10-record
cohort with explicitly synthetic trace/legacy scorers:20raw-validation calls and
5paired comparisons occur;changed paired initialization is rejected. Same-policy
state/hash/replay bindings and new archive schemas are preserved. Saved reconstruction
uses the actual new writer/loader paths and rejects changed result JSON.

Accounting:10training/10evaluation models,10final states,24000updates,1152000TRAIN
row presentations,27420forwards,1480320total rows,109680core forwards,54840query calls,
20state loads,one scientific bundle reload/write. Both evaluation and replay logits
are stored:672399360raw payload bytes,not336199680. Neither number is peak RAM or
total serialized size. Preflight/tests/parent and saved checks are separate work.
The discarded preflight uses both policies and both name families,English/Japanese,
6forwards/12rows/4backwards/0optimizer steps. Its source-only fixture is not a native
preflight result;the registered user run must execute the actual models/schedules.

## Parent loader and complete dependency inheritance

Immediate parent is accepted C331 diagnostic PASS with847sources/2051inputs,not an
older C330 schema or a scientific capability PASS. The exact summary/envelope,
manifest/work,full5898receipt,saved completion and2051final rereads are checked.
The accepted C331 snapshot reconstructs all inherited maps,including C330-R1.2 proofs.
Then C331's445supplementary files(3records+221JSON/log pairs),4science outputs,summary
and envelope add451mandatory parent files. With six own files the child has853sources
and2508inputs. No small-map fallback or missing accepted recovery test is allowed.

The real temporary-file fixture verifies all445proof-file hashes and rejects a
changed last module log. A production snapshot fixture constructs the complete
853/2508union using explicit synthetic accepted-parent callbacks;it is not the user's
real parent artifacts. Actual helper signatures are checked:parent snapshot receives
its five-part helper tuple,old plan and proof verification bind the old execution
HEAD,and immediate C331 semantic_recheck receives C331out,C329out,cx,C330seedflags,
read under no_neural. Older byte/proof reconstruction still occurs,not recursive
older scientific semantic bodies or parent neural inference.

All accepted C331/C330-R1.2/C329/C326/C325/C324/C308/factory/readout/scorer dependencies
stay pinned. Source input hashes and complete maps remain mandatory. Native unchanged
R4 read leases span phases;all2508inputs receive final uncached rereads. Six scientific
outputs are hash/size-bound before/after saved reconstruction and before final records.
A fresh process verifies all parent/source/input/output bytes,new module proofs and
saved trace/logit/gate reconstruction without refitting a second cohort.

## Regression bridge, launcher and approval boundary

Preserve the exact5898base test-ID digest and append the actual48-test loader:
5946tests/222modules,with only the inherited exact C204 mutable-ACTIVE exclusion.
New plan/guards/CLI belong to C332;ordinary test execution and PID/evidence validation
reuse accepted R1.2 helpers unchanged. Generic module-v2 receipts bind the NEW C332
HEAD/plan/index/module. Direct or immediate-child PID semantics are retained,not a
return to the incorrect equal-PID invariant. All planned tests must start and pass.

The222module collector/fresh-verifier fixture uses explicitly synthetic historical
IDs and receipt collaborators;444validator calls and tamper/fail-fast behavior are
checked. It is not execution of5946historical tests. Those real R1.2 process tests
remain in the inherited native suite. Production worker fixtures retain valid FAIL
results and prevent fitting after failed regression. Real Git/strict JSON/LF-CRLF/
exclusive-write/nonzero-subprocess tests exercise operational failure boundaries.

Both complete PowerShell files were read. active_v2 selects invoke_c332,which parses
itself and run_c332 before logging;the user command parses active_v2. The runner
uses .venv-py31315 and correct executor/root/folder/expected-head arguments. No native
PowerShell AST success is claimed on Linux. Local c332-trained-query and published
c332/latest.* names agree. No old command or publication HEAD bypass is authorized.

The final ACTIVE/review commit is documentation-only. Native preflight,all5946tests,
ten real fits,replays,2508final rereads and fresh verification remain mandatory.
INVALID repairs SAME C332;valid negative science does not trigger a retry. C333 stays
unregistered,Gate F stays NOT PASSED,and no production adoption,CI,paid service,
reinstall,artifact deletion or accepted-result mutation is authorized.
