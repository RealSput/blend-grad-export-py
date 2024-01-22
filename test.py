import bpy

def delete_all_meshes_except_active():
    # Get the active object
    active_object = bpy.context.active_object

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select all mesh objects except the active object
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and obj != active_object:
            obj.select_set(True)

    # Delete the selected objects
    bpy.ops.object.delete()
    
def dupframe():
    original_objects = tuple(bpy.context.scene.objects)
    bpy.ops.object.select_all(action='DESELECT')
    duplicated_meshes = []

    for obj in original_objects:
        if obj.type != 'MESH': return
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        if bpy.context.active_object and bpy.context.active_object.type == 'MESH':
            bpy.ops.object.duplicate(linked=False)
            duplicate = bpy.context.active_object
            duplicated_meshes.append(duplicate)
        bpy.ops.object.select_all(action='DESELECT')

    for duplicate_mesh in duplicated_meshes:
        duplicate_mesh.animation_data_clear()
        duplicate_mesh.select_set(True)

    bpy.context.view_layer.objects.active = duplicated_meshes[0]
    bpy.ops.object.join()

# Store each mesh in the scene into a list
mesh_list = bpy.data.objects

# Call the dupframe function
dupframe()
delete_all_meshes_except_active()

# Append meshes back to the scene from the list
for obj in mesh_list:
    bpy.context.collection.objects.link(obj) # FIX THIS PART, IT DOES NOT APPEND

# Update the scene
bpy.context.view_layer.update()
