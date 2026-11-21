# C258 acceptance and C259 controlled order-coverage boundary

## Formal verdict

C258 ACCEPTED PASS (diagnostic integrity only).
C257 remains ACCEPTED VALID NEGATIVE; C256 remains ACCEPTED PASS in its original bounded scope.
Gate E PASSED; Gate F NOT PASSED. No capability, causal-mechanism or production promotion.

Scientific execution HEAD:e31d4c28a00bc11fb5db3c2ba1b093e4eae15538.
Published log commit:62aac236dc90643dc57b3ed51855f79aeb22f1cd.
Publisher log SHA256:5a7ad7fff7846a76e43eec75542b8327de3a4ca42094e2c68d3e0d143dd32c64.
Log bytes:676199.
Summary SHA256:f6ccc7dc1b8c60c1f1e6bc7587bd9853eeb6bea6e1f7a010fd99de068bbd0ecc.
Local summary:runs/c258-v5b-middle-slot-93386fd77e3749bab4122685ff57720d/summary.json.
Publication changes only c258/latest.log and latest.json.
Acceptance is based on immutable published log ranges and recorded local postchecks, not independent
rerunning of learned artifacts or an independent rehash of the entire published console log.

## Execution validity

Own20 PASS in0.967s; focused3357 PASS in216.615s.
394 source pins/647 protected inputs verified. All8640 normal answers attributed:
2880 known-order and5760 novel-order answers,720 order/query cells,120 pooled query cells,40 signatures.
Scientific model forwards0,model/state loads0,learned checkpoint loads0,training0,new checkpoints0.
One saved-evaluation archive load per analysis pass; scientific analysis and persisted postcheck
are two passes. Historical test work and parent-file validation are separate work.
Parent saved-logit replay,integer accounting,zero-denominator handling,protected-input preservation
and persisted re-attribution PASS. Tracked tree clean;execution HEAD preserved;run_execution_valid=True.
capability_pass_claim=False;causal_mechanism_claim=False.

## Deciding descriptive results

Candidate novel-order HOLDOUT:1187/1440 correct,253 errors.
251 errors select another displayed entity's value;2 select the absent0..3 value;other bytes0.
For query b/乙:141/480 errors(29.375%). For pooled a/c:112/960 errors(11.6667%).
Among the141 b errors,64 select the middle-position distractor,75 the other displayed distractor,
and2 the absent value. Thus middle errors are64/141(45.3901%),not a universal majority signature.
These pooled summaries do not replace the complete per-seed/language/split output.

Candidate HOLDOUT per-language error counts:

|Seed|b EN /48|b JA /48|a/c EN /96|a/c JA /96|b middle EN+JA|b other EN+JA|b absent|
|---:|---:|---:|---:|---:|---:|---:|---:|
|256001|0|0|0|0|0|0|0|
|256002|26|23|1|1|19|29|1|
|256003|32|31|30|13|32|31|0|
|256004|1|0|0|0|0|1|0|
|256005|6|22|36|31|13|14|1|

All candidate b known-order cells were24/24 correct. Query b errors in the new orders therefore
match known-both-correct -> novel-wrong cases, not pre-existing b failures.
The seed256005 EN direction is reversed:12.5% b errors versus37.5% a/c errors.
Do not claim that every failing seed has the same b-only or middle-position failure.
Candidate novel TRAIN:1177/1440 correct,263 other-entity errors,no absent/other-byte errors.
Its b errors143/480 versus a/c120/960; middle b errors76 and other displayed b errors67.

EOS controls remain separate:novel HOLDOUT326/1440 correct,968 other-entity errors,146 absent-value
errors and0 other bytes;novel TRAIN805/1440 correct,551 other-entity and84 absent-value errors.
Their already-failed C256 criteria are not new independent C257 failures.

## Interpretation and non-claims

Some candidate states disproportionately fail queries about b after position changes, but the
hypothesized universal 'answer the middle value' explanation is not supported as a complete account.
Most candidate mistakes are wrong entity/value selections; patterns vary across seeds and spellings.
This is descriptive post-hoc decomposition of the same correlated C257 outputs, not independent
confirmation, a causal intervention, or evidence of a uniquely identified internal algorithm.
No C257 score or verdict is rescued. No general language, core superiority or deployment claim.
This concludes the single saved-answer decomposition promised in C258.

## Next question, not activation

At a fixed model,initialization and800-update budget,does training across all six fact orders
produce reliable held-assignment performance across all six,relative to a paired two-order reader?
Use fresh seeds259001..259005;both arms are the same actual C252 aligned pre-core reader,not the EOS
adapter. Copy identical full initial states. Pair the same underlying assignment/language/query
batch schedule and change only visible fact-order coverage. Never train HOLDOUT assignments.
Do not reuse accepted learned checkpoints,select failed seeds,add updates,or loosen gates.

All-six-order training makes the evaluated orders seen by that arm. Any PASS therefore establishes
held-assignment performance under trained order coverage,NOT unseen-order transfer for that arm.
Keep paired control effects separate from the all-seed treatment capability gate. No automatic
causal story about the internal mechanism follows even if distribution coverage helps.
C259 needs separate preregistration,implementation and committed-byte authoring review before
activation. C260 NOT REGISTERED.
