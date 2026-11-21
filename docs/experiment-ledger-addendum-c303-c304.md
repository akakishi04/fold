# C303 formal acceptance — valid negative

C303 ACCEPTED VALID NEGATIVE. residual_stop passes0/5 quad gates,not the preregistered5/5.
full_train passes3/5;core_frozen passes4/5. Gate F NOT PASSED. C304 NOT REGISTERED in this commit.

## Evidence and execution identity

Scientific execution HEAD:8e01ac5bb1dae57f129615731b7013eed43b5719.
Published log commit:726d43f4236f5128d88c3e38dfe77de4988c73b7.
Publication changes only docs/experiment-run-logs/c303/latest.json and latest.log.
Log SHA256:d50e96ddef4e2ec98bdc35ea72d1cb0286e65e5a43724930b028d2296fec71f4;767025 bytes.
Summary:runs/c303-v5b-gradient-route-ef832a6117c44389aa035cd16c76be70/summary.json.
Summary SHA256:33d3370d383d8f220cea46056cb0fefdae27498794110fb7672bca726bc45d01.
Manifest:265067d9ca156f5181b6275ce4274ffee919751bcf1cd395b470656bce163ad7.

Authoritative Validate completed before Execute. All15 models finished800 updates.
Own40/focused4709 PASS;source664/protected1228. Saved reconstruction PASS;all_groups_matched=True;
tracked tree clean;execution HEAD preserved;run_execution_valid=True. The FAIL is a valid
capability negative,not a broken run. Do not rerun C303 or retune its fixed conditions.

## Deciding measurements

Counts full_train/core_frozen/residual_stop:
- two-character full gates4/5/4;
- three-character full gates4/5/4;
- four-character full gates3/4/0;
- fitted seen-length TRAIN direct4/5/5;
- seen-length HOLDOUT direct4/5/4.

full_train quad passes303003/303004/303005. core_frozen also rescues303001,not303002.
residual_stop passes no quad gate and loses seen-length HOLDOUT gates on303004.
303001 full_train normal two-char TRAIN526/576,HOLDOUT222/288;core_frozen576/576,288/288.
Both frozen-core arms fit all seen-length TRAIN direct criteria,but residual_stop does not
retain core_frozen's transfer results. 303004 residual_stop HOLDOUT two285/288,triple285/288,
quad287/288 versus core_frozen288/288 in all three. These failures can be small in counts;
zero passed models does not mean zero correct answers.

The recorded gradient-receiving parameter union is14256 for full_train and10928 for each frozen
arm in every seed. The frozen core fingerprint is unchanged;full_train changes its core.
These are different backward policies,not inference-time branch deletion or matched backward FLOPs.

## Interpretation boundary

Stopping the residual's backward signal is not adopted. Merely freezing core performed better
than the candidate on this cohort,but4/5 and one fresh five-seed comparison do not establish a
universal replacement policy or core irrelevance. Do not explain this as proven gradient conflict.
All original masks,local criteria and old negative verdicts remain unchanged.

## User-requested next axis

The user proposed training identifier lengths2/3/4 and evaluating unseen5. Prior advice overstated
what such success alone could establish:it would not prove a length-independent rule or identify
which representation change is needed after failure. Maximum trained length,total exposure and
profile composition must be controlled;do not compare different seed cohorts' pass counts causally.
Prepare a separate comparison of4-only,3+4,and2+3+4 at common maximum length4 and1200 updates.
Use ordinary full CE learning in all arms,not the better C303 control selected after results.
The proposed5-character Japanese strings require52 UTF-8 prompt bytes,exceeding the existing
48-token frame once special tokens are included. No silent truncation,language removal or
HOLDOUT leakage is allowed. Audit the model/input capacity path before registration and use a
common verified context for all arms. C304 requires its own committed-byte review and activation.
