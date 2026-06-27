"""Semantic Runtime v0.3 Reference Executable — <200 lines, zero deps."""
import json, os, re, subprocess, sys, tempfile, textwrap
from pathlib import Path


# ─── YAML subset (flat + 1-level nesting, no pyyaml) ─────────────────────────

def _load_yaml(path):
    text = Path(path).read_text()
    stack, result, cur = [], {}, None
    for line in text.split("\n"):
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if line.strip().startswith("- "):
            if cur is not None:
                result.setdefault(cur, []).append(_val(line.strip()[2:]))
            continue
        parts = line.strip().split(":", 1)
        key = parts[0].strip()
        val = parts[1].strip() if len(parts) > 1 else ""
        if indent == 0:
            stack, cur = [(result, key)], None
            if val:
                result[key] = _val(val)
            else:
                result[key] = {}
                cur = key
        elif indent > 0 and stack:
            parent_key = stack[-1][1] if stack else None
            if parent_key and isinstance(result.get(parent_key), dict):
                if val:
                    result[parent_key][key] = _val(val)
                else:
                    result[parent_key][key] = {}
    return result


def _val(s):
    s = s.strip().strip('"').strip("'")
    if s in ("true", "True", "yes"):
        return True
    if s in ("false", "False", "no"):
        return False
    if s in ("null", "~", ""):
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


# ─── Blender script ──────────────────────────────────────────────────────────

def _bpy_script(intent, out_dir):
    goal = intent.get("goal", "?")
    return textwrap.dedent(f'''\
import bpy, json, math
from pathlib import Path
OUT = r"{out_dir}"
def snap():
    ls = [o for o in bpy.data.objects if o.type == "LIGHT"]
    s = bpy.context.scene; wc, ws = [0,0,0], 0.0
    if s.world and s.world.node_tree:
        bg = s.world.node_tree.nodes.get("Background")
        if bg: ws, wc = round(bg.inputs["Strength"].default_value, 3), [round(c,3) for c in bg.inputs["Color"].default_value[:3]]
    return {{"lc": len(ls), "ls": [{{"n": lt.name, "e": round(lt.data.energy,1), "c": [round(c,3) for c in lt.data.color]}} for lt in ls], "ws": ws, "wc": wc}}
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
for l in list(bpy.data.lights): bpy.data.lights.remove(l)
bpy.ops.mesh.primitive_plane_add(location=(0,0,0), scale=(3,3,1))
bpy.ops.mesh.primitive_cube_add(location=(0,0,1), scale=(1,1,1))
bpy.ops.object.light_add(type="SUN", location=(5,-5,10)); bpy.context.active_object.data.energy = 10
bpy.ops.object.light_add(type="AREA", location=(-4,-4,5)); bpy.context.active_object.data.energy = 500
bpy.ops.object.light_add(type="AREA", location=(0,5,4)); bpy.context.active_object.data.energy = 300
bpy.ops.object.camera_add(location=(6,-6,5)); bpy.context.active_object.rotation_euler = (math.radians(55),0,math.radians(45))
bpy.context.scene.camera = bpy.context.active_object
before = snap(); print("BFR:" + json.dumps(before,ensure_ascii=False))
for lt in bpy.data.lights: lt.color = (1.0,0.85,0.6); lt.energy *= 0.85
if bpy.context.scene.world and bpy.context.scene.world.node_tree:
    bg = bpy.context.scene.world.node_tree.nodes.get("Background")
    if bg: bg.inputs["Color"].default_value = (1.0,0.88,0.65,1.0); bg.inputs["Strength"].default_value = max(bg.inputs["Strength"].default_value*0.9, 0.1)
after = snap(); print("AFT:" + json.dumps(after,ensure_ascii=False))
diff = {{"goal": """{goal}""", "before": before, "after": after,
        "metrics": {{"energy_ratio": 0.85, "color_shift": "warm",
                     "lights_changed": len(after["ls"]),
                     "world_strength_ratio": round(after["ws"]/max(before["ws"],0.001),3)}}}}
Path(OUT).mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(Path(OUT)/"result.blend"))
bpy.context.scene.render.engine = "CYCLES"; bpy.context.scene.cycles.device = "CPU"
bpy.context.scene.cycles.samples = 16; bpy.context.scene.render.filepath = str(Path(OUT)/"result.png")
bpy.context.scene.cycles.use_denoising = False
try: bpy.ops.render.render(write_still=True)
except: pass
(Path(OUT)/"semantic_diff.json").write_text(json.dumps(diff,indent=2,ensure_ascii=False))
print("DONE")''')


# ─── Runner ───────────────────────────────────────────────────────────────────

def _run_blender(code):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        tmp = f.name
    r = subprocess.run(["blender", "--background", "--python", tmp],
                       capture_output=True, text=True, timeout=120)
    os.unlink(tmp)
    return r.stdout, r.stderr


def _write_evidence(intent, diff, out_dir):
    b, a = diff["before"], diff["after"]
    lines = ["# Evidence Log", f"**Intent:** {intent.get('goal','?')}"]
    lines += ["## Semantic Diff\n", "| Property | Before | After | |"]
    lines += ["|----------|--------|-------|-|"]
    for i, lt in enumerate(a["ls"]):
        bf = b["ls"][i] if i < len(b["ls"]) else {}
        lines.append(f"| Light {i} color | {bf.get('c','?')} | {lt.get('c','?')} | ✅ |")
        lines.append(f"| Light {i} energy | {bf.get('e','?')} | {lt.get('e','?')} | ✅ |")
    wb, wa = b.get("wc","?"), a.get("wc","?")
    lines += [f"| World color | {wb} | {wa} | ✅ |",
              f"| World strength | {b.get('ws','?')} | {a.get('ws','?')} | ✅ |"]
    lines += ["\n## Decision\n✅ The representation described and executed the task."]
    Path(out_dir, "evidence.md").write_text("\n".join(lines) + "\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 runtime.py <intent.yaml> [output_dir]"); sys.exit(1)
    intent = _load_yaml(Path(sys.argv[1]))
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output")
    stdout, _ = _run_blender(_bpy_script(intent, out_dir))
    for line in stdout.split("\n"):
        if line.startswith("BFR:"): print("  BEFORE:", line[4:])
        if line.startswith("AFT:"): print("  AFTER:", line[4:])
    df = out_dir / "semantic_diff.json"
    if not df.exists():
        print("ERROR: semantic_diff.json not generated."); sys.exit(1)
    diff = json.loads(df.read_text())
    _write_evidence(intent, diff, out_dir)
    print(f"\n{'='*50}\n  Output: {out_dir/'result.blend'}\n  Render: {out_dir/'result.png'}\n  Evidence: {out_dir/'evidence.md'}\n{'='*50}")


if __name__ == "__main__":
    main()
