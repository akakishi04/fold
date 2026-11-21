# V5-B saved middle-slot attribution v0.1 — C258

## Why this diagnostic

C257 validly missed its all-five-seed unseen-order gate:two models passed and three did not.
C256's value-assignment PASS remains. Before altering learning or architecture, inspect which
questions failed and which displayed value was returned. This is one saved-answer diagnostic,
not a claim that repeated diagnostics can replace a new controlled training experiment.

During C256, b/乙 always occupied the middle fact position. In the four novel permutations it
occupies an end. A concrete hypothesis is that some wrong answers to b still match the middle
fact's value. A competing pattern is broad errors across a,b,c, selection of the other distractor,
or outputs not assigned to any displayed entity. All are retained and reported.

Example: a=0;c=2;b=1;b= has target1; answer2 is the middle distractor, answer0 the other displayed
distractor, answer3 an absent value, and answerx an out-of-task byte. Correct answer1 is not
counted as support for the shortcut. Attributing the answer does not reveal its internal cause.

## Frozen evidence and actual interfaces

Use all ten accepted C257 saved evaluation records, not newly evaluated or trained models.
Seeds256001..256005, aligned_precore_read/eos_adapter, EN/JA, both original assignment splits.
Known orders012/210; novel021/102/120/201. Every query and every assignment remains included.
The original TRAIN/HOLDOUT names identify C256 assignment sets, not training performed in C258.

Validate the actual status FAIL/candidate2/control0 parent and all artifact bytes. Read its
fold-c257-order-eval-v1 archive. C257.load_inputs returns original C256 data and final measurement
records; C257.analyze replays all old/new/restored saved outputs and must reproduce the accepted
measurements and summary. There is one evaluation-archive load per pass and no learned bundle
load. The source-pinned parent writer stores logits from the final frozen states, not new actions
or additional training. The scored normal view must not be confused with the erased-input views.

Block Module._call_impl while loading/replaying/analyzing so an accidentally introduced model
forward fails. No model factory, optimizer or state-load call belongs to the diagnostic path.

## Counts and denominators

Attribute8640 normal answers:known2880 + novel5760 across ten frozen model records.
There are720 order/query cells, each12 assignments;120 pooled query cells, each24 known and48
novel answers;40 b-vs-a/c signatures, one perseed/arm/split/language.

Four exhaustive answer classes:correct, other displayed entity, absent0..3 value, other byte.
The first two additionally identify the entity and its visible position. All assignments have
three distinct values. The four classes sum to the exact row count; middle-wrong is a subset,
not a fifth class. No missing/invalid prediction is silently recoded as an ordinary wrong answer.

For every query compare original-pair correctness with each novel presentation. For b show the
known and novel correct counts, error-rate difference versus pooled a/c (48 versus96 rows),
middle/other distractor counts and outside-assignment counts. Report middle-error shares using
both all b errors and only in-assignment b errors as denominators. Zero denominators are null.
Keep all per-order/query cells so a pooled signature cannot conceal a concentrated failure.

## Interpretation

This plan is motivated by already observed aggregate C257 results. It is exploratory saved-output
analysis, not a fresh holdout or causal intervention. Permutations/queries/seeds here are correlated.
A large middle-distractor share is compatible with a positional shortcut but cannot prove it.
A small share is evidence against that particular observable signature, not proof of a different
internal algorithm. Do not treat diagnostic PASS as restored order-transfer capability.

The diagnostic integrity gate only requires correct input identity, parent replay, complete
attribution/accounting, no new model calls, unchanged protected files and exact persisted
recomputation. It has no hypothesis-support cutoff. All signature directions are valid outcomes.

## Runtime and next boundary

Model forwards0; new training0; new learned checkpoints0. Two analysis passes load the accepted
saved evaluation archive once each:scientific analysis and persisted postcheck. Parent hashing,
regression fixtures, all-view metric replay and serialization are separate runtime work.
Five generated JSON artifacts remain under ignored runs/, with console log alone published to Git.
C258 own20 and focused3357 must pass before the formal diagnostic. Parse dispatcher,launcher and
runner before execution. Preserve accepted code/results and C256/C257 verdicts. No Gate F change.

After this one decomposition, a proposed order-coverage training change requires a separate
controlled experiment; it is not automatically authorized or implemented by this diagnostic.
C259 is not registered.
