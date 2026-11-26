# C346 acceptance and C347 saved loss-transition question boundary

Review date: 2026-11-26 Japan time.

## Formal verdict

**C346 ACCEPTED VALID NEGATIVE.**
The documentation recovery completed a valid execution using the unchanged
C346-R0 executor. The fixed half-rate pair-max candidate failed its registered
gate: candidate_gate=false, eligible_seed_count=0. This is scientific negative
evidence for the fixed policy and budget, not an execution error.

C346 attempt01 remains INVALID. C345 remains accepted diagnostic evidence and
C344 remains ACCEPTED VALID NEGATIVE. Gate A/B PASSED; C/D PASSED in measured
scope; E PASSED; F NOT PASSED. No production adoption or broader capability claim.

## Identity and evidence scope

| Item | Value |
|---|---|
| Scientific execution HEAD | `622e623faa0c3c698a18033eb8b4bca554088918` |
| Published log commit | `426c52f9f33f2465e8b1cd1879182558b443f660` |
| Publication ancestry/scope | Sole parent is execution HEAD; only C346 latest.log/latest.json |
| Git log blob | `421ecd1125928ad8a4700dbff6ad29ba605b57f5` |
| Git metadata blob | `a08e7a62b6c7105de6eaf1948b0ffa0b05c0e685` |
| Git LF log | 615,757 bytes /4,426 LF |
| Git LF SHA256 | `2143d307891774f4149660ea0c2896f8095f1542aeb213c31da7c6df486d88f2` |
| Original Windows log | 620,183 bytes |
| Original SHA256 | `ede8f82041571f5481eeaa1dfbbc22c395ad71df0d67b73cd2decf118a2ee338` |
| Run folder | `runs/c346-pair-max-rate-68993e9eaa4e410886dbe0d24a3def3c/` |
| Primary summary SHA256 | `d06fa2a06287696424ac58e3d56e7262282caca81b028f61709f609ab728e816` |
| Execution envelope SHA256 | `b8b57583363d61aca10d947c891de0d8b3d8b2319e659652cacf101a334e3c3d` |
| Manifest | `8dad5562249bf21517bb8487c5c6970ac75b55405252dbbf5c3512d797d46d64` |

CRLF reconstruction exactly reproduces the original metadata size and SHA256.
The seven C346 OWN blobs remain identical to original source registration
`be76c4c53c36105638e59e059af241078758b628`. Attempt01 archives remain unchanged.

The public records contain all15 seed/arm results,180 normal summaries,10 paired
seed/control records,120 normal contrasts,180 terminal-loss summaries and120
terminal-loss contrasts. Their coordinates, counts and fixed gate can be
reconstructed and checked using the pinned C346 `check_summary()`.
The root's canonical reconstructed validation-summary SHA256 is
`16768a9a7994d8f9e6c4f7202a886c1bbf77422364e0a05f8c0a00b52d488325`.
The integrity fields paired_conditions_valid/all_replays/evaluation_policy are
attributed to the native verifier contract; they are not independent raw-tensor
measurements performed by the reviewer.

The complete primary/envelope, user-native tensor artifacts, source/input maps
and individual module receipt files were not fetched. The primary SHA above is
the published native identity, not a reviewer reconstruction of unexposed bytes.
Individual successful test IDs inside receipts and saved raw semantic replay were
verified by the pinned native verifier. The reviewer rebuilt the actual ID plan
and checked all public module counts, ordering, exits and final attestations.

## Execution validity

Full6,652 tests /243 isolated modules PASS in3,340.151 seconds, with zero failures,
errors or skips. All246 process exits are0. The actual loader inventory and
6,578-ID ordered C345 prefix match the log. Only the inherited C204 exclusion remains.

Full ordered-ID SHA256:
`39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394`.
Parent ordered-ID SHA256:
`2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a`.

Six native cleanup checks passed with the immutable C344-R1 receipt bound to
this C346 execution HEAD. Native locks,944-source/9,177-input registration,
parent saved semantics and the numerical preflight passed. The discarded
preflight has24 forwards/96 rows/12 backwards/zero updates.

All15 expected fits reached2,400 updates before the first cohort evaluation.
Saved evaluation/replay covers all15 states. Measured WORK equals the sealed
contract:36,000 updates/backwards,1,728,000 training rows,41,130 model forwards,
2,220,480 total row presentations,164,520 core calls and82,260 query calls.
All9,177 final uncached rereads and the separate fresh verifier completed.
The terminal status is `run_execution_valid=true`.

## Deciding metrics

| Arm | Full original-plus-interior gate | Interior gate |
|---|---:|---:|
| Ordinary mean CE | 2/5 | 2/5 |
| Default-rate pair-max | 1/5 | 1/5 |
| Half-rate pair-max candidate | **0/5** | **0/5** |

The candidate also fails the original6 gate in all5 seeds. These full gates
include all registered conditions; they are not thresholds on pooled accuracy alone.

| Fixed candidate condition | Result |
|---|---|
| All five complete candidate gates | FAIL;0/5 |
| Every answer/pair nonregression vs default pair-max | FAIL;68/120 inequalities pass |
| Every answer/pair nonregression vs ordinary CE | FAIL;64/120 inequalities pass |
| Four strict pooled interior gains vs default pair-max | FAIL;all four are negative |

| Interior normal results | Mean CE | Default pair-max | Half-rate pair-max |
|---|---:|---:|---:|
| TRAIN correct answers /2,880 | 2,824 | 2,471 | 2,254 |
| TRAIN both-query-correct pairs /1,440 | 1,384 | 1,036 | 827 |
| HOLDOUT correct answers /1,440 | 1,395 | 1,188 | 1,018 |
| HOLDOUT both-query-correct pairs /720 | 683 | 516 | 396 |

Candidate minus default pair-max: TRAIN -217 answers/-209 pairs;
HOLDOUT -170 answers/-120 pairs. The comparator had positive headroom at all
four endpoints: TRAIN409 answers/404 pairs;HOLDOUT252 answers/204 pairs.
The failure is not caused by a perfect-control ceiling.

## Seed differences and scientific interpretation

| Seed | Interior TRAIN answers: default to half /576 | Interior HOLDOUT answers: default to half /288 |
|---|---:|---:|
| 346001 | 494 to437 | 237 to190 |
| 346002 | 287 to379 | 108 to156 |
| 346003 | 572 to517 | 285 to259 |
| 346004 | 542 to379 | 270 to146 |
| 346005 | 576 to542 | 288 to267 |

The half-rate policy worsens interior answers in4/5 seeds in each split;346002
improves relative to a severely deteriorated default pair-max run. In that
default run, all six HOLDOUT domains have108/288 correct answers and0/144
both-query-correct pairs. This pattern is descriptive; it does not identify an
internal cause or establish constant predictions without inspecting saved logits.

Half-rate interior answers are below ordinary CE for every seed in both splits.
Original6 pooled answers improve relative to default pair-max (TRAIN2582 to2765;
HOLDOUT1255 to1369), yet remain below ordinary CE (2873/1428). A domain aggregate
improvement does not satisfy the fixed per-seed, per-domain retention conditions.

The supported conclusion is narrow: halving both constant rates from initialization,
under this objective, architecture, five seeds and2,400-update budget, did not
improve binding with the required retention. It does not establish that every
smaller rate is harmful, that a longer run would succeed, or that capacity,
clipping, gradient starvation or nonconvergence caused the failures.

## Loss and exact correctness are not interchangeable

These loss means weight normal answers/query pairs within the indicated domain
and split equally across the five seeds. They are not the exposure-weighted
whole-mixture training objective.

| Interior terminal loss | Mean CE arm | Default pair-max | Half-rate pair-max |
|---|---:|---:|---:|
| TRAIN mean CE | 0.038280522 | 0.228509936 | 0.356191183 |
| TRAIN pair-max | 0.062341004 | 0.296324170 | 0.502718800 |
| HOLDOUT mean CE | 0.107369740 | 0.993879073 | 0.786599756 |
| HOLDOUT pair-max | 0.194339660 | 1.774960732 | 1.224536909 |

On interior HOLDOUT, the half-rate aggregate has lower mean CE and pair-max
loss than default pair-max while losing170 answers and120 complete pairs.
Seed346001 also has lower both losses but47 fewer HOLDOUT correct answers.
Consequently the aggregate mismatch is not only a claim about one pooled mean.
The current summaries do not tell how much each rescued, regressed or unchanged
correctness group contributes to the loss difference.

This differs from C345's C344-cohort observation that all10 interior seed/split
comparisons had higher candidate losses. C346 uses fresh seeds and a different
rate comparison; do not combine the cohorts as if their numerical deltas were
paired. No objective-by-rate factorial interaction is identified because there
is no half-rate mean-CE arm.

## Repository update and preservation

The pre-acceptance handoff is preserved at
`docs/handoff-history/c346-pre-acceptance.md`. Attempt01 and its documentation
recovery remain at the existing archive/recovery paths. The permanent C272 seal
must remain in the authoritative handoff; acceptance must not repeat its deletion.
The C344-bounded cross-experiment synthesis remains an unchanged historical
snapshot; this acceptance is the later C346 evidence update.

The native run and all497 outputs must remain available:6 science files,primary,
envelope,and489 proof files. Do not rerun accepted C346 or substitute attempt01.

## Next one scientific question — not registration

**Which matched correctness groups account for lower terminal loss coexisting
with worse exact answers/query pairs under the half-rate policy?**

Proposed C347: saved-only loss/correctness-transition decomposition of all15
frozen C346 states,all5 seeds,6 domains,2 splits and both controls. Recompute
normal per-answer CE and canonical pair-max losses from saved full256 logits.
Partition matched comparisons by both correct,regressed,rescued,and both wrong;
also retain the pair same-answer-collapse partition as a secondary description.
Reconcile the signed loss contribution of every group to the already accepted
aggregate loss difference and exact answer/pair rescue/regression counts.
For a pair,correct means both query answers are correct;its failing category
includes one-correct pairs and does not mean both answers are wrong. The three
partition families reuse the same observations and are not added together.

Here a transition is a cross-arm terminal comparison,not a temporal learning
transition. Keep all groups,including explicit empty groups,with no selection
of favorable seeds or cases. No training,new model call,gradient,optimizer update,
model-state load,new checkpoint or desired-sign gate. Diagnostic PASS establishes
coverage/arithmetic/provenance only and preserves every C346 negative subgate.
It does not repair predictions or explain the causal optimization mechanism.

This acceptance does not register C347. Its source/tests/executor/launchers and
preregistration must be committed separately and independently reviewed from
complete remote bytes before activation. C348 remains unregistered.
