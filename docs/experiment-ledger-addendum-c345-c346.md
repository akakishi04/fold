# C345 acceptance and C346 learning-rate question boundary

Review date: 2026-11-22 Japan time.

## Formal verdict

**C345 ACCEPTED PASS — DIAGNOSTIC INTEGRITY ONLY.**
Execution revision C345-R0 completed validly using the accepted C344-R1 cleanup implementation.
C344 remains ACCEPTED VALID NEGATIVE,candidate_gate=false/eligible_seed_count=2.
C344attempt01 remains INVALID. Gate A/B PASSED; C/D PASSED in measured scope;
Gate E PASSED; Gate F NOT PASSED. No capability improvement or production adoption.

## Identity and evidence scope

- Scientific execution HEAD: `c81ffe102c3a9280f28a68e572403549ce77fa1d`.
- Log publication: `25ff2f93ce63c9668f3111672caf75db095d2f45`,soleparent execution,only C345latest.log/json.
- Git log blob: `d64ba92369be7f4100a228783df37d1eb700fbdf`.
- Git LF:755410bytes/3908lines,SHA256 `9bd110d8758e8d2a47f49e7bd8e6f85844d9fd84ea2067ca8a805d093dce49c2`.
- Windows CRLF reconstruction:759318bytes,SHA256 `9531d1f7ae6e9be8c220954dd0f233a9c20844e94a983765d0b673105865fc9a`,matching metadata exactly.
- Folder: `runs/c345-saved-objective-audit-749db4a6ede44b608c06ee1461b6e393/`.
- Primary science/summary.json SHA256: `cfc3fe5b8f4ec927d875e2a016a940b5d34aac9ef14d93644eeb26567c0e1f30`.
- Envelope SHA256: `e883c26d1df24d940cd51b551f06e46e7ac69da216ea6024dc299ee24d2cceab`.
- Manifest: `5e69553fd6661ef46459883500fd719b474fd7cacbd17d002c957eb3fb2f1a9f`.

All630public numerical records were independently parsed and checked:120terminal,
60terminal contrasts,120fixed200step blocks,180cycle/slot/profile groups,
60paired blocks and90paired groups. Complete coordinates,statistics,loss differences,
step/exposure/norm partition conservation and signed-count arithmetic agree.
All120normal summaries and60answer/pair contrasts bind C344's unchanged validated
parent summary and its complete public records.

The actual local loader rebuilt the6578test-ID/241module plan without executing
historical tests. All public begin/complete/count/OK/exit records match this plan.
The console omits source_trace_sha256 and the complete primary artifact. No placeholder
digest or complete reviewer-side C345summary reconstruction is claimed. User-local
checkpoint/trace/input maps and module proof files were not independently fetched.
Native persisted and separate fresh-process verification are explicitly attributed
to the accepted verifier and published completion. Public block/group summaries
cover24000trace rows; the individual raw rows were not themselves published/read.

## Execution validity

Full6578tests/241isolated modules PASS in3385.166seconds;failures/errors/skips0.
All244process exits0:241modules plus regression,science,fresh verifier.
Six native cleanup checks passed;unchanged C344-R1receipt validator accepts the
receipt bound to the C345execution HEAD. Native read leases,937sources/8679inputs,
all8679final uncached rereads,saved reconstruction and fresh verification complete.
run_execution_valid=true.

Full ordered ID SHA256:
`2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a`.
The6514parent IDs remain an exact ordered prefix,SHA256
`c5d7db147680f739c62bbbc2f12be324c66ba16ea108dc04beb3071f56abaaa3`.
Only the previously registered C204mutable-ACTIVE test is excluded.

Per child diagnostic/reconstruction pass:10saved-state records,51840normal answers,
25920query pairs,24000trace rows,12000paired rows. Scientific new forward,gradient,
update,model-state-load,checkpoint-write,network all0. Regression fixtures and
parent checks are separate from these scientific counters.

## Deciding terminal measurements

Control mean_ce -> candidate pair_max. Losses are answer/query-pair weighted means
within one domain/split across all five seeds,with equal per-seed denominators.
They are not exposure-weighted whole-mixture training objectives. Lower is better.

|Domain/split|Correct answers|Mean CE|Mean pair-max|
|---|---:|---:|---:|
|interior4 TRAIN|2864->2728/2880|0.011673977->0.111296027|0.020316586->0.192509275|
|interior4 HOLDOUT|1430->1331/1440|0.025826478->0.288532880|0.045815971->0.499002482|
|original6 TRAIN|2875->2877/2880|0.007122162->0.004923911|0.013711807->0.009339757|
|original6 HOLDOUT|1431->1438/1440|0.033253156->0.004057164|0.066434798->0.007846538|

**All10interior seed/split contrasts have higher candidate mean CE AND pair-max.**
All7answer-regressing seed/domain/split contrasts have higher both losses.
There are0worse-answer/lower-pair-max contrasts at this60-cell summary granularity.
Do not extend that zero to individual answers,pairs,profiles or the whole mixture.
Original2/3/4 remain perfect on normal answers,but pooled loss increases.
Original5TRAIN loses one answer;HOLDOUT remains perfect,with higher pooled losses.

|Seed|interior TRAIN answers /576|TRAIN pair-max|HOLDOUT answers /288|HOLDOUT pair-max|
|---|---:|---:|---:|---:|
|344001|576->576|0.000658684->0.001316901|288->288|0.000194757->0.000221628|
|344002|560->562|0.099380652->0.109815482|278->280|0.228647055->0.433637026|
|344003|576->552|0.000596191->0.151033328|288->275|0.000120767->0.406086830|
|344004|576->462|0.000369150->0.699392239|288->200|0.000055743->1.654885642|
|344005|576->576|0.000578254->0.000988427|288->288|0.000061531->0.000181286|

344002improves two answers in EACH split despite higher both losses:loss and exact
accuracy are not monotonically interchangeable. 344003/344004account for the main
interior answer deterioration. Original6improves in aggregate but344004regresses
in both splits. Do not claim uniform harm everywhere.

## Complete-trajectory findings

Stored preclip norm>1:1975/12000control ->5830/12000candidate,all five seeds increase.
Mean preclip norm:0.421556->1.610393. Cycle2mixed slot4:162/2000->1241/2000exceedances.

|Cycle2 slot|Mean CE control->candidate|Common pair-max control->candidate|
|---|---:|---:|
|2: original2|0.001106455->0.003422217|0.001990054->0.005388706|
|3: original3|0.001428943->0.005958762|0.002595078->0.010079822|
|4: mixed original4/original5/interior4|0.029069511->0.163171391|0.053636368->0.273876273|

Across12000same-step comparisons,candidate pair-max is higher10425/lower1570/equal5;
mean CE is higher11154/lower841/equal5. These are dependent trajectory observations.
For344002the last200step mean CE improves0.018462305->0.002846563 and pair-max
0.033702834->0.005167516,even though terminal interior full-domain losses worsen.
Preupdate mixed-minibatch block means and final domain means differ in population,
weighting and time;their opposite directions are not a contradiction.

## Scientific interpretation and nonclaims

The main interior answer deterioration accompanies worse matched terminal loss,
including the candidate's own pair-max measure,on actually fitted interior TRAIN.
The major deterioration is not lower terminal surrogate loss in exchange for worse
answers at the registered seed/domain/split summary level. It is a comparator-relative
endpoint shortfall,not proof of nonconvergence or a named optimizer defect.
C344's objective-policy intervention changed the training trajectory;C345 does not
identify which mediator caused that change.

Norm>1 is a threshold description,not exact clipping calls or actual update size.
Loss reduction changes gradient direction/scale and later weights. Slot4 is mixed,
not interior-only. Traces do not prove learned-then-forgotten answers. Original6TRAIN
contains familiar value combinations but its names/prompts were never fitted.
No universal rate,capacity,readout,clipping,gradient-starvation,parity or language claim.

## Repository update

The C344-bounded [synthesis](cross-experiment-evidence-synthesis-2026-11-22.md) and
[85-experiment index](cross-experiment-evidence-index-2026-11-22.json) are imported
unchanged from `45c18e39399a6f5ec073257d860377ecb624bd51`.
Their statement that C345was pending is historical. This acceptance supplies the
later result rather than rewriting their snapshot. The conditional interpretation
now resolves toward worse matched terminal loss for the main interior deterioration.
Previous handoff: [C345 pre-acceptance](handoff-history/c345-pre-acceptance.md).

## Next one scientific question — not registration

Does a fixed half-rate pair-max policy improve interior binding and retain every
registered domain relative to both default-rate pair-max and ordinary mean CE?

Proposed fresh paired comparison:ordinary mean CE at default rates as strongreference;
default pair-max;pair-max at half BOTH optimizer-group rates from initialization.
Keep2400updates,mixed45data,all streams,architecture,clipping,objective and evaluations
fixed within the pair-max comparison. This tests a rate policy,not a proved clipping
cause. No mean-CE half-rate arm: no objective-by-rate interaction or optimum claim.

The proposed gate requires all five candidates to pass complete existing gates,
nonnegative answer/pair counts for every seed/domain/split versus BOTH controls,
and four strict interior aggregate gains versus default pair-max. Report every
subgate separately. A perfect comparator may leave no strict-gain headroom;retain
the registered failure without replacing seeds,extending budgets or changing gates.
Terminal matched losses remain descriptive;gate PASS does not promise loss improvement.
C328's earlier late0.1rate change is a different objective/timing and remains negative.

This acceptance does not register C346. Source/tests/executor/launchers/preregistration
must be committed separately and independently reviewed from remote bytes before
activation. Do not rerun accepted C344/C345;C347 remains unregistered.
