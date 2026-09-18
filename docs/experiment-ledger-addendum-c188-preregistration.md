# C188 preregistration — learned target selection among multiple missing facts

V5-E; repository `akakishi04/fold`; branch `feat/sft-target-loss`.

Registered only after C187 acceptance commit
`bdbc71ca17a7a6138f54d1188c17ce7dd33dcece`.

**C187 ACCEPTED PASS. C188 ACTIVE / NOT YET JUDGED. C189 NOT REGISTERED.**
Gate E remains **NOT PASSED**. Earlier judgments, checkpoints and negatives stay fixed.

## One scientific question

Can a small learned selector, using frozen accepted C181 `INTERNAL_SEMANTICS`
representations, choose a **currently influential missing fact** when more than one fact
is unobserved, better than a syntax-blind TRAIN-only frequency reference?

C185-C187 intentionally kept target choice handwritten because there was only one
unobserved fact. C188 removes only that target-choice triviality. It does **not** also
connect the new selector to live acquisition; that would be a later experiment if C188
passes.

## Target definition

For one current partial observation, an unobserved fact is a valid target iff there
exist two completions consistent with the currently observed facts that:

1. differ only in that fact, and
2. produce different final Boolean outputs.

This teacher is computed from the registered C174 truth table and visible observations.
Unknown completion values are never model features. The target teacher has no model
inference interface and does not choose a single arbitrary label when several facts are
valid.

Training loss accepts the complete valid set:

```text
L = logsumexp(logits over all currently unknown facts)
  - logsumexp(logits over TRAIN teacher-valid influential facts)
```

Thus any currently influential target receives credit; ties in the logical target set are
not broken by an arbitrary teacher convention.

## Cohort

Use the unchanged C174 TRAIN/PILOT split and the same four repeatedly inspected PILOT
semantic groups. This is development evidence, not independent final confirmation.

Primary cohort includes only NEEDS rows with 2 or 3 unobserved facts where not every
unknown is influential. Rows where every unknown is valid are excluded from the primary
because any unknown choice is trivially successful. One-missing rows are excluded because
C185-C187 already made target selection trivial. Four-missing rows are also trivial in
this read-once family.

Registered counts, independently enumerated before registration:

| cohort | missing=2 | missing=3 | total |
|---|---:|---:|---:|
| TRAIN discriminating | 2696 | 1128 | **3824** |
| PILOT discriminating | 376 | 152 | **528** |
| full PILOT NEEDS secondary | 1152 | 616 | **1768** |

Missing=3 target-set sizes in the discriminating cohort:

```text
TRAIN: valid1=440, valid2=688
PILOT: valid1=72, valid2=80
```

## Frozen base representation

Use only the three accepted C181 `INTERNAL_SEMANTICS` bases, source seeds:

```text
181001
181002
181003
```

Restore bare C181 inference weights only: 25,726 parameters. No auxiliary head or
teacher exists in base inference. Base fingerprints are checked before and after feature
extraction; base weights are never optimized in C188.

For each source row, run the unchanged C178 bound representation through the frozen C181
TREE_LINKS base and capture the actual outputs of all seven shared-cell applications.
For each fact candidate construct:

```text
7 hidden states x 64 = 448
+ one-hot position of that fact's FACT leaf = 7
-----------------------------------------------
candidate feature width = 455
```

The same complete seven-state representation is shared across the four fact candidates;
only the fact leaf-position one-hot differs. Observable missingness masks already observed
facts from selection. The logical target teacher is absent from inference.

C184 local-index normalization is not a changed variable here: C188 uses the original
canonical C174 source rows. No renaming/OOD claim follows.

## Learned selector

Shared scorer applied independently to each fact candidate:

```text
455 -> 64 ReLU -> 1
```

Trainable parameters: **29,249**.

Fresh target-head seeds:

```text
188001
188002
188003
```

Cross all three frozen base seeds with all three fresh head seeds:
**9 final target selectors**.

For the same target-head seed:
- initial target-head weights must be identical across the three frozen bases;
- minibatch row schedule must be identical across the three frozen bases.

Training is TRAIN-only:
- rows: 3824 discriminating TRAIN rows
- updates/head: 2000
- batch: 256 with replacement
- Adam lr0.001, betas0.9/0.999, eps1e-8
- weight_decay0, amsgradFalse, foreachFalse
- row RNG: `head_seed + 1000000`
- CPU float32 / two threads / deterministic algorithms
- 18,000 total selector updates
- 4,608,000 sampled TRAIN rows
- no C181 base update

All nine final target heads are saved and reloaded before PILOT scoring. No validation
selection, best-head selection, ensemble or prediction repair.

## Transparent references

### FIRST_UNKNOWN

Choose the lowest-index currently unknown fact.

Registered PILOT discriminating result:

```text
missing2: 188 / 376 = 0.500000
missing3:  84 / 152 = 0.552631578947...
macro:                 0.526315789473...
```

### TRAIN-only syntax-blind frequency reference

Key only by the visible fact table (`raw[46:62]`): active/status/presence/value fields.
No syntax, operator, group, template ID, PILOT target label or PILOT frequency enters the
reference.

For each TRAIN discriminating key, count how often each fact slot is teacher-valid.
At evaluation, among currently unknown facts choose the highest TRAIN count; ties choose
the lower local slot. No smoothing or fallback.

All **32** PILOT visible keys are present in TRAIN.

Registered PILOT discriminating result:

```text
missing2: 268 / 376 = 0.7127659574468085
missing3: 128 / 152 = 0.8421052631578947
macro:                 0.7774356103023516
```

This TRAIN-frequency reference is the formal comparator.

## Fixed deciding gate

Primary metric is the equal mean of target-hit rates for missing-count 2 and 3 on the
528 discriminating PILOT rows.

For **each of all 9** frozen-base / fresh-head combinations:

1. missing2 target-hit rate must be strictly greater than `268/376`;
2. missing3 target-hit rate must be strictly greater than `128/152`;
3. equal m2/m3 macro must be strictly greater than `0.7774356103023516`;
4. selected-observed count must be zero;
5. all raw unknown-fact logits must be finite.

All nine must pass. No average/best-seed/head rescue. A tie to the reference fails.

Secondary, non-gating:
- target hit on all 1768 PILOT NEEDS rows with missing2/3, including trivial all-valid rows;
- per semantic group;
- FIRST_UNKNOWN comparison.

## Workload

Registered values:

```text
frozen base checkpoints loaded = 3
base feature rows              = 3 x (3824 + 1768) = 16776
base feature forwards          = 18
base shared-cell calls         = 126

target heads trained           = 9
selector updates               = 18000
sampled TRAIN rows             = 4608000
PILOT selector predictions     = 9 x 1768 = 15912

actual acquisitions            = 0
network calls                  = 0
evidence writes                = 0
answer generation              = 0
proof checks                   = 0
production runtime change      = False
Gate E candidate               = False
```

## Interpretation boundary

PASS supports only this bounded statement:

> On the registered C174 development family, a learned selector built on frozen accepted
> C181 representations can choose an influential missing fact among multiple unknowns
> more accurately than the registered TRAIN-only syntax-blind frequency reference.

PASS does NOT establish:
- live learned target acquisition;
- learned tool/provider choice;
- retry, stopping or alternative action policy;
- repeated-variable, larger-expression or natural-language generalization;
- independent final confirmation;
- answer/proof generation;
- Gate E completion.

FAIL after valid execution is an **ACCEPTED VALID NEGATIVE** for this selector/hyperparameter/
representation combination. Do not increase width, updates or change the teacher after
seeing results before first auditing representation, target-set/error and split confounds.

Source/hash/schema/nonfinite/incomplete execution or accepted-parent replay failures are
**INVALID EXECUTION / RETRY SAME C188** with scientific conditions unchanged.

## Outputs

Exactly 14 artifacts excluding summary:

```text
target-selection-plan.json
target-teacher.npz
frequency-reference.json
selector-results.json
pilot-predictions.npz
selector-181001-188001.pt
selector-181001-188002.pt
selector-181001-188003.pt
selector-181002-188001.pt
selector-181002-188002.pt
selector-181002-188003.pt
selector-181003-188001.pt
selector-181003-188002.pt
selector-181003-188003.pt
```

## Protection / prerequisite

Parent C187:
- execution HEAD `bbb79df40f3428f358bec7381cd872efa7845e63`
- summary SHA256 `910a8a51c70a7ddfd996d99d21bcd9bc362ba568919ed04fb7305071d9142ccd`

C188 acceptance base:
`bdbc71ca17a7a6138f54d1188c17ce7dd33dcece`.

C188 inherits the complete C187 source/artifact chain, then protects the accepted C187
summary/artifacts and C188 source. Expected:
- historical source pins: 103
- protected paths: 239

Scientific manifest SHA256:
`0f8d22b00839e5a7506d5dabc06c64a7add86eb8a00e41840414842b7a773682`.

## Implementation validation before formal run

The exact new C188 benchmark module was compiled locally. **36/36 new unit tests pass**.
They independently enumerate the full registered C174 Boolean family for teacher/cohort
and reference counts, verify the exact 3824/528/1768 cohorts and both baseline results,
exercise set-mass loss, masking, deterministic paired target-head initialization/schedules,
toy optimization, fixed gate and scope.

This local validation does NOT include the repository's actual C181 checkpoint files,
historical protected chain, Windows PowerShell, or the complete regression suite. Formal
C188 remains unexecuted until the user runs the registered command.

Expected focused regression:
**1413 = 1377 existing + 36 new; 73 modules.**

Run `tools/run_c188.ps1` with C187/C186/C185/C184/C183/C182/C181/C180/C179/C178/C177/
C176/C174 summaries and the exact registered HEAD. Judge C188, update ledger/handoff,
then prepare at most C189 in the same response. Do not register C189 before C188 judgment.
