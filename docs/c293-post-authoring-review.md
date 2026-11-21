# C293 independent post-authoring review

post_authoring_review = PASS
Scope:committed-byte/static review plus local behavioral fixtures,not authoritative FOLD science.
Review target:40b12de5ba46e9d5f3b89efaed006d293f764daa.
Acceptance base:b6e90c80768c48a999f253cfa5b3cced29b465aa.

## Committed-byte verification

All six OWN files were fetched from the immutable authoring commit after creation. Source and test
were reread in consecutive ranges covering the complete files;the remaining four were read in full.
Returned whole-file Git blob identities match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c293_fact_support_loss.py:9514bb3db5abfac91666ee67b1e1973511a2b682;28009 bytes.
- tests_lm/test_v05_c293_fact_support_loss.py:c6165987840f5c0a8c892169ee6637fc397547b3;27188 bytes.
- tools/run_c293.ps1:3e414cdfeda874992ccaf80f6ba78dd3efd9274a;4661 bytes.
- tools/invoke_c293.ps1:1d990afaade2a1fee7e7cdbac18b8a5b9dc4af50;5330 bytes.
- docs/experiment-ledger-addendum-c293-preregistration.md:9e2dfbfb2be82619fbf1707ff243dd1eb48d69e7;7921 bytes.
- docs/v5b-fact-support-loss-v0.1.md:0080e8c3cb9f9ee8878741593a460612712cfb75;1544 bytes.

Remote comparison acceptance-to-authoring shows exactly these six additions. No accepted source,
test,preregistration,log or dispatcher is changed. Activation must preserve the six reviewed blobs.

## Tests actually executed after remote-byte matching

python -m unittest tests_lm.test_v05_c293_fact_support_loss -v
Normal local default:Ran40 tests in6.819s;OK.
Entire same suite with io.text_encoding's default emulated as CP932:Ran40 in6.799s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. Not Windows and not the actual4357-test regression.
All six files decode as UTF-8 with no NUL. Both Python files and three runner-embedded Python
blocks compile. Symbol-table import/global audit found zero unresolved globals. Manifest
recomputation matches0aadd3137b216f6e0fbc37feffe8b0ad947e48eeb22da881f38e58ee38a424f7.

The fixtures run the real C293 fit loop for800 AdamW updates per arm on a small four-symbol
classification model,then repeat the candidate to test deterministic execution. This toy fixture
encodes its synthetic target identity in its input;it verifies numerical/control flow,not FOLD
binding or generalization. Another train_one fixture executes800 training+81 frozen evaluation
calls and checks881 forwards/46176 rows/3524 core-call accounting with a counting stand-in.

Loss tests verify uniform-logit closed forms,exact CE and1.25*CE values/gradients,the support/choice
identity and candidate-gradient equivalence,finite differences,offset and class/pair permutations,
and cases where support mass is high but the wrong fact wins. Unsupported-winner gradients are
checked. NaN/Inf,invalid labels,non-distinct support and malformed batches are rejected.
Actual five-seed schedules are built on synthetic data following the real value-pair domain;
all support labels equal the two existing fact values and exposures remain100/100.

Other fixtures exercise matching,replay rejection,15-record analysis,90 role-bearing partitions,
360 comparator records,one-candidate-miss negativity,19 hash rejections before parent dispatch,
604/1091 protection maps,an unprotected-helper failure,semantic suite-ID filtering,run ordering,
strict bundle schema,no-overwrite,hash and semantic tampering,and compact receipts. Parent archives,
Git,models,scorers and regression members are mocked where necessary. These are not C293 findings.
Actual OWN document reads are tested with CP932 defaults;AST checks reject implicit read_text
encoding in new source/test. No user environment change or decoding-error suppression is required.

## Parent/schema/deciding-path review

The direct import is C292. Its context returns C291 and the inherited core bundle. C291 supplies
C287 diagnostic,C284 evaluator/replayer,C283 quad scorer,C282 normal-TRAIN table builder and core.
C292 is a diagnostic parent,not a model-state bundle. Before dispatch,verify19 ordered summary
hashes:C292,C291,C290,C289,C288..C274. C292.verify_artifacts is called with18 ancestor paths and the
accepted C292 execution HEAD under its no-neural guard. Its three artifact descriptors are pinned
from the published C292 receipt. The parent recursively verifies the old datasets/checkpoints/
evaluation archives and all original masked/full gates. C291 input JSONs are read only after that
reconstruction,and their canonical hashes are checked again. No parent checkpoint trains C293.

The immutable C284.evaluate and replay_one sources were reread. Evaluate requires eval mode and
frozen parameters;replay strict-loads state,checks fingerprint,all-view logit drift<=1e-9 and exact
argmax. Its per-model train/final/replay call counts are preserved. C287.normalize_task/partition
sources were reread;seed/arm are metadata and returned rows/correct/direct_pass fields match the
child's actual use. C292.answer_role/tally apply full256-class argmax to original logical labels;
C293 reconciles role counts against old scoring before persistence. It does not filter predictions.

All598 inherited source pins and1081 protected inputs remain checked. C292's exact blob and all
repository-local modules exposed by the used parent/core contexts must be pinned. Add six OWN
sources and four C292 summary/output inputs for604/1091. No dependency omission is waived and no
accepted source is patched to accommodate the new experiment.

## Changed-variable and interpretation audit

Three fresh arms:CE,1.25*CE,and CE+.25*Lsupport. Support is the unordered pair of existing TRAIN
labels,not the correct-query label alone. The original CE remains unchanged in candidate;only
its support component is weighted more. All components come from the same single forward.
Same model14256 parameters,48-token context,normal mixed2/3 TRAIN,800 updates,constantLR.005,
initial state,batches and per-length exposures. Neither HOLDOUT nor four-character data trains.
The uniform scaling arm is a control,not an exact gradient/AdamW/clipping match. The candidate can
still confuse the two in-context facts;support loss alone is not a capability objective. Old masks,
full gates and output-role counts remain. A candidate PASS is not automatic superiority or Gate F.

15*(800+81+81)=14430 forwards;809280 rows;57720 core calls;12000 updates and576000 training rows.
One15-state checkpoint bundle write/load,15 strict loads. Auxiliary numerical work does not add
neural forwards. No speed or memory advantage is asserted. Operational tests are separate.

## Runner,regression and authoritative boundary

OWN40/modules178/loaded4358/focused4357. The sole inherited exact C204 exclusion is retained.
Fixture suite tests construct/inspect ID sets instead of source-string numeric counts. The actual
inherited regression suite must still be loaded and executed on the user's machine.
Runner has three embedded Python blocks. Postcheck paths=sys.argv[2:21],head=sys.argv[21],argc22.
Launcher fixes all19 summary paths and returns before science/publication on Validate failure.
Existing dispatcher was fetched again:tools/invoke_active_v2.ps1 Git blob
 e3923b6224959b442afefa02fafa967e2e6d462e.
It resolves only the unique ACTIVE token in Formal state and parses the selected launcher;the
launcher parses the runner. User invocation must retain the dispatcher ParseFile step as well.

Not executed here:Windows PowerShell parsing,actual user-local parent artifacts/source byte maps,
full4357 regression,real FOLD initial-model/table preflight,and15-model C293 science/strict replay.
These remain mandatory Validate/Execute gates. This review authorizes only the guarded launcher.
Invalid integrity retries SAME C293;valid all-five miss is ACCEPTED VALID NEGATIVE. C294 remains
unregistered until C293 formal judgment. Accepted C292/C291 verdicts and Gate F are unchanged.
