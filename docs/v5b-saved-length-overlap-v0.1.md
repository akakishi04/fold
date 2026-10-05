# V5-B saved cross-length error overlap — C305

C304 did not show improved five-character reliability from adding training lengths:four-only3/5,
three/four2/5,two/three/four2/5. Some mixed models also failed at trained lengths. Every model's
four/five full-gate flag agrees,but that is not evidence of identical wrong answers.

Before another training-policy change,align the original frozen outputs for the same facts,
query,language,profile and split. Four->five separates errors already present from errors newly
introduced by the length extension. Recoveries must be counted too;equal accuracy can conceal
opposite flips. Two/three references and four-bit signatures expose broader patterns without
retraining or changing any prediction. Conditional ratios keep their actual denominators.

This is a descriptive diagnosis of the same15 states,not a new capability demonstration or
proof of a causal failure mechanism. No masked gate is replaced,model selected,or Gate F promoted.
