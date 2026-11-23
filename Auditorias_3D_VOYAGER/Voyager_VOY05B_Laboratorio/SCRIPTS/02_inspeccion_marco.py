import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from comun import *
bpy.ops.wm.open_mainfile(filepath=str(R/'FUENTES/VOY05A_Puente_Original_Inspeccion.blend'),load_ui=False,use_scripts=False)
s=bpy.context.scene;setup(s)
for o in s.objects:
 if o.type=='MESH':o.hide_render=o.name not in ['Mesh_1832','Mesh_1833','Doorpanel_6']
for name,color in [('Mesh_1832',(.2,.65,.9,1)),('Mesh_1833',(.75,.55,.3,1)),('Doorpanel_6',(.4,1,.5,1))]:bpy.data.objects[name].color=color
c=[1.191131,6.382051,1.75]
render(s,'EXPL_MARCO_FRENTE.png',c,(0,-1,.05),2.8)
render(s,'EXPL_MARCO_OBLICUA.png',c,(1,-2,1),2.8)
render(s,'EXPL_MARCO_DESTINO.png',c,(0,1,.05),2.8)
data=[]
for name in ['Mesh_1832','Mesh_1833']:
 o=bpy.data.objects[name];v=world(o);v=(v-np.array([1.191131,6.382051,.71229556]))@np.array([[0,1,0],[-1,0,0],[0,0,1]]).T
 data.append(dict(object=name,custom_normals=o.data.has_custom_normals,faces=[dict(face=p.index,center=v[list(p.vertices)].mean(0).tolist(),lo=v[list(p.vertices)].min(0).tolist(),hi=v[list(p.vertices)].max(0).tolist(),vertices=list(p.vertices)) for p in o.data.polygons]))
dump('DATOS/marco_caras_exploracion.json',data)
