# C205 execution recovery — mutable historical active-state regression

## Disposition

**C205 — INVALID EXECUTION / RETRY SAME C205.**
**C206 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

Invalid execution:
- execution HEAD: `37509d34e1ccfc8abf3e92fca708327a5335e4ea`
- published log commit: `81346818971e8586dbd1629563f76a847c6e279a`
- log SHA256: `e98725bfd5c20b9e612f3640cf931f86beb5c00618f1e92b1c9e77a5d10d420b`
- focused regression: **1871 tests, 1870 PASS /1 FAIL**
- scientific diagnostic: **not started**
- run_execution_valid: False

## Failure

The only failing test was the accepted C204 operational test:

`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`

It asserted that the mutable authoritative handoff currently resolves:

```text
C204
```

After formally accepting C204 and activating C205, the correct current value became:

```text
C205
```

Therefore the historical test failed with:

```text
['205'] != ['204']
```

All25 original C205 tests passed.

## Root cause

The C204 test was not a stable historical regression. It coupled an accepted experiment's test
expectation to mutable repository control state (`docs/experiment-ledger-and-handoff.md`).

The test was correct only while C204 itself was ACTIVE. Once the experiment advanced, the test was
guaranteed to fail even though no C204 scientific behavior regressed.

Accepted C204 source/test bytes must remain unchanged because C205 pins their accepted identities.
Editing the historical C204 test would destroy evidence identity.

## Minimal recovery

Do not modify accepted C204 source/tests.

Starting at C205, focused regression uses an explicit immutable suite:

- load the inherited90 modules plus C205;
- require the historical dynamic test exact ID to occur exactly once;
- exclude exactly that one test ID;
- retain every other historical test;
- add a C205 immutable replacement test that verifies the exclusion contract itself;
- keep total executed regression count at **1871**.

Accounting:

```text
1846 inherited C204 tests
-   1 mutable current-ACTIVE test
+  26 C205 tests
=1871 focused regression tests
```

The excluded exact ID is:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

No wildcard/name-prefix filtering is allowed.

## Process correction

Historical regression tests must be **time-invariant after acceptance**.

They must not assert mutable repository-control values such as:
- current ACTIVE experiment number;
- current remote HEAD;
- current handoff text whose value intentionally advances;
- current branch-tip log commit.

Such behavior belongs to:
- active launcher preflight;
- current experiment post-authoring review;
- synthetic fixture tests whose expected value is embedded in the fixture.

If an already-accepted historical test violates this rule, child experiments may exclude only its
exact preregistered test ID and must replace its intended invariant with an immutable child-side test.
The accepted parent file itself remains untouched.

C205 scientific question,1e-6 tolerance, cohort, checkpoints, workload and attribution gate are
unchanged.
