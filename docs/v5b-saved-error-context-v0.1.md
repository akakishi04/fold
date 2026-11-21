# V5-B saved error-context audit — C311

The C310 saved-value-relabelling audit shows highly seed-specific failures. The majority of its
1,140,480 directed comparisons are consistent,but that number is not an independent sample size
and consistency cannot replace correctness. In particular seed309002's five-character saved
answers have violations under every training policy,also at trained lengths.

C311 makes the failure location explicit without changing the model:which ordered held-out
value pairs are wrong,are they wrong by selecting the other fact versus an absent value or a
non-digit byte,and are the same query answers already wrong at2/3/4 before unseen5?

Analyze the strict C310 saved argmax blocks. Preserve all15 parent models,original value split,
all three name profiles,English/Japanese,all256 possible outputs and exact original row IDs.
Reconcile720 parent totals;publish per-pair correct/error counts and four-length signatures.
This is diagnostic attribution by observed input factors,not evidence of a unique root cause,
new language capability or improved training stability. No new forward/training operations.
