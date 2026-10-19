# C332 acceptance -- trained first/mean query remains a valid negative

Date:2026-10-19 Japan time.
Formal verdict:C332 ACCEPTED VALID NEGATIVE. Scientific status FAIL;execution valid.
C331/C330 remain diagnostic PASS,C329 remains VALID NEGATIVE,Gate F NOT PASSED.
No first_mean adoption,no seed selection,no retry of the accepted C332 cohort.
C333 is not authorized by this acceptance;separate authoring/review/activation required.

## Exact evidence identity and review limits

Scientific execution:6a13f1e6a10cee4fad519853835fd256089456e8.
Published log commit:b587b47021bb8c03709591c643b8cbf6e0ade32a;sole parent is execution.
Metadata reports222470original Windows bytes;SHA256
fb5efdd82c9b1934588f0603b7d01c255d86e09b8a269690add6539007d444a1.
Log blob:f9a88e789d6aa8470cd9185ce3ff0b4155cbbd37.
Metadata blob:83ec8ef5c5cd35a2b0afab3731a401c22e939c35.
Paths:docs/experiment-run-logs/c332/latest.log and latest.json.
Remote review inspected exact-ref startup,regression completion,training progress,
all10seed results,all5paired comparisons,and terminal fresh verification. Deciding
counts below are sums of printed records. This does not claim independent rehashing
of the entire Windows log,local model replay,raw-logit recalculation or reading all
222local module receipts. Native executor/fresh verifier report those integrity checks.
Old attached C323/C324 logs are not current evidence.

Full5946tests/222modules PASS,0failures/errors/skips,1641.320seconds including process
orchestration. Ordered-ID SHA:
3e801a1c8f0ffcd9fb9aab46a5377a823fc76e98584ac0b4fe6558ec5da66855.
Native parent/read-lock checks,853source/2508input registration,TRAIN preflight,
5paired initializations,10final states,10same-policy replays,24000updates,saved
reconstruction and ALL2508final uncached rereads passed. Science/regression/verify
exit0;scientific_status=FAIL;persisted_trained_readout=PASS;run_execution_valid=true.

Local folder:runs/c332-trained-query-853335f262f5409e8d84c17da3809167/.
Primary science/summary.json SHA256:
478ea25268291aeec1c73c4169a0b4a5f04f45950054214ec8eec0e190f3b89d.
Mandatory execution-envelope.json SHA256:
d6343c4ad4c7149b118183a928810d80215ffac37891b0c6a0282d6ae75f982f.
Scientific manifest:2a216840891fcc13c98890d525a23054e074d88464cf546223dd693f4cb50874.

## Fixed-gate decision and deciding counts

All counts below pool five paired seeds332001..332005,not independent new tasks.
Each HOLDOUT domain has1440answers/720query pairs.

|Domain|Native answers|first_mean answers|Native pairs|first_mean pairs|
|---|---:|---:|---:|---:|
|original2|1440|1440|720|720|
|original3|1440|1440|720|720|
|original4|1440|1440|720|720|
|original5|1440|1428|720|708|
|original6|1405|1412|685|696|
|interior4|1440|1415|720|696|

Original6 gains+7answers/+11pairs;24rescued/17regressed answers and24rescued/13regressed
pairs. Original5 loses12answers/12pairs;interior loses25answers/24pairs. Original2..6
answer sum7165->7160/7200. Including interior,overall answer sum8605->8575/8640.
These sums are descriptive;no pooled average replaces the preregistered seed gates.

|Seed|Six answer gain|Six pair gain|Original2..5 gain(answer/pair)|Interior gain(answer/pair)|Candidate full gate|
|---|---:|---:|---|---|---|
|332001|+3|+3|-4/-4|0/0|false|
|332002|+7|+7|0/0|0/0|false|
|332003|+1|+1|0/0|0/0|true|
|332004|-8|-4|-8/-8|-25/-24|false|
|332005|+4|+4|0/0|0/0|false|

Eligible seeds1/5;candidate full-domain gate1/5 versus native0/5. The aggregate
original6 strict gains pass,but the all-five full gate and per-seed nondegradation
do not. Interior full gates5/5->4/5;original5full gates5/5->3/5;original2..4remain5/5.

Failed local/order conditions over both logical splits(all five seeds):
original2/3/4:0/0 in both arms;original5:0/0->7/4;
original6:31/11->18/7;interior4:0/0->12/6.
All-domain local failures31->37/2160;order failures11->17/1080. Local/order criteria
overlap and must not be added as independent observations. Console aggregate failures
do NOT reveal actual language/profile/entity/order or mask-only categories.

## Interpretation and next bounded question

Unlike C331's frozen substitution,this train-consistent paired comparison improves
the pooled original6 counts and four of five seed comparisons. Nevertheless it fails
reliability/retention criteria and is not adopted. Seed332004 loses in three domains;
seed332001 also loses original5. Do not exclude those seeds or lower thresholds.
C331 and C332 use different initial seeds and training histories;their contrast is
not an isolated causal estimate of training/inference mismatch. No claim of universal
first-byte benefit,capacity limit,optimal coefficient or Gate F passage follows.

Before further fitting,C333 should localize matched gate rescues/new failures across
C332 native/first_mean using saved measurements,all10states and sixdomains,including
successful strata. Separate normal binding,mask-only/mixed and both-order conditions;
reconcile all parent flags and HOLDOUT counts. This is a new paired-trained-policy
localization,not a rerun of C330's1200->2400 analysis or of C332 training.

## Inheritance boundary

Parent maps853sources/2508inputs are mandatory. C332 outputs to inherit are6science
files+summary+envelope+3regression records+222module JSON/log pairs=455files.
Keep ALL447test-proof files and accepted R1.2 module PID/log semantics. A six-own-file
child would protect859sources and2969inputs,not a smaller receipt-only union.
Accepted-source immutability,sole inherited exact C204 mutable-ACTIVE exclusion,
no automatic retry,native R4 leases,all final uncached rereads and fresh verification
remain. Publication-only failure never authorizes scientific refitting.
