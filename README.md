# semantic-runtime

**A reproducible semantic runtime for representing, executing, and evaluating design intent through observable transformations.**

---

## Overview

Most design software saves **what** you created. It does not save **how you thought** while creating it.

`semantic-runtime` is a research platform that asks: *Can we represent design thinking itself — not just the result, but the intent, the plan, the constraints, and the observable transformations — in a structured, measurable, and reproducible way?*

It is **not** a replacement for Blender. It is **not** a new AI model. It is a **semantic layer** that sits between natural language intent and 3D execution, recording the transformations that happened so they can be reviewed, measured, learned from, and reproduced.

---

## Research Status

This repository represents an active research prototype. The semantic representation, experiments, and implementation are expected to evolve as hypotheses are confirmed, refined, or rejected through reproducible evidence.

---

## Experimental Evidence

This repository contains reproducible experimental evidence for the current implementation. The results support — but do not conclusively prove — the project's current hypotheses.

| Experiment | Status | What It Shows |
|------------|--------|---------------|
| 001 — Representation Proof | ✅ 10/10 | The semantic schema can describe 10 diverse design tasks |
| 002 — Execution Proof | ✅ 3/3 | The schema can be translated into Blender and produce `.blend` + `.png` |
| 003 — Learning Proof | ✅ 5/5 | The system improves confidence across repeated attempts |

---

## Repository Philosophy

This project does not aim to replace design tools or AI models. It studies one specific question: **Can design intent be represented, executed, and evaluated in a way that is explainable, measurable, falsifiable, and reproducible?** Blender is the first backend. The semantic representation is tool-agnostic by design.

Blender remains the source of truth for scene state. The semantic runtime maintains only semantic representations and observable transformations. It never attempts to replace the underlying scene model.

---

## Quick Start

```bash
git clone https://github.com/your-org/semantic-runtime.git
cd semantic-runtime/reference
./run.sh
```

See `REPRODUCIBILITY.md` for detailed steps, expected outputs, and verification.

---

## Repository Structure

```
semantic-runtime/
├── README.md                   # You are here
├── REPRODUCIBILITY.md          # How to reproduce all results
├── ARCHITECTURE.md             # System design and layer boundaries
├── LIMITATIONS.md              # What this project does NOT claim
├── docs/
│   ├── 01-theory.md            # The immutable constitution
│   ├── 02-model.md             # The updatable model
│   ├── 03-implementation.md    # The replaceable implementation
│   └── 04-evidence.md          # All experimental evidence
├── spec/
│   ├── semantic-representation-0.1.0.md   # Archived: disproven
│   └── semantic-representation-0.2.0.md   # Current: proven
├── reference/
│   ├── README.md               # 15-minute replication guide
│   ├── run.sh
│   ├── example.intent.yaml
│   └── runtime.py
├── experiments/
│   ├── 001-representation-proof/
│   ├── 002-execution-proof/
│   └── 003-learning-proof/
├── src/
│   ├── translator.py
│   └── learner.py
└── knowledge_base/
```

---

## Design Principles

1. **Explainable** — Every decision shows its reasoning and alternatives
2. **Repeatable** — Successful decisions become reusable rules
3. **Measurable** — Objective metrics separate from interpretive judgments
4. **Falsifiable** — Every rule is a hypothesis that can be disproven
5. **Human in the Loop** — The final creative decision always belongs to the human

---

## Non-goals

The current project intentionally does not attempt to:
- create a universal creativity model
- replace existing DCC applications
- optimize rendering pipelines
- benchmark LLMs
- automate all design decisions

---

## Research Roadmap

**Current phase:** ✓ Representation ✓ Execution ✓ Learning

**Next milestone:** □ Independent replication by 5 external developers (zero interventions)

**Future work:** □ Additional backends □ Larger evaluation datasets □ Public benchmark suite

---

## Citation

If you use this work in your research:

```bibtex
@software{semantic_runtime,
  title = {semantic-runtime: A Reproducible Semantic Runtime for Design Intent},
  year = {2026},
  url = {https://github.com/your-org/semantic-runtime}
}
```

---

## License

MIT — See `LICENSE` for details.
