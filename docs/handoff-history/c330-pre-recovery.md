# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md Current response format(v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:explicit PowerShell7,ParseFile,tools/invoke_active_v2.ps1.
Accepted sources/tests/contracts/logs and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C329 ACCEPTED VALID NEGATIVE. C330 ACTIVE / NOT YET JUDGED. C331 NOT REGISTERED.**
C328 and all earlier verdicts unchanged. Do not rerun accepted C329 or older experiments.
C330 authoring approval is not scientific/native-regression PASS. No production adoption.

## Latest accepted evidence -- C329

Acceptance commit:a7a36bb212656f08bd8d1c5402512ce28acb1e00.
Report:docs/experiment-ledger-addendum-c329-c330.md.
Scientific execution:f8582ca34bd7e10c7403713e935debe94720dfde.
Published log commit:2d181d23c7f84749384e9283c8d8de2df7619bd8;sole parent equals execution.
Log docs/experiment-run-logs/c329/latest.log plus latest.json.
Publisher metadata150267Windows bytes;SHA256
625ed2c6a61293bd2c4d9f31784fc073b50bccc197646562c985850168ae57d4.
Log Git blob03d264150904b01f2041e0c34ffb6f5bc0f5b8c6.
Reviewer read remote native/regression/allfits/prefix/replay/seed/pair/final receipts
and independently summed deciding counts. No independent full Windows-log rehash,
local model/logit recomputation or optimizer-history replay is claimed. Older attached
C323/C324 logs are not evidence of this C329 execution.

Full5770tests/218modules PASS;673.454seconds;zero failures/errors/skips.
Native locks,parent semantics and allfive schedules/readout/backward preflight passed.
Five2400-step trajectories;five1200prefixes preserved;optimizer creations5;
ten saved checkpoints evaluated/replayed. Saved trajectory reconstruction,all1577
final uncached rereads,fresh832source/1577input envelope passed;all process exits0;
run_execution_valid=true. Scientific FAIL,paired success1/5 rather than required5/5.

Interior HOLDOUT answers1206->1427/1440(83.75%->99.097222%);pairs544->708/720.
All5paired interior counts improve;rescued/regressed answers224/3,pairs164/0.
By seed329001..329005:interior answers252->288,179->275,275->288,238->288,262->288;
pairs120->144,65->132,135->144,99->144,125->144.
Original pooled answers7072->7137/7200;paired answer gains8,45,13,-1,0;
paired pair gains8,42,6,7,0. Original pair gain sum63.
Interior full gate0/5->4/5;original2..6 retention1/5->1/5.
Length2/3/4 each4/5->5/5;length5:1/5->3/5;length6:1/5->1/5.
Only329005 passes the full paired criterion;do not select it for adoption.
The extension helps interior binding but is not yet all-seed reliable. Counts reuse
logical problems and are descriptive,not independent statistical samples. No optimal
budget,structural capacity,unseen-template,causal mechanism,Gate F or LLM claim.

## Exact C329 parent evidence

Folder:runs/c329-budget-66a7cc83726341aaa59542f02bc7a7e5/.
Primary science/summary.json SHA256:
89341eade41d5c35c2e7b9a7a84238b272adcd21c28d143da68fbc0aaf8fdf1a.
Mandatory execution-envelope.json SHA256:
6939cb8c53a44ffefd86342721d48d168e7c938f37432948ea3488fe1453b473.
Parent manifest9968ab6d8d2abdd3751b6ac1d1b1116a088d1c8abbdebdae50b580005d6fb7d8.
Parent science schemafold-c329-science-v1,statusFAIL,diagnostic_execution_valid=true,
candidate_gate=false,paired_success_count1. Envelopefold-c329-execution-envelope-v1.
Eight science outputs+primary+envelope=TEN immediate-parent files.
Inherit complete832source/1577input maps identically from both records.

## C330 registration and completed post-authoring review

Experiment:C330-v5b-saved-gate-localization;stage:V5-B-SAVED-GATE-LOCALIZATION.
Contract:docs/experiment-ledger-addendum-c330-preregistration.md.
Review:docs/c330-post-authoring-review.md.
Source/preregistration review target:a1d447e6b9f0d1a05f1dfa56a40223ea4c5c3c4c.
post_authoring_review = PASS.
Use the subsequent final activation HEAD in the user command,not this source-only
review target or an old acceptance/execution/publication HEAD.

All6committed files reread completely;Git blobs match independently hashed tested
local bytes. After reread,48/48normal PASS5.202s and48/48CP932-default-text-open
emulation PASS4.955s,zero failures/errors/skips. UTF8/noNUL/compile/import passed;
recursive LOAD_GLOBAL audit189code objects,undefined globals0. Manifest matches.
Author environmentLinuxPython3.13.5. Metric/parent/lease/runtime/inherited-suite
fixtures are explicitly synthetic,not native Windows/FOLD/full5818historical tests.
Actual diagnostic writer/loader/reconstruction and worker control paths exercised.
No author-side PowerShell AST execution claimed;mandatory user-side AST chain retained.

## C330 one scientific question and fixed scope

Which unchanged local binding,masked-dependence and both-order gates remain unmet
after the extension,and which matched conditions improve or regress1200->2400?
Use ALL ten saved checkpoint records,all5seeds,bothsteps,alloriginal2..6 and interior4,
TRAIN/HOLDOUT,3profiles,2languages,3entity subsets,both fact orders. No selection of
only failures or the successful seed. Original1 stays descriptive-only and excluded.
No new training,model forward,gradient,optimizer step,model state load or checkpoint.
Parent tensor semantic verification still reads/reconstructs saved evidence;separately
scoped work,not a new neural replay or free processing.

C270 scorer profiles tripled/shared_prefix2/shared_suffix2 are opaque slots. Preserve
actual input profile names too:original repeat/shared_prefix/shared_suffix;interior
u_dominant/balanced/v_dominant. Original5/6 remain untrained name families even on
logical TRAIN rows. Do not mistake scorer labels for actual name lengths.
Exact scorer writer fields,coordinates,normal/pair/masked integer counts,NLL,order
feasibility and saved flags are validated. Reconstruct local/order/domain/seed gates
and every per-seed/domain HOLDOUT count/gain and the unchanged parent composite.

Four local criteria unchanged:accuracy>=.90,query_pair_accuracy>=.80,
evidence_drop>=.35,query_drop>=.35. Both-order accuracy>=.80 separately retained.
Exclusive categories pass,normal_binding_only,mask_only,mixed;retain all overlapping
failed criteria. A mask-only category does not prove a causal shortcut. Do not sum
overlapping criteria as independent failed cells. Match exact coordinates,not row
position;preserve rescued,regressed,persistent and stable-pass transitions.

Work inventory:60score records;4320local+2160order cells;
2160local+1080order transitions;144strata of30local/15order cells.
Print10preserved seedflags,72extended2400strata,30domain/criterion transition summaries.
All detailed coordinates and both checkpoints remain in the local output.
Diagnostic PASS means integrity and full reconstruction,not favorable failure counts
or capability improvement. C329 remains VALID NEGATIVE regardless of C330 PASS.
capability_gate_applicable=false;Gate F remains NOT PASSED.
ManifestSHA256:
f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7.

## Complete protection, regression and execution

838sources=832inherited+6own;1593inputs=1577inherited+10parentfiles+6own.
Validate exact primary/envelope hashes,parent negative semantics,manifest/work,
full5770receipt,completed saved reconstruction and1577final rereads. All inherited
source/input bytes remain protected;no smaller-map or unpinned dependency fallback.
C329.semantic_recheck(out,data,old,new,cx,read) is called unchanged under no_neural,
using its five-trajectory/ten-checkpoint schema. It revalidates saved traces,tensor
hashes,raw-logit measurements and full summary without model forward. No recursive
older semantic bodies,though all older protected bytes remain checked.
Child own loader reads parent measurements.json/validation-summary.json explicitly.
No accepted module global/function is patched.

Route:invoke_active_v2 ->invoke_c330 ->run_c330 ->c330_execution controller/worker
->accepted_C329_composite_snapshot ->parent saved semantics ->ordinary full regression
->saved_gate_failure_localization under no_neural ->saved_localization_reconstruction
->final_uncached_input_recheck ->primary/envelope ->fresh byte/JSON verifier ->log push.
Full5818tests/219modules:5770inherited+48own;5819before sole inherited exact C204
mutable-ACTIVE exclusion. No new exclusions/skips or cached regression success.
Actual suite unique IDs/counts checked and ordered digest printed;separate ordinary
interpreter without scientific wrappers. All5818must pass before diagnosis.

Native unchanged R4 Windows read leases span all phases;initial independent reference
hashes and ALL1593final uncached rereads. Four outputs hash/size-bound before/after
saved reconstruction and again before summary/envelope writing. Fresh process checks
exact complete source/input maps and every source/input/output byte,manifest,parent,
regression,conservation and pure-JSON reconstruction. Not a new model/optimizer replay.

Four child outputs:diagnostic-plan.json,localization.json,transitions.json,
validation-summary.json. Primaryfold-c330-diagnostic-v1;envelopefold-c330-execution-envelope-v1.
Local:runs/c330-localization-<id>/science plus enclosing execution-envelope.json,
regression-result.json and science/regression/verify logs. Publish ONLY console to
 docs/experiment-run-logs/c330/latest.log and latest.json;never tensors or datasets.
10second heartbeats;phase markers;no200/1200/2400training progress expected.
Final:persisted_gate_localization=PASS ->execution_envelope_verified ->run_execution_valid=true.
Observed failed model criteria are diagnostic data,not execution failure.

## Stops and next handoff

Wrong host/branch/ExpectedHead,dirtytrackedtree,nonunique ACTIVE,missingdependency or
AST error SKIPS before scientific logging/publication. Source/input/schema/count/
criterion/parent/regression/saved-semantic/envelope failures stop SAME C330,not C331;
preserve evidence,no automatic retry. Publication-only failures are repaired without
redoing diagnosis. No CI,paidservice,reinstall,artifact deletion or old-result edits.
The user may report only finished. Read remote latest metadata/log;separate execution
HEAD from publication commit. Do not use old attached C323/C324 logs as current evidence.
For valid C330 finish acceptance AND next-C implementation/preregistration/committed
review/activation/command in the SAME response. INVALID repairs SAME C330.
Do not advance this branch for unrelated changes while the user runs the experiment.

## History and inherited compatibility seal

Pre-acceptance C329 handoff:docs/handoff-history/c329-pre-acceptance.md.
Acceptance and C330 preregistration are separate commits. All earlier records remain.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
