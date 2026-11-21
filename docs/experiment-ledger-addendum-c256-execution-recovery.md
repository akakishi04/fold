# C256 execution recovery — incorrect manifest fingerprint and launcher-test formatting

## Formal state and invalid attempt

C256 is INVALID EXECUTION / RETRY SAME C256. C257 remains NOT REGISTERED.
C255 remains ACCEPTED PASS for diagnostic integrity only. Gate F remains NOT PASSED.

Failed scientific execution HEAD:1029158a60d40df24f599fb719411dbde2ffec06.
Published invalid log commit:2dc541041c772d5b9a449bd247862ad906a9b5c8.
Log path:docs/experiment-run-logs/c256/latest.log.
Publisher SHA256:5e774f0043a8f4661bbda08fe1ccaa8f728b1e10315947677d7ee6a40f62dce8.
Publisher log length:1008 bytes.

Python syntax preflight passed. The Python parent/task precheck raised ValueError: counts/manifest
at the combined source/input-count and manifest-fingerprint guard. Own24 tests, focused3313 tests,
and scientific training were not reached. There is no C256 capability result or checkpoint.
The precheck occurs before the runner's experiment try/finally, so this short log has no POSTCHECK
or run_execution_valid line; do not invent such a line. Invalidity follows from the exception and
failure phase. The log does not print the actual source/input counts, so do not infer them from
its ambiguous error message.

## Reproduced root cause

The complete failed-run benchmark was copied from connector-fetched source and mechanically matched
against Git blob 1f91f80d2ea74406fe236fd99fb1c60e2e5a2ae0 before execution in the review container.
Its real manifest()/blob()/digest() computes:

43948ceb676d536301d4e3a63a7ee1407f8bec44034db59f8b4f6e4872ae53b1

but MANIFEST_SHA and the preregistration had recorded:

31b433a189aee26a02d11d1571300b216f21ceb205d3696f90fe95d02bb20a7c

Thus the manifest condition is independently proven false, regardless of the unprinted count values.
The prior handoff/conversational assertion that the manifest fingerprint had been confirmed was
incorrect and is superseded by this executed check. This was an authoring/review defect, not a
user command, GPU, model-capability or floating-point-tolerance issue.

The unchanged dataset independently regenerates to its correct registered hash:
ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b.
TRAIN144/HOLDOUT144, all marginals and maximum22-byte prompt length are unchanged.

## Additional defect found before issuing another retry

Executing the original24 own tests in the review environment produced22 passing tests, one failure
(test01 manifest fingerprint), and one error (test24 launcher ordering).
Test24 searched for the literal '$failure = $null', but the actual launcher contains '$failure=$null'.
The search raised ValueError: substring not found despite the parser being in the correct location.
This independent formatting-only defect would have stopped the next run after repairing the hash.
It was reproduced and repaired before returning another user command.

## Minimal recovery; scientific conditions fixed

1. Correct only the recorded MANIFEST_SHA to the actual hash of the existing manifest payload.
   The generated manifest JSON is byte-for-byte identical before and after the repair.
   Do not assign MANIFEST_SHA dynamically from the running manifest or bypass hash checking.
2. Split the ambiguous counts/manifest condition into a tested validate_registration helper.
   Print observed source/input counts and computed hash; reject either mismatch with a separate
   expected/actual message. The requirements remain382 source pins and623 protected inputs.
3. Expand existing test01 with rejection cases for missing pins/inputs and a deliberately wrong
   fixed manifest fingerprint. Test count stays24; no regression test is removed or excluded.
4. Make test24 locate the failure-variable assignment with a whitespace-tolerant regular expression.
   It still requires ParseFile before that assignment. The actual runner/launcher are unchanged.
5. Correct the fingerprint in the C256 preregistration and document this invalid attempt.

No changes to manifest fields, dataset bytes, model classes, seeds256001..256005, candidate/control,
800 updates/model, batch48, optimizer, sampler, metric definitions, thresholds, replay tolerance,
checkpoint semantics, historical sources/tests/logs, or scientific forward/row budgets.
C256 remains10 models,8000 updates,384000 training presentations,8120 forwards,401280 total rows.

Source repair commit:1a03d784c97d8190cd9c527b3aa498ea3b4027a1.
Test repair commit:d05ed16a733c693e8cb14783d40c47f48af55bae.
Registration correction commit:4afbfbe60417d228b6268b2652d536f3b67206f6.

## Executed post-repair review

post_repair_review = PASS
Review HEAD:4afbfbe60417d228b6268b2652d536f3b67206f6.

Source/test were re-fetched after publication. Complete locally executed file bytes matched the
returned Git blob identities:
-benchmark:56968388f643d8929f8911d93dfc4301941bd924;
-tests:a3e1c67d7f0d625cbc30f4e27936268adaef426e;
-unchanged runner:46bbd0365002aecc1248f74887c7b3f0d205d744;
-unchanged launcher:f6e3069c3d9526c3bc012dadf6d1e5f609b7fdae.

Actually executed:
-Python compile/import; recursive symbol-table audit:zero unresolved globals in source and tests;
-manifest payload byte identity before/after, corrected fixed-hash match, exact dataset regeneration;
-AST comparison:all pre-existing benchmark functions except precheck are unchanged;the only new
 function is validate_registration. This includes unchanged manifest,fit,metrics,run and replay;
-24 repaired own test methods:24/24 PASS before publication in0.836s and after remote readback/blob
 matching in0.787s;
-manifest/count negative tests, initializer/capacity/gradient tests, real GRU/core/reader computation
 excerpts on untrained models, evaluation/state-preservation and checkpoint-logit replay;
-three embedded Python blocks compiled, argument indices checked, parser-order assertion passed;
-constructed3314-ID filtering test yields3313, preserving the exact historical exclusion.

Scope must remain explicit: the complete C256 benchmark/test files and both scripts are exact
blob-matched copies. The reviewer-only b.context wiring substitutes namespaces assembled from
retrieved C231 factory, language_task, modules, C248 reader and C252 wrapper computational excerpts.
This uses the actual GRU/MLP/reader computation, not a toy linear replacement, but is NOT the full
historical repository import graph. Parent artifact validation/audit adapters are not exercised by
those24 methods. The regular repository test file itself retains its original real b.context call.

Reviewer runtime:Python3.13.5,PyTorch2.10.0+cpu,NumPy2.3.5. github.com/raw.githubusercontent.com DNS
resolution failed in this container; PowerShell is unavailable. NOT executed here:the complete3313
historical suite,Windows ParseFile,the user's protected parent files through the complete precheck,
or the formal10-model800-update C256 learning run. These remain mandatory on the authoritative
retry. The failed-run actual count values were not retroactively fabricated.

Only recovery/handoff documentation follows this review. Verify the final branch HEAD before
returning the retry command; do not advance the branch during the user's run.

## Stop

Retry the same C256 only. Do not register C257, suppress prechecks, loosen gates, substitute seeds,
change datasets, extend the budget, or reset the user's repository. Any remaining integrity fault
stops C256. A later complete execution-valid scientific FAIL remains an accepted negative, not a
reason for an unregistered rerun. Preserve the invalid log in Git history.
