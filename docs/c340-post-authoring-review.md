# C340 independent post-authoring review

Date: 2026-10-28 Japan time.
post_authoring_review = PASS
Reviewed source/preregistration HEAD d074f34ddd6256e05c39e85544a7a6bc07421c7f.
Parent f0ef770a98d8353b49d64df7cdbaa7bd6f7529b8 corrected only C339 acceptance
transcription/pooled reporting. C339's scientific verdict is unchanged.
This approves authoring,not native Windows/full6258/scientific PASS. Use the
subsequent documentation-only activation HEAD for execution.

## Independent remote-byte review

A reviewer distinct from both source authors fetched all7files again through the
GitHub connector at this exact HEAD,read through EOF and independently matched
their Git blobs to local tested bytes. Root separately fetched the remote Git commit
and verified whole-tree equality before post-publication tests. The source diff is
exactly7additions,no modified accepted source/test/contract/log/lock/dispatcher.
No review correction was required; the review target remains d074f34 throughout.

|File|Verified Git blob|
|---|---|
|fold_lm/v05_benchmarks/model_c340_length5_training.py|4837a70777445d8964aa3aa1274aa09356bec20d|
|tools/c340_execution.py|84c92a7225eaac526963dbe3b07439d25bf8dc48|
|tests_lm/test_v05_c340_length5_training.py|f6d78fcce1c7ac38f6d74ad0adc04046a0035bcf|
|tests_lm/test_v05_c340_execution.py|e42dabb158c42fb3f0b8ee4576d676c3baa268e7|
|tools/run_c340.ps1|664d7aba4cf18d81db6cf7faea669b72037930f7|
|tools/invoke_c340.ps1|bf1943204462390a8788b27ce4f5dcedca84c7e7|
|docs/experiment-ledger-addendum-c340-preregistration.md|cf6c51d2e9a9db30c86bc742268eb4d192bfe9c1|

## Executed checks after publication

- Combined own tests56/56 PASS,0failures/errors/skips,25.810seconds.
- CP932-default-text-open emulation56/56 PASS,0failures/errors/skips,20.111seconds.
  Both builtins.open/io.open use CP932 only for unspecified text encoding; explicit
  encodings and binary modes remain unchanged. This is not native Windows.
- All7files UTF8/noNUL;all4Python files compile/import;pyflakes0issues. Root's
  recursive231function/method/nested code-object audit finds0undefined LOAD_GLOBAL
  names. Independent reviewer also reports0undefined names(239code objects).
- Actual helpers/build_plan construct6258unique ordered tests/231modules with real
  32science+24execution own tests. Parent6202IDs retain SHA
  b5d92857cbb2c72d61a1e2a9af242f57e283fd7c26e5e6e86661d6cbdb35fbf4.
  Complete6258ordered-ID SHA:
  807b1fd8cbefff30b4d73e3f62b5a24170b014064e4e4a0a487800f8827ccd17.
  This constructs the full suite; it does NOT execute6258native tests.
- Recomputed manifest matches
  8016f388949a574a3609a563d1005c99b1c83455cd31148471f60a7c9b832914.
- PowerShell7.5.4 Linux Parser.ParseFile passes for invoke_active_v2.ps1,
  invoke_c340.ps1 and run_c340.ps1. This validates AST syntax,not native Windows
  paths/leases. User-side AST/preflight checks remain mandatory.
- git diff --check passes;the tested source commit has a clean tracked tree.

Author environment LinuxPython3.12.14/PyTorch2.10.0+cpu/NumPy2.3.5,2Torchthreads in
science tests. Registered native runtime remains Python3.13.15/PyTorch2.10.0+cu130/
NumPy2.3.5. No user environment reinstall.

## Scientific-variable review

Only candidate original-family slot4 normal TRAIN tokens change to canonical
original5,for all3profiles. Source IDs,targets,language and profile agree. Actual
C326.select_tokens/family masks leave interior4 unchanged even in shared slots.
Original2/3,logical data/events/masks,ordinary CE,native readout,optimizer,2400updates,
capacity and scorers stay fixed. C331 native_before leaves the query input unchanged.
Original6/HOLDOUT/masked prompts never enter fitting. Candidate original5 TRAIN is
now fitted;its HOLDOUT is a value-combination holdout,not an unseen template.

Tests use real canonical data/renderers/tokens including nonbinary values,exercise
all1200batches of the substitution boundary and all5schedule quotas. They reject
metadata/short/interior changes,missing profiles,bad dtypes,family leakage and token
fingerprint tampering. Actual native pairs have equal weights and independent
storage. Native preflight performs8forwards/16rows/4backwards/0updates. Independent
short fits match ordinaryCE,and a small Torch model checks2400updates/continuity.
These are software checks,not formal FOLD learning results.

Nonpadding presentations including BOS/EOS are measured in the loop and reconstructed:
3110400/control versus3225600/candidate per model. Extra115200tokens/model is explicit;
equal updates/padded64frames do not mean equal byte exposure. Logical fingerprints
match while actual token fingerprints differ. All10fits precede20evaluation/replays.

Real production scorers/raw-logit validators/query-pair grouping operate on synthetic
raw logits. C324 heldout_contrast preserves288answers/144pairs per domain/state;
replay_error checks<=1e-9drift AND exactargmax. Saved archives use actual loaders;
changed outputs/replay/state/cohort/nonfinite values are rejected. Synthetic full-
cohort tests replace trace checks,which are separately tested on actual tables and
toy2400updates. Simulated values are not reported as scientific evidence.

The fixed gate correctly requires all5candidate full gates,each seed's nonnegative
original6/pooled original2..5/interior4answer-and-pair gains,and strict aggregate
original6answer AND pair gains. Saturated ties remain valid negatives. Short-domain
pooling is explicit and does not guarantee zero individual-domain harm. Outside-
value partitions are descriptive,without an auxiliary loss or new support-error gate.

## Parent, protection and execution review

C339parent is diagnosticPASS with C338candidatefalse/eligible0,not trainedPASS.
Actual5argument dispatch:
C339.semantic_recheck(out339,source338,data329,validation_summary338,read).
The C338summary is a protected ancestor file and bound to accepted hashes through
the complete inherited snapshot. Parent reconstruction is under no_neural;older
C338semantic bodies are not rerun. Child saved-trained reconstruction separately
uses C340.semantic_recheck(out,data_out,cx,read),4arguments.

Accepted snapshot reconstructs895source/5769input maps;all467parent outputs including
461proofs are retained. Adding7OWN files produces902sources/6243inputs with no
collisions. Synthetic full-size union tests reject changed proofs/missing inputs.
Actual direct/lazy C338/C337/C332/C331/C330/C329/C328/C326/C325/C324 and lower
canonical helpers are in inherited OWN/source-pin coverage. Explicit parent Git
pins precede imports;no omitted deciding dependency was found.

Real worker/fresh-verifier control paths use explicit synthetic parent,OS leases
and scientific outputs. Accepted PID/log validators remain active. Tests reject
failed/partial regression,changed outputs and invalid capability flags. Finite
max_files6243 and ALL6243final uncached rereads precede final records;all6outputs
are hash/size-bound around reconstruction. Fresh verification checks maps/proofs/
saved metrics without independently replaying24000optimizer steps.

CLI/role/folder/ExpectedHead/module-index/plan arguments,manifest/counts,parent paths
and publication paths agree. No tests freeze current ACTIVE/branch tip. Actual loaders
verify counts,not source-string numeric literals. No inspect.getsource assertions
are present;launcher token/order assertions match actual files. Branch/tree/HEAD/
uniqueACTIVE/dependency/AST guards precede logging and publishing. The standard user
block parses active_v2;dispatcher parses launcher;launcher parses itself/runner.
The sole inherited exactC204exclusion is unchanged;no new skip/exclusion/test rewrite.

## Approval boundary

Independent review PASS;no unresolved blocker. Documentation-only activation may
set C340ACTIVE. The user must still execute native6258tests/231modules,10fresh fits,
evaluation/replays,6243rereads,fresh verification and log publication. C340 remains
NOT YET JUDGED until that evidence is reviewed. Integrity failure stays SAMEC340;
valid scientificFAIL is VALID NEGATIVE. C341 is not registered. Gate F completion,
production adoption and broad language capability remain unclaimed.
