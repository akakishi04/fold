# V5-B frozen four-character transfer — C283

C282 raised complete three-character pass counts from0/5 to4/5 at fixed architecture/update budget,
but did not pass the registered five-seed gate. The user asks whether experience with multiple
lengths may help completely unseen lengths. Four-character evaluation directly probes this with
existing C282 checkpoints;no new training is needed.

Both arms are untrained on four-character names. Preserve every state,including mixed seed282001
which failed original tasks. Freeze weights and compare original predictions before/after the new
probe. The original C282 failure cannot be repaired by renaming the next experiment's gate.

Four-character repeated/shared-prefix3/shared-suffix3 names reuse the existing logical task and
familiar bytes. English and Japanese prompts fit48 tokens without truncation. The inherited C270
scorer is used through an explicit reversible profile-name adapter;it is not told any new target
information and no target metadata is passed to the model.

The cleanest conclusion is empirical:compare all-five gates and paired row/collapse counts on the
same new prompts. A benefit may arise from diversity,training on a closer length,or their interaction.
This experiment alone cannot distinguish those explanations;do not claim an abstract length rule.
A three-character-only training control belongs to a later preregistered comparison,not this run.

Scientific training steps0;existing states10;forward calls1350;row presentations129600;core calls5400.
A capability miss is still valid evidence. Neither a four-character PASS nor a relative improvement
implies Gate F completion. Parent artifacts,source/tests and prior verdicts remain unchanged.
