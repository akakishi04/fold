# C190 acceptance / C191 handoff

## Formal judgment

**C190 — ACCEPTED PASS.**
**C191 NOT REGISTERED at this acceptance commit.**
Gate E remains **NOT PASSED**.

Successful C190:
- scientific execution HEAD: `b3d04dae6ed621deba987162b3d63c8f815bbe72`
- published log commit: `e47a6692ab7286f9f5ceecd4d987ad08a85ae25b`
- log SHA256: `32aa5642fa0f450103f6a93840bb4b40f31fb5d39a674df6aa0a5464c200a5ed`
- log bytes: 348500
- summary: `runs/c190-v5e-iterative-multimissing-fce03e62811c4166a11280c32ecfc534/summary.json`
- summary SHA256: `6902f97fd1fbcb1eb878884594a333ae41a0d35c83b872d287439386f7fabd59`
- focused regression: **1485/1485**, 74.098s
- source/artifact precheck PASS
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False; Gate E candidate False

## Deciding evidence

9 selector blocks x 9536 coherent-world episodes = **85824 episodes**.

All deciding scientific counters were zero:
- failed0
- initial_error0
- initial_replay_error0
- target0_error0
- selected_observed0
- first_acquisition_error0
- post1_error0
- target1_error0
- repeated_target0
- second_acquisition_error0
- post2_error0
- contract_error0

Live IO:
- first reads/publications: **85824**
- logical post1 NEEDS: **34948**
- second reads/publications: **34948**
- logical post2 NEEDS: **8352**
- total actual file reads: **120772**
- provider bytes read: **55555120**

Initial replay recovery succeeded exactly:
- unique initial policy rows: **15912 = 1768 x 9**
- initial forward calls:18
- shared-cell calls:126
- parent necessity argmax errors0
- parent target argmax errors0
- max necessity logit delta0.0
- max target logit delta0.0

Work:
- total base rows136684
- total target rows101736

Every selector had exactly **928 final NEEDS** after two acquisitions.

## Scientific interpretation

```text
initial multi-missing state
-> learned NEEDS + learned target0
-> real C172/C173 acquisition #1
-> actual state1
-> learned NEEDS/SUFFICIENT + learned target1 when needed
-> real acquisition #2 when needed
-> actual state2
-> learned necessity2
```

C190 establishes bounded two-acquisition learned information gathering over coherent complete
source worlds in the repeatedly inspected C174 development family. The same frozen C181+C188
components selected a new non-observed influential second target, drove real IO, preserved
runtime accounting, and reclassified the second actual state with zero error.

Non-claim:
- no third acquisition;
- no learned tool/provider choice;
- no arbitrary-length loop;
- no final independent holdout;
- no language/larger/repeated-variable generalization;
- no answer/proof;
- no Gate E completion.

## Next boundary

All remaining post2 NEEDS cases are in the missing3-origin path. After two successful
acquisitions, exactly one fact remains unobserved. Under the unchanged original internal
budget12, C190 ends phase2 with 3 internal units remaining. A third action+dispatch costs
exactly3, leaving0 and therefore no budget for a fourth learned decision.

C191 should test exactly this boundary:
can the same frozen components, with no resource increase, extend the loop by one third
learned acquisition, publish the remaining fact from the same coherent world, exhaust the
internal budget exactly, and stop without silently performing a fourth decision?

This keeps resource budget fixed; final learned sufficiency reclassification is intentionally
out of scope for C191.
