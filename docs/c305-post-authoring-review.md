# C305 independent post-authoring review

post_authoring_review = PASS
Scope: committed-byte/static review and executed local software tests,not authoritative Windows science.
Review target:0d48409fac678d7ad53b1bcd6b3d23e57bf2d143.
Acceptance base:75b6545c1dc1d570286e76bb0b53473673247d33.

## Committed-byte verification

After the authoring commit,all six OWN files were fetched from the immutable review target.
Source352lines and test360lines were read in consecutive ranges;the other four files in full.
Returned whole-file Git blob identities match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c305_saved_length_overlap.py:e822f5680193951cbc9270cb70cb0d4d5fcb12b6;20186bytes.
- tests_lm/test_v05_c305_saved_length_overlap.py:0750b73645465ea00a724d22ce0e082b1f157a9d;21375bytes.
- tools/run_c305.ps1:b119d2edb697c65a63085be0b73d5d5597833f6e;4504bytes.
- tools/invoke_c305.ps1:6034743c889586e218e5dda574021de47abeec57;6502bytes.
- docs/experiment-ledger-addendum-c305-preregistration.md:cf27544bdb7900e8e53980a8dcec7741bbccbfaf;6741bytes.
- docs/v5b-saved-length-overlap-v0.1.md:c64e7beb015132174892598ca509fc2d257bf8a4;986bytes.

Acceptance-to-authoring comparison contains exactly these six additions. No accepted source,
test,preregistration,log or dispatcher was modified. Activation must preserve all six blobs.

## Verification executed after all six remote matches

python -m unittest tests_lm.test_v05_c305_saved_length_overlap -v
Normal default:Ran32 tests in0.873s;OK.
Entire same suite with io.text_encoding default emulated as CP932:Ran32 in1.032s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. Pre-commit results are not substituted here.
All6 files are UTF-8/no-NUL. Both Python files and all3 runner-embedded Python blocks compile.
Recursive symbol-table global/import binding audit found0 unresolved globals.
Manifest recomputation matches844119479e6a43fc9fa5d3510ce05d8300ed2108dd819c6058b24b3b449632bd.

Behavioral tests exercise all four correct/error transitions,wrong-to-different-wrong changes,
zero-denominator nulls,prediction byte bounds,and2/3/4 reference indexing. An independent81-pattern
enumeration checks denominators and conservation. Full synthetic analysis reconstructs12960
aligned questions,51840 saved predictions,90 transitions,540 detailed groups and30 signatures.
Independent signature counters and subgroup sums check aggregation,not source-string literals.
Query-pair completeness,missing models,duplicate logical IDs,misaligned prompt IDs,wrong parent
totals/partitions and malformed/nonfinite/gradient-attached logits are rejected.

Tests block neural Module calls,state loading and torch.save inside the diagnostic scope and
verify restoration afterward. The actual child load_parent/reconstruct path runs against mocked
parent archives,including all31 hash failures before verifier dispatch. Wrong parent status,
cohort and archive schema are rejected. Temporary-file protection tests check676/1257 accounting
and missing direct helpers. The actual child run verifies precheck->reconstruct->precheck ordering,
JSON serialization/reconstruction and no overwrite. Byte and semantic tampering fail even when
an output descriptor is updated. Result scope checks reject capability promotion and bool-as-zero.

The semantic suite fixture constructs4782 unique IDs,removes only the exact inherited C204 ID,
and verifies4781 retained IDs. This is not execution of the actual inherited suite. Explicit UTF-8
reads cover all real OWN documents under CP932-default emulation;it is text-decoding emulation,
not a Windows environment. CLI parsing,context dispatch,repository guards and runner indices pass.

## Parent writer,alignment and dependency review

The actual C304 writer/verifier source was reread at its accepted immutable ref. It writes final
frozen outputs as records.raw[str(length)][split][profile][view],with canonical logical rows and
length-datasets prompt items carrying source_id/target. These are final evaluation logits,not
intermediate losses or optimizer states. C305 reads no learned checkpoint into a model.

All31 ordered summary hashes are checked BEFORE exact C304.verify_artifacts(parent_dir,30
ancestors,accepted_execution_HEAD). The exact parent summary seals all7 artifact descriptors.
Its unchanged verifier reconstructs prompts,training schedules,all original normal/masked gates
and replay metadata. C305 additionally requires the original15 length-pass records and valid
negative status. It does not infer individual error overlap from C304's matching4/5 gate flags.

Each child row aligns the same model,split,profile,source_id,query and target across all four
lengths. Prompt IDs/targets are checked against the canonical logical rows. Predictions retain
full256-class argmax behavior. Parent nested length_scores intentionally use canonical triple
profile labels;the child explicitly maps repeat/shared_prefix/shared_suffix into
tripled/shared_prefix2/shared_suffix2. All720 profile/language/length normal totals are reconciled,
including query-pair collapse,plus all120 model/length/split normal partitions.
No parent cohort analyzer is called with invented fields or altered profile semantics.

Sole repository import:C304. All670 inherited source pins and1243 protected inputs remain checked.
Actual repository-local parent/context/core helper files must be in that map. Add OWN6 and8
parent summary/artifact files for676sources/1257inputs. No accepted-source mutation,dependency
waiver or extra regression exclusion. Child numerical reconstruction and recursive parent
verification run under the no-neural guard;reading saved tensors and numerical argmax are allowed.

## Scientific and runtime boundaries

Primary descriptive contrast:four->five. Two/three references and all16 correctness signatures
remain secondary descriptions of the same cohort. Report newly introduced errors,recoveries,
persistent errors and whether persistent wrong answers themselves change. Null denominators are
not interpreted as zero rates. Every count has its denominator;none is a new capability gate.
The model/data observations are dependent and do not create independent seeds or significance.
No overlap pattern alone proves memorization,an attention mechanism or a length-independent rule.

Scientific training/model forwards/neural row presentations/core calls/model-state loads/new
checkpoints/network calls are0. Operational regression fixtures are separate. Outputs are three
UTF-8 JSON artifacts plus summary.json;no copied dataset or model bundle. Console mirrors90
transition groups and30 signature groups;all detailed data stays local/ignored. PASS means only
correct diagnosis/reconstruction. C304's negative and Gate F remain unchanged.

Runner has3 compiled Python blocks,31 ordered summary paths,postcheck paths[2:33],HEAD[33],argc34.
Validate performs parent protection and full real-data alignment before own32 and focused4781.
Failure returns before scientific logging/publication. Preserve unchanged active_v2 and the
dispatcher/selected-launcher/runner ParseFile chain. Own32/modules190/loaded4782/focused4781.

Not executed here:Windows PowerShell parsing,the actual31 parent archives and protected Windows
bytes,the real4781 inherited regressions,or C305 analysis on the user's C304 evaluation tensors.
The local checkout contains OWN files,not a complete repository clone. Parent verifiers/data,
Git and scorer totals are substituted in tests where unavailable. No actual C305 findings are
claimed by these tests. Mandatory Windows Validate/Execute retains all those checks.
Any integrity failure repairs SAME C305 without changing the cohort,alignment or counting rules.
C306 remains unregistered until C305 formal judgment;no model selection or Gate F promotion.
