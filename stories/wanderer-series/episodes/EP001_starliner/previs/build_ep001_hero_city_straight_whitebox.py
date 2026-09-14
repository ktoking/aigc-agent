import bpy
import os
import math
from mathutils import Vector

OUT = "/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/wanderer-series/episodes/EP001_starliner/previs"
BLEND = OUT + "/EP001_starliner_hero-city_straight_whitebox_v2.blend"
FRAMES = OUT + "/hero_city_straight_frames_v2"


def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = color
    return m


WHITE = mat("white model", (0.78, 0.80, 0.82, 1))
ROUTE = mat("fixed route", (0.08, 0.62, 1.0, 1))
EVENT = mat("battle event", (1.0, 0.25, 0.08, 1))
DARK = mat("ground", (0.055, 0.065, 0.08, 1))


def cube(name, loc, scale, material=WHITE):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    bevel = o.modifiers.new("model edge", "BEVEL")
    bevel.width = 0.08
    bevel.segments = 2
    return o


def cylinder(name, loc, radius, depth, material=WHITE):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    return o


def text(label, loc, size=0.5):
    bpy.ops.object.text_add(location=loc)
    o = bpy.context.object
    o.data.body = label
    o.data.align_x = "CENTER"
    o.data.align_y = "CENTER"
    o.data.size = size
    o.data.extrude = 0.02
    o.data.materials.append(WHITE)
    return o


def curve(points):
    c = bpy.data.curves.new("Straight fixed sightseeing route", "CURVE")
    c.dimensions = "3D"
    c.bevel_depth = 0.15
    c.bevel_resolution = 3
    s = c.splines.new("POLY")
    s.points.add(1)
    for point, co in zip(s.points, points):
        point.co = (*co, 1)
    o = bpy.data.objects.new("Straight fixed sightseeing route", c)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(ROUTE)


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
os.makedirs(FRAMES, exist_ok=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = "WORLD"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = FRAMES + "/hero_"
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 180
scene.world.color = (0.025, 0.03, 0.04)

# City is one continuous corridor. The line never turns or changes speed.
cube("city base", (0, 0, -0.45), (23, 10, 0.45), DARK)
cube("straight city avenue", (0, 0, 0.02), (21, 1.6, 0.06), WHITE)
for side in (-1, 1):
    for index, x in enumerate(range(-18, 20, 3)):
        h = 2.0 + ((index * 3) % 6)
        y = side * (3.2 + (index % 2) * 1.2)
        cube("city tower", (x, y, h / 2), (0.9, 0.85, h / 2), WHITE)
        cube("tower roof step", (x, y, h + 0.18), (0.48, 0.46, 0.18), WHITE)
        cube("tower roof unit", (x + 0.28, y - 0.22 * side, h + 0.46), (0.16, 0.14, 0.12), WHITE)
        # Staggered annexes make each city block legible in a white model.
        annex_h = 0.9 + (index % 3) * 0.55
        cube("tower annex", (x + 1.06, y - side * 0.28, annex_h / 2), (0.36, 0.42, annex_h / 2), WHITE)
        for level in range(1, int(h)):
            cube("tower facade band", (x, y - side * 0.88, level), (0.76, 0.035, 0.028), DARK)

# Road furniture makes the otherwise abstract straight corridor read as an urban route.
for x in range(-18, 20, 2):
    cube("avenue lane marker", (x, 0, 0.12), (0.42, 0.035, 0.025), DARK)
for x in range(-17, 20, 4):
    for side in (-1, 1):
        cylinder("streetlight", (x, side * 2.15, 0.62), 0.055, 1.2, WHITE)

# Event nodes are beside, not on, the fixed route.
for x, label in [(-14, "ARRIVAL"), (-7, "FIVE HERO BATTLE"), (2, "MOTHERSHIP FIRE"),
                 (10, "MOTHERSHIP FALL"), (17, "JUMP EXIT")]:
    cylinder(label + " node", (x, 0, 0.18), 0.46, 0.24, EVENT)
    text(label, (x, -3.3, 0.2), 0.42)

# Simplified hero and invader markers flank the route at the battle node.
for i, (x, y) in enumerate([(-7, 3.0), (-5.5, -3.0), (-4, 3.0), (-2.5, -3.0), (-1, 3.0)]):
    cylinder("hero marker", (x, y, 0.8), 0.25, 1.6, WHITE)
for i, (x, y) in enumerate([(-6, 5.0), (-4, 5.0), (-2, 5.0), (0, 5.0), (2, 5.0), (4, 5.0)]):
    cylinder("alien invader marker", (x, y, 0.7), 0.22, 1.4, EVENT)

# Mother ship stays above the same city corridor: an event, never a route turn.
# Layered rings and a recessed core retain readable structure in white-box overhead view.
cylinder("mother ship lower disk", (6.0, 0, 6.75), 4.65, 0.42, WHITE)
cylinder("mother ship main disk", (6.0, 0, 7.12), 3.95, 0.48, WHITE)
cylinder("mother ship command core", (6.0, 0, 7.55), 1.22, 0.52, DARK)
for radius, z in [(3.35, 7.42), (2.25, 7.50)]:
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=0.10, major_segments=48, minor_segments=12,
                                     location=(6.0, 0, z))
    bpy.context.object.name = "mother ship hull ring"
    bpy.context.object.data.materials.append(DARK)
for angle in range(0, 360, 45):
    r = math.radians(angle)
    x = 6 + math.cos(r) * 2.9
    y = math.sin(r) * 2.9
    cylinder("mother ship cannon housing", (x, y, 7.5), 0.42, 0.22, DARK)
    cylinder("mother ship cannon aperture", (x, y, 7.64), 0.20, 0.10, EVENT)
    cube("mother ship radial fin", (6 + math.cos(r) * 4.05, math.sin(r) * 4.05, 7.05), (0.32, 0.16, 0.13), WHITE)

# Exit is an in-place interior jump event at the end of the straight run.
bpy.ops.mesh.primitive_torus_add(major_radius=1.35, minor_radius=0.14, major_segments=40, minor_segments=12,
                                 location=(18.5, 0, 1.6), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(ROUTE)

curve([(-20, 0, 0.28), (20, 0, 0.28)])

# Low-poly Wanderer with a clearly visible forward arrow, animated linearly only along X.
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=(-20, 0, 0.8))
ship = bpy.context.object
ship.name = "WANDERER - constant speed straight flight"
ship.scale = (1.45, 0.74, 0.4)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
ship.data.materials.append(WHITE)
cube("ship viewing dome", (-20.0, 0, 1.22), (0.64, 0.48, 0.24), WHITE)
for frame, x in [(1, -20), (180, 20)]:
    ship.location = (x, 0, 0.8)
    ship.keyframe_insert(data_path="location", frame=frame)
# Orthographic overhead survey: fully readable one-line route.
bpy.ops.object.camera_add(location=(0, -25, 35))
camera = bpy.context.object
camera.data.type = "ORTHO"
camera.data.ortho_scale = 44
scene.camera = camera
look_at(camera, (0, 0, 0))

bpy.ops.object.light_add(type="AREA", location=(0, -6, 25))
light = bpy.context.object
light.data.energy = 1900
light.data.shape = "DISK"
light.data.size = 30
look_at(light, (0, 0, 0))

for frame, label in [(1, "EP001 arrival"), (55, "five hero battle"), (110, "mother ship event"),
                     (150, "mother ship fall"), (180, "interior jump exit")]:
    scene.timeline_markers.new(label, frame=frame)

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
bpy.ops.render.render(animation=True)
