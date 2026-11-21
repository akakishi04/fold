# C329 acceptance / C330 boundary

Review date: 2026-10-17 Japan time.
Formal verdict: C329 ACCEPTED VALID NEGATIVE. Scientific FAIL; execution valid.
C328 and all earlier verdicts remain unchanged. Gate F NOT PASSED.
C330 is not registered by this acceptance. Do not rerun accepted C329.

## Identity and review scope

Scientific execution HEAD: f8582ca34bd7e10c7403713e935debe94720dfde.
Published log commit: 2d181d23c7f84749384e9283c8d8de2df7619bd8.
Publication sole parent matches scientific execution; Git tree06d6cecedf7340cd838f6afaf7b5149f4182f911.
Log: docs/experiment-run-logs/c329/latest.log and latest.json.
Log blob03d264150904b01f2041e0c34ffb6f5bc0f5b8c6.
Publisher metadata reports150267 original Windows bytes;SHA256
625ed2c6a61293bd2c4d9f31784fc073b50bccc197646562c985850168ae57d4.
Reviewer read native startup,full regression completion,all five complete fits and
prefix-preservation messages,ten checkpoint-replay messages,all ten seed flags,
all five paired contrast records and the terminal integrity receipts. Paired counts
were independently summed. No independent whole-log byte rehash, model replay,
optimizer-history replay or full local-cell reconstruction is claimed. The compact
metric excerpt was not treated as complete local measurement coverage.

## Valid execution

Full5770tests/218modules PASS; failures/errors/skips0;673.454seconds.
Native locks,parent semantics and allfive schedule/readout/backward preflight passed.
Five uninterrupted2400-update trajectories;allfive1200 snapshots preserved;
optimizer creations5;ten checkpoint states evaluated and replayed. Saved trajectory
reconstruction,all1577 final uncached rereads,fresh832source/1577input envelope
verification completed. Regression/science/verify exit0;run_execution_valid=true.
Actual work:12000updates,576000TRAIN row presentations,15420model forwards,
904320total rows,61680core forwards,20checkpoint loads,one scientific bundle reload,
one new bundle write. Parent verification and tests are outside these counters.

Folder:runs/c329-budget-66a7cc83726341aaa59542f02bc7a7e5/.
Primary science/summary.json SHA256:
89341eade41d5c35c2e7b9a7a84238b272adcd21c28d143da68fbc0aaf8fdf1a.
Mandatory execution-envelope.json SHA256:
6939cb8c53a44ffefd86342721d48d168e7c938f37432948ea3488fe1453b473.
Manifest9968ab6d8d2abdd3751b6ac1d1b1116a088d1c8abbdebdae50b580005d6fb7d8.
Primary schemafold-c329-science-v1;envelopefold-c329-execution-envelope-v1.
Eight outputs plus primary and envelope makeTEN immediate-parent files.
Complete source/input unions832/1577 must be inherited without reduction.

## Deciding HOLDOUT counts

Each seed:288interior answers/144query pairs;1440original2..6 answers/720pairs.

|Seed|Interior answers1200->2400|Interior pairs1200->2400|Original answer gain|Original pair gain|Complete paired success|
|---|---|---|---:|---:|---|
|329001|252->288|120->144|8|8|false|
|329002|179->275|65->132|45|42|false|
|329003|275->288|135->144|13|6|false|
|329004|238->288|99->144|-1|7|false|
|329005|262->288|125->144|0|0|true|

Interior normal answers1206->1427/1440 (83.75%->99.097222%);pairs544->708/720.
Interior rescued/regressed answers224/3;pairs164/0. Both count gains positive in all5.
Original pooled answers7072->7137/7200;gain65. Paired pair gains sum63.
Interior complete gate0/5->4/5. Original2..6 retention1/5->1/5.
Original per-length complete gates1200->2400:2,3,4 each4/5->5/5;5:1/5->3/5;
6:1/5->1/5. Composite1/5,not the required5/5;scientific FAIL is retained.
Do not turn the seed329005 success into cohort success or select it for adoption.
Pooled counts reuse logical problems across seeds/profiles,not independent samples.

## Interpretation and next question boundary

This fixed extension improved interior binding in every paired seed and produced
one full joint success. It did not establish reliable all-seed retention,especially
for original6. A gain is observed but the registered policy fails its full criterion.
This does not prove more training is always beneficial,an optimal budget,architectural
capacity limits,unseen-template reasoning,Gate F or production suitability.

Before another fitting intervention,localize the remaining fixed-gate failures from
all ten saved checkpoints. Distinguish normal accuracy/query-pair failures from
mask-only failures and independent both-order failures;preserve overlapping failed
criteria and compare1200->2400 transitions on exactly matched cells. This should
reconstruct the existing gates,not relax them or substitute pooled accuracy.
The prospective C330 is a saved-measurement diagnostic with no new learning/model
forward. Exact implementation/tests/contract/review and activation remain separate.
