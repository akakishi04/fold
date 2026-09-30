# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C289 ACCEPTED VALID NEGATIVE. C290 ACTIVE / NOT YET JUDGED. C291 NOT REGISTERED.**
Scientific execution:b5026f48e0c8b39bbfb9069f34271d7b6ba9d50f.
Published log:b96ab8b01ec9c9eb876fada8339c8c0e0d0a8e12.
C288 remains ACCEPTED VALID NEGATIVE. C287 remains diagnostic ACCEPTED PASS.
No C289 rerun,seed exclusion,threshold relaxation or Gate F promotion.
C290 is the unique ACTIVE saved pair-margin/correctness diagnostic.

## Latest accepted science — C289

Acceptance:docs/experiment-ledger-addendum-c289-c290.md.
Acceptance commit:4ffae6420500e0233c1b19df07f6f0cfac73c16d.
Summary:runs/c289-v5b-early-pair-ac332442137243e68d4ec3bd754ba717/summary.json.
Summary SHA256:151117fcd43177b8e393eeee6935222e54f01caecf8a17b4656149aec5058897.
Manifest SHA256:48b33a7ed29cf9ded858753d5f64210006f559ef428c167e912621a71896ae21.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False;
all_auxiliary_prefixes_matched=True;persisted reconstruction PASS.
Own48/focused4205 PASS;source580/protected1041;15 models and12000 updates.
Quad ce_only3/5,pair_always0/5,pair_early0/5.
Two/three full3/4/4;fitted TRAIN direct4/5/4;seen HOLDOUT direct3/4/4.
CE passes quad289003..289005;both auxiliary arms fail quad for every seed.
On289002 both auxiliary arms pass seen tasks but miss one quad HOLDOUT answer.
On289001 early withdrawal loses the trained-length TRAIN direct pass retained by always-on.
Equal full-gate counts do not imply identical individual outputs. No further loss/switch tuning
is registered. The next diagnostic compares margin attainment with actual answer correctness.

## Active C290 — saved pair margin versus individual answers

Experiment:C290-v5b-saved-pair-margin-audit. Stage:V5-B-SAVED-PAIR-MARGIN-AUDIT.
Registration:docs/experiment-ledger-addendum-c290-preregistration.md.
Design:docs/v5b-saved-pair-margin-audit-v0.1.md.
Review:docs/c290-post-authoring-review.md.
Acceptance base:4ffae6420500e0233c1b19df07f6f0cfac73c16d.
Authoring/review target:9ad25da5fef6b8458f14a45a61e453ceea9551e8.

One question:does the existing auxiliary assignment margin coincide with both individual answers
being correct in C289 saved outputs,and which aligned answers change after withdrawal?
Retain15states,all5seeds289001..289005,ce_only/pair_always/pair_early,all2/3/4 tasks and value splits.
No architecture,weights,data,training policy or gate changes. Read old final normal logits only;
the exact parent verifier still reconstructs every original masked/full gate and matching invariant.
Exact C289 summary SHA and source pin commit all8 artifact descriptors and15 ancestor summary hashes.
All16 summary hashes are verified before the correct parent loader is dispatched.

Reconstruct19440 query-pair records. Compute the original grouped-sum assignment gap D and
softplus(1-D),independent256-class predictions,0/1/2 correct answers,collapse and normal NLL.
Margin D>=1 is descriptive only;do not replace accuracy/query-pair/two-order/mask gates.
Report90 final model/task/split aggregates and60 early-versus-CE/always comparisons covering12960
matched pairs. Keep exact individual argmax changes,rescues and regressions;equal gate counts alone
are not evidence of equal predictions. Pair records are dependent observations,not extra seeds.

Scientific model forwards,row presentations,core calls,training,model-state loads,new checkpoint
writes and network calls are all0. Reading old logits and numerical scoring is permitted. Neural
Module calls,load_state_dict and torch.save are blocked. PASS means diagnostic integrity only;
capability_gate_applicable=False. C289 and Gate F remain unchanged regardless of diagnostic values.
Outputs:audit-plan.json,pair-margin-report.json,validation-summary.json,plus full summary.json.
Console uses a compact validated receipt and aggregates;full maps and per-pair details remain local.
No old logger or published log is edited. Use the summary hash and exact parent verifier for children.

Registration:source586;protected1056;dependency-union66;own40;modules175;loaded4246;focused4245.
Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:123a8805343a6c7704ff6042d83928d3069aa43fe79e213e2b5798811d35b6f3.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (committed-byte/static plus local fixture own40).
Review target:9ad25da5fef6b8458f14a45a61e453ceea9551e8. All6 OWN files fetched after commit;
whole-file Git blobs match compiled/tested local bytes6/6. Post-match own40 PASS in4.844s on
Linux/Python3.13.5/PyTorch2.10.0+cpu. Python and3 embedded blocks compile;unresolved custom globals0.
Fixtures exercise full19440-pair analysis,paired changes,16 hash rejections,source/input maps,
run ordering,persistence/tampering,and cancellation-sensitive parent margin arithmetic.
Parent archives/Git/inherited scorers are mocked where required;this is NOT actual C290 science.
Real parent data/pins,full4245 regression,PowerShell ParseFile and user-local saved-output
reconstruction remain mandatory runtime gates. Reviewed OWN6 must not change at activation.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected order:legacy_dispatcher_pin=PASS -> active_experiment=C290 -> Validate(parent/source/input
586/1056,real complete pair-analysis dry-run,own40,focused4245) -> authoring_runtime_preflight=PASS ->
Execute(saved margin/correctness and exact prediction-change audit;zero new model calls) ->
persisted reconstruction -> log publication.
Validate failure skips science/publish. Integrity failure retries SAME C290.
Do not register C291 before C290 judgment or change any prior seed,loss,margin or gate.
C289 log exceeds1MiB:use its immutable Git blob and small result-resource line ranges when a
Contents fetch returns empty. Never equate publication or empty content with successful execution.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep this accepted legacy seal. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoffs are preserved under docs/handoff-history/c280-pre-acceptance.md through
c289-pre-acceptance.md. The latest preserves Git blob c8aef6cc095ecfc40e096be53000add62c5c552d.
Only this Formal state is authoritative;historical ACTIVE instructions are not executable.
Accepted source/tests/preregistrations/logs and protected dispatchers remain unchanged.
