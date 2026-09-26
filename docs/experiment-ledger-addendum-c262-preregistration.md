# C262 preregistration — paired minibatch chronology

Experiment:C262-v5b-paired-minibatch-order.
Stage:V5-B-PAIRED-MINIBATCH-ORDER.
C261 ACCEPTED VALID NEGATIVE;all earlier verdicts remain. Gate E PASSED;Gate F NOT PASSED.
C263 NOT REGISTERED. This registration is separate from C261 acceptance.

## One question

At identical Full aligned-reader initialization,exactly the same minibatches and800 updates,
does reversing their chronological order within an epoch alter held-assignment performance?
This separates an order intervention from initial-weight variation. Previous seeds controlled both
initialization andbatch generation,so earlier seed effects cannot be attributed to initial weights alone.
This is fresh paired training,not continued training of failed states oranother frozen-input probe.

## Accepted parent identity and loader contract

Acceptance/base:d83c37ad2febed01d1f5c94d6f60fa87f42dafda.
Acceptance:docs/experiment-ledger-addendum-c261-c262.md.
C261 execution:5de24467fd439378505a2357e898fc618de31d45.
Published log:d441c7e5a699bbb55558261a910483057b70e0f3.
Publisher log SHA256:1341aa09aaaab7f78a3aabadaaf4263cd6bdaa2c71fcdc695d1dbda0459d8bb6.
Summary SHA256:555ea1f2a1ae6970283d9b7784b0e382f6f58be202d493c0157c706c1255f9bf.
Summary:runs/c261-v5b-repeat-value-66e5eb87a146491e833bbd2f32ce6989/summary.json.

Required artifact SHA256:
-eval-outputs.pt:ad2b19919cae9a258aef91e6c50596ab3624ab4df6b86f1b251c9a5b75c81fd2;
-measurements.json:1f0b7d3e23f14ea744683cd90c504e82e95d307b6668cfaa3047e6310d25934b;
-repeat-dataset.json:1cf918049e4661bd11fc0aba90212e34eccd3e544c41b953f93ff5e3c1e59339;
-repeat-plan.json:bf8c32a5916d968871daeaa6ecf0c1fe38d75cd98b11d2d26096d578ff1a1301;
-validation-summary.json:fc1926548185238f6464bdf30900597d4147eb58be767be14aed901d6b6fa962.

load_parent calls actual C261.validate_result,requires execution identity,status FAIL andpass counts
with_core4/without_core3,then checks all five artifact hashes/sizes. It compares saved validation
summary with the accepted summary andrepeat-plan with C261.manifest. It does NOT call C261's
multi-parent verify_artifacts with an incorrect signature,load learned parent weights,orclaim to
rerun the old tensor replay. Hashes bind the already accepted artifacts. They are provenance only,
not training inputs. The new run path calls this loader through precheck.

## Models and initialization

Fresh seeds262001..262005,each used once as a pair. Both arms are actual C252 Full aligned readers,
created through C256.make_model with the protected C231.new_model factory. No new architecture.
Both14256 parameters. One complete fresh wrapper is deep-copied into forward_blocks/reverse_blocks;
check equal complete initial fingerprints andunchanged template. No tensor sharing orlearned parent
checkpoint reuse. The original core andcore-free experimental paths remain untouched;this experiment
uses the unchanged Full reference only anddoes not select a global architecture winner.

AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,global gradient clip1;batch48;800 updates/model.
CPU float64,threads2,deterministic algorithms. Reset fit RNG to seed+259000 in each arm.
No early stopping,extra updates,checkpoint selection,seed replacement orresult-driven thresholds.

## Fixed task and changed chronology

Use the C256 DISTINCT-value assignment split,not C261 repeated-value rows,for this controlled
training-order experiment. No previous verdict orC261 metric is changed. Actual C256.dataset hash:
ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b.
Actual C257.novel_dataset hash:
9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052.
Twelve distinct-value assignments per TRAIN/HOLDOUT partition,all6 orders,EN/JA identifiers,three
queries,48-slot byte encoding. Original144 plus extra288 rows/split;216 questions/language.
HOLDOUT never enters optimization. No labels,entity indices orcorrect answers enter model input.
Actual C259.training_tables builds TRAIN-only3x144x48 tokens plus144 target IDs.

For zero-based step s,epoch=s//3,offset=s%3. randperm144 uses seed+256000+epoch. Split into48-row blocks.
Both arms use the same blocks,including the same order of examples inside each block. The fact-order
pair remains epoch%3 in BOTH arms,using012/210,021/102,120/201 andthe original logical row's order bit.
Only the CHRONOLOGY OF MINIBATCHES changes;facts within each prompt are not reversed by this intervention.

Forward blocks:0,1,2 in a complete epoch. Reverse blocks:2,1,0.
There are266 complete epochs,then the final two updates798/799 in epoch266.
Forward consumes blocks0,1 in that final epoch;reverse consumes1,0. Block2 is absent in BOTH arms.
Do not naively use2,1 in the final reverse tail,which would change training examples/exposures.
No extra update is added to make an epoch complete. Fact-order pair updates stay267/267/266.

schedule returns the800x48 row-index matrix,800 fact-order pair indices,and432 exact prompt exposure
counts keyed by table_pair*144+logical_row. Save andregenerate chronology SHA256,exposure SHA256 and
full exposure counts. Every pair must have identical exposures butdifferent chronology hashes.
These describe the indices actually indexed by fit. Inputs at the same update are intentionally
different across arms;per-epoch consumed minibatch multisets andfinal exposure totals are identical.
Optimizer trajectories andgradients are allowed to diverge as consequences of order,not extra changes.

## Fixed gate and deciding comparisons

Actual C260.score uses C256/C257 scorers andtheir unchanged distinct-task criteria. Both languages
andboth TRAIN/HOLDOUT partitions must pass:
-original accuracy>=.90,order-pair>=.80,query-triplet>=.80,evidence_drop>=.35,query_drop>=.35;
-EACH additional fact order accuracy>=.90,query-triplet>=.80,evidence/query drops>=.35;
-all-six-order consistency>=.80.
Additional cells36 answers/12 triplets require33/36 and10/12. Six-order groups require29/36.
Primary joint PASS requires BOTH chronology arms to pass all five fresh seeds. A complete valid miss
is ACCEPTED VALID NEGATIVE. Neither arm's result rescues the other. This measures reliability under
the two specified schedules,not whether reversal is a universally better training procedure.

Report each arm's five seed outcomes andten paired HOLDOUT language comparisons:reverse minus forward
accuracy,each all-six-order score,answer disagreement count,forward-correct/reverse-wrong count,
forward-wrong/reverse-correct count,andboth-wrong-but-different answers. Denominator216 per comparison.
Reconcile disagreement categories andcorrect-count difference. Equal aggregate accuracy does not
imply identical answers. Never relabel raw-logit drift alone as a correctness orcapability change.
Different paired outcomes support sensitivity to this specific order intervention,not the cause of
all previous failures orproof that initialization is irrelevant. Identical outcomes do not show that
all possible data orders are harmless. No significance orpopulation guarantee from five pairs.

## Workload and persistence

Ten models x800 updates=8000 updates/384000 training rows.
Per model training+final scoring812 forwards/40992 rows;strict replay12 forwards/2592 rows.
Total8240 wrapper forwards/435840 rows. Full core calls32960 (four per wrapper forward);separate hooks
verify3248 train/final+48 replay per model. Final/replay evaluation forwards240.
One new10-state checkpoint bundle write/load;ten strict state loads;network calls0.
Historical tests,source/artifact hashing,schedule regeneration andserialization are additional work.

Six ignored artifacts plus summary.json:batch-plan.json,dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json. Model schema fold-c262-batch-models-v1 contains ten final
states in seed/arm order. Evaluation schema fold-c262-batch-eval-v1 contains final original/extra logits,
initial/final fingerprints,fit chronology/exposure records,counters andstrict-replay results.
These are final states,not initial outputs orselected intermediate checkpoints.
Actual C259.replay_one strictly loads states,checks final fingerprints,exact argmax andlogit tolerance
1e-9,records12/2592,andC262 adds core counts. Saved postcheck loads evaluation tensors,regenerates
schedules,andrecomputes scores/flips/gates without new model construction,forward orweight-bundle load.
Expect roughly53 MB raw evaluation logit payload plus weights,records andJSON;not a speed/storage claim.

## Protection and authoring review

Inherit412 source pins/685 inputs;add parent summary+FIVE artifacts andOWN6:418 pins/697 inputs.
Direct deciding dependency union38=five C231 LM sources,C230..C261 helpers,andC262. All reused lazy
scientific dependencies are pinned. Accepted source/tests/logs/dispatchers remain unchanged.
OWN6:
-fold_lm/v05_benchmarks/model_c262_minibatch_order.py;
-tests_lm/test_v05_c262_minibatch_order.py;
-tools/run_c262.ps1;
-tools/invoke_c262.ps1;
-this preregistration;
-docs/v5b-minibatch-order-v0.1.md.
Own24;modules147;loaded3454/focused3453. Sole inherited exact exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
Manifest SHA256:2e69e86ae813dcfde5f4096c1377c11cbe8907aa548d2c9cedcc6a0017bb279c.

Before activation,re-fetch committed files andmatch executable blobs to the complete locally tested
copies. Execute exact own24,compile/import,free-name audit,manifest/dataset hashes,semantic counts,
parent API/schema/source coverage andCLI/parser ordering checks. Tests explicitly use a synthetic
Tiny/core andBase/Orders/Trainer/Scorer/Audit adapters;they do not execute the Full FOLD architecture.
Test09 exercises the actual new800-update train loop andcheckpoint replay on Tiny. Test21 executes
actual run/saved-postcheck orchestration with substituted training records. Test22 constructs3454
IDs to test filtering,not to claim3453 historical tests ran. State all review limitations in the handoff.
Do not issue a launcher until committed-byte authoring review PASS. Windows ParseFile andthe full
historical/user-local artifact precheck remain mandatory during authoritative execution.

## Stop and scope

The authored task has been repeatedly inspected andall6 fact orders are training-visible. No unseen-
order claim,new independent benchmark,general language,core superiority,production adoption orGate F.
Integrity failures:INVALID / RETRY SAME C262. Valid misses are accepted without adjusting seeds,data,
steps orcriteria. Operational skips precede logging;log-only publication failures are repaired
without repeating completed training. No paid API,external corpus,model expansion,cleanup,history
rewrite orCI changes. Judge C262 before C263.
