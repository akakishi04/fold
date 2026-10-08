# C312 post-authoring review

post_authoring_review = PASS
Scope: committed-byte/static review and executed local software tests; NOT actual FOLD science.
Review target: fe23ba10bba919790f73087f53719d0f1a123fba.
Acceptance base: b583d14164fed3f6f03e0385e5d8c443138171f9.

## Committed-byte match

All six OWN files were fetched from the immutable authoring commit and reread after commit.
Source434lines and test411lines were read in consecutive complete ranges;four other files in full.
Their returned whole-file Git blob hashes match independently hashed local tested bytes6/6:

- fold_lm/v05_benchmarks/model_c312_value_balanced_batches.py: a676b684d605424c35713ac08940e06ab16553f4;29191bytes.
- tests_lm/test_v05_c312_value_balanced_batches.py: 441989ad706d4dfb58a539901823bac2cbce8734;28459bytes.
- tools/run_c312.ps1: 3faf54e3f695588ce991d15f95a0b548d4a46fdd;4675bytes.
- tools/invoke_c312.ps1: 2e6818f0cc9b0419ada4ad632ba65e6dc1b328c6;7201bytes.
- docs/experiment-ledger-addendum-c312-preregistration.md: 94c27d48a4819d44d211432be2b3e55c5f0d21b1;7568bytes.
- docs/v5b-value-balanced-minibatches-v0.1.md: 4e38f96d7888a4d74b1d8d1c277a95ae8d362db2;1269bytes.

The remote acceptance-to-authoring comparison contains exactly these six additions. No accepted
source,test,preregistration,log or dispatcher changed. Activation must preserve all six blobs.

## Tests actually rerun after all six matches

Normal: python -u -m unittest tests_lm.test_v05_c312_value_balanced_batches -v
Ran32 tests in18.876s;OK.

Whole same module imported and executed under io.text_encoding CP932-default emulation:
Ran32 tests in19.660s;OK. The patch covers module import,setup,all tests and teardown and changes
only the default when no explicit encoding was supplied. Both runs were uninterrupted full suites.
These post-match runs,not earlier pre-commit tests,are the executed review evidence.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. PowerShell is not installed locally.

All6 files are UTF-8/no-NUL. Both Python sources and all3 embedded Python blocks compile.
Recursive symtable/import-binding audit returns0 unresolved globals in both new Python files.
Manifest recomputation matches5c543202a3c252e69f3f099b369ef9905e39662a37947c8904756b17700fab2c.
All38 launcher paths are ordered C311 through C274. Postcheck paths=sys.argv[2:40],head[40],argc41.
The new launcher resolves only C312 and calls Validate before Execute or scientific publication.

## Behavioral coverage

The independently constructed logical data fixture matches the accepted canonical dataset SHA.
For every new seed,both schedules cover all96 intact query pairs exactly once per epoch and
all192 TRAIN rows100 times at each of2/3/4 lengths. Profile totals400each. The candidate has3
query pairs per each8 TRAIN-value strata in every update and12 targets per digit. No HOLDOUT
value pair enters training. Invalid targets,pair partitions,strata and identities are rejected.
The schedules do not change global RNG. A separate counter-based implementation checks balanced
allocation against the production stable-rank implementation;an independently constructed random
reference checks the unchanged control. No extra RNG draw or value-sorted within-batch ordering.

A complete1200-update execution of the new fit function on a controlled toy model is compared
with a separately written optimizer loop:all1200 CE values and final weights match exactly.
The actual train_one and replay paths also run on that toy:1308/67968/5232 initial fit/evaluation
counts and108/10368/432 replay counts are checked,with strict state restoration and altered-state
rejection. The toy uses label-encoded synthetic inputs and unused capacity padding to test software
controls;this is NOT evidence of FOLD accuracy or generalization.

Tests exercise actual model factory behavior with substitutes:equal initial values,correct total
parameter count and independent storage. A common-input runtime_preflight executes with the toy
backend and checks logits,preclip gradients and one optimizer step. Actual training first losses
are intentionally not required equal because the two minibatch assignments differ.

Tests29/30 extract and execute the accepted C309 schedule,C304 schedule_stats and C308 configure/
parameter_groups/optimizer_for/verify_optimizer functions by AST. Local support files contain only
fetched function slices,NOT complete parent modules/repository. These support slices are NOT
committed. On the user's checkout these tests extract from the full immutable accepted sources.
They verify actual helper algorithms and optimizer contracts using controlled data/models,not
execution of the real FOLD backbone or the full inherited parent tree.

The new analyze function reconstructs10 results,80 partitions,40 contrasts and primary5/5 gate.
A candidate failure remains FAIL. Tests reject incomplete cohorts,altered histories,changed
initial identities,wrong replay metadata and invalid capability promotion. Actual child run and
verify_artifacts execute with substituted parent/Git/model/scorer interfaces,checking ten fits
before ten archive replays,one ordered model bundle,all output identities,no overwrites,byte
alteration and semantic alteration even after updating an artifact descriptor.

All38 parent summary hash failures occur before parent verifier dispatch. Actual precheck runs
against a718/1343 filesystem fixture and rejects a missing helper pin. Synthetic test-suite objects
check4998 loaded IDs ->4997 exact retained IDs and reject duplicates. This is not execution of the
actual4997 inherited tests. Explicit UTF-8 inventory/source reads pass under CP932 emulation.

## Scientific path and parent audit

C311 writes diagnostic JSON,not trained models or datasets. Its exact verify_artifacts returns
(payload,error_report) after recursively checking C310/C309 saved artifacts. C312 verifies38
ordered summaries BEFORE calling that verifier with37 ancestors and C311's accepted execution
HEAD. Only then does it read original C309 dataset.json and length-datasets.json from paths[2].
Canonical data/prompt hashes,logical value targets and full render semantics are rechecked.
The C311 report is never used as training data,labels or learned initialization.

Sole direct repository import C311. Its C310/C309 context exposes the actual accepted C308
core_slow optimizer and C30464-slot wrapper,evaluator,scorer,replay and training tables. Original
pair/normalization/backend helpers are retained. All712 inherited source pins and1333 inputs are
checked,including C304.PINNED and actual repository-local context/core/factory-language coverage.
Add OWN6 plus4 C311 summary/artifacts to obtain718/1343. No dependency waiver,accepted helper
mutation,old verdict change or extra regression exclusion is authorized.

The control uses the old C309 random-pair algorithm with fresh order seeds. Candidate changes only
batch allocation/temporal order using the same global rank. All epoch examples,lengths,profiles,
update counts and LR settings remain identical. C309 old schedules are also compared by the
real runtime preflight. Both models use policy name core_slow,not differently configured optimizers.
All14,256 parameters train;core3,328 at.0005 and remaining at.005;CE only;clip1 before step.
The effect is conditional on this policy and cannot by itself identify why old models failed.

Strict-loaded final states are replayed through the actual C304 evaluator on all lengths2/3/4/5,
all profiles,normal/evidence-blind/query-blind and original TRAIN/HOLDOUT. Original thresholds
and full256 argmax remain unchanged. The candidate's own new5/5 gate is not pooled with old seeds.
The new archive stores the actual1200-step schedules,value-count matrices,losses,LR histories,
gradient accounting and original final logits;postcheck reconstructs plans,scores and paired results.

## Work and execution boundary

10*1200=12000 updates;576000 training rows;10*(1200+108+108)=14160 model forwards;
783360 total row presentations;56640 core calls;10 strict state loads;one model bundle write/read.
Operational discarded probes,recursive old-artifact checks and tests are separate costs.
No external network in science,no HOLDOUT augmentation,no weight/cohort selection or LR retuning.
Own32/modules197/loaded4998/focused4997;sole inherited exact C204 exclusion unchanged.

Not executed locally:Windows PowerShell ParseFile,the actual38 parent archives/Windows source
pins,the full4997 inherited regression suite,or10 actual FOLD fits/evaluations/replays. These remain
mandatory local Validate/Execute gates. Preserve dispatcher/selected-launcher/runner ParseFile.
Review PASS authorizes only the guarded C312 launcher,not a scientific result. Integrity failures
repair SAME C312 under fixed conditions. Valid capability failure is ACCEPTED VALID NEGATIVE.
C313 remains unregistered until C312 formal judgment. Gate F remains NOT PASSED.
