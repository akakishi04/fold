# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, parent artifact semantic audit, and historical
> regression immutability apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C205 ACCEPTED PASS. C206 ACTIVE / INVALID ATTEMPT RECOVERY. C207 NOT REGISTERED.**

## Accepted C205

Scientific execution HEAD:
`c78b79e95b92552c032df05220868122398fd339`

Published log commit:
`fd05da86e40e81feb96a3e7b6011e9d229299176`

Log SHA256:
`1dd3973c15013fb95296fda482eebe52298377c56eee3a9a50c7c3b0ee260427`

Summary SHA256:
`2f60e87aa7158bf22e1a4f6b15904a4e66096a1db81a6477e0b398be87fc3c2b`

C205 deciding result:
- focused regression **1871/1871**
-9/9 attribution blocks complete
- canonical unique rows15912, forward18, cell126
- canonical max necessity/target logit delta **0.0 / 0.0**
- expanded direct rows85824, forward90, cell630
- expanded max necessity/target logit delta
  **5.0067901611328125e-06 / 5.7220458984375e-06**
- max C204 block-max match error **0.0 / 0.0**
- candidate_gate_passed True
- run_execution_valid True
- production runtime modified False

Accepted claim: C204's gate-breaking numeric replay maxima are fully reproduced by phase0
duplicate-expanded batching; canonical unique structured-v2 inference reproduces C199 exactly.
C204 remains ACCEPTED VALID NEGATIVE under its original whole-run1e-6 gate.

## Active C206

Experiment:
`C206-v5e-terminal-derived-result-integration`

Stage:
`V5-E-TERMINAL-DERIVED-RESULT-INTEGRATION`

One question:
can every accepted mixed-channel terminal SUFFICIENT state emit a production
`VERIFIED_DERIVED` Boolean conclusion bound to exactly its observed supporting references,
without mutating observations/resources, while the opposite conclusion is rejected?

Behavior held:
- accepted C199 ALLOWED decision trace;
- C203 fixed fact->channel mapping;
- C201 mapper;
- C202/C173 acquisition lifecycle;
- exact C203/C204 decision/acquisition/channel totals.

Output separation:
- C171 `proof_fixture` is benchmark-only reference candidate production;
- C171 `completion_values` is evaluator-only semantic oracle;
- production `structured_derived_result.verify` is the deciding verifier;
- derived result must remain distinct from OBSERVED fact state.

Registered totals:

```text
episodes              85824
decisions            214948
acquisitions         129124
terminal SUFFICIENT   85824
verified DERIVED      85824
opposite rejected     85824
verifier calls       171648

RETRIEVE               88918
OBSERVE                 21252
ASK_USER                18954
channel switches         32564
```

Required errors:
- semantic unresolved0
- world value0
- verification0
- opposite rejection0
- support0
- mutation0
- derived schema0
- acquisition/runtime/projection0

Scope:
- training0
- fresh seeds0
- learned forward0
- network0
- production runtime modifiedFalse
- Gate E candidateFalse
- not learned proof or language answer generation

Authoring:
- source pins56
- protected inputs110
- artifacts5
- new tests30
- regression modules91
- focused regression1901
- manifest
  `4841fda580c84bc66fb66f2fb123d08ec0dd7feedf29ab2aecbf85954970ac51`

Historical mutable-state regression exclusion remains the one exact accepted C204 test ID.
Accepted C204 bytes remain unchanged.

## Invalid C206 attempt

Execution HEAD:
`95d087011a7071ad920b9ab1620706b9e0b74205`

Published log commit:
`922b51eaaf5dfbace77644d658bd4f17dab71218`

Log SHA256:
`3a3d8be20e2eec475b8512a5f284bec75d5c0708b7e9f04ff5606b13506a590f`

- focused regression1901;
-1900 PASS /1 FAIL;
- all scientific preconditions passed;
- failing test was C206 test25 with stale source-string count literals 1900/1899;
- implementation and runner already used1902 loaded /1901 kept;
- scientific diagnostic did not start;
- run_execution_valid False.

Recovery:
- test25 now builds the actual module loader/suite and semantically checks1902 candidate IDs ->1901 kept;
- exact historical exclusion still occurs once;
- scientific question/workload/verifier/output gate unchanged.

## Second invalid C206 attempt

Execution HEAD:
`ffaac098988476d2db483005d487bddd02102f32`

Published log commit:
`98fb270d0dc43bf4a7c2689e985748a5c86a3196`

Log SHA256:
`f9ee35e596e7e35d2340c977f0035955da188e1b404ae5a16e1d5de6dc98c77a`

- focused regression1901;
-1900 PASS /1 ERROR;
- failing test was C206 test25;
- error: `NameError: name 'c205' is not defined`;
- scientific diagnostic did not start;
- run_execution_valid False.

Recovery:
- test25 now uses `c206.c205`, the parent module binding already imported by C206;
- test25 additionally AST-audits bare `c###.` module aliases against module-level imports;
- no scientific condition changed.

## Post-authoring review

**post_authoring_review = PASS**

second-recovery review HEAD:
`fbdac7b62a8fc607031d006002ec299c1c3bc783`

Committed remote review verified:
- test25 uses `c206.c205` and has no bare unimported C205 alias;
- test25 AST-audits executable `c###.` references against module imports;
- cross-file alias audit found zero unbound executable aliases in C206 benchmark/tests;
- actual suite accounting remains1902 loaded /1901 kept;
- one exact historical exclusion remains unchanged;
- accepted C205/C171 identities and C206 scientific manifest are unchanged;
- source pins56 / protected inputs110;
- dispatcher -> C206 launcher -> C206 runner parser chain intact;
- C207 remains unregistered.

## Stop condition

Judge C206 before any C207 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/C171-history/regression/incomplete/protection failure
  -> INVALID / RETRY SAME C206.

Gate E remains NOT PASSED.
