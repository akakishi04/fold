# C309 post-authoring review

post_authoring_review = PASS
Scope:separate committed-byte/static review and executed local software tests,not authoritative FOLD science.
Review target:a5df5534002eb7878b05df6fbf1a09d04925705f.
Acceptance base:1e534105f5ac29b4e6f128adc3b47baa4e31966b.

## Committed-byte match and immutability

After authoring,all6 OWN files were fetched from the immutable review target and reread.
Source425lines and test465lines were covered by consecutive ranges. Runner,launcher,preregistration
and design were read in full. Whole-file Git blobs match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c309_core_lr_replication.py:8c66d64aa7ca3558d914a9b34bc9612ef444a9c2;29208bytes.
- tests_lm/test_v05_c309_core_lr_replication.py:4f189d5a83948d435e11258ad9128b37380f1554;31396bytes.
- tools/run_c309.ps1:013b1e5bbda11ac01d1c90ffb6761166b4dd21ca;4742bytes.
- tools/invoke_c309.ps1:331155c4e9763d64eae16d376d2d2795c20cdfca;6899bytes.
- docs/experiment-ledger-addendum-c309-preregistration.md:470951f8cf32d0d72db0772d807bf126eb03061c;8706bytes.
- docs/v5b-core-lr-replication-v0.1.md:da4dfc2aa2131ba3274a14cc069c20e5a0a07d01;1197bytes.

Remote acceptance-to-authoring comparison contains exactly these6 additions. No accepted source,
test,preregistration,log or dispatcher was modified. Activation must preserve all6 reviewed blobs.

## Actual post-match verification and execution method

Both complete32-test passes were executed AFTER matching all6 remote blobs:
- normal default:32tests,0failures,0errors;
- io.text_encoding default emulated as CP932:32tests,0failures,0errors.

The one-shot local shell suite hit the tool time limit;that interrupted run is NOT counted as a
complete PASS. Instead,the complete module was run in bounded batches within one persistent Python
process:one class setUpClass,all32 ordered unittest TestCase.run calls sharing a TestResult,then
one tearDownClass. Both modes included every test without exclusions. The CP932 patch remained
active across setup and all32 test calls and was restored afterward. Synthetic temporary files
used /dev/shm locally to avoid slow temporary storage;the registered source/tests were unchanged.

Normal active setup+test time59.015s;CP932 active setup+test time61.138s. These sums exclude tool
pauses and are not uninterrupted unittest runner wall-clock timings. Runtime:Linux/Python3.13.5/
PyTorch2.10.0+cpu/NumPy2.3.5. This is not Windows or the actual4909-test inherited regression suite.

All6 files UTF-8/noNUL. Both Python files and all3 embedded Python blocks compile. Recursive
symtable/import-binding audit found0 unresolved global references. New module defines32tests.
Manifest self-hash matches9350f7a5ec4e91a3292f6ecce041bc3ec09f1fa1a8372a4178b58d0ceb4df74d.
PowerShell was not available here;Windows dispatcher/launcher/runner ParseFile remains mandatory.

## Behavioral coverage and limitations

Actual child fit loops execute1200 AdamW updates for each of full_train/core_frozen/core_slow
on a controlled toy model. All3 reproduce isolated accepted C308 fit definitions exactly for all
losses,group-LR histories,gradient metadata and final weights with the same new seed inputs.
All5 child schedules equal the accepted schedule algorithm and have100exposures per trained
length. New inputs are bound only inside isolated reference namespaces;imported parent modules
are never rewritten. Policy drift and overlapping old/new seed cohorts are rejected.

Optimizer tests cover all parameter membership,independent model storage,initial equality and
core/noncore boundaries. The inherited probe checks frozen input-backward connectivity plus
full/slow equal initial gradients and first-step core0.1delta. Initial scientific copies remain
unchanged. One optimizer reaches1200steps;external RNG disturbance does not change the loss trace.
Clipping instrumentation verifies original model parameter order at all1200updates. Only frozen
core remains unchanged. Nonfinite outputs,wrong optimizer policy and altered LR/loss histories fail.

Actual train_one on the toy records1308model calls,67968row presentations and5232core calls via
forward hooks. It checks that final evaluation starts frozen. These counts are measured on the
toy's four-core-call forward,not measurements of the real FOLD backend. Actual child run/bundle
serialization tests confirm15fits before15replay dispatches and one model-bundle load. Both byte
and semantic artifact tampering are rejected. Run directories cannot be overwritten.

Other fixtures validate15results/120partitions/80contrasts,two paired contingencies,one new
candidate failure retaining a negative gate,all35 hash rejections before parent dispatch,exact
parent flags,700/1309 protection accounting and a missing-helper rejection. Semantic test-ID
fixtures construct4910unique tests and retain4909 after the sole inherited C204 exclusion;this
is not execution of the real4909-test suite. Actual OWN-file reads are explicit UTF-8 under CP932.

Only OWN6 are byte-identical local copies. Parent support comprises selected fetched C308
manifest/configuration/optimizer/schedule/fit/probe definitions,C306 first_batch_probe and C304
schedule_stats,not full parent modules or a repository clone. Synthetic target-coded inputs,
substitute LengthReadout/backend,Git,parent archives,scorers and replay callbacks are software
fixtures where real inputs are unavailable. No actual FOLD capability or real parent validation
has been measured locally. CP932 emulates default text decoding,not the entire Windows environment.

## Scientific path,parent writer and dependency audit

The actual C308 run/verify implementation was reread at the review commit. Its model archive is
fold-c308-core-lr-models-v1 and evaluation archive fold-c308-core-lr-eval-v1. It stores FINAL frozen
logits and1200loss/LR/gradient/event records. C309 does not directly reuse an old cohort analyzer:
it verifies35 ordered hashes first,then calls exact C308.verify_artifacts with34ancestors and the
accepted execution HEAD. The exact parent summary seals7 artifact descriptors;the parent rebuilds
its scores,optimizer histories,core invariants and replay metadata. Require bounded parentPASS,
exact15seed results,matched groups/replays and the two original paired-five tables.

Only verified dataset.json and length-datasets.json become new learning inputs. Regenerate/check
C304 prompts and canonical hashes. Parent predictions never become targets and old model weights
never initialize C309. The child run calls its own15-state bundle loader after all fits,then calls
C304 strict replay. Child archive schemas and seed identities are distinct from C308.

Sole direct import C308. Its context provides C307,C306probe,C305no-neural,C304wide,pair builder,
C287normalizer,C283transfer and backend. Source694/protected1295 remain enforced;actual repository-
local context/core/factory-language helpers and all C304.PINNED modules are checked. Add OWN6 plus
8parent files for700/1309. No dependency omission,accepted-source mutation or extra exclusion is waived.

Seed-independent accepted optimizer/probe helpers are called directly. Child seed-sensitive
factory/schedule/fit/analysis use309001..309005 and309101..309105. Model,data,LR ratio0.1,
FIT_RNG612000,shuffle offset306000,1200updates,clip order and all thresholds are held fixed.
Only new candidate results determine the new all-five gate. C308PASS cannot be pooled in to rescue
C309,or silently replaced by its outcome. No ratio tuning,extra cohort search or automatic adoption.

## Workload,runner and release boundary

15models*1200=18000updates;864000training rows;21240forwards;1175040totalrows;84960corecalls;
15strictstate loads,one bundle write/read,network0. Same scientific work as C308;backward costs
differ among policies. Operational probe2updates,tests and recursive old-artifact validation are
separate. All original scoring/masks and primary candidate5/5 criterion remain unchanged.

Runner contains3 compiled Python blocks.35summary arguments;postcheck paths[2:37],head[37],argc38.
Launcher contains35 fixed ordered paths and stops before science/publication on Validate failure.
Use unchanged active_v2 dispatcher with dispatcher/selected-launcher/runner ParseFile chain.
Own32/modules194/loaded4910/focused4909;sole inherited exact C204 exclusion unchanged.

Not executed here:WindowsParseFile,the real35 parent archives/protected bytes,actual-model
initial gradient/optimizer probes,the actual4909 inherited tests,or15realFOLD training/evaluation/
replay runs. All remain mandatory Windows Validate/Execute gates. This review authorizes only the
guarded launcher,not a scientific verdict. Integrity failure repairs SAME C309 with fixed conditions.
C310 stays unregistered until C309 formal judgment. Gate F remains NOT PASSED.
