# C331 post-authoring review

Date:2026-10-18 Japan time.
post_authoring_review = PASS
Committed source/preregistration review target:
5dbdd46959695f2ca48adbeea8084db5ba6a8dab.
Acceptance base:b195a3962dd868ffa430500ca3bf6ae87dc44b1d.
This approves authoring,not native Windows/full5898 regression or the scientific
frozen-model outcome. Use the subsequent documentation-only activation HEAD.

## Committed-byte reread

All six committed files were fetched again at the exact target and read through EOF.
Benchmark ranges1..110,111..220,221..324;executor1..115,116..225,226..335,336..445;
tests1..110,111..215,216..320,321..400,401..451;both full PowerShell files;
contract1..90,91..164. Returned blob identities match independently hashed local
raw bytes used in the post-reread tests below:

|File|Git blob|
|---|---|
|fold_lm/v05_benchmarks/model_c331_frozen_first_mean_query.py|15fc732df683e421648545acfa3ea5e7a8f3ddfd|
|tools/c331_execution.py|fcc35a8efc01f5bc385e66b1aa95b245a85c5ce2|
|tests_lm/test_v05_c331_frozen_first_mean_query.py|e5b695a26caf5a7169e85b24e714063ee8319139|
|tools/run_c331.ps1|0abacb5399b3a60a84d93255034ab4974128376a|
|tools/invoke_c331.ps1|287943b7af02caaedb57731588933457ff0ed143|
|docs/experiment-ledger-addendum-c331-preregistration.md|6e66ff39780b0c5a1b9aff6f88d08f5bb7a56e3f|

Remote compare against the acceptance commit confirms exactly these six additions.
No accepted C330/R1.2 or earlier source,test,contract,log,runner or dispatcher changed.
C330 acceptance,source registration and this documentation-only review are separate.

## Actual post-reread checks and limits

Normal own unittest run:48/48 PASS,0failures/errors/skips,1.868seconds.
CP932-default-text-open emulation:48/48 PASS,0failures/errors/skips,1.537seconds.
Harness elapsed times including loading were1.870/1.539seconds respectively.
Both builtins.open and io.open supply CP932 only when text encoding is unspecified;
explicit UTF8/binary opens are preserved. This is not native Windows locale testing.
All6files decode as UTF8 with no NUL;all3Python files compile/import. Recursive
LOAD_GLOBAL audits of197function/method/nested code objects found0undefined names.
The manifest self-hash matches:
8644f03a61e1dbdbb44a31514a392fd18cdb7ce71c190ee1a1fd2a8c759c30f8.

Environment:LinuxPython3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5,2Torch threads.
The local test tree contains the targeted authored files,not a full repository
checkout. Legacy scorers,source checkpoints,historical5850inventory and native lease
callbacks in integration fixtures are explicitly synthetic collaborators. No actual
C329 checkpoint inference,Windows/full5898 execution,PowerShell AST run or rerun of
the original C311 native failure was performed by this author check. Native user
preflight/full regression/real evidence checks remain mandatory.

Mutation control:replace the first_mean intervention by a no-op native mean in an
in-memory module only. Both test06(exact formula) and test07(changed multi-byte
behavior) fail their assertions. These2expected mutant failures are not failures
of the reviewed source. The six source-file hashes remained unchanged afterward.

## Readout implementation and scientific-variable audit

The actual C304 LengthReadout.forward and span_mask,plus C319 trained_readout,were
read. The native path derives a mean query and a last-byte query from pre-core local
states,performs two attentions and combines them through its unchanged memory and
post-core residual path. C331 hooks validate the native inputs before substituting
only .5*(mean+first_byte_local) at the first query projection call. The second last
query,weights,core,mask,attention operations and output averaging stay native.
No accepted module/global/function is patched. Only child-owned removable hooks
participate. The mean arithmetic and local valid mask preserve the native ordering.
Hooks clear temporary state and restore inventories on normal or exceptional exit.

Tests exercise the real production hook with a small explicit Torch model:exact
native-control parity,exact first/mean formula,last branch retention,multi-byte
change,single-byte invariance,padding exclusion,query provenance and cleanup. A
finite-difference check and actual autograd validate that the representation is not
silently detached;these are SOFTWARE gradient tests,not scientific training.
Endpoint identity is a byte offset,not a decoded Unicode-character boundary.
English length1 and query-blind one-byte spans are invariant controls;Japanese
length1 is not mislabeled one byte. C317's previously inspected intervention changed
the last branch to first;C331 changes the mean branch and retains last.

All ten C329 checkpoint identities are fixed,including both1200/2400 states and the
less successful seeds. No source weights are trained,selected or rewritten. Native
before/after and all query-blind controls require<=1e-9 logit drift and exact argmax.
The source data/prompt JSON fingerprint is checked across the cohort in memory in
addition to locked file-byte checks. Every mode checks the actual state hash.
The small discarded native preflight executes12forwards/12rows/0updates separately,
including the candidate on multi-byte input,with nonzero output weights to avoid a
vacuous zero-readout comparison. It never supplies a cohort state.

## Saved writer, scorers and accounting

The C329 five-trajectory/ten-state writer and safe bundle loader are reused unchanged.
C331 stores all3modes per checkpoint under fold-c331-query-probe-v1,not only favorable
predictions. Native_before reconstructs accepted C329 logits;native_after reconstructs
native_before. The child analyzes all modes and uses unchanged C324 original/interior
evaluators,replay checks and paired contrasts. Original profile names map explicitly
to the inherited interior scorer slots;no domain is silently dropped.

C330.adapted_score is reused to count failed local/order conditions. Native per-state
gates must reproduce accepted C330 seed flags. Existing local/masked/order thresholds
.90/.80/.35/.35/.80 are fixed. Counts are reported per original length and interior,
including rescued/regressed answers and pairs. Improvement,tie and harm all remain
valid diagnostic outcomes. PASS is integrity,not a favorable capability result.

Production run_probe orchestration executes with synthetic source-model collaborators
and real file/Torch archive writes in tests,checking all30mode calls in order and all
4outputs. Production analyze/summarize/compare execute across a full10-record/3-mode
synthetic raw tree,with explicitly synthetic legacy scorers/localizer:30raw-validation
calls and60contrast calls are checked;changed checkpoint binding is rejected. Saved
reconstruction and tampered JSON checks use actual child loader/writer paths.
These are not native FOLD output measurements or a claim that all legacy numerical
scorers were rerun in the author environment.

Cohort work:10model instances/10state loads/1bundle load,30evaluations*171forwards=
5130forwards,492480rows,20520core forwards,10260query projection calls. Scientific
train/gradient/optimizer steps and new checkpoints0. The saved raw-logit payload is
1008599040bytes,not peak memory or total serialization. Preflight,tests,parent and
saved verification are separately scoped. No efficiency gain is claimed.

## Parent evidence and full dependency inheritance

Immediate parent is accepted C330 R1.2,not original pre-recovery C330. Exact primary
and companion envelope hashes,diagnostic flags,whole recovery contract,full5850
receipt and1596final uncached rereads are checked. Both maps must agree on841sources
and1596inputs. C329's preserved negative verdict remains bound.

All443parent supplementary outputs are mandatory:three regression records plus220
module JSON/log pairs. Their hashes are checked and the actual accepted R1.2 helpers
reconstruct the parent's full5850-ID plan,per-test completion and PID/log evidence.
These443files plus4diagnostic outputs+primary+envelope make449parent output files.
Protection is847sources=841+6 and2051inputs=1596+449+6. No fallback to smaller maps,
omission of accepted recovery tests or unpinned lazy helper is permitted.
An actual443-temporary-file fixture detects changed module evidence bytes;the content
of that fixture is synthetic,not the user's accepted evidence.

The immediate C330 JSON semantic loader is called with its actual signature using
protected C329 source measurements. Canonical prompt/data validators are run,without
older recursive semantic-body reruns or parent model inference. All older bytes stay
protected. The accepted recovery loader is source-pinned before import;its helper
chain supplies the native runtime and unchanged R4 locks. The source C329 model and
all direct/lazy deciding dependencies retain inherited source/input protection.

## Regression bridge, process identity and failure boundaries

The new plan preserves the exact5850base ID sequence and appends the real48-test
loader,for5898tests/221modules. The sole inherited exact C204 mutable-ACTIVE exclusion
remains;no new exclusions/skips/cached successes. Accepted R1.2 allowed_module,
execute_module,check_module and validate_module_evidence are reused unchanged.
The new orchestration owns C331-specific guards/plan/counts rather than invoking the
C330-hardcoded guard or module CLI. Direct/immediate-child PID semantics therefore
remain accepted behavior,not a new equal-PID assumption.

The generic module receipt ABI remains fold-c330-r1-module-v2,but each receipt is
bound to the NEW C331 HEAD,plan,index,module. Overall C331 plan/evidence schemas are
new. Collector and fresh verifier delegate to the same accepted module validator.
Own tests cover this bridge with explicit collaborator doubles and221synthetic
receipts,checking442validator calls,changed log bytes,missing tests and failure
stops. This does not claim a real5898-module-process run in the author environment.
The actual accepted R1.2 process tests remain part of the user's inherited5850suite.

Actual scientific_worker control-flow fixtures verify parent->preflight->regression
->probe->saved reconstruction->final rereads->lease release. Failed regression never
reaches the probe. Real temporary Git,strict JSON,LF/CRLF/exclusive writes and a real
nonzero subprocess preserve failure evidence. No retry or silent selection exists.
Native R4 leases span the worker;all2051inputs receive final uncached rereads. All4
outputs are byte/size-bound around reconstruction and before result/envelope writing.
Fresh verification checks complete parent/input/source/output maps,all new module
receipts/logs,manifest,counts and saved child semantics without another model run.

## Launcher and approval

Selected invoke_c331 and run_c331 names,CLI arguments,local output prefix and c331
publication agree. Both scripts were fully read;user entry parses active_v2,the
unchanged dispatcher parses the selected launcher,and the launcher parses itself
and runner before scientific logging. Native PowerShell AST execution is not claimed
on the author Linux host. Wrong/stale/dirty/ambiguous invocations stop before science.

The final review/ACTIVE commit changes documentation only. Native preflight,all5898
tests,real frozen-model controls,2051final rereads and fresh verification must pass
in the registered user run. INVALID stays SAME C331;valid diagnostic outcomes are
accepted irrespective of benefit/harm. No C332,Gate F,production adoption,paidservice,
CI,reinstall,artifact deletion or old-science mutation is authorized.
