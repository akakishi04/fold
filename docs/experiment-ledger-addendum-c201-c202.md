# C201 acceptance / C202 handoff

## Formal judgment

**C201 — ACCEPTED PASS.**
**C202 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful C201:
- scientific execution HEAD: `1ce0334e0d5ee76c7e5fac40082c19bd43576415`
- published log commit: `49a85f2e7cc7a2d4779d354c9adc7e064f61cbfb`
- log SHA256: `5e19cae5bbac7bd8be9ecb23fd0bf1bbd0e1f1fc3ee376ba5890ccef7c088835`
- log bytes: 286491
- summary: `runs/c201-v5e-selected-fact-channel-route-37e1d67baaff4cd7a67addeb75da0aca/summary.json`
- summary SHA256: `c27ff79f20811ce373d175617b2a556c3c847d631f096fb401cb0251ad4fca4c`
- focused regression: **1759/1759** in 56.174s
- source/artifact precheck PASS
- Python syntax preflight PASS
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False; Gate E candidate False

## Deciding evidence

C201 satisfied every preregistered route/authority endpoint:

- accepted learned target route cases: **257472**
- route records:108
- route mismatches:0
- RETRIEVE route cases85824
- OBSERVE route cases85824
- ASK_USER route cases85824
- authority cross12
- authority failures0
- PENDING/ACQUISITION_RESERVED3
- PERMISSION_DENIED6
- PROVIDER_UNAVAILABLE3
- already-observed controls3/3
- invalid mapper cases rejected7/7
- candidate_gate_passed True

No new training, learned forward, provider call, network call or evidence write occurred.

## Scientific interpretation

C201 establishes that an accepted learned fact target can be preserved exactly while the
fact's exactly-one structured-v2 channel metadata determines a typed RETRIEVE / OBSERVE /
ASK_USER ActionProposal. The mapper does not absorb runtime authority: permission,
availability and already-observed checks remain enforced by structured_action_runtime.step().

## Non-claims

C201 does not establish:
- actual provider execution for all three channels;
- channel-specific observation publication;
- learned preference among multiple eligible channels;
- mixed-family answer quality;
- final Gate E completion.

## Next boundary

C202 should keep the accepted C199 learned fact targets, C200 v2 channel metadata and C201 mapper
fixed and extend the path through the real structured acquisition lifecycle.

One scientific question:

> For each accepted learned target and each one-hot channel variant, does the typed proposal
> reserve and dispatch through only that matching RETRIEVE / OBSERVE / ASK_USER endpoint,
> publish exactly the selected fact's current world value, leave nonselected facts untouched,
> and finish with the exact bounded resource contract?

C202 should exercise all **85824 accepted targets x3 channels =257472 acquisitions**.

To isolate channel dispatch from learned target generation, use the already-saved C199 phase0
target artifact; no new target inference or training.

Each episode begins from a registered post-decision state with:
```text
internal_remaining      12
acquisitions_remaining  4
all three channels available/permitted
internal_step           8
evidence_time/revision  1/1
```

Expected one-acquisition final state:
```text
internal_remaining      9
acquisitions_remaining  3
last_outcome            NONE
internal_step           11
one receipt
selected fact OBSERVED with the registered world bit
all nonselected facts UNOBSERVED
```

C202 remains a reference integration diagnostic. It is not a learned channel-preference claim
and not a final Gate E run.
