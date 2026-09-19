# C195 preregistration — generic-loop budget12 exhaustion safety

**C194 ACCEPTED PASS. C195 ACTIVE / NOT YET JUDGED. C196 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

With the accepted C194 generic loop held fixed and only initial TaskView
`internal_remaining: 13 -> 12`, does the loop reproduce accepted C191 budget12 behavior
without fake SUFFICIENT closure, unauthorized fourth inference, or extra provider work?

## Changed variable

Only initial numeric resource coordinate62:
`internal_remaining 13 -> 12`.

The generic `C194.run_loop()` implementation is reused unchanged.

## Held constant

- same C174 PILOT NEEDS cohort
- same1768 source rows ->9536 coherent worlds/selector
- all9 frozen C181 x C188 selector pairs
- same C172/C173 action/admission runtime
- same16 protected coherent-world sources
- max_dispatches3
- same teachers/raw argmax
- same generic-loop orchestration
- no training / fresh seeds / production runtime changes

## Exact reference

Accepted **C191** is the budget12 reference:
- execution `f83ed1d60758dc1ff895b2b9c42c69d6a68c0931`
- summary SHA256 `b05cd702e9572c61a3ae981e5279c7fb096fe1078c7d65f6401f180f307c84f4`

C195 uses its own loader for the accepted C191 prediction artifact.

Required replay:
- first3 necessity predictions exact
- all3 target predictions exact
- active finite necessity/target logits <=1e-6
- C191 row/local/world identity exact
- per-block second-read count exact
- per-block third/exhausted count exact
- actual file reads exact

## Exhaustion contract

For rows that require three acquisitions:

```text
start                  12 /4 /step7
decision0              11 /4 /8
acq1 + decision1        7 /3 /12
acq2 + decision2        3 /2 /16
acq3                     0 /1 /19
next scheduler debit     REFUSED
```

Required:
- exactly3 successful learned decisions
- exactly3 acquisitions
- status `BUDGET_EXHAUSTED`
- final resources0/1/19
- all four facts observed
- logical final state is SUFFICIENT under scoring teacher
- **no fourth learned prediction**
- no fake `SUFFICIENT_CLASSIFICATION`
- no fourth provider read/publication
- no runtime mutation caused by the failed debit beyond the already admitted third fact

Rows resolved after one/two acquisitions must still stop normally as
`SUFFICIENT_CLASSIFICATION`.

## Fixed gate — all 9 blocks

Per selector:
- episodes9536
- reference exhausted rows928
- first reads9536
- exhausted rows928
- third reads==exhausted rows
- sufficient rows + exhausted rows =9536
- exact actual-read accounting
- acquisition contract errors0
- status errors0
- resource errors0
- final logical errors0
- fake final decisions0
- reference replay errors0
- reference block mismatches0
- reference necessity/target prediction errors0
- unauthorized final predictions0
- active logit deltas <=1e-6

All9 must pass.

A completed finite mismatch caused by the generic loop/budget12 interaction is
**ACCEPTED VALID NEGATIVE**.
Source/hash/schema/reference-artifact identity/loader/nonfinite infrastructure/incomplete/
protection failure is **INVALID EXECUTION / RETRY SAME C195**.

## Interpretation

PASS means the generic loop handles both sides of the resource boundary correctly:
- budget13 => authoritative final SUFFICIENT closure (C194/C193)
- budget12 => safe exhaustion after third acquisition with no fabricated completion (C195)

PASS does not establish a learned resource policy, arbitrary-length looping, learned
tool/provider choice, independent final holdout, language, answer/proof, or Gate E completion.

## Workload

-85824 episodes /9 blocks
-max3 acquisitions
-no authorized fourth inference on exhausted rows
-artifacts5 excluding summary
-source pins136
-protected paths363
-expected regression **1605 =1581 existing +24 new**
-expected modules80
-production runtime modifiedFalse
-Gate E candidateFalse

## Authoring quality gate

Before user execution:
- C195 own C191-reference loader schema is fixed:
  necessity[9,9536,3], target[9,9536,3], row/local/world arrays;
- run path calls C195's own reference loader;
- generic loop is imported from accepted C194 unchanged;
- synthetic integration covers 3 acquisitions, rejected fourth debit, resources0/1/19,
  no phase3 prediction, and earlier SUFFICIENT stop;
-20 parent summaries are registered;
-precheck receives C194 +19 prior summaries +root;
-postcheck ExpectedHead is argv22;
-new tests24,total1605,modules80;
-reference/block mismatch is resolved before trace emission;
-log publisher configured for C195.

Scientific manifest SHA256:
`ebfa3e2f916368b4e2b07efa072c9f9c2b4ec62cb0c77ac69e3cb1f527b90128`.
