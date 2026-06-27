import bpy, math
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
for l in list(bpy.data.lights): bpy.data.lights.remove(l)

bpy.ops.mesh.primitive_plane_add(location=(0,0,0), scale=(6,6,1))
bpy.ops.mesh.primitive_cube_add(location=(0,0,1), scale=(2,2,0.5))
bpy.ops.object.light_add(type="POINT", location=(0,0,2.5))
bpy.context.active_object.data.energy = 50
bpy.context.active_object.data.color = (0.3, 0.4, 0.8)
bpy.ops.object.light_add(type="AREA", location=(-3,-3,2))
bpy.context.active_object.data.energy = 20
bpy.context.active_object.data.color = (0.2, 0.3, 0.7)
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes.get("Background")
if bg: bg.inputs["Strength"].default_value = 0.05; bg.inputs["Color"].default_value = (0.02, 0.02, 0.05, 1)
bpy.ops.object.camera_add(location=(5,-5,3))
cam = bpy.context.active_object; cam.rotation_euler = (math.radians(50), 0, math.radians(45))
bpy.context.scene.camera = cam
print("Scene 05: partial night")
