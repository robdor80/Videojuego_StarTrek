"""Guard the approved source and scope, independently of mutable campaign state."""
from pathlib import Path
import importlib.util
import json
import unittest

HERE=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('generator', HERE/'generate_valhalla_profile.py')
generator=importlib.util.module_from_spec(spec);spec.loader.exec_module(generator)

class Contracts(unittest.TestCase):
    def test_generated_source_matches_authority(self):
        self.assertEqual((HERE/'src/f04_valhalla.h').read_text(encoding='utf-8'),generator.render())
        approved=generator.rows()
        fixture=[list(map(int,line.split())) for line in (HERE/'tests/fixtures/valhalla_approved.tsv').read_text().splitlines()]
        self.assertEqual(fixture,[[s,t,a,b,g,o] for s,d,n,t,a,b,g,o in approved])
        self.assertEqual(sum(r[3] for r in approved if r[0] in [12,26,51,62,90]),40)
        self.assertEqual(sum(r[3] for r in approved if 63<=r[0]<=70),60)
    def test_separation_preparation_is_not_integration(self):
        contract=json.loads((HERE/'tests/fixtures/valhalla_areas_contract.json').read_text(encoding='utf-8'))
        self.assertEqual(contract['integration_reserved'],'F04-INTEGRACION-04')
        for field in ['separation_executable','embarkation_transfers_executable','defiant_independent_watch_coverage_certified','physical_scenes_modified','quantum_slipstream_installed_at_2387','cloak_executable','combat_executable']:
            self.assertFalse(contract[field])
        self.assertEqual(contract['areas'][3]['dedicated_section_ids'],[12,26,51,62,90])
        self.assertIn('independent_command_required',contract['areas'][0]['capabilities'])
        self.assertIn('independent_command_required',contract['areas'][1]['capabilities'])
        self.assertIsNone(contract['defiant_docking_anchor_section'])

if __name__=='__main__':unittest.main()
