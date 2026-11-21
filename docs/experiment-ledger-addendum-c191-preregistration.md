# C191 preregistration — third acquisition budget boundary

**C190 ACCEPTED PASS. C191 ACTIVE / NOT YET JUDGED. C192 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

With the original C190 internal budget **12 unchanged**, can post2 NEEDS episodes:
1. expose the same frozen C188 target head at phase2,
2. acquire the one remaining unobserved fact through unchanged C172/C173,
3. consume the remaining three internal units exactly,
4. and refuse a fourth learned decision because internal budget reaches zero?

This is a runtime-horizon/budget boundary, not a new target-ranking test.

## Changed variable

C190 acquisition horizon: max2 -> max3.

## Held constant

- C181 base seeds181001/2/3
- C188 head seeds188001/2/3
- all9 selector combinations
- internal budget12 / acquisitions4 / step7
- C174 development cohort
- same 9536 coherent worlds per selector /85824 episodes
- same 16 source snapshots
- C172/C173
- raw argmax
- initial exact-state memoization
- no training / no fresh seed / no production runtime modification

## Parent replay

C191 must replay accepted C190 before the new third action:
- phase0 necessity+target exact
- phase1 necessity+target exact
- phase2 necessity exact
- initial logit deltas <=1e-6
- first/second live read counts remain consistent with accepted C190

## Third-step scope

Accepted C190 has exactly **928 post2 NEEDS episodes per selector** =8352 total.
These originate from initial missing3 cases; after two admissions exactly one fact is unobserved.
Therefore target2 has one legal unknown after masking. A correct target2 is required, but this
is **not evidence of ranking among alternative third targets**.

## Resource path

```text
start                 12 internal /4 acquisitions /step7
decision0             11 /4 /8
acq1 + decision1       7 /3 /12
acq2 + decision2       3 /2 /16
acq3                    0 /1 /19
fourth decision         REFUSED
```

No post3 learned necessity decision is allowed in C191.

Scoring-only logical teacher must say the fully observed final state is SUFFICIENT.

## Fixed gate — all 9 blocks

Per selector:
- episodes9536
- parent_final_needs928
- phase0 replay errors0
- phase1 replay errors0
- phase2 necessity replay errors0
- target2 errors0
- selected observed0
- repeated target0/1 =0
- third acquisition errors0
- third reservations/provider calls/publications =928
- final logical NEEDS=0
- fourth decision accepted=0
- contract errors0
- actual reads =9536 + accepted C190 second reads +928
- initial replay logit deltas <=1e-6

All9 must pass.

Finite completed scientific miss => ACCEPTED VALID NEGATIVE.
Source/hash/schema/replay/nonfinite/incomplete/protection issue => INVALID / RETRY SAME C191.

## Workload

- 85824 logical episodes /9 blocks
- expected third acquisitions8352
- 15912 unique initial policy rows
- max3 acquisitions
- learned decisions max3
- no post3 learned decision
- no network / answer / proof / core evidence writes
- production runtime modifiedFalse
- Gate E candidateFalse
- expected regression **1509 =1485 existing +24 new;76 modules**
- historical source pins116
- protected paths304
- artifacts21 excluding summary

Scientific manifest SHA256:
`8cf89274974a4204156c2cb2eb1f87d101f8ab09b320dd7e649a4380ddb852f1`.

PASS claim boundary:
bounded third real acquisition + exact budget exhaustion under unchanged resources.
It does not establish final learned post3 reclassification, arbitrary loops, tool/provider learning,
independent final holdout, language, answer/proof, production adoption or Gate E completion.
