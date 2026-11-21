# V5-B six-boundary localization — C314

Five-to-six changed the random baseline from5/5 to2/5 and balanced from4/5 to1/5.
The original2..5 outputs reproduced exactly,so C313 was a valid capability negative.
Before adding training or another mechanism,locate newly introduced errors in saved outputs.

Pair every five/six normal answer by immutable state,logical row,language and name profile.
Use full256 argmax,correctness transitions,answer-role classes and target-vs-best-competitor
logit margins. The margin is not a probability or a universal confidence score. Keep ties.
Read actual prompt byte lengths;English24->27tokens,Japanese54->63 under the same64-slot frame.
Language and byte position co-vary,so localization alone cannot establish a context-limit cause.
Name profiles are synthetic families,not general linguistic proficiency benchmarks.

No new inference,training,model selection,answer correction or gate relaxation. Preserve all
parent failures and masked criteria. C314 PASS is diagnostic fidelity only. The next intervention
must be separately specified after observing this profile,not silently embedded into this audit.
