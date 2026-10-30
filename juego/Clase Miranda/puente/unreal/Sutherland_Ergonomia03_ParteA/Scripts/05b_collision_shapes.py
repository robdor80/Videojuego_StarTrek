import unreal as u,json,pathlib,traceback
R=pathlib.Path(__file__).resolve().parents[1];D=R/'Data';out={'ok':False,'actors':{}}
try:
 A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem);assert L.load_level('/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01')
 plan=json.loads((D/'export_meshes.json').read_text());wanted={x['actor'] for x in plan['collisions']+plan['doors']}
 for a in A.get_all_level_actors():
  if a.get_actor_label() not in wanted:continue
  out['actors'][a.get_actor_label()]={}
  for c in a.get_components_by_class(u.StaticMeshComponent):
   m=c.static_mesh
   if not m:continue
   def lib(s):return getattr(u,next(n for n in dir(u) if s in n))
   scene=lib('SceneUtilityFunctions') if any('SceneUtilityFunctions' in n for n in dir(u)) else lib('SceneUtils')
   query=lib('MeshQueryFunctions') if any('MeshQueryFunctions' in n for n in dir(u)) else lib('MeshQueries')
   lists=lib('ListUtilityFunctions') if any('ListUtilityFunctions' in n for n in dir(u)) else getattr(u,'GeometryScript_List')
   dm=u.DynamicMesh();res=scene.copy_collision_meshes_from_object(c,dm,True)
   print('COLL_COPY',a.get_actor_label(),str(res)[:200])
   vr=query.get_all_vertex_positions(dm,False);tt=query.get_all_triangle_indices(dm,False)
   vv=lists.convert_vector_list_to_array(vr[1]);tri=lists.convert_triangle_list_to_array(tt[1])
   rendered=[]
   for si in range(m.get_num_sections(0)):
    points,_,_,_,_=u.ProceduralMeshLibrary.get_section_from_static_mesh(m,0,si)
    rendered.extend([list(c.get_world_transform().transform_location(v).to_tuple()) for v in points])
   out['actors'][a.get_actor_label()][c.get_name()]={'mesh':m.get_path_name(),'world_cm':[list(v.to_tuple()) for v in vv],'triangles':[[v.x,v.y,v.z] for v in tri],'rendered_world_cm':rendered}
 out['ok']=True
except Exception:out['error']=traceback.format_exc();print(out['error'])
(D/'collision_shapes_before.json').write_text(json.dumps(out),encoding='utf-8');print('COLLISION_DUMP',out['ok']);u.SystemLibrary.quit_editor()
