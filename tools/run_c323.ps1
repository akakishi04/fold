param(
    [Parameter(Mandatory=$true)][ValidateCount(49,49)][string[]]$Summaries,
    [Parameter(Mandatory=$true)][string]$ExpectedHead,
    [Parameter(Mandatory=$true)][ValidateSet('Validate','Execute')][string]$Mode
)
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Python = Join-Path $Root '.venv-py31315\Scripts\python.exe'
function Confirm-Repository {
    $branch = git branch --show-current
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'feat/sft-target-loss') { throw 'Wrong branch' }
    $head = git rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead) { throw 'Unexpected HEAD' }
    $changes = @(git status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0 -or $changes.Count -gt 0) { throw 'Tracked tree is dirty' }
}
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw 'Authoritative Python missing' }
Confirm-Repository
$EntryPoint = @'
from pathlib import Path
import faulthandler, runpy, sys, traceback
from fold_lm.v05_benchmarks import model_c323_saved_fact_order_bias as b
phase = sys.argv[1]
if phase == 'Validate':
    paths = [Path(p) for p in sys.argv[2:]]
    assert len(paths) == 49
    b.runtime_preflight(paths, Path.cwd())
elif phase == 'Execute':
    log = Path(sys.argv[2]); args = sys.argv[3:]; native_out,native_err = sys.stdout,sys.stderr
    with log.open('x',encoding='utf-8',buffering=1) as diagnostic:
        class Tee:
            def __init__(self, native): self.native=native
            def write(self,txt): diagnostic.write(txt);diagnostic.flush();return self.native.write(txt)
            def flush(self): diagnostic.flush();self.native.flush()
            def __getattr__(self,n): return getattr(self.native,n)
        sys.stdout,sys.stderr=Tee(native_out),Tee(native_err)
        faulthandler.enable(file=diagnostic,all_threads=True)
        try:
            print('[C323 science] begin',flush=True)
            sys.argv=['fold_lm.v05_benchmarks.model_c323_saved_fact_order_bias',*args]
            runpy.run_module('fold_lm.v05_benchmarks.model_c323_saved_fact_order_bias',run_name='__main__',alter_sys=True)
            print('[C323 science] returned',flush=True)
        except BaseException:
            traceback.print_exc(file=sys.stderr);sys.stderr.flush();raise
        finally:
            sys.stdout,sys.stderr=native_out,native_err
            faulthandler.enable(file=native_err,all_threads=True)
else:
    raise ValueError('Unknown C323 execution phase')
'@
if ($Mode -eq 'Validate') {
    & $Python -m py_compile (Join-Path $Root 'fold_lm\v05_benchmarks\model_c323_saved_fact_order_bias.py') (Join-Path $Root 'tests_lm\test_v05_c323_saved_fact_order_bias.py')
    if ($LASTEXITCODE -ne 0) { throw 'C323 Python syntax failed' }
    & $Python -X faulthandler -u -c $EntryPoint Validate @Summaries
    if ($LASTEXITCODE -ne 0) { throw 'C323 parent/query-order precheck failed' }
    & $Python -X faulthandler -u -m unittest tests_lm.test_v05_c323_saved_fact_order_bias -v
    if ($LASTEXITCODE -ne 0) { throw 'C323 own tests failed' }
    $Regression = @'
from pathlib import Path
import faulthandler,sys,time,traceback,unittest
with Path(sys.argv[1]).open('x',encoding='utf-8',buffering=1) as diagnostic:
    class Tee:
        def write(self,s): diagnostic.write(s);diagnostic.flush();return sys.stderr.write(s)
        def flush(self): diagnostic.flush();sys.stderr.flush()
    stream=Tee();start=time.monotonic()
    def mark(phase,name):stream.write(f'[C323 regression {time.monotonic()-start:.3f}s] {phase}: {name}\n');stream.flush()
    class ObservedSuite(unittest.TestSuite):
        def _handleModuleFixture(self,test,result):
            name=test.__class__.__module__
            if name==getattr(getattr(result,'_previousTestClass',None),'__module__',None):return super()._handleModuleFixture(test,result)
            mark('module_setup_begin',name);super()._handleModuleFixture(test,result);mark('module_setup_return',name)
        def _handleClassSetUp(self,test,result):
            cls=test.__class__
            if cls==getattr(result,'_previousTestClass',None):return super()._handleClassSetUp(test,result)
            n=cls.__module__+'.'+cls.__qualname__;mark('class_setup_begin',n);super()._handleClassSetUp(test,result);mark('class_setup_return',n)
        def _tearDownPreviousClass(self,test,result):
            cls=getattr(result,'_previousTestClass',None)
            if cls is None or cls==getattr(test,'__class__',None):return super()._tearDownPreviousClass(test,result)
            n=cls.__module__+'.'+cls.__qualname__;mark('class_teardown_begin',n);super()._tearDownPreviousClass(test,result);mark('class_teardown_return',n)
        def _handleModuleTearDown(self,result):
            n=getattr(getattr(result,'_previousTestClass',None),'__module__',None)
            if n is None:return super()._handleModuleTearDown(result)
            mark('module_teardown_begin',n);super()._handleModuleTearDown(result);mark('module_teardown_return',n)
    faulthandler.enable(file=diagnostic,all_threads=True)
    try:
        from fold_lm.v05_benchmarks import model_c323_saved_fact_order_bias as b
        mods=b.regression_modules(Path.cwd());assert len(mods)==len(set(mods))==b.manifest()['modules']
        suite=b.regression_suite(Path.cwd());ids=tuple(t.id() for t in b.flatten(suite))
        observed=ObservedSuite(b.flatten(suite));assert len(ids)==len(set(ids))==5293 and tuple(t.id() for t in b.flatten(observed))==ids
        del suite;mark('suite_ready',f'focused={len(ids)};ordered=True')
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(observed)
        mark('suite_return',f'ran={result.testsRun};failed={len(result.failures)};errors={len(result.errors)}')
        status=0 if result.wasSuccessful() else 1
    except BaseException:
        traceback.print_exc(file=stream);stream.flush();raise
    finally:faulthandler.enable(file=sys.stderr,all_threads=True)
sys.exit(status)
'@
    $regressionLog = Join-Path $Root ('runs\c323-regression-' + [guid]::NewGuid().ToString('N') + '.log')
    Write-Output "regression_diagnostic_log = $regressionLog"
    & $Python -X faulthandler -u -c $Regression $regressionLog
    $code = $LASTEXITCODE
    $hex = '0x{0:X8}' -f [uint32]([int64]$code -band 4294967295L)
    $receipt = @("regression_exit_decimal = $code","regression_exit_hex = $hex","regression_diagnostic_log = $regressionLog")
    $receipt | Add-Content -LiteralPath $regressionLog -Encoding UTF8
    $receipt | ForEach-Object { Write-Output $_ }
    if ($code -ne 0) {
        Get-Content -LiteralPath $regressionLog -Encoding UTF8 -Tail 45
        throw "C323 focused regression failed; $code ($hex)"
    }
    Confirm-Repository
    Write-Output 'authoring_runtime_preflight = PASS'
    Write-Output 'scientific_execution_started = False'
    return
}
$Completed = $false
try {
    $Out = Join-Path $Root ('runs\c323-v5b-fact-order-' + [guid]::NewGuid().ToString('N'))
    $id = [guid]::NewGuid().ToString('N')
    $scienceLog = Join-Path $Root ('runs\c323-science-' + $id + '.log')
    $stderrLog = Join-Path $Root ('runs\c323-science-stderr-' + $id + '.log')
    if ((Test-Path -LiteralPath $scienceLog) -or (Test-Path -LiteralPath $stderrLog)) { throw 'Science diagnostic log collision' }
    Write-Output '=== C323 saved fact-order comparison ==='
    & $Python -X faulthandler -u -c $EntryPoint Execute $scienceLog --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead 2> $stderrLog
    $code = $LASTEXITCODE
    $hex = '0x{0:X8}' -f [uint32]([int64]$code -band 4294967295L)
    $receipt = @("science_exit_decimal = $code","science_exit_hex = $hex","science_diagnostic_log = $scienceLog","science_stderr_log = $stderrLog")
    $receipt | ForEach-Object { Write-Output $_ }
    $receipt | Add-Content -LiteralPath $scienceLog -Encoding UTF8
    Get-Content -LiteralPath $stderrLog -Encoding UTF8 -Tail 60
    if ($code -ne 0) {
        Get-Content -LiteralPath $scienceLog -Encoding UTF8 -Tail 80
        throw "C323 science failed; exit=$code ($hex)"
    }
    $Postcheck = @'
from pathlib import Path
import json,sys
from fold_lm.v05_benchmarks import model_c323_saved_fact_order_bias as b
out=Path(sys.argv[1]);paths=[Path(p) for p in sys.argv[2:51]];head = sys.argv[51]
assert len(sys.argv) == 52 and len(paths) == 49
b.precheck(paths,Path.cwd())
p,groups=b.verify_artifacts(out,paths,head)
print('summary =',out/'summary.json',flush=True)
print('summary_sha256 =',b.context()[4].c.audit.sha(out/'summary.json'),flush=True)
print('scientific_status =',p['status'],flush=True)
for row in p['validation_summary']['overall']:print('C323 overall',json.dumps(row,sort_keys=True),flush=True)
for row in groups:print('C323 group',json.dumps(row,sort_keys=True),flush=True)
print('diagnostic_complete = True; persisted_fact_order = PASS; model_forward_calls = 0',flush=True)
'@
    & $Python -X faulthandler -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw 'C323 saved result postcheck failed' }
    $Completed = $true
}
finally {
    Write-Output '=== C323 POSTCHECK ==='
    Confirm-Repository
    Write-Output 'tracked_tree = clean; execution_HEAD = preserved'
    Write-Output "run_execution_valid = $Completed"
}
