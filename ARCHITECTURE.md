# Architecture

This document defines the architectural boundaries of the project.

It intentionally describes responsibilities and dependencies rather than implementation details.

---

## Design Principle

The architecture is divided into three independent layers:

```
Theory
    ↓
Model
    ↓
Implementation
```

Each layer depends only on the layer above it.

Implementation may change.

Model may evolve.

Theory changes only if a core hypothesis is disproven.

---

## Layer 1 — Theory

**Purpose:** Define the research assumptions that give meaning to the project.

**Contains:**
- Vision
- Core contribution
- Five design principles
- Transformation Pair
- Learning methodology

**Must NOT contain:**
- Blender code
- APIs
- file formats
- implementation details

**Output:** Conceptual definitions.

---

## Layer 2 — Model

**Purpose:** Translate the theory into a formal system.

**Contains:**
- Intent Object
- Transformation representation
- Semantic runtime model
- Learning cycle
- Knowledge lifecycle

**May evolve** as experiments produce new evidence.

**Must NOT depend** on Blender-specific APIs.

**Output:** Machine-readable semantic structures.

---

## Layer 3 — Implementation

**Purpose:** Execute the model in a concrete environment.

**Current backend:** Blender.

**Contains:**
- translator.py
- learner.py
- runtime.py
- reference implementation

**Implementation is replaceable.** Future backends may include Unreal Engine, Unity, or Godot without modifying the Theory layer.

---

## Dependency Rules

**Allowed:**
```
Implementation → Model → Theory
```

**Forbidden:**
- Theory importing implementation concepts
- Model depending on Blender APIs
- Blender-specific assumptions inside semantic definitions

---

## Source of Truth

Scene state belongs to Blender.

The semantic runtime stores only:
- intent
- semantic representations
- observable transformations
- experimental evidence

The runtime never attempts to replace Blender's internal scene representation.

---

## Knowledge Flow

```
User Intent → Intent Object → Transformation Proposal → Execution
                                                              ↓
Knowledge Update ← Evidence ← Semantic Diff ← Observed Transformations
```

Each stage has a single responsibility.

---

## Replaceable Components

The following components may be replaced independently:
- LLM provider
- execution backend
- learning strategy
- persistence layer
- visualization

Replacing any of these must not require changes to the Theory layer.

---

## Stable Interfaces

The following interfaces are intended to remain stable across implementations:
- Intent Schema
- Transformation Schema
- Evidence Schema

Changes to these interfaces require versioning.

---

## Architectural Constraints

The project intentionally avoids:
- hidden mutable global state
- backend-specific semantic definitions
- irreversible execution without observable evidence
- coupling between research claims and implementation details

---

## Success Criterion

A successful implementation is one that can be replaced while preserving:
- semantic meaning
- experimental protocol
- reproducibility
- evidence

If replacing Blender with another backend requires changing the Theory layer, the architecture has failed.

---

## Architecture Test

Before introducing any new feature, ask:

1. Does this change Theory?
2. Does it only change the Model?
3. Is it purely an Implementation detail?

If the answer is unclear, the proposal should be reconsidered before implementation.
