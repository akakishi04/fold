# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C319 ACCEPTED VALID NEGATIVE. C320 ACTIVE / INVALID ATTEMPT RECOVERY. C321 NOT REGISTERED.**
C320 remains the unique ACTIVE experiment;NO scientific C320 run or result has been established.
The recovery token denotes preflight recovery,not a fabricated INVALID scientific summary.
C318/C317 diagnostic PASS,C316/C315 negatives,C308 bounded PASS and prior verdicts unchanged.
Latest accepted execution:529c54ef63b1015b25632b8123a9a552eebcd263.
Latest accepted publication:3abe218dc9191d26963e5b5022d4d1983300084d. Do not rerun C319.

## Current operational evidence and recovery boundary

C320 preflight at ead33368286ae4539fabf0e264651e98858a136c reported focused regression failure.
The supplied log tail ends after C173 test36,all displayed tests ok,without final unittest
summary or traceback. Original child exit code unknown. Science/publication explicitly skipped.
User's isolated C174 setup+first-test probe subsequently passed in3.525s with exit0/0x00000000.
Its path: runs/c320-c174-probe-e44a2b5fc4fb45ec88526968521ef5af.log.
This is not whole-C174 or whole-suite success. Root cause UNCONFIRMED;do not assert a C174 bug,
OOM,thread bug or native crash from the final printed test name alone.

Recovery review:docs/c320-preflight-recovery-review.md.
Recovery authoring/review target:e5e0a07e5ebfd0816f0f26c0cc757ed2f31b1f52.
post_authoring_review=PASS for operational delta,not scientific execution or root-cause closure.
Only run_c320.ps1/invoke_c320.ps1 changed in the authoring commit. No tests,model source,
preregistration,scientific manifest,thresholds,data,checkpoints or accepted ancestors modified.

The same full5221-test ordered suite runs once in one interpreter. A transparent TestSuite
subclass brackets native unittest module/class setup/teardown and delegates the actual work.
Unique UTF8 direct regression log captures runner output,markers and supported fatal traces.
PowerShell records the exact child exit immediately in decimal/hex;nonzero exit reports a
35-line diagnostic tail before the established preflight skip. Existing preflight log is
copied to runs/c320-preflight-previous-<guid>.log before the next attempt. No automatic retry,
per-module splitting,additional test exclusion,thread change or environment reinstall.
Logging has I/O/timing overhead;it does not prove why the original process stopped.

Changed committed bytes were refetched and matched2/2. Post-refetch local observer tests7/7
PASS17.842s,including identical standard/observed fixture order and outcomes under normal/CP932
emulation,exception/native-exit evidence and log preservation. These use controlled fixtures,
NOT actual FOLD archives/tests. Actual own24/full5221 and Windows parsing were not run here.
The original scientific implementation review remains in docs/c320-post-authoring-review.md;
this recovery review supersedes only the old identities of the two operational scripts.

## Fixed C320 scientific registration

Experiment:C320-v5b-frozen-unequal-name-lengths. Stage:V5-B-FROZEN-UNEQUAL-NAME-LENGTHS.
Registration:docs/experiment-ledger-addendum-c320-preregistration.md.
Design:docs/v5b-unequal-name-lengths-v0.1.md.
Original science authoring:b975f7d2c8cfbf3c9ae71c4b9f147ab1be10ebd1;all scientific bytes unchanged.
Manifest:34ac7cbac03191c2e64ae05887f7d04cbc90c3cf0a73e18427708c1bbeed307d.

Question:can equal-name-length-trained models handle(2,4) and(4,2) names within one question?
Freeze all10 C319 states,seeds319001..319005,both mean_last and last_only. Keep each state's
actual trained_readout policy throughout old1..6 before -> unequal layouts -> old1..6 after.
Primary is all5 mean_last models passing BOTH layouts with original local/masked thresholds:
accuracy.90/query_pair.80/evidence_drop.35/query_drop.35/two_order.80. No averaging across a failed
layout and no last_only successes substituting for primary failure. C319 remains negative.

Same14,256parameters/64slots,canonical facts/values/questions/fact orders,English/Japanese,
TRAIN/HOLDOUT splits,three name families and all normal/evidence-blind/query-blind views.
1728new normal prompts,disjoint from old normals,no new byte vocabulary,max Japanese39tokens.
Every old output reproduces within1e-9 and exact argmax;original gates,weights/hooks preserved.
No retraining,decoder restriction,source substitution or checkpoint filtering. Both layouts
are new combinations of individually trained lengths,not proof of arbitrary name reasoning.

46ordered parent hashes -> actual C319.verify_artifacts with45ancestors and accepted HEAD.
C319 summary:runs/c319-v5b-trained-last-0f94e96bbbba43b395fcf8eab1e38246/summary.json.
SHA256:48815ca382d0da078da12ec2d54f2c42261e94498b682f679d8f46d746ec0580.
Use its own seven artifacts/final same-policy logits/checkpoint bundle and all10 exact flags.
C319 both arms5/5 at2..5;six mean_last5/5,last_only4/5. last_only319005 normal six567/576 and283/288;
paired mean_last575/576 and288/288. Original C319 acceptance/docs remain authoritative.

Protection remains766sources/1443inputs;OWN6 count unchanged,operational script hashes update
before the first valid C320 run. Missing direct dependencies stop;no pin waiver. Own24/modules205/
loaded5222/focused5221 with the sole original exact C204 exclusion. No new test inventory.
Scientific work:10frozen models,3420forwards,328320rows,13680core calls,training0,10state loads,
one bundle read,new checkpoints0. Five registered artifacts plus summary and unchanged schemas.
Complete data/prompt/loader/scorer/accounting details and historical reviews are preserved in
docs/handoff-history/c320-pre-recovery-1.md and the unchanged preregistration/design files.

## Retry and stop

Use only the standard dispatcher with the new recovery HEAD after git pull and ParseFile.
It redoes full Validate:46real parents/pins,own24,full5221 in the original order/process.
If that passes,the existing C320 science and publisher proceed unchanged. This is not a bypass
using the isolated C174 result. Validate failure still skips science/publication;use the direct
regression log and exact exit code instead of requesting the same old successful-test tail.
A single successful retry would permit evaluation but would not establish the original root cause.
Any new integrity failure repairs SAME C320. No C321 until a valid C320 result is formally judged.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

## Historical state

Pre-recovery handoff:docs/handoff-history/c320-pre-recovery-1.md.
Git blob:0f1c53da9b0dfa40d5f4b32ee9d1e23ec305bf69.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
