# Reproducibility

## Goal

A developer with no prior knowledge of this project can clone, run, and verify the full Semantic Runtime pipeline in **≤15 minutes**.

## Requirements

| Dependency | Version | Notes |
|------------|---------|-------|
| Python | ≥3.10 | Standard library only (json, pathlib, subprocess) |
| Blender | ≥4.0 | Add to PATH; tested on 4.3.2 (aarch64, headless) |

## Replication steps (≤5 minutes)

```bash
git clone https://github.com/your-org/semantic-runtime.git
cd semantic-runtime/reference
./run.sh
```

### What happens

1. `run.sh` calls `python3 runtime.py example.intent.yaml output/`
2. `runtime.py` (152 lines, zero dependencies) parses the YAML intent
3. Generates a Blender Python script that:
   - Creates a default scene with 3 lights and a camera
   - Takes a **BEFORE** snapshot of all light colors, energies, and world settings
   - Executes the transformation: warm all lights (color → 1.0, 0.85, 0.6), reduce energy to 85%, warm the world background
   - Takes an **AFTER** snapshot
   - Computes a **Semantic Diff** between before and after
   - Saves `result.blend`, `result.png`, `semantic_diff.json`, `evidence.md`
4. `runtime.py` reads the diff and prints a summary

## Expected output

```
output/
├── semantic_diff.json    # Machine-readable before/after comparison
├── evidence.md           # Human-readable evidence log
├── result.blend          # Blender scene after transformation (≈430 KB)
└── result.png            # Rendered image (≈2 MB, 1280×720)
```

## Expected metrics

After running on `example.intent.yaml` ("اجعل الإضاءة دافئة"):

| Metric | Expected value | Tolerance |
|--------|---------------|-----------|
| Lights detected | 3 | ±0 |
| Color change | White → warm (1.0, 0.85, 0.6) | ±0.05 per channel |
| Energy change | 85% of original | ±5% |
| World color | Warm (1.0, 0.88, 0.65) | ±0.1 per channel |
| World strength | 90% of original | ±10% |
| Render output | .png exists, non-empty | — |
| Total runtime | <120 seconds | — |

## Verification

Run this after `./run.sh` completes:

```bash
cd output
python3 -c "
import json
d = json.load(open('semantic_diff.json'))
assert len(d['before']['ls']) == 3, f'Expected 3 lights, got {len(d[\"before\"][\"ls\"])}'
assert d['after']['ls'][0]['c'] == [1.0, 0.85, 0.6], f'Color mismatch'
assert d['after']['ls'][0]['e'] == 425.0, f'Energy mismatch'
print('✅ Replication verified')
"
```

## Failure modes

| Symptom | Likely cause | Action |
|---------|-------------|--------|
| `blender: not found` | Blender not in PATH | Install from blender.org, or set `alias blender=/path/to/blender` |
| `EGL Error` or GPU crash | No GPU in headless environment | Falls back to Cycles CPU automatically. First run may take 2-3 min to compile kernels. |
| Semantic diff missing | Blender script crash | Run `blender --background --python /tmp/semantic_*.py` manually to see full error |
| Different metric values | Blender version mismatch | Check `blender --version` ≥ 4.0. Minor Cycles sampling differences are expected. |
| `Permission denied` on run.sh | Execute bit missing | `chmod +x run.sh` |

## How we measure replication time

From `git clone` to verified `evidence.md`:

```
clone → cd reference → ./run.sh → verify → done
└─────────────── < 15 minutes ──────────────────┘
```

Measured: **9 seconds** in the development environment.
