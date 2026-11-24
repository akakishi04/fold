# C346 documentation recovery 1 — restore inherited provenance seal

Date: 2026-11-25 Japan time.
**C346 — INVALID EXECUTION / RETRY SAME C346.**
Experiment `C346-v5b-pair-max-rate`; stage `V5-B-PAIR-MAX-RATE`.
This is the first documentation recovery. The unchanged executable revision is
**C346-R0**, not C346-R1. C345 remains accepted diagnostic evidence, C344 remains
ACCEPTED VALID NEGATIVE, and Gate F remains NOT PASSED. C347 is not registered.

## 1. Failed attempt and immutable evidence

| Item | Value |
|---|---|
| Scientific execution HEAD | `e19e872577d7f574920e83b568499666f2cd41e4` |
| Published log commit | `3b70c50464ac60ff202c8c8fad4d01c200ed9d06` |
| Publication parent | Execution HEAD, sole parent |
| Original Windows log | 158,908 bytes |
| Original SHA256 | `87f33308c45d299e165923dfc4d8f7b3b82ebce87ab2876b07098ebf247f4419` |
| Git LF log | 157,018 bytes; 1,890 LF characters |
| Git LF SHA256 | `51158ffdf7a251dff9a83308e881b41ff2fc8c36050207cd018164c4def1e70e` |
| Git log blob | `29cfc34fe9e3522dd0aeab7421e6f8559a7c1441` |
| Git metadata blob | `d720962b06c60a3f448350f283c89f27685377de` |

Restoring CRLF reproduces the published metadata size and SHA256 exactly.
Publication succeeded and added only latest.log and latest.json. This is not a
log transport failure. Exact Git copies are archived under
`docs/experiment-run-logs/c346/attempt-01/`. The original handoff is preserved
without alteration in `docs/handoff-history/c346-pre-recovery-r1.md`.
Preserve the user's native attempt folder and all accepted parent artifacts.

## 2. Failure phase

The six native cleanup checks passed with the immutable C344-R1 implementation
receipt bound to the C346 execution HEAD. Native lock probing, parent saved
semantics, 944-source / 9,177-input registration and the native objective preflight
also passed. The discarded preflight used five schedules, three zero-step optimizer
configurations, 24 forwards, 96 rows, 12 backwards and zero optimizer updates.

Full regression then failed in module index156:

```text
tests_lm.test_v05_c272_query_boundaries.C272Tests.test_24_manifest_seal_and_dispatcher_pins
```

| Regression extent | Count |
|---|---:|
| Registered tests / modules | 6,652 / 243 |
| Modules begun / successfully completed | 157 / 156 |
| Tests in completed modules | 3,669 |
| Failed-module tests / passes / failures | 24 / 23 / 1 |
| Total tests executed / passed | 3,693 / 3,692 |
| Failures / errors / skips | 1 / 0 / 0 |
| Tests / modules not reached | 2,959 / 86 |

All 157 started module inventories agree with the accepted parent prefix.
The failing module, regression process and science process each propagated exit1.
The final `C346 science failed;no automatic retry` and PowerShell line19 errors
are downstream reports of the regression assertion, not its initiating cause.

No formal C346 model fitting, optimizer update or cohort evaluation began.
The final saved reconstruction, all-input uncached rechecks and fresh verifier
were not reached. Native preflight and historical regression fixture computation
are distinct from the registered 15-model scientific work.

## 3. Root cause and authoring omission

The initiating assertion at C272 test source line267 is:

```python
self.assertIn(b.MANIFEST_SHA, handoff)
```

The preceding assertion against the immutable C272 preregistration passed.
The current handoff omitted the historical C272 seal:

```text
89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
```

This seal agrees with the accepted C272 benchmark, preregistration and acceptance
addendum. It remained in the handoff at C345 execution/publication and was first
omitted by the C345 acceptance rewrite
`f5fc8e89b5bb3d2749df91aa3b503596a6be1fc2`. The accepted C272 test did not change.
The C346 activation retained that omission.

The prior C346 author checks really passed all74 OWN tests and verified the actual
regression inventory; the independent review really checked the seven OWN files.
Those checks did not execute the inherited handoff consumers against the final
rewritten activation document. This was an authoring/review coverage failure.
The earlier review's PASS must not be interpreted as full historical-regression
or final-document compatibility verification.

## 4. Minimal recovery and policy basis

Restore the exact historical seal under **Inherited regression compatibility
seals**, outside **Formal state**. Explain why that section is append-only and
must survive future handoff rewrites. Do not edit scientific code, tests,
launchers, preregistration, accepted parent files or test selection.

This is a specifically documented stable historical invariant:

- `docs/experiment-ledger-addendum-c273-preflight-recovery.md` records the same
  earlier omission and requires permanent retention while the pinned C272 test
  remains, without an additional regression exclusion.
- `docs/experiment-authoring-runtime-gate.md`, **Mutable handoff lifecycle rule**,
  explicitly names this C272 seal and the append-only compatibility section.
- The accepted C274 and C278 preregistrations repeat the append-only requirement.
- C273's test distinguishes this legacy seal from its own lifecycle-dependent
  ACTIVE/acceptance-addendum seal.

The general prohibition on fixing mutable current ACTIVE numbers, branch tips
or latest-log commits does not make this defined immutable provenance marker
mutable. Restoring the correct previously retained fact satisfies the existing
compatibility contract. No historical assertion is weakened or suppressed.
The existing exact C204 mutable-ACTIVE exclusion remains the only exclusion.

## 5. Affected consumer checks and final-document boundary

The missing seal affects all seven cases below, not only the first reached C272
case. Execute the unchanged tests against the repaired actual handoff:

```text
tests_lm.test_v05_c272_query_boundaries.C272Tests.test_24_manifest_seal_and_dispatcher_pins
tests_lm.test_v05_c273_dual_boundary_attention.C273Tests.test_24_manifest_seal_and_dispatcher_pins
tests_lm.test_v05_c274_directional_boundary_diagnostic.C274Tests.test_24_manifest_lifecycle_and_legacy_compatibility
tests_lm.test_v05_c275_saved_gate_failure_audit.C275Tests.test_24_manifest_lifecycle_and_legacy_compatibility
tests_lm.test_v05_c276_final_boundary_lr_reliability.C276Tests.test_24_manifest_lifecycle_and_legacy_compatibility
tests_lm.test_v05_c277_saved_lr_failure_profile_audit.C277Tests.test_24_manifest_lifecycle_and_legacy_compatibility
tests_lm.test_v05_c278_mean_final_dual_query.C278Tests.test_24_manifest_lifecycle_and_legacy_compatibility
```

Also execute the four adjacent lifecycle-aware consumers:

```text
tests_lm.test_v05_c279_saved_dual_failure_profile_audit.C279Tests.test_24_manifest_lifecycle_and_legacy_compatibility
tests_lm.test_v05_c280_evidence_only_dual_memory.C280Tests.test_24_manifest_lifecycle_and_legacy_compatibility
tests_lm.test_v05_c281_saved_support_transition_audit.C281Tests.test_32_lifecycle_seal_and_own_test_inventory
tests_lm.test_v05_c282_mixed_length_training.C282Tests.test_32_lifecycle_and_own_test_inventory
```

The inherited-reference audit found C204 as the pre-existing excluded mutable
ACTIVE assertion; live handoff consumers C272..C282; and later C325..C346 guard
tests using synthetic Git/handoff fixtures. Keep that classification explicit.
Resolve current operational state separately: exactly C346 ACTIVE in Formal state,
state INVALID ATTEMPT RECOVERY, C347 not registered, no automatic retry.

After the documentation-only activation edit, repeat these11 actual consumers
and unique-ACTIVE resolution on those final bytes. A review of pre-activation
text alone is insufficient. Future acceptance/activation handoff rewrites must
preserve this compatibility section and check the inherited consumers.

## 6. Preserved scientific and execution contracts

All seven C346 OWN files remain byte-identical to source registration
`be76c4c53c36105638e59e059af241078758b628`:

| Path | Git blob |
|---|---|
| `fold_lm/v05_benchmarks/model_c346_pair_max_rate.py` | `684970a7a1d073f22422cb46f7f1514802af832e` |
| `tools/c346_execution.py` | `7950248a3d9acd9e8eb8c7da48b1b707ea478d85` |
| `tests_lm/test_v05_c346_pair_max_rate.py` | `2363e5ea696c2bef28bb2d173907f7ae5d9e331c` |
| `tests_lm/test_v05_c346_execution.py` | `4cc5791bb81f6d261591243f9498cae5cdb00a94` |
| `tools/run_c346.ps1` | `01f631a6195c6a597e3c20a682fa5bb4ef7de657` |
| `tools/invoke_c346.ps1` | `1c0464aac7be79ae0d0c122cca8365e4feb04de0` |
| `docs/experiment-ledger-addendum-c346-preregistration.md` | `994b35c0549b85ebbf504b179cf2aae48c21e33a` |

Manifest: `8dad5562249bf21517bb8487c5c6970ac75b55405252dbbf5c3512d797d46d64`.
Execution revision remains C346-R0, cleanup implementation C344-R1. The new retry
execution HEAD identifies changed documentation; no nonexistent R1 executable
or revised manifest is introduced.

Actual inventory remains 6,653 raw / 6,652 selected / 243 modules;
OWN74 =48 science +26 infrastructure. C345's6,578 IDs remain the identical ordered
prefix. Full ordered-ID SHA256:
`39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394`.
Parent ordered-ID SHA256:
`2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a`.

Retain seeds346001..346005 and orders346101..346105, all three arms, identical
initializations/input streams, unscaled pair-max objective, original rates and
fixed half rates, 2,400 updates per model, architecture, data, CPU float64/two
threads, optimizer/clipping and all fixed gate conditions. All15 fits precede
evaluation. No scientific threshold, cohort, comparator or work budget changes.

Protection remains 944 sources / 9,177 inputs. Scientific WORK remains15 models,
36,000 updates, 1,728,000 training rows, 41,130 model forwards and the other sealed
counters. Native cleanup and objective preflights, complete isolated regression,
saved reconstruction, final uncached rereads and fresh verification remain required.
Do not reuse partial attempt01 successes to shorten the formal retry.

## 7. Review, retry and stop

Before issuing a retry command, independently retrieve the committed recovery
documents through EOF; verify exact archives, seven unchanged OWN blobs, manifest,
actual full ID inventory and all11 consumer checks. Record the review target and
results in `docs/c346-r1-post-authoring-review.md`. Then make the documentation-only
activation and verify its final handoff bytes again.

The Linux author environment is Python3.12.14 / Torch2.10.0+cpu / NumPy2.3.5.
Focused author checks establish document compatibility, not native Windows or
full6,652-test completion. The unchanged sources' previous74-test ordinary and
CP932-default-open PASS reports remain historical; this recovery does not claim
to have repeated those unchanged suites unless separately recorded.

Use `invoke_active_v2 -> invoke_c346 -> run_c346` on `feat/sft-target-loss`, with
the later reviewed recovery activation HEAD. Preserve the existing native
`.venv-py31315` environment and user-local artifacts. Parse the dispatcher in the
short retry block; its existing path parses the selected launcher and runner.
The old failed execution HEAD, log commit, source commit and main merge are not
the new retry ExpectedHead.

Any execution-integrity failure stops SAME C346. No automatic retry, C347
registration or scientific conclusion follows from this failed attempt.
If only log transport later fails, repair publication without retraining.
