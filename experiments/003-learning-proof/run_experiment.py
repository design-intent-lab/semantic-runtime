import subprocess, json, sys, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
import learner

SCENES_DIR = Path(__file__).parent / "scenes"
BLENDER = "/usr/bin/blender"

SCENES = [
    ("01_sunny_room",     {"light_count": 2, "total_energy": 510,  "avg_temperature": 5500}),
    ("02_warm_interior",  {"light_count": 2, "total_energy": 300,  "avg_temperature": 3500}),
    ("03_studio",         {"light_count": 3, "total_energy": 2300, "avg_temperature": 5000}),
    ("04_overcast_outdoor",{"light_count": 1, "total_energy": 3,   "avg_temperature": 6500}),
    ("05_partial_night",  {"light_count": 2, "total_energy": 70,   "avg_temperature": 8000}),
]


def run_blender(py_file):
    r = subprocess.run([BLENDER, "--background", "--python", str(py_file)],
                       capture_output=True, text=True, timeout=180)
    return r.stdout, r.stderr


def build_script(scene_name, scene_desc, attempt):
    adapted = learner.adapt_params("adjust_light_color", {
        "color": [0.3, 0.4, 0.8],
        "energy_multiplier": 0.25,
    }, scene_desc)

    c = adapted["color"]
    em = adapted["energy_multiplier"]
    conf = adapted.get("_confidence", 0.0)
    src = adapted.get("_source", "default")

    scene_path = SCENES_DIR / f"{scene_name}.py"

    return f'''
import bpy, sys, math

# === Load scene ===
exec(open(r"{scene_path}").read())

print(f"[LEARN] attempt={attempt}, source={src}, confidence={conf:.2f}")

# === Transform: make lighting nocturnal ===
lights = [o for o in bpy.data.objects if o.type == "LIGHT"]
print(f"[LEARN] Found {{len(lights)}} lights")
for lt in lights:
    print(f"  {{lt.name}}: energy={{lt.data.energy:.1f}}, color={{tuple(round(v,2) for v in lt.data.color)}}")

# World darkening
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Strength"].default_value = 0.05
    bg.inputs["Color"].default_value = (0.05, 0.05, 0.2, 1)

# Adjust light colors and energy
for light in bpy.data.lights:
    light.color = ({c[0]}, {c[1]}, {c[2]})
    light.energy = light.energy * {em}

# === Render ===
OUT = "/tmp/semantic_learn_{scene_name}_a{attempt}"
bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.cycles.device = "CPU"
bpy.context.scene.cycles.samples = 16
bpy.context.scene.cycles.use_denoising = False
bpy.ops.wm.save_as_mainfile(filepath=OUT + ".blend")
bpy.context.scene.render.filepath = OUT + ".png"
try:
    bpy.ops.render.render(write_still=True)
    print(f"[LEARN] Rendered {{OUT}}.png")
except Exception as e:
    print(f"[LEARN] Render skip: {{e}}")
'''


def main():
    os.makedirs("/tmp/semantic_learn", exist_ok=True)
    results = []

    for i, (scene_name, scene_desc) in enumerate(SCENES):
        attempt = i + 1
        print(f"\n{'='*50}")
        print(f"Iteration {attempt}/5: {scene_name}")
        print('='*50)

        script = build_script(scene_name, scene_desc, attempt)
        script_path = Path(f"/tmp/semantic_learn_{scene_name}.py")
        script_path.write_text(script)

        stdout, stderr = run_blender(script_path)
        for line in stdout.split("\n"):
            if "[LEARN]" in line or "Saved" in line or "Rendered" in line:
                print(f"  {line.strip()}")

        success = "Rendered" in stdout and "Error" not in stdout.split("\n")[-5:]
        errors = [l for l in stdout.split("\n") if "Error" in l and "Rendered" not in l]
        intervention = 1 if errors else 0
        conf = learner.compute_confidence("adjust_light_color")

        result = {
            "attempt": attempt,
            "scene": scene_name,
            "success": success,
            "error_count": len(errors),
            "human_intervention": intervention,
            "confidence": round(conf, 3),
        }
        results.append(result)

        learner.save_attempt("adjust_light_color", {
            "scene": scene_name,
            "scene_signature": f"lights={scene_desc['light_count']}_energy={scene_desc['total_energy']}_temp={scene_desc['avg_temperature']}",
            "parameters": {"color": [0.3, 0.4, 0.8], "energy_multiplier": 0.25},
            "success": success,
            "confidence": conf,
            "user_intervention": intervention,
        })

        print(f"  Result: {'✅' if success else '❌'}, errors={len(errors)}, confidence={conf:.3f}")

    # Summary
    print(f"\n{'='*50}")
    print("FINAL RESULTS")
    print('='*50)
    for r in results:
        print(f"  {r['attempt']}. {r['scene']:20s} {'✅' if r['success'] else '❌'} "
              f"errors={r['error_count']} intervention={r['human_intervention']} confidence={r['confidence']:.3f}")

    final_conf = learner.compute_confidence("adjust_light_color")
    print(f"\nFinal confidence: {final_conf:.3f}")
    print(f"Total interventions: {sum(r['human_intervention'] for r in results)}")
    print(f"First-attempt success (3/5): {sum(1 for r in results[:3] if r['success'])}/3")
    print(f"Success trend: {[r['success'] for r in results]}")

    # Write results.md
    lines = [
        "# نتائج التجربة 003: إثبات التعلم\n",
        "**الحالة:** مكتملة\n",
        "## جدول النتائج\n",
        "| # | المشهد | النجاح | أخطاء | تدخل | الثقة |",
        "|---|--------|--------|-------|------|-------|",
    ]
    for r in results:
        lines.append(f"| {r['attempt']} | {r['scene']:20s} | {'✅' if r['success'] else '❌'} | {r['error_count']} | {r['human_intervention']} | {r['confidence']:.3f} |")
    lines += [
        "\n## الملخص",
        f"- **الثقة النهائية:** {final_conf:.3f}",
        f"- **إجمالي التدخلات:** {sum(r['human_intervention'] for r in results)}",
        f"- **نجاح أول 3 محاولات:** {sum(1 for r in results[:3] if r['success'])}/3",
        f"- **اتجاه النجاح:** {[r['success'] for r in results]}",
        "\n## التحليل\n(سيملأ بعد المراجعة)\n",
        "## القرار\n(سيملأ بعد المراجعة)\n",
    ]
    Path(Path(__file__).parent / "results.md").write_text("\n".join(lines))

    return 0 if final_conf >= 0.7 else 1


if __name__ == "__main__":
    sys.exit(main())
