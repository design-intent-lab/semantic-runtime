# Architecture

Three layers with strict dependency direction: **Theory ← Model ← Implementation**.

```
┌─────────────────────────────────────────────────┐
│  Layer 1: Theory (docs/01-theory.md)            │
│  · Principles: explainable, repeatable,          │
│    measurable, falsifiable, human-in-loop        │
│  · Unit: transformation_pair (Δ_Context,         │
│    Δ_Result)                                     │
│  · Changes only when a core hypothesis is        │
│    disproven                                     │
└──────────────────────┬──────────────────────────┘
                       │ depends on
┌──────────────────────▼──────────────────────────┐
│  Layer 2: Model (docs/02-model.md)              │
│  · Intent, Components, Learning Cycle            │
│  · Describes how the theory works                │
│  · Evolves with experiments                      │
└──────────────────────┬──────────────────────────┘
                       │ depends on
┌──────────────────────▼──────────────────────────┐
│  Layer 3: Implementation (src/, reference/)      │
│  · Replaceable — current: Blender + Gemini       │
│  · Reference executable: reference/runtime.py    │
│  · Full translator: src/translator.py            │
│  · Learner: src/learner.py                       │
└─────────────────────────────────────────────────┘
```

## Dependency rules

- **Theory never imports Implementation.** The theory layer is text-only (docs/01-theory.md).
- **Model references Theory by name only.** The model layer is text-only (docs/02-model.md).
- **Implementation depends on both.** Code lives here and can reference concepts from Theory and Model.

## Scope boundaries

| Scope | Included | Excluded |
|-------|----------|----------|
| **v0.x** | Static 3D scenes | Animation, physics, characters |
| **Representation** | YAML intent, transformation pairs, semantic diff | Binary formats, real-time streaming |
| **Execution** | Blender (headless or GUI), Cycles CPU | External renderers, GPU-only pipelines |
| **Learning** | JSON knowledge base, confidence scoring, heuristic matching | Neural networks, online learning |

## Key files

| File | Layer | Purpose |
|------|-------|---------|
| `docs/01-theory.md` | Theory | Constitution — fundamental principles |
| `docs/02-model.md` | Model | Framework — intent, components, learning cycle |
| `spec/semantic-representation-0.2.0.md` | Model | Semantic representation specification |
| `src/translator.py` | Implementation | Full YAML→bpy translator (423 lines, 12 transform types) |
| `src/learner.py` | Implementation | Knowledge base and confidence scoring |
| `reference/runtime.py` | Implementation | Minimal reference executable (≤200 lines, zero deps) |
