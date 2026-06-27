import bpy, math
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
for l in list(bpy.data.lights): bpy.data.lights.remove(l)

bpy.ops.mesh.primitive_plane_add(location=(0,0,0), scale=(10,10,1))
bpy.ops.mesh.primitive_cube_add(location=(-2,0,1), scale=(1,1,2))
bpy.ops.mesh.primitive_cylinder_add(location=(2,1,0.5), scale=(0.5,0.5,0.5))
bpy.ops.mesh.primitive_uv_sphere_add(location=(0,-2,1), scale=(0.8,0.8,0.8))
bpy.ops.object.light_add(type="SUN", location=(5,-5,20))
bpy.context.active_object.data.energy = 3
bpy.context.active_object.data.color = (0.8, 0.85, 0.9)
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes.get("Background")
if bg: bg.inputs["Strength"].default_value = 0.3; bg.inputs["Color"].default_value = (0.7, 0.75, 0.85, 1)
bpy.ops.object.camera_add(location=(8,-8,6))
cam = bpy.context.active_object; cam.rotation_euler = (math.radians(55), 0, math.radians(45))
bpy.context.scene.camera = cam
print("Scene 04: overcast outdoor")
