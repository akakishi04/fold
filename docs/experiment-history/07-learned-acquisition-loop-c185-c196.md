# Learned acquisition and generic loop — C185-C196

## Scientific subject

This sequence turned the accepted learned necessity representation into actual information-gathering
behavior: decide whether information is needed, select what is needed, perform real bounded
acquisition, reobserve, repeat, and stop safely.

## Timeline and deciding data

### C185 — single-missing learned acquisition — PASS
- 44,544 candidate episodes
- 9,216 necessary acquisitions
- 35,328 correct skips
- 0 candidate failures
- all post-acquisition candidate decisions SUFFICIENT

Established the first learned semantic decision -> real acquisition -> reclassification path.

### C186 — non-admission reclassification — PASS
Three candidate models:
- 111,360 episodes
- 23,040 attempts
- 9,216 admitted
- 13,824 non-admitted
- 88,320 skips
- 0 failures

A denied/missing/non-admitted attempt did not become fake evidence or fake SUFFICIENT.

### C187 — authority restriction — PASS
Same candidate semantics under:
- allowed bit0 / bit1
- permission denied
- provider unavailable
- acquisition budget zero

Candidate totals:
- 111,360 episodes
- 23,040 proposals
- 13,824 denied
- 9,216 successful reads/admissions
- 0 candidate failures

Separated learned semantic NEEDS from runtime execution authority.

### C188 — multi-missing target selection — PASS
Nine selectors = 3 frozen C181 bases x3 fresh target heads.

Primary discriminating PILOT:
- missing2 376/376
- missing3 152/152
- macro 1.0 for all 9 selectors

References:
- FIRST_UNKNOWN macro 0.5263
- TRAIN-only syntax-blind frequency macro 0.7774

Secondary full multi-missing cohort:
- 1,768/1,768 correct for every selector
- selected observed facts = 0

### C189 — one real learned target acquisition — PASS
- 31,824 live episodes
- provider calls/publications/reservations 31,824 each
- all deciding errors 0
- post acquisition: 19,595 SUFFICIENT / 12,229 NEEDS

Closed learned target -> real IO -> actual-state reclassification for one step.

### C190 — iterative two-acquisition path — PASS
9 blocks x9,536 = 85,824 coherent-world episodes.
- first reads: 85,824
- post1 NEEDS / second reads: 34,948
- post2 NEEDS: 8,352
- total reads: 120,772
- all deciding errors 0
- parent initial replay exact

### C191 — third acquisition under original budget12 — PASS
- third reads/publications/reservations: 8,352
- total reads: 129,124
- after third acquisition all facts observed
- logical final NEEDS: 0
- fourth scheduler decision accepted: 0

Resource boundary:

```text
start                  12 /4 /step7
decision0              11 /4 /8
acq1 + decision1        7 /3 /12
acq2 + decision2        3 /2 /16
acq3                     0 /1 /19
fourth decision          refused
```

### C192 — post3 shadow necessity — PASS
Read-only frozen C181 on the actual post3 fully observed state:
- shadow rows: 8,352
- shadow errors: 0
- logical teacher errors: 0
- runtime mutations/read-after-shadow: 0

This isolated the C191 blocker to scheduler budget rather than semantic recognition.

### C193 — budget13 authoritative closure — PASS
One-variable intervention: initial internal budget12->13.
- first reads 85,824
- second reads 34,948
- third reads 8,352
- authoritative final decision rows 8,352
- final decision errors 0

The formerly shadow-only SUFFICIENT decision became runtime-authoritative.

### C194 — generic state-driven loop — PASS
Replaced manually unrolled phases with one bounded loop:

```text
current state
-> charge learned decision
-> SUFFICIENT => stop
-> NEEDS + legal target => real acquisition
-> reobserve actual state
-> repeat
```

C194 exactly reproduced C193 predictions/logits/read depths:
- necessity prediction errors 0
- target prediction errors 0
- max active logit deltas 0.0
- total reads 129,124

### C195 — generic-loop budget12 exhaustion — PASS
The same generic loop with budget12 reproduced the C191 resource boundary:
- first reads 85,824
- second reads 34,948
- third reads 8,352
- exhausted rows 8,352
- sufficient rows 77,472
- unauthorized final predictions 0
- fake final decisions 0
- reference logit deltas 0.0

C194/C195 therefore establish both sides of the explicit scheduler boundary:
- budget13 -> authoritative final SUFFICIENT
- budget12 -> safe exhaustion without fabricated completion

### C196 — result-aware generic loop under post-decision permission revocation — PASS
Two full 85,824-episode arms:
- ALLOWED reproduced accepted C194 exactly;
- PERMISSION_REVOKED_AFTER_DECISION produced 85,824 DENIED/PERMISSION_DENIED attempts;
- provider calls/publications/receipts/retries all 0;
- fact mutation/fake SUFFICIENT/resource errors all 0.

This establishes that loop continuation is conditioned on actual OBSERVATION_ADMITTED publication,
not merely on attempting an acquisition.

## Current boundary after C196

Still not established:
- post-reservation provider-failure reason propagation (C197 is active at this report cut);
- learned resource policy;
- arbitrary/unbounded looping;
- learned tool/provider choice;
- independent final holdout;
- language/answer/proof integration;
- Gate E completion.

## Cleanup implication

This is the most active chain. C181, C184, C188 and C190-C195 helpers/artifacts are still heavily
referenced by C196. Do **not** remove these from the scientific branch while C196 or its immediate
successors depend on them. Older one-off launchers may later be archived separately from benchmark
and test modules.
