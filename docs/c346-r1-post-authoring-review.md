# C346 documentation recovery 1 — independent post-authoring review

Date: 2026-11-25 Japan time.
**post_authoring_review = PASS**
Review target HEAD: `728fdf12e436cb5ba7373400b247dfd6e54425bc`.
Tree: `edda40167fff90dedddd5e3f8f3eb44c095a3b24`.
Sole parent: failed-attempt publication
`3b70c50464ac60ff202c8c8fad4d01c200ed9d06`.

The filename's r1 denotes the first recovery document. The executable is still
**C346-R0** and its cleanup implementation still **C344-R1**. No C346-R1 executor
exists. The scientific manifest and every OWN source/test/preregistration byte
remain unchanged. C346 is scientifically unjudged; attempt01 is INVALID.

## Independent committed-remote review

A nonauthor retrieved and read all five changed documentation/evidence files
through EOF and all seven original C346 OWN files at the exact review commit.
Remote Git object identities, byte lengths and SHA256 agree with the committed
tree, clean worktree and author-tested bytes. Commit metadata independently
confirms the stated tree and sole parent. No blocking discrepancy or post-review
source correction was found.

Independent review receipt SHA256:
`6c28ceb79d3177d6c90c74af2ae54c8e8a036501a19f478f8f94bd76cca0828e`.

| Changed path | Git blob | Meaning |
|---|---|---|
| `docs/c346-recovery-r1.md` | `060cade139381a6c95f956e73054f363acc4865f` | Invalidity, cause, minimal repair and fixed contracts |
| `docs/experiment-ledger-and-handoff.md` | `c2ec5163a77442d63d697d9b6882b0f0a15bc8b9` | Recovery status and restored permanent C272 seal |
| `docs/experiment-run-logs/c346/attempt-01/latest.json` | `d720962b06c60a3f448350f283c89f27685377de` | Exact published metadata copy |
| `docs/experiment-run-logs/c346/attempt-01/latest.log` | `29cfc34fe9e3522dd0aeab7421e6f8559a7c1441` | Exact published Git log copy |
| `docs/handoff-history/c346-pre-recovery-r1.md` | Same blob as the publication's original handoff | Exact pre-recovery operational history |

The reviewed recovery handoff has13,669bytes and SHA256
`12ab4b06f62feb66a6f3a39fc7c8565c5787f6e0150b4801ae3fcf31cd10190a`.
The recovery addendum has11,479bytes and SHA256
`fea163f7364ec6055818ac13e229c8ebde356524fe8151a7c16037346174790c`.
Activation changes review metadata in the handoff, so its later SHA256 is expected
to differ and must receive the separate final-byte check described below.

## Evidence and cause verified

The failed publication has the original execution
`e19e872577d7f574920e83b568499666f2cd41e4` as sole parent and adds only latest.log/json.
Git LF157,018bytes reconstructs the original Windows158,908bytes and metadata
SHA256 `87f33308c45d299e165923dfc4d8f7b3b82ebce87ab2876b07098ebf247f4419`.
The attempt archives and pre-recovery handoff exactly match that publication.

The log records157 modules begun,156 complete,3,693 tests run,3,692 passes and
one assertion failure. C272 test24's failing assertion prints the exact original
handoff. The C272 historical seal is absent there, though present in its immutable
benchmark/preregistration/acceptance records. The first omission is the C345
acceptance rewrite `f5fc8e89b5bb3d2749df91aa3b503596a6be1fc2`.

Six cleanup checks, native locks, parent saved semantics and objective preflight
completed. The formal15-model C346 cohort, final input rereads and fresh verifier
did not begin or complete. This supports INVALID EXECUTION, not a scientific
negative or a conclusion about half-rate training.

The C273 preflight-recovery record, authoring-runtime gate and C274/C278 accepted
preregistrations explicitly define this C272 value as an append-only historical
compatibility seal. Its restoration outside Formal state complies with that
stable contract. It does not freeze current ACTIVE/HEAD or weaken an assertion.
All accepted parent source/test files and the sole existing C204 exclusion remain.

## Actual author and independent checks

Both checks used the actual loader and unchanged existing test bodies. The author
check ran against the completed local repair with publication HEAD3b70c50 still
checked out; those audited file hashes exactly match review commit728fdf1.
The independent check ran at the clean committed728fdf1 worktree after remote
byte verification and also invoked the actual read-only executor guard.

| Check | Author | Independent reviewer |
|---|---|---|
| C272..C282 exact live-handoff consumers | 11 PASS /0.262327s | 11 PASS /0.233961s |
| Failures/errors/skips/expected failures/unexpected successes | All0 | All0 |
| Actual raw/selected/module inventory | 6653/6652/243 | 6653/6652/243 |
| OWN inventory | 48science+26infrastructure=74 | Same74 exact IDs |
| C345 ordered prefix | 6578IDs/241modules unchanged | Identical prefix verified |
| Seven OWN blobs against original sourcebe76c4c | Unchanged | Remote and local bytes unchanged |
| Manifest self-hash | PASS | PASS |
| Formal state | Unique C346 recovery ACTIVE | Same;actual guard PASS |

Full ordered-ID SHA256:
`39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394`.
Parent ordered-ID SHA256:
`2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a`.
Manifest:
`8dad5562249bf21517bb8487c5c6970ac75b55405252dbbf5c3512d797d46d64`.

The author report SHA256 is
`a40f527298139e181cbc07d9a24e7cd0f67b83e7cb61e85cbce1f2f6d16eecbd`.
Both reviews confirm944/9177 as the unchanged source/input contract; they do not
claim a new native Windows artifact snapshot. Protection, scientific WORK,
parent ABI, all rates/seeds/cohorts/gates and the full regression are unchanged
because the seven OWN files and all accepted dependencies retain their exact bytes.

Actual PowerShell7.5.4 `Parser.ParseFile` returned0 errors for the unchanged
active_v2 dispatcher (864tokens), invoke_c346 (494), run_c346 (142), and the short
retry-block template (91). The final literal ExpectedHead substitution must be
parsed again before delivery. The block parses the dispatcher before invocation;
the unchanged dispatcher/launcher then parse selected entry points.

Runtime: Linux Python3.12.14 / Torch2.10.0+cpu / NumPy2.3.5. These are focused
authoring/recovery checks, not a complete Windows6652-test run or15-model execution.
The unchanged OWN74 normal/CP932 reports in the original C346 review remain
historical and were not rerun for this documentation-only repair. No new Python
or PowerShell source requires a changed-source compile/free-name audit.

## Final activation boundary

This review authorizes a documentation-only activation that records this PASS
and review target. All five recovery artifacts, except the handoff's review
metadata, and all seven OWN blobs must remain unchanged.

Before the retry command is delivered, a nonauthor must retrieve the final
activation's remote handoff/review bytes, compare the activation delta, execute
the same11 actual consumers against the final handoff, and confirm uniqueC346
ACTIVE plus the actual clean-branch/HEAD guard. Do not substitute a pre-activation
test result for this final-document check. The main integration record may bind
that final activation HEAD and result without changing the reviewed feature HEAD.

Use that final feature activation HEAD as ExpectedHead, never the original source,
old failed execution, log publication, this recovery-review target or main merge.
The native environment remains the registered `.venv-py31315`. Retain attempt01,
rerun the complete preflight/regression/work/verifier contract, and freeze the
experiment branch during execution. C347 remains unregistered until C346 has a
valid scientific judgment. A further integrity failure stops SAME C346.
