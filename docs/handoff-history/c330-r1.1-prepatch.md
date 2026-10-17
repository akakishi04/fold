# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and Current response format(v2) in docs/experiment-conversation-handoff-protocol.md.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5. Standard explicit PowerShell7,
dispatcher ParseFile,tools/invoke_active_v2.ps1. Accepted source/tests remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C329 ACCEPTED VALID NEGATIVE. C330 ACTIVE / INVALID ATTEMPT RECOVERY. C331 NOT REGISTERED.**
C330 attempts01 and02 are INVALID EXECUTION, not scientific negative results.
C330-R1.1 implementation and committed-byte post-authoring review are complete.
post_authoring_review = PASS.
Use the subsequent documentation-only final recovery HEAD supplied in the user command,
not the source review target or either failed execution HEAD. No C329 retraining/C331.

## Latest failed attempt -- C330 attempt02 / R1

Execution:b5521796a4f301f963792b96768a1f16aea83309.
Publication:6507abc349f838e525b1152035f71707041d4343;sole parent equals execution.
Publisher7454Windows bytes;SHA76d77f1728a12d5b20f5052325fda5730e8e2ebaa711585353b5b5577668a73d.
Log blob912a591797a968bfb05a0b1f84fc406a4e865ee9;metadata blob b7a5571c5e78e6bd546f10c29de976acdd3905e1.
Exact copies:docs/experiment-run-logs/c330/attempt-02/latest.log and latest.json.
Local failed folder:runs/c330-localization-2e8b40e9df1a4d9885c4afd4b0795312/.
Native locks,C329 saved semantics,841source/1596input registration passed.
Regression coordinator failed in c330_recovery_r1.partition,line133,ValueError:test module/ID.
No isolated module started;no completed regression or C330 diagnostic. Exit1 in
regression/science;run_execution_valid=false. Log publication succeeded.

R1 incorrectly allowed only tests_lm in BOTH partition and validate_plan. The existing
C324R6 registry includes tests_tools.test_c324_locked_hash_r4(37),
tests_tools.test_c324_verified_session_r5(48),tests_tools.test_c324_scientific_recovery_r6(48).
The all-tests_lm author fixture missed this mixed namespace. It is an authoring bug,
not a user-environment fault. This attempt is NOT another observed native access violation.
Attempt01's0xC0000005 in C311 setup remains separately unresolved;see attempt-01 logs.
The latest review used the actual remote log/source,not old attached C323/C324 logs.
No independent whole-Windows-log rehash or native crash reproduction is claimed.

## R1.1 repair and completed source review

Source/review target:bec77853b3044b5c0a4254562589d48a8358283c.
Contract:docs/c330-recovery-r1.md (now R1.1;previous version archived).
Review:docs/c330-r1.1-post-authoring-review.md.
All3 changed protected files reread at exact commit;Git blobs match tested local bytes.
After reread:normal32/32PASS3.722s;CP932-default-open emulation32/32PASS3.604s;
failures/errors/skips0. Compile/import/UTF8/noNUL PASS;129code objects audited;
undefined globals0. Exact old guard reproduced on registry-name fixtures;reinstating
the old predicate breaks both targeted tests. Real32recovery IDs unchanged.

Author environmentLinuxPython3.13.5. The220module/5850ID planner fixture contains
both namespaces with synthetic inherited cases and the real32loader. Module-child
fixtures execute real unittest against explicitly synthetic module bodies. These are
NOT the real historical5850suite, native Windows, real C329 artifacts or scientific
C330 results. Do not describe them as such. No author-side PowerShell AST execution;
the existing mandatory user-side AST chain is unchanged.

Minimal code change:shared allowed_module accepts original tests_lm grammar plus
ONLY the three existing tests_tools names. Partition and plan validation both call
it. build_plan checks equality against the actual inherited R6 registry. Unknown
namespaces/nested names/loader errors/ID-prefix mismatches/duplicates remain rejected.
Errors include offending module/ID. No catch-and-skip or acceptance of arbitrary modules.

Only unaccepted R1 executor/test/contract changed;same file paths. Original C330
benchmark/executor/48tests/scientific contract,run_c330.ps1,invoke_c330 and active_v2
are unchanged. Original32 recovery test method IDs remain,with stronger checks.
Full5850tests/220modules,5851before sole inherited exact C204 exclusion;no new skips.
Original5818ordered-ID SHA:
0e90ec4c1cf292528d7aec95bac8388f12e53fb1ca9dad08ebba58c9174d5183.
Operational R1.1 contractSHA:
8db2d7bedfbf9276848791a0710a0e8bb031fc39d8186722e4540269d4347e5c.

One fresh ordinary interpreter per module,sequentially,once only. Preserve fixtures,
all actual started/successful IDs,PID/exit0,hash-bound plan/receipts/logs/aggregate.
Only full success authorizes diagnosis. Worker and fresh verifier reconstruct the
real plan and verify all5850 successful IDs. Isolation does not establish single-
process stress equivalence or prove the earlier native fault fixed;native run pending.

## Scientific constants and protection

Original science manifest:
f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7.
All10C329 states,5seeds,both1200/2400 checkpoints,sixdomains,TRAIN/HOLDOUT,allprofiles/
languages/entity sets/fact orders remain. Thresholds.90/.80/.35/.35/.80 unchanged.
4320local/2160order cells,2160local/1080order transitions. New scientific training,
forward,gradient,optimizer steps/checkpoints0. Diagnostic PASS is integrity only.

Parent C329 execution:f8582ca34bd7e10c7403713e935debe94720dfde.
Folder:runs/c329-budget-66a7cc83726341aaa59542f02bc7a7e5/.
PrimarySHA89341eade41d5c35c2e7b9a7a84238b272adcd21c28d143da68fbc0aaf8fdf1a.
EnvelopeSHA6939cb8c53a44ffefd86342721d48d168e7c938f37432948ea3488fe1453b473.
Parent remains accepted VALID NEGATIVE:paired1/5,interior0/5->4/5,retention1/5->1/5;
interior answers1206->1427/1440 and pairs544->708/720. All earlier verdicts unchanged.
Use unchanged five-trajectory/ten-state parent semantic loader under no_neural.
No older semantic-body recursion,but every inherited byte remains protected.

Protection841sources=832parent+6C330own+3recovery;
1596inputs=1577parent+10immediate-parent files+6C330own+3recovery.
Native R4 read leases,independent initial hashes and all1596final uncached rereads
remain. Four diagnostic outputs hash-bound around reconstruction and final records.
Primary/envelope must both require execution_revision=C330-R1.1,exact recovery_manifest
and its SHA;envelope binds regression_isolation. R1-named files/schemas stay for
compatibility;new manifest hash is mandatory. Original diagnostic-plan execution
counts are superseded by this manifest. Successors must use full841/1596 maps.

## Execution and stops

Standard invoke_active_v2 ->invoke_c330 ->run_c330.ps1 ->c330_recovery_r1.py.
Role:C330-R1.1-MODULE-ISOLATED-RECOVERY. No user selection of numbered recovery script.
Progress:locked parent ->full_regression_fresh_process_per_module ->220module
begin/complete records ->full5850success ->saved_gate_failure_localization ->saved
reconstruction ->1596final rereads ->fresh byte/receipt/JSON verifier ->log publication.
Module-level OK is not full-regression PASS. No scientific training-step display.
Local runs/c330-localization-<id>/ contains regression-plan-r1.json,module-NNN.json/
.log,regression-isolation-r1.json,regression-result.json,science outputs and envelope.
Only console is published to docs/experiment-run-logs/c330/latest.*;both invalid
attempt archives remain. Complete run requires execution_envelope_verified and
run_execution_valid=true. Any namespace/test/native/source/input/receipt/schema/
semantic failure stays INVALID SAME C330. No auto retry,no C331,no test omission.
Stale branch/HEAD/ACTIVE/host/dependency/trackedtree/AST skips before science logging.
No reinstall,paidservice,CI,artifact deletion or accepted-model retraining.
Publication-only failure repairs publication without diagnosis rerun.

User may report only finished. Read latest remote metadata/log;separate execution
HEAD from publication. Ignore old attachments for current verdict. For a valid C330
complete acceptance AND next-C implementation/registration/review/launcher in the
same response. Another INVALID stays same-C330 recovery. Do not move this branch for
unrelated work while the user's registered run is active.

## History and inherited compatibility seal

Prior R1 handoff:docs/handoff-history/c330-r1-prepatch.md.
Original R1 contract:docs/handoff-history/c330-r1-contract.md.
Both old reviews/attempt01/attempt02 remain as history,not current acceptance.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
