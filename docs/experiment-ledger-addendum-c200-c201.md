# C200 acceptance / C201 handoff

## Formal judgment

**C200 — ACCEPTED PASS.**
**C201 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful C200 recovery run:
- scientific execution HEAD: `11181a355f13e7be2fda3957b9cdd45ad8868316`
- published log commit: `2694d336c11b2f98d5e9f89ed5442d445ac1d45e`
- log SHA256: `75b48cc324db807542b0cd03a65ac182c40ca6113fcf9ddd77303db958eba04d`
- log bytes: 279171
- summary: `runs/c200-v5e-acquisition-channel-input-d892b01c24ee49cfbb87758e7a208be0/summary.json`
- summary SHA256: `624889546c9b484003e3f2bc79c1d746de28ea168def13da1a2dc87fde73520e`
- focused regression: **1731/1731** in 52.055s
- source/artifact precheck PASS
- Python syntax preflight PASS
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False; Gate E candidate False

The earlier C200 attempt at execution HEAD
`4334bf492fe4d98e22165bb785edf3bcc9def254`
remains **INVALID EXECUTION / RETRY SAME C200** evidence only. It stopped in regression before
the scientific diagnostic because a source-text import guard matched a docstring mention.
The accepted recovery changes only that test to inspect actual AST import nodes.

## Deciding evidence

C200 satisfied every preregistered input-contract endpoint:

- channel-mask roundtrips: **32 / 32**
- runtime authority cross: **448 / 448**
- hidden-completion pairs: **12 / 12**
- malformed cases rejected: **18 / 18**
- roundtrip failures:0
- runtime-cross failures:0
- hidden packet mismatches:0
- answer-changing hidden pairs:6
- v1 feature width:72
- v2 feature width:84
- exact v1 prefix preservation:True
- all8 channel masks representable
- candidate_gate_passed True

No training, learned forward, provider/tool call, network call or evidence write occurred.

## Scientific interpretation

C200 establishes a strict opt-in structured-task-input-v2 contract whose first72 features are
the exact canonical v1 policy packet and whose final12 bits expose per-fact semantic acquisition
eligibility for RETRIEVE / OBSERVE / ASK_USER.

The new channel metadata remains separate from runtime availability/permission. Hidden fact
completion can change the evaluator answer while the v2 packet remains identical, so C200 does
not encode hidden values through the new channel fields.

## Non-claims

C200 does not establish:
- learned or automatic acquisition-channel selection;
- execution of RETRIEVE / OBSERVE / ASK_USER;
- quality of a mixed three-channel policy;
- Gate E nine-family quality;
- final Gate E completion.

## Next boundary

The next smallest blocker is no longer input visibility; it is **selected-fact -> typed action
routing**.

C201 should use the already accepted learned fact target and v2 channel metadata, without new
training, to test an explicit reference mapper:

```text
learned selected fact
-> inspect that fact's declared one-hot channel
-> typed ActionProposal(RETRIEVE / OBSERVE / ASK_USER, same fact_index)
-> unchanged trusted runtime reauthorization
```

C201 must distinguish semantic channel eligibility from runtime availability/permission:
a declared channel selects the proposed action, but a denied/unavailable runtime still blocks
execution normally.

Use one-hot channel eligibility only in C201. Multi-eligible preference learning remains a
separate future question.

C201 is an integration/reference-path diagnostic, not a learned tool-choice claim.
