# C347 post-authoring review

Review date:2026-11-26 Japan time.
post_authoring_review = PASS
review_status = committed-byte/static review PASS; runtime gate pending
reviewed_source_head = 3f34750492c065ca9185517bd2e9e8f8b8865464
source_tree = 74d7b0069a8c0cef2f3ba58777ed48e9b95aa505
source_parent = c0597bbc24ca3db2761763b65cfe8521af7d1b2e

This review applies to all seven committed C347 OWN files, independently re-fetched
from the remote repository through EOF. The source commit contains only those seven
new files; C346 acceptance is a separate parent commit. Activation changes only
documentation and preserves every reviewed OWN blob. No user command was supplied
before independent review PASS. The independent reviewer authored none of these files.

## Reviewed file identity

| File | Git blob |
|---|---|
| docs/experiment-ledger-addendum-c347-preregistration.md | f42077fb9f692b1a99786e4e76d58bdd50f8a91f |
| fold_lm/v05_benchmarks/model_c347_saved_loss_transition.py | 5981644b491a390f2a0de7063a9966d76eb7e4c5 |
| tests_lm/test_v05_c347_execution.py | 9f386bb727f543276e09ffd8503b356c5864d580 |
| tests_lm/test_v05_c347_saved_loss_transition.py | ed31c2ce750a6c2d9048a2f48d1f65e701f39ff6 |
| tools/c347_execution.py | be4e4220b24e99e55a7c32b289ad85e8cfe278c0 |
| tools/invoke_c347.ps1 | f22dfe10a0f9c10812626e13be7c02f52dbfb9f1 |
| tools/run_c347.ps1 | 59bb3357cb337f97858392561f48a4d795f3a78a |

All modes are100644. Manifest:8e85821c7d4e69c49cd0695ccb5126a7dbb8b5cc0f5b9ca77f5fb0cd98a0aee3.
The independently recomputed seal agrees with source,preregistration and handoff.
No placeholder, stale child path, accidental parent mutation or missing direct
repository dependency was found. Inherited C346/C345/C344 and lazy ancestor helpers
remain pinned; no new external repository helper is called by the deciding path.

## Executed author checks and actual inventory

Author environment:Python3.12.14/Torch2.10.0+cpu/NumPy2.3.5.
The native user's registered Windows environment remains
Python3.13.15/Torch2.10.0+cu130/NumPy2.3.5; no environment change is authorized here.

| Author check | Outcome |
|---|---|
| Complete OWN normal |72/72 PASS,43.184146s|
| Complete OWN with CP932 default text-open simulation |72/72 PASS,43.333929s|
| Failures/errors/skips/expected failures/unexpected successes |0 in both runs|
| Four Python compile/import/pyflakes |PASS|
| Recursive bytecode free-global audit |324code objects/2271global loads,undefined0|
| Actual module loaders |6725raw/6724selected/245modules,OWN40+32|
| Actual PowerShell7.5.4 ParseFile |dispatcher/invoke/runner,0errors|
| Executed PowerShell validation-failure fixture |Validate entered,exit7,SKIPPED,no runner/publish/formal log|

All seven file SHA256 values were checked before and after both complete OWN runs
and static verification; no bytes changed. The committed blobs match those checked
bytes. Full selected-ID SHA:28b5c7fc80732b94cdb32f94f241cc142dff3e9da0dc68fdba26ded270ffef58.
The6652parent IDs/243groups remain the exact ordered prefix, SHA
39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394.
Every raw module was actually loaded and compared to its selected group; the sole
exclusion is tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
No new exclusions, skips or edits to accepted tests were introduced.

Normal author receipt SHA:c75ba742cf85a9db49956487f291f22bcb898d5dbd0c7271eec505a8910b584c.
CP932 author receipt SHA:e0ba9c4a3efb5dce93dc75cef20ff1f2891c6240b3f299e4fb8420cbe8a73270.
Static author receipt SHA:58f11b052d9306cfdad7c924e509b533a72a85ed420849ce1711dd1da94347d9.
PowerShell parser receipt SHA:df380efbea0e3e1a3e0969b2d9a16d5c776204d459d7723955cf13f3652478f3.
Independent committed review receipt SHA:0c768d3560f0dfb454fd6b155a13abc63c498bc48426b2416f84288bc6c44dc3.
Independent executable checks:72/72 PASS in41.480588s;all started/succeeded;failure/error/skip/expected-failure/unexpected-success0;actual245 raw loaders,seal and free globals independently checked.

## Scientific and parent-contract review

The new question is saved loss/correctness-transition decomposition on all15C346
states and all120seed/control/domain/split contrasts. Canonical full256 argmax/CE,
pair metadata, target alignment and every180terminal/120contrast binding match the
accepted writers. The parent is fold-c346-trained-v1 with FAIL and valid execution,
candidatefalse/eligible0; it is not C345's diagnostic schema or the invalid C346 attempt.
The exact parent primary/envelope hashes and source blobs are fixed separately.

The production diagnostic calls its real loader. Both real disk run and saved
reconstruction paths are exercised under no_neural. Fixtures use invented logits
and traces; only the historical trace verifier is stubbed during synthetic parent
construction, while real parent scorers/raw/replay/normal/terminal/gate checks remain.
This is software verification, not a formal evaluation on the user's native artifacts.

Tests cover all three exhaustive partitions, complete denominators, empty nulls,
signed contributions and delta extrema. Multiclass CW with lower CE and WC with
higher CE, a switched pair-max member, cancellation-aware reductions and exact
metadata/parent-result tampering prevent the relevant silent arithmetic errors.
Parent capability status is never promoted, and loss signs are not a PASS gate.
No trajectory analysis, new fitting, model call or parameter loading is introduced.

## Native Validate/Execute contract repair

Review found no documented waiver of docs/experiment-authoring-runtime-gate.md's
Validate-before-formal-log requirement. C347 therefore implements that boundary;
accepted C345/C346 scientific records and sources are unchanged.

Validate compiles/imports OWN and verifies runtime,cleanup,parent/source/input
protection and all6724regression tests before writing a successful receipt. It
reports actual/expected manifest digest before seal assertion and actual source/
input counts before separate mismatch failures. Its UTF-8 transcript closes before
receipt hashing; no successful receipt or formal publication follows validation failure.

The receipt binds canonical folder,HEAD,seal,runtime,compile/import inventory,
source/input maps,parent,cleanup,full proofs and transcript bytes. Execute checks
guards again and reopens the9681inputs plus495validation/proof files under separate
leases. Rehashing and exact map checks cover the process gap. It verifies the full
test evidence before diagnosis, so the suite runs once in Validate and zero times
in Execute. Both sets receive final uncached rereads and fresh-process verification.
The formal log reports reused receipt/log/closure hashes. Retention is493proofs+
2validation files+4science+primary+envelope=501contract outputs; auxiliary logs are
not silently counted as protected artifacts.

Actual entry-point tests observe compile/runtime/cleanup/parent/regression/proof/
reread ordering and reject missing,stale,mutated,incomplete or other-folder evidence.
Call order is not inferred from AST line numbers. Source-text assertions target
the actual launcher source/assignment; their tokens occur in executable statements,
and count contracts use actual loaders rather than numeric source-string matching.
CLI mode/argument index, PowerShell paths, publication C347 identity and UTF-8 writes
agree with preregistration. The timeout helper is the exact C346 mapping's cleanup
C344-R1, not its C345 parent.

## Final handoff lifecycle check

The final activation handoff was exercised against all eleven actual C272..C282
consumer tests before publication:11/11 PASS in0.190862s,all failure/error/skip/
expected-failure/unexpected-success counts0. Its12248-byte SHA256 is
a3449744333a641285dbaf7d0c72ee5bbe55fb1a8e4f2fc498995a3b38bc6535.
The previous6893-byte handoff is archived byte-for-byte with SHA256
578c49ee4baf9a177329c27a82ff821d1faf0ded18554b98cec044d7ff45acb9.
The permanent compatibility section remains exact; Formal state has only C347 ACTIVE.
Prepublication handoff-check receipt SHA:246c5d63edc94c6928232bcdce8f7855636e850deb4bf64775a4a3f0f5b1009b.

Historical handoff consumers are C272's permanent compatibility seal,
C273..C278 lifecycle-aware own seals plus that legacy seal, and C279..C282 immutable
acceptance/lifecycle checks. The eleven remain in the full suite. C347 tests only
the permanent C272 requirement against the live handoff; mutable ACTIVE checks use
fixtures plus actual final activation guards. No workaround exclusion was added.

The final activation must retain all seven source blobs and pass its actual guard
and eleven consumers again on the committed bytes. Native Windows validation,
full regression, original user artifacts and the formal C347 diagnostic remain
pending. C347 stays NOT YET JUDGED; Gate F remains NOT PASSED.
