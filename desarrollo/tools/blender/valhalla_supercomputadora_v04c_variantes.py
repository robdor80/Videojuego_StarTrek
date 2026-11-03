"""Create three reversible DIAGNOSTIC alternatives from the verified V04B.

Blender --background --factory-startup --python-exit-code 1 --python THIS_FILE --
  --input V04B.blend --output-dir NEW_DIRECTORY --evidence-dir NEW_DIRECTORY

A retains source placements 0840/3002; B retains 1921/3843; C proposes one
shared module at the mean centre and orientation of each pair, preserving A's
handedness and mesh data. Superseded originals are retained in a disabled
reference collection. No alternative is approved or written as a final V04C.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
import bpy
import numpy as np
from mathutils import Matrix

INPUT_SHA256='bb18697813040754122f5595f1d13d7eb93705828438e75a497cf460b251babd'
SOURCES=(('0840','1921'),('3002','3843'))
SIDES=('C01_Banco_A','C01_Banco_B','C02_Banco_A','C02_Banco_B')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def module_frame(obj):
    vertices=np.array([obj.matrix_world@v.co for v in obj.data.vertices]);matrix=np.array(obj.matrix_world)
    up=matrix[:3,1]/np.linalg.norm(matrix[:3,1]);normal=matrix[:3,2]/np.linalg.norm(matrix[:3,2]);tangent=np.cross(up,normal);tangent/=np.linalg.norm(tangent)
    basis=np.stack([tangent,up,normal],axis=1);projection=vertices@basis
    centre=(projection.min(0)+projection.max(0))/2@basis.T
    return centre,normal,tangent


def common_pose(a,b):
    ca,na,ta=module_frame(a);cb,nb,_=module_frame(b);normal=na+nb;normal/=np.linalg.norm(normal)
    tangent=np.cross(np.array([0.,0.,1.]),normal);tangent/=np.linalg.norm(tangent)
    angle=float(np.arctan2(np.cross(ta,tangent)[2],ta@tangent));c=np.cos(angle);s=np.sin(angle)
    rotation=np.array([[c,-s,0],[s,c,0],[0,0,1.]])
    result=np.eye(4);original=np.array(a.matrix_world);result[:3,:3]=rotation@original[:3,:3]
    result[:3,3]=rotation@(original[:3,3]-ca)+(ca+cb)/2
    return Matrix(result),{'rotation_from_a_deg':float(np.degrees(angle)),'centre_translation_from_a_m':((ca+cb)/2-ca).tolist()}


def main():
    parser=argparse.ArgumentParser()
    for name in ['input','output-dir','evidence-dir']:parser.add_argument('--'+name,required=True,type=Path)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);source=args.input.resolve();output=args.output_dir.resolve();evidence=args.evidence_dir.resolve()
    if sha(source)!=INPUT_SHA256:raise ValueError('Expected the reviewed, intact V04B')
    for directory in [output,evidence]:
        if directory==source.parent or (directory.exists() and any(directory.iterdir())):raise ValueError('Use new/empty diagnostic directories, outside the source folder')
    if output==evidence:raise ValueError('Use separate output and evidence directories')
    output.mkdir(parents=True,exist_ok=True);evidence.mkdir(parents=True,exist_ok=True)
    spec=importlib.util.spec_from_file_location('v04_helpers',Path(__file__).with_name('valhalla_supercomputadora_v04.py'));helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    results=[]
    for alternative in ['A','B','C']:
        bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(1);bpy.context.view_layer.update()
        original_states={o.name:helper.object_state(o) for o in bpy.data.objects};original_meshes={m.name:helper.mesh_digest(m) for m in bpy.data.meshes}
        reference=bpy.data.collections.new('V04C_REFERENCIA_206_NO_ACTIVA');scene.collection.children.link(reference);reference.hide_render=True;reference.hide_viewport=True
        proposals=bpy.data.collections.new('V04C_PROPUESTA_206_NO_APROBADA');scene.collection.children.link(proposals)
        pairs=[];archived=[];new_objects=[]
        def archive(obj):
            original_collections=[c.name for c in obj.users_collection]
            for collection in list(obj.users_collection):collection.objects.unlink(obj)
            reference.objects.link(obj);obj['V04C_colecciones_previas']=json.dumps(original_collections)
            archived.append({'object':obj.name,'original_collections':original_collections})
        for side in SIDES:
            for left,right in SOURCES:
                a=next(o for o in scene.objects if o.name.startswith(side) and '_'+left+'_' in o.name);b=next(o for o in scene.objects if o.name.startswith(side) and '_'+right+'_' in o.name)
                if a.get('fuente_componente')!='Component#206' or b.get('fuente_componente')!='Component#206':raise ValueError('Unexpected source component')
                pair={'id':side+'_'+left+'_'+right,'a':a.name,'b':b.name}
                if alternative=='A':archive(b);pair['active']=a.name
                elif alternative=='B':archive(a);pair['active']=b.name
                else:
                    matrix,measurement=common_pose(a,b);obj=a.copy();obj.name='V04C_DIAG_Compartido_'+pair['id'];obj.data=a.data;obj.matrix_world=matrix
                    for key in list(obj.keys()):del obj[key]
                    obj['fuente_componente']='Component#206';obj['V04C_pareja_fuente']=json.dumps([a.name,b.name]);obj['V04C_no_aprobado']=True
                    proposals.objects.link(obj);new_objects.append(obj.name);archive(a);archive(b);pair.update(active=obj.name,measurement=measurement)
                pairs.append(pair)
        assert set(original_states)<=set(bpy.data.objects.keys())
        for name,state in original_states.items():
            actual=helper.object_state(bpy.data.objects[name]);expected=dict(state)
            if any(a['object']==name for a in archived):expected['collections']=[reference.name]
            assert actual==expected,name
        assert all(helper.mesh_digest(bpy.data.meshes[n])==s for n,s in original_meshes.items())
        scene['estado_geometrico']='V04C DIAGNOSTICO '+alternative+' NO APROBADO: revisar lateralidad, jambas y remates; ultima entrega valida V04B'
        scene['V04C_variante_diagnostico']=alternative;scene['V04C_ultima_entrega_valida']='Sala_Supercomputadora_Valhalla_Puertas_V04B.blend'
        bpy.context.preferences.filepaths.save_version=0;target=output/('V04C_DIAG_'+alternative+'.blend')
        bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True,relative_remap=False)
        record={'variant':alternative,'file':target.name,'sha256':sha(target),'bytes':target.stat().st_size,'pairs':pairs,'archived_original_objects':archived,'new_objects':new_objects,'original_mesh_blocks_preserved':len(original_meshes),'approved':False}
        results.append(record);print('DIAGNOSTIC_VARIANT',alternative,target.name,len(archived),len(new_objects),flush=True)
        (evidence/'variantes_generadas.json').write_text(json.dumps(results,indent=2),encoding='utf8')
    assert sha(source)==INPUT_SHA256


if __name__=='__main__':main()
