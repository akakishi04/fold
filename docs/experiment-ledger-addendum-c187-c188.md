# C187 acceptance / C188 handoff

V5-E; repository `akakishi04/fold`; branch `feat/sft-target-loss`.

## Formal judgment

**C187 — ACCEPTED PASS.**
**C188 NOT REGISTERED at this acceptance commit.**
Gate E remains **NOT PASSED**. All earlier judgments, checkpoints, preregistrations and
valid negatives remain unchanged.

Successful C187 execution identity:
- execution HEAD: `bbb79df40f3428f358bec7381cd872efa7845e63`
- run: `runs/c187-v5e-restricted-acquisition-cc3717a5a9994142a9147953dce83573/summary.json`
- summary SHA256: `910a8a51c70a7ddfd996d99d21bcd9bc362ba568919ed04fb7305071d9142ccd`
- focused regression: **1377/1377**, 49.777s
- source/artifact precheck: PASS
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- `run_execution_valid = True`
- production runtime modified: **False**
- Gate E candidate: **False**

## Deciding evidence

C187 reused the six frozen C181 checkpoints and the C185 bounded driver. It changed
only one initial execution-resource coordinate in each restriction condition:

1. allowed, source bit 0
2. allowed, source bit 1
3. RETRIEVE permission denied
4. RETRIEVE provider unavailable
5. acquisition budget zero

Cohort: all 3712 one-missing PILOT rows (768 NEEDS / 2944 SUFFICIENT), two local
layouts, five conditions, eight policies = **296960 episodes / 80 blocks**.

For each of the three `INTERNAL_SEMANTICS` candidate models (seed181001/2/3):
- episodes: **37120**
- failures: **0**
- initial semantic errors: **0**
- missed proposals: **0**
- unnecessary proposals: **0**
- post-decision errors: **0**
- false SUFFICIENT after denial: **0**
- contract errors: **0**
- proposals: **7680**
- denied proposals: **4608**
- allowed provider calls/publications/reservations: **3072 / 3072 / 3072**
- initial decision flips from unrestricted C185: **0**

All three candidates together:
- candidate episodes: **111360**
- candidate failures: **0**
- proposals: **23040**
- denied proposals: **13824**
- successful reads/admissions: **9216**
- skips: **88320**
- restricted provider calls: **0**
- candidate initial decision flips from unrestricted: **0**

All-policy totals (controls included) were:
- action attempts 78732
- denied attempts 46988
- provider calls/publications/reservations 31744 each
- failed 65052
- false sufficiency after denial 72
- contract errors 0

Those all-policy errors are control behavior and MUST NOT be reported as candidate
errors. The candidate total remains zero failures.

Static replay: 56376 original predictions across all six frozen models, exact decisions,
max logit delta 0. The 32 allowed live blocks replay accepted C185 behavior. Total neural
rows 320708, 360 forward batches, 2520 shared-cell calls. No new training, fresh seed,
teacher, auxiliary head, answer generation, proof checking, network call or core
EvidenceState write.

## Scientific interpretation

C187 establishes, only in this bounded development scope, the following separation:

```text
same logical evidence
-> frozen learned semantic necessity
-> handwritten sole-unknown RETRIEVE proposal
-> independent C172/C173 authority check
   -> allowed: one real read/admission
   -> denied/unavailable/no budget: zero read/publication
-> actual current state
-> frozen learned reclassification
```

The learned candidate continues to classify the information as NEEDS when retrieval is
forbidden, unavailable or out of acquisition budget. The runtime independently prevents
IO. Therefore in this measured scope **"cannot acquire" is not collapsed into "already
knows"**, and semantic necessity is not being used as an authority bypass.

## Claim / non-claim

Claim:
- frozen candidate necessity remains correct under the three registered initial execution
  restrictions;
- unchanged runtime enforces the corresponding denial without provider IO;
- allowed controls continue to read/admit exactly once;
- live budgets/outcomes are not reset to training constants.

Non-claim:
- no learned selection among multiple missing facts;
- no learned tool choice, retry, alternative source selection or stopping policy;
- no arbitrary/concurrent revocation proof;
- no answer or proof generation;
- no natural-language, larger-expression or repeated-variable generalization;
- no independent final holdout;
- no Gate E completion or production adoption.

Target/tool remain handwritten and the cohort has exactly one missing fact. The same four
development semantic groups have been repeatedly inspected.

## Reviewer verification boundary

The uploaded C187 log was parsed as a complete RESULT payload. Its canonical reconstructed
summary is 269632 bytes and hashes exactly to the reported summary SHA256 above.
The 80 records, candidate per-seed totals, all-policy totals, provider/publication
arithmetic and fixed candidate gate were independently reaggregated from that payload.

Separate C187 artifacts, the full NPZ/traces/checkpoints/data, and the user's 1377 tests
were not independently rerun by the reviewer. This distinction remains part of the
accepted evidence.

## Next single boundary

The next proposed scientific question is the first **multi-missing target-selection**
question: with more than one unobserved fact, can a learned selector choose an actually
influential missing fact rather than merely deciding that some information is needed?

Do not connect target selection to live acquisition in the same experiment. First isolate
which-fact selection offline, keeping the accepted C181 necessity representation frozen.
C188 must be separately preregistered after this acceptance commit.
