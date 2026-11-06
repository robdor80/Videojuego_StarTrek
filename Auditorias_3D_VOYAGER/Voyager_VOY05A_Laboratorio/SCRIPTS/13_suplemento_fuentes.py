import json,runpy,sys,bpy
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.argv=['x','--'];api=runpy.run_path(str(R/'SCRIPTS/01_inspeccionar_blender.py'));api['load']('puente_max');s=bpy.context.scene;api['setup'](s);s.render.resolution_x=1400;s.render.resolution_y=1000
obs=[o for o in s.objects if o.type=='MESH']
for name,direction in [('MAX_CONTEXTO',(0,0,1)),('MAX_HOJA_GRUPOS',(0,-1,.25))]:
 if name=='MAX_CONTEXTO':
  for o in obs:o.hide_render=o.name=='Voyager Bridge' or o.name in ['Mesh992','Mesh993']
  cam=api['camera'](s,(0,2,1),(0,0,1),29,1.4)
 else:
  for o in obs:o.hide_render=not(o.parent and o.parent.name in ['door3','door4'])
  cam=api['camera'](s,(-9.6,2.15,.95),(-.8787,.4773,0),3.8,1.4)
 s.render.filepath=str(R/'CAPTURAS'/f'{name}.png');bpy.ops.render.render(write_still=True);bpy.data.objects.remove(cam,do_unlink=True)
print('MAX capturas diagnosticas',flush=True)
