# C276 operational preflight recovery — multi-parent hash fixture

## Status

C276 remains ACTIVE / NOT YET JUDGED. The first C276 invocation at activation HEAD
a5ce13504f6a1a6d77e262cde43766030908b922 stopped in Mode Validate during own24.
test_16_parent_loader_requires_exact_c275_pass raised ValueError:parent hash.
Scientific execution did not start and no scientific log was published.

## Root cause

C276.load_parent correctly verifies two distinct parent summaries:
-C275 summary SHA256:1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb;
-C274 summary SHA256:0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.

The own test fixture incorrectly used:
`audit.sha=lambda p:b.PARENT_SHA`
for both Path("p") and Path("q"). The first hash matched C275,but the second could never match the
registered C274 hash. The production loader was therefore behaving correctly;the test double did
not faithfully model the multi-parent provenance contract.

## Repair

-own test16 now returns parent hashes by path identity:
  - p -> PARENT_SHA;
  - q -> C274_SHA;
-it asserts that the loader queried p and q separately;
-it includes a negative case that deliberately returns PARENT_SHA for both inputs and requires
  ValueError:parent hash;
-no production scientific code,manifest field,architecture,data,optimizer,budget,seed or gate changed.

## Operational rule

docs/experiment-authoring-runtime-gate.md now includes a Multi-parent fixture fidelity rule:
-multi-parent loaders require independently modeled hash identities in own tests;
-single constant-return hash mocks are forbidden for multiple registered parent hashes;
-static review must compare the number of benchmark parent hash identities with fixture identities;
-a wrong-secondary-parent negative test is mandatory.

## Scientific invariants

C276 remains the same preregistered experiment:
-final_boundary architecture;
-fresh seeds276001..276005;
-lr0.005 control versus lr0.0025 candidate;
-identical initialization and batch order per seed;
-800 updates,CE-only loss and unchanged fixed gates.

The sealed C276 manifest remains unchanged:
312ed892ba64ef1b0289506d44d1e3da05eec6ee85e67b1d3b21cee282e18355.

Retry SAME C276 through Validate->Execute. C277 remains unregistered.
