# C321 scientific-execution recovery 1 — error capture, root cause unconfirmed

C321 INVALID EXECUTION / RETRY SAME C321. No accepted C321 capability result exists.
C320 remains ACCEPTED PASS in its bounded scope. C322 NOT REGISTERED. Gate F NOT PASSED.
This recovery repairs an observability gap,NOT a demonstrated root cause of the process exit.

## Original failed attempt

Scientific execution HEAD:5bffb4887a1f2729058472d875cf413bc26836e4.
Published log commit:caaa42ac45a332c8b946714919eda58c38533384.
Metadata:docs/experiment-run-logs/c321/latest.json.
Console:docs/experiment-run-logs/c321/latest.log.
Metadata log SHA256:25d7b0e289eaadeacce453f21022b52161302293c2706bc8a3c70056fc8c7733.
Metadata log bytes:947927. User publication receipt and retrieved metadata agree.
The commit contains only latest.json/latest.log. Preserve both;future latest updates do not
remove this immutable evidence identity. No synthetic scientific summary is created.

The log records own24 PASS (33.244s),full ordered5245 regression PASS (1098.824s),
failures0/errors0,regression_exit0/0x00000000,authoring_runtime_preflight=PASS.
Execute starts and prints registration_check772/1455 with the original manifest seal.
No first per-model [C321] progress line or completed summary is present before
run_execution_valid=False. Scientific subprocess nonzero exit is established by the runner
exception,but its exact code was not retained;the published text contains no Traceback.
This differs from the earlier C320 preflight interruption. Do not blame C174,OOM,hardware,
threads or a particular checkpoint without further evidence. Partial work is not a valid negative.

## Operational change

Authoring/review commit:22ae10b69bd800b64fd54ea772988ee752694e5c.
Only tools/run_c321.ps1 changes. The scientific Python module,own test file,launcher,47 ancestor
paths,preregistration,manifest,thresholds,readout policy and accepted sources remain byte-identical.

A shared embedded entry driver forwards Validate to the same runtime_preflight with exactly47
paths. For Execute it opens a unique UTF8 diagnostic file before invoking the unchanged module
through runpy.run_module(module,run_name="__main__",alter_sys=True),forwarding the exact original
--summaries/--output-dir/--expected-head arguments. Same one scientific process;no model function
replacement,profiling hook,exception suppression,automatic retries or environment/thread changes.

Python stdout/stderr text is flushed to the direct log before forwarding to the original stream.
Unhandled exceptions,including SystemExit,are recorded then propagated. Supported native fatal
traces point directly at that open file. Lower-level stderr that bypasses Python streams is
separately redirected by PowerShell. Some forced kills cannot emit a traceback;do not promise one.
After the child returns,PowerShell saves its exact exit IMMEDIATELY,then emits decimal/hex and
both log paths. Stderr tail and,on failure,direct diagnostic tail enter the normal published
console log before the existing throw/finally/publication path. Nonzero remains nonzero.
Unique log collisions are rejected before launch;diagnostic Python open uses exclusive x mode.

The complete regression block and complete postcheck tail are byte-identical to the original.
There remain exactly3 embedded Python blocks;postcheck paths[2:49],head49,argc50 unchanged.
No validation reuse or skipped regression:standard retry still runs own24 and full5245,then
science only after Validate passes. Launcher retains preflight archive and failed-run publication.
Standard dispatcher recognizes the INVALID ATTEMPT RECOVERY token and requires the new HEAD.
Logging adds I/O/timing overhead and cannot by itself establish why the original run failed.

## Post-authoring review actually performed

post_authoring_review=PASS for operational delta,not root-cause closure or FOLD scientific validity.
The complete254-line runner was refetched from the immutable authoring commit in consecutive
ranges. Returned Git blob1616f367072110e9c4e5252948da732c8f6091db matches the independently
hashed12882-byte local file. Compare with failed-log commit shows exactly one modified runner.
The original runner was independently matched to blob3e06070df3d0fb76b788b49b664c164fd02a2737.

AFTER refetch/match,nine local operational test methods were run without omission:
normal9/9 PASS in8.271s;CP932-mode9/9 PASS in8.016s;both processes exit0.
CP932 mode patches omitted text-encoding defaults and uses cp932/backslashreplace subprocess
stdio while preserving direct UTF8 logs. It is not full Windows emulation.

Tests execute the exact new embedded driver in fresh Python subprocesses using controlled
replacement modules,not FOLD checkpoints. They compare direct -m against the driver for
__main__/module identity,all CLI arguments including47 spaced/Japanese paths,and working directory.
Valid scientific status FAIL with normal return remains exit0;Python ValueError remains exit1;
SystemExit0/23 preserve their exits;os._exit37 leaves the last flushed output;controlled Linux
SIGABRT leaves a native fatal stack. Core dumps are disabled in that fixture. Those artificial
failures test evidence capture,not reproduction of the user's failure. Additional checks cover
Unicode stdout/stderr,native stderr bypass,import failures,existing-log refusal,exact47-path
preflight dispatch,incorrect-path-count rejection and unchanged block/index contracts.

All3 embedded blocks compile. New dependencies are standard-library modules only. No new
repository-local scientific dependency is introduced. Source772/protected1455 and manifest
813f7283535086c9b7ebd416da1fb1d50b5240ece9d58e364173b4cb4d433fea remain unchanged in definition.
The runner's new blob is captured by the existing child OWN protection at retry HEAD.

Local environment:Linux/Python3.13.5. PowerShell is NOT installed. Native PowerShell ParseFile,
actual47archives,own24/full5245 and actual10-checkpoint scientific evaluation were NOT rerun
here. They remain mandatory user-side gates. Local operational tests do not substitute for them.

## Retry and stop

Use the standard active dispatcher with the later recovery-documentation HEAD,not this authoring
commit or the old published attempt's HEAD. Existing failed-run log remains unchanged in Git.
A fresh run directory is used;no partial output is adopted as final. If Validate fails,skip
science/publication as before. If science fails,the unchanged launcher publishes its failed log,
now with child-exit and diagnostic tail when available. Inspect that evidence before another retry.
No C322,no change to family/model/seed/primary/gates,no capability or Gate F promotion.
Even a successful instrumented retry does not retrospectively identify the original root cause.
