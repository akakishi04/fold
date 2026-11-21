# C186 preregistration — frozen reclassification after non-admission

V5-E; akakishi04/fold; feat/sft-target-loss.
Registered AFTER C185 acceptance4ce19a7f08717fef8c963f53282cc4340458700f.
C185 ACCEPTED PASS. **C186 ACTIVE / NOT YET JUDGED. C187 NOT REGISTERED.**
Gate E NOT PASSED. All previous results/checkpoints/preregistrations stay immutable.

## One question

After an acquisition is attempted but supplies NO admissible observation, do the
frozen learned candidates retain the correct necessity judgment, rather than treating
the attempt or budget consumption as proof that enough information is now available?
Matched successful acquisitions must still yield SUFFICIENT after admission.

C185 established successful learned-trigger/file-read/admission/reclassification.
ALL its formal provider calls published a valid fact. Failure helper tests used
synthetic policy outputs. Those facts do not establish frozen-model behavior after
non-admission. C186 tests precisely this missing boundary,not another naming audit.

## Fixed substrate and changed variable

Reuse unchanged C185.run_block,bind_views,unique_target,charge_decision,FrozenPolicy,
RulePolicy and make_views. Use unchanged C170 input/C184 local canonicalizer/C178
preparation/C179 TREE_LINKS base/C172 reservations/C173 FileSnapshotProvider and owner.
No old source edit. New code is benchmark-only. Same six C181 final checkpoints,
source seeds181001/181002/181003,both FINAL_ONLY/INTERNAL_SEMANTICS. C182.restore_bare
checks the full25921parameter fingerprint and constructs only25726base parameters.
No auxiliary head,teacher,training,optimizer,new seed,checkpoint selection or ensemble.

ONLY the registered provider return is changed,AFTER an actual C173reference file read.
The shim receives the request and genuine delivery,not labels/model predictions.
It does not mutate the original delivery,source bytes or witness.

|Scenario|Registered source bit|After reference read|Admission / last_outcome|
|---|---:|---|---|
|FOUND_ZERO|0|Return original delivery|PUBLISHED / NONE0|
|FOUND_ONE|1|Return original delivery|PUBLISHED / NONE0|
|NO_DELIVERY|0|Return None|UNRESOLVED,MISSING_DELIVERY /4|
|WRONG_VALUE|0|Flip only value0->1;witness/hash unchanged|REJECTED,INVALID_EVIDENCE /6|
|PROVIDER_FAILURE|0|Raise existing C173ProviderFailure|UNRESOLVED,PROVIDER_FAILURE /NONE0|

These are deliberate return-path faults,NOT real network timeouts or outage simulation
with realistic timing. PROVIDER_FAILURE is injected after reading,not an OS-level
file-open failure. All attempted scenarios therefore pay one provider call/real read.
The C173 owner decides admission using its existing code;the experiment does not
manually erase a successfully admitted fact or insert a failed result as value0.
NONE is the existing outcome encoding for reasons not in C170.OUTCOMES; do not invent
new codes or conflate that encoding with a successful semantic observation.

## Cohort / comparisons / source secrecy

ALL3712C174PILOT rows with exactly one unknown:selected by visibility,not correctness.
Inherited labels768NEEDS/2944SUFFICIENT,4reused development groups/116templates.
Two layouts:identity and reverse,with both numeric references and opaque bindings
moved consistently. Five delivery scenarios x eight policies(six models + MISSING_RULE
and NEVER_QUERY). All scenarios have IDENTICAL initial visible numeric information;
scenario names,source bits,source files and provider faults never enter initial inputs.
The source driver carries labels only into post-hoc scoring and output traces.
No logical solver,proof-based correction or label-driven action is used.

Existing C185 eight tiny snapshots are recreated byte-for-byte,with hashes fixed in
manifest before any model execution. Each source has one external fact record.
C185 external IDs/provider IDs are intentionally reused with new per-episode request
scope suffixes. Those opaque strings are outside model features. No unrelated hidden
record is added. Setup/hash/serialization IO is additional to metered provider reads.

All six models and both rules are retained,not only the best candidate. Descriptive
FINAL_ONLY mistakes are not required to disappear;all eight policies must obey the
engineering contract. No new ability claim from reordered aliases/alternate worlds.

## Live episode contract

Keep C185 maxONE acquisition attempt/maxTWO classification decisions. Current budget
is charged BEFORE encoding each decision. First input11internal/4acquisition/step8.
After an attempted delivery,post input7internal/3acquisition/step12 for all five modes,
with actual current observation fields and last_outcome. No reset to training12/4/7.
The failure scenarios retain original unknown status,None value and empty reference;
all other facts/identities/scope/clocks remain unchanged. Successful admission alone
adds the delivered0or1 and its verified source reference. No duplicate intent remains.

Initial SUFFICIENT -> no acquisition and no second decision. Initial NEEDS -> sole
unknown target via preserved inverse binding;C172/C173 attempt;then raw reclassification.
After failed admission,correct answer is the SAME necessity label as before. This
also matters for controls that unnecessarily query a sufficient task:they should
still classify that task sufficient despite an unknown,not merely inspect missingness.
After successful admission,correct necessity is SUFFICIENT. Wrong post decisions are
not corrected by a fault flag. NEEDS ends UNRESOLVED without retry. A false SUFFICIENT
is retained and scored,not hidden behind a deterministic safety replacement.
These are classifier outputs,not verified answers or RuntimeState ANSWERED terminals.

Budget units are bookkeeping,not exact CPU operation counts. No permission withdrawal,
exhausted initial budget,multiple-target selection,learned retry or durable state claim.

## Replay and fixed workload

First restore all6models and replay all9396original PILOT rows with original1024batch
order:56376predictions,raw decisions exact/logitsabsdiff<=1e-6,rtol0. No TRAIN replay.
For FOUND_ZERO/FOUND_ONE,replay C185saved live inputs/decisions/logit-presence exactly
and logitswithin1e-6 in all32matched blocks,including both rules. All new fault blocks'
INITIAL phase must likewise reproduce C185completion0inputs/decisions/logits:the
fault is introduced AFTER this phase. A disagreement here is execution drift,INVALID,
not a new scientific result. Source NPZ axes,policy IDs,rows and layouts are checked.
New fault POST decisions are the measured behavior;finite errors become VALID NEGATIVE.

|Registered quantity|Value|
|---|---:|
|Rows / layouts / scenarios / policies|3712 /2 /5 /8|
|Blocks / episodes|80 /296960|
|Per-policy episodes|37120|
|Candidate episodes,3internal models|111360|
|Rule episodes|74240|
|Initial live neural rows|222720|
|Post live neural rows|measured0..222720|
|Static replay rows|56376|
|Total neural row upper bound|501816|
|Checkpoint loads / fresh seeds / training|6 /0 /0|
|Correct-candidate attempts / skips|23040 /88320|
|Correct-candidate admissions / non-admissions|9216 /13824|

Counts after the initial decisions depend on RAW predictions,not truth labels.
Measure actual provider calls,read bytes,reservations,publications,non-admitted attempts,
forward rows/batches,seven shared-cell calls/batch and debit units. Normalized repeated
inputs are actually forwarded,not substituted by cached previous decisions.
CPUfloat32/two threads/deterministic algorithms,batch1024. No parameter changes.
MISSING_RULE:3712calls per block,2944unnecessary attempts;on the three fault blocks
per layout its post decisions wrongly sayNEEDS on2944sufficient cases. NEVER_QUERY:
0calls and768missed attempts per block. Deliberate baseline errors stay in results.

## Fixed deciding gate

All80blocks must complete. Each of three INTERNAL_SEMANTICS candidates must have
zero failed episodes over37120episodes:correct initial decisions,no missed or
unnecessary attempts,correct raw post classification,zero false sufficiency after
non-admission,and exact unchanged-evidence/receipt/target/resource/outcome contracts.
Successful candidates admit9216total;failure candidates correctly remainNEEDS for
13824total attempts. These expectations do not override actual decisions.

All policies must have zero measured contract errors. Both rules must show the fixed
patterns above. FINAL_ONLY scientific errors remain descriptive. Any finite measured
violation -> ACCEPTED VALID NEGATIVE after review;retain cases and finish all independent
blocks. Malformed/nonfinite/source/hash/unchanged-replay/incomplete/protection failures
->INVALID EXECUTION;restore SAME C186 validity without changing scientific conditions.
No threshold relaxation,row exclusion,checkpoint repair,newseed or rerun-until-PASS.
Either outcome preserves C185PASS,C182negative and all prior evidence.

PASS supports frozen classification remaining evidence-sensitive through these bounded
non-admission events. It is NOT full failure recovery,self-chosen retries,verified
answers,natural language,general reasoning or final Gate E. Same4development semantic
groups are reused. No independent sample-size claim from layouts/scenarios/seeds.

## Outputs / integrity / implementation tests

13artifacts excluding summary:plan,replay,results,gzipJSONLtraces,NPZ plus8source snapshots.
NPZ:policy8 xlayout2 xscenario5 xrow3712 xphase2;save raw inputs/decisions/logits and
logit_present. Missing decisions-1;zero absent/rule logits are NOT learned scores.
Traces retain initial/final complete packets,bindings,maps,actual action/dispatch/receipt,
raw decisions and post-hoc scores. Group counters and false sufficiency are recorded.
Non-admission itself is expected behavior,not a scoring failure or an implicit zero bit.

Inherit C185.precheck through all former source/artifact guards. Add accepted C185summary
and13artifacts,4prior source pins and4ownfiles:92historicalpins/200protected input paths,
plus outer C37/composition fixture. Source files/older models are never overwritten.
Parent summary843fb9816270e4a597ca094c6e90408a35910490324db60bc3018f62156ac949;
parent executionHEAD36c0ab26de2334f8b54d3e0754bf408deec7f0db.
Manifest SHA2560cbe7212e5bafd9fc52f3f315d2d4732afaca6eb11940c6fa16ac58aeb336edc.

32/32new helper tests PASS on the ACTUAL complete new module. Tests are deliberately
self-contained:synthetic delivery dataclass/fetch/error,synthetic complete packet-shaped
traces,score/gate/replay arrays. They validate injection order/nonmutation,value-only
corruption,unrepaired mistakes,known0versusunknown,live-debit/outcome invariants,scope,
pending/terminal restrictions,strict complete gate and fixed manifest. They DO NOT
exercise the complete old C185driver/C173owner/checkpoint/artifact chain. No copied or
substituted old runtime is presented as actual integration. No official model scores
have been measured while implementing/testing C186.
Two new Python files compile;three embedded Python runner blocks parse. Windows PS
itself,all1317tests,full200input chain,and296960officialepisodes remain UNEXECUTED.
Local Git network lookup failed DNS;no complete local checkout was available.
Wall-clock/actualIO/serialized bytes will be recorded;no production latency/peakVRAM claim.
**1317expected=1285+32;70modules.** One regression then one frozen batch.
Run tools/run_c186.ps1 with C185/C184/C183/C182/C181/C180/C179/C178/C177/C176/C174summaries
and ExpectedHead. Progressstatic56376replay,blocks1/80..80/80,RESULT/POSTCHECK.
Judge C186 ->ledger/handoff->next design. **No C187 before judgment.**
