# C321 formal acceptance — valid negative

C321 ACCEPTED VALID NEGATIVE. Both mean_last and last_only are0/5 on the registered
interior-name-order capability gate. C320 bounded PASS and all earlier verdicts remain.
Gate F NOT PASSED. C322 NOT REGISTERED at this acceptance commit.

## Evidence identity and execution validity

Scientific execution:a31d5c5389f41cdb137b0bf375b7c7a99d8fb882.
Published log commit:b4e1686971d8d4a6d988a7f0e5e02a80cea6ec41.
Log SHA256:44c54ed61f481a82f5e683d10563750073821a56ffedaad462034d4d49cd4456;960689bytes.
Summary:runs/c321-v5b-interior-order-ef98962d405b402ba3926a6d1c2625b2/summary.json.
Summary SHA256:0e95c700cbac90025beb7baf1d65413cb1694de72b659540c2eb901f77f52fd9.
Own24/full5245 PASS;full5245 completed927.170s with0failures/0errors/exit0.
Scientific module returned normally with exit0/0x00000000;statusFAIL is its capability result.
All10 frozen states completed before/interior/after. Every original replay error0.0;
all_replays=True,persisted_interior_order=PASS,run_execution_valid=True,clean tree/HEAD preserved.
Source772/protected1455;no training. Publication changed latest.json/latest.log only.

## Deciding aggregates from all20 final partitions

mean_last:TRAIN1500/2880,HOLDOUT711/1440,total2211/4320 (51.1806%).
last_only:TRAIN1546/2880,HOLDOUT746/1440,total2292/4320 (53.0556%).
mean_last collapsed query pairs1996/2160;last_only1951/2160. These counts sum the original
collapsed_pairs field,not a new decoder or a different gate. Every state and both splits fail
the original full gate. 0/5 does not mean0% accuracy;neither pooled accuracy nor the comparison
cohort can replace the registered primary. Only the finite new name patterns were evaluated.

## Interpretation and recovery closure

The existing models do not reliably transfer to same-length,same-endpoint,same-character-count
names with different interior order. This is a much larger failure than the few six-character
errors. It does not invalidate C320 or prove that the architecture cannot learn order.
Internal hidden representations have NOT been measured by this experiment. Shared argmax
answers are not proof of identical logits,probabilities or internal states.

The prior scientific interruption did not recur after diagnostics were added. Its root cause
remains UNCONFIRMED. Preserve failed attemptcaaa42ac45a332c8b946714919eda58c38533384 and recovery
documents;normal completion does not retrospectively identify an OOM,thread or hardware cause.
Do not rerun C321.

## Next proposed diagnostic,not registration

Use saved C321 logits to compare the paired queries for each identical two-fact context.
Contrast full256-class output differences,offset-invariant differences and the direction of
relative preference between the two true value classes. Compare new interior names with the
saved original four-character controls,retaining all10 states and all profiles/languages/splits.
No new inference,training or restricted-value answering. Equal argmax versus genuinely weak
query-dependent discrimination must be distinguished before attributing the failure to a
specific representation or selecting the next learning intervention.
