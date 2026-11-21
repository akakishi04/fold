# C266 preregistration — saved query-pair attribution

Experiment:C266-v5b-saved-query-pair-audit. Stage:V5-B-SAVED-QUERY-PAIR-AUDIT.
C265 ACCEPTED VALID NEGATIVE. C264/C263 bounded PASS and all older verdicts remain.
Gate E PASSED;Gate F NOT PASSED. C267 NOT REGISTERED.
Acceptance/base:92da414cec60028f813b8196f61b5a432f7c6b90.
Acceptance:docs/experiment-ledger-addendum-c265-c266.md.

## One question and stopping boundary

When only the queried compound identifier changes in C265's saved answers,do the two queries
collapse to one answer,swap their values,or fail differently? This is one descriptive saved-output
decomposition,not additional model inference,training,architecture repair or causal localization.
Include all20 states,all3 profiles,both languages,all subsets and both visible fact orders.
Conclude this single decomposition instead of extending an unbounded frozen-name diagnostic chain.
Any later training/architecture intervention needs a new separately registered scientific question.

## Source identity and actual parent dispatch

C265 execution:e0809d90c552471dee8723ce1b10528488f23be0.
Published log:4a51a286efcbe20336dba61699736e02ed51b5fa.
Publisher log SHA256:fb1c50a21c8829aef5a98dccbe189205006c127590fbe7eb9c418e59818fc025.
Summary:runs/c265-v5b-identifiers-755ab6d49ab84080ac18ff8f0699953f/summary.json.
Summary SHA256:f8c00bbcb311eeaf686ee43ef36d0597180e57c2bd70598d0fc23357c4da7998.
C264 source:runs/c264-v5b-two-fact-46c2297b66ba41a9b8f66f7bfca48935/summary.json.
SHA256:1c7e3d517bcf764f2b4eb89e432cb8ce303861359957f1fbfd77de9f19eb1503.
C263 source:runs/c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6/summary.json.
SHA256:1fcceab38de3e34a3858828285fd43503df9e455e2fdb3bd31524b5035813e21.
The two older summaries are inherited protected inputs,not newly counted files.

Parent artifacts are fixed in PARENT_ARTIFACTS and inherited verbatim from the acceptance record:
-eval-outputs.pt:546f5eb5dd62aa205c046fc5f2c7065837dc9ce578c79725c72ac451f87ae782;
-identifier-dataset.json:4bcc707da1814d765c4218f73203e175d092bea096becc593b789fbbcdb729bb;
-identifier-plan.json:1a6316f251e15e29e67d22eb2d6be02407a6fa4ea6a610759b332f5bd9de53a3;
-measurements.json:208943819e92e4f5cdd4f299668c86b14cba338180e1686ddd40d776b8315656;
-validation-summary.json:fd2e2028c442b651b740b7e0e82ea9e326750c0052b22a9d7b072486a2988bbd.

load_reference invokes actual C265.verify_artifacts(c265_dir,c264_summary,c263_summary,C265_EXECUTION),
FOUR arguments. This verifies the accepted saved outputs,older anchors,restoration and metrics.
Require its status FAIL,whole-model counts0 in all four arms,and exact profile counts:
doubled5/5/3/3,shared_prefix3/2/0/1,shared_suffix0/0/0/0 in standard_forward,standard_reverse,
lower_forward,lower_reverse order. Do not require the negative parent to have capability PASS.
Then read fold-c265-identifiers-eval-v1 from eval-outputs.pt. Analyze records[*].renamed[profile]
normal tensors,NOT the original-name anchor or restored tensors. Each view is288x256 CPU float64.
All three views must be finite and complete;masked outputs remain parent integrity evidence.
Source rows are the exact C264 metadata,hash8adacd9b13b87c9f6a2bd7e1bf0f735e9a1a63b521840ef301a855586643e6c1.
They supply target/group identity only;C266 has no model-input path.

## Exhaustive partition and accounting

Group by language,entity subset,value assignment and visible fact order. Each group contains the
two distinct queried entities in ascending original entity-index order. Targets differ. Classify
exactly one of six mutually exclusive outcomes from the two argmax byte predictions:
-both_correct:each query gets its own value;
-swapped:each gets the other entity's value;
-collapse_entity0:both return the first logical entity's value;
-collapse_entity1:both return the second logical entity's value;
-collapse_outside:both return the same byte not assigned to either displayed entity;
-other_different:unequal predictions not covered by correct/swapped (at least one outside value).
Here entity0/entity1 are offsets within the selected subset,not global a/b identities. Independently
record the selected global entity and its first/last displayed position for displayed-value collapse.
No collapsed outside answer is silently assigned a displayed position.

Also classify every answer as correct,other_entity,absent_digit(0..3 but not either displayed value),
or other_byte. Retain all categories and reconcile integer counts. Each pair contributes two answers.
Record the maximum absolute difference between the two full logit vectors and exact vector equality.
Same argmax does NOT imply equal logits,absence of query representation,or identical internal states.

Per profile144 pairs/288 answers per state. Total8640 pairs/17280 normal answers.
720 state/profile/language/subset/order cells,12 pairs/24 answers each.
120 state/profile/language summaries,72 pairs/144 answers each.
Reconcile every profile's correct-answer total and every cell's correct count and complete-query
accuracy against the actual accepted C265 measurement records. No new capability scoring formula
replaces the original verdict. Pair-attribution plus aggregates must account for every source row.

Keep doubled as matched descriptive reference for both collision profiles. Produce80 contrasts:
20 states x2 languages x2 collisions. Each uses all72 corresponding pairs. Additionally partition
the doubled-both-correct subset into retained,collapsed,swapped,other. Report that subset denominator;
when it is zero,the fraction is null,not zero or success. Full unconditional category tables remain.
This is not selection of good states or rescue of poor profiles. Conditional comparisons are not
independent samples,statistical significance tests,or internal-mechanism identification.

## Diagnostic gate and resource boundaries

PASS means all source validation,complete attribution,count reconciliation and persisted reattribution
succeeded. There is NO minimum collapse rate and no capability improvement gate. Evidence against the
collapse hypothesis is a valid diagnostic PASS too. capability_pass_claim=False,causal_parser_claim=False,
Gate F NOT PASSED. C265 remains negative. Do not tune categories or select profiles after reading outputs.

Scientific model forwards0,model-state loads0,learned-bundle loads0,training0,new learned checkpoints0.
The saved_only context blocks Module calls and forbids torch.load for learned or unknown archives.
It requires CPU weights_only=True for the evaluation archives. Actual parent validation plus explicit
C265 archive read performs6 archive loads per analysis pass:two C265,two C264,two C263 evaluation
archives. By basename this is4 eval-outputs.pt and2 evaluations.pt. Check actual calls rather than
claiming six without counting. Run and persisted postcheck are two passes,12 archive reads total.
These reads,hashing and historical tests are additional CPU/RAM/I/O work;zero new inference is not
zero computation. No claim about measured peak memory or wall-clock. No output tensor duplication:
new artifacts are JSON attribution/aggregates,not copied learned weights or raw tensor bundles.

Six ignored artifacts plus summary.json:audit-plan.json,pair-attribution.json,cells.json,
profile-summary.json,matched-contrasts.json,validation-summary.json. Postcheck reloads source archives,
recomputes all attribution and compares every persisted JSON value and hash/size. Only console logs
are published. All older files and learned artifacts remain unchanged;no cleanup or CI change.

## Protection and authoring gate

Inherit436 source pins/736 inputs;add OWN6 plus C265 summary+FIVE artifacts:442 pins/748 inputs.
Direct deciding dependency union42=five C231 LM sources,C230..C265 helpers and C266,including lazy calls.
OWN6:benchmark,own tests,runner,launcher,this preregistration,and design:
fold_lm/v05_benchmarks/model_c266_query_pair_audit.py;
tests_lm/test_v05_c266_query_pair_audit.py;
tools/run_c266.ps1;tools/invoke_c266.ps1;
docs/experiment-ledger-addendum-c266-preregistration.md;docs/v5b-query-pair-audit-v0.1.md.
Own24;modules151;loaded3550/focused3549. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:85be4d973b9f8ce8a59e1ffa9028faceb1de3fcc8d8b3035264c2af72ed88b3e.

Tests use synthetic saved logits and independently computed correct/query-pair counts,not trained
FOLD models. They exercise the actual new analyzer,partition,matched contrasts,loader dispatch,
archive/model-call guards,run orchestration and saved postcheck. The parent verifier is mocked;
its five simulated archive reads test child accounting,not the real historical import graph.
The dummy3550-ID suite tests the inherited exclusion,not execution of3549 historical tests.
Re-fetch committed OWN bytes,match tested blobs,execute exact own24 and compile/import/free-name,
manifest/count/CLI/parent-semantic review before activation. Record real limitations in the handoff.
Windows parser,full historical regression and real parent-artifact checks remain mandatory.
Integrity failures retry SAME C266;no C267 until judgment. Operational skips precede logs;repair
log-only publication failures without rerunning completed diagnostics. No paid API or external corpus.
