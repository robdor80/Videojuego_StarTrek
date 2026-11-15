#!/usr/bin/env python3
"""F10/H06 — contrato del formulario básico; pruebas de referencia SIN CoreRPG/IA."""
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "sistemas/gameplay/character_creation"
SCHEMA = BASE / "f10_formulario_inicial_v0.1.json"
POLICY = BASE / "f10_species_maturity_policy_v0.1.json"
CREATION = BASE / "character_creation_contract_v1_0.json"
HTML = ROOT / "audiovisual/ui/academy/formulario_cadete_v0.1.html"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class F10CharacterFormV01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = read_json(SCHEMA)
        cls.policy = read_json(POLICY)
        cls.creation = read_json(CREATION)
        cls.html = HTML.read_text(encoding="utf-8")

    def test_three_species_and_author_approved_ages(self):
        by_id = {s["id"]: s for s in self.schema["species"]}
        self.assertEqual(set(by_id), {"human", "vulcan", "human_vulcan_hybrid"})
        self.assertEqual({x: s["minimum_age"] for x, s in by_id.items()},
                         {"human": 18, "vulcan": 25, "human_vulcan_hybrid": 22})
        authoritative = {s["species_id"]: s for s in self.policy["species"]}
        for sid, spec in by_id.items():
            self.assertEqual(spec["minimum_age"], authoritative[sid]["minimum_playable_age_earth_years"])
            self.assertEqual(authoritative[sid]["content_scope"], "MAIN_GAME")
            self.assertTrue((ROOT / self.schema["source_of_truth"][
                {"human": "human", "vulcan": "vulcan", "human_vulcan_hybrid": "hybrid"}[sid]]).is_file())
        self.assertIsNone(self.schema["validation"]["age_maximum"])

    def test_exact_embedded_single_source(self):
        match = re.search(r'<script id="formulario-definicion" type="application/json">(.*?)</script>',
                          self.html, re.DOTALL)
        self.assertIsNotNone(match, "El prototipo debe poder abrirse como file:// sin fetch")
        embedded = json.loads(match.group(1))
        self.assertEqual(embedded, self.schema)

    def test_common_field_ids_unique_and_required_f10_coverage(self):
        ids = [v["id"] for v in self.schema["common_fields"]]
        self.assertEqual(len(ids), len(set(ids)))
        for required in ("nickname", "character_name", "species_id", "age", "birth_place",
                         "upbringing_place", "citizenship", "physical_appearance", "education",
                         "objective", "motivation", "biography"):
            self.assertIn(required, ids)
            self.assertTrue(next(f for f in self.schema["common_fields"]
                                 if f["id"] == required)["required"], required)
        expected = set(self.creation["required_character_fields"])
        exported = {"display_name", "species_id", "age_or_birth_date", "adult_equivalent_status",
                    "origin", "citizenship_context", "culture_context", "appearance_profile",
                    "prior_education", "prior_activities_and_hobbies", "prior_experience",
                    "initial_long_term_objective"}
        self.assertEqual(exported, expected)
        self.assertIn("f10_draft", self.html)
        self.assertIn("perfil_jugador_no_autoritativo", self.html)
        self.assertNotIn("person_created", self.schema)

    def test_conditional_upbringing_and_rituals(self):
        upbringing = self.schema["upbringing_by_species"]
        self.assertEqual({x[0] for x in upbringing["human_vulcan_hybrid"]},
                         {"vulcan", "earth", "mixed", "other"})
        self.assertEqual(len(self.schema["special_fields"]), 7)
        for field in self.schema["special_fields"]:
            self.assertNotIn("human", field["species"])
            self.assertEqual(set(field["species"]), {"vulcan", "human_vulcan_hybrid"})
        self.assertIn("kolinahr", {f["id"] for f in self.schema["special_fields"]})
        self.assertTrue(self.schema["validation"]["kolinahr_completed_requires_context_in_form"])

    def test_activities_match_existing_contract(self):
        activities = read_json(BASE / "prior_activity_model.json")
        self.assertEqual({x[0] for x in self.schema["activity"]["categories"]},
                         set(activities["categories"]))
        self.assertEqual(self.schema["activity"]["minimum"], 1)
        self.assertGreaterEqual(self.schema["activity"]["maximum"], 2)
        self.assertIn("ended_at_or_current", self.html)
        self.assertIn("started_at_or_age", self.html)

    def test_visual_model_is_separate_and_offline(self):
        model = self.schema["visual_model"]
        self.assertEqual(model["selection_mode"], "DISABLED_UNTIL_VERIFIED_CATALOG")
        self.assertIn('id="model-3d" type="text" disabled', self.html)
        self.assertIn("modelo_3d_ref:null", self.html)
        self.assertNotIn('type="file"', self.html)
        self.assertNotIn("fetch(", self.html)
        self.assertNotIn("XMLHttpRequest", self.html)
        self.assertNotIn("localStorage", self.html)
        self.assertNotIn("OPENAI_API_KEY", self.html)

    def test_never_claims_authoritative_validation(self):
        rules = self.schema["validation"]
        self.assertTrue(rules["semantic_review_required"])
        self.assertFalse(rules["precheck_may_return_valid"])
        self.assertTrue(rules["client_cannot_create_person"])
        self.assertTrue(rules["no_extra_adult_proof"])
        self.assertIn("BORRADOR_PENDIENTE_VALIDACION_F10_Y_REVISION_IA", self.html)
        self.assertIn("NO se han ejecutado", self.html)
        self.assertIn("f10_draft", self.html)


if __name__ == "__main__":
    unittest.main()
