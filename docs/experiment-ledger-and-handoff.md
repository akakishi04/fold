# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and Current response format(v2) in docs/experiment-conversation-handoff-protocol.md.
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Runtime Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5. Entry:explicit PowerShell7,
ParseFile,tools/invoke_active_v2.ps1. Accepted source/tests/logs remain immutable.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C329 ACCEPTED VALID NEGATIVE. C330 ACTIVE / INVALID ATTEMPT RECOVERY. C331 NOT REGISTERED.**
C330 attempt01 is INVALID EXECUTION;no scientific result was produced or accepted.
R1 source is written;post-authoring review PENDING. No retry command until review.
Do not rerun C329 or advance to C331. Earlier verdicts remain unchanged.

## Invalid C330 attempt01

Execution:90ba026a0b24beeb448dcb1db354aab3501489bf.
Publication:d362e1b654b04fb0a8ee285ddbd9f7ca5f37b6e5;sole parent equals execution.
Published logs remain at docs/experiment-run-logs/c330/latest.* and exact archive
copies at docs/experiment-run-logs/c330/attempt-01/latest.*.
Publisher Windows log bytes20290;SHA256
99755b6c4ddfff20f6c144ca63a9b3646e066d1cc034de9b610fcd058e1fa99d.
Native locks/C329 saved semantics/838source1593input registration passed.
Full5818test/219module regression crashed in C311Tests.setUpClass -> C311.analyze
line139 with native exit0xC0000005 (3221225477). Scientific/controller exit1;
run_execution_valid=false. No complete regression receipt or C330 diagnosis.
Underlying native cause NOT established;do not blame a specific library/hardware.

## Same-C330 R1 repair

Contract:docs/c330-recovery-r1.md.
New execution route:unchanged invoke_c330 ->run_c330.ps1 ->c330_recovery_r1.py.
Only the not-yet-accepted runner's Python target changes. C330 diagnostic,original
executor,48tests,launcher and original scientific contract remain byte-identical.
R1 adds executor,32tests,contract. No accepted C329-and-earlier edits.
R1 contractSHA:e6bc2750bc4df477e12110ab0c60b2093e5eff985409439ae987d277685448ef.
Original C330 diagnosticSHA:f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7.

Keep all5818 old test IDs/order,verified by fixed SHA:
0e90ec4c1cf292528d7aec95bac8388f12e53fb1ca9dad08ebba58c9174d5183.
Append32tests:5850total/220modules (5851before sole inherited C204 exclusion).
Run each module ONCE in a new ordinary interpreter,sequentially,no retries/skips.
Track all actual started/successful IDs and normal fixture setup/teardown.
Bind plan,PID,exit0,module receipts/logs and aggregate;rebuild full plan and verify
all evidence in worker and fresh final verifier. No scientific phase without full
success. Isolation is mitigation,not proven native-root-cause repair or a claim of
single-process cross-module stress coverage. Native validation remains pending.

R1 protection841sources/1596inputs=832/1577 parent +original6own +new3own +10parent
files in the input map. Native R4 leases/all1596final uncached rereads retained.
Primary and envelope require execution_revision=C330-R1,exact recovery_manifest and
its SHA;envelope additionally binds regression_isolation. Original diagnostic-plan
is scientific-definition evidence;runtime counts are superseded by the R1 manifest.
Diagnostic cells4320/order2160 and matched transitions2160/1080 unchanged;all ten
C329 states retained;all thresholds unchanged;new scientific model work0.

## Exact accepted parent and scientific boundary

Parent C329 execution:f8582ca34bd7e10c7403713e935debe94720dfde.
Parent folder:runs/c329-budget-66a7cc83726341aaa59542f02bc7a7e5/.
PrimarySHA89341eade41d5c35c2e7b9a7a84238b272adcd21c28d143da68fbc0aaf8fdf1a.
EnvelopeSHA6939cb8c53a44ffefd86342721d48d168e7c938f37432948ea3488fe1453b473.
Parent valid negative,paired1/5;complete832source1577input maps. Use unchanged C329
five-trajectory/ten-state loader,not an older diagnostic schema. No old-model refit.
Original C330 question/cohort/masks/local gates remain as preregistered. C330 PASS
would mean diagnostic integrity,not capability or a changed C329 verdict.

## Stops and handoff

Stale branch/HEAD/ACTIVE/dirtytree/host/dependency/AST:SKIPPED before logging.
Source/input/test/receipt/native/schema/semantic/envelope failure:INVALID SAME C330.
No C331,no auto retry,no test omission,no package reinstall,no user artifact deletion,
no CI or paid service. Log publication only failure is repaired without rerunning.
User may send only finished;read latest remote C330 logs,distinguish execution HEAD
from publication. Ignore old C323/C324 attachments as evidence of current execution.

## History and inherited compatibility seal

Prior complete handoff:docs/handoff-history/c330-pre-recovery.md.
C329 acceptance:docs/experiment-ledger-addendum-c329-c330.md.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
