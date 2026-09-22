# C234 preregistration — contextual binding pilot

**C233 ACCEPTED VALID NEGATIVE. C234 ACTIVE / NOT YET JUDGED. C235 NOT REGISTERED.**
Stage V5-B-CONTEXTUAL-BINDING-PILOT. Gate E PASSED; Gate F NOT PASSED.

## One scientific question

Can the unchanged full V5-B model select the queried object's observed value on held-out two-value
contexts, while responding correctly to paired changes in facts and queried object?
Keep the ordinary GRU-only model alongside it. This is not a renewed C233 superiority test.

Changed scientific task: from next-byte template loss to single-answer contextual binding.
Fixed architecture, per-model400-step optimizer recipe, byte adapter and precision. Both families
start afresh on the new data. No trained checkpoint continuation or learned memory integration.

## Accepted parent and validity

C233 execution HEAD: `fedf6c3e5c163d449d1ad793a87d4fa6952deb1d`.
Published log commit: `519d71abe912639869130cb4dff3f196e166b92f`.
Summary SHA: `5e9895008ebf02c72c3b5c00a8668f1c8078feef94dd2fc1eff192d41e8709bf`.
Validation SHA: `c839db0ed26f0369dcedb6227ae5278ca60904d8636da0d00e49da02d75998e4`.
Local summary: `runs/c233-v5b-core-ablation-f73f95f4afa44668a64b953f1bbad723/summary.json`.

The parent is an accepted valid negative: serialized status FAIL, baseline qualified, full wins3,
baseline wins3, ties0 and all replays true. The child explicitly validates that contract; it does
not demand a parent scientific PASS or rewrite the result. Parent sources244/protected inputs346
and all five artifacts remain unchanged. Acceptance record: experiment-ledger-addendum-c233-c234.md.

## Fixed data

Object vocabulary EN box/book/ball/umbrella; JA 箱/本/玉/傘. Values ASCII0/1/2/3.
Each prompt has two different objects with different values, followed by one requested object.
Example `box=0;book=3;box=` -> target byte `0`.

72 binding groups (six object pairs x12 ordered value assignments), eight realizations per group
(two languages, two fact orders, two queried objects):576 rows.
EVAL holds co-occurring unordered value pairs {0,3} and {1,2}, across every realization.
TRAIN384 rows/48 groups; EVAL192 rows/24 groups. Every individual object/value pairing occurs in TRAIN.
EVAL96 rows per language,24 targets of each digit. Always first/last fact50%, constant25%.

Dataset SHA: `72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85`.
Dataset generation, split and exact metadata are hashed; no downloaded corpus or additional data.
Longest input27 bytes. Use unchanged C231 prefix adapter; score only separate answer byte.

## Fixed controls and gate

For each of three full-model seeds and each language:
- exact unconstrained256-way argmax answer accuracy >=0.90;
- both-correct fact-swap pair accuracy >=0.80;
- both-correct query-swap pair accuracy >=0.80;
- accuracy drop when masking both observed values >=0.35;
- accuracy drop when masking queried object >=0.35.

Fact pairs hold objects/order/query fixed and swap assigned values. Query pairs hold facts fixed and
query the other object.48 pairs of each kind per language, drawn from the same96 EVAL rows; not
independent evidence sets. Masked rows replace removed content with '?'. Their distribution differs
from training; paired normal-input changes complement rather than erase that confound.

Report `full_binding_gate` and `gru_binding_gate` independently. Primary `context_binding_gate`
requires the full-model criteria plus changed/replayed weights and fixed workload. It does NOT
require full-model superiority over GRU. Neither family is parameter/compute matched; report no
core superiority claim. C233's negative stays negative even if this different task succeeds.

## Workload

Fresh paired seeds234001/234002/234003. Full13488 parameters; GRU-only10160.
Instantiate full via C231, copy common INITIAL weights through accepted C233.new_baseline before
either family trains. No parent trained weights are used; parent artifacts are validation evidence.

AdamW lr0.005, betas0.9/0.999, eps1e-8, weight_decay0; gradient norm clipping1.0;
batch32,400 steps/model. CPU generator seed+1000 draws TRAIN-only rows with replacement, identically
for paired families. CPU float64, threads2, deterministic algorithms.

Six models /2400 training steps /76800 sampled answer presentations. Total workload doubles from
C233 because both families train, but per-model budget remains400. No early stopping, EVAL tuning,
seed substitution or checkpoint selection. Initial/final EVAL and final normal/masked predictions
are recorded; checkpoint fingerprints and logits/argmax must replay (max logit error1e-9).

Complete finite ability misses are valid negatives. Artifact/source/schema/nonfinite or failed
checkpoint replay is INVALID / RETRY SAME C234. Failure to beat a threshold never authorizes a
budget increase or threshold relaxation in C234.

## Authoring / protection

OWN6:
- fold_lm/v05_benchmarks/model_c234_context_binding.py
- tests_lm/test_v05_c234_context_binding.py
- tools/run_c234.ps1
- tools/invoke_c234.ps1
- this preregistration
- docs/v5b-contextual-binding-v0.1.md

Parent244 sources + OWN6 =250. Protected346 + parent summary/artifacts6 + OWN6 =358.
Ten direct dependency entries: C231's five language/import sources plus C231/C232/C233/C230
benchmark/helper entry points and this benchmark. Transitive dependencies remain parent-pinned.
No accepted production source, historical test or existing artifact is edited or removed.

New tests32; modules119; loaded2786/focused2785. Preserve only the inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Artifacts5: binding-plan.json, dataset.json, trained-models.pt, measurements.json,
validation-summary.json. All outputs remain under ignored runs/; console/receipt publication only.
Manifest SHA: `0c3c3cedd0a15fa8b392cbe38ba5285113a948b78ef3511bf106cbc75d7b2d38`.

## Post-authoring review

`post_authoring_review = PENDING`

Initial targeted author-side run:30/30 tests PASS in1.006s, Python3.13.5 / PyTorch2.10.0+cpu.
These use synthetic parent interfaces with real GRU/optimizer layers. They verify exact data/group
splits, balanced positional baselines, prefix separation, paired controls, masked inputs, identical
sampling, prediction scoring, checkpoint serialization and a synthetic full-run valid-negative
path. The full-run test simulates training and is not a model-quality result.

Pending here: test31 actual parent/model TRAIN-only smoke; test32/full2785 historical suite;
Windows PowerShell AST; user-local accepted artifacts; formal six-model2400-step training.
Container network cannot resolve raw.githubusercontent.com; source reads through GitHub succeed.
Do not report those pending tests as passed or tune this pilot from author-side held-out results.

After committing all files, re-fetch code/tests/runner/launcher, compare exact Git blobs to tested
copies, rerun authoring tests and recheck manifest, actual parent semantics/helper paths, all32 test
methods, free names, ten dependencies,250/358 protection and complete ACTIVE/HEAD/parser/CLI guards.
Record review HEAD and explicit execution limitations before issuing the standard launcher command.

## Stop

32 own tests ->2785 focused tests ->C234 only. Judge C234 before C235 registration.
Gate F NOT PASSED. No larger model, external data, paid API, CI, numeric-memory optimization,
cleanup or history rewrite is part of this work.
