import sys,json,hashlib,argparse
from pathlib import Path
sys.dont_write_bytecode=True
import bpy,numpy as np
from mathutils import Matrix,Vector
parser=argparse.ArgumentParser(description='Export the validated V04E to explicit UE coordinates, preserving source UV and normals.')
parser.add_argument('--input',required=True)
parser.add_argument('--output-dir',required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
source=Path(args.input).resolve()
out=Path(args.output_dir).resolve()
assert hashlib.sha256(source.read_bytes()).hexdigest()=='e55df3cf537365ac8e145b9a7cd96605f5b0edaa5537473a734f090f931a8670'
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
out.mkdir(exist_ok=False,parents=True);images=out/'imagenes';images.mkdir()
leaves=['Component_435035','Component_435936'];C=Matrix.Diagonal((100.,-100.,100.,1.));CI=C.inverted()
materials=[]
for material in bpy.data.materials:
    principled=next((n for n in material.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if material.node_tree else None
    tex=next((n.image for n in material.node_tree.nodes if n.type=='TEX_IMAGE' and n.image),None) if material.node_tree else None
    if tex:
        assert tex.packed_file
        file=images/Path(tex.filepath).name
        if not file.exists():file.write_bytes(bytes(tex.packed_file.data))
    materials.append({'name':material.name,'color':list(principled.inputs['Base Color'].default_value if principled else material.diffuse_color),'alpha':float(principled.inputs['Alpha'].default_value if principled else material.diffuse_color[3]),'roughness':float(principled.inputs['Roughness'].default_value) if principled else .5,'metallic':float(principled.inputs['Metallic'].default_value) if principled else 0.,'image':('imagenes/'+file.name) if tex else None})

def transformed(v):return [float(v[0]*100),float(-v[1]*100),float(v[2]*100)]
def payload(obj,world=None,origin=None):
    mesh=obj.data;mesh.calc_loop_triangles();v=[v.co.copy() for v in mesh.vertices]
    normalmatrix=world.to_3x3().inverted().transposed() if world is not None else None
    if world is not None:v=[world@point-Vector(origin) for point in v]
    vertices=[transformed(point) for point in v];triangles=[]
    assert len(mesh.uv_layers)<=1,('Review extra UV channels',mesh.name)
    for tri in mesh.loop_triangles:
        order=[0,2,1];indices=[int(tri.vertices[j]) for j in order];loops=[tri.loops[j] for j in order]
        normals=[]
        for li in loops:
            n=mesh.corner_normals[li].vector.copy()
            if normalmatrix is not None:n=normalmatrix@n
            n.normalize();normals.append([float(n.x),float(-n.y),float(n.z)])
        triangles.append({'v':indices,'uv':[[float(x) for x in mesh.uv_layers[0].data[li].uv] if mesh.uv_layers else [0.,0.] for li in loops],'n':normals,'material':int(mesh.polygons[tri.polygon_index].material_index)})
    return {'vertices':vertices,'triangles':triangles,'materials':[m.name if m else 'Material' for m in mesh.materials]}

poses={}
for frame in [1,20,60]:
    scene.frame_set(frame);bpy.context.view_layer.update();poses[frame]={}
    for name in leaves:
        found=[(i.object.original,i.matrix_world.copy()) for i in bpy.context.evaluated_depsgraph_get().object_instances if i.parent and i.parent.name==name and i.object.type=='MESH'];assert len(found)==1
        obj,matrix=found[0];v=np.array([matrix@v.co for v in obj.data.vertices]);poses[frame][name]={'object':obj,'matrix':matrix,'min':v.min(0),'max':v.max(0),'center':(v.min(0)+v.max(0))/2}
scene.frame_set(20);bpy.context.view_layer.update()
closed=[poses[20][n] for n in leaves];opened=[poses[60][n] for n in leaves]
allmin=np.min([r['min'] for r in closed],axis=0);allmax=np.max([r['max'] for r in closed],axis=0);root=(allmin+allmax)/2;root[2]=allmin[2]
door={'id':'VALHALLA_SC_EXTERIOR_D01','root':transformed(root),'opening_width_cm':float((opened[0]['min'][1]-opened[1]['max'][1])*100),'opening_height_cm':float((allmax[2]-allmin[2])*100),'leaves':[],'capsule_radius_cm':35.,'capsule_half_height_cm':90.}
meshes={};instances=[]
for index,name in enumerate(leaves):
    r=closed[index];key='Hoja_Izquierda' if index==0 else 'Hoja_Derecha';meshes[key]=payload(r['object'],r['matrix'],r['center']);delta=opened[index]['center']-r['center'];assert abs(delta[0])<1e-5 and abs(delta[2])<1e-5
    door['leaves'].append({'name':name,'mesh':key,'closed':transformed(r['center']-root),'travel':transformed(delta)})
assert abs(door['leaves'][0]['travel'][1]+door['leaves'][1]['travel'][1])<.001
door['travel_cm']=abs(door['leaves'][0]['travel'][1])
for item in bpy.context.evaluated_depsgraph_get().object_instances:
    obj=item.object.original
    if obj.type!='MESH' or not obj.data.polygons or (item.parent and item.parent.name in leaves):continue
    key='M_'+obj.data.name
    if key not in meshes:meshes[key]=payload(obj)
    matrix=C@item.matrix_world@CI
    if matrix.determinant()<0:
        mirrored=key+'_MirrorX'
        if mirrored not in meshes:
            import copy
            data=copy.deepcopy(meshes[key])
            for v in data['vertices']:v[0]=-v[0]
            for tr in data['triangles']:
                for field in ['v','uv','n']:tr[field]=[tr[field][j] for j in [0,2,1]]
                for normal in tr['n']:normal[0]=-normal[0]
            meshes[mirrored]=data
        key=mirrored;matrix=matrix@Matrix.Diagonal((-1.,1.,1.,1.))
    location,rotation,scale=matrix.decompose();assert min(scale)>0,(obj.name,list(scale))
    rebuilt=Matrix.LocRotScale(location,rotation,scale)
    assert max(abs(matrix[i][j]-rebuilt[i][j]) for i in range(4) for j in range(4))<1e-4,('Affine shear requires a baked variant',obj.name)
    instances.append({'mesh':key,'source_object':obj.name,'source_instance':item.parent.name if item.parent else obj.name,'location':list(location),'rotation':[rotation.x,rotation.y,rotation.z,rotation.w],'scale':list(scale)})
record={'schema':1,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'coordinates':'UE cm: X=100 Blender X, Y=-100 Blender Y, Z=100 Blender Z; triangle winding reversed; explicit loop normals and original UV','door':door,'materials':materials,'meshes':meshes,'instances':instances}
(out/'sala_v04e.json').write_text(json.dumps(record,separators=(',',':'),allow_nan=False),encoding='utf8')
print('EXPORTED',len(meshes),'meshes',len(instances),'placements',len(materials),'materials','door',door,flush=True)
