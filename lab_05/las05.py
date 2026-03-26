import bpy 
import os
import math
import random

TYPY_ROSLIN = {
    "drzewo": {
        "wysokosc": (3.0, 5.0),
        "liczba_lisci": (4, 6),
        "promien_lisci": (0.4, 0.7),
        "liczba_korzeni": (4, 6),
        "kolor_lodygi": (0.15, 0.08, 0.02, 1),
        "kolor_lisci": (0.05, 0.35, 0.1, 1),
    },

    "krzew": {
        "wysokosc": (0.8, 1.8, 5.0),
        "liczba_lisci": (5, 8),
        "promien_lisci": (0.5, 0.9),
        "liczba_korzeni": (2, 4),
        "kolor_lodygi": (0.25, 0.15, 0.05, 1),
        "kolor_lisci": (0.1, 0.5, 0.05, 1),
    },

    "paproc": {
        "wysokosc": (0.5, 1.2),
        "liczba_lisci": (6, 10),
        "promien_lisci": (0.6, 1.0),
        "liczba_korzeni": (2, 3),
        "kolor_lodygi": (0.2, 0.3, 0.1, 1),
        "kolor_lisci": (0.0, 0.6, 0.15,1),
    },

}

def stworzLodyge(mat, wysokosc = 1.5, r = 0.14, x = 0, y = 0):
    bpy.ops.mesh.primitive_cylinder_add(
        radius = r,
        depth = 1.0,
        location=(x,y,wysokosc/2)
    )
    lodyga = bpy.context.active_object
    lodyga.scale.z = wysokosc
    lodyga.data.materials.append(mat)

    return (lodyga)

def stworzLiscie(mat, wysokosc = 1.5, liczbaLisci = 3, promienLisci = 0.3, x = 0, y = 0, r = 0.14):
    liscie = []

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

        liscie.append(lisc)

    return liscie

def stworzKorzenie(mat, liczbaKorzeni = 4, x = 0, y = 0, r = 0.14):
    korzenie = []
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
        korzenie.append(korzen)

    return korzenie

def stworzrosline(wysokosc = 1.5, liczbaLisci = 3, promienLisci = 0.3, liczbaKorzeni = 4, kolor_lodygi = (0.151, 0.255, 0.127), kolor_lisci = (0.083, 0.194, 0.046), x = 0, y = 0, r = 0.14):
    # materiał łodygi
    matLodyga = bpy.data.materials.new(name='Lodyga')
    matLodyga.use_nodes = True
    bsdf = matLodyga.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = kolor_lodygi
    bsdf.inputs["Metallic"].default_value = 0.6
    bsdf.inputs["Roughness"].default_value = 0

    # materiał liści
    matLiscie = bpy.data.materials.new(name='Liscie')
    matLiscie.use_nodes = True
    bsdf1 = matLiscie.node_tree.nodes["Principled BSDF"]
    bsdf1.inputs["Base Color"].default_value = kolor_lisci
    bsdf1.inputs["Metallic"].default_value = 0
    bsdf1.inputs["Roughness"].default_value = 0

    matKorzenie = bpy.data.materials.new(name='Korzenie')
    matKorzenie.use_nodes = True
    bsdf2 = matKorzenie.node_tree.nodes["Principled BSDF"]
    bsdf2.inputs["Base Color"].default_value = (0.116,0.069,0,1)
    bsdf2.inputs["Metallic"].default_value = 0
    bsdf2.inputs["Roughness"].default_value = 1

    lodyga = stworzLodyge(matLodyga, wysokosc, r, x, y)

    liscie = stworzLiscie(matLiscie, wysokosc, liczbaLisci, promienLisci,  x, y, r)

    korzenie = stworzKorzenie(matKorzenie, liczbaKorzeni,  x, y, r)

    return (lodyga, liscie, korzenie)

def stworzroslinetyp(x = 0, y = 0, typ = "drzewo"):
    wysokosc = random.uniform(TYPY_ROSLIN[typ]["wysokosc"][0], TYPY_ROSLIN[typ]["wysokosc"][1])
    liczba_lisci = random.randint(TYPY_ROSLIN[typ]["liczba_lisci"][0], TYPY_ROSLIN[typ]["liczba_lisci"][1])
    promien_lisci = random.uniform(TYPY_ROSLIN[typ]["promien_lisci"][0], TYPY_ROSLIN[typ]["promien_lisci"][1])
    liczba_korzeni = random.randint(TYPY_ROSLIN[typ]["liczba_korzeni"][0], TYPY_ROSLIN[typ]["liczba_korzeni"][1])
    kolor_lodygi = TYPY_ROSLIN[typ]["kolor_lodygi"]
    kolor_lisci = TYPY_ROSLIN[typ]["kolor_lisci"]

    roslina = stworzrosline(wysokosc, liczba_lisci, promien_lisci, liczba_korzeni, kolor_lodygi, kolor_lisci, x, y)

    return roslina

def wybierztypbiomu(x, y, rozmiar_pola):
    if abs(x) < 0.3 * (rozmiar_pola / 2) and abs(y) < 0.3 * (rozmiar_pola / 2):
        print("drzewo")
        return "drzewo"
    elif (abs(x) > 0.3 * (rozmiar_pola / 2) and abs(x) < 0.7 * (rozmiar_pola / 2)) or (abs(y) > 0.3 * (rozmiar_pola / 2) and abs(y) < 0.7 * (rozmiar_pola / 2)):
        rand = random.random()
        if rand < 0.7:
            print("krzew")
            return "krzew"
        else: 
            print("drzewo")
            return "drzewo"
    else:
        rand = random.random()
        if rand < 0.5:
            print("krzew")
            return "krzew"
        else:
            print("paproc")
            return "paproc"

def generujLas(liczbaroslin = 18, rozmiar_pola = 10.0, seed = 42):
    random.seed(seed)
    # czyszczenie sceny 
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

    # tworzenie kolekcji 
    Las = bpy.data.collections.new("Las")
    bpy.context.scene.collection.children.link(Las)

    # generowanie lasu
    for i in range(liczbaroslin):
        # losowanie pozycji rosliny 
        x = random.uniform(-rozmiar_pola, rozmiar_pola)
        y = random.uniform(-rozmiar_pola, rozmiar_pola)

        # typ rosliny 
        typ = wybierztypbiomu(x, y, rozmiar_pola)

        # generowanie rośliny 
        lodyga, liscie, korzenie = stworzroslinetyp(x, y, typ)

        # dodawanie do kolekcji
        Las.objects.link(lodyga)

        for lisc in liscie:
            Las.objects.link(lisc)

        for korzen in korzenie:
            Las.objects.link(korzen)

    # światło 
    bpy.ops.object.light_add(type='SUN', location=(3, 3, 8))
    sun = bpy.context.active_object
    sun.rotation_euler = (0.9, 0.2, 0.5)
    sun.data.energy = 1.5

    # Kamera 
    bpy.ops.object.camera_add(location=(15, -14.5, 10))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 1.0)
    bpy.context.scene.camera = camera

    # render do PNG
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.render.filepath = os.path.abspath('las_05.png')
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = 800
    scene.render.resolution_y = 600
    bpy.ops.render.render(write_still=True)

    print("Render zapisany: las_05.png")


# generowanie lasu
generujLas()