# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md Current response format (v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Assistant authors/tests/registers; user executes locally. No Codex handoff.
Native Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5; PowerShell7 / ParseFile / active_v2.
Accepted sources/tests/contracts/logs/dispatchers remain immutable.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C343 ACCEPTED PASS (DIAGNOSTIC INTEGRITY).**
C342 remains ACCEPTED VALID NEGATIVE, candidate_gate=false / eligible_seed_count=2.
**C344 NOT REGISTERED.** No ACTIVE experiment during acceptance/authoring.
No production adoption. Do not rerun accepted C343.

## Latest accepted evidence

Report: docs/experiment-ledger-addendum-c343-c344.md.
Scientific execution: 1effc2138967715e9e9319e1da19c3653e4fd9ac.
Log publication: 74eda8f681f7a68f1d8c4ae91203c2b151855ce6, sole parent execution.
Only latest.json/latest.log added; seven reviewed implementation files unchanged.
6442 tests / 237 modules PASS; zero failures/errors/skips; 2956.442 seconds.
237 matching module begin/end and test-footer records; all 240 process exits zero.
923 sources / 7693 inputs; all 7693 final uncached rereads; fresh verifier complete.
run_execution_valid=true; child scientific forward/update counts zero.
Windows log 890204 bytes SHA bd3f00df72c1995e1880bb0f9b9faaa99b346e46b9e46434321b02cafa2ced3d.
Git LF 886413 bytes / 3791 lines matches metadata by exact CRLF reconstruction.

All 144 strata / 30 criterion summaries, 261 failed local / 141 failed order rows,
120 normal support / 60 paired normal summaries independently reconcile. All parent
C342 support, answer/pair rescues/regressions and failure counts remain identical.
Full analysis: 4320 local / 2160 order cells, 51840 normal observations,
25920 paired answers / 12960 query pairs. These are distinct counting units.

Candidate interior4 has 131 actual TRAIN errors, all wrong_observed: 342001=99,
342005=32. Among 1440 TRAIN query pairs, 1312 both correct, 125 one correct and
three neither correct; the latter groups imply same-value collapse / swapped values.
TRAIN improvement 2677->2749 includes 132 rescues and 60 new regressions.
HOLDOUT improvement 1295->1366 includes 101 rescues and 30 new regressions.
Candidate original6 errors are all new: TRAIN six wrong_observed, HOLDOUT six
absent_digit; zero persistent wrong answers in either split. Names of length6 were
never fitted, even on TRAIN value combinations. No mask-only failures in either arm.
C342 full candidate 2/5 stays unchanged. Error location is not a causal mechanism.

## Next one-question boundary

Prepare C344: ordinary mean CE versus pair-max full256 CE on identical mixed45
TRAIN streams, fresh five paired seeds, fixed 2400 updates, same architecture,
readout, optimizer/rates and data. Pair-max averages max(CEa,CEb) over 24 complete
query pairs. torch.maximum ties split gradients symmetrically. No new forward,
parameters, examples, output filtering or teacher information at inference.
Historical C268/C288 paired auxiliaries were valid negatives; this is a different
within-pair reduction, not a claim that all paired objectives were untested.

Proposed fixed gate: all five candidate full gates; each seed/domain/split normal
answer AND pair gain >=0; strict aggregate interior TRAIN/HOLDOUT answer/pair gains.
Saturation/ties remain valid negatives. Record full final TRAIN/HOLDOUT support,
collapse, counts and individual rescue/regression contrasts without selected groups.

## Parent contract and authoring requirements

Parent folder: runs/c343-mixed-length-localization-f1a8f5665ebb48c98b273cb549e721fd/.
Primary: 883c1c0142173f038bec25f65589643af9ba40ef2442e7c376b845a61f1477ce.
Envelope: 275ac041de4a858ca5a7f50aabb16898e85befebb2ee3ba6159a06198a7c993a.
Manifest: 7e5de7e3040acd3d7aff1a748e8b7b97d36461badaa0c65c612b3f3a5e3c12d6.
Retain all 483 outputs, including 477 regression proofs; parent 923 sources / 7693 inputs.
C343.semantic_recheck(out343,out342,data_out,cx,read) has five arguments. Call the
C343 benchmark directly; its executor.parent_semantics only verifies C342.
Canonical data is root/h['c330'].PARENT_FOLDER/science (accepted C329).
Parent ordered6442 ID SHA0581297af93ba5c06494f1e41627de8a2f574ee2ef62a46147225a55755ad7f5.
Seven OWN additions imply 930 sources / 8183 protected inputs; actual test count
must come from real loaders. Preserve sole inherited C204 exclusion and parent prefix.

Complete source/tests/preregistration, all direct/lazy dependency coverage, zero
unbound names, actual AST/inventory and independent remote-byte review before ACTIVE.
No launcher until review PASS. Separate acceptance and next-source commits.
Native user artifacts were not transferred to author checkout; native protections
must be verified at execution. Freeze branch while user runs. INVALID retries same C;
publication-only failure repairs transport without retraining.

## History and inherited compatibility seal

C343 pre-acceptance: docs/handoff-history/c343-pre-acceptance.md.
C343 review: docs/c343-post-authoring-review.md.
C342 report: docs/experiment-ledger-addendum-c342-c343.md.
C272manifest seal89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.
