# C324 R2 - native interpreter crash; diagnostic-only recovery

## Formal verdict and evidence

C324 INVALID EXECUTION / RETRY SAME C324. Not ACCEPTED VALID NEGATIVE.
C325 NOT REGISTERED; Gate F NOT PASSED. C323 acceptance is unchanged.
The previous R1 operational skip is distinct from this native scientific-process failure.

Failed scientific execution HEAD: 47ccd303f4382b7938db639e86aeb151e1f83af1.
Published failure log commit: 68397de27b4c538ddbd22dc2209fddb7afbc2409.
Published metadata: C324, log_bytes=976635,
log_sha256=8a5e28af87430010931afef2b2da3b61590f32930bee2967daff37c8db6a3271.
The metadata agrees with the user's publication receipt. The reviewer read the
published beginning and final sections; this is not an independent whole-log SHA256
recomputation. The exact Git blobs are preserved under
`docs/experiment-run-logs/c324/attempts/68397de27b4c538ddbd22dc2209fddb7afbc2409/`.

Observed in the published log:
- Initial 50-parent artifact verification: 8635.121 seconds (about 2h24m).
- R1 dependency/native-gradient preflight: PASS.
- Own64: PASS, 5.618 seconds.
- Full ordered regression: 5357 tests, 1074.995 seconds, zero failures/errors, exit0.
- Execute process enters parent_artifacts BEGIN a second time, then dies.
- Fatal Python error: _PyEval_EvalFrameDefault: Executing a cache.
- Frame: model_c242_balanced_recombination.py / parent_module, line ???, invalid frame.
- Exit -1073740791 / 0xC0000409; run_execution_valid=False.
No C324 training-phase marker or completed child result appears before the failure.
The source calls this parent precheck before any child fitting. No capability result
is available, and the full-regression success does not turn the scientific run valid.

## Cause boundary

The immediate failure is a CPython fatal evaluator error, not a Python ValueError
from R1 and not a PowerShell syntax failure. run_c324.ps1:138 merely reports the
nonzero child-process exit. Underlying corruption/trigger is NOT established.
The word CACHE here is a bytecode-interpreter diagnostic; it does not itself prove
that a disk .pyc cache is corrupt. Do not infer a specific Python bug, PyTorch bug,
GPU/RAM exhaustion or hardware fault from this log alone.
No Python/PyTorch reinstall, BIOS change, thread-count change or weakened validator
is authorized by this recovery.

## Authorized next action: NATIVE_DIAGNOSTIC_R2, NOT scientific retry

The same active dispatcher now routes the invalid-C324 recovery state to a bounded
import/bytecode diagnostic and returns before the scientific runner.
The diagnostic preserves the interpreter and scientific source, executes no
optimizer steps or model forward calls, and performs no parent archive verification.
It does not rerun the full5357 regression; it is not a replacement for that suite.

Exactly two fresh worker processes use the authoritative venv Python:
1. Existing cache lookup policy, with -B to suppress cache writes.
2. A new empty pycache_prefix plus -B, bypassing source-directory caches without
   deleting the original cache or writing new cache files.

Each records Python/build/GIL status and selected runtime settings, imports
PyTorch/NumPy, compares C242.parent_module's loaded code structure with a fresh
compilation of the exact source, calls that import-only function 4096 times,
and constructs the C324 import context three times. No model is constructed by
the probe. Model calls, optimizer construction, torch.load and the C324 scientific
entry/parent precheck are guarded against use. Targeted existing pyc bytes are copied
locally for evidence, never executed through marshal or deleted by the diagnostic.
Only the selected environment keys are printed, not a complete environment dump.

Both outcomes are collected even if one worker crashes. Native stdout/stderr and
exit codes are retained; each worker has a120-second hard bound and a10-second
heartbeat. These are control limits, not promised run duration or speedup figures.
No automatic retry-until-success, full training, cache deletion, library upgrade,
registry modification, remote dataset download or C325 registration occurs.

A successful short probe DOES NOT prove the full validator crash is fixed. If both
pass, report non-reproduction and use its runtime/code evidence for the next same-C
recovery. If existing-cache code differs but fresh code matches, report that measured
discrepancy without claiming it explains all native failures. Continue after reviewing
the complete diagnostic report, never by automatically returning to science.

## Source and transport boundary

The diagnostic controller rejects a changed branch/HEAD/tracked tree and any change
in fold_lm, fold_reasoning or tests_lm relative to the failed execution HEAD.
The scientific model, seeds324001..324005, schedules, thresholds, full suite5357,
792 source pins /1491 protected inputs and sealed scientific manifest remain unchanged.
The new scripts are operational diagnostic sources, not unpinned scientific helpers.
Their source blobs belong in the R2 review/diagnostic identity; no C324 science invokes them.

Normal dispatcher guards and ParseFile checks remain. The original50 parent paths
and normal scientific launcher body remain byte-identical after removing the new
recovery-routing block. Invalid recovery with an unknown action stops before logging.

The standard publisher transports the diagnostic under C324/latest.* with the
explicit execution_role=C324-R2-NATIVE-DIAGNOSTIC and scientific_execution_requested=False.
Here latest.json.execution_head identifies the diagnostic code, NOT a new scientific
execution. The failed scientific evidence is immutable in the attempt archive.
Do not classify a diagnostic publication/exit0 as a C324 scientific PASS or valid negative.
Local output lives in a fresh runs/c324-native-r2-* directory; no previous output is overwritten.

## External technical references (interpretation only)

Microsoft __fastfail documentation describes 0xC0000409 as non-continuable fail-fast;
it does not establish the underlying failure in this case.
https://learn.microsoft.com/en-us/cpp/intrinsics/fastfail
Python3.13 sys.pycache_prefix and command-line -B documentation describe the two
cache controls used by the diagnostic. They are not a claim that this failure is
necessarily disk-cache corruption.
https://docs.python.org/3.13/library/sys.html#sys.pycache_prefix
https://docs.python.org/3.13/using/cmdline.html#cmdoption-B

## Latency priority

The 8635.121-second observation replaces guesswork about the initial silent phase.
Do not impose another full pass merely to obtain runtime/cache evidence. Safe batched
source checks and equivalent ancestor-verification deduplication remain required
harness work before a future scientific retry/next C. No measured optimization is
claimed by this diagnostic-only change, and no historical checks are waived.
