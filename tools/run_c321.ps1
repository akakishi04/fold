param(
    [Parameter(Mandatory=$true)][ValidateCount(47,47)][string[]]$Summaries,
    [Parameter(Mandatory=$true)][string]$ExpectedHead,
    [Parameter(Mandatory=$true)][ValidateSet("Validate","Execute")][string]$Mode
)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Python = Join-Path $Root ".venv-py31315\Scripts\python.exe"
function Confirm-Repository {
    $branch = git branch --show-current
    if ($LASTEXITCODE -ne 0 -or $branch -ne "feat/sft-target-loss") { throw "Unexpected branch" }
    $head = git rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead) { throw "Unexpected HEAD" }
    $dirty = @(git status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0) { throw "Tracked tree must be clean" }
}
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw "Authoritative Python missing" }
Confirm-Repository
$EntryPoint = @'
from pathlib import Path
import faulthandler, os, runpy, sys, time, traceback

assert len(sys.argv) >= 2, "Expected Validate or Execute"
phase = sys.argv[1]
module = "fold_lm.v05_benchmarks.model_c321_interior_name_order"
if phase == "Validate":
    from fold_lm.v05_benchmarks import model_c321_interior_name_order as b
    paths = [Path(p) for p in sys.argv[2:]]
    assert len(paths) == 47
    b.runtime_preflight(paths, Path.cwd())
    print("source_and_artifact_precheck = PASS; source_pins = 772; protected_inputs = 1455", flush=True)
elif phase == "Execute":
    assert len(sys.argv) >= 4, "Expected diagnostic path and unchanged module arguments"
    diagnostic_path = Path(sys.argv[2])
    module_args = sys.argv[3:]
    original_stdout, original_stderr = sys.stdout, sys.stderr
    with diagnostic_path.open("x", encoding="utf-8", buffering=1) as diagnostic:
        class Tee:
            def __init__(self, original):
                self.original = original
            def write(self, text):
                diagnostic.write(text)
                diagnostic.flush()
                return self.original.write(text)
            def flush(self):
                diagnostic.flush()
                self.original.flush()
            def __getattr__(self, name):
                return getattr(self.original, name)

        started = time.monotonic()
        sys.stdout, sys.stderr = Tee(original_stdout), Tee(original_stderr)
        faulthandler.enable(file=diagnostic, all_threads=True)
        try:
            print(f"[C321 science] process_begin: pid={os.getpid()}; version={sys.version.split()[0]}; executable={sys.executable}", flush=True)
            print(f"[C321 science] module_begin: {module}", flush=True)
            # Execute the unchanged scientific module as __main__, as with -m.
            sys.argv = [module, *module_args]
            runpy.run_module(module, run_name="__main__", alter_sys=True)
            print(f"[C321 science] module_return: elapsed_seconds={time.monotonic()-started:.3f}", flush=True)
        except BaseException:
            # Record before propagating; never turn an exception into successful completion.
            print("[C321 science] python_exception: propagating original exception", file=sys.stderr, flush=True)
            traceback.print_exc(file=sys.stderr)
            sys.stderr.flush()
            raise
        finally:
            sys.stdout, sys.stderr = original_stdout, original_stderr
            # Keep the native handler off a file that is about to close.
            faulthandler.enable(file=original_stderr, all_threads=True)
else:
    raise ValueError("Unknown C321 driver phase")
'@
if ($Mode -eq "Validate") {
    Write-Output "=== C321 authoring preflight ==="
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c321_interior_name_order.py") (Join-Path $Root "tests_lm\test_v05_c321_interior_name_order.py")
    if ($LASTEXITCODE -ne 0) { throw "C321 syntax preflight failed" }
    & $Python -X faulthandler -u -c $EntryPoint Validate @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C321 parent/interior precheck failed" }
    & $Python -X faulthandler -u -m unittest tests_lm.test_v05_c321_interior_name_order -v
    if ($LASTEXITCODE -ne 0) { throw "C321 own tests failed" }
    $Regression = @'
from pathlib import Path
import faulthandler, os, sys, time, traceback, unittest

assert len(sys.argv) == 2, "Expected unique regression diagnostic log path"
with Path(sys.argv[1]).open("x", encoding="utf-8", buffering=1) as diagnostic:
    class Tee:
        def write(self, text):
            diagnostic.write(text)
            diagnostic.flush()
            return sys.stderr.write(text)
        def flush(self):
            diagnostic.flush()
            sys.stderr.flush()

    stream = Tee()
    started = time.monotonic()
    def mark(phase, detail):
        stream.write(f"[C321 regression {time.monotonic()-started:.3f}s] {phase}: {detail}\n")
        stream.flush()

    class ObservedSuite(unittest.TestSuite):
        # Delegate all original fixture semantics; only bracket lifecycle transitions.
        def _handleModuleFixture(self, test, result):
            name = test.__class__.__module__
            if name == getattr(getattr(result, "_previousTestClass", None), "__module__", None):
                return super()._handleModuleFixture(test, result)
            mark("module_setup_begin", name)
            super()._handleModuleFixture(test, result)
            mark("module_setup_return", name)
        def _handleClassSetUp(self, test, result):
            cls = test.__class__
            if cls == getattr(result, "_previousTestClass", None):
                return super()._handleClassSetUp(test, result)
            name = cls.__module__ + "." + cls.__qualname__
            mark("class_setup_begin", name)
            super()._handleClassSetUp(test, result)
            mark("class_setup_return", name)
        def _tearDownPreviousClass(self, test, result):
            previous = getattr(result, "_previousTestClass", None)
            if previous is None or previous == getattr(test, "__class__", None):
                return super()._tearDownPreviousClass(test, result)
            name = previous.__module__ + "." + previous.__qualname__
            mark("class_teardown_begin", name)
            super()._tearDownPreviousClass(test, result)
            mark("class_teardown_return", name)
        def _handleModuleTearDown(self, result):
            name = getattr(getattr(result, "_previousTestClass", None), "__module__", None)
            if name is None:
                return super()._handleModuleTearDown(result)
            mark("module_teardown_begin", name)
            super()._handleModuleTearDown(result)
            mark("module_teardown_return", name)

    faulthandler.enable(file=diagnostic, all_threads=True)
    try:
        mark("python", f"pid={os.getpid()}; version={sys.version.split()[0]}; executable={sys.executable}")
        mark("suite_import_begin", "model_c321_interior_name_order")
        from fold_lm.v05_benchmarks import model_c321_interior_name_order as b
        modules = b.regression_modules(Path.cwd())
        assert len(modules) == len(set(modules)) == b.manifest()["modules"]
        mark("suite_load_begin", f"modules={len(modules)}")
        suite = b.regression_suite(Path.cwd())
        assert suite.countTestCases() == b.manifest()["focused_tests"]
        ids = tuple(test.id() for test in b.flatten(suite))
        observed = ObservedSuite(b.flatten(suite))
        assert tuple(test.id() for test in b.flatten(observed)) == ids
        assert len(ids) == len(set(ids)) == b.manifest()["focused_tests"]
        del suite
        mark("suite_ready", f"expected_focused_tests={len(ids)}; ordered_ids_preserved=True")
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(observed)
        mark("suite_return", f"tests_run={result.testsRun}; failures={len(result.failures)}; errors={len(result.errors)}; successful={result.wasSuccessful()}")
        exit_code = 0 if result.wasSuccessful() else 1
    except BaseException:
        mark("python_exception", "propagating without converting to success")
        traceback.print_exc(file=stream)
        stream.flush()
        raise
    finally:
        faulthandler.enable(file=sys.stderr, all_threads=True)
sys.exit(exit_code)
'@
    $regressionLog = Join-Path $Root ("runs\c321-regression-" + [guid]::NewGuid().ToString("N") + ".log")
    Write-Output "regression_diagnostic_log = $regressionLog"
    & $Python -X faulthandler -u -c $Regression $regressionLog
    $regressionExit = $LASTEXITCODE
    $exitBits = [uint32]([int64]$regressionExit -band 4294967295L)
    $exitHex = "0x{0:X8}" -f $exitBits
    $exitReceipt = @(
        "regression_exit_decimal = $regressionExit"
        "regression_exit_hex = $exitHex"
        "regression_diagnostic_log = $regressionLog"
    )
    $exitReceipt | Add-Content -LiteralPath $regressionLog -Encoding UTF8
    $exitReceipt | ForEach-Object { Write-Output $_ }
    if ($regressionExit -ne 0) {
        Write-Output "=== Regression diagnostic tail ==="
        Get-Content -LiteralPath $regressionLog -Encoding UTF8 -Tail 35
        throw "C321 focused regression failed; exit=$regressionExit ($exitHex); diagnostic=$regressionLog"
    }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C321 frozen interior-name-order evaluation ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c321-v5b-interior-order-" + [guid]::NewGuid().ToString("N"))
    $scienceId = [guid]::NewGuid().ToString("N")
    $scienceLog = Join-Path $Root ("runs\c321-science-" + $scienceId + ".log")
    $scienceStderrLog = Join-Path $Root ("runs\c321-science-stderr-" + $scienceId + ".log")
    Write-Output "science_diagnostic_log = $scienceLog"
    Write-Output "science_stderr_log = $scienceStderrLog"
    if ((Test-Path -LiteralPath $scienceLog) -or (Test-Path -LiteralPath $scienceStderrLog)) { throw "Refusing to overwrite science diagnostic logs" }
    & $Python -X faulthandler -u -c $EntryPoint Execute $scienceLog --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead 2> $scienceStderrLog
    $scienceExit = $LASTEXITCODE
    $scienceExitBits = [uint32]([int64]$scienceExit -band 4294967295L)
    $scienceExitHex = "0x{0:X8}" -f $scienceExitBits
    $scienceReceipt = @(
        "science_exit_decimal = $scienceExit"
        "science_exit_hex = $scienceExitHex"
        "science_diagnostic_log = $scienceLog"
        "science_stderr_log = $scienceStderrLog"
    )
    $scienceReceipt | ForEach-Object { Write-Output $_ }
    $scienceReceipt | Add-Content -LiteralPath $scienceLog -Encoding UTF8
    if (Test-Path -LiteralPath $scienceStderrLog -PathType Leaf) {
        Write-Output "=== C321 native stderr tail ==="
        Get-Content -LiteralPath $scienceStderrLog -Encoding UTF8 -Tail 60
    }
    if ($scienceExit -ne 0) {
        Write-Output "=== C321 direct science diagnostic tail ==="
        Get-Content -LiteralPath $scienceLog -Encoding UTF8 -Tail 80
        throw "C321 scientific execution failed; exit=$scienceExit ($scienceExitHex); diagnostic=$scienceLog; stderr=$scienceStderrLog"
    }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c321_interior_name_order as b
out = Path(sys.argv[1])
paths = [Path(p) for p in sys.argv[2:49]]
head = sys.argv[49]
assert len(sys.argv) == 50 and len(paths) == 47
b.precheck(paths, Path.cwd())
p, metrics = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[2].c.audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
print("primary_arm =", s["primary_arm"], flush=True)
print("primary_gate =", s["primary_gate"], flush=True)
print("pass_counts =", json.dumps(s["pass_counts"], sort_keys=True), flush=True)
for name in ("seed_results", "final_partitions", "reproductions"):
    for row in s[name]:
        print("C321", name, json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("all_replays =", s["all_replays"], flush=True)
print("persisted_interior_order = PASS; train_steps = 0; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -X faulthandler -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C321 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C321 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
