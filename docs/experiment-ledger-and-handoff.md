# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and Current response format(v2),Execution recovery mode.
Repository akakishi04/fold;branch feat/sft-target-loss;local M:\asobiba\fold.
Runtime Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5;PowerShell7/ParseFile/active_v2.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C335 ACCEPTED VALID NEGATIVE. C336 ACTIVE / INVALID ATTEMPT RECOVERY. C337 NOT REGISTERED.**
C336 attempts01/02 INVALID EXECUTION;no accepted diagnosis.
C336 R2 implementation and committed-byte post-authoring review complete.
post_authoring_review = PASS.
Source/review target2072b613055093e600fdafe4807de3fa77f5c2ad.
Use the subsequent documentation-only final recovery HEAD supplied in the user
command,not source-review,old execution or log-publication HEAD. No C335 retraining.

## Operational skip and actual latest attempt02

User's STALE_EXPECTED_HEAD specified C335 execution3b185a97ef86ab911d425620b4e6645fbd0c9f9e
against current3ab32fc78d924914b07141d4a009de3c8e39fcbe. This invocation executed and
published nothing. It is operational,not another invalid scientific attempt.
Current3ab32f was the already-published C336 R1 log,not a new registration.

Actual attempt02 execution5029fbbad2209f462af8939c0e77f56a5a63be5e;
publication3ab32fc78d924914b07141d4a009de3c8e39fcbe,sole parent matching execution.
Publisher197751Windows bytes;SHA256
45d503dddd1abdffe9ed6e44bdbc04495ae009a62759349429754347c4abaab5.
Log blobdefe297ea99b6ca185aab39947c09c874d4540ee;
metadata blobe4a09ba1b5f9ce8953457e2e971ec3ed19624db3.
Exact archives docs/experiment-run-logs/c336/attempt-02/latest.*. Attempt01 retained.
Native locks,capacity4360,parent semantic validation and877source/4360input registration
passed. Full6090tests/226modules PASS,0failures/errors/skips,1680.515seconds.
OrderedID SHA469a8865f79307ef97c8dba2eac3d87d522f75f80fb7c16e34c64510a9ee5132.
Then saved_query_order_patterns -> run_diagnostic -> analyze -> logical_groups raised
ValueError:logical row semantics. Science exit1;run_execution_valid=false.
No complete diagnosis,final uncached rereads or fresh verification. Full regression
success alone does not validate science. R1 capacity defect did not recur.
Remote review inspected startup,regression completion and failing traceback;no
independent full-Windows-log rehash or local trained-artifact reconstruction claimed.
Do not use old attached C323/C324 logs as current C336 evidence.

## R2 schema repair and completed review

Contract docs/c336-execution-recovery-r2.md;
review docs/c336-r2-post-authoring-review.md;
amended docs/experiment-ledger-addendum-c336-preregistration.md.
The accepted canonical writer uses two distinct integers from0..3,NOT a0/1-only
catalog. C336's logical_groups and classify had each enforced the wrong binary range.
This was an authoring/schema audit error;the synthetic dataset duplicated it.
R2 corrects those two guards to values0..3 and targetbytes48..51,requiring distinct
integers and exact target/query binding. All256-way argmax/taxonomy unchanged.
Third values remain other_class even when in0..3 but absent from the observed pair.
No data/prediction rewriting,wrong-answer repair or post-hoc subset selection.
Original erroneous preregistration archived c336-pre-r2-preregistration.md;R1handoff
archived c336-pre-recovery-r2.md under docs/handoff-history. Both attempts retained.
No accepted historical source/test/contract edits. R1executor,runner,launcher and
active dispatcher unchanged;explicit max_files=4360 and all final rereads remain.

Committed benchmark/tests/amended contract reread throughEOF at2072b613;returned
Git blobs match tested local bytes. Source compare confirms minimal scope. Post-reread
normal32/32PASS6.349s,CP932-default-text-open emulation32/32PASS6.860s;0failures/errors/skips.
Compile/import/UTF8/noNUL/no trailing whitespace checks passed. Recursive global audit
199code objects,undefined0. Same32test ID order/digest:
96ce8e07f180137d2035601083aade23244cac87e83f23dfae3eff23940a2b73.
Each old guard restored separately is rejected by actual run_diagnostic on canonical
rows before output writes. Expected negative-control exceptions,not suite failures.
Reviewed source restored;file hashes and unchanged manifest rechecked afterward.

The exact canonical192TRAIN/96HOLDOUT dataset is reconstructed independently and
checked against frozenSHA and C267.dataset/validate_data. Tests cover all12ordered
value pairs*16two-value response patterns,third-digit behavior,row-order invariance,
bad ranges/types,complete12960quad/6480transition writer/reconstruction and all30
parent contrasts with explicit synthetic predictions and ancestor/scorer callbacks.
R1 capacity/proof/tamper/failure-ordering tests remain intact.
Author environmentLinuxPython3.13.5/Torch2.10.0+cpu,targeted tree,not full checkout.
Two historical author dependencies are verbatim source EXTRACTS:C267 data/render/
validator and C324LockedHashes with helpers/constants. They are NOT complete modules
or native Windows locks and are NOT committed. User tests import full accepted
protected modules. No actual C335prediction archive,Windows/full6090run or pwsh AST
execution claimed. Standard user-side dispatcher/launcher/runner AST chain mandatory.

## Fixed scientific scope and accepted parent

C336-v5b-saved-query-order-patterns / V5-B-SAVED-QUERY-ORDER-PATTERNS.
Manifest unchanged:e6f992e680bc4b80284dbc04366566f737fb1bfd3f55fb0ac10d76d90ebd76af.
All10C335saved states,seeds335001..335005,native/alternating,native evaluation policy.
Original2..6/interior4,TRAIN/HOLDOUT,en/ja,all profiles/entity/value/query/order cases.
12960four-responsegroups/6480pairedgroups/51840normalanswers/720strata.
No new model forward,training,gradient,optimizer update,state load or checkpoint.
All seven categories and30parent contrasts remain;diagnostic PASS means integrity,
not capability. C335negative,eligible1/5 and GateFNOTPASSED remain.
Original1/masked views remain in full parent114-view validation,not new taxonomy.

Canonical source model_c267_name_coverage_training.py blob
5a167f078ab5b3aa8052e7995d004a25ca25fc0f;
DATA_SHA1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
HOLDOUT value pairs(0,2),(1,3),(2,0),(3,1);TRAIN the other8ordered distinctpairs.
Integer entity subsets(0,1),(0,2),(1,2);targets48+queriedvalue. No scientific data change.

C335 acceptance8984740dcc538cf785ca2fdc96db735b9ff8a4a1;
execution3b185a97ef86ab911d425620b4e6645fbd0c9f9e;
publication2587c5905e137728f22de06321c3e41943038945.
Folder runs/c335-alternating-training-7dd29eebabd64360b31b40985bd6fd40/.
PrimarySHA6624fc176f349f7688af45da55ac5855951e7094c824201b16fe127b92aa25c4.
EnvelopeSHA70f5102a454db4370533f8da2f765d2e4eac6ab29d0bb93f5f4cbe976b9b5ab0.
Parent871sources/3893inputs plusALL461parentoutputs and6own ->877sources/4360inputs.
All direct/lazy data/scorer/recovery dependencies remain protected. No smaller-map
fallback or omitted supplementary module evidence. Reconstruct immediate C335 saved
semantics via its unchanged four-argument semantic_recheck under no_neural;no older
recursive semantic bodies,model inference or optimizer replay. All inherited bytes
still checked. NativeR4 held leases,independent initial hashes,4360final rereads and
four byte/size-bound diagnostic outputs remain mandatory.

## Execution, expected progress and stops

Same32own IDs/6090selected tests/226modules,sole inherited exactC204mutable-ACTIVE
exclusion only. Base6058ID SHA
0e87a5c604e102e837f606fcb5a731c80f1abee1381e63d20076f2e849f0c3be.
Sequential fresh module processes with accepted R1.2PID/log/test validators. No new
skip,exclusion,cached success or retry. Previous6090receipt is not reused after edits.
Standard active_v2 ->invoke_c336 ->run_c336 ->c336_execution;unchanged AST gates.
Role C336-SAVED-QUERY-ORDER-PATTERNS;locked_input_capacity=4360/4360.
Parentvalidation ->full6090regression ->saved_query_order_patterns ->saved_diagnostic_reconstruction
->4360final_uncached_input_recheck ->independent freshverification ->console publication.
Print720C336strata and preserved_parent_gate=false(expected). Complete requires
persisted_query_order_patternsPASS,execution_envelope_verified,run_execution_valid=true
and log publication. No scientific training-step progress expected.
Local runs/c336-query-order-<id>/science plus226moduleJSON/logpairs andregressionrecords.
ConsoleONLY docs/experiment-run-logs/c336/latest.log/latest.json. Exact earlier logs
are retained. Future successor must inherit455proofs+6science/summary/envelope=461outputs
and explicitly configure its own registered protected-input capacity.

Any technical failure repairs SAME C336;no C337 or automatic rerun. Unfavorable
behavioral distributions are valid evidence,not permission to retry. Publication-only
failure repairs publication alone. STALE_EXPECTED_HEAD/RESULT_ALREADY_PUBLISHED are
operational;never use current/publicationHEAD to bypass a registered literalHEAD.
No CI,paidservice,package reinstall,artifact deletion or accepted C335retraining.
User may report finished;fetch live latest metadata/log. Valid result requires
acceptance AND next-C implementation/preregistration/committed review/activation/command
in one response. INVALID stays sameC. No unrelated branch movement while user runs.

## History and inherited compatibility seal

Both C336invalid attempts,all earlier reviews and pre-R2 handoff/contract archived.
Original C311native-fault cause remains unestablished;this is a schema error.
- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604
