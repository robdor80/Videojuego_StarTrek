import bpy,bmesh,json,sys,math,collections,csv
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];outputs=[]
for label,filename in [('blend','collection.blend'),('recovery','recovery.blend'),('obj_work','obj_work.blend'),('obj_split','OBJ_ORIGINAL')]:
 if filename=='OBJ_ORIGINAL':
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.wm.obj_import(filepath=r'C:\Users\andro\Desktop\Nueva carpeta\TrekmeshesEU_Chainsaw_USSVoyagerBridge_OBJ\Voyager Bridge.obj',use_split_objects=True,use_split_groups=True,validate_meshes=True,forward_axis='NEGATIVE_Z',up_axis='Y')
 else:bpy.ops.wm.open_mainfile(filepath=str(R/'TEMP'/filename),load_ui=False,use_scripts=False)
 obs=[o for o in bpy.context.scene.objects if o.type=='MESH'];rows=[];globaltri=collections.defaultdict(list)
 for ob in obs:
  me=ob.data;me.calc_loop_triangles();w=ob.matrix_world;v=[w@x.co for x in me.vertices];used=set(i for p in me.polygons for i in p.vertices);pcoords=[v[i] for i in used];lo=[min((p[i] for p in pcoords),default=0) for i in range(3)];hi=[max((p[i] for p in pcoords),default=0) for i in range(3)];area=up=down=vertical=0;zero=0
  materials=collections.Counter();alltris=[]
  for t in me.loop_triangles:
   a,b,c=[v[i] for i in t.vertices];cross=(b-a).cross(c-a);ar=cross.length/2;area+=ar
   if ar<1e-10:zero+=1
   elif cross.normalized().z>0.95:up+=ar
   elif cross.normalized().z<-.95:down+=ar
   else:vertical+=ar
   materials[me.materials[t.material_index].name if t.material_index<len(me.materials) and me.materials[t.material_index] else 'NONE']+=1
   key=tuple(sorted(tuple(round(x,5) for x in p) for p in [a,b,c]));globaltri[key].append(ob.name)
  rows.append({'object':ob.name,'parent':ob.parent.name if ob.parent else None,'vertices':len(v),'used_vertices':len(used),'loose_vertices':len(v)-len(used),'faces':len(me.polygons),'triangles':len(me.loop_triangles),'zero_area_world':zero,'surface_area':area,'up_area':up,'down_area':down,'side_or_sloped_area':vertical,'surface_bounds_min':lo,'surface_bounds_max':hi,'surface_dimensions':[hi[i]-lo[i] for i in range(3)],'material_triangles':dict(materials)})
 duplicates=[{'count':len(names),'objects':dict(collections.Counter(names)),'triangle':key} for key,names in globaltri.items() if len(names)>1]
 output={'label':label,'objects':rows,'duplicate_world_triangles_at_1e5':duplicates,'note':'Triangles quantized 1e-5 m. Coincident surfaces can be intentional. No exhaustive intersections test.'}
 if label=='blend':
  def bvh(obs):
   vv=[];ff=[]
   for ob in obs:
    base=len(vv);vv.extend(ob.matrix_world@v.co for v in ob.data.vertices);ff.extend(tuple(base+i for i in t.vertices) for t in ob.data.loop_triangles)
   return BVHTree.FromPolygons(vv,ff,all_triangles=True)
  def cast(tree,p,d,limit=30):
   h,n,i,dist=tree.ray_cast(Vector(p),Vector(d),limit)
   return {'hit':list(h) if h else None,'normal':list(n) if n else None,'distance':dist}
  tests=[]
  for name in ['Mesh12','Mesh13','Mesh18','Mesh15','Mesh63','Mesh58','Mesh17']:
   ob=bpy.data.objects[name];row=next(x for x in rows if x['object']==name);lo=row['surface_bounds_min'];hi=row['surface_bounds_max'];tree=bvh([ob]);cx=(lo[0]+hi[0])/2
   for f in [.1,.5,.9]:
    cy=lo[1]+(hi[1]-lo[1])*f
    for z in [.1,.9,1.7,2.2]:
     a=cast(tree,[cx,cy,z],[-1,0,0]);b=cast(tree,[cx,cy,z],[1,0,0]);tests.append({'object':name,'y_fraction':f,'z':z,'left':a,'right':b,'width':a['distance']+b['distance'] if a['distance'] is not None and b['distance'] is not None else None})
   tests.append({'object':name,'vertical_center':{'floor':cast(tree,[cx,(lo[1]+hi[1])/2,1.7],[0,0,-1]),'ceiling':cast(tree,[cx,(lo[1]+hi[1])/2,1.7],[0,0,1])}})
  output['corridor_rays']=tests
  # Referenced coordinate connectivity: source bridge parts remain intact.
  bridgeparts=[]
  for name in ['Mesh98','Mesh99','Mesh100','Mesh101','Mesh102','Mesh103','Mesh104','Mesh105']:
   ob=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.transform(bm,matrix=ob.matrix_world,verts=list(bm.verts));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5);remaining=set(bm.verts);components=[]
   while remaining:
    seed=remaining.pop();stack=[seed];group=[seed]
    while stack:
     a=stack.pop()
     for e in a.link_edges:
      b=e.other_vert(a)
      if b in remaining:remaining.remove(b);stack.append(b);group.append(b)
    faces=set(f for v in group for f in v.link_faces)
    if faces:
     mn=[min(v.co[i] for v in group) for i in range(3)];mx=[max(v.co[i] for v in group) for i in range(3)];components.append({'vertices':len(group),'faces':len(faces),'min':mn,'max':mx,'size':[mx[i]-mn[i] for i in range(3)]})
   bridgeparts.append({'object':name,'components_after_weld':len(components),'components':sorted(components,key=lambda c:c['faces'],reverse=True)});bm.free()
  output['bridge_connected_parts']=bridgeparts
 if label=='recovery':
  # Floor panel normal and covering offset, independent measurement.
  output['floor_panel_z']={n:next(x for x in rows if x['object']==n) for n in ['Mesh468','Mesh1206','floorfront','Mesh1497','hallwayfloor']}
 (R/'DATOS'/f'deep_{label}.json').write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding='utf8')
 with (R/'DATOS'/f'componentes_{label}.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print('DEEP',label,'tris',sum(x['triangles'] for x in rows),'coincident',sum(len(x)-1 for x in globaltri.values() if len(x)>1),flush=True)
