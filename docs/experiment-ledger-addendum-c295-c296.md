# C295 formal acceptance — valid negative

## Formal verdict and evidence identity

C295 ACCEPTED VALID NEGATIVE. The preregistered ce1600 candidate passes2/5 quad gates,not5/5.
CE800 passes1/5. Gate F NOT PASSED. Do not rerun or extend C295 after observing these results.
Scientific execution HEAD:c5ba373c0ed7e4699adc06cd2aac44624b4330e8.
Published log commit:e213d8b56093f9ef37b1d9aeafc1d0fcd4f209d0.
Published metadata log SHA256:89e2cba2d8cd23a79afc054aeb7a770aa33c070689c96313dc13217fdf007b6b;751004 bytes.
Summary:runs/c295-v5b-ce-budget-2361f7495977449a9c95d5dfff51d6ad/summary.json.
Summary SHA256:ea6e10cc0d0371b3dbf11316f37a794b97a7dbd1889053ce771644e9e96f10a5.
Manifest:b35abbf4b55aa4b4722678ea26a558ce9ef3117c839257b6185fd4312c601a7f.

## Execution validity

Own32 and focused4421 passed;the preflight completed before scientific execution.
Five uninterrupted1600-update trajectories produced10 fixed snapshots. Actual train_steps8000,
training_rows384000,model_forwards9620,row_presentations539520,core_calls38480.
common_trajectory=True;persisted_ce_budget_scores=PASS. Final log reports tracked_tree clean,
execution_HEAD preserved,run_execution_valid=True. This is not a runtime failure.
Source616/protected1116 and the exact original masked/full scoring/replay contracts were retained.
The review uses published evidence;user-local tensor archives were not independently rerun here.

## Deciding metrics

In ce800/ce1600 order:quad1/2,two_char3/3,triple3/3,all_tasks1/2,
fitted_train_direct3/3,seen_holdout_direct3/3.
295001 passes both checkpoints;295004 changes from quad FAIL to PASS. 295002/295003 fail TRAIN,
seen-length HOLDOUT and quad at both times. 295005 passes seen tasks but fails quad at both times.
No formerly passing quad seed is lost,but only one additional seed passes.

295004 quad normal answers:ce800 TRAIN576/576,HOLDOUT287/288;ce1600 both perfect. Thus its new
pass resolves one normal HOLDOUT error,not a wholesale rescue of a failed training trajectory.

295002 TRAIN two/triple correct530/528 ->532/534 out of576. HOLDOUT two/triple/quad correct
167/169/168 ->163/158/152 out of288. The extension does not reliably improve this trajectory.
295003 TRAIN two/triple correct531/530 ->527/528 out of576. Its two-character HOLDOUT NLL
increases4.94217856826785 ->5.64062820253469 despite correct count105->110/288.
Report accuracy and NLL separately;neither train-step loss nor aggregate accuracy replaces gates.

## Interpretation and limits

A fixed doubling of ordinary CE's training budget rescues one near-complete quad case but does
not eliminate persistent failures on already-trained inputs. This does not establish a general
training-time law,model-capacity impossibility,or equal-compute superiority. The paired checkpoints
are dependent observations from five trajectories,not ten independent seeds. C294's oracle
conditional metric remains diagnostic only. No old gate is relaxed and no model is adopted.

## Immutable output receipt

- architecture-plan.json:2761 bytes;b35abbf4b55aa4b4722678ea26a558ce9ef3117c839257b6185fd4312c601a7f.
- dataset.json:36024 bytes;1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
- triple-dataset.json:158236 bytes;432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.
- quad-dataset.json:172066 bytes;86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.
- trained-models.pt:1238007 bytes;24f7983cabf6f0845de5866e685f3f6a08649a3b92d7e72bd0242aa077799f73.
- evaluations.pt:159485135 bytes;9b7a7fd8cec297a02a489508c775aa86c676a10abc323bef9e6665c8124c47d5.
- measurements.json:788445 bytes;aaf116e6a81d6169650633309a17d80d690eab8e1b2a900aece5ed1644794589.
- validation-summary.json:66441 bytes;626faa71d03ba592ceda1e8af1331ccd92960c0ed696c1742ecb48038f95d028.

## Next question,not registration

Before changing the architecture or extending again,test batching of the existing training
renderings:at an equal800-update budget,does balancing all six length/profile combinations
inside minibatches improve reliability versus the existing rendering-homogeneous batches?
Use fresh paired seeds,ordinary CE,identical initialization,exact same rendered-example multiset
in each complete24-update block,and identical final8 updates. No new data or loss information.
This tests a batching/order policy,not proof that catastrophic forgetting or gradient conflict
caused C295 failures. C296 must receive separate preregistration,implementation and committed-byte
review before activation. C296 NOT REGISTERED in this acceptance commit;C297 NOT REGISTERED.
