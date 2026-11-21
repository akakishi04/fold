# C240 acceptance and C241 assignment-holdout boundary

## Formal verdict

**C240 ACCEPTED PASS — diagnostic integrity only.**
C239 remains ACCEPTED VALID NEGATIVE; C238 remains ACCEPTED PASS for minimal seen-TRAIN fitting.
Gate E PASSED; Gate F NOT PASSED. No new capability or causal mechanism is accepted by C240.

Scientific execution HEAD: `7bf66561cfb151a6ba2562791a1645b760ad6f1f`.
Published log commit: `24141d62cdb58be0d11ae3b57e35b5f0593c7e50`.
Publisher-recorded log SHA256:
`48066d34eee74c201dae7660fd32dd8b04bebedefd73547e745cfa51f8b24315`.
Log bytes:552807.
Summary SHA256:
`3551a5da3346381fdeb81b80a7cd297822ee51f64e80f9d966158ecf4c36b8b0`.
Local summary:
`runs/c240-v5b-saved-position-audit-4b604be67f5b47f0b18cabdb2513d12d/summary.json`.

The log publication commit is one commit after the scientific execution HEAD. Acceptance uses
published execution/postcheck evidence and retrieved log ranges, not a reviewer rerun of user-local
models or an independent complete-byte rehash of the console log.

## Execution validity

24 own tests PASS in0.104s;2929 focused tests PASS in112.356s.
Python syntax/source/artifact/discrete-parent-replay prechecks PASS.
286 source pins/430 protected inputs.
No new training, model forward, checkpoint load or checkpoint write occurred in the scientific
C240 audit. 288 saved predictions,96 normal rows,576 rule comparisons,48 matched order pairs and
24 diagnostic cells were processed. All discrete parent metric replays and persisted audit
recomputations PASS. Protected inputs/tracked tree/execution HEAD were preserved and
`run_execution_valid=True`.
`diagnostic_status=PASS`, `capability_pass_claim=False`, `causal_claim=False`,
`nll_recomputed=False`.

## Deciding measurements

Across all6 models x2 languages, TRAIN contributes48 normal rows and HOLDOUT48.

TRAIN:
- correct entity answer:48/48;
- query_fixed_position match:48/48;
- other_entity:0/48;
- outside_supplied:0/48.

HOLDOUT:
- correct entity answer:4/48;
- query_fixed_position match:44/48;
- other_entity answer:44/48;
- outside_supplied:0/48.

For all48 matched TRAIN/HOLDOUT order pairs:
- same saved normal answer:4/48;
- both correct:4/48;
- both match the query_fixed_position rule:44/48.

The fixed-position rule is behaviorally degenerate with correct entity binding on TRAIN and with
the other entity's value on this binary HOLDOUT. Therefore44/48 agreement is a strong descriptive
fit to the preregistered shortcut rule, but it is not proof that the model internally executes
that rule.

Always-first/always-last and constant-digit matches vary by cell and do not provide a single
uniform explanation across all rows. No HOLDOUT normal answer falls outside the two supplied digits.

## Scientific interpretation and non-claims

C239's errors are strongly consistent with a position-linked shortcut: when fact order reverses,
44/48 saved answers are exactly the other entity's supplied value and also match the fixed
query-to-position rule. This sharpens the behavioral diagnosis from C239.

It does NOT identify an internal algorithm, prove that a particular layer encodes positions,
or show that position is the unique cause of the earlier failure. Multiple internal functions can
produce the same bytes. The binary fixture creates explicit identifiability degeneracies.

C240 does not repair/invert any answer, rerun C239, recompute NLL from argmax bytes, claim
general-language competence, establish Full/core superiority or promote Gate F.

## Accepted artifacts

- audit-plan.json: `31d2b0579d65b354979ef1d98e3012a57a95820e2f12cd729c931c8d8525bc25`
- diagnostics.json: `3db440f1348746bbdee122abd404fa7894cca9a9cc5a7abd8d688735c575be8e`
- paired-orders.json: `4e9bb61c419a9f710374261f8b5c95fd5414ce254fb2a7d5b1963ca88bc9fc6f`
- row-audit.json: `bffbba05c1625ff8375867a7642c9087ba6edcc901fa31214e2b396a87bf2d4e`
- validation-summary.json: `ba79501874430b2967db3e2c57cf9bd8abe8cae0258e6827ff1b92e7b716a66e`

## Next question — assignment holdout after breaking the position shortcut

Use fresh models and the same16-row pool, but TRAIN only on the [0,1] value assignment while
including BOTH fact orders, both queries and both languages (8 rows). HOLDOUT the swapped [1,0]
assignment while also including both orders/queries/languages (8 rows).

Because each queried entity occurs in both rendered positions during TRAIN, the C239
query-to-fixed-position rule cannot solve all TRAIN rows. Conversely, because TRAIN uses only one
assignment, a fixed entity-value lookup (box->0, book->1 and Japanese equivalents) can fit TRAIN but
must fail the swapped HOLDOUT. Thus a HOLDOUT pass would rule out those two simple behavioral
shortcuts on this bounded fixture; it still would not prove a unique internal binding mechanism.

Keep fresh initial states, architectures, optimizer,400 updates,batch32 and complete-cohort policy.
Each TRAIN row appears4 times/update. Evaluate HOLDOUT only after the training endpoint.
Score exact accuracy, query-pair both-correct, order-pair both-correct, and inherited evidence/query
mask drops. Fact-swap pairs do not exist within an assignment-fixed split and are not fabricated.

This acceptance document does not register C241. Separate preregistration and post-authoring
review control activation. Gate F remains NOT PASSED and numeric-memory tuning remains paused.
