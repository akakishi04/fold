param(
    [Parameter(Mandatory=$true)][ValidateCount(48,48)][string[]]$Summaries,
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
import faulthandler, runpy, sys, traceback
module = "fold_lm.v05_benchmarks.model_c322_saved_query_contrast"
phase = sys.argv[1]
if phase == "Validate":
    from fold_lm.v05_benchmarks import model_c322_saved_query_contrast as b
    paths = [Path(p) for p in sys.argv[2:]]
    assert len(paths) == 48
    b.runtime_preflight(paths, Path.cwd())
elif phase == "Execute":
    diagnostic_path = Path(sys.argv[2]); arguments = sys.argv[3:]
    stdout, stderr = sys.stdout, sys.stderr
    with diagnostic_path.open("x", encoding="utf-8", buffering=1) as diagnostic:
        class Tee:
            def __init__(self, original): self.original = original
            def write(self, text):
                diagnostic.write(text); diagnostic.flush(); return self.original.write(text)
            def flush(self): diagnostic.flush(); self.original.flush()
            def __getattr__(self, name): return getattr(self.original, name)
        sys.stdout, sys.stderr = Tee(stdout), Tee(stderr)
        faulthandler.enable(file=diagnostic, all_threads=True)
        try:
            print("[C322 science] module_begin", flush=True)
            sys.argv = [module, *arguments]
            runpy.run_module(module, run_name="__main__", alter_sys=True)
            print("[C322 science] module_return", flush=True)
        except BaseException:
            traceback.print_exc(file=sys.stderr); sys.stderr.flush(); raise
        finally:
            sys.stdout, sys.stderr = stdout, stderr
            faulthandler.enable(file=stderr, all_threads=True)
else:
    raise ValueError("Unknown C322 driver phase")
'@
if ($Mode -eq "Validate") {
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c322_saved_query_contrast.py") (Join-Path $Root "tests_lm\test_v05_c322_saved_query_contrast.py")
    if ($LASTEXITCODE -ne 0) { throw "C322 syntax preflight failed" }
    & $Python -X faulthandler -u -c $EntryPoint Validate @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C322 parent/pair precheck failed" }
    & $Python -X faulthandler -u -m unittest tests_lm.test_v05_c322_saved_query_contrast -v
    if ($LASTEXITCODE -ne 0) { throw "C322 own tests failed" }
    $Regression = @'
from pathlib import Path
import faulthandler, sys, time, traceback, unittest
with Path(sys.argv[1]).open("x", encoding="utf-8", buffering=1) as diagnostic:
    class Tee:
        def write(self, text):
            diagnostic.write(text); diagnostic.flush(); return sys.stderr.write(text)
        def flush(self): diagnostic.flush(); sys.stderr.flush()
    stream=Tee(); started=time.monotonic()
    def mark(phase, name):
        stream.write(f"[C322 regression {time.monotonic()-started:.3f}s] {phase}: {name}\n"); stream.flush()
    class ObservedSuite(unittest.TestSuite):
        def _handleModuleFixture(self, test, result):
            name=test.__class__.__module__
            if name==getattr(getattr(result,"_previousTestClass",None),"__module__",None):
                return super()._handleModuleFixture(test,result)
            mark("module_setup_begin",name); super()._handleModuleFixture(test,result); mark("module_setup_return",name)
        def _handleClassSetUp(self, test, result):
            cls=test.__class__
            if cls==getattr(result,"_previousTestClass",None): return super()._handleClassSetUp(test,result)
            name=cls.__module__+"."+cls.__qualname__
            mark("class_setup_begin",name); super()._handleClassSetUp(test,result); mark("class_setup_return",name)
        def _tearDownPreviousClass(self, test, result):
            previous=getattr(result,"_previousTestClass",None)
            if previous is None or previous==getattr(test,"__class__",None): return super()._tearDownPreviousClass(test,result)
            name=previous.__module__+"."+previous.__qualname__
            mark("class_teardown_begin",name); super()._tearDownPreviousClass(test,result); mark("class_teardown_return",name)
        def _handleModuleTearDown(self, result):
            name=getattr(getattr(result,"_previousTestClass",None),"__module__",None)
            if name is None: return super()._handleModuleTearDown(result)
            mark("module_teardown_begin",name); super()._handleModuleTearDown(result); mark("module_teardown_return",name)
    faulthandler.enable(file=diagnostic,all_threads=True)
    try:
        from fold_lm.v05_benchmarks import model_c322_saved_query_contrast as b
        assert len(b.regression_modules(Path.cwd()))==b.manifest()["modules"]
        suite=b.regression_suite(Path.cwd()); ids=tuple(t.id() for t in b.flatten(suite))
        observed=ObservedSuite(b.flatten(suite)); assert tuple(t.id() for t in b.flatten(observed))==ids
        assert len(ids)==len(set(ids))==b.manifest()["focused_tests"]; del suite
        mark("suite_ready",f"expected_focused_tests={len(ids)}; ordered_ids_preserved=True")
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(observed)
        mark("suite_return",f"tests_run={result.testsRun}; failures={len(result.failures)}; errors={len(result.errors)}")
        code=0 if result.wasSuccessful() else 1
    except BaseException:
        traceback.print_exc(file=stream); stream.flush(); raise
    finally:
        faulthandler.enable(file=sys.stderr,all_threads=True)
sys.exit(code)
'@
    $regressionLog = Join-Path $Root ("runs\c322-regression-" + [guid]::NewGuid().ToString("N") + ".log")
    & $Python -X faulthandler -u -c $Regression $regressionLog
    $code = $LASTEXITCODE
    $hex = "0x{0:X8}" -f [uint32]([int64]$code -band 4294967295L)
    $receipt = @("regression_exit_decimal = $code", "regression_exit_hex = $hex", "regression_diagnostic_log = $regressionLog")
    $receipt | Add-Content -LiteralPath $regressionLog -Encoding UTF8
    $receipt | ForEach-Object { Write-Output $_ }
    if ($code -ne 0) {
        Get-Content -LiteralPath $regressionLog -Encoding UTF8 -Tail 35
        throw "C322 focused regression failed; exit=$code ($hex)"
    }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    return
}
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c322-v5b-query-contrast-" + [guid]::NewGuid().ToString("N"))
    $id = [guid]::NewGuid().ToString("N")
    $scienceLog = Join-Path $Root ("runs\c322-science-" + $id + ".log")
    $stderrLog = Join-Path $Root ("runs\c322-science-stderr-" + $id + ".log")
    if ((Test-Path -LiteralPath $scienceLog) -or (Test-Path -LiteralPath $stderrLog)) { throw "Diagnostic log collision" }
    & $Python -X faulthandler -u -c $EntryPoint Execute $scienceLog --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead 2> $stderrLog
    $code = $LASTEXITCODE
    $hex = "0x{0:X8}" -f [uint32]([int64]$code -band 4294967295L)
    $receipt = @("science_exit_decimal = $code", "science_exit_hex = $hex", "science_diagnostic_log = $scienceLog", "science_stderr_log = $stderrLog")
    $receipt | ForEach-Object { Write-Output $_ }
    $receipt | Add-Content -LiteralPath $scienceLog -Encoding UTF8
    Get-Content -LiteralPath $stderrLog -Encoding UTF8 -Tail 60
    if ($code -ne 0) {
        Get-Content -LiteralPath $scienceLog -Encoding UTF8 -Tail 80
        throw "C322 diagnostic execution failed; exit=$code ($hex)"
    }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c322_saved_query_contrast as b
out = Path(sys.argv[1])
paths = [Path(p) for p in sys.argv[2:50]]
head = sys.argv[50]
assert len(sys.argv) == 51 and len(paths) == 48
b.precheck(paths, Path.cwd())
p, groups = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[3].c.audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
print("capability_gate_applicable = False", flush=True)
for row in p["validation_summary"]["overall"]:
    print("C322 overall", json.dumps(row,sort_keys=True), flush=True)
for row in groups:
    print("C322 group", json.dumps(row,sort_keys=True), flush=True)
print("diagnostic_complete = True; persisted_query_contrast = PASS; model_forward_calls = 0", flush=True)
'@
    & $Python -X faulthandler -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C322 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C322 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
