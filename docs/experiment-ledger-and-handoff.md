# FOLD experiment ledger and handoff

Updated: 2026-11-22 Japan time.
Conversation protocol:docs/experiment-conversation-handoff-protocol.md,Current response format v2.

## Formal state

Gate A/B PASSED; Gate C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C345 ACCEPTED PASS (DIAGNOSTIC INTEGRITY ONLY).** Execution C345-R0 valid.
C344 remains ACCEPTED VALID NEGATIVE,candidate_gate=false/eligible_seed_count=2.
C344attempt01 remains INVALID. No capability improvement or production adoption.
**C346 NOT REGISTERED.** Prepare the next one-question comparison and independent review.
C347 NOT REGISTERED. Do not rerun accepted C344/C345.

## Latest accepted evidence

Report:docs/experiment-ledger-addendum-c345-c346.md.
Scientific execution:c81ffe102c3a9280f28a68e572403549ce77fa1d.
Publication:25ff2f93ce63c9668f3111672caf75db095d2f45;soleparent execution,onlylatest.log/json.
Original Windows759318bytes/SHA2569531d1f7ae6e9be8c220954dd0f233a9c20844e94a983765d0b673105865fc9a.
Git LF755410bytes/3908lines reconstructs original exactly.
Full6578tests/241modules PASS3385.166s,failures/errors/skips0;all244process exits0.
Sixnativecleanup checks pass,C344-R1implementation receipt bound toC345head.
937sources/8679protectedinputs,all8679finaluncachedrereads,freshverifier complete.
FullID SHA2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a.
Parent6514IDs exactorderedprefix. All630publicrecords/parentbindings verified.
Console omits source_trace_sha256:no reviewer-side fullC345summary/nativeartifact reconstruction.
Native persisted/freshsemantics explicitly attributed;run_execution_valid=true.

## Findings and limits

InteriorTRAIN meanCE .011673977->.111296027;pairmax .020316586->.192509275;
answers2864->2728/2880. HOLDOUT meanCE .025826478->.288532880;
pairmax .045815971->.499002482;answers1430->1331/1440.
All10interiorseed/split contrasts worse onbothlosses;all7answer-regressing
seed/domain/split contrasts alsohigher bothlosses;0oppositesign atthisgranularity.
344002answers+2eachsplit despitehigherlosses. Original6aggregate answers/losses improve.
Norm>1 1975->5830/12000;cycle2mixedslot4 162->1241/2000.
Not exactclippingcalls,convergence,causaloptimizer/clipping or learnedthenlost proof.
Slot4mixedoriginal4/5/interior;terminaldomainmeansnotwholeexposureweightedobjective.
Original6TRAIN names neverfitted. PreserveC344false/eligible2 andGateFNOTPASSED.

## Accepted C345 artifact contract

Folder:runs/c345-saved-objective-audit-749db4a6ede44b608c06ee1461b6e393/.
Primarycfc3fe5b8f4ec927d875e2a016a940b5d34aac9ef14d93644eeb26567c0e1f30.
Envelopee883c26d1df24d940cd51b551f06e46e7ac69da216ea6024dc299ee24d2cceab.
Manifest5e69553fd6661ef46459883500fd719b474fd7cacbd17d002c957eb3fb2f1a9f.
Primaryfold-c345-diagnostic-v1;envelopefold-c345-execution-envelope-v1.
Validation summary is diagnostic,nested parent_validation_summary retainsC344negative.
C345semantic_recheck(out,parent_out,data_out,cx,read) takes5arguments underno_neural.
C344semantic_recheck(out344,data_out,cx,read) takes4arguments;keepcontractsdistinct.
Keep ALL491C345outputs:4science+primary+envelope+485proofs(3+241JSON/logpairs).
Inherited8679inputs/937sources;acceptedsource/test/launcher/preregbytesimmutable.

## Proposed next question, not activation

Fixed half-rate pair-max frominitialization versus defaultpair-max,with ordinary
meanCE default-rate strongreference. Freshpairedseeds,2400updates,mixed45data,
sameweights/streams/core/clipping/objective/evaluation withinpairmaxcomparison.
Question is binding+retention,not optimization-improvement gate. Terminal losses
are descriptive,not convergence/causalclipping proof. Full sourcecounts/tests/gate
andcommand belong toseparateC346registration andindependentremoteauthoringreview.
Do not issue anexecutioncommand before reviewedactivation.

## Historical and documentation context

docs/handoff-history/c345-pre-acceptance.md preserves previousactivehandoff.
docs/experiment-ledger-addendum-c344-c345.md preserves C344R1acceptance.
docs/cross-experiment-evidence-synthesis-2026-11-22.md and
cross-experiment-evidence-index-2026-11-22.json are unchanged C344-bounded snapshots
from45c18e39399a6f5ec073257d860377ecb624bd51;C345pendingthereis historical.
After nextactivation integrate main preserving allmain-onlysourcefiles andnotes.
