# C206 preregistration — terminal derived-result integration

**C205 ACCEPTED PASS. C206 ACTIVE / NOT YET JUDGED. C207 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

After reconstructing the accepted mixed-channel terminal SUFFICIENT states, can every terminal
Boolean conclusion be emitted through the production `structured_derived_result.verify` contract
as `VERIFIED_DERIVED`, bound to exactly the actually observed supporting references, while
verification leaves observations/resources unchanged and rejects the opposite conclusion?

This is an output-contract integration prerequisite. It is **not learned proof generation**.

## Accepted parent

C205:
- execution HEAD:
  `c78b79e95b92552c032df05220868122398fd339`
- summary SHA256:
  `2f60e87aa7158bf22e1a4f6b15904a4e66096a1db81a6477e0b398be87fc3c2b`
- status:
  **ACCEPTED PASS**

Behavioral trajectory is held to the accepted C199 ALLOWED saved necessity/target trace.
C204 established that its live frozen argmax trajectory is behaviorally identical.

## Fixed runtime reconstruction

For all9 blocks /85824 episodes:

```text
accepted saved decision trace
-> C203 fixed fact->channel layout
-> C201 mapper
-> C202/C173 acquisition lifecycle
-> terminal SUFFICIENT TaskView
```

Required runtime totals remain:

```text
episodes              85824
decisions            214948
acquisitions         129124
terminal SUFFICIENT   85824

RETRIEVE               88918
OBSERVE                 21252
ASK_USER                18954
channel switches         32564
```

No learned forward occurs in C206.

## Derived-result producer/checker separation

Candidate producer:
- C171 benchmark-only `proof_fixture`;
- evaluator/reference code only;
- not production answer logic;
- not learned reasoning.

Semantic oracle:
- C171 independent exhaustive `completion_values`;
- evaluator-only;
- must return exactly one possible terminal conclusion.

Deciding checker:
- production `fold_lm.v05.structured_derived_result.verify`.

C206 protects the accepted C171 production/verifier fixture source identities through the hashes
already protected by accepted C199.

## Correct terminal candidate

At every terminal state:

1. `completion_values(view)` must contain exactly one bit;
2. that bit must equal the actual coherent-world root value;
3. C171 proof fixture may use only current OBSERVED facts with their exact current reference IDs;
4. production verifier must emit:

```text
schema            fold-structured-derived-result-v1
status            VERIFIED_DERIVED
reason            VALID_LOCAL_PROOF
derivation_kind   BOOLEAN_LOCAL_PROOF
value             exact semantic conclusion
support/proof     exact candidate support/proof
checked_steps     1..7
```

Required correct verifications:

```text
85824 / 85824
```

## Opposite-value negative control

For every terminal state, bind the opposite conclusion while keeping the same proof/support.

Production verifier must return:

```text
status                  REJECTED
value                   None
supporting_references   ()
proof                   ()
```

Required opposite controls:

```text
85824 / 85824 rejected
```

Total verifier calls:

```text
171648
```

## Observation / resource boundary

Before and after correct + opposite verification, the trusted terminal TaskView must remain
byte-for-byte unchanged.

Verification must not:
- change fact status/value/reference IDs;
- create an OBSERVED result;
- debit/replenish internal or acquisition resources;
- create pending intents/receipts;
- commit the logical conclusion into evidence.

Derived conclusion remains a separate `DerivedResult`.

## Fixed PASS gate

Global:

```text
episodes                   85824
decisions                 214948
acquisitions              129124
terminal_sufficient        85824
verified_derived           85824
opposite_rejected          85824
verifier_calls            171648

RETRIEVE                    88918
OBSERVE                      21252
ASK_USER                     18954
channel_switches              32564

support_min >= 1
support_max <= 4
checked_steps in [85824, 85824*7]

all scientific/runtime/verification errors 0
projection_errors 0
```

Each of9 block records requires:
- episodes9536;
- terminal_sufficient9536;
- verified_derived9536;
- opposite_rejected9536;
- verifier_calls19072;
- failed0;
- projection_error0;
- support count range1..4.

A valid complete miss is **ACCEPTED VALID NEGATIVE**.

Source/hash/schema/parent-artifact/C171-history/regression/incomplete/protection failure is
**INVALID EXECUTION / RETRY SAME C206**.

## Scope / non-claims

C206 registers:
- training0;
- fresh seeds0;
- learned forward calls0;
- network calls0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

PASS establishes only terminal state -> bounded derived-result contract integration.

PASS does not establish:
- learned proof generation;
- natural-language answer generation;
- learned channel preference;
- independent holdout;
- final Gate E completion.

## Historical regression immutability

Inherited historical dynamic test exclusion remains exactly:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

The accepted C204 file remains unchanged.

Regression accounting:

```text
1902 loaded candidates
-1 exact historical mutable-state test
=1901 executed focused regression tests
```

## Authoring quality gate

C206 OWN:
- `fold_lm/v05_benchmarks/gate_e_c206_terminal_derived_result_integration.py`
- `tests_lm/test_v05_c206_terminal_derived_result_integration.py`
- `tools/run_c206.ps1`
- `tools/invoke_c206.ps1`
- this preregistration;
- `docs/terminal-derived-result-integration-v0.1.md`

Expected:
- source pins56;
- protected inputs110;
- output artifacts5;
- new tests30;
- focused regression **1901**;
- regression modules **91**.

Scientific manifest SHA256:

`4841fda580c84bc66fb66f2fb123d08ec0dd7feedf29ab2aecbf85954970ac51`

## Post-authoring review requirement

Before execution, committed remote bytes must be independently reviewed for:
- accepted C205 summary/source identity;
- accepted C171 historical hashes from C199 protected inputs;
- benchmark-only proof producer vs production verifier separation;
- independent completion oracle and coherent-world comparison;
- correct/opposite verifier contracts;
- no TaskView/resource mutation;
- exact mixed-channel replay totals;
- historical dynamic test exact-ID exclusion;
- all source-string assertions against exact target functions;
- PowerShell launcher + runner parser chain;
- source/protected/test/module/artifact counts;
- C207 non-registration.

Until review passes:

`post_authoring_review = PENDING`

The first C206 attempt was INVALID in regression because test25 still source-string-asserted stale
1900/1899 suite literals after two launcher-safety tests had raised the real counts to1902/1901.
The scientific code and runner counts were already correct. test25 now constructs and counts the
actual suites semantically. Revised committed bytes must be independently reviewed before retry.

## Execution / stop

User-facing execution uses `tools/invoke_active.ps1`.

Expected progress:
- active_experiment = C206
- C206 repository preflight
- Python syntax preflight
- source/artifact precheck PASS
- focused regression1901/1901
-9 block progress records
- RESULT
- POSTCHECK
- remote log publication

Judge C206 before any C207 registration.
