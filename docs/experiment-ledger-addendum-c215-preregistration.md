# C215 preregistration — V5-F H1/H2 chunk commit

**C214 ACCEPTED PASS. C215 ACTIVE / NOT YET JUDGED. C216 NOT REGISTERED.**
Gate E **PASSED**. Gate F **NOT PASSED**.

## Scientific question

Can a deterministic H1 hot-memory / H2 capsule-bank chunk-commit boundary preserve supported
readouts and capability status across commit and post-commit edits without hidden operation replay?

## Accepted parent

C214 execution `b4a020aeb006ec758e06ce1dc6d1b0ad5784e150`
summary `bd7a310fc89873b4571d1748a96fa1a121d147a0617d48e2d8824d4769deb37d`
validation `974546ca0e93bd0b936a68cdfcc9068bbdf6d8a53be9c7f2e8c6edafc50b543f`
status **ACCEPTED PASS**.

## Changed variable

New production reference:
`fold_lm/v05/memory_bank.py`

Schema:
`fold-v5f-h1-h2-bank-v1`

It adds H1/H2 placement, representation-only chunk commit, HOT_REQUIRED, current protected-factor
descriptors and storage_epoch.

## Fixed gate

Snapshots9; status sequence:
`SUPPORTED,HOT_REQUIRED,SUPPORTED,SUPPORTED,HOT_REQUIRED,SUPPORTED,SUPPORTED,SUPPORTED,SUPPORTED`.

H1 observed counts `[0,1,0,0,1,0,0,0,0]`.
H2 factor counts `[0,0,1,1,1,2,1,1,1]`.
Total observed counts `[0,1,1,1,2,2,1,1,1]`.

Two commits: COMMITTED/COMMITTED, semantic clocks unchanged, readout deltas `[0.0,0.0]`.

Final: storage_epoch2, H2 reflected evidence revision4, semantic clocks6/4/3, H2 factor beta only,
hot records0, operation history0.

Full-reference max abs error <=1e-10.

Controls:
- NOOP commit;
- OUT_OF_SCOPE read+commit preserves state;
- NUMERIC_UNSAFE read+commit preserves state;
- no value exposure for unsupported reads.

No learned Writer/Reader/Port Selector/Coverage classifier, model forward or training.
C215 is not a Gate F decision.

## Authoring

OWN7; source pins122; protected inputs230; artifacts5; tests34; regression modules100;
loaded2150 / focused2149.

Manifest:
`90327cc0691bc80d7faf78f77e36a501f178ac9f861b0524f6e174be3635f9bf`

## Post-authoring review

`post_authoring_review = PENDING`

Review must verify parent identity, H1/H2 semantics, no history field, commit clock invariance,
HOT_REQUIRED routing, post-commit replace/retract, controls, counts, aliases, runner argv,
PowerShell parser and C216 non-registration.
