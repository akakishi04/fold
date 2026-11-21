# C308 formal acceptance — bounded capability PASS

C308 ACCEPTED PASS. All five core_slow candidates pass every registered five-character criterion.
This is a capability PASS within the registered task,not diagnostic-only PASS. Gate F NOT PASSED.
C307/C306 remain ACCEPTED VALID NEGATIVE. C309 NOT REGISTERED in this acceptance commit.

## Evidence identity and validity

Scientific execution HEAD:2fc902e8c7f57579087a61e25e7c1e88f8c66090.
Published log commit:045de9e384e6d19f35b48722a55b3fac1062ddbd.
Publication changes only docs/experiment-run-logs/c308/latest.json and latest.log.
Metadata log SHA256:3e6c4612c1237fc98414b7ae799e86a9bb230d2c412e81bfcdaebecff72a1167;806750 bytes.
Summary:runs/c308-v5b-core-lr-02b24ac7b9da4a36a14a5545bd42aab6/summary.json.
Summary SHA256:42a2dbc75c6bf958bff26315f918fc999728196eac7fe890eee28aa392f63c8a.
Manifest:c13d8d4ed974f977840e7cc1d84d5d60e3bfc78bdbc9384ff1f5d4906f65210f.
Own32/focused4877 PASS;focused suite1177.183s. Source694/protected1295.
All15 fits and frozen final evaluations/strict replay complete;all_groups_matched=True;
persisted_core_learning_rate=PASS;tracked tree clean;execution HEAD preserved;run_execution_valid=True.
Configured/received gradient parameters full14256,frozen10928,slow14256. No C308 rerun required.
These conclusions use the published immutable console receipt and postcheck,not direct access
to the user's ignored local tensor files. Those files were checked by the authoritative runner.

## Deciding results

For every evaluated length2/3/4/5:full_train4/5,core_frozen5/5,core_slow5/5.
All-length passes likewise4/5,5/5,5/5. Fitted-TRAIN direct5/5 in every arm;
trained-length HOLDOUT direct4/5,5/5,5/5.
All15 per-seed flags are positive except full_train308002,which fails each length but fits TRAIN.
Against full_train:candidate both-pass4,candidate-only1,control-only0,both-fail0.
Against core_frozen:both-pass5,all discordant/both-fail counts0.

For308002,full_train normal HOLDOUT correct counts at2/3/4/5 are77/79/80/81 out288,
while both frozen and slow answer288/288 at each length. Its TRAIN partitions are576/576.
Thus this is a substantial unseen-value-combination rescue,not merely a threshold-near single error.
There is no evidence of pass-count superiority of core_slow over core_frozen in this cohort.
Do not infer wider language capability,arbitrary-length transfer,optimal learning-rate ratio,
core necessity,or universal reliability. The same fixed templates and datasets have been reused.

## Next decision boundary

A separately preregistered fresh-seed replication should retain ALL THREE policies,ratio0.1,
1200 updates,2/3/4 training,unseen5 evaluation and the original local/masked gates. Change only
initialization/order seeds and bookkeeping identity. No favorable seed reuse,old checkpoint reuse,
ratio tuning,additional lengths or pooling old/new counts to replace a new all-five primary gate.
Even another5/5 is not superiority over an equally successful frozen control or Gate F completion.
Do not repeat seed searches until success. C309 requires its own committed-byte review and activation.
