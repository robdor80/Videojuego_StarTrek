#!/usr/bin/env python3
"""LORE-02 D mutation tests: every negative probe must be rejected."""
import copy
import unittest
from validate_lore02_d import inputs, validate, validate_data

class Lore02D(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs = inputs()

    def change(self, edit, expected):
        data = copy.deepcopy(self.docs)
        edit(data)
        errors = validate_data(data,check_paths=False)
        self.assertTrue(any(expected in e for e in errors), errors)

    def test_positive_document_gate(self):
        self.assertEqual(validate()["phenomena"],20)
        self.assertEqual(validate()["adversarial"],40)

    def test_forged_knowledge(self):
        self.change(lambda d: d["phenomena"]["records"][0].update(knowledge_state="TRUE_CAUSE_KNOWN"),"hidden truth leak")

    def test_unauthorized_runtime(self):
        self.change(lambda d: d["phenomena"].update(runtime_import_allowed=True),"authority leak")

    def test_unauthorized_ai(self):
        self.change(lambda d: d["methods"].update(authority="AI_AUTONOMOUS"),"authority leak")

    def test_fabricated_measurements(self):
        self.change(lambda d: d["phenomena"]["records"][0].update(numeric_strength=9.2),"fabricated numeric/runtime")

    def test_guaranteed_solution(self):
        self.change(lambda d: d["phenomena"]["records"][0].update(guaranteed_resolution="press_button"),"fabricated numeric/runtime")

    def test_mission_forced(self):
        self.change(lambda d: d["phenomena"]["records"][0].update(encounter_rule="MANDATORY_QUEST"),"forced mission")

    def test_player_dependency(self):
        self.change(lambda d: d["phenomena"]["records"][0].update(presence_rule="ONLY_WHEN_PLAYER_NEAR"),"player dependency")

    def test_hostile(self):
        self.change(lambda d: d["phenomena"]["records"][0].update(default_disposition="HOSTILE"),"forced hostility")

    def test_invented_canon(self):
        self.change(lambda d: d["phenomena"]["records"][0]["provenance"].update(claim_class="SCREEN_CANON"),"inflated screen canon")

    def test_nonexistent_source(self):
        self.change(lambda d: d["disciplines"]["records"][0]["provenance"].update(source_ids=["MA_FAKE"]), "unknown source")

    def test_duplicate_source(self):
        self.change(lambda d: d["registry"]["sources"].append(dict(d["registry"]["sources"][-1])), "duplicate source ID")

    def test_duplicate_id(self):
        self.change(lambda d: d["phenomena"]["records"][1].update(phenomenon_id=d["phenomena"]["records"][0]["phenomenon_id"]),"duplicate/bad ID")

    def test_orphan_discipline(self):
        self.change(lambda d: d["phenomena"]["records"][0].update(discipline_refs=["l02d_missing"]),"orphan discipline")

    def test_orphan_technology(self):
        self.change(lambda d: d["phenomena"]["records"][0].update(technology_refs=["l02a_missing"]),"orphan technology")

    def test_orphan_equipment(self):
        self.change(lambda d: d["phenomena"]["records"][0].update(equipment_refs=["l02b_missing"]),"orphan equipment")

    def test_orphan_phenomenon(self):
        self.change(lambda d: d["cases"]["records"][0].update(phenomenon_ref="l02d_missing"),"orphan phenomenon")

    def test_orphan_role(self):
        self.change(lambda d: d["cases"]["records"][0].update(specialist_refs=["l02d_role_missing"]),"orphan role")

    def test_orphan_method(self):
        self.change(lambda d: d["cases"]["records"][0].update(method_refs=["l02d_missing"]),"orphan method")

    def test_world_truth_in_public_case(self):
        self.change(lambda d: d["cases"]["records"][0].update(world_truth="SECRET_ANSWER"),"hidden truth/offscreen")

    def test_no_competing_hypothesis(self):
        self.change(lambda d: d["cases"]["records"][0].update(hypotheses_es=["certeza"]), "no competing hypothesis")

    def test_disallow_unreviewed_complete(self):
        self.change(lambda d: d["phenomena"].update(status="COMPLETE"), "premature approval")

    def test_facility_spawn(self):
        self.change(lambda d: d["facilities"]["facilities"][0].update(not_auto_spawned=False), "auto facility")

    def test_staff_autogrant(self):
        self.change(lambda d: d["facilities"]["roles"][0].update(no_inherent_command_authority=False), "auto staff/access")

    def test_invalid_scenario(self):
        self.change(lambda d: d["adversarial"]["records"][0].update(expected_guardrail=""), "invalid adversarial scenario")

    def test_clinical_regression(self):
        self.change(lambda d: d["medical"].update(facilities=[]),"LORE-02 C regression")

    def test_equipment_regression(self):
        self.change(lambda d: d["equipment"].update(records=[]),"LORE-02 A/B regressions")

    def test_admin_status(self):
        self.change(lambda d: d.update(status=d["status"].replace("| C — Medicina y xenobiología | ✅ COMPLETE |", "| C — Medicina y xenobiología | 🟨 IN_PROGRESS |")), "C status not regularized")

    def test_era_not_falsely_closed(self):
        self.change(lambda d: d.update(status=d["status"].replace("| D — Ciencia y fenómenos | 🟨 IN_PROGRESS |", "| D — Ciencia y fenómenos | ✅ COMPLETE |")), "D status prematurely closed")

if __name__ == "__main__":
    unittest.main(verbosity=2)
