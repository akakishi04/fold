# FOLD experiment ledger and handoff

Updated: 2026-11-22 Japan time.
Conversation protocol: docs/experiment-conversation-handoff-protocol.md, Current response format v2.

## Formal state

Gate A/B PASSED; Gate C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C344 ACCEPTED VALID NEGATIVE.** Execution revision C344-R1 completed validly.
candidate_gate=false / eligible_seed_count=2. Attempt01 remains INVALID EXECUTION.
C343 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY); C342 remains ACCEPTED VALID NEGATIVE.
**C345 NOT REGISTERED / AUTHORING PENDING.** No active experiment is executable yet.
No production adoption. Do not rerun accepted C344 or delete its retained artifacts.

## Latest accepted evidence

Report: docs/experiment-ledger-addendum-c344-c345.md.
Scientific execution:8d1e1170cd614503deab1e09474fe82de4bba561.
Publication:9d163289775373aaf62028a7b8aeacbfb41593a6,sole parent execution,only latest.log/json.
Windows log355860bytes/SHA256aba71fc3bba513a3dab51a34b46b06641b1b0f5c2fa713c201c3491643867b49.
Git LF352156bytes/3704LF reconstructs that original exactly.
Full6514tests/239modules PASS in3208.100s,zero failures/errors/skips.
All242 module/regression/science/verifier exits0; six native timeout cleanup checks PASS.
930sourcepins/8183protectedinputs; all8183final uncached rereads and fresh verifier complete.
run_execution_valid=true. All10fits finish before evaluation/replay; science24000updates/
27420model forwards/1480320rows. Saved states, exact argmax replay and arithmetic verified.
Complete10seed/120normal/5paired/60contrast records pass the immutable summary validator.

Full-gate count2/5 in both arms, but different seeds:control344004/344005;
candidate344001/344005. Seven of60contrasts regress on both endpoints,14/120inequalities.
Interior TRAIN answers2864->2728/2880;pairs1424->1293/1440.
Interior HOLDOUT answers1430->1331/1440;pairs712->640/720.
Strict gainsTRAIN(-136,-131),HOLDOUT(-99,-72):all negative.
Interior TRAIN rescues16/regressions152;HOLDOUT rescues10/regressions109.
All candidate interior errors are new relative to the paired control.
Original6 improves overall(TRAIN2875->2877,HOLDOUT1431->1438),but344004regresses.
Original2/3/4 perfect botharms;original5candidate has one new TRAIN error.
No optimizer,clipping,pooling or capacity cause is proven.

## Preserved native artifacts and successor boundary

Folder:runs/c344-pair-max-training-76ae8eb6e3bf4d08ac577c5fde9e0caa/.
Primary610398ced893ff1d1885faf9bd02ffef57779ca2bd96bfa995b6929e6d8f20d7.
Envelopec77f0fcf5fcbbf59d3961894713dbf8dcb30ae89841df0325b980a07d8913562.
Manifesta663ebb0b09671c6d277b5abec6d09604a49a194d5d61409a1a5bf5018785ad8.
Accepted executorblob76c8663caafc97ece440df71e250e546198d425b;
benchmarkblob6261a0c267df027835093c7ce53958f8f0034186.
Retain ALL489parent outputs:six science files+primary+envelope+481regressionproofs.
The481are three records plus239JSON/log pairs. SevennewOWNfiles imply937sources/8679inputs.
Parent helper requires model_c344_pair_max_training.semantic_recheck(out344,data_out,cx,read),
four arguments under no_neural. Do not substitute C343-only semantics.

## Next one scientific question

C345 is a saved-objective/trajectory diagnostic:does worse pair-max binding coincide
with a higher matched terminal pair-max loss,or a lower surrogate despite worse exactanswers?
Use all10saved states' full256 normal predictions across6domains and2splits;compute
bothCEreductions and bind normal answer/pair counts to accepted C344.
Use all24000preupdate loss/norm records,fixed200stepblocks,and complete cycle/slot/profilegroups.
Canonicalslot4 is mixed original4/original5/interior4,not a pure-family trace.
Zero new model forwards/backwards/updates;no seed/threshold/coefficient retuning.
No exact learned-then-forgotten claim from minibatch traces;no causal clipping claim.
Per-domain terminal losses are not an overall exposure-weighted training objective.
Diagnostic integrityPASS will not replace C344's negative capability judgment.
Source/tests/preregistration and independent remote review must complete before activation.

## History and compatibility

Pre-acceptance handoff:docs/handoff-history/c344-pre-acceptance.md.
Original failed attempt:docs/experiment-run-logs/c344/attempt-01/latest.log and latest.json.
R1 contract:docs/c344-recovery-r1.md;review:docs/c344-r1-post-authoring-review.md.
C343 report:docs/experiment-ledger-addendum-c343-c344.md.
All accepted science/test/launcher/preregistration bytes remain frozen.
The C272 manifest seal remains89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.
