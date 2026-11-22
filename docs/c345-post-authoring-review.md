# C345 post-authoring review

Date: 2026-11-22 Japan time.
post_authoring_review = PASS
Review target HEAD:588586870562a8f930b7e2053dcf669ee8d0b650.
Source tree:2587c2ff0086f84257ca52ddf6393b123a42d5ed.
Sole parent/acceptance base:a7174ae51f71f001901793603ab9f7ddb26ed923.

## Independent remote-byte review

A reviewer who authored none of the seven C345 OWN files fetched each complete file
through the authenticated GitHub connector at the exact source commit and read it
through EOF. Remote commit metadata confirms the tree and sole parent. Every
computed blob,byte count and SHA256 equals the frozen author bytes. The source
commit adds exactly seven paths; no accepted source,test,launcher or preregistration
changes. The final nested token-bank fingerprint and all three test37 mutation
cases are present in the fetched files. No review blocker remains.

|Path|Bytes|Git blob|
|---|---:|---|
|fold_lm/v05_benchmarks/model_c345_saved_objective_audit.py|29786|8203e6e45d23d099a5da5bbd53443f6fc16f449e|
|tools/c345_execution.py|29030|9462d6e39dffecf7e49e6328d4b344b97e582413|
|tests_lm/test_v05_c345_saved_objective_audit.py|24770|5618224a1e8488ac784144965145d2e9eaab3a73|
|tests_lm/test_v05_c345_execution.py|34421|a94436824e2bd9bcd45c223c431eb243a9774cf4|
|tools/run_c345.ps1|966|110e487ad9a97e639e43a30f2105f73777f674af|
|tools/invoke_c345.ps1|3163|bc381384ba8ade67f08d8ad2992c0b481386b6ba|
|docs/experiment-ledger-addendum-c345-preregistration.md|13647|718e1c06c77ff8dd06fee92c6dcde26b0f8ee3e9|

## Author verification of those exact bytes

Combined science40+execution24=64 tests PASS in the Linux author environment:

|Condition|Tests|Seconds|Failures|Errors|Skips|Expected failures|Unexpected successes|
|---|---:|---:|---:|---:|---:|---:|---:|
|Normal text-open defaults|64|111.006|0|0|0|0|0|
|CP932 default text-open emulation|64|112.490|0|0|0|0|0|

Runtime:Python3.12.14/Torch2.10.0+cpu/NumPy2.3.5. These tests began with
acceptance HEADa7174ae51f71f001901793603ab9f7ddb26ed923 and the completed new files
present locally. All four Python hashes stayed constant during both tests and match
published source5885868. They are author checks on the published bytes, not claims
of a native Windows formal C345 run or tests starting after source publication.

The actual production loader/writer/reconstruction roundtrip is covered using
canonical data and explicitly invented saved logits/traces. Synthetic fixtures
stub the historical full-trace checker only where invented histories cannot claim
real training; separate dispatch tests require the production checker on all ten
states. The formal run never uses those patches. Mutation tests require analysis
to have run before rejecting changed trace values,tokens or even an empty family
container. Repeated/existing artifact writes fail; no retry or overwrite is added.

An initial author run found one tuple-key table fingerprint error in the production
roundtrip. It was repaired before the source commit. The final code represents
all arm/family containers and typed(slot,profile,tensor) entries as nested sorted
sequences for the accepted state hash. Both final64-test runs include this repair.
The earlier unsuccessful author run is not presented as a PASS.

## Mechanical inventory and static checks

UTF8/noNUL/import/compile and pyflakes on all four new Python files:PASS/0findings.
Free-global audit:267function/nested code objects,1764LOAD_GLOBAL,0unbound names.
The independent compiled-module walk counts273 objects when adding four module
and two class bodies; it yields the same1764global loads and zero unbound names.
No new inspect.getsource-dependent assertions are introduced. API arity is checked
with inspect.signature, and production loader/call-order tests exercise behavior;
no comment/docstring string match is accepted as evidence of that behavior.

The real helper/build_plan loader yields6579raw candidates,6578selected IDs and
241modules. Own40+24 methods append to the identical parent6514-ID/239-group prefix.
Only the inherited exact C204 mutable-ACTIVE exclusion remains; there is no new
exclusion,skip,mutable-state assertion or accepted-test edit.
Full ordered-ID SHA256:
2c40afb18970b97273869cf98ac1580d84c2df3050b20b07f3da9f53331cee2a.
Parent ordered-ID SHA256:
c5d7db147680f739c62bbbc2f12be324c66ba16ea108dc04beb3071f56abaaa3.
Counts are constructed from the loader,not source-string numeric literals.

Actual PowerShell7.5.4 Parser.ParseFile checks returned zero errors for
invoke_active_v2.ps1(864tokens),invoke_c345.ps1(494),run_c345.ps1(142),and the
standard short user block(92). The block's quoted ExpectedHead is replaced with
the later activation commit and parsed again before delivery. The dispatcher parses
its selected launcher; the launcher parses itself and runner before logging.
Branch,tracked-tree,ExpectedHead,unique ACTIVE and dependencies precede publication.
CLI argument names/order and module-index/plan hash are consistent.

## Scientific and parent semantics

Manifest seal5e69553fd6661ef46459883500fd719b474fd7cacbd17d002c957eb3fb2f1a9f
matches the code and preregistration. The study remains V5-B-SAVED-OBJECTIVE-AUDIT:
zero new neural/training work,all ten accepted C344 states,all6domains/bothsplits.
120terminal groups/60contrasts/51840answers/25920canonical pairs and24000trace rows/
12000paired steps/120blocks/180groups/60paired blocks/90paired groups reconcile.

Full256 CE/argmax uses canonical targets. Pair construction checks actual shared
metadata and counterpart queries; it is not an adjacency guess. All parent normal
counts/contrasts are bound exactly. All saved raw views and replay are validated.
The terminal mean is per domain/split,not an exposure-weighted global objective.
Slot4 is mixed original4/original5/interior4; event/length masks reconstruct actual
24-pair composition in both cycles. Batch losses are never assigned to one family.
Norm>1 is a threshold count,not exact clipping calls. Final logged minibatch losses
are preupdate,not final checkpoint full-set evaluations. No causal/optimality or
learned-then-forgotten claim is encoded. Diagnostic PASS cannot change C344's
candidatefalse/eligible2 capability result.

Parent identity is the actual trained C344 writer schema with valid execution and
scientific FAIL,not the old C343 diagnostic schema. Exact primary/envelope hashes,
C344-R1 receipt and parent outputs/proofs are bound. Parent semantics uses
semantic_recheck(out344,data_out,cx,read),four arguments,under no_neural. Child
run_diagnostic/recheck uses(out,parent_out,data_out,cx,read),five arguments.
The accepted native context/data loader is invoked by the real production path.

Every new deciding-path repository dependency is in the inherited C344 chain plus
seven OWN files. Lazy support/profile/schedule/readout validators are included;
no missing source pin was tolerated. Protection is937sources/8679inputs,including
all489parent outputs and481proofs. Native lease capacity8679 and all8679final
uncached rereads are explicit. No ancestor neural rerun or unlocked fallback.

## Execution and inheritance

The execution order is fixed:accepted R1six-case native preflight before expensive
leases/snapshot;immediate C344 semantics;6578isolated tests;zero-neural diagnostic;
saved reconstruction;all8679rereads;separate fresh verifier;console-log publication.
The C345-R0 envelope names timeout_cleanup_implementation C344-R1. The inherited
receipt retains its implementation schema but binds the child execution HEAD;
the parent receipt separately binds its original HEAD. Both are checked exactly.
Full regression modules reuse only the accepted scoped R4/R5 cleanup barrier.

Four local science artifacts plus primary/envelope and485regression proofs mean
491outputs for a successor. The proof count is3records+241JSON/log pairs.
Scientific load counters apply per child computation/reconstruction pass; they do
not collapse the separate parent validation,unit fixtures or fresh process into
one file read. Native runtime remains Python3.13.15/Torch2.10.0+cu130/NumPy2.3.5.

## Activation boundary

This PASS authorizes a documentation-only activation after the reviewed source
commit. Keep all seven OWN blobs unchanged. The authoritative handoff must contain
exactly C345 ACTIVE / NOT YET JUDGED and cite this source review. User ExpectedHead
is the later activation commit,not this source commit,the C344 execution/log,
acceptance commit or a main merge. Native formal C345 execution remains pending.
