# Semantic Runtime

A reproducible semantic runtime for representing, executing, and evaluating design intent in 3D content creation.

**تمثيل التفكير التصميمي بطريقة منظمة يمكن تنفيذها وقياسها ومراجعتها وتحسينها اعتماداً على الأدلة.**

## Quick start

```bash
cd reference
./run.sh
# → output/evidence.md, output/result.blend, output/result.png
# ≤ 15 minutes for a new developer
```

## The problem

Design software records *what* was created, not *how* the designer thought.

## The contribution

A unified semantic representation for creative workflows that is **explainable, repeatable, measurable, falsifiable, and keeps the human in the loop.**

## Project status

| Experiment | Result | Date |
|-----------|--------|------|
| 001 — Representation proof (v0.1.0) | ❌ 6/10 | 2026-06-27 |
| 001 — Representation proof (v0.2.0) | ✅ 10/10 | 2026-06-27 |
| 002 — Execution proof | ✅ 3/3 | 2026-06-27 |
| 003 — Learning proof | ✅ confidence 0.0→0.99 | 2026-06-27 |

## Key files

| File | Purpose |
|------|---------|
| `docs/01-theory.md` | Constitution — fundamental principles |
| `spec/semantic-representation-0.2.0.md` | Current specification (proven) |
| `reference/runtime.py` | Minimal reference executable (≤200 lines, zero deps) |
| `src/translator.py` | Full YAML→bpy translator (12 transform types) |
| `src/learner.py` | Knowledge base and confidence scoring |

## Architecture

Three layers with strict dependency direction: **Theory → Model → Implementation**. See `ARCHITECTURE.md`.

## Success metrics

| Metric | Current | Target |
|--------|---------|--------|
| Replication time | ≤5 min | ≤15 min |
| Experiments completed | 3/3 | — |
| Spec versions tested | 2 (v0.1.0, v0.2.0) | — |
| Evidence documents | 4 (one per experiment + reference) | — |
