import bpy, math
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
for l in list(bpy.data.lights): bpy.data.lights.remove(l)

bpy.ops.mesh.primitive_plane_add(location=(0,0,0), scale=(3,3,1))
bpy.ops.mesh.primitive_cube_add(location=(0,0,1), scale=(1,1,1.5))
bpy.ops.object.light_add(type="AREA", location=(5,-5,5))
bpy.context.active_object.data.energy = 1000
bpy.context.active_object.data.color = (1,0.95,0.9)
bpy.ops.object.light_add(type="AREA", location=(-4,-4,3))
bpy.context.active_object.data.energy = 500
bpy.context.active_object.data.color = (0.9,0.9,1)
bpy.ops.object.light_add(type="AREA", location=(0,6,4))
bpy.context.active_object.data.energy = 800
bpy.context.active_object.data.color = (0.95,1,1)
bpy.ops.object.camera_add(location=(6,-5,4))
cam = bpy.context.active_object; cam.rotation_euler = (math.radians(50), 0, math.radians(45))
bpy.context.scene.camera = cam
print("Scene 03: studio lighting")
