# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C320 ACCEPTED PASS. C321 ACTIVE / INVALID ATTEMPT RECOVERY. C322 NOT REGISTERED.**
C321 is the unique ACTIVE experiment. One attempted scientific run is INVALID EXECUTION;
no C321 capability result has been accepted. C320 bounded capability PASS and earlier verdicts
remain unchanged. Do not rerun C320 or treat a successful log publication as scientific PASS.
Latest accepted execution:0e4687acfa72355cbddc47c3ceb98700354fe34d.
Latest accepted publication:7a693b5d7747ab67146a8c2fa2f996cb10b5054d.
Latest INVALID attempt execution:5bffb4887a1f2729058472d875cf413bc26836e4.
Latest INVALID attempt publication:caaa42ac45a332c8b946714919eda58c38533384.

## Failed C321 attempt and same-C recovery

Failed console:docs/experiment-run-logs/c321/latest.log atcaaa42ac45a332c8b946714919eda58c38533384.
Metadata SHA256:25d7b0e289eaadeacce453f21022b52161302293c2706bc8a3c70056fc8c7733;947927bytes.
Own24 PASS,full5245 PASS (1098.824s),regression failures0/errors0,exit0/0x00000000.
Authoring runtime preflight PASS. Execute prints registration_check772/1455,then terminates
before the first per-model progress line. run_execution_valid=False. No complete summary.
Scientific subprocess was nonzero,but exact exit and Python exception text were not recorded.
ROOT CAUSE UNCONFIRMED. Do not infer C174/threads/OOM/hardware or a checkpoint bug from this log.
Unlike the prior C320 issue,the regression phase completed. This is not a scientific negative.

Recovery review:docs/c321-science-recovery-review.md.
Operational authoring/review commit:22ae10b69bd800b64fd54ea772988ee752694e5c.
Only run_c321.ps1 changed:shared preflight/science entry driver,unique directUTF8 science log,
Python exception/native-fatal capture,separate native stderr file,and exact immediate child exit
in decimal/hex. Failed output tails enter the existing published console before the throw.
It forwards the unchanged scientific module and exact original arguments;no model monkeypatch,
new training,per-module split,extra exclusion,environment change or automatic retry.
This repairs missing diagnostic information,NOT a demonstrated original failure cause.

Committed254-line runner refetched and blob-matched1616f367072110e9c4e5252948da732c8f6091db.
Post-refetch operational tests:normal9/9 PASS8.271s;CP932-mode9/9 PASS8.016s,both exit0.
Controlled subprocesses test direct-m equivalence,valid-negative return,ordinary exceptions,
SystemExit,abrupt exit,native abort,Unicode/import/overwrite and exact path forwarding.
They are NOT actual FOLD science,own24 or full5245. Linux/Python3.13.5;no native PowerShell.
Regression block and postcheck tail byte-identical;3embeddedblocks compile;postcheck[2:49]/49/50.
Standard guarded retry still runs all mandatory Validate gates before science. Windows ParseFile,
real parent verification,own24/full5245 and actual model evaluation remain user-side gates.

## Unchanged C321 scientific contract

Experiment:C321-v5b-frozen-interior-name-order. Stage:V5-B-FROZEN-INTERIOR-NAME-ORDER.
Registration:docs/experiment-ledger-addendum-c321-preregistration.md.
Design:docs/v5b-interior-name-order-v0.1.md.
Original scientific authoring review:docs/c321-post-authoring-review.md.
Original authoring target:672a96440ec779d7f440685bb0c856da0e7e41c5.

Four-character name pairs share endpoints and character multisets but differ in interior order:
u_dominant uuvu/uvuu;balanced uuvv/uvuv;v_dominant vuvv/vvuv.
All10C319states,seeds319001..319005,both mean_last/last_only,own trained readout,14256parameters,
64slots,original bilingual facts/value splits/questions/orders and all three views are retained.
864new normal prompts,maximum45encoded tokens. No retraining,new vocabulary or state selection.
Primary:all5 mean_last states pass all3families under unchanged local/masked gates:
accuracy.90/query_pair.80/evidence_drop.35/query_drop.35/two_order.80. Comparator cannot rescue it.
Old1..6before -> newinterior -> old1..6after;old outputs reproduce C319<=1e-9 and exactargmax,
original2..6gates unchanged;full weights/hooks preserved. No partial-run outputs accepted.

Parent:C320 execution0e4687acfa72355cbddc47c3ceb98700354fe34d,
summaryruns/c320-v5b-unequal-names-d1599525908a404998a52011a5567b81/summary.json,
SHA2569e41e82228f26cf525ee54e4097abd493a339641d6b3d3f5b2a6d10ba8868431.
Verify47ordered parents through the same protected loaders;C319 checkpoint bundle remains at
summaries[1],not the C320 output directory. Same sole direct import C320 and inherited helpers.
Own6/source772/protected1455;own24/modules206/loaded5246/focused5245;exact C204 exclusion only.
Manifest813f7283535086c9b7ebd416da1fb1d50b5240ece9d58e364173b4cb4d433fea unchanged.
Science3150forwards/302400rows/12600core calls,10strictstate loads,training0,newcheckpoints0.
New runner adds logging overhead only;scientific workload and output schemas are unchanged.

## Latest accepted C320 evidence

Acceptance:docs/experiment-ledger-addendum-c320-c321.md.
Mean_last5/5 for(2,4),5/5 for(4,2),5/5 both;normal8640/8640. Last_only4/5 both,
only319002 short_long HOLDOUT287/288 fails. All original replays0.0;run_execution_valid=True.
C320's own earlier preflight interruption also remains unexplained despite its successful retry.
No old accepted results or test bytes are changed for C321 recovery.

## Execution and stop

Pull the recovery HEAD and use tools/invoke_active_v2.ps1 via PowerShell7 after dispatcherParseFile.
Validate retains47parents,own24/full5245 in one ordered interpreter,then unchanged science.
New science process emits science_diagnostic_log/science_stderr_log and science_exit_decimal/hex.
Original preflight preservation and regression diagnosis remain. A scientific failure still
publishes an INVALID attempt log;Validate failure skips science/publication. No forced success.
If another failure occurs,inspect its direct error/exit evidence before retrying again.
C322 remains unregistered. No changes to scientific conditions and no Gate F promotion.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

## Historical state

Pre-recovery handoff:docs/handoff-history/c321-pre-science-recovery-1.md.
Git blob:425f0533c8ddefb52c3c507d9f532f8eec6f1311.
Earlier state/history is preserved in that file and immutable commits.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
