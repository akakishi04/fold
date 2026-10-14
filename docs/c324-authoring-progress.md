# C324 authoring progress - TRAIN template selection component

Status: PARTIAL IMPLEMENTATION ONLY. Not a preregistration, not ACTIVE, not an
executable scientific C324. C323 acceptance and all scientific verdicts unchanged.
Starting point: 88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf.
Authoring branch: work/c324-training-templates.

## Implemented

`fold_lm/v05_benchmarks/c324_training_templates.py` implements the actual paired
TRAIN-template selection. The original arm returns the original nine length/profile
tables. The interior4 arm changes only the three length-four tables, with the fixed
repeat/shared_prefix/shared_suffix to u_dominant/balanced/v_dominant slot mapping.
Both retain source IDs, logical targets, row order, table sizes and length-two/three
strings. The original arm never accesses interior input. Masked views are excluded
from the returned strings. Results use frozen metadata and immutable table values.
The helper validates alignment and basic logical row semantics; it does NOT replace
upstream canonical artifact/hash/source checks. It neither trains nor runs a model.

Writer contracts checked by reading accepted source at the starting commit:
- C304.prompt_dataset: source_id/target/views records, length->split->profile lists;
- C321.new_prompts: source_id/target/views records, split->interior-profile lists;
- C321.render: fact permutations and query identity retained in generated strings.
The component consumes TRAIN-only projections, not complete evaluation containers.

## Checks actually performed

Python 3.13.5, Linux, isolated component workspace; no installed repository snapshot.
`python -m unittest discover -s tests_lm -p test_v05_c324_training_templates.py -v`
20 tests run, zero failures/errors, 0.006 seconds, exit 0.
UTF-8 decoding, no literal NUL, Python AST parsing and compile checks passed.
Synthetic writer-shaped fixtures cover both languages, both queries and both fact
orders. They do not represent the canonical 192-row TRAIN archive or a neural run.

Local tested source Git blob: 16d77bdc65971eb3cddf054da778096619b2eed9.
Local tested test Git blob: bd74d754560745932847a674ac974f57df45e13c.
These hashes describe the exact local files; compare committed remote blobs before
claiming a remote-byte review. This document does not declare that review PASS.

## Still required before registration

Complete the C324 benchmark with fresh paired initialization, fixed schedules,
TRAIN-only tensor construction, native mean_last in both arms, fixed-budget fitting,
original/interior evaluation, masked controls, paired-effect gates, artifact persistence,
checkpoint replay, all ancestor hashes and complete deciding-path source protection.
Include this new helper in that protection; it is not part of the inherited 784 pins.
Add production-path tests and extend the exact historical regression suite without
new exclusions. Freeze exact seeds, workload, counts, thresholds and schemas in the
preregistration, then create runner/launcher with PowerShell parse and stale-state
guards. Re-fetch committed source for independent post-authoring review. Only after
review PASS may the authoritative handoff activate C324 and issue an execution HEAD.

No complete-regression, real-parent-archive, model-learning, PowerShell launcher or
full experiment post-authoring review success is claimed by these component tests.
