# C255 execution recovery — own-test exact-equality mismatch

## Invalid attempt

C255 attempt at scientific execution HEAD `70ca4c4c71f7e304d0a78313e642f5fdb57d4da2`
is **INVALID / RETRY SAME C255**. The published transport commit is
`372ef97671bdec0dc7db07e8dea456e60c7f2f02`; log SHA256
`d9db7508f1ad693884c4854121453375782d0f358855eda3f3164dbc22ddb285`.

Preflight/source/archive checks passed, then own tests ran24 and stopped with exactly one failure:
`test_07_coherent_control_matches_donor_not_recipient`.
Focused regression and the actual C255 diagnostic did not run. The final log records
`run_execution_valid=False`.

## Root cause

The registered C255 scientific replay contract is:
- raw-logit max absolute difference <=1e-9;
- exact argmax equality.

The benchmark implements this contract through `replay()`. The failing authoring test instead
used `torch.equal()`, requiring bitwise equality between:
1. donor logits computed in their original batch positions, then permuted; and
2. logits recomputed after permuting the saved donor rows before LayerNorm/decoder.

C255 `score_one()` had already accepted the same synthetic coherent controls through the registered
<=1e-9 replay helper, proving that the discrepancy was within tolerance with unchanged argmax.
The test therefore imposed a stricter, unregistered floating-point requirement than the science path.

## Minimal repair

Change only test07's coherent-control assertion from bitwise `torch.equal` to the existing
`b.replay(...)` helper and assert its returned error <= `b.TOL`.

Do NOT change donor mapping,model/head code,tolerance,seed,data,metric,workload,gate,or any accepted
parent file. No threshold was relaxed:the test is aligned to the preregistered tolerance already
enforced by the scientific code and postcheck.

Repair source commit:
`f10a493f5ea6a92f06bd3a0860444b69c64de5a1`.
New test blob SHA:`ac7cd0a8d3176ea87af0dd5eb8cc2b0f1104b9b5`.

C255 remains the only experiment eligible for retry. C256 stays NOT REGISTERED.


## Second invalid attempt — masked activation bitwise identity

A second C255 attempt executed from HEAD `275754bf58adbac6fdef92a34b6d2c309be0548b`
and published log commit `b7496ffd46c12d469e9478eed05d3c81b9c780dc`.
The published log SHA256 is
`933ccbc8613f06f94f9cc6184e052f5ed290b22b81b04ca48e76323fe3e25f34`.

This attempt passed:
- repository/source/archive precheck;
- all24 repaired own tests;
- all3289 focused regression tests.

It then entered the actual C255 diagnostic and stopped on model1 before any valid diagnostic result
was completed. The failure was:
`ValueError: masked fact-pair identity` from the evidence-blind negative-control guard.
The run ended with `run_execution_valid=False`. This is therefore another **INVALID / RETRY SAME C255**
attempt,not scientific evidence.

### Root cause

For evidence-blind paired rows,the rendered prompt is semantically identical because both fact
values are replaced by `?` while language,object order and query stay fixed. C255 preregistered a
negative control requiring those paired saved activations/output to replay.

The runtime guard implemented the activation part with bitwise `torch.equal(post[d],post)` and
`torch.equal(read[d],read)`. The accepted scientific replay contract elsewhere in C255 is
raw numeric replay within `TOL=1e-9` plus exact output argmax. On the authoritative environment,
the saved activations for identical evidence-blind prompts were not bitwise identical,so the
bitwise guard rejected the run before the registered output-level replay could be evaluated.

This is an integrity-harness numerical-representation issue,not a performance result. No threshold
on accuracy,seed,cohort,scientific metric or capability gate is involved.

### Second minimal repair

Keep the exact donor mapping,all five seeds,data,model/head source,metric/gate/workload and
`TOL=1e-9`. Replace only the bitwise activation identity check with max-absolute activation
difference <= the already registered `TOL`. Keep exact finite shape/dtype checks. The existing
evidence-blind output negative control still requires C255 self/value-swap logits to replay within
the same <=1e-9 bound with exact argmax.

The synthetic authoring assertion for this evidence-blind output control is changed from
`torch.equal` to the same `b.replay(...)` contract. The coherent donor control remains on the
same repaired replay contract from the first recovery.

Scientific benchmark repair commit:
`ff8dbe38a6cafa778d09e8f8237d2f5d7f984d18`.
Test alignment commit:
`7fdc5790a0b53c5b8aa5b171c85ed70e3f29dd88`.

C255 remains the only eligible experiment. C256 remains NOT REGISTERED.
