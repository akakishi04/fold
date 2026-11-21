# C338 post-authoring review

Date:2026-10-25 Japan time.
post_authoring_review = PASS
Committed source/preregistration target:031a67c9e276086f3f76cda611f88f75cafff0d8.
Acceptance base:8b7cdc54a7a735320617e1650cd349efb5850288.
This approves authoring, not native Windows execution, full6170historical success,
scientific improvement, Gate F or production adoption. Use the subsequent
DOCUMENTATION-ONLY activation HEAD in the user command, not this source-only target.

## Exact remote reread and change scope

All six files were fetched again at the exact source commit and read through EOF.
Benchmark ranges1..110,111..210,211..310,311..410(actual394lines);
executor1..110,111..210,211..310,311..430(actual413lines);
tests1..110,111..220,221..330,331..440,441..540,541..650(actual615lines);
full21-line runner and58-line launcher;contract1..105,106..220(actual196lines).
The returned Git blobs match independently hashed local raw bytes used below:

|File|Git blob|
|---|---|
|fold_lm/v05_benchmarks/model_c338_value_support_training.py|53185474d560e2961ff05b5484da84c8f27c956f|
|tools/c338_execution.py|3cc1dd228baab13a1feef96d38b8213ff53d7080|
|tests_lm/test_v05_c338_value_support_training.py|2a551a691d046c9d1717c0b7886a27ba455134d3|
|tools/run_c338.ps1|b6047449844f0d9e0d0cd57e3ce17b08d0f7d722|
|tools/invoke_c338.ps1|c63845cb038f2bfbf316bb0c435c4aad1d5698bc|
|docs/experiment-ledger-addendum-c338-preregistration.md|a7d4129cf94cd2808933cef0933a6ae7c0037e19|

Remote compare confirms exactly six additions from the acceptance commit. No
accepted C337/C336/C335 or older source,test,contract,log,dispatcher or lock code
changed. No correction to the published six files was needed during this review.

## Checks actually run AFTER the complete remote reread

Normal own suite:48/48PASS,0failures/errors/skips,17.375seconds.
CP932-default-text-open emulation:48/48PASS,0failures/errors/skips,17.512seconds.
The emulation patches builtins.open/io.open only for text opens lacking encoding;
explicit encodings and binary mode stay unchanged. Not native Windows locale testing.
All6files UTF8/noNUL;all3Python files compile/import. Recursive LOAD_GLOBAL audit
covered269function/method/nested code objects;undefined global bindings0.
Actual48method ordered-ID SHA256:
9b644436261b62ce1daf2915018911b32e694ac956b7adfaa4391bcd1f4774a4.
Manifest self-hash:
d2c6bcbadfa3f04c35cad137fece59c9499f8b5de37589425479b05376b9fe73.

Two in-memory negative controls were run after normal/encoding checks:
- Remove the extra term from the candidate total: test05scalar formula,
  test06decomposition,test17independent updates each fail(3assertion failures,0errors).
- Replace the pair logsumexp by only the queried target logit: test05scalar formula,
  test13query invariance,test14both-value gradients each fail(3assertion failures,0errors).
These expected mutant failures are not failures of the reviewed source. Both
functions were restored, and all six source SHA256 values remained unchanged.

Environment:LinuxPython3.13.5,PyTorch2.10.0+cpu,NumPy2.3.5;test class uses2Torchthreads.
The local tree is a TARGETED review tree, not a complete repository checkout.
Local-only verbatim C267dataset writer/constants,C336profiles helper and C337audit_logits
extracts were used; they are not committed and do not replace native accepted files.
Historical scorers,models/schedules,summary validation,module inventories/proofs and
OS read leases in integration fixtures are explicitly synthetic collaborators.
No native FOLD training,actual C335logit diagnosis,Windows locks,full6170historical
suite,or native PowerShell AST execution is claimed. pwsh was not available.
The existing mandatory user-side dispatcher/launcher/runner AST chain remains.

## Single scientific variable and mathematics

Both arms use native mean/last during fitting,evaluation and replay. No inference
candidate filtering,first_mean/alternating readout,new parameters,input channel or
accepted-function patch. The existing native wrapper checks query-input provenance.
Only the objective differs:ordinary mean256classCE versus CE+SupportNLL,where
SupportNLL=mean(logsumexp(all256)-logsumexp(the two TRAIN supplied values)).
Alpha is fixed0/1;alpha0 returns exact ordinaryCE tensor/gradient. Computing control
support telemetry does not include it in the control gradient. Logits are never
mutated or truncated, and both supplied labels stay out of model.forward.

The decomposition CE=SupportNLL+within-pairCE is explicitly tested and documented.
The candidate therefore doubles support weighting, not an independent information
source. Increased objective scale may affect clipping/updates; unchanged update/
forward counts are not an equal-FLOP/effective-learning-rate claim. The support term
alone does not select the queried value. No gain from a label-assisted inference
filter is counted. New gate metrics always use the raw256class argmax.

Tests check scalar arithmetic,exact alpha0 CE/gradient equality,float64 finite
differences,analytic softmax-difference gradients,query/order invariance,support on
both values,input immutability,shape/type/bool/invalid coefficients and nonfinite/
overflow rejection. The canonical fixture is compared to the actual imported C267
writer and frozen digest. Full0..3schema and all12ordered value pairs are retained;
training has its fixed8pairs,not a binary-only substitute.

## Real update tests and clearly separated toy scope

Production optimize is exercised with a small explicit Torch model and real AdamW,
gradient clipping,backward,query hooks,model/core counters and serialization.
Short traces compare both objectives against an independent reference loop.
Test18 runs actual production train_one/optimize for2400updates PERarm,then runs an
independent2400-update reference for each arm. Loss histories and final tensor
fingerprints match exactly;candidate/control final fingerprints differ. The real
train wrapper confirms2400forwards/115200rows/9600core calls;native query receipt
confirms4800projection calls. Post1200/pre1201weight+optimizer state agrees.
These are software-model runs, NOT the native14256parameter FOLD experiment.
The native discarded preflight also executes against the toy model in tests.

The source-level native factory,prepared-data path and schedule were compared with
accepted C332/C335/C329/C324 helpers. Pair construction happens before either fit;
initial equality/storage independence are checked. No old checkpoint is loaded for
training. The frozen cohort and matched schedules are not modified after results.
All fitting completes before eval/replay;production orchestration verifies10training
calls followed by20native evaluations with real file/archive writes in a fixture.
The live native preflight still must verify all5actual schedules,6native forwards,
12rows,4backwards and0updates in the user environment before scientific fitting.

## Parent writer/loader and complete protection audit

Immediate parent is C337diagnosticPASS,not C335training. Both exact summary/envelope
hashes,883/4827maps,6122full receipt,completion flags and preserved C335negative are
required. The pinned C337executor/benchmark are checked before helper imports.
Its dictionary helper contract is preserved. C337.snapshot reconstructs inherited
maps without modifying them;all463new parent outputs are then added,including ALL
457regression proofs(3records+227JSON/logpairs). The new sixfiles yield889sources/
5296inputs. Tests build a real5296-file temporary union with explicit synthetic
ancestor callbacks,and separately validate457parent proof-file hashes/tampering.

C337summary does NOT embed the full C336summary. The child loads the protected
C336science/summary.json,checks the accepted hash from C337.PARENT_SUMMARY,then calls
C337.semantic_recheck(C337science,C336science,C335science,C329data,C336validation,read).
Test39 fixes this exact six-argument dispatch and missing-source rejection. No
four-argument/older-loader guess and no recursive older semantic-body replay.
Canonical data/prompts are checked under no_neural using accepted validators.
C332/C329/C324 training/readout/scorer helpers and C337audit_logits/C336profiles are
already inherited direct/lazy dependencies and remain pinned/protected.

Native R4 read leases cover parent validation,preflight,regression,fitting and saved
reconstruction. max_files=INPUT_COUNT=5296 is explicit and finite;no4096default,
eviction or unlocked fallback. Test44 requires the exact argument and verifies
worker/fresh-verifier validity for a scientific negative outcome. All5296inputs
must receive final uncached rereads. No earlier evidence is made optional.

## Regression, scientific scoring and persisted result

The new actual48-test loader appends to unchanged6122ordered parent IDs,for6170tests/
228modules. Sole inherited exact C204mutable-ACTIVE exclusion remains;no newskip.
C338owns its guard/plan/moduleCLI and reuses accepted C330R1.2execution/evidence ABI,
including direct/immediate-child PID relationships and canonicalbegin/endmarkers.
Synthetic228module tests call the same collector/verifier bridge456times and reject
tampered logs;actual historical process tests remain in the native full regression.
These synthetic inventories are not claimed as6170real historical tests run here.

Actual child analysis uses10synthetic state records/all evaluation+replay trees,
real C337support arithmetic and independent paired-count fixtures;legacy scorers and
trace validation are explicitly substituted there. State/pairing/replay mutation
is rejected. Separate actual trace tests cover schedule/support/hash/boundary/rate/
loss arithmetic and no intermediate selection. Saved reconstruction and primary/
envelope verification check their real child control paths with synthetic ancestors.
A failed regression blocks fitting;valid negative science persists as statusFAIL
with scientific_execution_valid=true. No automatic retry or coercion toPASS.

Gate requires all5candidate full oldgates,perseed/perdomain nondegradation of answer/
pair counts and outside errors,and strict total answer/pair gains plus fewer outside
errors. A local short-domain loss cannot be hidden by pooled totals. Tied/saturated
controls can validly fail strict gain. These are prospective C338criteria,not changes
to accepted C335verdicts or numeric task thresholds.

Cohort work:24000updates,1152000TRAINrows,27420forwards,1480320totalrows,109680corecalls,
54840queryprojections,20saved-state loads,1bundle read/write,10finalstates. All6science
outputs are byte/size-bound around reconstruction and before summary/envelope.
Fresh verifier reconstructs saved metrics and proof maps,not all historical optimizer
steps or another model cohort. Full actual native execution remains outstanding.

## Launcher and approval boundary

BothPowerShellfiles were reread in full. Selected paths,ExpectedHead/Folder arguments,
outputprefix,c338publisher and CLI modes agree. Standard userblock parses active_v2;
unchanged dispatcher parses invoke_c338;launcher parses itself and run_c338 before
logging. Wrong/stale/dirty/missingdependency/ambiguousACTIVE invocations skip before
science. NativePowerShellAST execution was not possible on this authorhost.

The activation commit changes review/handoff documentation only. Only after native
preflight,all6170tests,full fixed-budget training,saved replay,reconstruction,5296final
rereads and fresh verification can C338 receive a scientific verdict. No paidservice,
CI,reinstall,artifact deletion,C339,GateFpass or production adoption is authorized.
