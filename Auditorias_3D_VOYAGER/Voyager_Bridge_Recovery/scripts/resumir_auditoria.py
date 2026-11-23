import json,collections
from pathlib import Path
r=json.loads((Path(__file__).resolve().parents[1]/'informes/auditoria_voyager.json').read_text())
print('SCOPE',r['scope']);print('SCENES',[(s['name'],s['units']) for s in r['scenes']]);print('COLLECTIONS',[(c['name'],len(c['objects'])) for c in r['collections']])
print('TYPE',collections.Counter(o['type'] for o in r['objects']))
print('IMAGES',collections.Counter(i['status'] for i in r['images']))
for i in r['images']: print('IMAGE',i['name'],i['size'],i['status'],i['filepath'],i['colorspace'],len(i['packed_files']),i['external_exists'])
print('OBJ',[(o['name'],o['collections'],o['hide_viewport'],o['hide_get'],o['hide_render'],o['mesh']['vertices'],o['mesh']['polygons'],o['mesh']['bounds_world'],len(o['material_slots'])) for o in r['objects'] if o['name']=='Voyager Bridge'])
print('MAX STREAMS',r['max_binary']['streams'])
for x in r['max_binary']['strings']:
 print('STRINGS',x['stream'],len(x['hits']),[h['text'] for h in x['hits'][:35]])
print('POSER',r['poser']['material_count'],[(m['name'],m['line']) for m in r['poser']['materials']])
for m in r['materials']:
 assignments=[a for a in m['assignments'] if a['subset']!='legacy_OBJ']
 if assignments:
  print('MAT',repr(m['name']),'NORMAL',m['normalized_name'],'NODES',[n['type'] for n in m['nodes']], 'COLOR',m['diffuse_color'],'OBJ',[(a['object'],a['faces']) for a in assignments], 'POSER',m['poser_exact_normalized_candidates'])
  if any(w in m['normalized_name'] for w in ['light','glow']):
   print('DETAIL',json.dumps(m,ensure_ascii=True))
print('MESH468',json.dumps(next(o for o in r['objects'] if o['name']=='Mesh468'),ensure_ascii=True))
