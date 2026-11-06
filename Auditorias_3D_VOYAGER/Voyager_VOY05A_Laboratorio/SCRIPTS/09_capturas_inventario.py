import bpy,sys,runpy,json,math
import numpy as np
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.argv=['x','--'];api=runpy.run_path(str(R/'SCRIPTS/01_inspeccionar_blender.py'));rows=json.loads((R/'DATOS/inventario_puertas_accesos.json').read_text());manifest=[]
for source in ['coleccion','puente_obj']:
 api['load'](source);scene=bpy.context.scene;api['setup'](scene);scene.render.resolution_x=1200;scene.render.resolution_y=1000
 allmesh=[o for o in scene.objects if o.type=='MESH'];geometry={o.name:np.array([o.matrix_world@v.co for v in o.data.vertices]) for o in allmesh}
 overlay=bpy.data.collections.new('VOY05A_ANOTACIONES_NO_ARQUITECTURA');scene.collection.children.link(overlay)
 for row in [x for x in rows if x['source']==source]:
  center=np.array(row['center_world'],float);normal=np.array(row['normal_world'],float);normal/=np.linalg.norm(normal);is_horiz=abs(normal[2])>.5
  if source=='puente_obj':
   # Normal points outside for the three doors. Inspect from bridge side.
   direction=-normal
   for o in allmesh:
    p=geometry[o.name];delta=np.linalg.norm(p[:,:2]-center[:2],axis=1).min();o.hide_render=bool(delta>3 or p[:,2].min()>center[2]+2.8)
  else:
   direction=normal.copy()
   o=bpy.data.objects[row['objects'][0]];p=geometry[o.name];mid=(p.min(0)+p.max(0))/2
   if (center-mid)@normal<0:direction=-normal
   for ob in allmesh:ob.hide_render=ob!=o
  width=row['width'];height=row['height']
  if row.get('front_surface_envelope'):width=row['front_surface_envelope']['width'];height=row['front_surface_envelope']['height']
  width=width or 1.2;height=height or 2.4;span=max(width*1.3,height*1.3,1.3)
  if source=='puente_obj' and row['id']!='BR_04':center[2]+=height/2
  segments=row.get('profile_segments',[]);annotations=[]
  # Only highlight measured original boundary segments. No invented outline on closed doors.
  for k,seg in enumerate(segments):
   cu=bpy.data.curves.new(row['id']+'_edge','CURVE');cu.dimensions='3D';cu.bevel_depth=max(.002,span*.0013);cu.bevel_resolution=0;sp=cu.splines.new('POLY');sp.points.add(1)
   for point,v in zip(sp.points,seg):point.co=(*list(np.array(v)+direction*.006),1)
   ob=bpy.data.objects.new(row['id']+'_edge',cu);overlay.objects.link(ob);ob.color=(1,.65,.02,1);annotations.append(ob)
  scene.display.shading.color_type='OBJECT'
  # Preserve material diagnostic colors for model; boundary overlays yellow.
  for ob in allmesh:
   if ob.data.materials and ob.data.materials[0]:ob.color=ob.data.materials[0].diffuse_color
   else:ob.color=(.65,.7,.75,1)
  cam=api['camera'](scene,center,direction,span,1.2)
  if source=='puente_obj':
   distance=max(.8,span*.6);cam.location=Vector(center)+Vector(direction)*distance;cam.data.clip_start=max(.01,distance-.35)
  scene.render.filepath=str(R/row['capture']);bpy.ops.render.render(write_still=True);bpy.data.objects.remove(cam,do_unlink=True)
  manifest.append(dict(id=row['id'],image=row['capture'],source=source,center=center.tolist(),direction=direction.tolist(),orthographic_span=span,visible_meshes=[ob.name for ob in allmesh if not ob.hide_render],overlay='yellow actual source boundary segments' if segments else 'none'))
  for ob in annotations:bpy.data.objects.remove(ob,do_unlink=True)
 # The distributed scene keeps complete architecture, all leaves closed, no animation added.
 for ob in allmesh:ob.hide_render=False
 scene.display.shading.color_type='MATERIAL'
 for im in bpy.data.images:
  if im.source=='FILE' and not im.packed_file:
   try:im.pack()
   except Exception:pass
 # Embed data table as a Blender text block for identification.
 tx=bpy.data.texts.new('VOY05A_INVENTARIO.json');tx.write(json.dumps([x for x in rows if x['source']==source],indent=2,ensure_ascii=False))
 cam=api['camera'](scene,(0,0,0) if source=='puente_obj' else (35,15,0),(0,-1,.8),22 if source=='puente_obj' else 120,1.2)
 bpy.ops.wm.save_as_mainfile(filepath=str(R/'ESCENAS'/f'VOY05A_{source}_Revision.blend'),compress=True)
 (R/'DATOS'/f'{source}_imagenes_empaquetadas.json').write_text(json.dumps([dict(name=x.name,path=x.filepath,packed=bool(x.packed_file)) for x in bpy.data.images],indent=2),encoding='utf8')
(R/'DATOS/capturas_inventario_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8');print('CAPTURAS',len(manifest),flush=True)
