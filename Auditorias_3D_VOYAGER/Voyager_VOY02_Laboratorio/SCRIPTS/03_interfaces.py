from geom import *
mv,mt,ids,obs=load('modulos');out=[];canonical={}
for k,o in enumerate(obs):
 tr=mv[mt[ids==k]];lo=tr.min(axis=(0,1));hi=tr.max(axis=(0,1));center=(lo+hi)/2
 frcenter=floor(tr,center[0],center[1],start=lo[2]+min((hi[2]-lo[2])*.5,1.0),limit=2)
 center[2]=frcenter['point'][2] if frcenter else lo[2]
 tr=tr-center;lo=tr.min(axis=(0,1));hi=tr.max(axis=(0,1));ports=[]
 for ax,side,code in [(0,-1,'X-'),(0,1,'X+'),(1,-1,'Y-'),(1,1,'Y+')]:
  normal=np.eye(3)[ax]*side;p=(lo+hi)/2;p[ax]=lo[ax] if side<0 else hi[ax];p[2]=1.;inside=p-normal*.08;fr=ray(tr,[*inside[:2],.65],[0,0,-1],2);floorz=fr['point'][2] if fr else None;ceiling=ray(tr,[*inside[:2],1.5],[0,0,1],5)
  blocked=[]
  for z in [.4,1.,1.7,2.2]:
   a=p.copy()-normal*.06;a[2]=z;blocked.append(ray(tr,a,normal,.12) is not None)
  widths=[];tangent=np.array([-normal[1],normal[0],0])
  for z in [.4,1.,1.7,2.2]:
   a=inside.copy();a[2]=z;l=ray(tr,a,-tangent,10);r=ray(tr,a,tangent,10);widths.append(l['distance']+r['distance'] if l and r else None)
  profiles=section_segments(tr,ax,p[ax]-side*.002)
  candidate=not any(blocked[:3]) and floorz is not None and abs(floorz)<.05 and all(w is not None and w>=.65 for w in widths[:3])
  ports.append({'code':code,'point':[float(p[0]),float(p[1]),float(floorz or 0)],'normal':normal.tolist(),'floor_z':floorz,'ceiling_z':ceiling['point'][2] if ceiling else None,'centerline_blocked_z040_100_170_220':blocked,'width_z040_100_170_220':widths,'open_candidate':bool(candidate),'section_segments':profiles})
 result={**o,'normalize_translation':(-center).tolist(),'bounds_min':lo.tolist(),'bounds_max':hi.tolist(),'ports':ports};out.append(result)
 canonical[o['name']]=tr
(R/'DATOS/interfaces_modulos.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print('SELFTEST',self_test())
for o in out:
 if o['name'] in ['Mesh12','Mesh13','Mesh18','Mesh14','Mesh25','Mesh28','Mesh57','Mesh38','Mesh40','Mesh41','Mesh37','Mesh42','Mesh17','Mesh5','Mesh6','Mesh9','Mesh81']:
  print(o['name'],o['parent'],'PORTS',[(p['code'],p['open_candidate'],[round(x,4) if x else x for x in p['width_z040_100_170_220']],p['centerline_blocked_z040_100_170_220'],round(p['floor_z'],4) if p['floor_z'] else p['floor_z']) for p in o['ports']])
