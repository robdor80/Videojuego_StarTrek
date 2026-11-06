import bpy,bmesh,json,sys,math
from pathlib import Path
from mathutils import Vector
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from walkgeom import World
w=World();T=Vector(json.loads((R/'DATOS/prototipo_conjunto.json').read_text())['bridge_translation']);manifest=json.loads((R/'DATOS/manifest_blender.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(R/'ESCENAS/VOY03_Circulacion.blend'),load_ui=False,use_scripts=False);source=bpy.data.scenes['01_REFERENCIA_ORIGINAL'];s=bpy.data.scenes.new('TEMP_EVIDENCIA_SUPERFICIES');s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=2000;s.render.resolution_y=1450;s.render.resolution_percentage=100;s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.view_settings.view_transform='Standard';copies=[]
def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=color;return m
cols=[material('DIAG_'+str(i),c) for i,c in enumerate([(.15,.55,.95,1),(.2,.75,.5,1),(.95,.65,.12,1),(.6,.35,.9,1),(.85,.1,.08,1)])]
for o in source.objects:
 if o.name not in manifest['architecture_fingerprints']:continue
 c=o.copy();c.parent=None;c.matrix_world=o.matrix_world;c.data=o.data.copy();s.collection.objects.link(c);copies.append((o,c))
def shot(name,at,aim,scale):
 cd=bpy.data.cameras.new(name);cam=bpy.data.objects.new(name,cd);s.collection.objects.link(cam);cam.location=Vector(at)+T;cam.rotation_euler=(Vector(aim)+T-cam.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=scale;cd.clip_start=.001;cd.clip_end=1000;s.camera=cam;s.render.filepath=str(R/'CAPTURAS'/f'{name}.png');bpy.ops.render.render(write_still=True,scene=s.name);print('SHOT',name,flush=True)
for o,c in copies:
 n=str(o.get('VOY02_ORIGEN','')).removeprefix('OBJ:');c.hide_render=n not in w.support_names
 if not c.hide_render:
  z=sum((c.matrix_world@v.co).z-T.z for v in c.data.vertices)/max(1,len(c.data.vertices));k=0 if z<.1 else 1 if z<.4 else 2 if z<.55 else 3;c.data.materials.clear();c.data.materials.append(cols[k])
  for p in c.data.polygons:p.material_index=0
shot('B12_niveles_suelos_aislados',(10,-11,5),(0,.3,.35),19)
shot('B13_escalones_apoyos_aislados',(6.2,-1.6,2.0),(4.0,.05,.55),4.4)
# Full architectural context again; only render cutaway and obstacle colour differ.
for o,c in copies:
 c.hide_render=not str(o.get('VOY02_ORIGEN','')).startswith('OBJ:');c.data=o.data.copy();bm=bmesh.new();bm.from_mesh(c.data);bm.transform(c.matrix_world);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,2.3+T.z),plane_no=(0,0,1),clear_outer=True);bm.transform(c.matrix_world.inverted());bm.to_mesh(c.data);bm.free()
 if o.get('VOY02_ORIGEN')=='OBJ:Mesh_2096':
  c.data.materials.clear();c.data.materials.append(cols[4])
  for p in c.data.polygons:p.material_index=0
foot=w.state(-2.6933333333333485,-1.5933333333333455)['foot'];center=Vector(foot)+T
def line(name,points):
 cv=bpy.data.curves.new(name,'CURVE');cv.dimensions='3D';cv.bevel_depth=.009;sp=cv.splines.new('POLY');sp.points.add(len(points)-1)
 for p,co in zip(sp.points,points):p.co=(*co,1)
 ob=bpy.data.objects.new(name,cv);s.collection.objects.link(ob);cv.materials.append(cols[4])
for angle in np.linspace(0,math.pi,6,endpoint=False):
 pts=[]
 for th in np.linspace(math.pi,2*math.pi,60):pts.append(center+Vector((.35*math.cos(th)*math.cos(angle),.35*math.cos(th)*math.sin(angle),.35+.35*math.sin(th))))
 for th in np.linspace(0,math.pi,60):pts.append(center+Vector((.35*math.cos(th)*math.cos(angle),.35*math.cos(th)*math.sin(angle),1.55+.35*math.sin(th))))
 pts.append(pts[0]);line('CAPSULA_NEGATIVA',pts)
shot('B14_bloqueo_diagonal_Mesh2096',(-4,-3,4),(-2.65,-1.55,.8),4.7)
# Read-only visual operation: no save.
