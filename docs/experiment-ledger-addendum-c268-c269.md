# C268 acceptance and C269 query-span boundary

## Formal verdict

C268 ACCEPTED VALID NEGATIVE. The preregistered candidate `ce_pair_margin` passed 3/5 seeds,
not the required 5/5. The matched `ce_only` control also passed 3/5. Candidate pooled HOLDOUT
accuracy improved only descriptively from 1100/1440 to 1115/1440 while same-answer collapse changed
from 114/720 to 107/720; neither pooled metric replaces the all-five-seed gate. Gate F NOT PASSED.
No optimizer, loss, architecture or production default is adopted from C268.

Scientific execution HEAD: aa45ea5df68dcba70c99a009c46b7bf8468304a1.
Published log commit: 1c93db5f8d48e47074ef20e2ce72ba506fe3c660.
Publisher log SHA256: 75941f645021d15bcef12577e6dd78f390c3b8a73de776cc47e38b09a4e2f4bb.
Publisher log bytes: 1077720; Git LF blob: cc8e970a8515396b313e138aee284243a0492b92;
4934 newline-terminated records after checkout normalization.
Summary: runs/c268-v5b-query-loss-9f62513c65d34a7aa7b1452c9540a5a6/summary.json.
Summary SHA256: 9e9ea4dd0d20b0ae0b8d315549a1cf1aa13c79853b3dd129c0f01e395a2bf67c.

The earlier C268 attempt at 8c464589b7f9e339b1a8d195b2d73d35c1279e39 remains an
INVALID execution record. This accepted verdict applies only to the recovered execution above.

## Execution validity

The recovered run passed the exact inherited source/artifact precheck with 454 source pins and
774 protected inputs. C268 own24 passed in 12.527s. Focused3597 passed in 320.666s, with only the
preregistered inherited C204 exact exclusion. Ten models completed 800 updates each: 8000 updates,
384000 training rows, 8540 model forwards, 435840 row presentations and 34160 core calls.
One 10-state bundle was written/loaded; 10 strict state loads completed. all_pairs_matched=True;
all_replays=True. Persisted paired-loss reconstruction passed, tracked tree stayed clean and the
scientific execution HEAD was preserved. `run_execution_valid=True`; `scientific_status=FAIL`.
This is therefore a valid capability negative, not an execution failure.

## Deciding HOLDOUT metrics

Primary fixed gate: all five `ce_pair_margin` seeds must satisfy every existing TRAIN/HOLDOUT,
profile, language, entity-subset, visible-order, answer-cell, query-pair, masking and two-order
criterion. Candidate passed seeds 268001, 268004 and 268005; failed 268002 and 268003. The control
passed the same three seeds and failed the same two. Thus `candidate_gate=False`.

Pooled descriptive totals across five seeds and both languages:

| profile | CE-only correct /480 | pair-margin correct /480 | CE-only collapsed /240 | pair-margin collapsed /240 |
|---|---:|---:|---:|---:|
| doubled | 367 | 375 | 38 | 33 |
| shared_prefix | 366 | 369 | 38 | 35 |
| shared_suffix | 367 | 371 | 38 | 39 |
| all | 1100 /1440 | 1115 /1440 | 114 /720 | 107 /720 |

The +15 correct answers are concentrated entirely in seed268003. Seed268002 has 145/288 correct
in both arms; collapse changes 70->67. Seed268003 changes 91->106 correct and 44->40 collapse.
Seeds268001/268004/268005 are perfect 288/288 with zero collapse in both arms. The candidate therefore
shows a bounded average improvement on this cohort but no improvement in preregistered pass count.
Shared-suffix collapse is not uniformly reduced: pooled collapse is 38->39 there.

At update800 every arm reports a near-zero training CE and the reported pair penalty is 0.0.
That does not rescue HOLDOUT failure: the preregistration explicitly states that a zero pair-margin
penalty can coexist with wrong answers.

## Scientific interpretation

Directly encouraging opposite relative preference for the two queried targets is insufficient to
make held-value binding reliable across fresh initializations under this fixed paired-batch training
policy. The output-space margin can be fully satisfied on TRAIN while two states still miss the
strict HOLDOUT criteria. This narrows the immediate engineering hypothesis: the remaining failure
is not fixed merely by adding this particular pairwise output-margin term.

The result does not prove that pairwise objectives are generally useless, that optimization is the
only problem, or that the internal query representation is absent. It also does not show that the
paired sampler itself improved C267, because both C268 arms share that sampler and fresh seeds.

## Confounds / non-claims

C268 is a small authored symbolic task family with TRAIN-seen identifier profiles and a structured
held-value split. It is not unseen-name transfer, arbitrary-string understanding, general language
ability or a population benchmark. The candidate changes gradient direction under global clipping,
so even a positive result would not isolate a single internal mechanism. Pooled correlated rows are
descriptive rather than independent replications. Do not retune margin2.0, coefficient0.1, seeds,
budget or thresholds after this result to convert it into a PASS.

## Accepted artifacts

- loss-plan.json: cf16b504aa03e1e5f61c000c161b44c3a551fe7c103096c9119274947fb4e07b; 2492 bytes.
- dataset.json: 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1; 36024 bytes.
- trained-models.pt: c4f7bfa9a38bffe871efda54dc9c06d0f82b8acf2b84b42344d6417455daba47; 1238007 bytes.
- evaluations.pt: 59a17ceb9d228ff4472394b2e9ef11bcf30d5e6d0c448163ac325dc7b10cc6d6; 53143359 bytes.
- measurements.json: b95667f0de648574afacab38ef21fa1d24d0ba9945ff504eba04f5c4e4f8a00e; 261557 bytes.
- validation-summary.json: 2b20b57ccd87057405dd11600854d538b5ff933907665ee3c787243a4d96e209; 7000 bytes.

## Next question, not activation

C269 should test one structural question rather than another post-hoc loss rescue:

**With the same paired CE-only training, does replacing the current pre-core EOS query vector with a
visible query-span pooled pre-core vector improve reliable held-value binding across five fresh
seeds?**

The candidate may identify the query span only from visible delimiter bytes already present in the
input: bytes strictly after the final ';' and before the final '='. It must not receive entity ID,
target, split, profile or pair metadata. Pool all byte positions in that span so UTF-8 identifiers
are handled as their visible byte sequence rather than assuming a two-character or ASCII-only name.
Keep the pre-core memory states, learned query/key/output maps, post-core residual, parameter count,
dataset, profiles, paired sampler, CE objective, optimizer and 800-update budget fixed. Compare
against the unchanged C252-style EOS-query reader from exactly matched fresh initial weights.

This is a bounded structured-input architecture test. Even a PASS would not establish a general
parser or authorize production adoption. C269 requires separate preregistration, implementation,
committed-byte review and activation. C270 NOT REGISTERED.
