import bpy
import os
import math
from mathutils import Vector


OUT_DIR = "/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/wanderer-series/episodes/EP001_starliner/previs"
BLEND_PATH = OUT_DIR + "/EP001_starliner_route_whitebox.blend"
MOVIE_PATH = OUT_DIR + "/EP001_starliner_route_whitebox.mp4"
FRAME_DIR = OUT_DIR + "/render_frames_8s"


def material(name, rgba, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = rgba
    mat.metallic = metallic
    mat.roughness = roughness
    return mat


WHITE = material("White model", (0.78, 0.80, 0.82, 1))
LIGHT = material("Highlight", (0.95, 0.97, 1.0, 1))
DARK = material("Ground", (0.06, 0.07, 0.09, 1))
ROUTE = material("Route", (0.15, 0.70, 1.0, 1), metallic=0.2, roughness=0.3)
ALERT = material("Event marker", (1.0, 0.24, 0.08, 1), metallic=0.1, roughness=0.4)


def add_box(name, location, scale, mat=WHITE, bevel=0.12):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new("Soft model edges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    obj.data.materials.append(mat)
    return obj


def add_cylinder(name, location, radius, depth, mat=WHITE, vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def add_text(text, location, size=0.85):
    bpy.ops.object.text_add(location=location, rotation=(0, 0, 0))
    obj = bpy.context.object
    obj.name = text
    obj.data.body = text
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.extrude = 0.02
    obj.data.materials.append(LIGHT)
    return obj


def add_curve(name, points, bevel, mat):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 24
    curve.bevel_depth = bevel
    curve.bevel_resolution = 3
    spline = curve.splines.new("NURBS")
    spline.points.add(len(points) - 1)
    for p, co in zip(spline.points, points):
        p.co = (co[0], co[1], co[2], 1)
    spline.order_u = min(3, len(points))
    spline.use_endpoint_u = True
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def add_city(name, center, rows, cols, spacing=2.0, max_height=5.0):
    cx, cy = center
    for row in range(rows):
        for col in range(cols):
            x = cx + (col - (cols - 1) / 2) * spacing
            y = cy + (row - (rows - 1) / 2) * spacing
            height = 1.4 + ((row * 7 + col * 11) % 11) / 10 * max_height
            if (row + col) % 7 == 0:
                height *= 0.45
            add_box(f"{name}_block_{row}_{col}", (x, y, height / 2), (0.65, 0.65, height / 2), WHITE)


def add_ship():
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=(0, 0, 0))
    hull = bpy.context.object
    hull.name = "WANDERER starliner white model"
    hull.scale = (1.9, 0.9, 0.48)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    hull.data.materials.append(LIGHT)
    upper = add_box("Observation dome", (0.15, 0, 0.43), (0.82, 0.60, 0.30), WHITE, bevel=0.22)
    wing_l = add_box("Port stabilizer", (-0.15, 1.12, 0), (0.78, 0.12, 0.08), WHITE, bevel=0.05)
    wing_r = add_box("Starboard stabilizer", (-0.15, -1.12, 0), (0.78, 0.12, 0.08), WHITE, bevel=0.05)
    root = bpy.data.objects.new("Wanderer rig", None)
    bpy.context.collection.objects.link(root)
    for part in (hull, upper, wing_l, wing_r):
        part.parent = root
    return root


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


# Reset scene.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for block in (bpy.data.materials, bpy.data.curves, bpy.data.meshes, bpy.data.cameras, bpy.data.lights):
    pass

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
os.makedirs(FRAME_DIR, exist_ok=True)
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = FRAME_DIR + "/route_"
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 240
scene.world.color = (0.012, 0.015, 0.022)

# Base terrain.
add_box("White model terrain", (0, 0, -0.3), (23, 17, 0.3), DARK, bevel=0.3)

# Route: city safari -> mother ship battle -> jump gate -> infected city.
route_points = [(-18, -9, 1.2), (-12, -5, 2.0), (-7, -1, 2.4), (-1, 2.5, 3.0),
                (5, 4, 3.2), (10, 2.5, 2.8), (14, -2, 2.3), (18, -6, 1.5)]
add_curve("Fixed sightseeing route", route_points, 0.12, ROUTE)

# World 1: superhero city.
add_city("Hero city", (-9, -1), 5, 7, 2.0, 7.0)
add_text("01  HERO CITY", (-9, -8.2, 0.15), 0.85)
for pos in [(-12, 2.7, 1.0), (-8, 4.0, 1.0), (-5, 1.4, 1.0)]:
    add_cylinder("Battle event", pos, 0.6, 0.18, ALERT)

# World 2: mother ship battle zone.
add_city("Battle perimeter", (2.3, 5.8), 3, 5, 1.8, 4.2)
add_text("02  MOTHERSHIP", (3.0, 10.0, 0.15), 0.85)
mother = add_cylinder("Alien mother ship", (3.5, 5.5, 7.3), 4.5, 0.9, WHITE, 64)
mother.scale.z = 0.35
for angle in range(0, 360, 45):
    rad = math.radians(angle)
    add_cylinder("Mother ship cannon", (3.5 + math.cos(rad) * 2.7, 5.5 + math.sin(rad) * 2.7, 6.9), 0.25, 0.2, ALERT, 24)
for x, y in [(0.8, 2.2), (4.0, 2.0), (6.0, 5.0), (2.2, 8.6), (5.4, 8.3)]:
    add_cylinder("Hero action marker", (x, y, 0.5), 0.35, 1.0, WHITE, 16)

# World 3: jump gate and infected city.
add_text("03  JUMP GATE / INFECTED CITY", (15.2, -12.0, 0.15), 0.70)
bpy.ops.mesh.primitive_torus_add(major_radius=3.1, minor_radius=0.22, major_segments=48, minor_segments=12,
                                 location=(13.5, -3.5, 3.5), rotation=(math.radians(90), 0, math.radians(20)))
gate = bpy.context.object
gate.name = "Jump gate"
gate.data.materials.append(ROUTE)
add_city("Infected city", (17, -8.5), 3, 4, 1.8, 4.0)
for index in range(20):
    angle = math.radians(index * 43)
    radius = 1.6 + (index % 4) * 0.45
    add_cylinder("Infected crowd marker", (17 + math.cos(angle) * radius, -8.5 + math.sin(angle) * radius, 0.18), 0.13, 0.36, WHITE, 12)

# Waypoint pylons.
for label, loc in [("START", route_points[0]), ("CITY", route_points[2]), ("BATTLE", route_points[4]), ("GATE", route_points[6]), ("END", route_points[7])]:
    add_cylinder(label + " waypoint", (loc[0], loc[1], 0.6), 0.25, 1.2, ROUTE, 20)
    add_text(label, (loc[0], loc[1] - 0.8, 1.3), 0.38)

# Animated ship following the fixed path.
ship = add_ship()
for frame, point, yaw in [(1, route_points[0], math.radians(42)), (45, route_points[2], math.radians(35)),
                          (110, route_points[4], math.radians(6)), (180, route_points[6], math.radians(-45)),
                          (240, route_points[7], math.radians(-55))]:
    ship.location = point
    ship.rotation_euler = (0, 0, yaw)
    ship.keyframe_insert(data_path="location", frame=frame)
    ship.keyframe_insert(data_path="rotation_euler", frame=frame)
# Camera: overhead survey move that keeps full route readable.
bpy.ops.object.camera_add(location=(0, -30, 46))
camera = bpy.context.object
camera.name = "Previs camera"
scene.camera = camera
camera.data.type = "ORTHO"
camera.data.ortho_scale = 44
look_at(camera, (0, -1.5, 0))

# Lighting.
bpy.ops.object.light_add(type="AREA", location=(0, -2, 28))
key = bpy.context.object
key.name = "Softbox key"
key.data.energy = 2200
key.data.shape = "DISK"
key.data.size = 26
key.data.color = (0.78, 0.86, 1.0)
look_at(key, (0, 0, 0))
bpy.ops.object.light_add(type="AREA", location=(-18, -8, 10))
fill = bpy.context.object
fill.data.energy = 900
fill.data.size = 12
fill.data.color = (1.0, 0.35, 0.15)
look_at(fill, (-8, 0, 0))

# Timeline markers for review.
for frame, name in [(1, "START - approach hero city"), (45, "hero city overview"), (110, "mother ship battle"),
                    (180, "jump gate"), (240, "infected city arrival")]:
    scene.timeline_markers.new(name, frame=frame)

bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
bpy.ops.render.render(animation=True)
