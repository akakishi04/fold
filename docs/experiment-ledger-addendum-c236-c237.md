# C236 acceptance and C237 frozen signal-path boundary

## Formal verdict

**C236 ACCEPTED VALID NEGATIVE.**
C235 remains ACCEPTED PASS for diagnostic integrity only; C234 remains ACCEPTED VALID NEGATIVE.
Gate E PASSED; Gate F NOT PASSED.

Scientific execution HEAD: `0bc91722ca27803f065d2458505b502a2d01e50f`.
Published log commit: `46e453a7e3900085002479791c6544b8669b9cf0`.
Published log SHA256: `784bba560a4b9a9d168def96314ef9da36df4d9594d913ed526b1e0f297a92e8`.
Log bytes: 525683.
Summary SHA256: `0e8628e048cc34e5b43104c0228c65fe18baee216c295223b0caa14c827327ec`.
Local summary: `runs/c236-v5b-minimal-binding-9cc3975f1c304ea893b8b53104ee8f71/summary.json`.

The published log commit is one commit after the scientific execution HEAD and changes only
`docs/experiment-run-logs/c236/latest.json` and `latest.log`.
Acceptance is based on that published evidence and its recorded user-local artifact postcheck,
not an independent reviewer rerun of the six trained checkpoints. The log digest is the publisher's
recorded digest; do not represent a partial log read as an independent full-byte hash verification.

## Execution validity

24 own tests PASS in 1.675s. 2833 focused tests PASS in 60.430s.
Python syntax, source/artifact precheck and executable C234/C236 training-AST parity PASS.
262 source pins / 382 protected inputs.
Six fresh models completed 400 steps each: 2400 total training steps / 76800 answer presentations.
All evaluation/reload calls completed: 2454 total model forwards / 77664 total row presentations.
All checkpoint and prediction replays passed; all weights changed; initial fingerprints matched
registered C234 initial states. Postcheck preserved tracked tree and execution HEAD.
`run_execution_valid = True`, `all_replays = True`, `all_weights_changed = True`.

Scientific `status = FAIL`, `full_probe_gate = False`, `gru_probe_gate = False` is a valid ability
miss under the registered recipe, not an execution defect. Do not rerun C236, extend its training,
select favorable seeds or relax any threshold to turn it into PASS.

## Deciding metrics

All 12 seed/family/language cells have the same decisive results:
- exact TRAIN accuracy 0.50 = 4/8;
- fact-pair both-correct 0.00 = 0/4;
- query-pair both-correct 0.00 = 0/4;
- evidence-mask accuracy drop 0.00;
- query-mask accuracy drop 0.00.

| Seed | Full EN NLL | Full JA NLL | GRU-only EN NLL | GRU-only JA NLL |
|---:|---:|---:|---:|---:|
|234001|0.706943|0.707664|0.702236|0.705506|
|234002|0.731304|0.730583|0.725732|0.723517|
|234003|0.703373|0.703610|0.700514|0.701477|

NLL values above are the logged six-decimal values, not additional-precision measurements.
Registered accuracy >=0.90, fact/query pair >=0.80 and evidence/query drop >=0.35 all failed.
The single-digit exact task remains scored over all 256 output byte classes, not a restricted
0/1 answer picker. Do not call the observed 50% a formal random-chance test.

## Scientific interpretation and non-claims

Restricting training from 384 rows to the selected balanced 16 existing TRAIN rows did not establish
even seen-prompt fitting for either fixed architecture at the 400-step budget. Failure cannot be
described only as difficulty on held-out rows. It does not prove architecture-wide impossibility,
that more optimization cannot work, or that a named module caused the failure.

Zero change in accuracy after masking is NOT proof of zero change in logits or intermediate
representations. Nonzero hidden responses could still be too small, misaligned, or mapped to the
same winning output. The prior conversational phrase 'minimal binding ability exists if C236
passes' was stronger than the preregistered boundary: even a C236 pass could have been memorization
of 16 prompts, not demonstrated general binding. The actual negative supplies no such positive claim.

No Full-versus-GRU superiority conclusion, useful-language claim, generalization claim or Gate F
promotion follows. C234/C235 evidence and verdicts remain unchanged.

## Accepted artifacts

- measurements.json: `19d24911d53e08898324514fedaafc32f27168f1526f9958b1572481cf957971` (9505 bytes)
- probe-dataset.json: `bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c` (2654 bytes)
- probe-plan.json: `86f534a54964a31d0139d5a3ceb3ef4b5e3c2ab46667adb002390a5b5d347957` (2669 bytes)
- trained-models.pt: `90c711f1609b77d426395446e9e7757b2a897c6e2372322fabe3c16cf5f6fc45` (601940 bytes)
- validation-summary.json: `a1e46ad4b0373daf6c1a920edc1ec8b7be5f9ab7f6c56490a9baa89062232042` (297 bytes)

## Next question

Freeze the six accepted C236 final models and inspect whether factual/query changes remain
numerically distinguishable from input tokens through the causal encoder's EOS state, the actual
readout input/output and output logits, even when the selected answer does not change.
Use paired query changes, paired value-assignment swaps, and fact-order reversals as separately
reported contrasts. This is descriptive signal-path localization, not causal attribution.

Keep all weights, prompts, targets and three input views fixed. Passive capture must reproduce
an uninstrumented run and the saved C236 final predictions/metrics. Do not train, select a new
checkpoint, change the architecture, or define a post-hoc ability threshold.

This acceptance document does not register C237. Its separate preregistration, authoring review
and authoritative handoff control readiness. Numeric-memory tuning remains paused.
