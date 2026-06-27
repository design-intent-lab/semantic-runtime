import bpy, math
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
for l in list(bpy.data.lights): bpy.data.lights.remove(l)

bpy.ops.mesh.primitive_plane_add(location=(0,0,0), scale=(4,4,1))
bpy.ops.mesh.primitive_cube_add(location=(0,0,1), scale=(0.5,0.5,1.5))
bpy.ops.mesh.primitive_cylinder_add(location=(2,0,0.5), scale=(0.3,0.3,0.5))
bpy.ops.object.light_add(type="POINT", location=(2,0,2))
bpy.context.active_object.data.energy = 200
bpy.context.active_object.data.color = (1.0, 0.6, 0.2)
bpy.ops.object.light_add(type="POINT", location=(-2,-2,3))
bpy.context.active_object.data.energy = 100
bpy.context.active_object.data.color = (1.0, 0.7, 0.3)
bpy.ops.object.camera_add(location=(5,-5,3))
cam = bpy.context.active_object; cam.rotation_euler = (math.radians(50), 0, math.radians(45))
bpy.context.scene.camera = cam
print("Scene 02: warm interior")
