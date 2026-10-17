# C330 R1.1 -- repair the registered regression-module namespace contract

Date: 2026-10-18 Japan time. SAME C330 / V5-B-SAVED-GATE-LOCALIZATION.
C330 remains ACTIVE / INVALID ATTEMPT RECOVERY. C329 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED; C331 NOT REGISTERED. No C330 scientific verdict exists.
This contract supersedes the unaccepted R1 execution contract, not its scientific
question. Original R1 contract is archived in docs/handoff-history/c330-r1-contract.md
and remains at b5521796a4f301f963792b96768a1f16aea83309.

## Attempt02: observed software defect, distinct from attempt01

Scientific execution HEAD: b5521796a4f301f963792b96768a1f16aea83309.
Publication commit: 6507abc349f838e525b1152035f71707041d4343; sole parent is execution.
Publisher log SHA256: 76d77f1728a12d5b20f5052325fda5730e8e2ebaa711585353b5b5577668a73d.
Publisher original Windows bytes: 7454. Git log blob: 912a591797a968bfb05a0b1f84fc406a4e865ee9.
Metadata blob: b7a5571c5e78e6bd546f10c29de976acdd3905e1.
Exact archive: docs/experiment-run-logs/c330/attempt-02/latest.log and latest.json.
Local failed attempt: runs/c330-localization-2e8b40e9df1a4d9885c4afd4b0795312/.

Native locks, C329 saved semantics and841-source/1596-input registration passed.
The regression coordinator then raised ValueError: test module/ID in partition(),
line133 of tools/c330_recovery_r1.py. Regression/science exit1; run_execution_valid=false.
No regression_module_begin occurred: no isolated test module ran and diagnosis was
not reached. This attempt is NOT another observed 0xC0000005 native exception.
The earlier C311 access violation remains unresolved by this run.

R1 accepted only tests_lm.* in BOTH partition() and validate_plan(). But the accepted
C324 R6 RECOVERY_MODULES registry already contains these three tests_tools modules:
- tests_tools.test_c324_locked_hash_r4 (37 tests);
- tests_tools.test_c324_verified_session_r5 (48 tests);
- tests_tools.test_c324_scientific_recovery_r6 (48 tests).
They were already part of the original5818 test-ID sequence. They are not new tests
or loader errors. Source: tools/c324_scientific_recovery_r6.py,
Git blob353f54f1bd66117728839049e99b17fc3aee4bf2.
The prior author's all-tests_lm synthetic inventory missed the real namespace mix.

## Minimal repair and explicit invariants

Only three unaccepted R1 files change: tools/c330_recovery_r1.py,
tests_lm/test_v05_c330_recovery_r1.py and this contract. Paths are retained deliberately.
The runner, launcher, dispatcher, original C330 benchmark/executor/48tests/scientific
contract and all C329-and-earlier accepted files stay unchanged.

allowed_module() accepts the existing tests_lm module grammar plus ONLY the three
exact registered tests_tools module names. Both partition and plan validation use
it. build_plan also checks that the inherited R6 registry equals this list.
Unknown namespaces/tool modules, nested or malformed names, mismatched module/ID
prefixes, missing/duplicate IDs and noncontiguous groups remain errors. Error output
now includes the offending module and ID. There is no catch-and-skip conversion.

Original5818 ordered test IDs retain fixed digest:
0e90ec4c1cf292528d7aec95bac8388f12e53fb1ca9dad08ebba58c9174d5183.
The same32 recovery test method IDs are retained and strengthened;5850tests across
220modules remain required. There are5851 before the unchanged sole exact C204
mutable-ACTIVE exclusion. No new exclusion, skip, relaxed assertion or cached success.
Mixed-namespace planner/partition/plan-validator/module-child paths are now covered.
Large inventories and module bodies in these author tests remain explicitly synthetic;
real unittest loading/execution of those bodies is not execution of the historical
C324 tooling suite or the user's5850-test inventory.

All modules run once, sequentially, each in a fresh ordinary interpreter. No retry,
parallel execution or success selection. Normal per-module fixtures execute intact.
Track all actual started/successful test IDs. Require every expected ID and zero
failures/errors/skips/expected failures/unexpected successes. Require process exit0,
identity-bound module receipts, and hashes of every receipt/log. Setup failure or
native crash cannot produce a complete regression receipt. Worker and fresh verifier
rebuild the real plan and verify all5850 successful IDs before accepting diagnosis.

## Scientific constants, parent and protection

Original C330 scientific manifest is unchanged:
f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7.
Benchmark blob73c30cba137b4d11a9ac39c8f3702bdd0b2e6baf;
original executor blob1fb5fb47e1e9998cd8ec3a38b25afeb7ec44b31a.
All10 C329 states,5seeds,both1200/2400 checkpoints,sixdomains,TRAIN/HOLDOUT,
profiles/languages/entity sets/fact orders and thresholds .90/.80/.35/.35/.80 remain.
4320local/2160order cells and2160local/1080order transitions remain. New scientific
forwards/gradients/training/optimizer steps/checkpoints remain0. No C329 retraining.

Parent execution f8582ca34bd7e10c7403713e935debe94720dfde;
folder runs/c329-budget-66a7cc83726341aaa59542f02bc7a7e5/;
primarySHA89341eade41d5c35c2e7b9a7a84238b272adcd21c28d143da68fbc0aaf8fdf1a;
envelopeSHA6939cb8c53a44ffefd86342721d48d168e7c938f37432948ea3488fe1453b473.
Use unchanged C329 five-trajectory/ten-state semantic loader under no_neural.
No recursive older semantic body, but all inherited bytes remain checked.

Protection remains841sources=832parent+6C330own+3recovery;
1596inputs=1577parent+10immediate-parent files+6C330own+3recovery.
No reduction or unpinned dependency. Native R4 leases, independent initial hashes
and all1596final uncached rereads remain. All four diagnostic outputs are bound
before/after reconstruction and before summary/envelope; fresh verification checks
complete source/input/output maps, all regression evidence and pure-JSON reconstruction.

Both result and envelope require execution_revision=C330-R1.1 and the exact
recovery_manifest object and SHA256:
8db2d7bedfbf9276848791a0710a0e8bb031fc39d8186722e4540269d4347e5c.
The existing r1-named plan/module/evidence schemas and filenames stay unchanged;
the required new recovery hash disambiguates their revision. Original diagnostic
plan execution counts are superseded by this execution manifest, not silently used.
A successor must honor the full841/1596 unions and this exact revision.

## Author review and invocation boundary

Reread all three committed modified files, compare Git blob identities with tested
local bytes, then rerun32tests,CP932 default-text-open emulation,compile/import,
UTF8/no-NUL and free-global audits before issuing the command. Preserve the prior
review as history. Do not claim native Windows/full5850 or C311 crash reproduction.
The original R1 sources are available at the failed execution HEAD, not overwritten
in Git history. No old test failure is reclassified as scientific evidence.

Standard active_v2 dispatcher and PowerShell AST chain remain. Existing run_c330.ps1
still invokes c330_recovery_r1.py; role becomes C330-R1.1-MODULE-ISOLATED-RECOVERY.
Guards still bind branch, ExpectedHead, tracked tree and unique ACTIVE C330 before
logging. Local runs/c330-localization-<id>; console publication remains C330/latest.*.
After parent verification expect220 module begin/complete records, then complete5850
regression, unchanged diagnosis, final rereads and fresh verification. Individual
module OK is not full success. Any failure stops SAME C330 without retry or C331.
No package/environment changes, artifact deletion, CI, paid services or gate changes.
Publication-only failure is repaired without rerunning the diagnostic.
