# C315 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review plus executed local software tests,NOT actual FOLD science.
Review target:1d15baedb214a9af0109056e8dd2dd7f302c788b.
Acceptance base:c9443536d956944c3f04d9825d01742a7851bbee.

## Committed bytes

After the authoring commit,all six OWN files were fetched from the immutable target and reread.
Python source456lines and tests481lines were read in consecutive complete ranges;the other
four files were read in full. Returned Git blob IDs match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c315_single_character_mix.py:8bf47583b3c8dd3e4e35a8612912d170a2a8b77c;31852bytes.
- tests_lm/test_v05_c315_single_character_mix.py:aacc6c4972bedc0193b03aedab48bb14aa5d136b;32418bytes.
- tools/run_c315.ps1:df97dd89595d13bab015340f606179c1a4beb034;4621bytes.
- tools/invoke_c315.ps1:1dcd4c66a0cbf30ea0690dcb00014b782522bdc1;7497bytes.
- docs/experiment-ledger-addendum-c315-preregistration.md:7c54e928166f5fb5260b4e4410fbfadf5d8c1288;7630bytes.
- docs/v5b-single-character-mix-v0.1.md:cec6bf17e4b5a90f4cb10f75993d5e2ae8f9f222;1177bytes.

The remote acceptance-to-authoring comparison contains exactly these six additions. No accepted
source,test,preregistration,log or dispatcher changed. Activation must retain all six reviewed blobs.

## Executed checks after all six matches

Normal:python -u -m unittest tests_lm.test_v05_c315_single_character_mix -v
Ran32 tests in16.153s;OK,zero failures/errors.

Complete same module imported and executed under io.text_encoding default-CP932 emulation:
Ran32 tests in16.735s;OK,zero failures/errors. Patch covers module import,setup,all tests and teardown;
only omitted encoding is mapped to cp932. Both are uninterrupted full unittest runs. Pre-commit
runs are not substituted for these post-fetch executions. TERM-not-set cleanup output after OK
was not a test failure;both processes returned success.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. No PowerShell installed locally.
CP932 default emulation is not full Windows/console emulation.

All six files decode as UTF8 and have no NUL. Both Python files and three embedded runner Python
blocks compile. Recursive symtable/import-binding check finds zero unresolved global references,
allowing module bindings,builtins and standard module globals. Manifest self-hash matches:
eb47e7656de2e83666bb780ea6bbbed34e9c56cfd00d4611ad8cca75b5e50c6d.
Launcher paths are41 ordered C314..C274. Postcheck paths=sys.argv[2:43],head[43],argc44. C315-only
ACTIVE guard and Validate-before-Execute/publication path are preserved. Dispatcher/selected
launcher/runner ParseFile chain remains mandatory;PowerShell parsing itself was not run here.

## Behavioral coverage

An independently constructed logical dataset and rendered old2..5/six inputs reproduce their
accepted SHA256 values. The single-character renderer equals all three degenerate legacy name
families but stores/evaluates only one canonical repeat profile. All normal strings across1..6
are4608 distinct;longest input remains63 encoded tokens in64slots. Actual accepted C304 prefix/
span function ASTs confirm one-character English/Japanese query spans and masking semantics.
No duplicate length1 profile is silently used to multiply observations,training or capability scores.

Every new seed's schedules cover the same96 intact query pairs once per epoch. Control exposes
each row100 times per length2/3/4;candidate75 times per1/2/3/4. Candidate longer profiles receive
25 exposures per row each and canonical length1 gets75 total. Independent schedule examples and
actual accepted C312 pair_inventory/plan_for_order function ASTs verify control compatibility.
Private generators do not perturb global RNG. Bad target bindings and malformed pair partitions
are rejected by the inherited pair contract. No held-out value pair or length5/6 enters training.

The actual child fit function executes1200 updates on a controlled small model with the same
parameter-count partition. A separately written optimization loop reproduces every loss and
final weight. Production train_one/evaluate/replay execute on this model and verify1344 initial
train/evaluation calls plus144 replay calls,strict checkpoint identity and error detection.
Evaluation has16 unique profile blocks and144 forward calls,not a tripled single-character block.
Synthetic training inputs encode labels directly and padded parameters match capacity for software
checks;these are NOT real FOLD learning/generalization results. Accepted optimizer function ASTs
are exercised with controlled models to confirm core.0005/other.005 and reject altered rates.

Other tests reject changed schedules,loss/LR histories,raw domains,cohorts,initial pairing,wrong
checkpoint state and capability relabeling. All41 parent-hash positions fail before parent verifier
dispatch. Tests check real child data-path indices,736/1379 temporary protection files and missing
helper rejection. Actual runtime_preflight function is exercised using controlled models.
Production run dispatch performs ten train calls before ten replays,loads the child bundle and
reconstructs persisted results;existing run directories are not overwritten. Byte tampering and
semantic tampering after updating a descriptor both fail. Semantic suite-ID tests build5086
synthetic TestCases,retain exactly5085 and reject duplicates;this is not the actual inherited suite.

Local parent support consists of fetched exact function slices for C312 batching,C304 prefix/span
and C308 optimizer,not full parent modules or a repository clone. These support files are NOT
committed. Tests09/29/30 extract the same functions from the user's full accepted source.
Other parent/Git/scorer/backend inputs are substituted when unavailable. No test establishes that
real FOLD will pass six or that all real41 parent archives are present.

## Scientific path and interpretation audit

C314 is a diagnostic JSON writer,not a checkpoint or training-data writer. C315 verifies41 ordered
summary hashes before C314.verify_artifacts with40 ancestors and the accepted scientific HEAD.
It reads C312 dataset/old prompts at paths[2] and C313 six prompts at paths[1] only after recursive
verification. Three canonical hashes,source IDs,targets and every old2..6 prompt are preserved.
C314's error report is not used as a teacher or to filter rows/models. All fresh seed pairs stay.

Sole direct import C314;its C313/C312 contexts provide actual C308 policy,C304 LengthReadout/prefix/
span/scorer,C296 pair helper,C287 normalization and C310 no-neural guard. Explicit pins and inherited
C304.PINNED plus repository-local context/factory-module coverage remain mandatory. All730 inherited
source pins and1369 inputs stay checked;OWN6 plus4 C314 files gives736/1379. No parent mutation,
new exclusion or missing-dependency waiver. Full models are built anew and all parameters train.

First actual minibatches differ;requiring their losses equal would be incorrect. Discarded common
English/Japanese one/two-character inputs instead require identical initial outputs,preclip
gradients and one optimizer update. The actual LengthReadout/span source supports those query
spans;real FOLD bilingual smoke remains a mandatory user-side preflight.

Primary is all five new one_to_four models passing six local/masked criteria. Length1 is described
by normal/masked counts and NLL only;it does not receive a newly invented full gate or feed the
six decision. Original scorer is reused for2..6;new cohort analysis handles the singleton profile
without sending it to an incompatible three-profile validator. All six lengths are archived and
strictly replayed,including full256-class argmax. No answer correction or selective decoder.

Adding1 at fixed1200updates trades away25 exposures at each long trained length. Length/profile
timing and profile frequency also change. This tests an explicit budget-allocation policy,not
isolated breadth,causal proof of rule abstraction,or a guaranteed fix for long-name confusion.
No length5 learning,optimizer retuning,capacity increase or Gate F promotion is authorized.

Science totals:10models,12000updates,576000training rows,14880forwards,852480row presentations,
59520core calls,10strict state loads,one checkpoint bundle write/read,network0. Operational probes,
parent reconstruction and software tests are separate. Seven artifacts plus summary;child schemas
fold-c315-single-mix-models-v1/fold-c315-single-mix-eval-v1 keep all losses,LR/gradient/schedule traces
and final logits. No parent cohort analyzer or older raw schema is silently substituted.

## Mandatory runtime boundary

Not executed here:Windows PowerShell ParseFile,the actual41 parent archives/protected Windows
bytes,the real5085 inherited regressions,or ten real FOLD training/evaluation/replay runs. Those
remain mandatory local Validate/Execute gates. This review authorizes only the guarded launcher.
Any integrity failure repairs SAME C315;valid primary failure is ACCEPTED VALID NEGATIVE. C316
stays unregistered until C315 formal judgment. All previous verdicts and Gate F remain unchanged.
