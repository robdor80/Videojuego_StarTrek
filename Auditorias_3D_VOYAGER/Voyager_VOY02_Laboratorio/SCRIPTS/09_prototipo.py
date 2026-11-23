from geom import *
from math import atan2
v,t,ids,obs=load('obj');bridge=v[t];names=np.array([o['name'] for o in obs]);ds=json.loads((R/'DATOS/puertas_medidas.json').read_text());scale=1.1;door=next(d for d in ds if d['id']=='D_POST');origin=np.array(door['center']);Btranslation=-origin*scale
for d in ds:
 bridge[np.isin(names[ids],d['leafA'])]+=d['leafA_vector'];bridge[np.isin(names[ids],d['leafB'])]+=d['leafB_vector']
bridge=bridge*scale+Btranslation
vv,tt,ii,oo=load('modulos');interface=json.loads((R/'DATOS/interfaces_modulos.json').read_text());by={o['name']:o for o in interface};source={o['name']:vv[tt[ii==k]]+by[o['name']]['normalize_translation'] for k,o in enumerate(oo)}
def rot(yaw):return np.array([[math.cos(yaw),-math.sin(yaw),0],[math.sin(yaw),math.cos(yaw),0],[0,0,1]])
def place(id,src,entry,at,normal):
 port=next(p for p in by[src]['ports'] if p['code']==entry);wanted=-np.array(normal,float);yaw=atan2(wanted[1],wanted[0])-atan2(port['normal'][1],port['normal'][0]);translation=np.array(at)-rot(yaw)@port['point'];return {'id':id,'source':src,'yaw':yaw,'translation':translation.tolist(),'original_to_canonical':by[src]['normalize_translation']}
def port(pl,code):
 p=next(p for p in by[pl['source']]['ports'] if p['code']==code);return rot(pl['yaw'])@p['point']+pl['translation'],rot(pl['yaw'])@p['normal']
def box(center,size):
 c=np.array(center);s=np.array(size)/2;vs=np.array([c+s*np.array([x,y,z]) for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]);faces=np.array([[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]]);return vs[faces]
def solid_quad(a,b,c,d,thickness_vector):
 vs=np.array([a,b,c,d,a+thickness_vector,b+thickness_vector,c+thickness_vector,d+thickness_vector]);f=np.array([[0,1,2],[0,2,3],[4,6,5],[4,7,6],[0,4,5],[0,5,1],[1,5,6],[1,6,2],[2,6,7],[2,7,3],[3,7,4],[3,4,0]]);return vs[f]
adapters=[]
def adapter(id,start,normal,length,widthA,widthB,heightA,heightB):
 start=np.array(start,float);n=np.array(normal,float);end=start+n*length;tan=np.array([-n[1],n[0],0]);z=np.array([0,0,1.]);a=start-tan*widthA/2;b=start+tan*widthA/2;c=end+tan*widthB/2;d=end-tan*widthB/2
 floortr=solid_quad(a,b,c,d,-z*.06);left=solid_quad(a,d,d+z*heightB,a+z*heightA,-tan*.08);right=solid_quad(b,b+z*heightA,c+z*heightB,c,tan*.08);roof=solid_quad(a+z*heightA,d+z*heightB,c+z*heightB,b+z*heightA,z*.06);tri=np.vstack([floortr,left,right,roof]);adapters.append({'id':id,'start':start.tolist(),'end':end.tolist(),'normal':n.tolist(),'length':length,'widthA':widthA,'widthB':widthB,'heightA':heightA,'heightB':heightB,'triangles':tri.tolist(),'kind':'GEOMETRIA_NUEVA_SOLO_LABORATORIO','grade':'C','note':'Transition of measured minimum free sections; source moldings and full outer-profile continuity are not restored.'});return end
placements=[]
end=adapter('AD_PUENTE',[0,0,0],[0,1,0],1.4,.82,3.1808,1.95,2.81635)
long=place('PASILLO_PRINCIPAL','Mesh13','Y-',end,[0,1,0]);placements.append(long);p,n=port(long,'Y+')
end=adapter('AD_CRUCE',p,n,.6,3.1808,2.9613,2.81635,2.81635);hub=place('CRUCE_CUATRO','Mesh38','Y-',end,n);placements.append(hub)
p,n=port(hub,'X+');end=adapter('AD_RAMAL_TURBO',p,n,.6,2.9613,3.1808,2.81635,2.81635);access=place('ACCESO_TURBO','Mesh37','Y-',end,n);placements.append(access)
p,n=port(access,'Y+');end=adapter('AD_GARGANTA_TURBO',p,n,.65,1.5715,1.1493,2.10,2.10);turbo=place('CABINA_TURBO','Mesh17','Y-',end,n);placements.append(turbo)
p,n=port(hub,'Y+');end=adapter('AD_RAMAL_CAMAROTE',p,n,.6,2.9613,3.1808,2.81635,2.81635);res=place('PASILLO_CAMAROTE','Mesh18','Y-',end,n);placements.append(res)
p,n=port(res,'Y+');end=adapter('AD_CAMAROTE',p,n,1.4,3.1808,1.07979,2.81635,2.10);room=place('CAMAROTE_EXISTENTE','Mesh4','X-',end,n);placements.append(room)
rc=np.array(room['translation']);props=[{'id':'REF_CAMA','center':(rc+[1.65,1.5,.30]).tolist(),'size':[1.10,2.10,.60]},{'id':'REF_ESCRITORIO','center':(rc+[-2.45,.8,.375]).tolist(),'size':[.65,1.40,.75]},{'id':'REF_ARMARIO','center':(rc+[-2.45,2.6,1.0]).tolist(),'size':[.65,1.5,2.0]}]
geometry=[bridge];gids=[np.array(['PUENTE:'+x for x in names[ids]])]
for p in placements:tr=transform(source[p['source']],p['yaw'],p['translation']);geometry.append(tr);gids.append(np.full(len(tr),p['id']))
for a in adapters:tr=np.array(a['triangles']);geometry.append(tr);gids.append(np.full(len(tr),a['id']))
for p in props:tr=box(p['center'],p['size']);geometry.append(tr);gids.append(np.full(len(tr),p['id']))
full=np.vstack(geometry);fullids=np.concatenate(gids);cc=Collision(full,fullids)
bridgeRoute=json.loads((R/'DATOS/transitos_puente.json').read_text())['routes'][0]['points'];bridgeRoute=(np.array(bridgeRoute)*scale+Btranslation).tolist();bridgeRoute.append([0,0,.002]);hubc=np.array(hub['translation']);mainroute=bridgeRoute+[[0,1.4,.002],[0,float(hubc[1]),.002]]
turboroute=mainroute+[list(np.array(access['translation'])+[0,0,.002]),list(np.array(turbo['translation'])+[0,0,.002])]
roomroute=mainroute+[list(np.array(res['translation'])+[0,0,.002]),list(rc+[0,-2.9,.002]),list(rc+[0,0,.002]),list(rc+[.70,1.5,.002])]
tests=[]
for name,route in [('PUENTE_AL_TURBOLIFT',turboroute),('PUENTE_AL_CAMAROTE',roomroute)]:
 results=[cc.path(route,height=h,radius=.35,spacing=.025,margin=.0125) for h in [1.6,1.75,1.9]];support=support_path(full,route);tests.append({'id':name,'routes':results,'support':support})
# Alternative room shells: same capsule inside unmodified source, for 1:1 catalog scale.
rooms=[]
for src in ['Mesh1','Mesh4','Mesh5','Mesh6','Mesh81','Mesh9']:
 tr=source[src];ctr=by[src];c=Collision(tr);p=[0,0,.002];pose=c.pose(p,height=1.9,radius=.35);ff=floor(tr,0,0,start=.8);rooms.append({'source':src,'center_pose':pose,'center_floor':ff,'candidate_ports':[p['code'] for p in ctr['ports'] if p['open_candidate']]})
out={'scale_bridge':scale,'bridge_translation':Btranslation.tolist(),'bridge_door_openings':ds,'placements':placements,'adapters':adapters,'furniture_reference_only':props,'routes':tests,'room_shell_tests':rooms,'whole_bridge_access_note':'Upper walkway to rear exit verified; central and navigation routes not demonstrated across all level transitions. Do not infer a fully walkable bridge.'}
(R/'DATOS/prototipo_conjunto.json').write_text(json.dumps(out,indent=2),encoding='utf8');np.savez_compressed(R/'DATOS/prototipo_geometria.npz',triangles=full,labels=fullids)
for test in tests:print(test['id'],[(q['height'],q['clear'],q['samples'],q['failures'][:1]) for q in test['routes']],'FLOOR',test['support']['clear'],test['support']['failures'][:2])
print('ROOMS',[(r['source'],r['center_pose']['clear'],r['candidate_ports']) for r in rooms])
