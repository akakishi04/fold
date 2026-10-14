# C324 R2 outcome / R3 bounded parent-validation observation

Date: 2026-10-15. Execution recovery, not a new scientific C.
C324 scientific execution remains INVALID at47ccd303f4382b7938db639e86aeb151e1f83af1.
C325 NOT REGISTERED. C323 and all earlier formal verdicts unchanged.
This document does not itself authorize execution; current handoff and post-authoring
review must authorize the final operational HEAD.

## R2 observed result

Diagnostic execution HEAD:7ca1ce4ae287e58a16d7e13da99fd03fb76ca89f.
Diagnostic publication:3de15c5b5850c732001f21b87658a5621faf7e68.
Published metadata:13208bytes, SHA256
1adbf28a1975172eceed6f2b97b57c504d5093164427f6b3dec361854ac11818.
Read both worker outcomes and terminal report from the immutable publication.
No reviewer-side whole-log hash recomputation is claimed. R3 rehashes the full local
published R2 log and checks its metadata/report before launching its child.

existing_cache:exit0,10.890s,completed=True,timed_out=False,stderr0bytes.
fresh_source_cache_path:exit0,28.854s,completed=True,timed_out=False,stderr0bytes.
Both:4096 parent_module calls,3 C324.context calls,source_matches_loaded=True,
0 model forwards,0 training updates,0 parent artifact verifications.
C242.parent_module loaded and freshly compiled code signature:
906d23d94088e8d5f69886f9d3208224e51dc0341ffa42fb4c0c43824addd8a6.
Source SHA256:f88cff429533266089dba137b1f5b9138aec9c9c608671f0745edad5a8bdf363.
Existing targeted pyc46793bytes,signature8dba7f65b58a08f339450e1a6563d701dd904f3e21123ca1c30f6131691e201f;
fresh lookup target did not exist. Existing pyc preserved,not deleted.
Runtime:CPython3.13.15,GIL enabled,Py_GIL_DISABLED0,torch2.10.0+cu130,numpy2.3.5;
reported selected environment overrides empty in both processes.

R2 diagnostic_completed=True and STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY confirmed.
This completes the bounded diagnostic. It does not accept scientific C324, prove
all disk caches healthy, rule out intermittent/native/runtime/hardware problems,
or show that the original50-parent workload no longer crashes. In particular,
the word cache in the fatal message does not establish an on-disk pyc diagnosis.

## R3 question and bounded work

Observe the ACTUAL C324.load_parent path rather than repeating the import-only test.
One child process,existing read-only cache lookup with-B,no new cache deletion.
The child has a180-second wall-time control limit INCLUDING its imports. This is a
termination policy,not a promised runtime or a claim that validation finishes.
Controller emits a10-second heartbeat. Exactly one child;no retry-until-success.

A sampler thread records the main thread stack nominally once per second to flushed
samples.jsonl. It reads code names/line numbers only,never frame locals. Stack depth
is capped160;external paths are reduced to basenames. The controller retains the
samples even on native crash/timeout and reports phase sample counts,nearest FOLD
frame,leaf frame and last stack. An incomplete final sample is explicitly flagged;
malformed complete samples are not silently accepted.

No sys.settrace/sys.setprofile/cProfile hooks and no changes to parent functions.
Sampling/thread scheduling and GIL availability can bias timing. Sample counts are
NOT exact function-call counts or unbiased CPU/wall-time percentages. A short
window does not represent the entire ancestor traversal.

## Actual dispatch and safety boundary

active v2 dispatcher -> invoke_c324.ps1 recovery registry ->
invoke_c324_parent_profile_r3.ps1 -> c324_parent_profile_r3.py -> one worker -> STOP.
Only recovery_action=PARENT_PROFILE_R3 authorizes this path. Existing R2 route is
retained. The normal scientific body and50 ordered paths in invoke_c324.ps1 remain
byte-for-byte unchanged. No normal C324 run is requested by R3.

Both controller guards require exact HEAD/branch/clean tracked tree and no changes
to fold_lm,fold_reasoning,tests_lm or tools/run_c324.ps1 relative to failed47ccd.
Parent paths are read from the registered launcher,validated as exact C323..C274
order,then the unchanged loader performs its existing parent hash/schema/semantic
checks. The R3 controller also validates the full R2 publication before starting.
C324.run/runtime_preflight/fit/make_models,torch Module calls and optimizer
construction are blocked in the worker;original no_neural guard is also entered.
Tensor archive reads needed by parent validation remain allowed. No new checkpoint
or scientific result is written. Sampling/results are local-only runs artifacts;
only the standard console text log is published.

No full regression in this diagnostic. No cached PASS,no relaxed threshold,no
validation bypass,no state adoption,no training or prediction-based selection.
The scientific manifest remains b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f;
full5357 regression remains required for any later scientific execution under its
then-reviewed execution contract. This operational tool does not alter those counts.

## Interpretation and next boundary

A timeout is an expected possible bounded observation,not an additional scientific
failure and not proof that the validator is wrong. Parent-validation completion,
worker exit,diagnostic completion,and scientific validity are distinct fields.
A completed parent check would still not prove the original native crash fixed.
Use observed hot frames to target equivalent batching/deduplication;do not infer a
measured speedup before implementing and comparing on fixed input snapshots.
All results end STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY. No C325,no scientific retry
until another explicit review/registration. No blind repetition of R2 or R3.

## Authoring tests

26 software tests:guards,R2 log identity/tamper,50 path ordering,persistence,
stack privacy/depth bounds,sampler lifecycle,partial log recovery,exact process
exit/timeout preservation,one-child controller,launcher boundaries,AST no-trace
contract,and real PyTorch subprocess fixtures (synthetic parent success and blocked
model forward). These do not execute the user's50 real parent archives.
Post-authoring review must reread all four committed executable/test files and match
their Git blobs to the tested local bytes before changing the authoritative route.
