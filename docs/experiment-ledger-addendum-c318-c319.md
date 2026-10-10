# C318 formal acceptance — native branch diagnostic

C318 ACCEPTED PASS (DIAGNOSTIC INTEGRITY ONLY). C319 NOT REGISTERED here.
C316/C315 and other prior scientific verdicts stay unchanged. Gate F NOT PASSED.

## Evidence identity and execution validity

Scientific execution:f4624509c4311b3e7b04b3d861cfcb3e9d58bfd0.
Publication:3444c11cb68c85e35202f65f26ba258aaadc2c1a.
Metadata:docs/experiment-run-logs/c318/latest.json.
Metadata log SHA256:a217afd677f4af6d9aa93b90693bbfec6d48e639469b735d48b5cf10d2fafe5d.
Metadata log bytes:1251771 (working-console bytes;Git normalizes line endings).
Summary:runs/c318-v5b-readout-branches-bb278106ee824f26996434d7d895726a/summary.json.
Summary SHA256:5b838ca1420dc36b146ba4afa548d889f16172bd1d1705e4f5df97a5664c5203.
Own24 PASS;focused5173 PASS in711.118s;source754/protected1418.
All10 frozen states completed original/mean-only/last-only/original.
Both original replay errors0.0 for every state;all degenerate controls held.
persisted_readout_branches=PASS;run_execution_valid=True;tracked tree clean;HEAD preserved.
Publication changes only latest.json/latest.log. No training or new model checkpoint.
Review used the published receipt,score tables,reproduction rows and postcheck;the user's
large local tensor archives were not independently rerun in the assistant environment.

## Deciding local/masked pass counts

Order of lengths below:2,3,4,5,6. Each entry is number of all-gate passes among five states.
- Original two_to_four:[5,5,5,5,4];original one_to_four:[5,5,5,5,4].
- Mean-only two_to_four:[4,0,0,0,0];mean-only one_to_four:[2,0,0,0,0].
- Last-only two_to_four:[5,5,5,3,2];last-only one_to_four:[5,4,5,4,0].
Mean-only loses every scored length>=3 gate. Last-only preserves more short-length gates,
but not six reliability;original combined readout remains strongest by these pass counts.
Zero passing models is not zero correct answers. Keep native local/masked thresholds.
Example only,not a whole-cohort aggregate:one_to_four316005 six HOLDOUT English shared-suffix
48/48 correct originally ->42/48 in last_only (six regressions,no rescues). This shows a
context where removing the mean branch damages otherwise correct answers.

## Interpretation and next question

Do not adopt either frozen single-branch substitution. C318 changes a function trained with
both branches,so it cannot determine how a single-branch model would learn from initialization.
It does not identify universal branch necessity or independent additive causal contributions.

Proposed C319:train native mean-plus-last versus scale-preserving last-only from fresh paired
initializations under the same existing two_to_four training policy. The last-only calculation
must be used consistently during training,evaluation and strict checkpoint replay,with gradients
intact. No inference-only replacement after joint training. Preserve full parameter storage,
original total memory coefficient,optimizer,training data/budget and original all-gate metrics.
This is a proposed study,not authorization to run before preregistration/review/activation.
