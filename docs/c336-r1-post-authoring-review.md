# C336 R1 post-authoring review

Date: 2026-10-20 Japan time.
post_authoring_review = PASS
Source/recovery review target: cb7a7dc1b9287c4c1ac790d88441e496427e94c1.
Invalid publication base: de6d6bb1d43b69d26f0463426fbf56229871d087.
This approves the authoring repair, not Windows/full6090 or C336 diagnostic success.
Use the subsequent documentation-only recovery HEAD in the retry command.

## Committed-source verification

Both modified Python files were fetched again at the exact source commit and read
through EOF: executor1..150,151..300,301..411; tests1..180,181..340,341..483.
The complete100-line recovery contract was reread. Local raw-byte Git blob hashes
match the returned remote identities:

| File | Git blob |
|---|---|
| tools/c336_execution.py | 2d35c49a0adf570458c7232cf44e373e7e2e54c4 |
| tests_lm/test_v05_c336_saved_query_order_patterns.py | a63cc7da34ba531ad3ed171d63c42a5f93d5cd7d |

The source commit compare confirms only these two existing code files changed,
plus recovery/handoff documentation and exact attempt/history copies. No benchmark,
preregistration, accepted source/test, R4 helper, runner, launcher or dispatcher edits.
Local full R4 source matches6459b1f6e4051fbfc54db2894f7abe3a7521df3a; unchanged benchmark
matches78e33df0faed7cddcc888d4c068f8026327d99e8. These are reconstructed targeted files,
not a complete repository checkout. No hidden dependency replacement is claimed.

## Executed post-reread checks

- Normal own suite:32/32PASS;0failures/errors/skips;7.056seconds.
- CP932-default-text-open emulation:32/32PASS;0failures/errors/skips;7.949seconds.
- All three C336 Python files compile/import and decodeUTF8,without NUL/trailing whitespace.
- Recursive LOAD_GLOBAL audit:200nested code objects;undefined globals0.
- Actual32test ID order unchanged,verified against pre-repair AST method names;
  digest96ce8e07f180137d2035601083aade23244cac87e83f23dfae3eff23940a2b73.
- Scientific manifest self-hash unchanged and valid:
  e6f992e680bc4b80284dbc04366566f737fb1bfd3f55fb0ac10d76d90ebd76af.
- AST comparison finds only scientific_worker changed among executor functions/classes;
  all snapshot,loader,regression,semantic verification and output-writing functions remain.

Each suite ran in a separate Python invocation. CP932 emulation wraps builtins.open
and io.open only for unspecified/locale text encoding;explicit encodings and binary
opens remain unchanged. Environment:LinuxPython3.13.5/Torch2.10.0+cpu/NumPy2.3.5;
fixture setup uses2Torch threads. No package installation or CI. No pwsh executable
available;native PowerShell AST execution was not performed. The unchanged mandatory
user-side dispatcher/launcher/runner AST chain remains.

## Capacity and protection checks

The registered4360-input union exceeded inherited default4096. The fix supplies
max_files=s.INPUT_COUNT to the unchanged accepted cache;it is neither unlimited nor
an eviction workaround. The new log prints the configured and registered counts.
No source/proof/input/semantic protection is removed. This is a cached-lease bound,
not a claim that the process uses exactly4360OS handles in total.

Strengthened test22 now materializes all3893synthetic ancestor inputs,461parent
outputs and6child files. The production snapshot/parent-proof code runs through the
REAL accepted LockedHashes with an explicit SOFTWARE lease fixture. Default4096
reproduces failure before the full union. Explicit4360 completes the exact map.
Checks require all4360leases remain until context exit,one independent initial hash
and one final reference hash per input(exact per-path call counts),cache reuse at
capacity,and rejection of the4361st distinct file before acquiring another lease.
No eviction occurs. All leases close after either success or exception. Equal-size
byte mutation still fails the final uncached-reference check. Original parent-proof
count/tamper assertions remain. The lease fixture does not establish Windows sharing
semantics;no actual user checkpoint/ancestor outcome is reconstructed in this fixture.

Strengthened test29 runs the actual scientific_worker and fresh verifier with its
existing synthetic collaborators. Its cache constructor now requires explicit integer
max_files equal to the registered input count;the old permissive **kwargs omission
is no longer accepted. Existing call ordering and changed diagnostic-flag rejection
remain checked. The production pipeline still stops before diagnosis on regression
failure and requires all4360 final uncached rereads.

Three in-memory worker mutations were tested independently:omit max_files,restore4096,
or use infinity. The targeted worker test rejects each(1test/1expected error per
mutant,0failures/skips). Those are intentional negative controls,not failures of the
reviewed source. The worker function was restored and all local file blob hashes and
manifest were rechecked afterward. No mutated source was committed.

## Scope and approval boundary

Same32own IDs,6090selected tests/226modules,877sources/4360inputs. No new exclusion,
skip,retry,cached test success or change to accepted historical tests. The existing
R4 source is already an inherited protected dependency and is not modified.
All10C335states,all domains/splits/languages,12960quads/6480paired quads/51840answers,
720strata,all30parent contrasts and four diagnostic outputs remain unchanged.
No new model inference/training/gradient/optimizer work or checkpoint. No C335 rerun.
C335 stays ACCEPTED VALID NEGATIVE;GateFNOTPASSED;C337NOTREGISTERED.

The current attempt stopped during parent snapshot,before C336 full regression or
classification. It supplies no C336scientific evidence. Exact failed log/metadata
are archived under c336/attempt-01. Earlier author review remains historical,not
proof of successful native execution. The original author missed the capacity limit.

NativeWindows/full6090tests/actual4360-protected-input diagnosis remain unexecuted by
the author. A user retry must complete them and fresh verification before acceptance.
The final commit changes documentation only. Any new technical failure stays SAME
C336. No environment reinstall,paid service,artifact deletion,threshold relaxation,
accepted-source mutation or automatic retry. Future successors must explicitly pass
their own preregistered protected-input count instead of inheriting4096 implicitly.
