import json,struct,math,collections,hashlib,io,csv
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];summ=json.loads((R/'DATOS/glb_resumen.json').read_text(encoding='utf8'));allout=[];images=[]
for s in summ:
 p=Path(s['path']);data=p.read_bytes();off=12;j=None;binary=b''
 while off<len(data):
  sz,ty=struct.unpack_from('<II',data,off);off+=8
  if ty==0x4e4f534a:j=json.loads(data[off:off+sz])
  if ty==0x004e4942:binary=data[off:off+sz]
  off+=sz
 def accessor(i):
  a=j['accessors'][i];v=j['bufferViews'][a['bufferView']];typ={5126:'f',5125:'I',5123:'H',5121:'B',5122:'h',5120:'b'}[a['componentType']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];fmt='<'+typ*n;sz=struct.calcsize(fmt);stride=v.get('byteStride',sz);start=v.get('byteOffset',0)+a.get('byteOffset',0)
  return [struct.unpack_from(fmt,binary,start+k*stride) for k in range(a['count'])]
 out={'path':str(p),'primitives':[],'accessor_errors':[],'images':[]}
 for i,a in enumerate(j.get('accessors',[])):
  try:accessor(i)
  except Exception as e:out['accessor_errors'].append({'accessor':i,'error':str(e)})
 for mi,me in enumerate(j['meshes']):
  for pi,pr in enumerate(me['primitives']):
   pos=accessor(pr['attributes']['POSITION']);uv=accessor(pr['attributes']['TEXCOORD_0']) if 'TEXCOORD_0'in pr['attributes'] else [];norm=accessor(pr['attributes']['NORMAL']) if 'NORMAL'in pr['attributes'] else [];inds=[x[0] for x in accessor(pr['indices'])] if 'indices'in pr else list(range(len(pos)))
   bad=repeat=zero=uvzero=opposite=normbad=0;geotris=[]
   for k in range(0,len(inds),3):
    ids=inds[k:k+3]
    if len(ids)!=3:continue
    if any(i<0 or i>=len(pos) for i in ids):bad+=1;continue
    if len(set(ids))<3:repeat+=1
    a,b,c=[pos[i] for i in ids];ab=[b[i]-a[i] for i in range(3)];ac=[c[i]-a[i] for i in range(3)];cross=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]];area=math.sqrt(sum(x*x for x in cross))/2
    if area<1e-10:zero+=1
    elif norm:
     avg=[sum(norm[idx][i] for idx in ids)/3 for i in range(3)]
     if sum(cross[i]*avg[i] for i in range(3))<0:opposite+=1
    if uv:
     a,b,c=[uv[i] for i in ids]
     if abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))<1e-12:uvzero+=1
    geotris.append(tuple(sorted(tuple(round(x,6) for x in pos[idx]) for idx in ids)))
   if norm:normbad=sum(abs(math.sqrt(sum(x*x for x in n))-1)>0.01 for n in norm)
   out['primitives'].append({'mesh':mi,'name':me.get('name'),'primitive':pi,'material':pr.get('material'),'vertices':len(pos),'triangles':len(inds)//3,'invalid_indices':bad,'repeated_index_triangles':repeat,'area_below_1e_10':zero,'uv_zero_area':uvzero,'normals_opposed_to_winding':opposite,'normals_nonunit_001':normbad,'duplicate_triangles_local_1e6':sum(n-1 for n in collections.Counter(geotris).values() if n>1)})
 for idx,im in enumerate(j.get('images',[])):
  v=j['bufferViews'][im['bufferView']];blob=binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']];row={'index':idx,'name':im.get('name'),'mime':im.get('mimeType'),'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest()}
  try:
   pic=Image.open(io.BytesIO(blob));pic.load();row.update(width=pic.width,height=pic.height,mode=pic.mode,decode='OK');images.append((row.copy(),pic.copy()))
  except Exception as e:row['decode']=str(e)
  out['images'].append(row)
 out['totals']={k:sum(x[k] for x in out['primitives']) for k in ['vertices','triangles','invalid_indices','repeated_index_triangles','area_below_1e_10','uv_zero_area','normals_opposed_to_winding','normals_nonunit_001','duplicate_triangles_local_1e6']};allout.append(out)
(R/'DATOS/gltf_validacion_numerica.json').write_text(json.dumps(allout,indent=2,ensure_ascii=False),encoding='utf8')
if images:
 out=Image.new('RGB',(1400,math.ceil(len(images)/7)*160),'#222222');d=ImageDraw.Draw(out)
 for n,(row,pic) in enumerate(images):
  pic.thumbnail((190,130));x=(n%7)*200;y=(n//7)*160;out.paste(pic.convert('RGB'),(x,y));d.text((x+3,y+132),f"{row['index']} {row['name'] or ''}"[:29],fill='white')
 out.save(R/'CAPTURAS/texturas_embebidas_OBJ.png')
print(json.dumps([{'path':x['path'],'totals':x['totals'],'images_decoded':len(x['images']),'accessor_errors':x['accessor_errors']} for x in allout],indent=2))
