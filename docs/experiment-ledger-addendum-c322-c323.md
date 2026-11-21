# C322 formal acceptance — saved paired-query contrast

C322 ACCEPTED PASS (DIAGNOSTIC INTEGRITY ONLY). C321 stays ACCEPTED VALID NEGATIVE (interior-order0/5).
C320 bounded unequal-length PASS remains. Gate F NOT PASSED. C323 NOT REGISTERED at this commit.

## Authoritative evidence identity
Scientific execution HEAD: b7943ab4435d68d2716e6137b596042b777f2efb.
Publication commit: 278e883bd5b6555aa2bef8a43e1634dc5e44e6f0.
Log: docs/experiment-run-logs/c322/latest.log.
Log bytes: 1173665; SHA256: eb081b5f0f3b421dc987c1605b21efca5312438cdcad9d70865fc0fc4f7f8e85.
CRLF byte count and SHA256 reconstructed and independently matched published metadata.
Summary: runs/c322-v5b-query-contrast-f164844010f04c24bcfda4a743b44a72/summary.json.
Summary SHA256: fdcf1f2ac893a46c900e50db93740004926c70765ca269ba0cfe7474bf4c5796.
Own24 PASS in 11.643s; full focused5269 PASS in1245.157s,0failures,0errors,
one process,exit0/0x00000000. Sources778/protected1467;manifest
719cd169028e0c0ead99f4620035b532cefed65145c4bcb4f8af3c781fda01e8.
Precheck saved_query_pair_reconciliation PASS;status PASS;persisted_query_contrast PASS;
science exit0;run_execution_valid=True;tracked tree clean;scientific HEAD preserved.
Publication contains exactly latest.log/latest.json. No training,new model forward,
state loading,new checkpoint write or network call by the C322 diagnostic body.

## Deciding observations (all five seeds per arm; each condition 2160 paired contexts)
Original length4 controls:both arms4320/4320 normal correct;0/2160 same predictions;
2160/2160 both correct and both target-value directions. Mean query contrast
mean_last24.805650267612712,last_only24.404063485988974.
Unseen interior-order names:
- mean_last:2211/4320 normal correct;1996/2160 same predictions;
  107/2160 both correct;118/2160 two-target preference direction;
  1315/2160 positive query contrast;mean contrast0.6438573484898602;
  offset-invariant logit difference mean0.8812483978153208.
- last_only:2292/4320 normal correct;1951/2160 same predictions;
  171/2160 both correct;190/2160 two-target preference direction;
  1410/2160 positive query contrast;mean contrast0.9952475930687953;
  offset-invariant logit difference mean0.9393070819791876.
For both interior arms,near-shift-invariant pairs0/2160 at fixed 1e-9 tolerance.
Thus most paired answers collapse to the same argmax despite nonidentical
output score vectors. Positive contrast does NOT imply correct 256-way decoding.
No class restriction,selected seeds or changed outputs. 240 groups and40 score
reconciliations all agree with C321 saved output/unchanged scoring. These 8640
paired contexts are dependent contrasts,not independent trials.

## Interpretation limits and next research boundary
The output head is weakly query-sensitive for the new name-order patterns,not
literally invariant. Nothing here identifies the hidden layer responsible or
proves a certain architecture incapable of learning those names. C322 PASS is
audit integrity,not a new model capability result,so C321 negative and Gate F
remain unaltered.

Suggested next question:in existing C321/C322 saved outputs,are collapsed answers
more consistent with the first or last fact's associated value than with the
requested name? Compare both fact order permutations at fixed facts/values/query
and their original-four control,without new neural inference or rerouting.
This proposal is NOT C323 registration,which requires separate immutable prereg,
source,test,runner,launcher,committed-byte review and activation.

## Regression performance evidence (not a causal speed profile)
C322 full5269 took1245.157s. Class boundaries from its execution log show
c182 ~50.8s,c304 ~48.5s,c316 ~47.2s,c309 ~46.9s,c315 ~46.8s among
the slowest; many earlier historical tests consume the time. Preserve full
single-process ordered regression while seeking safe batching of source
attestations,cached immutable artifact checks and better phase timers.
No relaxation of validation just to reduce runtime.
