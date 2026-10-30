"""Documentary boundaries: these contracts never install equipment in Core."""
import json
from pathlib import Path
import unittest

FIXTURES = Path(__file__).resolve().parent / 'fixtures'
ROOT = FIXTURES.parents[4]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


class OdysseyContracts(unittest.TestCase):
    def test_facilities_share_intrepid_rules(self):
        contract = read(FIXTURES / 'odyssey_facilities_contract.json')
        inherited = read(ROOT / contract['contract_ref'])
        self.assertEqual(contract['template_id'], 4)
        self.assertEqual(contract['clock'], inherited['clock'])
        self.assertEqual(contract['authority'], inherited['authority'])
        self.assertFalse(contract['runtime_reservations_implemented'])
        self.assertFalse(contract['runtime_facilities_instantiated'])
        config = contract['reference_configuration']
        self.assertIsNone(config['facility_count'])
        self.assertEqual(config['facilities'], [])
        self.assertFalse(config['capabilities']['emh']['counts_as_fleet_crew'])
        self.assertFalse(config['capabilities']['aquarius']['installed_by_default'])
        self.assertFalse(config['capabilities']['aquarius']['creates_people_on_deployment'])
        self.assertIsNone(config['capabilities']['auxiliary_craft']['count'])

    def test_experimental_program_inherits_approved_decision(self):
        contract = read(FIXTURES / 'odyssey_experimental_program_contract.json')
        approved = read(ROOT / contract['contract_ref'])
        self.assertTrue((ROOT / contract['decision_ref']).is_file())
        self.assertTrue((ROOT / contract['general_capability_contract']).is_file())
        self.assertEqual(contract['capability_id'], approved['capability_id'])
        self.assertEqual(contract['class_operational_by_year'], 2383)
        self.assertEqual(approved['program']['odyssey_test_phase']['from_year'], 2383)
        self.assertFalse(contract['installed_by_default'])
        self.assertFalse(approved['program']['odyssey_test_phase']['class_wide_default'])
        self.assertFalse(contract['runtime_implemented'])
        self.assertTrue(contract['conventional_warp_retained'])
        self.assertTrue(contract['quantum_torpedoes_are_distinct'])
        self.assertEqual(contract['valhalla_first_service_target_year'], 2387)
        self.assertFalse(contract['valhalla_slipstream_installed_at_commissioning'])
        self.assertFalse(contract['player_participation_required'])
        self.assertFalse(contract['automatic_future_events'])
        self.assertIsNone(contract['individual_hull_identity'])
        self.assertIsNone(contract['exact_hull_commission_date'])

    def test_specialists_use_existing_sections_without_new_people(self):
        contract = read(FIXTURES / 'odyssey_experimental_program_contract.json')
        rows = [list(map(int, line.split())) for line in
                (FIXTURES / 'odyssey_approved.tsv').read_text().splitlines()]
        self.assertEqual(len(rows), 72)
        self.assertEqual([sum(r[i] for r in rows) for i in range(1, 6)],
                         [1600, 500, 330, 205, 565])
        self.assertEqual(contract['additional_departments'], 0)
        self.assertEqual(contract['additional_sections'], 0)
        ranges = {'command': range(1, 11), 'navigation': range(1, 11),
                  'engineering': range(11, 23), 'science': range(23, 35)}
        for domain, sections in contract['potential_specialist_sections'].items():
            self.assertTrue(all(s in ranges[domain] for s in sections))
        self.assertIn('authorized_post_or_temporary_commission', contract['assignment_requirements'])
        self.assertIn('rest_and_critical_service_coverage', contract['assignment_requirements'])


if __name__ == '__main__':
    unittest.main()
