# C294 independent post-authoring review

post_authoring_review = PASS
Scope:committed-byte/static review plus local numerical/control fixtures,not user-local science.
Review target:11366c4e8d90ff51e048aeb1d7b74123a5be124a.
Acceptance base:8bdfdeae1daeab051af6407e5101578e66c1d06f.

## Remote-byte verification

All six OWN files were fetched after the authoring commit at its immutable SHA. Source and tests
were read in consecutive ranges covering their complete files;the four other files were read in
full. Whole-file Git blob identities match independently hashed local bytes6/6:

- fold_lm/v05_benchmarks/model_c294_saved_support_choice_audit.py:c645e0b62eba41c6f48fa140fa26f8cc3a26e3b9;22002 bytes.
- tests_lm/test_v05_c294_saved_support_choice_audit.py:373cbf0508ed08b54ad4a3dd36d38ed61b49cc95;21925 bytes.
- tools/run_c294.ps1:38a8d97b0f0956ebcdfb987e4eef8483c50adbb6;4878 bytes.
- tools/invoke_c294.ps1:d92c4c7b8fe13bf9c7eee16c24cc35f8a5a55c25;5434 bytes.
- docs/experiment-ledger-addendum-c294-preregistration.md:b53c603e615f20b7b0e5bee8bdd112e38d6a79fa;7095 bytes.
- docs/v5b-saved-support-choice-audit-v0.1.md:4fb328a83a30c27267bf3fba1069f26c6d953477;1492 bytes.

Remote acceptance-to-authoring comparison shows exactly these six additions. No accepted source,
test,preregistration,log or protected dispatcher changed. Activation must preserve all six blobs.

## Checks executed after matching

python -m unittest tests_lm.test_v05_c294_saved_support_choice_audit -v
Normal local default:Ran32 tests in10.569s;OK.
Entire same module with io.text_encoding default emulated as CP932:Ran32 in9.977s;OK.
Runtime:Linux/Python3.13.5/PyTorch2.10.0+cpu. Not actual Windows or the full4389 regression suite.

All6 files decode as UTF-8 with no NUL. Both Python files and3 runner-embedded Python blocks compile.
Symbol-table global/import-binding audit:zero unresolved globals,allowing standard __file__/__name__.
Manifest recomputation matches e929d73dabbcc3c6c229c46282854f8c196802e4e52995f10eb94b977b9ba1c6.

Numerical tests cover the four mutually exclusive categories,uniform closed-form CE/support/choice,
independent support-masked argmax reference,query/fact-order independence of the support set,
exact ties without target preference,1e8 row-offset invariance,and an outside full winner despite
support mass above1/2. They check finite values,shape/dtype/no-grad contracts and CE decomposition.
The complete38880-row fixture analysis reconstructs90 partitions and540 profile/language groups.
Tests compare original counts/roles/NLL to independently supplied parent references and reject
missing/duplicate identities,wrong parent totals,and wrong normal NLL or role counts.

Other fixtures execute20 hash checks before parent dispatch,wrong parent/archive rejection,
no-neural/state/save guards with restoration,610/1106 protection maps and an unprotected helper
failure,semantic suite ID filtering,CLI indices,run ordering,full persistence and reconstruction,
no overwrite,byte tampering and semantic tampering. Actual text reads in all6 files are exercised
under CP932-default emulation and AST checks reject implicit read_text encoding in source/test.

These fixtures use synthetic logits/data and substitute parent archives,Git and inherited suite
members where required. They are not actual C294 findings. No C293 checkpoint,real local data,or
full inherited4389-test suite was executed in this review environment.

## Parent writer,adapter and direct dependency audit

C293 run/verify_artifacts was re-read at the committed target. It saves records with final frozen
raw[task][split][profile][view] logits in fold-c293-support-eval-v1,then reconstructs the complete
metrics,loss histories,matching and all original normal/masked gates. Its verifier returns
(payload,metrics). C294 uses this exact contract,not a training checkpoint loader or a similarly
named older adapter. The parent summary includes final_partitions with original output roles and
final_normal_nll;C294 checks the actual field names and reconciles them rather than guessing them.

All20 ordered summary hashes are checked before C293.verify_artifacts(parent_dir,19 ancestor
paths,accepted_execution_HEAD). Constants follow the immutable C293/C292/C291/C290/C289 chain.
The exact C293 summary SHA seals all8 artifact names/hash/size descriptors. Parent validation
reconstructs original masked/full gates before the new normal-logit analysis. No old weights are
loaded into a model. C294 guards Module calls,load_state_dict and torch.save under no_grad.

The only direct repository import is C293. All604 inherited source pins and1091 inputs remain
checked. Every repository-local module exposed by the used parent context/core bundle must be
in the inherited map,and the direct parent must have its exact published blob. Add6 OWN plus9
parent summary/artifact inputs:610 source pins/1106 protected inputs. No coverage waiver or
accepted-source edit is used. C294 itself is added to the source/input protection maps.

## Interpretation and numerical boundaries

Oracle support comes from the two verified input fact values,sorted by numeric class ID. The
requested target is used to validate binding and score correctness,not to order candidates or
choose a tied winner. Full and conditional argmax therefore use the same lowest-class tie rule.
Exact within-support and support/outside ties are separately visible. No fitted tie tolerance.

Stable log-softmax computes per-row CE=Lsupport+Lchoice within rtol/atol1e-10. The same identity is
checked for aggregates and original normal NLL is reconciled to the parent summary. This does not
imply the neural model internally has separate support and choice stages. Original predictions
and every old capability gate stay unchanged. Conditional accuracy uses privileged support and
is NOT a deployed restricted decoder,model improvement,causal identification or Gate F success.
Keep all15 models and complete original data;dependent rows are not extra independent seeds.

## Runner,count and execution boundaries

Own32/modules179/loaded4390/focused4389;only the inherited exact C204 exclusion remains.
The semantic suite fixture checks constructed test ID sets and the exclusion. Real inherited
suite construction/execution remains a Windows runtime obligation,not a completed local check.
No accepted tests are changed and no source-string numeric-count assertion is introduced.

Runner contains3 compiled Python blocks;postcheck paths=sys.argv[2:22],head=sys.argv[22],argc23.
Launcher has20 exact ordered summary paths. Validate failure returns before scientific logging
and publication;Execute only follows authoring_runtime_preflight PASS. The unchanged versioned
active dispatcher must be parsed in the user block,it parses the selected launcher,and that
launcher parses its runner. No PowerShell ParseFile execution is claimed on this Linux host.

Mandatory pending Windows gates:real20 ancestor summaries/artifacts,full parent reconstruction,
610/1106 source/input bytes,complete real-data numerical dry-run,own32,full4389 regression,
PowerShell parsing and actual saved-output Execute/postcheck. PASS here authorizes only that
guarded entry,not a scientific verdict. Integrity failure retries SAME C294. C295 remains
unregistered until C294 formal judgment. C293 and Gate F verdicts remain unchanged.
