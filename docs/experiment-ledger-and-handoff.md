# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, parent artifact semantic audit, historical
> regression immutability, semantic count contracts, and Python import-binding audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C209 ACCEPTED PASS. C210 ACTIVE / INVALID ATTEMPT RECOVERY. C211 NOT REGISTERED.**

## Accepted C209

Scientific execution HEAD:
`a9e4bdae10b574eb5fd66f4a3dc027bab5a18194`

Published log commit:
`dae623b349a12764c7ee4705ee2a32adddf8b59c`

Log SHA256:
`778e8d87a20afbdb488c169c8acb73b0876fbd34e7b6cc9cb4940c286c898d41`

Summary SHA256:
`49476c781212f87a2782fdb6b042582dcd18941642b452855bb92690f90facc3`

C209 deciding result:
- focused regression **1973/1973**
- episodes144
- original fact counts1->16 /2->112 /4->16
- dummy TRUE facts272
- status normalizations32
- exhaustive semantic assignments736
- semantic errors0
- source unchanged144
- mapping valid144
- dummy-missing errors0
- C178 necessity-compatible144
- C188 target-compatible144
- combined-compatible144
- equal source units50 / equal projected units50
- pair projection errors0
- candidate_gate_passed True
- run_execution_valid True

Accepted claim: the visible-only candidate projection makes all fixed C207 development packets legal
for the frozen C181/C188 input contract while preserving Boolean semantics, original fact indices and
trusted runtime/evidence state.

## Active C210

Experiment:
`C210-v5e-baseline-development-measurement`

Stage:
`V5-E-BASELINE-DEVELOPMENT-MEASUREMENT`

One question:
what raw matched development performance/cost measurements are produced by the9 projected frozen
candidate model pairs, INTERNAL_ONLY and FIXED_ACQUISITION on the same frozen144 C207 episodes under
the same runtime and answer boundary?

Frozen data:
- visible `c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543`
- scorer `0591682848a69ac020a0f4a7bb2939e6df79ffd116567fe3c994a5f8e3fa3912`

Policy identities:
- INTERNAL_ONLY
- FIXED_ACQUISITION
- all9 C181/C188 base/head combinations

Total registered policy-episode evaluations:

```text
1584
```

Shared answer boundary for all policies:
- C171 completion_values;
- C171 benchmark proof_fixture;
- production structured_derived_result.verify.

This symbolic shared boundary is disclosed and is not claimed as learned FOLD reasoning.

Registered harness controls:

```text
INTERNAL_ONLY:
correct48 / answered48 / unresolved96
attempts0 / provider calls0 / publications0 / user turns0

FIXED_ACQUISITION:
correct128 / answered128 / unresolved16
attempts96 / provider calls90 / publications80 / user turns16
authority violations0 / malformed publications0
```

Candidate:
- C209 projection for learned input only;
- original C207 v2 TaskView remains trusted runtime;
- frozen combined necessity/target initial inference;
- at most one actual acquisition attempt;
- after successful publication, one live frozen necessity reclassification;
- emit only after learned SUFFICIENT plus shared resolver verification;
- no retry after denied/failed acquisition.

C210 measures raw per-policy/per-family:
- resolution/correctness/coverage/abstention;
- acquisition/provider/publication/user-turn counts;
- unnecessary/missed acquisition;
- authority/malformed evidence boundaries;
- verifier and internal costs;
- candidate learned stop/target diagnostics;
- frozen inference workload.

C210 performance is **not** a PASS criterion.

Measurement-completeness gate only:
-11 policy identities;
-144 episodes per policy;
-1584 episode records;
-9 candidate model identities;
- exact fixed/internal harness-control totals;
- guarded unsupported assertions0;
- authority violations0;
- malformed publications0;
- candidate initial inference rows144 each;
- candidate total inference rows =144 + measured post rows.

Scope:
- numerical margin registrationFalse
- candidate selectionFalse
- independent holdout createdFalse
- training0
- fresh seeds0
- network0
- production runtime modifiedFalse
- Gate E candidateFalse

Authoring:
- source pins87
- protected inputs165
- artifacts5
- new tests24
- regression modules95
- focused regression1997
- manifest
  `09a7bbc84d37c93d6e559acffc8eaa0ff5c7f902271ebefff83b15363a10cb18`

## Invalid C210 attempt

Execution HEAD:
`633ce9bed165d30b0adb671c1faf12d34a9ad0cc`

Published log commit:
`482d36ca1563fc7379fa48c346e255a526a48cec`

Log SHA256:
`158e54bde84b156ebd665285ea85f32224dc943174ed9cc46997fd71753434fd`

The run completed1997/1997 regression tests and1584/1584 policy-episode measurements, but post-run
dependency coverage audit found that deciding candidate inference called C189
`combined_predict/necessity_predict` without C189 being present in the preregistered source/protected
set.

This is a source/protection failure, so the numeric result is not accepted scientific evidence.

Recovery:
- pin the complete deciding helper chain:
  - C175 `efd1bb246442fb4f472e33e450c16b192acfa18a`;
  - C179 `504c79b6a881c64dba2494ef6ad35bffd9099f5a`;
  - C182 `a5fb10af6238d425f82b093a0c3676d247b1f0e3`;
  - C189 `b34b40d84ab6597cc1cd26e47f64d58254d3304f`;
- source pins87;
- protected inputs165;
- scientific question/policies/checkpoints/fixtures/workload unchanged;
- retry same C210 only.

## Post-authoring review

**post_authoring_review = PASS**

recovery review HEAD:
`1c483c9999b800fe44c2fa580455b619516cc23e`

Committed remote review verified the complete deciding-path dependency chain and no further unpinned deciding helper remains. Scientific policy identities, checkpoints, fixtures, workload and measurement semantics are unchanged.

Re-review verified:
- deciding-path C175/C179/C182/C189 helper blobs are explicitly source-pinned;
- source/protected counts are87/165;
- every other C210 scientific condition remains unchanged;
- direct deciding-path repository dependencies are all source-pinned/protected;
- full144 baseline controls,9 candidate identities,1584 measurement accounting remain unchanged;
- semantic regression counts, Python alias bindings, PowerShell parser chain and runner CLI indexes
  remain valid;
- C211 remains unregistered.

## Stop condition

Judge C210 before any C211 registration.

- complete valid matched measurement -> ACCEPTED PASS;
- complete measured candidate quality may be poor and still remains valid C210 evidence;
- source/schema/hash/parent/regression/incomplete/protection failure -> INVALID / RETRY SAME C210.

Gate E remains NOT PASSED.
