import bpy, math
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
for l in list(bpy.data.lights): bpy.data.lights.remove(l)

bpy.ops.mesh.primitive_plane_add(location=(0,0,0), scale=(5,5,1))
bpy.ops.mesh.primitive_cube_add(location=(0,0,1), scale=(1,1,1))
bpy.ops.object.light_add(type="SUN", location=(10,-10,15))
bpy.context.active_object.data.energy = 10
bpy.ops.object.light_add(type="AREA", location=(-5,-5,5))
bpy.context.active_object.data.energy = 500
bpy.ops.object.camera_add(location=(6,-6,4))
cam = bpy.context.active_object; cam.rotation_euler = (math.radians(60), 0, math.radians(45))
bpy.context.scene.camera = cam
print("Scene 01: sunny room")
