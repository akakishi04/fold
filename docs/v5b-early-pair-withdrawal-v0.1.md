# V5-B early pair-loss withdrawal — C289

C288's auxiliary trained all5 models to exact answers on fitted lengths2/3,but quadruple all-five
reliability worsened:CE3/5 versus pair1/5. Pooled four-character correctness nevertheless improved
3902->4011/4320 and collapse175->90/2160. Neither result should hide the other. Trained accuracy,
held-out value generalization and unseen-length reliability are different observations.

C289 asks whether pair supervision can be useful early without remaining active for all800 updates.
It compares ce_only,pair_always,pair_early on5 fresh matched seeds. The pair_early candidate uses the
same C288 coefficient.25 and margin1 for the first400 steps,then exact CE. Pair_always retains the
auxiliary;ce_only supplies a concurrent no-auxiliary anchor. All3 receive the same data,LR,capacity
and800-update budget. Always/early share an auditable exact400-step prefix. AdamW is never reset.

This does not presume that late auxiliary pressure caused C288's failures. By later updates the
auxiliary may be nearly saturated,so withdrawal may do little. Conversely it may discard useful
learning. Changing duration also changes integrated auxiliary weighting. We test this specific
policy,not a unique causal decomposition or a retrospectively tuned schedule.

Three arms are intentional:using only always-on as the control could make early withdrawal look
helpful while remaining worse than ordinary CE. The same-seed CE anchor prevents that omission at
50% more total work than a two-arm test;each arm still receives the same800 steps. Report both
comparisons,absolute quad gates,all tasks and90 final TRAIN/HOLDOUT partitions in one result.

No new architecture,training example,inference metadata or extra neural forward per model is
introduced. Generated weights/data stay local-only. A candidate PASS does not prove arbitrary-length
reasoning or automatically close Gate F. A valid miss is evidence,not permission to change this C.
