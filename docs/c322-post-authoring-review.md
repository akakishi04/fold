# C322 post-authoring review

post_authoring_review = PASS
Scope: committed-byte/static review plus executed local software tests,NOT actual parent-data science.
Review target:6da3aba9af21754e1616148e07cd6b316913f8f5.
Acceptance base:9025d339a67ae4b4b22435b8bda068c204d49d5e.

## Remote committed bytes

All6 OWN files were refetched from the immutable authoring commit. The264line science module
and234line test module were read in complete consecutive ranges;the other4 files in full.
Returned blob IDs were compared with independently computed local Git blob hashes,6/6:

- fold_lm/v05_benchmarks/model_c322_saved_query_contrast.py:c93fb85922c5907c424698897de4af2888f81f77;17312bytes.
- tests_lm/test_v05_c322_saved_query_contrast.py:05616da76649531810127c31d9b3a507d4021c2e;17364bytes.
- tools/run_c322.ps1:6e1fdd1a52c7849b864ac86479681e7d4130f6d3;9581bytes.
- tools/invoke_c322.ps1:c03b4a54fd5086dba23e029c280d4d439b811f50;7905bytes.
- docs/experiment-ledger-addendum-c322-preregistration.md:d9f4be707e1b96f115d33dc9d5191e8f1a9fae79;6066bytes.
- docs/v5b-saved-query-contrast-v0.1.md:76f9c845eb6bf9ae6a70e5497b6dbbec55fe8f35;1019bytes.

Remote compare against acceptance shows exactly these6 additions. No accepted source/test/log/
preregistration/dispatcher changes. The initial tree-creation attempts with an invalid base-tree
reference/unavailable blobs failed without branch changes;only the successful final tree and
this immutable commit are review targets. Activation must retain all6 reviewed blobs.

## Tests actually executed AFTER refetch and hash comparison

Normal complete module:24/24 PASS in5.674s;zero failures/errors;process exit0.
Default-CP932-emulated complete module:24/24 PASS in4.789s;zero failures/errors;process exit0.
The encoding patch spans module loading,setup,all tests and teardown;explicit UTF8 is retained.
Both runs were uninterrupted full unittest runs. Logs mechanically verified24unique completed
IDs per mode;none omitted. All6 hashes rechecked after tests. No pre-commit run is counted here.
Environment:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. CP932 emulation is not full Windows.
PowerShell executable unavailable;no native PowerShell parsing claim. Terminal cleanup messages
after OK did not change the successful process exit codes.

Both Python files and all3 embedded runner Python blocks compile. UTF8/noNUL verified. Recursive
symbol-table/import-binding audit found0 undefined referenced globals in both new Python files.
Manifest self-hash719cd169028e0c0ead99f4620035b532cefed65145c4bcb4f8af3c781fda01e8 matches.
48 launcher paths ordered C321..C274;postcheck paths[2:50],head[50],argc51 verified.

## Arithmetic,identity and persistence controls

Independent hand-numbered vectors check raw/offset-invariant distances,mA/mB/D and exact signs.
A constant shift produces nonzero raw distance but zero offset-invariant distance. A third-class
winner can give identical wrong argmax answers despite positive D and distinct vectors. All-class
ties preserve the original lowest-index argmax rather than forcing a supplied value. Nonfinite,
wrong shape/dtype,gradient-retaining tensors and identical target classes are rejected.

Pairing tests deliberately separate adjacent queries and verify canonical entity orientation.
Duplicate row IDs,missing query partners and incorrect target bindings fail. Correctness-category
conservation and complete8640pair/240group/40reconciliation inventory are exercised. Incorrect
parent totals,cohort truncation and changed policy provenance are rejected. All48 hash failures
occur before parent verifier dispatch. Actual child precheck exercises778/1467 temporary file
fixtures and rejects an unprotected local helper.

Actual child run/verify/runtime_preflight paths execute under a no-neural guard with controlled
saved outputs and substituted parent/Git/scorer interfaces. Only four JSON outputs plus summary
are written;torch.save and AdamW are forbidden in the production run fixture. Byte tampering,
semantic tampering with resealed descriptors,and existing-output-directory overwrite fail.
Semantic suite tests construct5270 unique IDs and preserve exact5269 retained IDs/order;they do
NOT run the real inherited5269 tests. CLI/context binding,UTF8 and runner-index contracts pass.

Local tests use synthetic logits and substitute parent/scorer/Git interfaces. They do not execute
the actual C321 archive verifier against the user's files or the real inherited scorer. No local
neural-model fixture or actual checkpoint inference is needed by this diagnostic. The test
results establish software behavior,not an observed C322 contrast outcome or model competence.

## Parent writer,scorer semantics and dependency audit

C321 writes fold-c321-interior-eval-v1 records with raw.before containing original1..6 and
raw.interior containing the three new families. Its saved logits were produced by the same C319
state under its own trained readout. C322 verifies48 expected summary hashes before calling exact
C321.verify_artifacts(C321dir,47ancestors,accepted C321 execution). Require valid parentFAIL,
pass_counts0/0,primary_gateFalse and all5 artifact descriptors. Reuse C321.load_parent on the tail
for validated logical data. Read evaluations.pt from C321,not a trained-model bundle or C320's
unequal-layout archive. Only raw.before['4'] and raw.interior NORMAL logits enter new metrics;
all masked views and old gates remain validated by the unchanged parent verifier.

Actual C270.score source at accepted blob88b94c92267b916b304ecd44a8d02f89ab0eb301 was inspected.
Its collapsed_pairs counts equal normal argmax for the two queries in each fixed language/entity/
permutation/value group. C287 normalize_task and partition at blob05ab28c666203eaf69506c024a2805f31986a3ff
were inspected:partition sums those answer-cell rows/correct/pairs/collapsed_pairs. The child
pair grouping uses the same logical keys and canonical query orientation,so those four totals
can reconcile exactly. It does not reinterpret collapsed as identical logits. C321.score_new
performs the existing new-profile adapter,while old4 uses C304.score_length. New arithmetic
compares targets only after inference;there is no restricted-value answering or task relabeling.

Sole direct science import C321. C320/C319 context and inherited scorer/audit/no-neural helpers
are existing protected dependencies. All772source pins and1455inputs remain verified;local lazy/
context/factory-language helper coverage required. Add OWN6 and6C321parentfiles ->778/1467.
Precheck returns its verified loaded inputs rather than loading them a second time immediately;
this is not cross-process caching or a verifier waiver. Protected hashes and repository guard
are checked again at end;postcheck freshly loads and reconstructs every JSON artifact.

## Runtime and interpretation boundary

Science uses saved17280normal answers grouped into8640query pairs,240groups and40reconciliations.
New model forwards/training/model-state loads/checkpoint writes/network calls are0. Recursive
verification still reads old tensor archives and uses memory/CPU;those costs are not claimed zero.
Raw output difference and offset-invariant difference are descriptive,not a new capability gate.
D sign and both-target-direction can improve without the correct256-way class winning. Equal
output cannot locate an information loss to any particular internal layer. Old4/new4 uses the
same length but different name families,not an independent dataset or fresh-seed replication.
C322 PASS is integrity only;C321's negative,C320's bounded PASS and Gate F remain unchanged.

Runner preserves the one-process ordered observed-suite approach,unique direct UTF8 diagnostic
logs,fatal traces where supported,immediate decimal/hex child exits and previous-preflight copies.
No automatic retry or new test exclusion. The Python blocks compile and were source-reviewed;
native PowerShell execution was not performed here. The earlier C321 interruption's cause stays
unknown despite its successful retry. No environment-fix claim.

Not executed here:48 actual parent archives/Windows protected files,native PowerShell ParseFile,
actual full5269regression or C322 analysis on real saved outputs. Mandatory user Validate/Execute
gates retain all of these. On integrity failure repair SAME C322;do not change metrics/cohort or
interpret diagnostic PASS as capability success. C323 waits for formal C322 judgment.
