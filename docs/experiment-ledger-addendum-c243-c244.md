# C243 acceptance and C244 two-partner boundary

## Formal verdict

**C243 ACCEPTED PASS — diagnostic integrity only.**
C242 remains ACCEPTED VALID NEGATIVE. Gate E PASSED; Gate F NOT PASSED.
No new capability, independent replication, or internal causal mechanism is established.

Scientific execution HEAD: `1ff8bcfd4905b54c9f685eee26e197eb62394ab2`.
Published log commit: `8dbf3c9a2ed661b8b826243ee996aa1057b19eba`.
Publisher-recorded log SHA256: `53b5dbb8867f5f02dfd79225a0dd2e9fbf7541ef2ba98df5b6ab2e7d43784ace`.
Log bytes: 573039.
Summary SHA256: `adf53e7f0306ab9d3fa209f24fb4fa1dbdc3d717037a4e7931579e670acdd2ce`.
Local summary: `runs/c243-v5b-saved-recombination-audit-9a4a52f99ee2402dbbc3cb303935217a/summary.json`.

The publication is one commit after execution and changes only c243/latest.log and latest.json.
Acceptance uses immutable retrieved log ranges, publisher metadata and recorded user-local
postchecks. It is not a reviewer checkpoint rerun or an independent full-log byte rehash.

## Execution validity

24 own tests PASS in 0.276s; 3001 focused tests PASS in 90.778s.
304 source pins / 466 protected inputs. Python syntax, parent/source/artifact and discrete-metric
prechecks passed. The audit covered 1728 saved predictions, 576 normal rows, 5760 rule comparisons,
864 pair records and 24 diagnostic cells. Scientific model forwards, new training steps and
checkpoint loads/writes were all zero. NLL was not reconstructed from argmax bytes.

All discrete replays and persisted error-audit recomputations passed. Protected inputs, tracked
tree and scientific execution HEAD were preserved. `run_execution_valid = True`,
`diagnostic_status = PASS`, `capability_pass_claim = False`, `causal_claim = False`.

## Deciding counts

TRAIN has 192 normal answers overall: all correct. Correct binding and partner-of-other both
predict those same answers, so TRAIN cannot distinguish the two rules.

HOLDOUT category totals (each family contributes 192 answers):

| Category | Full | GRU-only | Combined |
|---|---:|---:|---:|
| correct |65|66|131|
| other supplied value |9|29|38|
| absent TRAIN partner of nonqueried value |99|67|166|
| absent TRAIN partner of queried value |19|30|49|
| byte outside 0..3 |0|0|0|
| total |192|192|384|

Thus 215/384 HOLDOUT answers are absent from their prompt, including 166/384 matching the
preregistered partner-of-other rule. This is 215 of the 253 wrong answers, not 215 additional
samples. The partner-of-other rule accounts for 99/192 Full and 67/192 GRU-only outputs; it is
not a uniform explanation of all models or all errors. Keep individual seed/language counts
in the original log and local diagnostics rather than interpreting the aggregate as 384
independent model-training trials.

## Interpretation and limitations

Wrong answers are predominantly absent digits, not just selecting the wrong supplied digit.
Many agree with the fixed TRAIN co-occurrence map 0<->1 and 2<->3. This is useful behavioral
localization, but not proof that a particular hidden layer or algorithm performs that lookup.
The four digit categories are exhaustive on this HOLDOUT; named-category membership alone is
not causal evidence. Full and GRU-only differences here do not establish architectural superiority.

The C242 training task allowed another entity's value to identify the correct value uniquely.
Masking both evidence values did not reveal this shortcut. The next task should make the
nonqueried value insufficient even when query identity and order are known. Removing one
registered shortcut does not establish that every possible shortcut has been removed.

## Accepted artifact identities

- audit-plan.json: 02f2420c59bfa7a232686ea42cf2ed47ee6c17ebe2714e81a2fbc169a8e70379 (2155 bytes)
- diagnostics.json: 054369ba51d66be1166fff873ded22d31e683141a534937f5cfb4f4341c47347 (8888 bytes)
- pair-audit.json: 67fcc06862d282150fc4f5f0815d88ae52a0928c4574c698292d4ed49fb2ed72 (160981 bytes)
- row-errors.json: 2a89dc0e500523718bd020948a328da0418a1080c90278ed712ff5e854516620 (231518 bytes)
- validation-summary.json: beb8da05e254bb9872e6a555318dd62ce6deecd9b4b3c1e20aa5a0c3ccd63e0e (313 bytes)

## Next question, not registration

Can fresh models learn held-out value-pair recombination when every TRAIN value has two possible
partners rather than one, at the same 400 updates, batch32 and total training presentations?

Preserve all existing box/book rows, both orders/queries/languages. TRAIN64 combines the original
matching {0,1}/{2,3} with the fixed second matching {0,2}/{1,3}, including both assignment directions.
HOLDOUT32 is the remaining matching {0,3}/{1,2}. Selection is fixed here before C244 results.

Alternate the two complete balanced 32-row blocks, original matching on update1 and added matching
on update2, through update400. Every block has balanced language/query/order/target counts; over
two updates every TRAIN row is seen once. Fresh initial weights, architectures and optimizer stay
fixed. Each retained row receives 200 presentations instead of C242's 400. Coverage and update
schedule change jointly; do not call this a one-variable causal attribution.

On the union TRAIN, a predictor given only language/query/order/nonqueried value can reach at most
50%, instead of 100% in C242. The old partner rule also reaches 50%. This is a finite-data ceiling,
not a model measurement. HOLDOUT remains unseen by the new model. It is a subset of C242's
HOLDOUT, so any comparison must rescore the old saved predictions on exactly that same subset,
not compare incompatible full-HOLDOUT averages. No NLL reconstruction from saved bytes.

No trained checkpoint reuse, threshold rescue, larger model, extra training presentations or
Gate F promotion. Separate C244 preregistration and committed-byte review control activation.
