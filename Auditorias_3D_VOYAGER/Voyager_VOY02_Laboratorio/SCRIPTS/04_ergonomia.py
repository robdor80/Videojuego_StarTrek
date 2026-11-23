from geom import *
v,t,ids,obs=load('obj');tr=v[t];names=np.array([o['name'] for o in obs]);floorkeys=[i for i,o in enumerate(obs) if 'Voygray'in o['materials']];ground=tr[np.isin(ids,floorkeys)];co=Collision(tr,ids=names[ids])
stations=[('mando_izq',[-.62,.87]),('mando_der',[.63,.87]),('navegacion',[0,-2.67]),('estacion_derecha',[4.75,-2.7]),('estacion_izquierda',[-4.18,-2.53]),('centro',[0,0]),('paso_frontal',[0,-4.5]),('paso_posterior',[0,4]),('lado_der',[5.8,.2]),('lado_izq',[-5.8,.2])]
measure=[]
for name,xy in stations:
 f=floor(ground,*xy,start=.8)
 if not f:continue
 z=f['point'][2];up=ray(tr,[*xy,z+.01],[0,0,1],6);measure.append({'zone':name,'xy':xy,'floor_z':z,'floor_object':names[ids[np.where(np.isin(ids,floorkeys))[0][f['triangle']]]],'first_surface_above':up,'standing_capsules':[{'height':h,'result':co.pose([*xy,z],height=h,radius=.35)} for h in [1.6,1.75,1.9]]})
# Doors: use full surrounding geometry, not the size of one leaf. Temporarily remove only known leaf panels, recording all exclusions.
doors=[('D_LATERAL_IZQ',[-6.3035,.184],[ -.8660254,.5,0],['door_2','Mesh_1757']),('D_LATERAL_DER',[6.316,.184],[.8660254,.5,0],['Mesh_1995','Mesh_2003']),('D_POSTERIOR',[1.191,6.382],[0,1,0],['Mesh_1979','Mesh_1987']),('D_TURBO',[-3.95,3.6],[-.58,.81,0],[])]
doorout=[]
for code,xy,n,leaves in doors:
 n=np.array(n,float);n/=np.linalg.norm(n);tan=np.array([-n[1],n[0],0]);sel=~np.isin(names[ids],leaves);context=tr[sel];cids=names[ids][sel];p=np.array([*xy,0.]);inside=p-n*.35;f=floor(ground,*inside[:2],start=.8);z=f['point'][2] if f else None
 if z is None:doorout.append({'id':code,'error':'no floor at guessed center','guessed_xy':xy});continue
 p[2]=z;profiles=[]
 for dz in [.1,.5,1.,1.5,1.7,1.9,2.1]:
  # All hits along the tangent from the measured plane-center. Includes trim and installed side pieces.
  q=p+[0,0,dz];l=ray(context,q,-tan,3);r=ray(context,q,tan,3);profiles.append({'height_above_floor':dz,'width':l['distance']+r['distance'] if l and r else None,'left':l,'right':r})
 # Sweep fixed-width vertical slab at doorway plane: first body-overlap even if centerline ray misses lintel.
 cc=Collision(context,ids=cids);scale_tests=[]
 for scale in [1.,1.1,1.15,1.2,1.25,1.3,1.508135]:
  tests=[]
  for h in [1.6,1.75,1.9]:
   # Equivalent inverse-scaled human in unscaled scene.
   points=[(p-n*.55).tolist(),(p+n*.55).tolist()];res=cc.path(points,height=h/scale,radius=.35/scale,spacing=.04,margin=.01/scale);tests.append({'human_height_m':h,'clear':res['clear'],'minimum_clearance_scaled_m':res['minimum_clearance']*scale if res['minimum_clearance'] is not None else None,'blocking_objects':sorted(set(x for f in res['failures'] for x in f['blocking_objects'])),'samples':res['samples']})
  scale_tests.append({'scale':scale,'results':tests})
 doorout.append({'id':code,'center':p.tolist(),'outward_normal':n.tolist(),'tangent':tan.tolist(),'floor_source':f,'excluded_leaves_only':leaves,'width_profiles':profiles,'scale_tests':scale_tests})
out={'floor_and_capsules':measure,'door_probes':doorout,'capsule_hypothesis':{'radius_m':.35,'heights_m':[1.6,1.75,1.9],'final_character_config':'not established; Sutherland test scripts use r35/h90 cm but final Voyager character not established'},'analytic_tests':self_test()}
(R/'DATOS/ergonomia_inicial.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print('ZONES',[(m['zone'],round(m['floor_z'],4),m['floor_object'],m['first_surface_above']['distance'] if m['first_surface_above'] else None) for m in measure])
for d in doorout:
 print('DOOR',d['id'],'CENTER',d.get('center'),'WIDTHS',[(p['height_above_floor'],round(p['width'],4) if p['width'] else None) for p in d.get('width_profiles',[])],'TESTS',[(p['scale'],[(x['human_height_m'],x['clear'],x['blocking_objects'][:4]) for x in p['results']]) for p in d.get('scale_tests',[])])
