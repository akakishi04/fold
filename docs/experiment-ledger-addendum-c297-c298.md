# C297 formal acceptance — crossed initialization/order diagnostic

## Formal verdict and evidence identity

C297 ACCEPTED PASS (training diagnostic integrity only). C296 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C298 NOT REGISTERED in this acceptance commit.
Scientific execution HEAD:18576c2df5f928d5904bd99bd39a2de58c5736da.
Published log commit:d541b5a370adbe4b80064294076d98be7c2a75d5.
Log metadata:719346 bytes;SHA25663373ead97249c2099668d11ecb494f3a07242812fd2e79d500b01763578d834.
The publication commit changes only docs/experiment-run-logs/c297/latest.json and latest.log.
Summary:runs/c297-v5b-init-order-1e8b2002a1e142db81c0c8b5d51a1b4a/summary.json.
Summary SHA256:9bfceee367a11edfe9ae5b62f381cdaf183ef357109f5dff7b345a11e3180aba.
Source blob:49497d433c6302cd2a65635564f254edbf169104.
Manifest:6fc874b494cdc0b9dea5c55b57e482ef8eca50cc9790abc62840cf29e52bb903.

## Execution validity

Own32 and focused4493 passed;the published regression reports4493 tests in596.652s.
Source628/protected1146;all9 registered cells completed800updates.
Grid matching,strict state replay and persisted reconstruction passed;tracked tree clean;
execution HEAD preserved;run_execution_valid=True. capability_gate_applicable=False.
No rerun or relaxation of any old capability criterion is authorized.

## Deciding observations

Rows are initial297001/297002/297003;columns are order297101/297102/297103.
Two-character and three-character task matrices are all True,with all normal TRAIN/HOLDOUT
answers correct in all9 cells. Four-character matrix is:
[[True,True,True],[False,False,False],[True,True,True]].
All four-character errors occur in the middle row in this finite grid. The other six cells
have864/864 normal four-character answers correct and all original masked/full gates passed.
Middle-row quad counts (TRAIN/HOLDOUT):566/576+280/288;576/576+287/288;565/576+281/288.
These are18,1,18 normal errors respectively. Thus equal FAIL flags conceal a substantial order effect.
The word TRAIN in the quad split refers to value combinations,not length4 training.

For quad HOLDOUT accuracy,the exact finite-grid decomposition has initial_ss0.0006858710562414245,
order_ss0.00011520490397804866,interaction_ss0.00023040980795610482,total_ss0.0010314857681755845.
It describes these chosen9 outcomes,not population variance,significance,or a universal cause.

## Interpretation limits and correction of conversational overreach

The observed full-gate pattern is associated with initial state in this fixed3x3 grid. It does
not establish that shuffle is irrelevant,that all historical failures have this cause,or that a
particular architecture change must follow. Seen-length/TRAIN failures from earlier experiments
were not reproduced here. Previous interventions were not proven irrelevant merely by missing
an all-five gate. Keep model capability distinct from diagnostic PASS.

## Next-question boundary

A separate C298 may decompose the SAME three initialized parameter sets into backbone versus
added reader components at one explicitly fixed original order. Include all three old initial
levels and all nine component combinations,not just the failed row. This is a targeted follow-up,
not an independent replication or permission to select a lucky model. Matching-component diagonal
cells should retrain from scratch and reproduce the corresponding accepted C297 trajectory;
o trained checkpoint splice or continuation. One order cannot establish order-independent effects.
C298 requires its own preregistration,code,tests,launcher and post-commit review before activation.
