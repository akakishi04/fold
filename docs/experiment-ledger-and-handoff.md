# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and Current response format(v2), Execution recovery mode.
Repository:akakishi04/fold; branch:feat/sft-target-loss; local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5; explicit PowerShell7/ParseFile/active_v2.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C335 ACCEPTED VALID NEGATIVE. C336 ACTIVE / INVALID ATTEMPT RECOVERY. C337 NOT REGISTERED.**
C336 attempt01 INVALID EXECUTION; no diagnostic result. No rerun of accepted C335.
C336 R1 source repair is authored; committed-byte post-authoring review is pending.
Do not issue a retry command before that review is recorded PASS.

## Current failure and repair

Failure execution:c0efb27bbabe969d5f90667437deadb1d9a39dec.
Publication:de6d6bb1d43b69d26f0463426fbf56229871d087;sole parent equals execution.
Log metadata SHA:f7436128435da8e2448860f3898bbbc4ca64a2cf549c34d6383044a41b2af7de;
7699 original Windows bytes. Exact archives:docs/experiment-run-logs/c336/attempt-01/latest.*.
Native lock probe passed; parent snapshot stopped while protecting module proofs:
ValueError:locked-file bound exceeded; no eviction fallback. Science exit1;
run_execution_valid=false. Full regression/diagnosis/final rereads NOT reached.

Cause:C336 omitted max_files when constructing accepted LockedHashes,using default4096
for a registered4360-input union. This is authoring error,not a scientific negative,
memory/hardware diagnosis or proof of model corruption. Recovery contract:
docs/c336-execution-recovery-r1.md. Pass max_files=s.INPUT_COUNT,retain ALL inputs,
finite capacity,no eviction/unlocked fallback,unchanged parent/replay/hash verification.
Only own executor/tests change; same32IDs/6090tests/226modules/877sources/4360inputs.
Benchmark,manifest,preregistration,accepted R4 implementation,runner/launcher unchanged.

## Authoritative scientific scope and latest accepted parent

The complete pre-repair handoff is preserved verbatim at
 docs/handoff-history/c336-pre-recovery-r1.md.
C335 acceptance:8984740dcc538cf785ca2fdc96db735b9ff8a4a1;
report:docs/experiment-ledger-addendum-c335-c336.md.
C335 execution:3b185a97ef86ab911d425620b4e6645fbd0c9f9e;
publication:2587c5905e137728f22de06321c3e41943038945.
6058tests/225modules passed; scientificFAIL/executionvalid; eligible1/5.
No alternating/first_mean/off-diagonal/production adoption; older verdicts unchanged.
C335 folder:runs/c335-alternating-training-7dd29eebabd64360b31b40985bd6fd40/.
PrimarySHA6624fc176f349f7688af45da55ac5855951e7094c824201b16fe127b92aa25c4.
EnvelopeSHA70f5102a454db4370533f8da2f765d2e4eac6ab29d0bb93f5f4cbe976b9b5ab0.

C336-v5b-saved-query-order-patterns / V5-B-SAVED-QUERY-ORDER-PATTERNS.
Unchanged contract:docs/experiment-ledger-addendum-c336-preregistration.md.
Scientific manifest:e6f992e680bc4b80284dbc04366566f737fb1bfd3f55fb0ac10d76d90ebd76af.
All10C335states/native+alternating,allTRAIN/HOLDOUT,en/ja,original2..6/interior4,
all profiles/entity/value/query/order conditions. Saved256-way argmax,unmodified.
12960four-responsegroups/6480pairedgroups/51840answers/720strata. No new model
forward/training/state load/optimizer update. PASS concerns diagnostic integrity only.
Seven exclusive response categories and all30parent HOLDOUT contrasts unchanged.
Original1/masked views remain in parent/full114-view validation. C335negative preserved.
Parent maps871/3893 plusALL461parent files and6own ->877/4360. Mandatory parent
regression proof semantics,source pins,native leases and all4360final uncached rereads.
Full6090 tests precede diagnosis; no new skips or exclusions. BaseID SHA
0e87a5c604e102e837f606fcb5a731c80f1abee1381e63d20076f2e849f0c3be.

## Execution and stops

active_v2 ->invoke_c336 ->run_c336 ->c336_execution. Existing AST preflight retained.
Role C336-SAVED-QUERY-ORDER-PATTERNS. New locked_input_capacity logs4360/4360.
Preserved parent candidate_gate=false is expected,not an error. Complete requires
persisted_query_order_patterns PASS,execution_envelope_verified,run_execution_valid=true
and log publication. Any technical failure repairs SAME C336,no C337. No automatic
retry,scope/gate relaxation,accepted-source mutation,package reinstall or data deletion.
A publication-only failure repairs publication alone. Never substitute publication
HEAD into an old command to bypass RESULT_ALREADY_PUBLISHED. Fetch live latest logs;
do not use old C323/C324 attachments as C336 evidence.

## History and inherited compatibility seal

Prior handoff/reviews and every earlier attempt remain archived. Original C311native
fault cause remains unestablished;this failure is a Python capacity guard,not that fault.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
