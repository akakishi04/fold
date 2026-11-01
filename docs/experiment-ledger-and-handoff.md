# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md Current response format(v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Assistant authors/tests/registers; user executes locally. No Codex handoff.
Native Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5; PowerShell7 / ParseFile / active_v2.
Accepted sources/tests/contracts/logs/dispatchers remain immutable.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C341 ACCEPTED PASS (DIAGNOSTIC INTEGRITY).**
C340 remains ACCEPTED VALID NEGATIVE, candidate_gate=false / eligible_seed_count=2.
**C342 ACTIVE / NOT YET JUDGED.** C343 NOT REGISTERED. No production adoption.
Do not rerun accepted C341 or use a source-only HEAD as C342 ExpectedHead.

## Latest accepted evidence

C341 report: docs/experiment-ledger-addendum-c341-c342.md.
Acceptance commit: d8ab608b482d877a3927ef48b0f03a4212451aa1.
Scientific execution: a6a052912d52f786dd8c809ed6e8e96996c74edd.
Log publication: 69ac5ae2e6fb4e268b3ef0453a83c3ad9cd1ecdb; sole parent is execution.
6314 tests / 233 modules PASS; zero failures/errors/skips; 2343.503 seconds.
All 233 module begin/end records match and all 236 process exits are zero.
909 sources / 6723 protected inputs; all 6723 final uncached rereads; fresh verifier
complete; run_execution_valid=true. Scientific diagnosis used no new fitting/forwards.
Windows log425560bytes SHA5fd76fc01880f02b3d3f48e09b4f2e5282b3d9bbc1291c6898187222e0f066c2.
GitLF422456bytes reconciles exactly by CRLF reconstruction.
Ordered6314ID SHA3ee31f196c842e57f786d5efe1c22df5460d41ddc92b86cf40d8c9f56209ac76.

All 144 strata / 30 criterion transitions and all 116 failed rows reconcile.
Control75local/27order -> candidate10local/4order failures. Mask-only failures0.
Candidate340003original4: four new local/two order failures, all shared_suffix/ja/
entities[1,2], both splits/orders; original4 was absent from candidate fitting.
Candidate340002interior4: five persistent local/two order failures, including normal
TRAIN prompts actually fitted. Residual failure is not exclusively unseen-domain.
Candidate340004original6: one NEW local regression at HOLDOUT/shared_suffix/en/
entities[1,2]/order[2,1], accuracy7/8 and pairs3/4, both masked drops.625 pass.
All29control original6 failed accuracy/query-pair cells were rescued; the final one
is different. C340 full-candidate2/5 and accepted negative stay unchanged.
No mechanism, optimal curriculum, broad generalization or Gate F completion proved.

## C342 registration and authoring review

Preregistration: docs/experiment-ledger-addendum-c342-preregistration.md.
Source/preregistration HEAD: eb9ddb8388df4e2321b6b2e88769a827dd6cd09b.
Review: docs/c342-post-authoring-review.md.
post_authoring_review = PASS
Review target HEAD: eb9ddb8388df4e2321b6b2e88769a827dd6cd09b.
Independent reviewer fetched/read all seven remote files through EOF and matched
remote/tree/local blobs. Source commit has seven additions, no accepted-code changes.
Combined64 normal PASS65.235s / CP932 PASS65.540s, all failure/error/skip counters0.
UTF8/noNUL/compile/import/pyflakes PASS; 262 code objects / 1831 global loads, unbound0.
Actual6378/235 inventory and parent6314 ordered prefix verified; direct/lazy coverage
66files, uncovered0. PowerShell7.5.4 actual AST of dispatcher/launcher/runner PASS.
These authoring checks are not the native full suite, leases or scientific result.
Execute the clean documentation-only activation commit containing this handoff.
The final user command supplies that full commit as ExpectedHead.

## C342 one question, intervention and fixed gate

Stage V5-B-MIXED-LENGTH45-TRAINING. At fixed2400updates, does restoring original4
within original-family slot4 improve original4 retention against fresh original5-only
training while retaining original6 and each other gate domain?
Arms original5 / mixed45; fresh seeds342001..342005; orders342101..342105; five pairs.
Only original-family slot4 tokens change: whole-fit per-row original4/5 exposure
0/100 versus50/50. Original2=200,original3=200,interior4=100 remain fixed in both.
Original6, HOLDOUT logical rows and masked prompts never enter fitting.
Immutable C326 allocation on first-cycle original-family edges uses per-profile
length4 quotas8/8/9, then exact corresponding-event complement in cycle2(8/9/8).
Every candidate row receives25length4+25length5 per cycle; pair queries stay together.
No target/language/entity/profile/seed selection, fallback or result-dependent tuning.

Canonical192TRAIN/96HOLDOUT, templates/value split, event order/targets/family masks,
fresh paired weights, ordinaryCE256/native_before, capacity/rates/optimizer are fixed.
All five candidate states must pass original2..6 AND interior4 full gates. For EACH
seed and EACH of six domains require answer AND query-pair HOLDOUT gains>=0. Summed
original4 gains must be strictly positive for BOTH measures. Pooled retention cannot
hide a domain loss. Ties/perfect-control saturation are valid negatives, not retries.
This is a new original4-retention estimand and does not amend C340 or re-estimate its
six-transfer gain against original4-only. The mixture reduces original5 exposure;
its fixed ratio/temporal assignment are part of the intervention. Interior4 may stay
unresolved. No optimal curriculum, universal length claim or Gate F completion.

## Workload, protection and progress

10 fresh fits,2400updates/model,48rows/update, one continuous core_slow AdamW each.
14256parameters/core3328,64slots/paddedframes,CPUfloat64,twoTorchthreads.
Scientific totals:24000optimizer/gradient steps,1152000TRAINrows,27420model forwards,
1480320row presentations,109680core forwards,54840query projections,20state loads.
One checkpoint-bundle load/write,zero network calls. All fits finish before evaluation.
114views/state; native_before/all256argmax; exact argmax and1e-9 replay.
Actual tokens/model3225600control vs3168000candidate; actual int64le token/target
streams are recorded/reconstructed. Equal updates do not imply equal nonpadding/FLOPs.
Discarded preflight separately:16forwards/32rows/8backwards/0updates.

Full regression6378tests/235modules,own40science+24infrastructure. Before the sole
inherited exact C204 mutable-ACTIVE exclusion6379; no new skip/exclusion.
Full ordered-ID SHA76dfa4fd2952bdffd80250e57880d58cda72e7f7c16402c1817fed39ff294460.
916sources/7205inputs = parent909/6723 +475parentoutputs +7OWN; parent proofs469.
Finite lease max_files7205; all7205final uncached rereads. Successor retains481outputs.
Manifest538150bd2b43ff286e4d5b0e0c1d665ea1e1c4d43cf8148cba1c5d1a4192734c.

Parent folder runs/c341-length-gate-localization-eff5826958774979923f8d9aa67a1abf/.
Primary ec30706ed3761c7b36c4ef215a85c53ccc79cbd1ffb271a5b387fe2049b406eb.
Envelope6cc5988f3126f0b51a2d5543755cf58471e8839354e3dcf6bc86b7ce1f30ac8e.
Immediate parent C341.semantic_recheck(out341,out340,read) takes exactly3arguments.
C340 source folder runs/c340-length5-training-0c8af407e2564082b7221f1c95ddb709/.
C342 previous() remains C332; native preflight/run/semantic APIs take5/6/4arguments.

Route invoke_active_v2 -> invoke_c342 -> run_c342 -> c342_execution. Guards for
branch/clean tracked tree/ExpectedHead/uniqueACTIVE/dependencies/AST precede logging.
Standard user block parses dispatcher; dispatcher parses launcher; launcher parses
itself/runner. Stale invocation skips without science or publication.
Run prefix runs/c342-mixed-length45-<id>/; console log publication c342/latest.* only.
Expected phases: parent protection/semantics -> native_mixed_length45_preflight ->
6378isolated regression tests -> paired_mixed_length45_training -> saved evaluation/
replay/reconstruction ->7205rereads ->fresh verifier ->run_execution_valid=true ->log push.
Training prints seed/arm/every200updates; module progress and verification heartbeats.

## Completion and stop

Read remote docs/experiment-run-logs/c342/latest.json and latest.log after completion.
Distinguish metadata.execution_head from publication commit. Full valid execution
is required before judging candidate_gate. A scientific FAIL can be valid negative.
Integrity failure is INVALID / RETRY SAME C342; do not advance or relax the design.
Publication-only failure repairs the existing log push without retraining.
Freeze this experiment branch while the user executes; no unrelated remote commits.
After formal C342 judgment prepare C343 in the same reply under protocol v2; until
then C343 remains unregistered. No automatic retry, accepted-source edits or deletion.

## History and inherited compatibility seal

C342 pre-activation docs/handoff-history/c342-pre-activation.md.
C341 pre-acceptance docs/handoff-history/c341-pre-acceptance.md.
C341 authoring review docs/c341-post-authoring-review.md.
C340 acceptance docs/experiment-ledger-addendum-c340-c341.md.
C272manifest seal89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.
