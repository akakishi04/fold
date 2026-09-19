# C194 preregistration — generic bounded loop equivalence

**C193 ACCEPTED PASS. C194 ACTIVE / NOT YET JUDGED. C195 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can a single generic, state-driven bounded loop reproduce accepted C193 exactly without
hand-written phase1/phase2/phase3 orchestration branches?

This is a runtime-orchestration equivalence test, not a new model-capability test.

## Changed variable

Only the orchestration form changes:

```text
C193:
phase0 -> maybe acquire
phase1 -> maybe acquire
phase2 -> maybe acquire
phase3 -> final necessity

C194:
while unresolved:
    charge one decision
    inspect current state
    if any active row has an unobserved fact:
        frozen necessity + frozen target
    else:
        frozen necessity only
    SUFFICIENT -> stop
    NEEDS + legal target -> acquire -> re-enter
```

The loop bound is derived from `max_dispatches=3`: at most three acquisitions and therefore
at most four learned decisions. There is no phase-specific stopping branch.

## Held constant

- initial internal budget13
- same C174 PILOT NEEDS cohort
- same 1768 source rows ->9536 coherent worlds/selector
- all9 frozen C181 x C188 selector pairs
- same C172/C173 runtime
- same 16 protected coherent-world source snapshots
- same teachers and raw argmax
- same initial unique-state memoization
- no training/fresh seeds/production runtime changes

## Parent replay requirement

Accepted C193 is the reference behavior.

Per selector C194 must reproduce:
- all necessity predictions exactly
- all target predictions exactly
- active finite necessity/target logits within <=1e-6
- first/second/third read counts exactly
- final authoritative decision row count exactly
- total actual file reads exactly

C194 uses its own C193-artifact loader. Parent loader dispatch is source-level tested.

## Fixed gate — all 9 blocks

Per selector:
- episodes9536
- scientific necessity errors0
- target errors0
- selected observed0
- repeated target0
- acquisition errors0
- contract errors0
- final decision errors0
- parent replay errors0
- parent block mismatches0
- parent necessity prediction errors0
- parent target prediction errors0
- parent active logit deltas <=1e-6
- first reads9536
- 0 < third reads == final decision rows <= second reads <= first reads
- actual reads = first + second + third

All9 must pass.

A completed finite scientific mismatch is **ACCEPTED VALID NEGATIVE**.
Source/hash/schema/parent replay infrastructure/nonfinite/incomplete/protection failure is
**INVALID EXECUTION / RETRY SAME C194**.

## Interpretation

PASS means the accepted C193 behavior is not dependent on its manually unrolled phase
orchestration: the same frozen components and runtime close correctly through one generic
bounded decide/acquire/reobserve loop.

PASS does not mean:
- production runtime integration is complete;
- arbitrary/unbounded loops are safe;
- resource policy is learned;
- tool/provider choice is learned;
- independent holdout/generalization is established;
- answer/proof or Gate E is complete.

## Workload

- 85824 episodes /9 blocks
- max3 acquisitions /max4 learned decisions
- artifacts5 excluding summary
- source pins131
- protected paths352
- expected regression **1581 =1557 existing +24 new**
- expected modules79
- production runtime modifiedFalse
- Gate E candidateFalse

## Authoring quality gate

Verified before user execution:
- C193 parent NPZ schema is defined in C194's own loader:
  necessity[9,9536,4], target[9,9536,3], row/local/world identity arrays;
- run path calls C194's own loader;
- no parent-helper loader dispatch;
- generic loop source contains no phase1/phase2/phase3 branches;
- target-capable vs necessity-only mode is selected from current active-state missingness;
- 19 parent summaries are registered;
- precheck receives C193 +18 prior summaries +root;
- postcheck ExpectedHead is argv21;
- new tests24, total1581, modules79;
- C193 coherent sources are reused from the protected C191 source directory;
- log publisher is configured for C194.

Scientific manifest SHA256:
`046659d7103d327e8b75e13258b597db4813fb0f7c844f35e444b54b0ea21d99`.
