exec(compile((__import__('pathlib').Path(__file__).parent/'03_sondeo.py').read_text(encoding='utf-8'),str(__file__),'exec'))
import numpy as np, math, csv
results={}
def sample_ray(key,origin,direction,limit=20,exclude=()):
    h=[h for h in ray(origin,direction,limit) if h['object'] not in exclude]
    results[key]={'origin_BU':list(origin),'direction':list(direction),'hits':h}
    print(key,[(a['object'],a['point']) for a in h[:8]])
leaves=('Plane.018_0','Plane.019_0')
n=Vector((math.cos(math.radians(10)),math.sin(math.radians(10)),0))
t=Vector((-n.y,n.x,0))
center=Vector((-5.829,-8.33,0))
for off in [-.16,0,.16]:
    for z in [.1,1.5,2.5,3.7,3.8]:
        c=center+n*off;c.z=z
        for sign in [-1,1]:sample_ray(f'portal_turbo_o{off}_z{z}_s{sign}',c,t*sign,2,leaves)
    for s in [-.7,0,.7]:
        c=center+n*off+t*s;c.z=.01
        sample_ray(f'dintel_turbo_o{off}_s{s}',c,(0,0,1),5,leaves)
for x,y in [(0,-5),(0,-6.5),(0,-3),(1,-3),(2,-5),(3.7,-3.7),(5.3,-3.7),(0,-8.5),(3,-8.5),(0,.6),(5.5,.6),(-8.12772,-8.71576),(-7,-9),(-9,-9)]:
    sample_ray(f'vertical_{x}_{y}',(x,y,.01),(0,0,1),8)
for x,y in [(0,-1.8),(-.5,-1.8),(-.5,-2.27),(.5,-2.27),(4.7,-3.7),(5.6,-3.7),(5.9,-3.7),(-2,-3.8),(2,-3.8)]:
    sample_ray(f'mueble_{x}_{y}',(x,y,2.4),(0,0,-1),3)
for z in [.2,1,1.773,2.5]:
    for sign in [-1,1]:sample_ray(f'turbo_radial45_z{z}_s{sign}',(-8.12772,-8.71576,z),Vector((1,1,0)).normalized()*sign,5)
for y in [-1.8,-3.7,-5.5,-7,-8.33]:
    for z in [.1,.8,1.5,2.5]:
        sample_ray(f'pasillo_d_y{y}_z{z}',(3.6,y,z),(1,0,0),4)
        sample_ray(f'pasillo_i_y{y}_z{z}',(3.6,y,z),(-1,0,0),4)
for y in [-1.8,-3,-5.5,-8.5]:
    sample_ray(f'suelo_y{y}',(3.6,y,.5),(0,0,-1),1)
for x in [6.35,6.49,6.62]:
    for z in [.7,2.1,3.1,4.3]:
        for sign in [-1,1]:sample_ray(f'portal_Ypos_x{x}_z{z}_s{sign}',(x,.872,z),(0,sign,0),2,('Plane.001_0','Plane.017_0'))
    sample_ray(f'dintel_Ypos_x{x}',(x,.872,.61),(0,0,1),5,('Plane.001_0','Plane.017_0'))
# Simetría de la puerta -Y del lado X positivo.
for sign in [-1,1]:sample_ray(f'portal_Xpos_s{sign}',(5.671431,-8.302217,2.5),Vector((n.y,n.x,0))*sign,2,leaves)
# Plano central de las consolas: Y=-3.5 y X=+/-2.7.
for x,y in [(2.7,-3.5),(-2.7,-3.5),(2.7,-3.2),(2.7,-4.3)]:sample_ray(f'consola_{x}_{y}',(x,y,2.3),(0,0,-1),3)
(ROOT/'datos/mediciones_rayos.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
# Extremos de grupos semánticos: conserva las agrupaciones originales.
groups={'consolas_centrales':[f'Editable Mesh_Mat.{i:03}_0' for i in range(3,12)],
        'superficie_central':['Editable Mesh_Mat.008_0'],
        'controles_centrales':['Editable Mesh_Mat.009_0'],
        'superficie_lateral':['Plane.040_0'], 'soporte_lateral':['Plane.008_0'],
        'pantallas_laterales':['Plane.041_0','Plane.042_0'],
        'asiento_capitan':['Sphere.001_0'],'apoyabrazos_capitan':['Cube.002_0'],
        'control_capitan':['Cube_0']}
gb={}
for g,names in groups.items():
    v=np.array([list(bpy.data.objects[name].matrix_world@v.co) for name in names for v in bpy.data.objects[name].data.vertices])
    gb[g]={}
    for side,mask in [('todo',np.ones(len(v),dtype=bool)),('Xneg',v[:,0]<-.001),('Xpos',v[:,0]>.001)]:
        a=v[mask]
        if len(a):gb[g][side]={'min_cm':(a.min(0)*100).tolist(),'max_cm':(a.max(0)*100).tolist(),'dimensions_cm':(np.ptp(a,axis=0)*100).tolist(),'objects':names}
(ROOT/'datos/grupos_medidos.json').write_text(json.dumps(gb,indent=2),encoding='utf-8')
