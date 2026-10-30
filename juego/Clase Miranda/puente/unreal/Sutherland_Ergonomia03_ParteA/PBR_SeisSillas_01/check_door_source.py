import bpy,json,pathlib,math
R=pathlib.Path(__file__).parent
old=json.loads((R.parent/'Data/export_meshes.json').read_text())
out=[]
for n in sorted({d['source'] for d in old['doors']}):
    o=bpy.data.objects[n];new=[(v.x*100,-v.y*100,v.z*100) for v in [o.matrix_world@v.co for v in o.data.vertices]]
    previous=[v for d in old['doors'] if d['source']==n for v in d['expected_world_cm']]
    # Same source topology and both leaf halves, independent of vertex ordering.
    def keys(points):return {tuple(round(v,2) for v in p) for p in points}
    out.append({'source':n,'source_vertices':len(new),'old_leaf_vertices':len(previous),'world_vertices_match_0_01cm':keys(new)==keys(previous)})
(R/'door_source_verification.json').write_text(json.dumps(out,indent=2))
print(out)
