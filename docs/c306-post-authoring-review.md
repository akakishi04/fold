# C306 post-authoring review

post_authoring_review = PASS
Scope: separate committed-byte/static review plus executed local software tests,not authoritative Windows science.
Review target:eb84648751125f11289abd257aedd20787f39088.
Acceptance base:73282101c89ac14cf5aa55d6d91c4bedc87b176d.

## Remote-byte match and scope

All six OWN files were fetched after the authoring commit from the immutable review target.
Source371lines and test403lines were read in consecutive ranges,with an additional source-tail
fetch where the response was truncated. Other files were fetched in full. Their whole-file
Git blob identities match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c306_broad_length_core_freeze.py:5ca6ce358a7f6fe5fc3daf3c172289d6a4f0a786;26257bytes.
- tests_lm/test_v05_c306_broad_length_core_freeze.py:1cbba18fc0dfbece7bc49ab7d3034f26a7b029bd;29504bytes.
- tools/run_c306.ps1:65521ed065d0f74dc80a2637e984410e35d9255a;4674bytes.
- tools/invoke_c306.ps1:ec290e015e5556cc91f6cd48b87fd00438e05721;6605bytes.
- docs/experiment-ledger-addendum-c306-preregistration.md:9598a3ab1414645adf0c276ecb5ddb8fe1df07bc;8827bytes.
- docs/v5b-broad-length-core-freeze-v0.1.md:776499cdc30633a8a8c754fb5a8bfff331614166;1110bytes.

The acceptance-to-authoring compare contains exactly these six additions. No accepted source,
test,log,preregistration or dispatcher changed. Activation must preserve all six reviewed blobs.

## Post-match verification actually executed

python -m unittest tests_lm.test_v05_c306_broad_length_core_freeze -v
Normal default:Ran32 tests in14.770s;OK.
Whole same suite with io.text_encoding default emulated as CP932:Ran32 in20.192s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. These are after all six remote matches.
All6 files UTF-8/no-NUL. Both Python files and all3 embedded runner Python blocks compile.
Recursive symbol-table/import-binding audit found0 unresolved globals. Manifest recomputation:
28a55839e6cf0c31ceac29fafb7e535b30d24259a0983589ebd4ae6121080b27 matches.
PowerShell itself was not parsed or executed here;its guarded Windows ParseFile chain remains mandatory.

The actual C306 fit loop executes1200 AdamW updates in both arms on target-coded toy inputs.
A repeat frozen-arm fit reproduces the CE history and verifies one optimizer at step1200,with
core parameters excluded from optimizer membership. The frozen core is unchanged;the full-train
core changes. These toy inputs test software control flow,NOT task generalization.

Integration fixtures extract C304 LengthReadout,span_mask,prefix_tensor,schedule_stats,evaluate,
replay_error and replay_one definitions. They use substitute correctly sized backbone/core/reader
components,not the actual complete FOLD backend. Factory checks include14256 stored parameters,
14256/10928 trainable counts,independent storage and common64-slot configs. The first-batch probe
checks initial output and noncore pre-clip gradient agreement,absent frozen-core gradients and
nonzero encoder gradients. It does not substitute a no-grad forward for core freezing.

Local parent support contains selected fetched definitions,not a full byte-identical parent module
or complete repository clone. On the user's checkout the test extracts the definitions from the
full accepted C304 source. Only OWN6 are asserted byte-identical to the committed remote files.
No local parent support excerpt is committed. The actual Windows backend probe remains pending.

The real child train_one executes1200 training plus108 evaluation calls on a controlled model;
the accepted replay helper then executes108 calls and verifies unchanged outputs/state. The counting
fixture simulates4 core calls per model call;it is not measured actual FOLD core execution.
All five schedules are checked for100 exposures per row per2/3/4 length,400updates per profile,
complete pairs,private-RNG determinism and a separate sampled-epoch reference. Tests reject wrong
pair/target/arm,core drift,loss metadata,unmatched initial states and invalid replay counts.
The synthetic analyzer preserves80 partitions/40 contrasts;one failing candidate keeps the gate negative.

Actual load_parent dispatch is exercised against a diagnostic payload that returns ONE dict.
Each of32 bad summary hashes is rejected before parent verification. Wrong parent status,source
and artifact inventory are rejected. Temporary-file checks exercise682/1267 protection and a
missing helper. Production run tests dispatch all10 fits before all10 replays,exercise the actual
child bundle serialization/loading,JSON reconstruction and no overwrite. Byte and semantic
corruption fail even with an updated output descriptor. Semantic suite IDs verify4814 minus the
one inherited C204 exclusion=4813;the full actual inherited suite was not executed here.

UTF-8 reads of all actual OWN files pass under CP932-default emulation. This emulates text-decoding
only,not Windows. Test31's mutation zeros encoder WEIGHTS and checks initial-state mismatch;despite
its imprecise comment,it is not a gradient-zeroing experiment. Gradient routing is checked by the
actual first-batch probe and test04,not inferred from that mutation or a source-string assertion.

## Scientific path,writer and dependency audit

C305.verify_artifacts returns a single payload dict,not the tuple returned by C304. C306 uses
that exact schema. Verify32 ordered hashes first,then call C305 with31 ancestors and its accepted
scientific HEAD. Its exact summary seals3 outputs;its verifier recursively reconstructs C304 and
the aligned diagnostic. The source requires diagnostic scope,exact parent flags and720/120
reconciliation counts. It never reads C305 predictions as training targets.

C305 has no dataset/model output. Read the verified C304 dataset from the SECOND summary's
directory after recursive verification. The exact C304 prompt_dataset/validate_prompts enforce
canonical data and old renderer identities. Parent writer semantics were checked:raw outputs
are frozen final evaluation logits;the child makes fresh models and never loads learned parents.

C304 train_one/analyze require old seed/cohort and full-core change,so C306 does not call them.
The child owns initialization,training,schedule,cohort/result analysis. Reused C304 LengthReadout,
training_tables,schedule_stats,score_length,evaluate/replay_one have compatible helper contracts.
Its replay_one only needs the supplied model/state/record,strict final hash and raw outputs;it
checks all2/3/4/5 views with1e-9 tolerance and exact argmax,108/10368/432 replay accounting.
C287 normalization still receives the canonical triple-shaped scores through C304.score_length.

Only direct import is C305. Source protection retains all676 inherited pins,explicitly checks
C305/C304 and every C304.PINNED backend/core/reader/scorer blob,and requires actual pair/context/
core/factory-language helper files in that map. Add OWN6 plus4 parent inputs for682/1267.
No accepted source/test/log or dispatcher changes,no waived dependency,no new test exclusion.

## Intervention,counts and runtime boundary

The only policy change is core requires_grad and optimizer membership. Core remains in the forward
and backward-to-input graph;no detach,new hooks,coefficient,auxiliary loss,pretrained core or best
seed donor. Both arms use fresh paired seeds306001..306005,ordinaryCE,identical2/3/4 examples,
64slots,1200updates and paired schedule. Core freezes at that seed's random initial state. Full
weights differ after learning by design. Fewer trainable weights/global clipping/backward costs
are part of the policy and are not claimed to isolate a unique mechanism.

10*1200=12000 updates;576000training rows;10*(1200+108+108)=14160forwards;
783360 total rows;56640 core calls;10 state loads,one model bundle write/read,network0.
No extra first-batch probe updates enter science. All original local/masked thresholds remain.
Primary all5 candidate length5 pass;control also reported. Prior C303/C304 counts are motivation,
not concurrent baselines. Gate F and old verdicts are not automatically promoted.

Runner3 embedded blocks compile;32 fixed parent paths;postcheck slice[2:34],HEAD[34],argc35.
The fetched unchanged active_v2 dispatcher blob is e3923b6224959b442afefa02fafa967e2e6d462e.
It checks the formal ACTIVE token and parses the selected launcher;that launcher parses its runner.
The final user block must parse the dispatcher too. Validate failure exits before science/publish.
Own32/modules191/loaded4814/focused4813. Source counts and return-value bindings match the manifest.

Not executed here:Windows PowerShell ParseFile,all32 actual parent archives and Windows protected
bytes,the complete4813 inherited tests,or10 actual C306 model training/evaluation/replay runs.
All remain mandatory local Validate/Execute gates. This review authorizes only the guarded launcher.
Any integrity failure repairs SAME C306 without changing the scientific conditions. C307 remains
unregistered until formal C306 judgment.
