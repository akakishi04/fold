# Standalone Language Model Milestone Proposal

> **Status: DRAFT / NON-AUTHORITATIVE / NOT ADOPTED**
>
> This document records a planning proposal only. It does **not** change the authoritative
> experiment ledger, Gate status, active C experiment, architecture specification, or development
> roadmap. Formal adoption is intentionally deferred to a later main-chat review.

- Recorded: 2026-09-21
- Repository: `akakishi04/fold`
- Working branch at record time: `feat/sft-target-loss`
- Scope: near-term project-level milestone proposal

## 1. Proposal in one sentence

Set the next large project goal to:

> **Complete a small but reproducible standalone FOLD language model that can learn from real
> training data and produce meaningful end-to-end responses to unseen natural-language input
> through the FOLD runtime.**

The purpose is to move the project from "individual architectural mechanisms are being validated"
to "a usable language model exists as an integrated artifact."

This is a **north-star / product milestone above the existing V5-A..V5-I gates**, not a replacement
for those gates.

## 2. Current authoritative context

At the time this proposal was recorded, the authoritative
`docs/experiment-ledger-and-handoff.md` states:

- Gate A/B: PASSED;
- Gate C/D: PASSED in measured scope;
- Gate E: NOT PASSED;
- C208: ACCEPTED VALID NEGATIVE;
- C209: ACTIVE / NOT YET JUDGED;
- C210: NOT REGISTERED.

Therefore the immediate execution path remains the existing Gate E / C-series work. This proposal
must not be used to skip, rename, or retroactively reinterpret those experiments.

## 3. Naming caution

The planning conversation initially used the working label **"FOLD v0.1 — Standalone Language
Model Milestone."**

That label should **not** be adopted as-is without review because the repository already uses
"v0.1" for an existing kernel/version lineage while the current architecture roadmap is v0.5.

Until the main-chat review chooses a formal release/milestone name, this document uses:

> **Standalone Language Model Milestone**

as a neutral working name.

## 4. Proposed completion criteria

The milestone should not be considered complete merely because a toy fixture or one synthetic task
passes. A formal adoption should define measurable thresholds for the following criteria.

### 4.1 End-to-end language path

A reproducible path exists from user text to final generated text:

```text
natural-language input
  -> encoding / input representation
  -> FOLD state/runtime
  -> internal computation / routing
  -> output representation
  -> decoding
  -> final text response
```

The path must be executable without manually injecting hidden target information or expected
answers.

### 4.2 Real-data training

The model can train on a non-toy language dataset or clearly defined real-language subset.

Required evidence should include at least:

- training loss behavior;
- held-out loss/quality behavior;
- checkpoint save/load;
- resume from checkpoint;
- data split/provenance manifest;
- repeatable training invocation.

Large-scale training is **not** implied by this proposal. The first target should remain small enough
to diagnose locally.

### 4.3 Generalization beyond memorization

The resulting model must be evaluated on held-out inputs that were not present verbatim in training.

Candidate checks include:

- paraphrases;
- unseen combinations of learned concepts;
- short instruction following;
- simple multi-step reasoning;
- exact-copy versus semantic-response cases kept separate.

Passing training examples alone is insufficient.

### 4.4 FOLD-specific mechanisms have measurable effect

At least one controlled ablation must demonstrate that the mechanisms claimed as part of the FOLD
architecture materially affect behavior, quality, compute, storage, or memory use.

Examples may include controlled removal or replacement of:

- shared core / shared basis mechanisms;
- working state / recurrence;
- controller / routing;
- bounded memory or retrieval paths;
- compressed/module-specific components.

A formal experiment must distinguish "the model works" from "the proposed FOLD mechanism caused the
observed difference."

### 4.5 Fair baselines

The integrated model should be compared against appropriate baselines under declared budgets.

At minimum, formal adoption should remain compatible with the baseline requirements already listed
for V5-I, including dense, parameter-sharing/recurrent, quantized, and ablation baselines.

A Transformer baseline may also be included where tokenization, model size, training data, compute,
and evaluation can be made sufficiently comparable.

Useful comparison axes include:

- held-out loss / byte-normalized loss where appropriate;
- task quality and coverage;
- serialized model bytes;
- resident memory and peak RAM/VRAM;
- training wall-clock;
- TTFT / inference latency;
- active compute / internal steps;
- checkpoint/resume behavior.

No single metric should be treated as proof of architectural superiority.

### 4.6 Reproducibility

A clean environment should be able to reproduce the basic lifecycle:

```text
dataset
  -> train
  -> checkpoint
  -> load
  -> inference
  -> evaluation
```

Required commands, versions, seeds, manifests, and known deviations should be recorded according to
the repository's existing experiment/accounting rules.

## 5. Relationship to the current roadmap

This milestone is intended to sit **above**, not replace, the v0.5 roadmap.

A tentative mapping is:

```text
current work
  -> finish Gate E under the authoritative C-series process
  -> integrate only the later capabilities actually required for a standalone LM
  -> establish real-language training + end-to-end generation
  -> held-out/generalization evaluation
  -> controlled ablations and fair baselines
  -> Standalone Language Model Milestone
```

Gate F/G capabilities may be prerequisites depending on the final milestone definition.

Gate H (Vision) should not automatically be a blocker for the first standalone language-model
milestone unless the main-chat review explicitly chooses multimodality as a requirement.

Gate I remains the natural place for broader scaling and practical comparison.

## 6. Research tracks that should not automatically block this milestone

The following ideas remain useful research tracks, but should not become mandatory blockers merely
because they are interesting:

- PC-ALM / local-credit alternatives;
- Multi-Axis shared-basis variants;
- shared-basis automatic module partitioning;
- KV/context-memory replacement hypotheses;
- reflex-like fast response mechanisms;
- native-agent behavior;
- MinePilot integration;
- autonomous Godot-world experiments;
- Vision, unless explicitly promoted to a milestone requirement.

They may be adopted earlier if an experiment shows they are required to satisfy a defined milestone
criterion. Otherwise they should remain parallel hypotheses or later-stage work.

## 7. Why define this milestone

The project currently has many viable research directions. Without an integration target, a
successful local experiment can immediately create another architectural branch before the system
is ever tested as one language model.

This milestone creates a stopping rule:

> New mechanisms are valuable, but the near-term integration question is whether FOLD can become a
> reproducible standalone language model with measurable generalization and explicit resource
> accounting.

This does not imply freezing research. It provides a criterion for deciding which research results
must enter the first integrated model and which can remain separate.

## 8. Risks to resolve before formal adoption

1. **Version-name collision**  
   "FOLD v0.1" conflicts with existing repository version terminology.

2. **Ambiguous phrase: "works as an LLM"**  
   Formal adoption needs numeric or task-level acceptance thresholds.

3. **Toy-task inflation**  
   Synthetic success must not be presented as general language competence.

4. **Baseline unfairness**  
   Parameter count alone is insufficient; storage, active compute, tokenizer/input unit, training
   budget, and wall-clock must be declared.

5. **Scope expansion**  
   Vision, agency, MinePilot, long-context memory, and new architecture hypotheses can turn one
   milestone into several unless blocker status is explicitly decided.

6. **Gate bypass risk**  
   This project-level goal must not be used to declare Gate E or later gates passed without their
   own preregistered acceptance evidence.

## 9. Decisions reserved for the later main-chat review

Before this proposal becomes authoritative, the main chat should explicitly decide:

- formal milestone/release name;
- whether this is a release milestone, roadmap milestone, or Gate-I exit target;
- exact minimum real-data training scope;
- held-out/generalization tasks and thresholds;
- required baseline set;
- which FOLD mechanisms are mandatory for the first integrated model;
- whether memory is required;
- whether Vision is required or deferred;
- which existing authoritative documents should be updated.

Only after those decisions should README, architecture/roadmap text, or authoritative experiment
state be modified.

## 10. Proposed adoption rule

If formally adopted later, the milestone should be expressed as a measurable integration contract,
not as a claim that FOLD has already achieved language-model capability.

Until then:

> **This document is a proposal record only.**
