import json,hashlib,math,re,csv,collections
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];originals=Path(r'C:\Users\andro\Documents\Voyager_Bridge_Recovery\originales');desktop=Path(r'C:\Users\andro\Desktop\Nueva carpeta\TrekmeshesEU_Chainsaw_USSVoyagerBridge_OBJ')
textures=[];formats={'.png','.jpg','.jpeg','.tga','.bmp','.tif','.tiff','.dds'}
for root in [originals,desktop]:
 for p in root.rglob('*'):
  if not p.is_file() or p.suffix.lower() not in formats:continue
  row={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
  try:
   with Image.open(p) as im:im.load();row.update(width=im.width,height=im.height,mode=im.mode,decode='OK')
  except Exception as e:row['decode']=str(e)
  textures.append(row)
def norm(s):return re.sub('[^a-z0-9]','',Path(s.replace('\\','/')).stem.lower())
recovery=json.loads((R/'DATOS/blender_recovery.json').read_text(encoding='utf8'));candidates=[]
for im in recovery['images']:
 if im['source']!='FILE':continue
 matches=[t['path'] for t in textures if norm(t['path'])==norm(im['name'])]
 candidates.append({'image':im['name'],'declared_path':im['filepath'],'original_path_exists':im['original_external_exists'],'basename_candidates':matches,'scope':'name similarity only; not proof of shader assignment'})
mtls=[]
for p in [desktop/'VoyagerB.Mtl',desktop/'VoyagerB_original.Mtl']:
 current=None;materials=[]
 for line in p.read_text(encoding='latin1').splitlines():
  ls=line.strip()
  if ls.startswith('newmtl '):current={'material':ls[7:],'maps':[]};materials.append(current)
  if current and (ls.lower().startswith('map_') or ls.lower().startswith('bump ')):
   command,ref=ls.split(None,1);actual=p.parent/ref.replace('\\','/');current['maps'].append({'channel':command,'reference':ref,'exists':actual.is_file(),'resolved':str(actual)})
 mtls.append({'path':str(p),'materials':materials})
glbs=json.loads((R/'DATOS/glb_resumen.json').read_text(encoding='utf8'));materials=[]
for g in glbs:
 for i,m in enumerate(g['materials']):
  pr=m.get('pbrMetallicRoughness',{});maps={}
  for k,v in pr.items():
   if k.endswith('Texture'):maps[k]=v
  for k,v in m.items():
   if k.endswith('Texture'):maps[k]=v
  materials.append({'source':g['path'],'index':i,'name':m.get('name'),'baseColorFactor':pr.get('baseColorFactor',[1,1,1,1]),'metallic':pr.get('metallicFactor',1),'roughness':pr.get('roughnessFactor',1),'emissive':m.get('emissiveFactor',[0,0,0]),'doubleSided':m.get('doubleSided',False),'maps':maps,'extensions':m.get('extensions',{})})
data={'external_images':textures,'recovery_image_candidates':candidates,'mtl':mtls,'gltf_materials':materials}
(R/'DATOS/materiales_auditoria.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8')
for name,rows in [('texturas_externas',textures),('materiales_gltf',materials),('recovery_candidatos_imagen',candidates)]:
 with (R/'DATOS'/f'{name}.csv').open('w',newline='',encoding='utf-8-sig') as f:
  wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
print('external',len(textures),'failures',[t['path'] for t in textures if t['decode']!='OK']);print('roots',collections.Counter('recovery' if 'Recovery' in t['path'] else 'desktop' for t in textures));print('recovery basename candidates',sum(bool(x['basename_candidates']) for x in candidates),'of',len(candidates))
for x in mtls:print('MTL',x['path'],'mats',len(x['materials']),'maps',sum(len(m['maps']) for m in x['materials']),'broken',sum(not x['exists'] for m in x['materials'] for x in m['maps']))
for g in glbs:
 mats=[m for m in materials if m['source']==g['path']];print('GLB maps',Path(g['path']).name,collections.Counter(k for m in mats for k in m['maps']),'extensions',g['extensionsUsed'])
