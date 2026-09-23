# V5-B assignment holdout with balanced positions v0.1 — C241

## One question

C240 found that44/48 C239 HOLDOUT answers matched the preregistered query-to-fixed-position rule.
If training itself contains each queried entity in both rendered positions, can the same fixed
models/optimizer learn the entity/value relation well enough to transfer to the swapped value
assignment that is never used for optimization?

This is a bounded assignment-transfer question. It is not new vocabulary/entity generalization,
not a proof of an internal binding algorithm, and not a Gate F run.

## Partition

Start from the exact C239 outer TRAIN/HOLDOUT mapping, which together contains the same16 C238
prompts. Repartition without modifying row bytes:

- C241 TRAIN8: values == [0,1], both fact orders, both queried objects, English/Japanese.
- C241 HOLDOUT8: values == [1,0], both fact orders, both queried objects, English/Japanese.

Canonical C241 outer mapping SHA256:
`1d373b3652bf03027a1e23c45e2fc117895015640193b49f9c38f07099a1ae7a`.

Exact prompt strings/IDs do not overlap between the two assignments. Each split has4 rows/language,
2 rows/order,2 rows/query and balanced target bytes0/1. Parent row provenance split="TRAIN" remains
unchanged; the C241 outer mapping determines optimizer membership.

This split deliberately removes the C239 position correlation inside TRAIN. For object0 and object1
queries, the queried entity appears once in each rendered position per assignment/language pair.
The preregistered query_fixed_position shortcut therefore reaches only50% on TRAIN.

A fixed entity-value lookup (box->0/book->1 and Japanese equivalents) can solve this TRAIN assignment
but reaches0% on the swapped HOLDOUT. A HOLDOUT pass therefore rules out both of those simple
behavioral rules on this fixture, while still not identifying a unique internal mechanism.

## Fresh initialization and training

Never start from C239/C238 trained states. Recreate Full/GRU-only models using seeds234001-234003,
make the common-weight GRU-only copy before either paired model trains, and require each fresh
fingerprint to match C239's saved initial_sha256.

Keep Full13488/GRU-only10160 parameters,width16,48 slots,byte renderer,unrestricted256-way output,
AdamW lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,batch32 and400 updates/model.
CPU float64,threads2,deterministic algorithms.

Each update contains all8 TRAIN rows exactly4 times. The C241 fit function is executable-AST
identical to accepted C239.fit except the progress tag. This keeps the complete-cohort8x4 policy,
loss and optimizer fixed. Every retained TRAIN row receives1600 presentations/model.

Only TRAIN is evaluated before training. HOLDOUT is first rendered for evaluation after step400;
it cannot influence optimizer updates, early stopping, seed/checkpoint selection or further learning.

## Metrics and gate

The inherited C234 fact-pair metric is intentionally NOT fabricated here: each split contains only
one value assignment, so a within-split fact-swap pair does not exist.

For every language/split score:
- exact unrestricted-byte answer accuracy;
- answer NLL;
- evidence-blind/query-blind accuracy and drops;
- query-pair both-correct accuracy: same assignment/order, two queried entities;
- order-pair both-correct accuracy: same assignment/query, two fact orders.

Each split has4 rows/language,2 query pairs and2 order pairs. The fixed gate requires on BOTH TRAIN
and HOLDOUT for every Full seed/language cell:
- accuracy >=0.90;
- query-pair >=0.80;
- order-pair >=0.80;
- evidence-drop >=0.35;
- query-drop >=0.35.

At these discrete counts this means4/4 answers,2/2 query pairs and2/2 order pairs.
GRU-only is reported independently and cannot substitute for Full.

Classify each seed/family/language cell as TRAIN_FIT_MISS, ASSIGNMENT_HOLDOUT_MISS or BOTH_PASS.
A valid Full miss is ACCEPTED VALID NEGATIVE. A Full pass supports only this binary assignment
transfer under the fixed fixture; it does not establish new values, entities or general language.

## Workload and integrity

Six models x400 updates=2400 training steps /76800 answer presentations.
Per model:initial TRAIN3 + final TRAIN3/HOLDOUT3 + reload TRAIN3/HOLDOUT3 =15 evaluation forwards.
Totals:2490 full-model forwards /77520 row presentations. One new six-state checkpoint bundle.
No parent model forward or scientific network call.

Require exact fresh initial fingerprints, changed weights, non-mutating evaluation, actual
forward/row counters, strict checkpoint identity/order, exact prediction replay and raw-logit/metric
replay <=1e-9. Source/artifact/schema/nonfinite/replay/workload failures are INVALID / RETRY SAME C241.

## Scope and stop

A pass would be stronger than C238's seen-prompt fit because the swapped assignment was withheld
and both rendered positions were represented during training. It still uses only two entities,
two digits and existing language forms; alternative shortcuts remain possible.

No answer inversion, larger model, extra steps, new corpus, paid API, history rewrite or production
runtime change. Gate F remains NOT PASSED; numeric-memory tuning remains paused.
Judge C241 before registering C242.
