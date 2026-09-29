# V5-B saved matched-cell length-transfer attribution — C285

C284 matched maximum training length3 and found quad gates2/5 for three_char_only versus3/5 for
mixed_length. There were two candidate-only passes, one control-only pass and one shared failure.
The comparison is not uniformly favorable and five seeds do not settle the general diversity claim.

The candidate at284001 passed length2/3 but failed4; both284002 arms failed even length3.
These are different observable failure patterns. C285 locates their fixed-criterion counterparts
without another model change:compare each state's three-character cells with structurally matched
four-character cells, and compare both arms on the same four-character cells.

The analysis preserves all10 states and reconstructs all3240 fixed records. It separates persistent
co-failure, newly failing cells, rescued cells and maintained successes for each criterion. Normal
accuracy,collapse and ablated-correct counts accompany the tables. There is no hidden seed selection.

Matching is by split,structural profile,language,entity pair,fact order and criterion. It is deliberately
cell-level attribution, not row-level correspondence or causal proof. A shared failing cell at both
lengths can contain different erroneous rows. The original training and transfer gates remain fixed.

The diagnostic result should inform whether the next intervention should target training stability,
new length-specific binding failure,or mask-only sensitivity. It does not select the next intervention
in advance and does not replace independent replication where stronger superiority evidence is needed.
No model is trained,forwarded or loaded by C285 science; saved logits are reconstructed by the pinned
C284 verifier. Formal PASS means integrity only, never capability closure or automatic Gate F promotion.
