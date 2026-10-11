# C320 post-authoring review

post_authoring_review = PASS
Scope: committed-byte/static review plus executed local software controls,NOT actual FOLD science.
Review target:b975f7d2c8cfbf3c9ae71c4b9f147ab1be10ebd1.
Acceptance base:1c60afa5997ca9f61a6f5b44e73a31e2b15cd609.

## Remote bytes and changes

All6 OWN files were refetched after commit from the immutable review target. Source324lines
and tests337lines were covered by consecutive complete ranges;the four other files in full.
Each returned whole-file Git blob matched the independently hashed local file:

- fold_lm/v05_benchmarks/model_c320_unequal_name_lengths.py:5e183c330c883d8c44d9cd66ac2b89365517f9cc;22623bytes.
- tests_lm/test_v05_c320_unequal_name_lengths.py:ad0c790c3c49a65a8f84402ca7d62581de5c8441;25813bytes.
- tools/run_c320.ps1:2a918708669ba45dcca3228983acc8b492f40800;4722bytes.
- tools/invoke_c320.ps1:3538dedd11348fe14f9818471da3d15d7c4f99bd;8005bytes.
- docs/experiment-ledger-addendum-c320-preregistration.md:1df2d0c6be363598da653ef89581610ce3721d69;7684bytes.
- docs/v5b-unequal-name-lengths-v0.1.md:a5798613c71658282767133b4290ed5bb710e738;1155bytes.

Remote comparison acceptance->authoring shows only these6 additions. No accepted source/test/
preregistration/log/dispatcher changed. Activation must preserve all6 reviewed OWN blobs.

## Executed after the six refetch matches

Normal complete module:24/24 PASS in12.710s;zero failures/errors;process exit0.
Complete module under io.text_encoding default-CP932 emulation:24/24 PASS in12.890s;
zero failures/errors;process exit0. Patch spans module import,setup,test methods,teardown.
Both runs uninterrupted. Each log's24 distinct test IDs checked,with no omissions.
CP932 default emulation is not full Windows/console emulation. Local runtime Linux/Python3.13.5/
PyTorch2.10.0+cpu. No PowerShell executable exists locally. Terminal cleanup messages after OK
were unrelated to successful unittest exits. Earlier pre-commit tests are not this evidence.

All6 hashes rechecked after both runs. UTF8/noNUL;both Python files and all3 embedded runner
Python blocks compile. Recursive symtable/import-binding audit reports0 unresolved globals,
after accounting for actual module bindings,builtins and standard module globals.
Manifest self-hash:34ac7cbac03191c2e64ae05887f7d04cbc90c3cf0a73e18427708c1bbeed307d.
46 launcher paths ordered C319..C274;postcheck paths[2:48],head[48],argc49. Own24/modules205/
loaded5222/focused5221,with sole inherited exact C204 exclusion unchanged. Synthetic suite IDs
exercise the exact5222->5221 retained set and duplicate rejection,not actual5221 regression runs.

## Behavioral and source-level review

Canonical synthetic logical data and independently rendered original1..6 prompts match accepted
DATA/PROMPTS hashes. Child equal-length rendering matches those original bytes. Every new prompt
is independently parsed for distinct2/4 names,values,question target and presented fact order.
All1728normal new inputs are distinct/disjoint from old normal inputs. No new byte vocabulary.
Every UTF8byte,BOS/EOS,padding and actual C304 query-span mask checked;maximum37bodybytes/39tokens.
Changing target metadata cannot change rendered text. Masks and both name-length assignments hold.

Tests execute actual accepted C304 forward/span/scorer-adapter ASTs,C315 evaluate/validate_raw/
replay_error and C319 trained_readout/hook_snapshot with controlled encoder/core components.
The actual child infer_one runs BOTH retained policies through old144/new54/old144 forwards,
validating342forwards/32832rows/1368core calls per state and unchanged full weights/hooks.
Both original outputs reproduce exactly on these controlled models. Wrong policy/fingerprint,
missing cohort,invalid receipts and false replay are rejected. New scoring uses the accepted
C304 profile adapter with a controlled C270 scorer;actual local/masked model competence is untested.

Every one of46 parent-summary hash mismatches is rejected before dispatch to parent verification.
The real precheck runs on766/1443 temporary file fixtures and rejects an unpinned repository helper.
Production run-path tests check a single C319 checkpoint-bundle read at summaries[0],all10
inference dispatches,no optimizer and no new trained-model write. Only evaluation tensors saved.
No-neural persisted reconstruction passes;byte tampering and semantic tampering after descriptor
resealing fail. Existing run-directory overwrite is rejected. Actual runtime_preflight is tested
on controlled bilingual inputs with both policy wrappers. Primary must pass BOTH layouts in all5
mean_last models;secondary successes cannot compensate,and primary/secondary are not swapped.

Local parent support files contain exact fetched function slices,not full modules/a repository
checkout,and are NOT committed. On the user checkout,tests extract those functions from the full
accepted files. Parent archives,Git,model factory/scoring interfaces are substituted in some
software tests. This is explicitly NOT actual saved-checkpoint capability or full inherited
regression evidence. There is no claim that scientific C320 ran here.

## Parent writer,dependency and inference audit

Accepted C319 source was inspected at blob8222ddc165464b8acb84380f47d397504308a9df,including its
writer/loader/verifier at the immutable review ref. It saves final same-policy evaluation records
after all fits and strict policy-specific replays. Checkpoint schemafold-c319-trained-readout-
models-v1 carries ordered seed/arm identities;eval schemafold-c319-trained-readout-eval-v1 has
readout_policy/full final fingerprint/raw1..6 outputs. C320 does not treat the C318 diagnostic
archive as a model checkpoint. It calls the actual C319 loader/factory and strict-loads all10
original states,including last_only319005. No new initial states are used as scientific outputs.

C320 first verifies46 ordered summary hashes,then invokes actual C319.verify_artifacts with45
ancestors and the C319 scientific HEAD. Parent validates every fit/schedule/policy/replay and
seven artifact hashes/sizes. Only its own verified dataset/prompts/final raw records are read.
C319.context()[1] is the accepted C317 repository guard;its final context element is the original
backend namespace. Actual C319.trained_readout wraps EVERY old/new pass using the record's own
training policy. Thus a last-only checkpoint is never accidentally tested with mixed inference.

All760 inherited source pins/1429 input paths checked. Repository-local context/lazy/factory-
language helper coverage retained. Add OWN6 and8C319 files ->766/1443. The scientific direct
import is only C319;standard torch/stdlib imports are not repository source dependencies.
Accepted C304.score_length groups logical facts/query pairs/orders/views and takes no identifier-
length argument. It is reused per new layout,without calling the old fixed-length cohort analyzer.

## Interpretation and remaining gates

One changed task constraint:the names have unequal lengths2+4/4+2 within a question. Both lengths
are individually trained,but the composition is not. Positions,separations and name geometry
change with it. Different lengths can also provide an extra identifying cue;success alone would
not prove content-based name matching or arbitrary composition. No new mechanism is inferred.
The retained mixed baseline is prospective primary,chosen after old results but before new
results. This is not independent model selection or fresh-seed confirmation and cannot relabel
C319. Both trained-policy cohorts remain fully reported. No Gate F promotion.

Science3420forwards/328320rows/13680core calls,training0,10strict loads,one parent bundle read,
new checkpoint0. Raw logit payload672399360bytes excludes overhead and is not peak RAM. Six
operational smoke forwards,recursive parent verification and regression are separate costs.

Mandatory user gates NOT executed here:46actual local parent archives/Windows protected bytes,
PowerShell ParseFile,real bilingual saved-model probes,full5221 inherited regression and all10
actual checkpoint evaluations. The review authorizes only the guarded launcher. Validate failure
skips science/publication;integrity failure repairs SAME C320 with fixed conditions. Valid new
primary failure is ACCEPTED VALID NEGATIVE. C321 waits for formal judgment. Old verdicts stay.
