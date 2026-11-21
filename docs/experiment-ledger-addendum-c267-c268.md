# C267 acceptance and C268 paired-query objective boundary

## Formal verdict

C267 ACCEPTED VALID NEGATIVE. mixed_names passed1/5 (267005 only);doubled_only passed0/5.
The preregistered requirement was all five mixed_names states. Reduced collapse does not rescue
that gate. C266 remains diagnostic PASS;C265 negative;C263/C264 bounded PASS. Gate F NOT PASSED.
No production architecture/optimizer change or unseen-name-transfer claim.

Scientific execution HEAD:3418e545bc261cf1bb920f2ae8f819deec69150c.
Published log commit:92b57170c6b2c3c3dc451f9d6de402114cbd6f12.
Log blob:798096cf2d24363ccf8f109ae2d6f89843b4cf8d.
Publisher log SHA256:f8ee03f3e30132601b1a6f055388a3411b93638280ff1680a6c1075aa20c852c.
Log bytes1072898;4910 lines. Metadata blob006ddc934d7d910fd332603768ce1c33d316f664.
Summary:runs/c267-v5b-name-coverage-f8a591aae4aa4b7aa373aba2e520181c/summary.json.
Summary SHA256:f5f550d362428feaee12d7eee96db4cc324cea311b9b4e91ec50e4f150ec6ef8.

Acceptance uses the published log previously retrieved in full through the blob API and its parsed
metrics/postcheck,plus immutable publication metadata. No independent learned-state rerun or
complete-log reviewer rehash is claimed. A contents-API empty content response for this >1 MB file
is a retrieval limitation,not evidence that the run or log is missing. Do not re-execute on that basis.

## Execution validity

Own24 PASS;focused3573 PASS. Source pins448/protected inputs761 verified. Ten models completed800
updates each:8000 updates,384000 training rows,8540 wrapper forwards,435840 row presentations,
34160 core calls. One final bundle write/load;ten strict state loads. all_pairs_matched=True;
all_replays=True. Final persisted_name_coverage_scores_and_pairs=PASS;protected inputs preserved;
tracked tree clean;scientific HEAD preserved;run_execution_valid=True. scientific_status=FAIL.

## Deciding HOLDOUT metrics

Counts combine all five seeds and both symbolic languages. Each profile/arm contains480 answers
and240 same-facts/two-query pairs. These pooled descriptions do not replace individual cell gates.

|Profile|Control correct /480|Mixed correct /480|Control collapsed /240|Mixed collapsed /240|
|---|---:|---:|---:|---:|
|doubled|284|260|33|57|
|shared_prefix|248|254|88|66|
|shared_suffix|212|257|163|76|

Overall744/1440 versus771/1440 correct;collapse284/720 versus199/720.
The shared-suffix symptom decreased substantially,but accuracy remained257/480;doubled-name
accuracy decreased by24 answers and collapse increased by24 pairs. This is not uniform improvement.
Only267005/mixed_names passes every criterion. For mixed_names,267002 passes all TRAIN criteria
but fails HOLDOUT;267001/267003 have TRAIN misses and267004 misses every TRAIN answer cell.
Do not describe all failures as either mere underfitting or purely held-out generalization failure.
Control TRAIN scores on collision profiles are not fit-to-seen-profile scores:those profiles were
not optimized in doubled_only. Both learning effects and scope must remain explicit.

## Operational incident, not a second scientific attempt

After the user completed C267,the assistant mistakenly repeated the earlier C266 verdict and C267
launcher instead of judging the new published C267 result. The repeated command was safely stopped
as STALE_EXPECTED_HEAD because the log-publication commit had advanced the branch. No second C267
execution or publication occurred. The command was wrong;the user had correctly reported completion.

Commit fece51c05c2b38ffa2e96ea601fc4b8a127305b8 subsequently changed only the shared dispatcher to
report RESULT_ALREADY_PUBLISHED when active experiment and published execution_head match the stale
command. It does not authorize execution at an arbitrary current HEAD. Published can also mean an
invalid attempt;the status is availability,not PASS. The earlier operational patch had only source
readback checks,not Windows parser/regression execution. Do not retroactively claim otherwise.
Keep the normal stale guard. Fetch and judge latest logs on completion;never recycle an earlier
experiment response or silently substitute current HEAD into an old command. C267 needs no rerun.

## Accepted artifact hashes

coverage-plan.json:4f83a11bd6b2c31d7f1bd23b617772d1eab413e5099d5aafe3c4a34eb453f2d7;2631 bytes.
dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024 bytes.
trained-models.pt:a300bae3930b23c78bb4cd5285f581b21a243b6529eb770d24669ad25b92bd58;1238007 bytes.
evaluations.pt:e01decea02b8109fbed19cc01d03091867edac02fbaed00f2a7a78e40b4782f3;53143103 bytes.
measurements.json:d1c9404f3893d3b110fdbf58e15a4f241847fce8304d58a24ac35d1604acfb23;262390 bytes.
validation-summary.json:b8ab346a36cb2167e4d6cd0cbd3f19fefdc161b35a120fe40c33e00d4a8ec3f1;6831 bytes.

## Next question, not activation

With mixed-name coverage fixed,does adding a paired-query discrimination loss improve held-out
value binding relative to ordinary cross-entropy on exactly the same paired batches?
Both arms must share the fresh initial weights,paired batches,profiles,optimizer and800-update
budget. Only the loss changes. The extra term uses training targets as supervision,not model inputs.
Do not claim this isolates C267's historical failure cause or that paired batching itself helped.
C268 requires separate implementation,preregistration and committed-byte authoring review before
activation. C269 NOT REGISTERED.
