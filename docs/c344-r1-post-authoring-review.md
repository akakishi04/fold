# C344 R1 independent post-authoring review

Date: 2026-11-22 Japan time.
**post_authoring_review = PASS**
Review target HEAD: `ca6df52fb72ed0020df7e3d027d738d28870464f`.
Tree: `ab92d489e8093721c33d4abcfe976418f821b58c`.
Sole parent: invalid-attempt publication `8d83d94b7923c0ebb06c052ee473c003cd490335`.
Execution revision: `C344-R1`; scientific manifest remains
`a663ebb0b09671c6d277b5abec6d09604a49a194d5d61409a1a5bf5018785ad8`.

## Committed-byte identity

Independent reviewers retrieved all seven OWN files and the recovery documents
through EOF and compared remote text, Git object IDs and tested local bytes.
Both the code/science review and evidence/document review passed without a
blocking discrepancy or a post-publication source correction. The source commit changes
exactly eight paths: three unaccepted C344 OWN files, the authoritative handoff,
the R1 contract, the original handoff archive and the two attempt-01 log archives.
No accepted source/test or historical dispatcher/launcher is edited.

| C344 OWN path | Bytes | Git blob |
|---|---:|---|
| `fold_lm/v05_benchmarks/model_c344_pair_max_training.py` | 42,806 | `6261a0c267df027835093c7ce53958f8f0034186` |
| `tools/c344_execution.py` | 35,923 | `76c8663caafc97ece440df71e250e546198d425b` |
| `tests_lm/test_v05_c344_pair_max_training.py` | 43,790 | `95238b223fc88e7436a7fa8253b1c4324fd60a11` |
| `tests_lm/test_v05_c344_execution.py` | 40,903 | `9d90efe54454296f610b7f0e8bdf81be1ef852af` |
| `tools/run_c344.ps1` | 966 | `d479b15b6f5bf1ccb5bd8a99b45d181df1ca9f18` |
| `tools/invoke_c344.ps1` | 3,150 | `dafe28b0befa4b9f2a7d65ab2665e0e0140cebd2` |
| `docs/experiment-ledger-addendum-c344-preregistration.md` | 21,834 | `f8ae384e9a8d7dce38e89f78d10929008229a52a` |

The changed OWN files are the executor, infrastructure test module and preregistration.
The benchmark, science test module and two numbered PowerShell entry points retain
their original blobs. The active_v2 dispatcher is also unchanged. Both attempt-01
archives reproduce the log publication's exact Git bytes; the pre-recovery handoff
is an exact copy of the original. The original scientific preregistration is kept
as a prefix with an explicit R1 execution-contract appendix.

## Author validation

| Check | Result |
|---|---|
| Combined C344 own tests, ordinary file encoding | 72 PASS; 88.620 seconds |
| Combined own tests, CP932 default text-open emulation | 72 PASS; 85.799 seconds |
| Final infrastructure module after its last correction | 24 PASS; 2.419 seconds |
| Failures / errors / skips / expected failures / unexpected successes | 0 in both combined runs |
| Changed Python UTF8, no NUL, compile/import, pyflakes | PASS; 0 pyflakes findings |
| Free-global audit of changed files | 160 code objects / 1,204 LOAD_GLOBAL instructions / 0 unbound names |
| Actual full unittest inventory | 6,515 before the existing exclusion; 6,514 selected / 239 modules |
| Own module inventory | 48 science + 24 infrastructure methods; original IDs retained |
| Parent inventory | 6,442 IDs / 237 groups preserved as an identical ordered prefix |
| Registered source and input counts | 930 / 8,183; same seven OWN paths |
| PowerShell 7.5.4 AST parser | 0 errors for active_v2 / invoke_c344 / run_c344 |
| Standard retry block AST template | 90 tokens / 0 errors |

Author environment: Linux Python3.12.14 / Torch2.10.0+cpu / NumPy2.3.5.
The combined runs used the frozen local source with HEAD8d83d94 and match the
published source bytes. They are not described as tests started after publication.
CP932 emulation changes only implicit text-open encoding; explicit UTF8 and binary
I/O retain their behavior. No native Windows qualification or full 6,514-test
scientific execution is claimed from these author runs.

Both combined reports independently bind the same five checked source/test/prereg
files. Executor SHA256:
`ecc37c1f6fdb68272d3e492de12a18de20f71bc2e0ccd90355c521c7bd9f2fe4`.
Infrastructure test SHA256:
`3b2b691e26cf680f5a6d29868a078d5588eb15d5e1e33387108d11ada849c9aa`.
Full ordered-ID SHA256:
`c5d7db147680f739c62bbbc2f12be324c66ba16ea108dc04beb3071f56abaaa3`.
Parent ordered-ID SHA256:
`0581297af93ba5c06494f1e41627de8a2f574ee2ef62a46147225a55755ad7f5`.
The sole inherited C204 mutable-ACTIVE exclusion remains the same exact ID.

## Recovery behavior checked

The actual failing and corresponding R5 timeout tests remain in the full inventory.
Only their module-local monitor bindings are wrapped. Original arguments, executable,
50ms timeout, returned object and non-timeout behavior are preserved; exceptions
propagate and bindings restore on success and failure.

Behavioral cases cover immediate readiness, first/second-log sharing delays,
permanent error32, non32 errors, missing files, partial-handle close, CloseHandle
failure and changed log contents. Both log handles must coexist before success;
all acquired handles are closed or close failure is reported. One10s deadline
bounds all polls. Fresh hashes run only after probe handles have been closed.

The six exact historical timeout test executions are R4x3 then R5x3. Author tests
run their actual subprocess/TemporaryDirectory behavior. On Linux, only the Windows
DELETE-access operation is an explicit stand-in; on Windows the same behavioral
test uses the real native API. Win32 argument/return types also have explicit ABI
fixtures. This combination is not represented as a measurement of Windows sharing.

The production six-case preflight runs after native-runtime validation and before
expensive snapshot/parent hashing. Every exact ID must start, succeed and complete
one cleanup barrier, with no skips or hidden retries. Failure blocks the heavy
snapshot and subsequent stages. It supplements the full regression.

The existing envelope binds revisionC344-R1 and the exact preflight receipt. The
fresh verifier rejects altered/missing IDs, counts, success fields, pins, HEAD or
revision. Original primary/envelope/artifact/proof files remain the same set;
no extra artifact file changes the489-output successor contract.

The new exact R4/R5 source/test pins already belong to the inherited C324-R6
FIXED/EXTRA protection inventory. All four match accepted blobs. No newly called
repository helper is left outside source protection.

## Scientific scope and retry

The scientific benchmark and all48 science tests are byte-identical to the original
registration. Seeds, paired initial states, token/target streams, cohorts, optimizer,
2,400 updates/model, all gate thresholds,60contrasts and four strict endpoints stay
fixed. Model work and numerical preflight counts are unchanged. The early cleanup
checks have no neural work.

Attempt01 remains INVALID EXECUTION, not a valid scientific negative. No formal
C344 model fitting or candidate/control evaluation was completed in that attempt.
C343 remains accepted diagnostic evidence; C342 remains valid negative; Gate F is
not passed. C345 is not registered.

Use the later documentation-only R1 activation HEAD as ExpectedHead on
feat/sft-target-loss. The activation must retain all seven reviewed OWN blobs.
The standard block parses active_v2; the dispatcher/launcher parse the selected
entry points. Final block substitution changes only the40-hex ExpectedHead and is
parsed again before delivery. main integration must preserve the registered feature
HEAD so that the user's log publication continues on the experiment branch.

Native Windows completion remains pending. The barrier proves delete-readiness
at its observation point and unchanged logs, not identity or termination of every
possible handle owner. Any later sharing failure remains an error in the original
cleanup. All preflight, regression, artifact or native failures stop SAME C344.
