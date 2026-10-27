"""Ejecutar con Blender -b BASE --python este_script. Solo guarda ANALISIS."""
import bpy, math, json, hashlib
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'blender/Miranda_Puente_Sutherland_Analisis.blend'
assert Path(bpy.data.filepath).name=='Miranda_Puente_Sutherland_Base.blend'
original=list(bpy.data.objects)
def fingerprint(o):
    d={'type':o.type,'parent':o.parent.name if o.parent else None,'matrix':[list(r) for r in o.matrix_world],
       'materials':[s.material.name if s.material else None for s in o.material_slots]}
    if o.type=='MESH':d.update(vertices=[list(v.co) for v in o.data.vertices],polygons=[list(p.vertices) for p in o.data.polygons])
    return hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()
before={o.name:fingerprint(o) for o in original}
vis={o.name:(o.hide_render,o.hide_get()) for o in original}
refs=bpy.data.collections.new('ANALISIS_REFERENCIAS_NO_EXPORTAR');bpy.context.scene.collection.children.link(refs)
labels=bpy.data.collections.new('ANALISIS_ROTULOS');bpy.context.scene.collection.children.link(labels)
cameras=bpy.data.collections.new('ANALISIS_CAMARAS');bpy.context.scene.collection.children.link(cameras)
groups={}; metadata=[]
CYAN=(.03,.65,.95,1);ORANGE=(1,.3,.03,1)
def move(o,col):
    for c in list(o.users_collection):c.objects.unlink(o)
    col.objects.link(o)
def cylinder(a,b,r,name,color,verts=12):
    a=Vector(a);b=Vector(b)
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=(b-a).length,location=(a+b)/2)
    o=bpy.context.object;o.name=name;o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();o.color=color;move(o,refs);return o
def mannequin(tag,h,foot,angle,color):
    prefix='REF_'+tag;parts=[];foot=Vector(foot)
    def p(x,y,z):return foot+Vector((x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle),z))*h
    def rod(a,b,r,label):parts.append(cylinder(p(*a),p(*b),r*h,prefix+'_'+label,color))
    for s in [-1,1]:
        rod((s*.065,0,.03),(s*.065,0,.45),.034,'pierna')
        rod((s*.13,0,.77),(s*.17,0,.49),.026,'brazo')
        rod((s*.065,-.025,.025),(s*.065,.055,.025),.025,'pie')
    rod((0,0,.44),(0,0,.79),.12,'tronco')
    rod((0,0,.77),(0,0,.87),.035,'cuello')
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.07*h,location=p(0,0,.93))
    head=bpy.context.object;head.name=prefix+'_cabeza';head.color=color;move(head,refs);parts.append(head)
    # Regla lateral exacta: pies z=0, remate z=h, marcas cada 50 cm.
    rod((.25,0,0),(.25,0,1),.006,'altura_exacta')
    for z in [0,h]+[v*.5 for v in range(1,int(h/.5)+1)]:
        parts.append(cylinder(p(.22,0,z/h),p(.28,0,z/h),.009,prefix+'_marca',color))
    for o in parts:o['analysis_only']=True;o['height_reference_cm']=h*100
    lo=min((o.matrix_world@Vector(c)).z for o in parts for c in o.bound_box)
    hi=max((o.matrix_world@Vector(c)).z for o in parts for c in o.bound_box)
    # La regla lleva marcas con grosor: la estatura se define por pies y cabeza, no por las marcas.
    metadata.append({'id':tag,'height_cm':h*100,'feet_world_cm':[x*100 for x in foot],'head_top_world_cm':(foot.z+h)*100,'note':'Altura exacta pies-cabeza. Silueta esquematica; anchura y postura no antropometricas.'})
    return parts
positions={
 'capitan':[((-.95,-2.7,.299),0),((.95,-2.7,.299),0)],
 'central':[((-2,-5.25,0),0),((2,-5.25,0),0)],
 'lateral':[((5.28,-4.7,0),math.pi/2),((5.28,-2.7,0),math.pi/2)],
 'puerta_turbo':[((-4.9,-8.95,0),math.pi/2),((-4.9,-7.6,0),math.pi/2)],
 'cabina':[((-8.15,-9.55,.001001),math.pi/2),((-8.15,-7.9,.001001),math.pi/2)],
 'puerta_Ypos':[((5.8,.3,.6),math.pi/2),((5.8,1.25,.6),math.pi/2)]}
for zone,pp in positions.items():
    groups[zone]=[]
    for (name,h,color),(foot,ang) in zip([('Quinn',1.773,CYAN),('Alto',2.5,ORANGE)],pp):
        groups[zone]+=mannequin(zone+'_'+name,h,foot,ang,color)
bpy.context.view_layer.update()
sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH';sc.render.image_settings.file_format='PNG'
sc.render.resolution_x=1800;sc.render.resolution_y=1400;sc.render.resolution_percentage=100
sh=sc.display.shading;sh.light='STUDIO';sh.color_type='OBJECT';sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='BOTH'
sh.background_type='WORLD';sc.world.color=(.10,.10,.10);sc.view_settings.view_transform='Standard'
camdata=bpy.data.cameras.new('ANALISIS_Vista');cam=bpy.data.objects.new('ANALISIS_Vista',camdata);cameras.objects.link(cam);sc.camera=cam
roof=[o for o in original if o.type=='MESH' and min((o.matrix_world@Vector(c)).z for c in o.bound_box)>3.8]
def text_label(body,location,size=.17,color=(1,1,.8,1),top=False):
    data=bpy.data.curves.new('ANALISIS_Texto','FONT');data.body=body;data.size=size;data.align_x='CENTER'
    o=bpy.data.objects.new('ANALISIS_'+body,data);labels.objects.link(o);o.location=location;o.color=color
    o.rotation_euler=(0,0,0) if top else cam.rotation_euler
    if hasattr(o.display,'show_shadows'):o.display.show_shadows=False
    return o
def render(name,eye,target,zones,ortho=None,cut=False,open_door=False,lens=26):
    for o in original:o.hide_render=vis[o.name][0]
    for o in roof:o.hide_render=cut or vis[o.name][0]
    if open_door:
        for n in ['Plane.018_0','Plane.019_0']:bpy.data.objects[n].hide_render=True
    for zone,oo in groups.items():
        for o in oo:o.hide_render=zone not in zones
    for o in labels.objects:o.hide_render=True
    cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    camdata.type='ORTHO' if ortho else 'PERSP';camdata.ortho_scale=ortho or 20;camdata.lens=lens;camdata.clip_start=.05;camdata.clip_end=200
    if ortho:
        for body,loc in [('PODIO +29.9 cm',(0,-.4,3.2)),('CONSOLA 143.9 cm',(0,-4.15,3.2)),('TURBO',(-8.1,-8.7,5)),('+Y',(7,2.5,5)),('+X',(8,-4,5))]:text_label(body,loc,.22,top=True)
    else:
        # Leyenda sobreimpresa mediante texto de cámara, sin tocar materiales del puente.
        rotation=cam.rotation_euler.to_matrix();depth=2
        # Campo vertical visible en el plano a 2 m: sensor horizontal / aspect.
        width=camdata.sensor_width/1000*depth/(lens/1000);height=width*sc.render.resolution_y/sc.render.resolution_x
        for body,col,offset in [('Quinn 177.3 cm',CYAN,.45),('Humanoide 250 cm',ORANGE,.40)]:
            text_label(body,cam.location+rotation@Vector((0,height*offset,-depth)),width*.025,col)
    sc.render.filepath=str(ROOT/'capturas'/name);bpy.ops.render.render(write_still=True)
render('01_cenital_referencias.png',(-1.8,-4.3,26),(-1.8,-4.3,0),list(groups),20.5,True)
render('02_capitan_podio.png',(0,-6.7,2.65),(0,-1.9,1.65),['capitan'],lens=25)
render('03_consolas_centrales.png',(0,-9.6,2.9),(0,-3.6,1.4),['central'],lens=21)
render('04_puestos_laterales.png',(3.1,-3.7,2.2),(5.8,-3.7,1.45),['lateral'],lens=17)
render('05_puerta_turbo_cerrada.png',(-1.5,-8.6,2.65),(-5.9,-8.3,1.9),['puerta_turbo'],lens=25)
render('06_turbo_interior.png',(-5.4,-8.33,2.6),(-8.8,-8.7,2),['cabina'],open_door=True,lens=20)
render('07_puerta_Ypositivo.png',(2.7,.87,2.8),(6.49,.87,2.5),['puerta_Ypos'],lens=22)
# Guardado independiente: techos ocultos para inspección, geometría original intacta.
for o in original:o.hide_render=vis[o.name][0];o.hide_set(vis[o.name][1])
for o in roof:o.hide_render=True;o.hide_set(True)
for oo in groups.values():
    for o in oo:o.hide_render=False;o.hide_set(False)
for o in labels.objects:o.hide_render=True;o.hide_set(True)
cam.location=(-1.8,-4.3,26);cam.rotation_euler=(0,0,0);camdata.type='ORTHO';camdata.ortho_scale=20.5
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_distance=20
            area.spaces.active.region_3d.view_location=Vector((-1.8,-4.3,0))
            area.spaces.active.region_3d.view_rotation=(1,0,0,0)
            area.spaces.active.shading.color_type='OBJECT'
after={o.name:fingerprint(o) for o in original}
assert before==after,'Se detectó una modificación en originales'
bpy.context.preferences.filepaths.save_version=0
assert OUT.name!='Miranda_Puente_Sutherland_Base.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),copy=True)
(ROOT/'datos/referencias.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
(ROOT/'datos/verificacion_en_memoria.json').write_text(json.dumps({'original_objects':len(original),'unchanged':before==after,'fingerprints':after,'roof_hidden_for_inspection':[o.name for o in roof],'analysis_copy':str(OUT)},indent=2),encoding='utf-8')
print('ANALISIS_GUARDADO',OUT)
