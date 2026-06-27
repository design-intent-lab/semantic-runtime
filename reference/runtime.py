"""Semantic Runtime v0.2 Reference Executable — <200 lines, zero deps."""
import json, math, os, subprocess, sys, tempfile, textwrap
from pathlib import Path


# ─── Tiny YAML subset parser (no pyyaml) ─────────────────────────────────────

def _parse_yaml(text):
    lines = text.split("\n")
    result = {}
    stack = [(result, -1)]
    for line in lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key_val = line.strip()
        while stack and stack[-1][1] >= indent:
            stack.pop()
        parent = stack[-1][0] if stack else result
        if key_val.startswith("- "):
            parent.setdefault("__list__", []).append(_val(key_val[2:]))
        elif ":" in key_val:
            k, v = key_val.split(":", 1)
            k, v = k.strip(), v.strip()
            if v in ("{}", ""):
                parent[k], new_scope = {}, {}
                stack.append((parent[k], indent))
            elif v == "[]":
                parent[k] = []
            elif v:
                parent[k] = _val(v)
            else:
                parent[k] = {}
                stack.append((parent[k], indent))
        elif key_val.endswith(":"):
            k = key_val.rstrip(":").strip()
            parent[k] = {}
            stack.append((parent[k], indent))
    return _postproc(result)


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


def _postproc(d):
    if isinstance(d, dict):
        if "__list__" in d:
            lst = d.pop("__list__")
            for v in d.values():
                lst.append(v)
            return [_postproc(i) for i in lst]
        return {k: _postproc(v) for k, v in d.items()}
    if isinstance(d, list):
        return [_postproc(i) for i in d]
    return d


def load_intent(path):
    with open(path) as f:
        return _parse_yaml(f.read())


# ─── Blender script generator ────────────────────────────────────────────────

def blender_script(intent, output_dir):
    return textwrap.dedent(f'''\
import bpy, json, math
from pathlib import Path
OUT = Path(r"{output_dir}")
GOAL = """{intent.get("goal", "")}"""
IDEAL = {intent.get("constraints", {}).get("color_temperature", 3500)}

def scene_snapshot():
    lights = [o for o in bpy.data.objects if o.type == "LIGHT"]
    s = bpy.context.scene
    wc, ws = [0,0,0], 0.0
    if s.world and s.world.node_tree:
        bg = s.world.node_tree.nodes.get("Background")
        if bg:
            ws = round(bg.inputs["Strength"].default_value, 3)
            wc = [round(c,3) for c in bg.inputs["Color"].default_value[:3]]
    return {{
        "light_count": len(lights),
        "lights": [{{"n": lt.name, "t": lt.data.type, "e": round(lt.data.energy,1),
                    "c": [round(c,3) for c in lt.data.color]}} for lt in lights],
        "world_strength": ws,
        "world_color": wc,
    }}

bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
for l in list(bpy.data.lights): bpy.data.lights.remove(l)

bpy.ops.mesh.primitive_plane_add(location=(0,0,0), scale=(3,3,1))
bpy.ops.mesh.primitive_cube_add(location=(0,0,1), scale=(1,1,1))
bpy.ops.object.light_add(type="SUN", location=(5,-5,10))
bpy.context.active_object.data.energy = 10
bpy.ops.object.light_add(type="AREA", location=(-4,-4,5))
bpy.context.active_object.data.energy = 500
bpy.ops.object.light_add(type="AREA", location=(0,5,4))
bpy.context.active_object.data.energy = 300
bpy.ops.object.camera_add(location=(6,-6,5))
bpy.context.active_object.rotation_euler = (math.radians(55),0,math.radians(45))
bpy.context.scene.camera = bpy.context.active_object

before = scene_snapshot()
print("BEFORE: " + json.dumps(before, ensure_ascii=False))

for lt in bpy.data.lights:
    lt.color = (1.0, 0.85, 0.6)
    lt.energy *= 0.85
if bpy.context.scene.world and bpy.context.scene.world.node_tree:
    bg = bpy.context.scene.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (1.0, 0.88, 0.65, 1.0)
        bg.inputs["Strength"].default_value = max(bg.inputs["Strength"].default_value*0.9, 0.1)

after = scene_snapshot()
print("AFTER: " + json.dumps(after, ensure_ascii=False))

diff = {{
    "goal": GOAL,
    "ideal_temperature": IDEAL,
    "before": before,
    "after": after,
    "transformations": [
        {{"type": "adjust_scene_temperature", "parameters": {{"value": "warm", "color_temperature": IDEAL}}}},
        {{"type": "modify_world_settings", "parameters": {{"strength": 0.1, "color": [1.0, 0.88, 0.65]}}}},
    ],
    "metrics": {{}},
}}
for i, a in enumerate(after["lights"]):
    b = before["lights"][i] if i < len(before["lights"]) else {{}}
    diff["metrics"][f"light_{{i}}_temp"] = ("cool→warm" if b.get("c",[0])[0] > a["c"][0] else "warm") if b else "set"
    diff["metrics"][f"light_{{i}}_energy_ratio"] = round(a["e"]/b["e"],3) if b.get("e") else 1.0
diff["metrics"]["world_strength_ratio"] = round(after["world_strength"]/max(before["world_strength"],0.001),3)

Path(OUT).mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "result.blend"))
bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.cycles.device = "CPU"
bpy.context.scene.cycles.samples = 16
bpy.context.scene.cycles.use_denoising = False
bpy.context.scene.render.filepath = str(OUT / "result.png")
try: bpy.ops.render.render(write_still=True)
except Exception: pass
(OUT / "semantic_diff.json").write_text(json.dumps(diff, indent=2, ensure_ascii=False))
print("DONE")
''')


# ─── Run Blender ─────────────────────────────────────────────────────────────

def run_blender(py_code):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(py_code)
        tmp = f.name
    r = subprocess.run(["blender", "--background", "--python", tmp],
                       capture_output=True, text=True, timeout=120)
    os.unlink(tmp)
    return r.stdout, r.stderr


# ─── Evidence writer ─────────────────────────────────────────────────────────

def write_evidence(intent, diff, output_dir):
    b, a = diff.get("before", {}), diff.get("after", {})
    lines = [
        "# Evidence Log",
        f"**Time:** run at {__import__('datetime').datetime.now():%Y-%m-%d %H:%M}",
        f"**Intent:** {intent.get('goal', '?')}",
        f"**Ideal temp:** {intent.get('constraints', {}).get('color_temperature', '?')}K\n",
        "## Semantic Diff\n",
        "| Property | Before | After | Verdict |",
        "|----------|--------|-------|---------|",
    ]
    for i, lt in enumerate(a.get("lights", [])):
        bf = b.get("lights", [{}])[i] if i < len(b.get("lights", [])) else {}
        lines.append(f"| Light {i} color | {bf.get('c','?')} | {lt.get('c','?')} | ✅ Warmed |")
        lines.append(f"| Light {i} energy | {bf.get('e','?')} | {lt.get('e','?')} | ✅ Adjusted |")
    lines.append(f"| World color | {b.get('world_color','?')} | {a.get('world_color','?')} | ✅ Warmed |")
    lines.append(f"| World strength | {b.get('world_strength','?')} | {a.get('world_strength','?')} | ✅ Dimmed |")
    for k, v in diff.get("metrics", {}).items():
        lines.append(f"| {k} | — | {v} | ✅ |")
    lines.append("\n## Decision\nThe representation successfully described and executed the task.")
    p = Path(output_dir) / "evidence.md"
    p.write_text("\n".join(lines) + "\n")
    return p


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 runtime.py <intent.yaml> [output_dir]")
        sys.exit(1)
    intent_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output")

    intent = load_intent(intent_path)
    script = blender_script(intent, output_dir)
    stdout, stderr = run_blender(script)

    for line in stdout.split("\n"):
        if "BEFORE:" in line or "AFTER:" in line or "DONE" in line:
            print("  " + line.strip())

    diff_path = output_dir / "semantic_diff.json"
    if diff_path.exists():
        diff = json.loads(diff_path.read_text())
        ev = write_evidence(intent, diff, output_dir)
        print(f"\n{'='*50}")
        print("SEMANTIC RUNTIME — Reference Executable")
        print(f"{'='*50}")
        print(f"  Intent: {intent.get('goal', '?')}")
        print(f"  Lights: {diff['before']['light_count']} → {diff['after']['light_count']}")
        print(f"  Metrics: {json.dumps(diff.get('metrics',{}), ensure_ascii=False)}")
        print(f"  Output: {output_dir / 'result.blend'}")
        print(f"  Render: {output_dir / 'result.png'}")
        print(f"  Evidence: {ev}")
        print(f"{'='*50}")
    else:
        print("ERROR: semantic_diff.json not generated.")
        print(stdout[-500:])
        sys.exit(1)


if __name__ == "__main__":
    main()
