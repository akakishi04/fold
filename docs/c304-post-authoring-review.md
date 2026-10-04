# C304 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review and executed local software tests,not authoritative Windows science.
Review target:a4064f0a341d1a3628de3fd667f3178a5be4f5a0.
Acceptance base:c8ccecbbfbb74cffb520ed4da507c9f7b8c0623b.

## Committed-byte match

All six OWN files were fetched from the immutable authoring commit after it was published.
Source499lines and test382lines were read in consecutive ranges;the four other files in full.
Returned whole-file Git blob identities match independently computed local Git hashes6/6:

- fold_lm/v05_benchmarks/model_c304_length_breadth.py:cacb5852a29171aa8079e634d929fdd54e7f4f58;35200bytes.
- tests_lm/test_v05_c304_length_breadth.py:8dc02ca8065b79ed64d621ba3b0e6d5b822085b2;28751bytes.
- tools/run_c304.ps1:156899faa484148b38db8b8b7a6184aa16fa4ccb;4507bytes.
- tools/invoke_c304.ps1:c81123ff74135009f187ad451bfb573050743184;6427bytes.
- docs/experiment-ledger-addendum-c304-preregistration.md:56dfc2c1d1f5be1d97738be7f11e8362a8a26613;9429bytes.
- docs/v5b-length-breadth-v0.1.md:93a21794159d1fc3e38254650ae221ba5f0a8f4f;1114bytes.

The acceptance-to-authoring comparison contains exactly these six additions. No accepted source,
test,log,preregistration or dispatcher changed. Activation must preserve these reviewed blobs.

## Verification actually executed after remote matching

python -m unittest tests_lm.test_v05_c304_length_breadth -v
Normal local default:Ran40 tests in17.649s;OK.
Entire same suite with io.text_encoding's default emulated as CP932:Ran40 in17.788s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. No authoritative Windows result is inferred.
Every OWN file is UTF-8/no-NUL. Both Python files and all3 embedded runner Python blocks compile.
Recursive symbol-table/import-binding audit:0 unresolved global names in new source/test.
Manifest recomputation matchesaf8f2ffc7b04e27bdd3597ede0d5b2cd55b6b6b526238dabf11a1b17f3edd9a0.
Post-match checks are distinct from the earlier development test run.

The new fit loop executes1200 actual AdamW updates per arm on small controlled models,with
synthetic target-encoding tokens. These models test scheduling/optimization/software contracts,
NOT generalization. A repeated candidate fit verifies deterministic losses and one optimizer
with step1200. The real child train_one and replay_one execute1308 and108 calls respectively
on a control model and check row/core counts and exact checkpoint replay. Production run/verify
fixtures dispatch15 fits before15 replays and exercise real child bundle serialization/loading,
no overwrite,hash tampering and semantic tampering even after descriptor replacement.

The integration tests are written to extract accepted backend/core/reader/scorer definitions
from the full source files on the user's checkout. This local runtime is NOT a full clone:
its parent support files are reconstructed excerpts from the fetched definitions,not byte-identical
copies of the accepted parent modules. They include the GRU/residual-MLP/core/readout numerical
path and the scorer grouping rules. Only OWN6 are asserted byte-identical to the committed files.
Local integration results therefore establish bounded software behavior with these support excerpts,
not successful execution of the complete inherited source graph or the actual Windows checkpoints.
No reconstructed parent support file is committed to the repository.

Within that scope,tests verify unchanged14256 parameter/state inventories,independent storage,
48/64 logits and parameter-gradient agreement with a nonzero reader,all5-length Japanese bytes,
full BOS/EOS preservation,query masks,all15 schedules and no length/profile aliasing. Scorer
integration preserves local cells and masks:a single wrong answer in an8-row cell fails,as does
a normal-perfect fixture whose evidence-blind outputs are also perfect. Synthetic analysis keeps
all120 partitions/80 comparisons;one candidate failure keeps the all-five gate negative.
Parent fixtures reject every one of30 hashes before dispatch and check670/1243 maps plus missing
helpers. Semantic suite-ID fixture checks4750 loaded minus the one inherited exclusion=4749.
Actual full inherited suite execution remains pending. CP932 emulation covers text decoding only.

## Source-level scientific and dependency audit

C303's accepted writer stores the canonical dataset.json among8 artifacts. Its exact summary hash
and exact verifier cover all output descriptors,previous parents,gradient/state accounting and
original results. C304 verifies30 ordered summary hashes BEFORE dispatch with29 ancestors and
the accepted scientific HEAD;requires C303's valid-negative three-arm counts and matching/replay.
It uses only verified logical TRAIN data to initialize a new training task,not C303 weights.

The accepted C231 factory was traced to ShortByteLanguageModel in fold_lm/v05/language_task.py,
and its fixed-routing core in fold_lm/v05/modules.py. Neither allocates slot-indexed parameters.
Copying max_tokens and core.slots to64 therefore changes the frame,not learned parameter count.
The old C278 class hardcodes48 in its input/span contracts,so C304 owns an explicit generalized
readout instead of modifying accepted files or changing their globals. Its numerical mean/final
attention,pre-core memory,post-core residual and normalization provenance checks were compared
against the actual fetched C278 implementation. All real runtime models use the accepted backbone,
not the local reconstructed excerpts. Preflight must verify actual old48/new64 behavior again.

A52-byte Japanese five-character prompt requires54 tokens with BOS/EOS. All three arms use64,
all languages remain,and overflow fails rather than truncating. Old2/3/4 strings must exactly
match their actual parent renderers. The new5 prompts use the same byte alphabet and value split.
The compatibility probe uses TRAIN rows0 and4(the English and Japanese counterparts),all3 older
lengths/all profiles/views. Its artificial labels and nonzero-reader perturbation are explicitly
software probes on discarded copies,not extra training or capability observations.

The C270 scorer was inspected:its score depends on logical facts,queries,orders and view logits,
not identifier length. C304 maps profile names into that unchanged scorer and keeps length outside
the canonical score object. C287 normalize_task/partition were reread and accept this exact
triple-shaped grid with child seed/arm metadata. They do not infer length from prompt tokens.
C267 counted and C260 core_counter were reread;they count calls/rows without a48-slot assertion.
Every such helper remains in the inherited664-source map. PINNED additionally asserts exact
backend/core/C278/C269/C270/C267 blobs. The actual factory language_module and context/pair helpers
must be pinned. Source670/protected1243 equals inherited664/1228 plus OWN6 and9 parent inputs.
No dependency waiver or accepted-file mutation is authorized.

## Design,counts and limitations

Three arms share max trained length4,total1200updates,logical pair order,400updates per profile,
initial weights within each fresh seed,and ordinary full CE. Candidate100 presentations per row
at each2/3/4;controls300 at4 or150 each3/4. Temporal spacing and per-length allocation differ;
this is not an isolated causal estimate of the number of lengths. No newly selected frozen-core
policy is mixed in. The profile cycle avoids binding each of3 lengths to one of3 profiles.
No5/HOLDOUT/masked examples enter the optimizer. All models then evaluate2/3/4/5 and all old views.

15*1200=18000 updates;864000training rows.15*(1200+108+108)=21240forwards;
1175040total rows;84960core calls;15state loads,one model-bundle write/read,network0.
All arms have64 slots. These counts do not imply equal token-level compute to old48-slot runs.
The prior claim that5/5 would establish a length-independent rule was too strong;bounded structured
identifier transfer is the only tested scope. Core_frozen4/5 from C303 is not adopted here.
Primary remains all5 candidate models pass ALL five-character local and masked criteria.
Old-length results and prior judgments are not retroactively promoted. Gate F remains NOT PASSED.

Runner3 Python blocks compile.30 fixed paths;postcheck sys.argv[2:32],HEAD[32],argc33.
Validate precedes science;any failure returns before log publication. Preserve unchanged active_v2
and its dispatcher/selected-launcher/runner ParseFile chain. Own40/modules189/loaded4750/focused4749;
sole inherited exact C204 exclusion retained. No extra count-based source-string assertion.

Not executed here:Windows PowerShell parsing,the actual30 local parent archives and protected
Windows bytes,the full4749 inherited suite,or15 actual C304 scientific training/evaluation runs.
These remain mandatory Validate/Execute gates. Any integrity issue repairs SAME C304 without
changing scientific conditions. C305 waits for formal judgment;no best-seed or threshold selection.
