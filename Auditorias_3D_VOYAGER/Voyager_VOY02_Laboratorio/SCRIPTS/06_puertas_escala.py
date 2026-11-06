from geom import *
v,t,ids,obs=load('obj');tri=v[t];names=np.array([o['name'] for o in obs]);by={o['name']:o for o in obs};mapping=json.loads((R/'DATOS/correspondencias_max_obj.json').read_text());groups=mapping['functional_groups'];ground=tri[np.isin(ids,[i for i,o in enumerate(obs) if 'Voygray'in o['materials']])]
doors=[]
for code,ga,gb,pa,pb,sign in [('D_IZQ','door3','door4','door_2','Mesh_1757',-1),('D_DER','door05','door04','Mesh_1995','Mesh_2003',1),('D_POST','door06','door07','Mesh_1987','Mesh_1979',1)]:
 a=(np.array(by[pa]['bounds_min'])+by[pa]['bounds_max'])/2;b=(np.array(by[pb]['bounds_min'])+by[pb]['bounds_max'])/2;tan=b-a;tan[2]=0;tan/=np.linalg.norm(tan);normal=np.array([tan[1],-tan[0],0])
 if code=='D_IZQ' and normal[0]>0:normal=-normal
 if code=='D_DER' and normal[0]<0:normal=-normal
 if code=='D_POST' and normal[1]<0:normal=-normal
 center=(a+b)/2;inside=center-normal*.3;fr=floor(ground,*inside[:2],start=.8);center[2]=fr['point'][2];leafA=[r['obj'] for r in groups[ga] if r['candidate']];leafB=[r['obj'] for r in groups[gb] if r['candidate']];moved=tri.copy();maskA=np.isin(names[ids],leafA);maskB=np.isin(names[ids],leafB)
 # Measured leaf length and clearance stroke. Physically move full assemblies, do not hide trim.
 allA=moved[maskA].reshape((-1,3));allB=moved[maskB].reshape((-1,3));wa=np.ptp(allA@tan);wb=np.ptp(allB@tan);stroke=float(max(wa,wb)+.04);moved[maskA]-=tan*stroke;moved[maskB]+=tan*stroke
 cc=Collision(moved,ids=names[ids]);heights=[]
 for side in [-.02,0,.02]:
  p=center+normal*side+[0,0,.02];hit=ray(moved,p,[0,0,1],5);heights.append(hit['point'][2]-center[2] if hit else None)
 widths=[]
 for dz in [.1,.5,1.,1.5,1.7,1.9]:
  p=center+[0,0,dz];l=ray(moved,p,-tan,2);r=ray(moved,p,tan,2);widths.append({'above_floor':dz,'width':l['distance']+r['distance'] if l and r else None})
 scales=[]
 for scale in [1.,1.1,1.15,1.2,1.25,1.3,1.50813535]:
  rs=[]
  for h in [1.6,1.75,1.9]:
   path=cc.path([(center-normal*.3).tolist(),(center+normal*.3).tolist()],height=h/scale,radius=.35/scale,spacing=.025,margin=.0125/scale);rs.append({'human_height':h,**path})
  scales.append({'scale':scale,'tests':rs})
 doors.append({'id':code,'center':center.tolist(),'normal':normal.tolist(),'tangent':tan.tolist(),'floor':fr,'leafA':leafA,'leafB':leafB,'leafA_vector':(-tan*stroke).tolist(),'leafB_vector':(tan*stroke).tolist(),'stroke_obj_units':stroke,'ceiling_clearances':heights,'widths':widths,'scale_tests':scales,'note':'Full leaves moved in numerical copy. Feasibility of pockets separately tested; passing through opening does not certify door mechanism.'})
(R/'DATOS/puertas_medidas.json').write_text(json.dumps(doors,indent=2),encoding='utf8')
for d in doors:print(d['id'],'CENTER',d['center'],'NORMAL',d['normal'],'STROKE',d['stroke_obj_units'],'CLEAR_H',d['ceiling_clearances'],'WIDTH',d['widths'],'PASS',[(s['scale'],[(t['human_height'],t['clear'],sorted(set(x for f in t['failures'] for x in f['blocking_objects']))[:4]) for t in s['tests']]) for s in d['scale_tests']])
