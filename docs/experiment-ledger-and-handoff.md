# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> and post-authoring review pass apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C202 ACCEPTED PASS. C203 ACTIVE / NOT YET JUDGED. C204 NOT REGISTERED.**

## Accepted C202

Scientific execution HEAD:
`a140f33b02aa4056b7c1fcff9041b09f9b7342c4`

Published log commit:
`bdf66220a633c8e3f261e09b7491369aec7f1994`

Log SHA256:
`b8b3e1f8663f606e1518be448983bc7855d656b265e228dc0dd23726cb37c640`

Summary SHA256:
`b568d8b652802c16fb75b85416c6d4ed956abcf767164d688ee39be1178e8c82`

C202 deciding result:
- focused regression **1785/1785**
- dispatch cases257472
- 27/27 block/channel records failed0
- provider calls257472
- publications257472
- receipts257472
- RETRIEVE/OBSERVE/ASK_USER provider calls85824 each
- route/action/dispatch/channel/receipt/value/mutation/resource errors0
- candidate_gate_passed True
- run_execution_valid True
- training/learned-forward/network0
- production runtime modified False

Accepted claim: each accepted learned target can execute through its exactly-one typed channel using
the real structured acquisition lifecycle, with matching-provider isolation and exact selected-fact
publication/resource semantics.

## Active C203

Experiment:
`C203-v5e-mixed-channel-multistep-replay`

Stage:
`V5-E-MIXED-CHANNEL-MULTISTEP-REPLAY`

One question:
can the accepted C199 ALLOWED multi-step necessity/target trace be replayed exactly while
fact-specific channel assignments switch within an episode, with correct channel dispatch,
fact/value publication, parent resource accounting and final SUFFICIENT closure?

Fixed layout:
```text
fact0 RETRIEVE
fact1 OBSERVE
fact2 ASK_USER
fact3 RETRIEVE
```

Fixed parent totals:
- episodes85824
- decisions214948
- acquisitions129124
- final SUFFICIENT85824

The exact channel call totals and within-episode switch count are a deterministic projection of
the frozen C199 prediction artifact through the fixed layout.

Decision/action separation:
- before each replayed decision: parent RETRIEVE-only authority masks;
- after NEEDS+target: temporarily all three runtime channels enabled;
- C201 mapper + existing runtime/lifecycle dispatch;
- parent masks restored before the next replayed decision.

Scope:
- training0
- fresh seeds0
- learned forward calls0
- network0
- production runtime modifiedFalse
- Gate E candidateFalse

Authoring:
- expected regression **1813 =1785+28**
- expected modules **88**
- source pins31
- protected inputs53
- artifacts5
- manifest
  `2b9723733441019df8d73fa40fcf1421023c4765cbe6fdc91a31b2765b447ae6`

## Post-authoring review

**post_authoring_review = PASS**

implementation review HEAD:
`869ab03706db9b97119d61cf10f5f8ca1aaa40de`

The review re-fetched committed remote bytes and checked benchmark/tests/runner/launcher/
preregistration/docs, accepted C202/C199 identities, C174 summary/pilot-data and C199 prediction
artifact contracts, 28-test definition count, 88-module/1813-test runner contract, 31 source pins /
53 protected inputs, manifest identity, py_compile inputs, all launcher parent paths,
decision/action authority ordering, provider-channel isolation, fact/resource postconditions,
stale C-number/HEAD/path residue and C204 non-registration.

## Stop condition

Judge C203 before any C204 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/import/regression/incomplete/protection failure -> INVALID / RETRY SAME C203.

Gate E remains NOT PASSED.
