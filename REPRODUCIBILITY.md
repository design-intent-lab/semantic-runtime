# Reproducibility

## Goal

A developer with no prior knowledge of this project can clone, run, and verify the full Semantic Runtime pipeline in ≤15 minutes.

## Requirements

| Dependency | Version | Notes |
|------------|---------|-------|
| Python | ≥3.10 | Standard library only (json, pathlib, subprocess) |
| Blender | ≥4.0 | Add to PATH; tested on 4.3.2 (aarch64, headless) |

## Replication steps

```bash
git clone <url> semantic-runtime
cd semantic-runtime/reference
./run.sh
```

Expected output:

```
output/
├── semantic_diff.json    # Machine-readable before/after comparison
├── evidence.md           # Human-readable evidence log
├── result.blend          # Blender scene after transformation
└── result.png            # Rendered image
```

## Expected metrics

After running the reference executable on `example.intent.yaml` ("اجعل الإضاءة دافئة"):

| Metric | Expected value | Tolerance |
|--------|---------------|-----------|
| Lights detected | 3 | ±0 |
| Color change | White → warm (1, 0.85, 0.6) | ±0.05 per channel |
| Energy change | 85% of original | ±5% |
| World color | Warm (1, 0.88, 0.65) | ±0.1 per channel |
| World strength | 90% of original | ±10% |
| Render output | .png exists, non-empty | — |

## Failure modes

| Symptom | Likely cause | Action |
|---------|-------------|--------|
| `blender: not found` | Blender not in PATH | Install from blender.org |
| Render fails with EGL error | No GPU in headless env | Engine auto-fallsback to Cycles CPU |
| Semantic diff missing | Blender Python crash | Run `blender --background --python runtime.py` manually |
| Different metric values | Blender version difference | Check `blender --version` ≥ 4.0 |

## Verification

Run after replication:

```bash
python3 -c "
import json
d = json.load(open('output/semantic_diff.json'))
assert len(d['before']['lights']) == 3, 'Expected 3 lights'
assert d['after']['lights'][0]['c'] == [1.0, 0.85, 0.6], 'Color should be warm'
print('✅ Replication verified')
"
```
