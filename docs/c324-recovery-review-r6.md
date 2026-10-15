# C324 R6 post-authoring review

post_authoring_review = PASS
Target HEAD:8fd4ef3ef287212735d568c805db8d56236c6a31.
Base:f7a909f2e1a0b4bd5d03c0a54bcb63519b022b19.
Review date:2026-10-16.
Scope:authoring readiness for the SAME C324 scientific retry. This is not a claim
of a successful Windows R6 run,5490-test execution,model fitting or native-crash fix.

## Remote-byte review performed after committing

All4 executable/test files and the full R6 contract were fetched at the immutable
target commit and reread. Python sources were read in consecutive ranges through
their entry points. Returned Git blob identities match separately computed local
raw-byte Git blobs. No executable file changed during this post-commit review.

| File | Git blob | Bytes |
|---|---|---:|
| tools/c324_scientific_recovery_r6.py |353f54f1bd66117728839049e99b17fc3aee4bf2|26045|
| tests_tools/test_c324_scientific_recovery_r6.py |7354ef2dd4afced0e1723b3c7cc12c90585f8663|17967|
| tools/invoke_c324_scientific_r6.ps1 |070499d688d8daf371649d58fb24857082a21a47|2841|
| tools/invoke_c324.ps1 |1f55a57029837bab4535811fc214711473f5f00a|9296|
| docs/c324-scientific-recovery-r6.md |6df3b0bef9ecd413b8df304b33cc0cdd9b087d21|9751|

UTF-8/no literal NUL checked. Both new Python files compile. Symtable review found
zero unresolved global names after accounting for Python-provided __file__ and
other module globals. Source-string assertions were matched to the actual named
functions. All50 parent path lines and the old normal launcher body remain exact;
the launcher's changes are one recovery action and its explanatory comment.

## Executed author-side verification

Linux/Python3.13.5; no user's local parent archives.
After remote-byte matching:
python -m unittest tests_tools.test_c324_scientific_recovery_r6 -v
48tests, failures0,errors0, elapsed0.935s.
Same48tests with text-file default opens explicitly emulated as CP932:
failures0,errors0,elapsed0.939s.

Real checks include Git object creation and cat-file batch parsing, filesystem
hashing, LF/CRLF parity, corrupted bytes/framing, JSON strictness, parsed-input
copy isolation, changed input/order/lifetime rejection, and native subprocess
nonzero exit propagation without retries. Suite inventory uses actual TestSuite
objects and unique IDs, not assertions on source-number literals.

The R6 scientific_worker control function was exercised with explicitly synthetic
scientific/lease/library adapters. It follows preflight ->full regression receipt
->fit call ->saved verification ->release parsed data ->final input reread, then
writes the required envelope. A failed regression receipt never reaches fitting.
A synthetic scientific FAIL remains FAIL while producing valid execution evidence.
This does not assert native Windows compatibility or actual neural training.

## Contract and dependency review

R5 real qualification is complete:244.561s,exit0,no timeout,all7 verifier bodies
executed once,9reuses,1486/1486final uncached input rereads. Scientific work0.
R6 explicitly promotes that mechanism into a registered scientific orchestration,
not a silent wrapper around an unprotected scientific result.

The primary C324 source/manifest/work/thresholds are unchanged. The existing
792source/1491input summary has a MANDATORY companion envelope containing the
802source/1501input complete union. The10supplements include every new runtime
helper, all3extra test modules, their3launchers and the R6 contract. The effective
union is checked before fitting and independently after result persistence.
Old R4/R5 code is fixed by exact blobs. No deciding-path module is claimed covered
merely because HEAD can reconstruct it; raw source bytes are protected as well.
Future C325 must inherit the envelope union, not just the old primary summary.

Actual parent writer/reader contracts reviewed: unchanged C324 load_parent returns
4dictionaries; precheck returns3items with data/old/new as its third tuple; run
returns a scientific summary and saves all8outputs plus summary; verify_artifacts
rereads checkpoints/evaluations and reconstructs saved JSON. R6 caches only the
canonical parsed parent tuple, not child predictions,weights or verifier outcomes
from an earlier process. Unmodified C324 saved semantic verification remains required.

Regression registration:primary5357+R4(37)+R5(48)+R6(48)=5490selected;
213modules,5491loaded before the existing single C204 exclusion. No new exclusions
or skips. Regression runs in its own interpreter without the science worker's
function substitutions. All tests must finish successfully before model fitting.

New source batch gives exact verified blob bytes for known read requests only;
live HEAD/branch/status guards remain real Git calls. Locked input identities are
checked throughout; final1501uncached reference rereads plus fresh-process raw
input/output/envelope checks are required. Primary result and envelope must agree.
Do not claim the fresh final process reconstructs parent semantics: it checks
persisted bytes/contracts; the real child semantic reconstruction ran in-worker.

## Remaining execution gates

No local PowerShell executable was available; no author-side PowerShell AST run is
claimed. The supplied command must parse active_v2; the dispatcher parses invoke_c324;
its recovery branch parses invoke_c324_scientific_r6 before invoking it.

Full5490tests and the actual R6 parent/preflight/fitting/replay/envelope run remain
user-side execution gates. Full-run duration and native-crash repair are unproven.
An INVALID attempt remains SAME C324; a finite scientific negative is not retrained.
A transport-only failure is repaired without rerunning the scientific work.
C325 remains NOT REGISTERED. Final activation changes only review/handoff documents.
