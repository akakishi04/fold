# C280 acceptance and C281 saved support-intervention audit

## Formal verdict

C280 ACCEPTED VALID NEGATIVE. Both all_token_dual and evidence_only_dual passed 4/5 original
two-character subgates, 0/5 complete three-character subgates, and 0/5 whole-state gates.
The preregistered all-five evidence_only_dual candidate gate is False. Gate F NOT PASSED.

Scientific execution HEAD: 2c2eb8a86a03910ba9c63ff277c137d1e842a32f.
Published log commit: ae0a53cd8e0beb65ac4e1909edadecd51d833fdf.
Publisher log SHA256: a673ce8370a872c3be220691e9f672db52969aaf24bbbfef3f8cb2386bdd3403.
Publisher log bytes: 813504.
Git-normalized log blob: 3387b046ac4c3ab346a252952e67fbd5995c5ed7.
Summary: runs/c280-v5b-evidence-only-dual-bb662d609be24ad9a1fd20d4aef54174/summary.json.
Summary SHA256: 00410f3d879cb9571186e2ebf08a1ca9df0b31b64a639adae53f503c068bc7db.

## Execution validity

The prior manifest-seal error stopped operational Validate before science and published no scientific
attempt. This acceptance refers only to the subsequent run at the recovered execution HEAD above.

The published run attests precheck source526/protected926 and sealed manifest
c02aa9b88d7eeb9a7671674b982b5d7dad420c88cae10b4e40b4c6130219e1ac.
Own24 and focused3885 passed before scientific execution. The log reports 3885 tests in 276.948s.
All ten arms completed 800 updates. Registered science: 8000 updates, 384000 training rows,
9080 model forwards, 487680 row presentations, and 36320 core calls. The parent analyzer checks
matched initialization/batch identities, strict state replay and the workload before reconstruction.
The published tail reports persisted_evidence_dual_scores=PASS, protected inputs preserved,
tracked tree clean, execution HEAD preserved, and run_execution_valid=True.

This is an audit of published evidence and committed source, not an independent local re-execution
of the ten-model experiment. Publisher SHA/bytes above are publisher-reported transport identity;
the Git-normalized blob is a separate identity and must not be confused with Windows log bytes.

## Deciding metrics

|arm|two-character|three-character|whole-state|
|---|---:|---:|---:|
|all_token_dual|4/5|0/5|0/5|
|evidence_only_dual|4/5|0/5|0/5|

Seeds280001,280002,280003,280005 pass the two-character subgate in both arms.
Seed280004 fails the two-character subgate in both arms. Every seed/arm fails the complete
three-character subgate. These are full fixed-criterion gates, not pooled accuracy percentages.

## Scientific interpretation

Restricting direct attention key/value support to evidence positions is insufficient to satisfy the
registered reliability criterion with this training policy. The shared seed280004 two-character
failure cannot be assigned specifically to the candidate mask. It also does not justify dropping
that seed, changing LR, extending training or declaring a new optimization policy.

The published gate totals do not say whether evidence_drop failures were rescued, whether new answer
failures replaced them, or whether gains differ between shared-prefix and shared-suffix prompts.
The next experiment should reconstruct these paired transitions from saved C280 outputs, rather than
immediately introduce another architectural change.

## Confounds and non-claims

No capability win, no Gate F promotion, no claim that evidence support is irrelevant.
The intervention removes direct query-tail key/value reads; it does not remove fact information
already encoded in query states or the unchanged post-core residual. It is therefore not a complete
causal isolation of every query-mediated path.
C278 and C280 use different seed cohorts; their 5/5 versus 4/5 two-character rates are not a matched
mask-effect comparison. Use the two C280 arms for the paired contrast.
Failure counts for multiple criteria can overlap on the same evaluation cell and are not independent
samples. C281 must report both rescue and newly introduced failures, not only net differences.

## Accepted artifacts

- architecture-plan.json: c02aa9b88d7eeb9a7671674b982b5d7dad420c88cae10b4e40b4c6130219e1ac; 3371 bytes.
- dataset.json: 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1; 36024 bytes.
- triple-dataset.json: 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73; 158236 bytes.
- trained-models.pt: cf628e8505d371ce298778e697bbb72f8df48708b80306a2ab17c1f4d30c4d6f; 1238071 bytes.
- evaluations.pt: 7d3db012ef8288a336b9327a57876beb023f31d0c716e2650e08ed36ab2193de; 106277991 bytes.
- measurements.json: a5d55cf9914f2a4168b7ffc12c56e4d291ceb8c94736f958a8a8f69893477ecc; 525082 bytes.
- validation-summary.json: bf13ebb24d23c90b8b317b6df7294b5eaef5f3df5c854e10f77aacf57d263f19; 23004 bytes.

## Next question, not activation

For the accepted C280 paired outputs, which fixed-criterion failures does evidence-only support rescue
or introduce, especially for shared_suffix2, and how much of the residual is shared seed280004
failure rather than a candidate-specific regression?

C281 should verify all C280 artifacts and replay saved scoring with neural Module calls blocked,
then reconstruct all 2160 fixed records, matched criterion transitions, seed/split/profile views,
normal and reconstructed ablated accuracies, and mask-only versus answer-involving failures.
All five seeds remain in the primary result. A supplementary 280004/rest partition is a post-C280
explanatory stratum, never seed exclusion or a revised capability gate.
Zero training, zero model forwards, zero model-state loads and zero new checkpoint writes.
PASS means diagnostic integrity only. C281 requires separate preregistration, implementation,
committed-byte review and runtime Validate. C282 NOT REGISTERED.
