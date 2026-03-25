import bpy 
import os
import math

def stworzLodyge(wysokosc, r,  x, y, mat):
    bpy.ops.mesh.primitive_cylinder_add(
        radius = r,
        depth = 1.0,
        location=(x,y,wysokosc/2)
    )
    lodyga = bpy.context.active_object
    lodyga.scale.z = wysokosc
    lodyga.data.materials.append(mat)

def stworzLiscie(wysokosc, liczbaLisci, promienLisci, x, y, r, mat):
    for i in range(liczbaLisci):
        alpha = i * 2 * math.pi / liczbaLisci

        xp = r * math.cos(alpha)
        yp = r * math.sin(alpha)

        bpy.ops.mesh.primitive_cube_add(
            size = promienLisci,
            location=(x + xp,y + yp,wysokosc)
        )

        lisc = bpy.context.active_object
        lisc.rotation_euler = (14,17,0)
        lisc.data.materials.append(mat)

def stworzKorzenie(liczbaKorzeni, x, y, r, mat):
    for i in range(liczbaKorzeni):
        alpha = i * 2 * math.pi / liczbaKorzeni

        xp = r * math.cos(alpha)
        yp = r * math.sin(alpha)

        bpy.ops.mesh.primitive_cube_add(
            size = 0.2,
            location=(x + xp,y + yp,0.1)
        )

        korzen = bpy.context.active_object
        korzen.data.materials.append(mat)

def stworzrosline(wysokosc = 1.5, liczbaLisci = 3, promienLisci = 0.3, liczbaKorzeni = 4, x = 0, y = 0, r = 0.14):

    matLodyga = bpy.data.materials.new(name='Lodyga')
    matLodyga.use_nodes = True
    bsdf = matLodyga.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (151/255,225/255,127/255,1)
    bsdf.inputs["Metallic"].default_value = 0.6
    bsdf.inputs["Roughness"].default_value = 0

    matLiscie = bpy.data.materials.new(name='Liscie')
    matLiscie.use_nodes = True
    bsdf1 = matLiscie.node_tree.nodes["Principled BSDF"]
    bsdf1.inputs["Base Color"].default_value = (83/255,194/255,46/255,1)
    bsdf1.inputs["Metallic"].default_value = 0
    bsdf1.inputs["Roughness"].default_value = 0

    matKorzenie = bpy.data.materials.new(name='Korzenie')
    matKorzenie.use_nodes = True
    bsdf2 = matKorzenie.node_tree.nodes["Principled BSDF"]
    bsdf2.inputs["Base Color"].default_value = (102/255,51/255,0,1)
    bsdf2.inputs["Metallic"].default_value = 0
    bsdf2.inputs["Roughness"].default_value = 1

    stworzLodyge(wysokosc, r, x, y, matLodyga)

    stworzLiscie(wysokosc, liczbaLisci, promienLisci, x, y, r, matLiscie)

    stworzKorzenie(liczbaKorzeni, x, y, r, matKorzenie)


# czyszczenie sceny 
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

stworzrosline(1.5,3,0.3,4)
stworzrosline(1,3,0.3,4,0,-2)
stworzrosline(2,3,0.4,4,0,2)

# światło
bpy.ops.object.light_add(type='SUN', location=(3, 3, 8))
sun = bpy.context.active_object
sun.rotation_euler = (0.9, 0.2, 0.5)
sun.data.energy = 1.5

# Kamera 
bpy.ops.object.camera_add(location=(5, -4.5, 4))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.8)
bpy.context.scene.camera = camera

# render do PNG
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.filepath = os.path.abspath("rosliny_lab04.png")
scene.render.image_settings.file_format = 'PNG'
scene.render.resolution_x = 800
scene.render.resolution_y = 600
bpy.ops.render.render(write_still=True)

print("Render zapisany: rosliny_lab04.png")
