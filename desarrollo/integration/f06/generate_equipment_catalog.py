"""Compile explicitly fictional QA reference equipment, never installed truth."""
import argparse
import json
from pathlib import Path
SOURCE = Path(__file__).resolve().parents[3] / 'sistemas/gameplay/ship_operations/consoles/sensors/equipment_catalog_qa_v1.json'

SLOTS = ['offensive_energy_emitters', 'launchers', 'shield_generators',
         'armour_layers', 'warp_drives', 'impulse_drives']

def require(condition, message):
    if not condition:
        raise ValueError(message)

def build(source=SOURCE):
    data = json.loads(source.read_text(encoding='utf-8'))
    require(type(data['version']) is int and data['version'] == 1 and
            data['status'] == 'QA_FICTION_NON_CANON', 'Unsupported or non-QA catalog')
    require(data['slots'] == SLOTS, 'Equipment slot semantics/order changed')
    require(0 < len(data['classes']) <= 1024, 'Invalid catalog size')
    seen = set()
    rows = []
    for row in data['classes']:
        cid, counts = row['class_id'], row['count']
        require(type(cid) is int and 0 < cid < 10000 and cid not in seen, 'Invalid/duplicate class')
        require(len(counts) == 6 and all(type(n) is int and 0 <= n <= 64 for n in counts), 'Invalid equipment count')
        seen.add(cid)
        rows.append('{' + str(cid) + ', {' + ','.join(map(str, counts)) + '}}')
    registry = json.loads(SOURCE.with_name('ship_class_registry.json').read_text(encoding='utf-8'))
    require(seen == {row['id'] for row in registry['classes']}, 'Every registered design needs an explicit QA reference')
    return '#pragma once\nstruct F06EquipmentCatalog { unsigned class_id,count[6]; };\ninline constexpr F06EquipmentCatalog F06_EQUIPMENT_CATALOG[] = {\n' + ',\n'.join(rows) + '\n};\n'

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--out', type=Path, required=True)
    a = p.parse_args(); a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(build(), encoding='utf-8')
