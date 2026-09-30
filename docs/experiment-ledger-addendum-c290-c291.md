# C290 formal acceptance — diagnostic integrity only

## Verdict

C290 ACCEPTED PASS (saved-data diagnostic integrity only).
C289 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C291 NOT REGISTERED in this acceptance commit.
Scientific execution HEAD:327e0a2e45270a4eb60f43daf8cca5c21242987c.
Published log commit:76706cdc46914e67957abb37fcb75c46d1af0eaa.
Publication changes only docs/experiment-run-logs/c290/latest.json and latest.log.
Metadata log SHA256:8577054a4ebc4dfb323f8352fc671b21ee28cca7013ce03212a889aef7c8f27d;703272 bytes.
Summary:runs/c290-v5b-pair-margin-dd335cb112744775980aa441008b9a7f/summary.json.
Summary SHA256:1f4a3c16130b4c4517ddc7b5c09d7404ed83652fd0d6ce8b9a2438195a9cb11e.

## Validity and immutable outputs

Authoritative Windows run:own40 PASS;focused4245 PASS in316.400s;authoring_runtime_preflight PASS.
Source586/protected1056;manifest123a8805343a6c7704ff6042d83928d3069aa43fe79e213e2b5798811d35b6f3.
Saved-data reconstruction PASS;diagnostic_complete=True;capability_gate_applicable=False.
POSTCHECK:tracked_tree clean;execution_HEAD preserved;run_execution_valid=True.
Scientific model forwards,training,model-state loads,new checkpoint writes,core calls,row presentations and network calls are0.
The operational regression suite is not part of this zero-neural scientific workload.

Artifacts committed by the exact summary hash:
- audit-plan.json:2124 bytes;123a8805343a6c7704ff6042d83928d3069aa43fe79e213e2b5798811d35b6f3.
- pair-margin-report.json:6580944 bytes;28c87864bab54bd6b2402b0f52d478e35eddc7c67c8eb82ee1afa9e37f4307da.
- validation-summary.json:46427 bytes;88ad4b349cd7bacfe9ea8ca3dccd016329fc684cf828d619ae9b4db76da2b703.
All15 parent models,19440 pair records,90 partitions and60 comparisons/12960 matched pairs are retained.
C290 verifier dispatches the exact C289 verifier and reconstructs its masked/full gates before the new numerical audit.
Direct repository import C289 and its reachable helper sources remain protected;no source repair is needed.

## Findings

The auxiliary assignment margin is empirically not a guarantee of independent answer correctness.
For seed289002 quad HOLDOUT,each auxiliary arm meets the margin on144/144 pairs but has one wrong answer
(287/288 correct;143/144 both-correct pairs). The always-on mean pair penalty is4.5317428877068147e-11.
For seed289003 quad HOLDOUT,each auxiliary arm again meets144/144 margins with one wrong answer.
For seed289005 quad HOLDOUT,each auxiliary arm meets144/144 margins with four wrong answers
(284/288 correct;140/144 both-correct). Thus small auxiliary loss can coexist with relevant mistakes.

This issue is not unique to the auxiliary arms:seed289001 CE-only two-character HOLDOUT has97 margin-met
pairs,all97 containing an error,and zero both-correct pairs among144. Treat the auxiliary as a surrogate,
not a capability metric. No causal claim follows from this cross-tabulation.

Withdrawal and always-on have exactly equal NORMAL argmax outputs for seeds289002..289005 across all
three tasks and both value splits,as checked by aligned comparisons,not inferred from equal gate counts.
Seed289001 differs:TRAIN argmax flips7/6/11 and HOLDOUT flips74/71/78 for two_char/triple/quad respectively.
All four-character gates remain CE3/5,always0/5,early0/5. Do not rerun C289,discard difficult seeds,
change old thresholds,or reinterpret C290 PASS as model improvement.

## Interpretation boundary

A summed correct-versus-swapped pair gap can be positive even if one answer is compensated by the other,
or an unexamined third class wins. C290 establishes co-occurrence,not which loophole is causal.
No proof of late-training harm,saturation,universal transfer degradation,or superiority is claimed.
The same dependent examples are reused;this is not independent replication.
A subsequent separately preregistered objective comparison may test an answer-wise hardest-rival margin,
while retaining concurrent CE and pair-sum controls and all existing fixed capability gates.
