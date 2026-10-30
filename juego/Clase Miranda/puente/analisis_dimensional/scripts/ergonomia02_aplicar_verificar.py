"""Edición localizada de puertas. Ejecutar únicamente con Ergonomia_01.blend."""
import bpy, json, sys, math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).parent))
from ergonomia02_inspeccion import object_state, material_state, digest, sha
SOURCE=ROOT.parent/'blender/Miranda_Puente_Sutherland_Ergonomia_01.blend'
TARGET=ROOT.parent/'blender/Miranda_Puente_Sutherland_Ergonomia_02.blend'
assert Path(bpy.data.filepath)==SOURCE
assert not TARGET.exists(),'El destino ya existe; se evita sobrescribir trabajo previo.'
before=json.loads((ROOT/'datos/ergonomia02_inspeccion.json').read_text(encoding='utf-8'))
assert sha(SOURCE)==before['protected_sha256'][str(SOURCE)]
assert bpy.context.scene.unit_settings.scale_length==1
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.update()
changed={}
def tree(name):
    o=bpy.data.objects[name]
    return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])
def first(name,p,d,limit=10):
    hit=tree(name).ray_cast(Vector(p),Vector(d),limit)
    return hit[0]
ang=math.radians(10)
portals=[
 {'id':'D1_referencia_turbo','side':-1,'frame':'Plane.004_0','leaves':['Plane.018_0','Plane.019_0'],
  'center':(-5.65857,-8.27379),'tangent':(-math.sin(ang),math.cos(ang),0),'floor':0.,'adjacent':['Plane.011_0','Plane.022_0','Plane.039_0','Plane.026_0'],'room':'Cabina existente; marco interior Plane.039_0 permanece intacto.'},
 {'id':'D2_opuesta_Yneg','side':1,'frame':'Plane.004_0','leaves':['Plane.018_0','Plane.019_0'],
  'center':(5.65857,-8.27379),'tangent':(math.sin(ang),math.cos(ang),0),'floor':0.,'adjacent':['Plane.011_0','Plane.022_0'],'room':'Sin habitación construida detrás.'},
 {'id':'D3_Xpos_Ypos','side':1,'frame':'Plane.013_0','leaves':['Plane.001_0','Plane.017_0'],
  'center':(6.34916,.872141),'tangent':(0,1,0),'floor':.6,'adjacent':['Plane.009_0','Plane.010_0','Plane.014_0','ceiling_0'],'room':'Sin habitación construida detrás.'},
 {'id':'D4_Xneg_Ypos','side':-1,'frame':'Plane.013_0','leaves':['Plane.001_0','Plane.017_0'],
  'center':(-6.34916,.872141),'tangent':(0,1,0),'floor':.6,'adjacent':['Plane.009_0','Plane.010_0','Plane.014_0','ceiling_0'],'room':'Sin habitación construida detrás.'}]
def leaf_stats(p):
    output=[];t=Vector(p['tangent'])
    for name in p['leaves']:
        o=bpy.data.objects[name];vs=[o.matrix_world@v.co for v in o.data.vertices if (o.matrix_world@v.co).x*p['side']>0]
        zz=[v.z for v in vs];ts=[v.dot(t) for v in vs]
        output.append({'object':name,'bottom_world_m':min(zz),'top_world_m':max(zz),'leaf_height_cm':100*(max(zz)-min(zz)),
                       'top_above_floor_cm':100*(max(zz)-p['floor']),'width_cm':100*(max(ts)-min(ts))})
    return output
def measure(p):
    x,y=p['center'];f=p['floor'];t=Vector(p['tangent']);n=Vector((t.y,-t.x,0))
    # Trabajar ligeramente dentro del espesor evita rayos coplanares con la fachada.
    c=Vector((x,y,f+.2));c+=n*.03*p['side']
    zhit=first(p['frame'],c,(0,0,1),6);assert zhit is not None,(p['id'],'sin dintel')
    c.z=f+1.5
    left=first(p['frame'],c,-t,2);right=first(p['frame'],c,t,2)
    assert left is not None and right is not None,(p['id'],'sin jambas')
    verts=[bpy.data.objects[p['frame']].matrix_world@v.co for v in bpy.data.objects[p['frame']].data.vertices]
    verts=[v for v in verts if v.x*p['side']>0]
    return {'floor_world_cm':100*f,'clear_height_center_cm':100*(zhit.z-f),'lintel_world_cm':100*zhit.z,
            'clear_width_cm':100*(right-left).length,'width_endpoints_world_m':[list(left),list(right)],
            'frame_bottom_world_cm':100*min(v.z for v in verts),'frame_crown_world_cm':100*max(v.z for v in verts),
            'leaves':leaf_stats(p)}
measure_before={p['id']:measure(p) for p in portals}
reference=measure_before[portals[0]['id']]
overlap=reference['leaves'][0]['top_world_m']-reference['lintel_world_cm']/100
assert .002<overlap<.02,('Solape de referencia inesperado',overlap)
def set_z(o,i,z):
    v=o.data.vertices[i];world=o.matrix_world@v.co
    old=list(world);world.z=z;v.co=o.matrix_world.inverted()@world
    changed.setdefault(o.name,[]).append({'vertex':i,'before_world_m':old,'after_world_m':list(world)})
for p in portals[1:]:
    floor=p['floor'];frame=bpy.data.objects[p['frame']]
    old_lintel=measure_before[p['id']]['lintel_world_cm']/100
    delta=old_lintel-(floor+3.)
    assert .8<delta<1.,('Reducción inesperada',p['id'],delta)
    # El z nominal de la coronación es ~4.74; todos sus vértices quedan fijos.
    # El contorno superior del hueco baja rígidamente, incluidos biseles y retornos.
    for v in frame.data.vertices:
        w=frame.matrix_world@v.co
        if w.x*p['side']>0 and floor+3.1<w.z<4.65:set_z(frame,v.index,w.z-delta)
    for name in p['leaves']:
        o=bpy.data.objects[name]
        vs=[(v.index,o.matrix_world@v.co) for v in o.data.vertices if (o.matrix_world@v.co).x*p['side']>0]
        zmin=min(w.z for _,w in vs);zmax=max(w.z for _,w in vs)
        assert zmax-zmin>3.8
        assert all(abs(w.z-zmin)<.00002 or abs(w.z-zmax)<.00002 for _,w in vs),'La hoja tiene una estructura no prevista'
        for i,w in vs:
            if abs(w.z-zmax)<.00002:set_z(o,i,floor+3.+overlap)
for name in changed:bpy.data.objects[name].data.update()
bpy.context.view_layer.update()
measure_after={p['id']:measure(p) for p in portals}
assert len(changed)==6 and set(changed)=={'Plane.001_0','Plane.017_0','Plane.018_0','Plane.019_0','Plane.004_0','Plane.013_0'}
def original_subset_unchanged(name,side):
    o=bpy.data.objects[name];old=before['states'][name]
    return all(list(v.co)==old['vertices'][v.index] for v in o.data.vertices if before['objects'][name]['world_vertices'][v.index][0]*side>0)
assert all(original_subset_unchanged(n,-1) for n in ['Plane.004_0','Plane.018_0','Plane.019_0']), 'Referencia modificada'
checks={}
for p in portals:
    a=measure_before[p['id']];b=measure_after[p['id']]
    checks[p['id']]={'width_difference_cm':b['clear_width_cm']-a['clear_width_cm'],
      'frame_base_difference_cm':b['frame_bottom_world_cm']-a['frame_bottom_world_cm'],
      'crown_difference_cm':b['frame_crown_world_cm']-a['frame_crown_world_cm'],
      'leaf_bottom_difference_cm':[bb['bottom_world_m']*100-aa['bottom_world_m']*100 for aa,bb in zip(a['leaves'],b['leaves'])],
      'leaf_width_difference_cm':[bb['width_cm']-aa['width_cm'] for aa,bb in zip(a['leaves'],b['leaves'])]}
    if p is not portals[0]:assert abs(b['clear_height_center_cm']-300)<.01,(p,b)
    assert abs(checks[p['id']]['width_difference_cm'])<.001
    assert max(abs(v) for v in checks[p['id']]['leaf_bottom_difference_cm'])<.001
    assert max(abs(v) for v in checks[p['id']]['leaf_width_difference_cm'])<.001
    assert abs(checks[p['id']]['crown_difference_cm'])<.001
# Muestreo denso de cierre de los revestimientos en una franja dentro del hueco original.
coverage={}
for p in portals:
    f=p['floor'];x,y=p['center'];t=Vector(p['tangent']);n=Vector((t.y,-t.x,0));tr=tree(p['frame'])
    a=measure_before[p['id']];b=measure_after[p['id']];half=b['clear_width_cm']/200
    misses=[];count=0
    for ui in range(41):
        u=(-.95+1.9*ui/40)*half
        for zi in range(71):
            z=f+3.03+(b['frame_crown_world_cm']/100-f-3.04)*zi/70
            pos=Vector((x,y,z))+t*u-n*.7
            hit=tr.ray_cast(pos,n,1.4)[0];count+=1
            if hit is None:misses.append({'u_m':u,'z_world_m':z})
    coverage[p['id']]={'rays':count,'misses':misses,'tested':'95% de la anchura útil, desde dintel central +3 cm hasta coronación -1 cm; rayos normales al revestimiento.'}
    assert not misses,(p['id'],'Huecos de revestimiento',misses[:5])
# La UV y la conectividad de TODAS las mallas se preservan; solo cambian coordenadas indicadas.
unrelated_changed=[]
for name,old in before['states'].items():
    o=bpy.data.objects[name];new=object_state(o)
    if name not in changed:
        if digest(new)!=digest(old):unrelated_changed.append(name)
    else:
        assert new['uv']==old['uv'],name
        for key in old:
            if key!='vertices':assert digest(new[key])==digest(old[key]),(name,key)
        indices={v['vertex'] for v in changed[name]}
        for i,coords in enumerate(new['vertices']):
            if i not in indices:assert coords==old['vertices'][i],(name,i)
assert not unrelated_changed,unrelated_changed
assert {m.name:digest(material_state(m)) for m in bpy.data.materials}==before['material_hashes']
payload={'source':str(SOURCE),'target':str(TARGET),'blender':bpy.app.version_string,'units':'cm; coordenadas globales, 1 BU = 1 m',
         'portals':portals,'before':measure_before,'after':measure_after,'changes':changed,'checks':checks,
         'coverage':coverage,'unrelated_objects_changed':unrelated_changed,'reference_unchanged':True,
         'materials_unchanged':True,'uv_unchanged':True,'reference_leaf_overlap_cm':overlap*100,
         'expected_hashes':{o.name:digest(object_state(o)) for o in bpy.data.objects},
         'protected_sha256':before['protected_sha256']}
assert all(sha(path)==h for path,h in payload['protected_sha256'].items())
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(TARGET),copy=True)
(ROOT/'datos/ergonomia02_resultados.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding='utf-8')
print('GUARDADO',TARGET)
for p in portals:print(p['id'],'ANTES',measure_before[p['id']],'DESPUES',measure_after[p['id']])
print('VERIFICACIONES_EN_MEMORIA_OK; verificación independiente pendiente de reapertura.')
