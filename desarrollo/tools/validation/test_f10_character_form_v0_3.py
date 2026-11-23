#!/usr/bin/env python3
"""F10/H06: formulario v0.3 — contrato, no evaluacion psicologica clinica ni autoridad Core."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
CREATION = ROOT / "sistemas/gameplay/character_creation"
SCHEMA = CREATION / "f10_formulario_inicial_v0.3.json"
HTML = ROOT / "audiovisual/ui/academy/formulario_cadete_v0.3.html"
AGES = CREATION / "f10_species_maturity_policy_v0.1.json"


class F10FormV03Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.html = HTML.read_text(encoding="utf-8")
        cls.ages = json.loads(AGES.read_text(encoding="utf-8"))

    def test_three_species_and_approved_age_floor(self):
        expected = {"human":18, "vulcan":25, "human_vulcan_hybrid":22}
        self.assertEqual({x["id"]:x["minimum_age"] for x in self.s["species"]}, expected)
        authoritative = {x["species_id"]:x["minimum_playable_age_earth_years"]
                         for x in self.ages["species"]}
        self.assertEqual({k:authoritative[k] for k in expected}, expected)
        for x in self.s["species"]:
            self.assertIn(x["id"],self.html)

    def test_career_goal_is_aspiration_not_professional_authority(self):
        fields = {x["id"]:x for x in self.s["common_fields"]}
        self.assertTrue(fields["career_goal"]["required"])
        self.assertEqual(fields["career_goal_other"]["required_if"],
                         {"field":"career_goal","equals":"other"})
        labels = {x[0]:x[1] for x in fields["career_goal"]["options"]}
        for option in ("starship_captain", "first_officer", "chief_engineer",
                       "chief_science", "chief_medical", "chief_security", "undecided"):
            self.assertIn(option, labels)
        self.assertIn('id="career_goal"',self.html)
        self.assertIn('id="career_goal_other"',self.html)
        self.assertIn("aspiración, no nombramiento",self.html)

    def test_personality_self_report_not_diagnosis(self):
        fields = {x["id"]:x for x in self.s["personality_fields"]}
        self.assertEqual(set(self.s["validation"]["personality_fields_required"]),
                         {"personality_description","values","teamwork_style","stress_style"})
        self.assertTrue(all(fields[x]["required"]
                            for x in self.s["validation"]["personality_fields_required"]))
        self.assertEqual(fields["strengths"]["max_selected"],3)
        self.assertEqual(self.s["psychological_assessment"]["assessment_status"],"NO_REALIZADA")
        self.assertFalse(self.s["psychological_assessment"]["no_automatic_fitness_decision"] is False)
        self.assertTrue(self.s["psychological_assessment"]["no_diagnosis"])
        self.assertFalse(self.s["validation"]["gameplay_effects_automatic"])
        for label in ("personality_description","values","teamwork_style",
                      "stress_style","leadership_style","ethical_dilemma"):
            self.assertIn('id="'+label+'"',self.html)
        self.assertIn("SELF_REPORTED_BY_PLAYER_NOT_STARFLEET",self.html)
        self.assertIn("evaluacion_psicologica_institucional",self.html)

    def test_model_3d_removed_and_physical_description_kept(self):
        self.assertNotIn("visual_model",self.s)
        self.assertFalse(self.s["presentation"]["model_3d_field_present"])
        self.assertNotIn('id="model-3d"',self.html)
        self.assertNotIn("modelo_3d_ref",self.html)
        self.assertIn('id="physical_appearance"',self.html)

    def test_safe_f10_boundary_and_old_drafts(self):
        self.assertTrue(self.s["validation"]["client_cannot_create_person"])
        self.assertFalse(self.s["validation"]["precheck_may_return_valid"])
        self.assertTrue(self.s["validation"]["semantic_review_required"])
        self.assertEqual(self.s["import_compatibility"]["missing_personality_on_legacy_import"],
                         "PROMPT_USER_TO_COMPLETE")
        self.assertIn('id="import_json"',self.html)
        self.assertIn("prior_experience:experiences",self.html)
        self.assertIn("BORRADOR_PENDIENTE_VALIDACION_F10_Y_REVISION_IA",self.html)
        self.assertNotIn("fetch(",self.html)
        self.assertNotIn("OPENAI_API_KEY",self.html)


if __name__ == "__main__":
    unittest.main()
