"""Static inventory only. Does NOT compile UBT/UHT or execute Unreal tests."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
sources = list((ROOT / 'unreal/Source').rglob('*.cpp'))
text = '\n'.join(p.read_text(encoding='utf-8') for p in sources)
expected = json.loads((ROOT / 'unreal/expected-tests.json').read_text())
actual = re.findall(r'IMPLEMENT_SIMPLE_AUTOMATION_TEST\([^,]+,"(F05\.[^"]+)"', text)
assert len(expected) == len(set(expected)) == len(actual) == 12
assert sorted(actual) == sorted(expected), 'Missing, duplicate or unexpected Unreal automation'
headers = list((ROOT / 'include').glob('*.h')) + [ROOT / '../f04/include/f04_bridge.h']
api = '\n'.join(p.read_text(encoding='utf-8') for p in headers)
calls = set(re.findall(r'\b(f0[45]_\w+)\s*\(', text))
declared = set(re.findall(r'F04_API\s+(?:const\s+)?\w+(?:\s*\*)?\s+(f0[45]_\w+)\s*\(', api))
assert calls <= declared, f'Unreal calls undeclared ABI: {calls - declared}'
print(json.dumps({'result': 'PASS_STATIC_ONLY', 'automation_names': sorted(actual),
                  'declared_abi_calls_checked': len(calls), 'ubt_uht': 'NO_EJECUTADO',
                  'unreal_execution': 'NO_EJECUTADO', 'real_rhi': 'NO_EJECUTADO'}, indent=2))
