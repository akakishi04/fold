# C301 independent post-authoring review

post_authoring_review = PASS
Scope:separate committed-byte/static review and executed local behavioral fixtures,not authoritative FOLD science.
Review target:36156946c5035ba6f52e5973d0f5f9e2ded9898b.
Acceptance base:32bbfd3e74a0031ae8c327c7426d5a2900bd5c5e.

## Remote-byte match

All six OWN files were fetched from the immutable authoring commit after it was published.
Source/test were reread in consecutive ranges covering all440/463 lines;the other four files
were read in full. Returned whole-file Git blobs match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c301_learned_residual_gain.py:a1c2baa1762b57be32eff4b4b9828bd7e5da340f;29467 bytes.
- tests_lm/test_v05_c301_learned_residual_gain.py:b3309b46e3536e9617e3906ca9cd56c062946143;31763 bytes.
- tools/run_c301.ps1:bf5259e8b20ffa83f406f5ee2254b3b09d273d6e;4516 bytes.
- tools/invoke_c301.ps1:a87836602b39a1313e770e14c3c7e6062c57c7a2;6101 bytes.
- docs/experiment-ledger-addendum-c301-preregistration.md:70d309f8a0d867f798a46b4879fc8c56b2d4bbe0;8599 bytes.
- docs/v5b-learned-residual-gain-v0.1.md:164f63e9f0cbe4dcf723d8a567f39b74813fe5aa;1376 bytes.

The acceptance-to-authoring comparison contains exactly these six additions. No accepted source,
test,preregistration,log or dispatcher changed. Activation must preserve all six reviewed blobs.

## Checks actually run after all six matches

python -m unittest tests_lm.test_v05_c301_learned_residual_gain -v
Normal default:Ran40 tests in9.454s;OK.
Entire same40-test module with io.text_encoding default emulated as CP932:Ran40 in9.533s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. This is not the authoritative Windows runtime.
Earlier pre-commit tests are not substituted for these post-match runs.
All6 files are UTF-8/no-NUL;both Python files and all3 embedded runner Python blocks compile.
Symbol-table audit finds0 unresolved global references after accounting for imports,builtins and
standard module globals. Manifest recomputation matches:
c10f5dd5be005595a12502ff9ebe43802f987464ca1b85da2adb28a47f175dd9.

Actual C301 fit loops run800 updates in each arm on a controlled toy model;candidate rerun with
a different external RNG reproduces its trace and final state. Optimizer instrumentation verifies
one optimizer with step800. A separate actual train_one/replay fixture checks881/46176/3524 followed
by81/7776/324 counts and strict gain/state restoration. These are not actual FOLD capability tests.
Synthetic inputs encode targets for control tests and never enter the scientific dataset.

Gradient tests verify scalar finite differences,nonzero gradients through both summands and gain,
exact original/control/candidate initial outputs and common gradients,nonunit-gain numerical output,
exception cleanup,wrong-sum/dtype/nonfinite rejection and unchanged hook registries. Factory tests
check14256 versus14257 parameters and independent storage. All5 actual C301 schedules are built
on valid synthetic pairs and have100 exposures per logical row at each trained length.
The accepted C278 class body is executed via its AST with controlled backbone/reader modules to
verify its actual dynamic-hook and autograd protocol. The local support file holds that fetched
class slice,not the entire parent repository module,and is not committed. On Windows the test
extracts the class from the full accepted source. This does not validate the real FOLD backbone here.

Other fixtures cover27 hash failures before parent dispatch,652/1202 source/input accounting,
missing helper protection,first-gradient matching,loss/gain-history reconstruction,strict replay,
10-record scoring,60 partitions/30 contrasts,one failed candidate preserving the all-five negative,
production run ordering,actual bundle loader,serialization/no-overwrite,and byte plus semantic
tampering. Suite filtering is checked by exact synthetic test ID sets4638->4637,not source text.
Parent archives,Git,scorers and inherited suite members are substituted where unavailable.

## Parent and scientific-path review

C300 is a four-artifact frozen intervention diagnostic. It has no dataset copies or trained-model
bundle. C301 validates all27 summary hashes before the exact C300 verifier,which recursively
reconstructs its original before/after results and all parent artifacts. Only then read the
already-verified C299 data JSONs and recheck canonical hashes. No old trained weights initialize
C301. The actual run path invokes its own loader and its own wrapper-aware checkpoint replay.

Sole direct repository import:C300. Its inspected context yields C299 and the inherited evaluator,
normalizer,quad scorer,training tables and model/core bundle. C296 pairs_from_rows/render_batch
were reread at the authoring ref:they validate192 rows,96 intact pairs and the exact24x4 event
schema,with labels returned separately. Their source blob isae4fd7a45ec9306b1b81a82f8707269f1d88277b.
C297 context confirms the helper identity. C284 replay_error was reread:it validates every task,
split,profile and normal/evidence/query-blind view with float64 checks,drift<=1e-9 and exact argmax.
Only this numerical helper is reused in C301's own strict wrapper replay;the old cohort analyzer
and old counter are not used for the new14257-parameter wrapped candidate.

Every646 inherited source pin and1191 protected input remains checked. Add6 OWN and5 C300
summary/artifacts to obtain652/1202. Explicit C278 readout pin is retained;repository-local context
and the lazily selected C296 pair helper must be in the inherited map. No direct dependency waiver.

## Intervention fidelity and scope

The new wrapper keeps C278's original forward/assertions active. Temporary hooks capture r and a
without detaching their graphs and verify the actual normalizer input equals r+a before replacing
it with alpha*r+a. The late hook is registered after C278's own hook during local_encoder. Control
returns None and therefore preserves the original input. All hooks are removed on success/failure.
Candidate g=0 means alpha=2*sigmoid(0)=1 exactly. Real initial forward/common-gradient equality is a
mandatory operational preflight,not inferred solely from the formula or toy test. In science,
each pair's first CE and common pre-clip gradient hash are also required to match.

Only one global parameter is added. g and the original weights jointly optimize normal TRAIN CE;
no evaluation-conditioned gain choice,per-query routing,extra supervision or auxiliary loss.
A learned alpha is not a unique measure of component importance:other weights can also rescale.
The gain's gradient participates in global clipping,so later optimization is deliberately different.
Mathematical sigmoid bounds and possible float64 endpoint saturation are explicit. No clipping of
learned values or hidden inference fallback. All old gates,models and failures remain visible.
Fresh paired seeds and concurrent fixed control replace the previously recombined diagnostic cohort.

Science budget10*800=8000updates,384000training rows,9620forwards,539520total rows,38480core calls,
10strict state loads,one new10-state checkpoint bundle and one bundle read. Candidate adds1 scalar;
no equal-capacity or speed claim. Operational three-forward/backward preflight is separate.
Runner's3 embedded blocks compile;27 inputs;postcheck slice[2:29],head[29],argc30. Launcher has27
fixed ordered paths and returns before publication on Validate failure. Existing active_v2
was reread at blobe3923b6224959b442afefa02fafa967e2e6d462e and remains unmodified. Preserve external
ParseFile plus dispatcher-selected-launcher and runner parsing. Own40/modules186/loaded4638/
focused4637;only the inherited exact C204 exclusion remains.

Not executed here:Windows PowerShell ParseFile,real27 parent archives and Windows protected bytes,
actual4637 inherited tests,or10 real FOLD training/scoring/replay runs. These remain mandatory local
Validate/Execute gates. Review PASS authorizes the guarded launcher only,not C301 capability PASS.
Any integrity failure repairs SAME C301;valid all-five miss is ACCEPTED VALID NEGATIVE.
C302 stays unregistered until formal C301 judgment. Gate F NOT PASSED.
