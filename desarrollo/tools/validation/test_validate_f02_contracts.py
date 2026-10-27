"""Hermetic tests for F02 documentary validator; no Core/UE5 runtime."""
import json
import tempfile
import unittest
from pathlib import Path
from validate_f02_contracts import REG, blob_sha, check


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = []
        rows = []
        for i in range(24):
            path = f'data/model_{i}.json'
            data = {'schema_version': '0.1', 'a': 1, 'b': 2, 'c': 3, 'd': 4}
            dump(self.root / path, data)
            self.src.append(path)
            rows.append({'id':f'ID-{i}', 'source_path':path,
                         'source_blob_sha': blob_sha((self.root / path).read_bytes()),
                         'source_schema_version':'0.1',
                         'verified_source_selectors':['a','b','c'] + (['d'] if i == 0 else [])})
        self.p02 = {'records':rows}
        adapters = []
        for i in range(12):
            adapters.append({'id':f'ADP-{i+1:02d}',
                             'verified_source_refs':self.src[i:19:12],
                             'gap_refs':[f'P03-G{i+1:02d}'] if i < 11 else [],
                             'first_internal_sensors_slice':'MUST' if i < 8 else 'OPTIONAL',
                             'acceptance_test_refs':['F02-T01']})
        self.p03 = {'adapters': adapters}
        self.p04 = {'classification':'DESIGN_AND_STATIC_VALIDATION_ONLY',
                    'compatibility_axes':[{'id':f'A{i}'} for i in range(6)],
                    'compatibility_decisions':[{'id':f'D{i}'} for i in range(10)],
                    'failures':[{'id':f'E{i}', 'test_refs':['F02-T01']} for i in range(13)],
                    'tests':[{'id':f'F02-T{i:02d}', 'adapter_ref':'ADP-01'} for i in range(1,17)],
                    'migration_preflight':[], 'forbidden_shortcuts':[]}
        self.sensor_path = self.root / 'sistemas/gameplay/ship_operations/sensor_resolution/sensor_result_contract.json'
        dump(self.sensor_path, {'forbidden_player_fields':[
            'authoritative_entity_id','ground_truth','unrevealed_hidden_properties']})
        self.save_all()

    def save_all(self):
        dump(self.root / REG / 'INVENTARIO_INTERCAMBIO_P02.json', self.p02)
        dump(self.root / REG / 'MAPA_ADAPTADORES_P03.json', self.p03)
        dump(self.root / REG / 'REGISTRO_FALLOS_COMPATIBILIDAD_P04.json', self.p04)

    def errors(self):
        return check(self.root)[1]

    def test_valid_fixture(self):
        self.assertEqual(self.errors(), [])

    def test_blob_sha_drift(self):
        dump(self.root / self.src[5], {'schema_version':'0.1','a':999,'b':2,'c':3,'d':4})
        self.assertIn('Git blob SHA drift', ' '.join(self.errors()))

    def test_missing_p02_selector(self):
        self.p02['records'][0]['verified_source_selectors'][0] = 'missing'
        self.save_all()
        self.assertIn('selector missing', ' '.join(self.errors()))

    def test_missing_gap(self):
        self.p03['adapters'][0]['gap_refs'] = []
        self.save_all()
        self.assertIn('gap coverage mismatch', ' '.join(self.errors()))

    def test_broken_test_ref(self):
        self.p04['failures'][1]['test_refs']=['F02-T99']
        self.save_all()
        self.assertIn('missing/unknown test reference', ' '.join(self.errors()))

    def test_leaked_sensor_field_requirement(self):
        dump(self.sensor_path, {'forbidden_player_fields':['ground_truth']})
        self.assertIn('anti-leak fields missing', ' '.join(self.errors()))

    def test_missing_source(self):
        (self.root / self.src[0]).unlink()
        self.assertIn('missing source', ' '.join(self.errors()))

    def test_duplicate_adapter(self):
        self.p03['adapters'][1]['id']='ADP-01'
        self.save_all()
        self.assertIn('duplicate/empty id', ' '.join(self.errors()))

    def test_windows_crlf_checkout(self):
        p=self.root/self.src[2]
        p.write_bytes(p.read_bytes().replace(b'\n', b'\r\n'))
        self.assertEqual(self.errors(), [])


if __name__ == '__main__':
    unittest.main()
