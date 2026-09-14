import bpy
import math
from pathlib import Path
from mathutils import Vector

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
def material(name, rgb):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    return m
WHITE = material('clay', (.77,.80,.81))
BLUE = material('route', (.04,.43,.76))
BASE = material('seabed', (.46,.55,.59))
DARK = material('trench', (.18,.26,.30))
ORANGE = material('pod', (.95,.40,.10))
def cube(name, p, s, m=WHITE):
    bpy.ops.mesh.primitive_cube_add(location=p)
    o=bpy.context.object; o.name=name; o.scale=s; o.data.materials.append(m)
    return o
def sphere(name, p, s, m=WHITE):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=p)
    o=bpy.context.object; o.name=name; o.scale=s; o.data.materials.append(m)
    return o
def line(name, points, radius=.10, m=WHITE):
    c=bpy.data.curves.new(name,'CURVE'); c.dimensions='3D'; c.bevel_depth=radius; c.bevel_resolution=2
    sp=c.splines.new('POLY'); sp.points.add(len(points)-1)
    for v,p in zip(sp.points,points): v.co=(*p,1)
    o=bpy.data.objects.new(name,c); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    return o
def label(body,p,size=.75):
    bpy.ops.object.text_add(location=p)
    o=bpy.context.object; o.data.body=body; o.data.size=size; o.data.align_x='CENTER'; o.data.materials.append(DARK)
def ring(p,r):
    return line('transit ring',[(p[0],p[1]+r*math.cos(a*math.tau/48),p[2]+r*math.sin(a*math.tau/48)) for a in range(49)],.16)
def position(t): return (-30+t,0,4-t*.045)

# Spatially compressed storyboard model, not a geographic survey.
cube('seafloor', (0,0,-2),(33,10,.5), BASE)
cube('fault opening',(7,4,-1.46),(4,3,.04),DARK)
for x in range(-29,31,3):
    for side in [-1,1]:
        z=.4+(x%5)*.20
        sphere('seabed rock',(x,side*7,-1.1),(1.3,.8,z),BASE)
for x in [-28,-26,-24]:
    for y in [3,5]: line('seagrass',[(x,y,-1.5),(x+.2,y,-.4),(x-.1,y,.3)],.05)
for x in [-23,-21,-19]: ring((x,0,3.55),2.4)

# 12-21 s: canyon, submerged architecture and a large seated statue.
for x in [-16,-13,-10]:
    for y in [4.0,6.0]:
        cube('ruin pillar',(x,y,.4),(.38,.4,1.8))
    cube('ruin lintel',(x,5,2.25),(.5,1.6,.3))
for i in range(4): cube('ruin stair',(-12,-5,-1.1+i*.35),(2-i*.3,2-i*.3,.2))
cube('statue seat',(-12,-5,.5),(1.1,1,1))
cube('statue torso',(-12,-5,2.3),(.75,.55,1.2))
sphere('statue head',(-12,-5,4),(.65,.58,.8))
for y in [-5.8,-4.2]:
    cube('statue legs',(-11.2,y,.5),(.4,.3,1.2))
    line('statue arm',[(-12,y,3),(-11.2,y,2),(-10.8,y,1.7)],.25)

# 21-30 s: varied organisms beside a clear travel corridor.
for i in range(9):
    x=-8+i*.9; y=3+(i%3)*.7; z=2+(i%2)*.8
    o=sphere('leader organism',(x,y,z),(.65,.18,.28))
    line('organism tail',[(x-.4,y,z),(x-1,y,z+.1)],.04)

# 30-40 s: volcanic cone, vents and fault edge.
bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=2.5,radius2=.6,depth=2.5,location=(3,-5,-.25))
bpy.context.object.data.materials.append(WHITE)
ring_obj=line('volcano rim',[(3+.6*math.cos(a*math.tau/40),-5+.6*math.sin(a*math.tau/40),1.0) for a in range(41)],.12,DARK)
for i in range(3):
    cube('hydrothermal chimney',(6+i,-5+i*.3,-.1),(.25,.25,1.4))
    line('vent plume',[(6+i,-5+i*.3,1.3),(6.3+i,-5,2.3),(6.8+i,-4.8,3.5)],.18,BASE)
for x in [4,7,10]: cube('fault cliff',(x,7,-.5),(1.3,.5,1.0))

# 40-48 s: giant skeleton and ribbon animal.
line('skeleton spine',[(x,-5,-.4) for x in range(11,19)],.18)
for x in range(12,19):
    line('rib',[(x,-5+1.7*math.cos(a*math.pi/16),-.8+1.8*math.sin(a*math.pi/16)) for a in range(17)],.09)
sphere('ancient skull',(10.5,-5,-.3),(1.1,.8,.6))
line('ribbon organism',[(11+i*.25,4+math.sin(i*.3),2+.3*math.cos(i*.3)) for i in range(30)],.22)

# 48-56 s: huge animal kept beside the route. Separate animation conveys passing.
giant=sphere('passing giant',(23,5,3),(5.2,1.3,1.1))
line('giant fin',[(23,5,3),(24,8,2.6),(21,5,2.8)],.25)
for i in range(7): line('filter plates',[(19+i*.35,4,2.9),(19+i*.35,4,3.6)],.05,DARK)
for frame,y in [(1,5),(577,5),(673,7.5),(720,9)]:
    giant.location.y=y; giant.keyframe_insert(data_path='location',frame=frame)

line('fixed route',[position(t) for t in range(61)],.12,BLUE)
pod=sphere('ABYSS pod',position(0),(.75,.75,.75),ORANGE)
for frame,t in [(1,0),(720,60)]:
    pod.location=position(t); pod.keyframe_insert(data_path='location',frame=frame)
for o in [pod,giant]:
    action=o.animation_data.action
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points: k.interpolation='LINEAR'
labels=[(-27,'00-07s\nSHALLOW'),(-20.5,'07-12s\nTRANSIT'),(-13.5,'12-21s\nRUINS'),(-4.5,'21-30s\nLIFE'),(5,'30-40s\nVOLCANO / FAULT'),(14,'40-48s\nREMAINS'),(22,'48-56s\nGIANTS'),(28,'56-60s\nEXIT')]
for x,title in labels: label(title,(x,-12,0),.65)
label('EP002 ABYSS | 60s ROUTE PREVIS',(0,11,0),1.1)
label('SPACE COMPRESSED - BLUE: ROUTE / ORANGE: POD',(0,-16,0),.65)
scene=bpy.context.scene
scene.render.engine='BLENDER_WORKBENCH'
scene.display.shading.light='STUDIO'; scene.display.shading.color_type='MATERIAL'
scene.display.shading.show_shadows=True; scene.display.shading.show_cavity=True
scene.display.shading.background_type='WORLD'; scene.world.color=(.78,.83,.85)
scene.render.resolution_x=1280; scene.render.resolution_y=720; scene.render.resolution_percentage=100
scene.render.fps=12; scene.frame_start=1; scene.frame_end=720
bpy.ops.object.camera_add(location=(0,-39,58))
cam=bpy.context.object; cam.data.type='ORTHO'; cam.data.ortho_scale=72
cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler(); scene.camera=cam
for sec,title in [(0,'SHALLOW'),(7,'TRANSIT'),(12,'RUINS'),(21,'LIFE'),(30,'SEGMENT 02 / VOLCANO'),(40,'REMAINS'),(48,'GIANTS'),(56,'EXIT')]:
    scene.timeline_markers.new(title,frame=sec*12+1)
scene.render.image_settings.file_format='PNG'
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'EP002_abyss_route_v1.blend'))
scene.render.filepath=str(OUT/'route_overview.png'); bpy.ops.render.render(write_still=True)
scene.render.resolution_percentage=75
(OUT/'render').mkdir(exist_ok=True)
scene.render.filepath=str(OUT/'render/frame_')
bpy.ops.render.render(animation=True)
