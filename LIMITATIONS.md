# Limitations

## Scope (v0.x)

- **Static scenes only.** Animation, physics, characters, and deformations are excluded.
- **Blender-only execution.** The reference runtime targets Blender; no other DCC tools are supported.
- **Interpretive evaluation requires human approval.** The system can suggest warm/cold/etc., but does not decide.

## Representation

- **YAML is not validated.** The parser accepts any structure; malformed intents may produce undefined behavior.
- **No binary format support.** All representations are plaintext YAML/JSON.
- **No streaming.** The system processes one complete transformation at a time.

## Execution

- **No inverse transforms.** The system cannot undo a transformation automatically.
- **Heuristic scene analysis.** `analyze_scene` uses simple heuristics (closest object, largest mesh) rather than AI.
- **No multi-GPU or distributed rendering.** Execution is single-process, single-GPU (or CPU fallback).
- **Render engine mismatch.** Blender 4.3 uses "BLENDER_EEVEE_NEXT"; the reference executable uses Cycles CPU for headless compatibility.

## Learning

- **Confidence reflects repetition, not accuracy.** A successful but trivial task inflates confidence as much as a difficult one.
- **No negative learning.** Failed attempts reduce confidence globally, not per-scenario.
- **Scene signature is coarse.** The signature `{light_count}_{total_energy}_{avg_temp}` may collide for different scenes with similar aggregate metrics.

## Reproducibility

- **Blender startup time.** First launch may take several minutes to compile Cycles kernels.
- **GPU dependency for EEVEE.** The reference executable defaults to Cycles CPU to avoid GPU-related crashes in headless environments.
- **Time-sensitive evidence logs.** The evidence log includes wall-clock time, which is environment-dependent.

## Known failure patterns

| Pattern | First observed | Status |
|---------|---------------|--------|
| `target_ref` with description not pre-resolved by `analyze_scene` | Experiment 001 (v0.1.0) | Mitigated in v0.2.0; heuristic resolution limited |
| `clean_scene()` destroys context for modification tasks | Experiment 002 (task 8) | Not yet resolved |
| Heuristic "جميع الأرجل" doesn't match "Leg" object names | Experiment 002 (task 5) | Not yet resolved |
