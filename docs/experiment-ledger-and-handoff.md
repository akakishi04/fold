# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Accepted sources/tests/logs/preregistrations and protected dispatchers remain immutable.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C323 ACCEPTED PASS (DIAGNOSTIC INTEGRITY). C324 NOT REGISTERED.**
No ACTIVE experiment. Do not rerun C323 or execute historical launch commands.
C322 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY).
C321 remains ACCEPTED VALID NEGATIVE (interior-order 0/5); C320 remains bounded
ACCEPTED PASS (unequal lengths 5/5 mean_last); all earlier verdicts unchanged.
Latest accepted execution:1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4.
Latest accepted publication:e434a7ac6dd867e32f8135fc1b4c395e1644ffb9.

## C323 accepted evidence

Acceptance:docs/experiment-ledger-addendum-c323-c324.md.
Summary:runs/c323-v5b-fact-order-f1b710e74fbe495aba6410d0d9530248/summary.json.
Summary SHA256:fcc87597395300e45eacabaa94b87b6910093669532279f9ed6c67ec3f84af1f.
Log SHA256:ba9f788c326b6c4bc3a86a9d6bde542410fffa73d50c0d961707fd2a3980b8f8;
1072473 bytes. Uploaded log raw bytes exactly match published metadata.
Own24/full5293 PASS; regression1214.580s; failures0/errors0; exit0.
Source784/protected1478; saved reconstruction PASS; run_execution_valid=True.
Independent console audit:240 unique groups,4 exact overall reaggregations,
4320 counterfactuals,8640 question pairs,17280 normal answers. No rerun.
Old4 both arms:4320/4320 correct,1080/1080 four-correct,0/1080 all-four lock.
Interior mean_last:2211/4320 correct; first-both15/1080; last-both113/1080;
all-four same-output-class814/1080; four-correct29/1080; collapse1996/2160.
Interior last_only:2292/4320 correct; first-both29/1080; last-both95/1080;
all-four same-output-class809/1080; four-correct62/1080; collapse1951/2160.
Five seeds/both languages/three profiles/TRAIN+HOLDOUT are aggregated above.

PASS means valid diagnosis,not model capability. Interior names have equal endpoints
and character multisets but different internal character order. Same-output lock is
more common than consistent first/last fact-order following; not a causal mechanism
claim and not evidence that the complete logit vector is query-invariant.
Retain the logged runpy warning; science exit0 and separate persisted recheck passed.
Gate F remains NOT PASSED; no accepted source or checkpoint was changed.

## Next direction — C324 not registered

One-question candidate:can equal-budget exposure to interior-order name templates
improve held-out binding without losing original name-task performance?
Both arms should use native mean_last. Change only the length-four TRAIN templates
(original versus fixed C321 interior names),with paired fresh initialization and
identical logical rows/targets/order/exposures/optimizer/step count. Preserve original
length-two/three inputs. Evaluate interior and original task retention separately,
including query-pair,masked-evidence,masked-query and both-order criteria.
This would test learnability under explicit coverage,not frozen unseen-pattern
success. Exact seeds/workload/gates and full source/tests/launcher remain to be
registered and independently reviewed. No executable C324 command yet.

Before activation:read C319 trainer and C321 renderer/scorer writer-side semantics;
preserve all784 accepted pins/1478 protected inputs; add complete deciding-path
source protection and child artifact contracts; no new historical exclusions.
Separate acceptance from next-C registration. Do not mark authoring review PASS
without rereading committed remote source and verifying the executable paths.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

## Historical state

Pre-acceptance:docs/handoff-history/c323-pre-acceptance.md.
Git blob:101aedc81227c080b50c03d056b1c57d21de542a.
Earlier C322 evidence and C323 registration/review remain in that immutable snapshot
and the existing addenda. Only this Formal state is authoritative.
