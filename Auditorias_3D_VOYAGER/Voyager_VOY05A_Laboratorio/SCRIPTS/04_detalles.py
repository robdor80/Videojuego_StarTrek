import sys,runpy,json,bpy,math,bmesh
import numpy as np
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.argv=['x','--'];api=runpy.run_path(str(R/'SCRIPTS/01_inspeccionar_blender.py'));load=api['load'];camera=api['camera'];setup=api['setup']
load('coleccion');s=bpy.context.scene;setup(s);s.render.resolution_x=1200;s.render.resolution_y=1000
obs=[o for o in s.objects if o.type=='MESH']
for o in obs:o.hide_render=True
for name in ['Mesh1','Mesh3','Mesh4','Mesh5','Mesh6','Mesh7','Mesh8','Mesh9','Mesh10','Mesh11','Mesh14','Mesh16','Mesh17','Mesh19','Mesh25','Mesh26','Mesh27','Mesh28','Mesh29','Mesh35','Mesh38','Mesh40','Mesh41','Mesh50','Mesh51','Mesh52','Mesh53','Mesh54','Mesh55','Mesh57','Mesh59','Mesh62','Mesh64','Mesh65','Mesh67','Mesh68','Mesh69','Mesh70','Mesh71','Mesh72','Mesh73','Mesh74','Mesh75','Mesh76','Mesh77','Mesh78','Mesh79','Mesh80','Mesh81','Mesh82','Mesh83','Mesh84','Mesh91','Mesh92','Mesh93','Mesh94','Mesh95','Mesh96','Mesh97','Mesh103']:
 if (R/'CAPTURAS'/f'DET_{name}_YP.png').exists():continue
 o=bpy.data.objects[name];o.hide_render=False;v=np.array([o.matrix_world@x.co for x in o.data.vertices]);lo=v.min(0);hi=v.max(0);c=(lo+hi)/2;span=float(max(hi-lo)*1.23)
 for suffix,dr in [('XM',(-1,0,0)),('XP',(1,0,0)),('YM',(0,-1,0)),('YP',(0,1,0))]:
  cam=camera(s,c,dr,span,1.2);s.render.filepath=str(R/'CAPTURAS'/f'DET_{name}_{suffix}.png');bpy.ops.render.render(write_still=True);bpy.data.objects.remove(cam,do_unlink=True)
 o.hide_render=True
load('puente_obj');s=bpy.context.scene;setup(s);s.render.resolution_x=1400;s.render.resolution_y=1000
doors=json.loads((R/'REFERENCIAS/puertas_medidas.json').read_text());manifest=[]
for d in doors:
 c=np.array(d['center'])+[0,0,.95];normal=np.array(d['normal']);names=d['leafA']+d['leafB']
 # Context local clipping by visibility; complete original geometry remains in saved scene.
 for o in s.objects:
  if o.type=='MESH':
   vv=np.array([o.matrix_world@x.co for x in o.data.vertices]);dist=np.linalg.norm(vv[:,:2]-c[:2],axis=1).min();o.hide_render=bool(dist>2.8 or vv[:,2].min()>2.35)
 cam=camera(s,c,-normal,2.7,1.4);s.render.filepath=str(R/'CAPTURAS'/f'BR_{d["id"]}_CONTEXTO.png');bpy.ops.render.render(write_still=True);bpy.data.objects.remove(cam,do_unlink=True)
 for o in s.objects:
  if o.type=='MESH':o.hide_render=o.name not in names
 cam=camera(s,c,-normal,2.5,1.4);s.render.filepath=str(R/'CAPTURAS'/f'BR_{d["id"]}_HOJAS.png');bpy.ops.render.render(write_still=True);bpy.data.objects.remove(cam,do_unlink=True)
 manifest.append(dict(id=d['id'],center=c.tolist(),normal=normal.tolist(),objects=names))
# Overview, disposable roof cut, no door displaced.
for o in s.objects:
 if o.type=='MESH':o.hide_render=min((o.matrix_world@x.co).z for x in o.data.vertices)>2.35
cam=camera(s,(0,0,.7),(0,0,1),20,1.4);s.render.filepath=str(R/'CAPTURAS/BR_GENERAL.png');bpy.ops.render.render(write_still=True)
(R/'DATOS/capturas_puente_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print('DETALLES FINALIZADOS',flush=True)
