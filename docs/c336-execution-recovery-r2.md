# C336 R2 -- preserve the real four-value parent schema

Date:2026-10-21 Japan time. Stage:V5-B-SAVED-QUERY-ORDER-PATTERNS.
INVALID EXECUTION / RETRY SAME C336. C335 ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED; C337 NOT REGISTERED. This is a schema-adapter correction.

## Operational skip versus the actual attempt02

The user's STALE_EXPECTED_HEAD invocation supplied old C335 execution
3b185a97ef86ab911d425620b4e6645fbd0c9f9e against current
3ab32fc78d924914b07141d4a009de3c8e39fcbe. It executed nothing and published nothing.
This skip is not another C336 invalid attempt or a scientific verdict.
Do not replace ExpectedHead with the log-publication commit merely to bypass it.

The current commit is the already-published C336 R1 attempt02:
execution5029fbbad2209f462af8939c0e77f56a5a63be5e;
publication3ab32fc78d924914b07141d4a009de3c8e39fcbe,whose sole parent is execution.
Publisher reports197751Windows bytes and SHA256
45d503dddd1abdffe9ed6e44bdbc04495ae009a62759349429754347c4abaab5.
Exact log blobdefe297ea99b6ca185aab39947c09c874d4540ee;
metadata blobe4a09ba1b5f9ce8953457e2e971ec3ed19624db3.
Copies are archived at docs/experiment-run-logs/c336/attempt-02/latest.*.
Attempt01 and original latest bytes remain preserved. No local artifact deletion.

## Reached phases and evidence boundary

Native lock probe,capacity4360,accepted parent semantics and877source/4360input
registration passed. All6090tests/226modules passed;failures/errors/skips0;
regression elapsed1680.515seconds. Ordered-ID digest
469a8865f79307ef97c8dba2eac3d87d522f75f80fb7c16e34c64510a9ee5132.
Then saved_query_order_patterns -> run_diagnostic -> analyze -> logical_groups
raised ValueError:logical row semantics. Science exit1;run_execution_valid=false.
No complete C336 diagnosis,final input rereads or fresh verification was reached.
The R1 capacity defect did not recur. Regression PASS does not make this run valid.
Remote audit inspected startup,completion and full failing traceback,not an
independent rehash of the original Windows log or local artifact reconstruction.

## Root cause: two observed values are not a binary value catalog

The accepted writer model_c267_name_coverage_training.dataset uses permutations of
range(4),two distinct integers per fact pair. Source blob
5a167f078ab5b3aa8052e7995d004a25ca25fc0f. Its DATA_SHA,also retained by C304/C329,is
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
TRAIN has eight ordered value pairs;HOLDOUT has(0,2),(1,3),(2,0),(3,1).
Entity pairs are(0,1),(0,2),(1,2);both en/ja and both query/fact orders are retained.
Targets are48+the queried value,so observed target bytes range48..51.

C336 incorrectly demanded values exactly{0,1} in logical_groups and targets exactly
{48,49} in classify. Fixing only the first guard would fail at the second. The
initial documentation repeated the same error. The old synthetic data used invented
entity names and only0/1pairs and never matched the actual canonical dataset hash.
This is an authoring/schema audit error,not corrupt C335 data or a model failure.

## Minimal correction and unchanged scientific question

Change only the two benchmark guards to require distinct integers in0..3 and distinct
target bytes in48..51. Keep exact target/query binding,the two-observed-value taxonomy,
all256-way argmax,no label repair and all original row/group coverage checks.
A third value remains other_class even if it is one of0..3 but absent from that
particular pair. value_lock still requires one of the two observed values.
Reject bool,float,duplicate or out-of-range values;do not remove validation.

The unaccepted C336 preregistration is explicitly amended and its original archived
at docs/handoff-history/c336-pre-r2-preregistration.md. No saved dataset,split,
checkpoint,prediction,seed,profile,threshold,scope,count or accepted result is edited.
The manifest already specifies two observed values without a0/1-only catalog;it
remains byte-identical withSHA
e6f992e680bc4b80284dbc04366566f737fb1bfd3f55fb0ac10d76d90ebd76af.
Same32own IDs/6090full tests/226modules/877sources/4360inputs. Same12960quads,
6480paired quads/51840answers/720strata/all30parent HOLDOUT contrasts.
R1 executor2d35c49a0adf570458c7232cf44e373e7e2e54c4 remains unchanged,including explicit
max_files=INPUT_COUNT,all held leases and4360final uncached rereads. No C335 retraining.
No accepted source/test/contract,runner,launcher or dispatcher changes.

## Tests and author-environment boundary

Replace the toy logical dataset with an independent exact canonical reconstruction:
all192TRAIN/96HOLDOUT rows,IDs,integer entities,values and order must match the frozen
DATA_SHA. Test02 compares it to actual C267.dataset and validate_data. Production
analysis/loader/writer/reconstruction tests now process these rows across the full
12960quad/6480transition fixture. Predictions and parent scorer/semantic collaborators
remain explicitly synthetic;this is not the user's C335 prediction archive.
Preserve the old binary-pair tests and add all12ordered target pairs*16within-pair
response patterns,third-value behavior,row-order invariance and bad-type/range controls.
Keep all R1 boundary tests,proof/tamper checks and exact existing32method IDs.

Author environment is a targeted reconstructed Linux tree,not a complete checkout.
Modified files and unchanged C336 executor/launcher are reconstructed byte-identically.
For two historical dependencies,the author uses verbatim source EXTRACTS:C267 dataset/
validator/render and C324 LockedHashes with their required constants/helpers. These
are not full historical modules or native Windows protection. They are never committed.
On the user machine,test02/test22 import the actual accepted full modules,which remain
inherited protected dependencies. Full6090native execution is still required.

Before retry authorization,retrieve the committed benchmark/tests/amended contract
through EOF,match tested Git blob hashes,rerun normal/CP932 own suites and free-name/
compile/manifest audits. Independently restore each old guard and require the actual
run_diagnostic path to fail on canonical rows before writing any diagnostic output.
Record those intentional negative controls separately from ordinary test success.

## Stop and invocation

No retry command until post-authoring review PASS. Standard PowerShell7/ParseFile/
active_v2 ->invoke_c336 ->run_c336 remains. Use the final reviewed recovery commit,
not3b185a(C335),5029fb(already-run R1),or3ab32f(publication).
Repeat the complete registered run including6090tests;do not reuse the previous
regression receipt under new source. Completion requires persisted_query_order_patterns
PASS,execution_envelope_verified,run_execution_valid=true and log publication.
Any technical failure remains SAME C336;no C337,automatic rerun,filtering,threshold
relaxation,CI,paid service,package installation,artifact deletion or accepted-source edit.
