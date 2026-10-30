"""Compile existing class IDs into a Core declarative catalog; no live crew data."""
import json, pathlib, sys
source=pathlib.Path(__file__).resolve().parents[3]/'mundo/lore/starships/classes/core_starship_classes.json'
classes=json.loads(source.read_text(encoding='utf-8'))['classes']
ids=[c['class_id'] for c in classes]
assert len(ids)==len(set(ids)) and 'miranda' in ids
assert all(s.replace('_','').isalnum() and s.isascii() for s in ids)
pathlib.Path(sys.argv[1]).write_text('/* Generated from core_starship_classes.json */\n'+
    'static constexpr const char* class_ids[] = {'+','.join(json.dumps(s) for s in ids)+'};\n'+
    'struct Complement { const char* id; uint64_t crew,residents; };\n'+
    'static constexpr Complement complements[] = {'+','.join('{'+json.dumps(c['class_id'])+','+str(c['nominal_complement']['starfleet'])+','+str(c['nominal_complement']['residents'])+'}' for c in classes if 'nominal_complement' in c)+'};\n',encoding='utf-8')
