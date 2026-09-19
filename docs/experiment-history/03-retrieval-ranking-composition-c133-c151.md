# Retrieval, ranking and composition — C133-C151

## Scientific subject

This sequence connected learned selection to a real persisted retrieval component and then explored
why compositional descriptor ranking failed or generalized across controlled factor combinations.

## Real retrieval boundary — C133-C138

### C133 — real retrieval vertical integration
PASS. The learned Control Lane drove RETRIEVE into a persisted JSON corpus through exact
StructuralIndex search, provenance validation, evidence commit, reobservation and ANSWER.
Eight persisted-corpus cases/seed passed.

### C134-C138
These experiments expanded the retrieval boundary through miss semantics, bounded recovery,
learned query formation, content-addressed corpus growth, and compositional alias generalization.
Their purpose was to separate "retrieval plumbing works" from "the learned representation ranks the
right semantic item."

## Factor/composition diagnosis — C139-C149

The ranking sequence then investigated hash collisions and factor alignment:
- collision diagnosis / collision-free multiseed robustness;
- color alias localization;
- training-only color alignment;
- exhaustive frozen factorial ranking;
- mismatch attribution;
- material/all-factor alignment;
- composition ordering and train-consistent composition;
- margin accounting.

### C142 — training-only color alignment
PASS within the finite fixture:
- baseline: 135/144
- COLOR_AUX: 144/144
- 9 baseline errors rescued, 0 new errors
- worst unseen expected-class margin improved from negative to positive.

Important limit: auxiliary supervision altered shared encoder weights and explicitly supplied
factor information during training. This was not unsupervised semantic discovery.

## Global composition recipe — C150-C151

### C150 — global auxiliary negatives
PASS.
- WITHIN_FACTOR: 20,735/20,736
- GLOBAL_CONCEPT: 20,736/20,736
- paired rescues: 1
- new errors: 0
- GLOBAL_CONCEPT minimum full-catalog margin: +0.1425753

The practical gain in raw accuracy was one decision; the more important result was strict
all-model/all-catalog closure under the registered synthetic catalog.

### C151 — cross-split replication
PASS across four replacement splits and 12 fresh initializations:
- WITHIN_FACTOR: 20,727/20,736
- GLOBAL_CONCEPT: 20,736/20,736
- 9 rescues, 0 new errors
- all GLOBAL_CONCEPT strict models passed.

This closed further tuning of the synthetic composition recipe and froze it as a task-scoped
research candidate.

## Durable conclusions

- Real persisted retrieval plumbing and semantic ranking are distinct failure surfaces.
- Provenance-correct retrieval does not repair a semantically wrong selected record.
- Factor-aware auxiliary training substantially improved this closed synthetic vocabulary.
- GLOBAL_CONCEPT-style negative scope was more robust than within-factor negatives on the
  registered catalog and replacement splits.
- The result is not evidence of open-domain language understanding or automatic factor discovery.

## Cleanup implication

C139-C151 contain many one-off diagnostic/training scripts. Their scientific conclusions are now
captured here and in accepted summaries. Before deleting implementations, retain the frozen
checkpoint lineage and any helper still imported by C152+ or by current regression modules.
