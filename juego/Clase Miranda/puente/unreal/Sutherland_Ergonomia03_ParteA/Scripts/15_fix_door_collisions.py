import unreal as u,json,pathlib,traceback,hashlib,shutil
R=pathlib.Path(__file__).resolve().parents[1];D=R/'Data';P=R/'Unreal';out={'ok':False,'modified':[]};backup=R/'Backups/Puertas_20261028';backup.mkdir(exist_ok=True)
assert pathlib.Path(u.Paths.project_dir()).resolve()==P
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def package_path(mesh):return P/'Content'/(mesh.get_path_name().split('.')[0].removeprefix('/Game/')+'.uasset')
def render_digest(mesh):
 data=[]
 for si in range(mesh.get_num_sections(0)):
  v,t,n,uv,tan=u.ProceduralMeshLibrary.get_section_from_static_mesh(mesh,0,si)
  data.append({'v':[list(x.to_tuple()) for x in v],'t':list(t),'n':[list(x.to_tuple()) for x in n],'uv':[list(x.to_tuple()) for x in uv],'tangent':[[list(x.tangent_x.to_tuple()),x.flip_tangent_y] for x in tan]})
 slots=[{'name':str(x.material_slot_name),'imported':str(x.get_editor_property('imported_material_slot_name')),'material':x.material_interface.get_path_name() if x.material_interface else None} for x in mesh.get_editor_property('static_materials')]
 return hashlib.sha256(json.dumps({'sections':data,'materials':slots},sort_keys=True).encode()).hexdigest()
def positions(dm):return u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm,False)[1])
try:
 if (D/'doors_20261028_fix.json').exists():assert not json.loads((D/'doors_20261028_fix.json').read_text()).get('ok'),'Already fixed; verify only'
 A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem);assert L.load_level('/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01')
 mp=P/'Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap';bp=backup/mp.name
 if not bp.exists():shutil.copy2(mp,bp)
 assert sha(mp)==sha(bp);out['map_before_sha256']=sha(mp)
 doors=sorted([a for a in A.get_all_level_actors() if isinstance(a,u.STAutomaticDoor)],key=lambda a:str(a.door_id))
 for door in doors:
  floor=60. if str(door.door_id) in ['DOOR_F07_001','DOOR_F07_003'] else (.1 if str(door.door_id)=='DOOR_F07_004' else 0.)
  for side,c in [('LeftLeaf',door.left_leaf),('RightLeaf',door.right_leaf)]:
   mesh=c.static_mesh;path=package_path(mesh);dest=backup/'Content'/path.relative_to(P/'Content');dest.parent.mkdir(parents=True,exist_ok=True)
   if not dest.exists():shutil.copy2(path,dest)
   before_hash=sha(dest);assert sha(path)==before_hash,('Changed since backup',str(path));before_render=render_digest(mesh)
   cut=floor+.2-c.get_world_location().z;kept=None
   for flip in [False,True]:
    dm=u.DynamicMesh();u.GeometryScript_SceneUtils.copy_collision_meshes_from_object(c,dm,False);initial=positions(dm);initial_max=max(v.z for v in initial)
    opt=u.GeometryScriptMeshPlaneCutOptions();opt.fill_holes=True;opt.fill_spans=True;opt.flip_cut_side=flip
    u.GeometryScript_MeshBooleans.apply_mesh_plane_cut(dm,u.Transform(location=u.Vector(0,0,cut)),opt);vs=positions(dm)
    if vs and abs(max(v.z for v in vs)-initial_max)<.001 and abs(min(v.z for v in vs)-cut)<.001:kept=dm;break
   assert kept,('Could not retain upper collision half',str(door.door_id),side)
   cfg=u.GeometryScriptCollisionFromMeshOptions();cfg.method=u.GeometryScriptCollisionGenerationMethod.CONVEX_HULLS;cfg.auto_detect_spheres=False;cfg.auto_detect_boxes=False;cfg.auto_detect_capsules=False;cfg.simplify_hulls=False;cfg.max_convex_hulls_per_mesh=1;cfg.min_thickness=.01;cfg.remove_fully_contained_shapes=False
   coll=u.GeometryScript_Collision.generate_collision_from_mesh(kept,cfg)
   u.GeometryScript_Collision.set_simple_collision_of_static_mesh(coll,mesh,u.GeometryScriptSetSimpleCollisionOptions(),u.GeometryScriptSetStaticMeshCollisionOptions())
   assert render_digest(mesh)==before_render,'Visible geometry/material/UV changed'
   assert u.EditorAssetLibrary.save_loaded_asset(mesh)
   out['modified'].append({'door':str(door.door_id),'side':side,'asset':mesh.get_path_name(),'package':str(path),'backup':str(dest),'before_sha256':before_hash,'after_sha256':sha(path),'render_material_uv_digest':before_render,'visual_unchanged':True,'floor_cm':floor,'collision_lower_world_z_cm':floor+.2,'method':'Clip only hidden collision below floor + 0.2 cm; retain upper convex hull, render/UV/materials unchanged.'})
   (D/'doors_20261028_fix_inprogress.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 assert len(out['modified'])==8;assert sha(mp)==out['map_before_sha256'];out['ok']=True
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(D/'doors_20261028_fix.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('DOOR_COLLISION_FIX',out['ok'],len(out['modified']),out.get('error'));u.SystemLibrary.quit_editor()

