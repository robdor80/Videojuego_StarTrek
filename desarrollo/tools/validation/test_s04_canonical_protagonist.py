"""Documentary regression suite: S04 canonical player, 17 Nov 2026.

Checks consistency of versioned design. No CoreRPG/HOST/UE5 execution.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CC = "sistemas/gameplay/character_creation/"
LORE = "mundo/lore/characters/starfleet/"


def data(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def doc(path):
    return (ROOT / path).read_text(encoding="utf-8")


class S04ProtagonistContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = data(CC + "s04_fixed_protagonist_contract_v2.json")
        cls.b = data(CC + "s04_protagonist_biography_v1.json")
        cls.status = data(CC + "s04_initial_persona_status_v2.json")

    def test_single_fixed_male_hybrid(self):
        s = self.c["selection"]
        self.assertEqual(self.c["contract_id"], "s04_fixed_player_protagonist")
        self.assertEqual(s["mode"], "SINGLE_FIXED_CANONICAL_PROTAGONIST")
        self.assertEqual(s["allowed_species_ids"], ["human_vulcan_hybrid"])
        self.assertFalse(s["allow_species_selection"])
        self.assertFalse(s["allow_sex_selection"])
        self.assertFalse(s["allow_free_biography_input"])
        self.assertEqual(s["sex"], "male")

    def test_chronology_and_parents(self):
        c = self.c
        self.assertEqual(c["campaign"]["start_year"], 2383)
        self.assertEqual(c["selection"]["age_at_academy_entry_years"], 45)
        self.assertEqual(c["selection"]["approximate_birth_year"], 2338)
        self.assertEqual(c["selection"]["apparent_human_age_approx"], 30)
        self.assertEqual(c["parentage"]["mother_species"], "vulcan")
        self.assertEqual(c["parentage"]["father_species"], "human")
        self.assertEqual(c["parentage"]["father_direct_descendant_of"], "khan_noonien_singh")
        self.assertEqual(self.b["identity"]["age_at_admission_earth_years"], 45)
        self.assertEqual(self.b["identity"]["birth_year_approx"], 2338)

    def test_unsettled_details_are_not_fabricated(self):
        b = self.b
        self.assertIsNone(b["identity"]["birth_exact_date"])
        self.assertIsNone(b["identity"]["parents_names"])
        self.assertIsNone(b["identity"]["place_of_birth"])
        self.assertIsNone(b["formation"]["university_degrees"])
        self.assertIsNone(b["formation"]["music_instruments"])

    def test_lifespan_and_real_combat_training(self):
        c = self.c
        self.assertEqual(c["biology"]["working_lifespan_range_years"], [150, 200])
        self.assertTrue(c["biology"]["exceptional_inherited_augment_expression"])
        self.assertFalse(c["biology"]["invincible"])
        self.assertCountEqual(c["training"]["martial_mastery"],
                              ["kung_fu", "karate", "aikido", "suus_mahna"])
        self.assertTrue(c["training"]["skill_values_from_core_validated_evidence_not_manual_points"])

    def test_scientist_is_not_auto_security(self):
        self.assertEqual(self.c["education"]["primary_vocation"], "science")
        self.assertFalse(self.c["education"]["security_department_auto_assignment"])
        self.assertFalse(self.c["education"]["previous_starfleet_service"])

    def test_editable_fields_are_cosmetic_plus_name(self):
        custom = self.c["customization"]
        self.assertIn("display_name", custom["editable_fields"])
        self.assertIn("hair_style", custom["editable_fields"])
        self.assertIn("facial_hair", custom["editable_fields"])
        self.assertIn("sex", custom["immutable_fields"])
        self.assertIn("species_id", custom["immutable_fields"])
        self.assertIn("khan_lineage", custom["immutable_fields"])
        self.assertTrue(custom["cosmetics_do_not_mutate_core_capabilities"])

    def test_intro_and_legendary_chronology(self):
        i = self.c["intro"]
        self.assertEqual(i["life_stage_count"], 5)
        self.assertTrue(i["janeway_first_defense"])
        self.assertTrue(i["picard_final_speech"])
        self.assertFalse(i["sisko_2383_participant"])
        self.assertTrue(i["skip_and_rewatch_without_replaying_admission"])
        sisko = doc(LORE + "benjamin_sisko_lore05b_v0.1.md")
        self.assertIn("2388", sisko)
        self.assertIn("2392", sisko)

    def test_recorded_relationships_without_auto_romance(self):
        p = doc(LORE + "jean_luc_picard_lore05b_v0.1.md")
        j = doc(LORE + "kathryn_janeway_lore05b_v0.1.md")
        seven = doc(LORE + "seven_of_nine_lore05b_v0.1.md")
        self.assertIn("DEC-0022", p)
        self.assertIn("DEC-0022", j)
        self.assertIn("DEC-0022", seven)
        self.assertTrue(self.c["relationships"]["future_relationships_event_driven"])
        self.assertEqual(self.c["relationships"]["seven_initial_state"],
                         "NO_FORCED_AFFINITY_OR_EARLY_ENCOUNTER")

    def test_admission_is_not_an_admiral_reward(self):
        a = self.c["admission"]
        self.assertTrue(a["declares_khan_lineage"])
        self.assertEqual(a["supported_by"], ["jean_luc_picard", "kathryn_janeway"])
        self.assertTrue(a["institutional_decision_only_by_authorized_F10"])
        self.assertTrue(a["not_rank_or_clearance"])

    def test_old_product_contracts_kept_and_superseded_in_design(self):
        self.assertTrue((ROOT / CC / "f10_initial_player_rules_v0.1.json").is_file())
        self.assertTrue((ROOT / CC / "character_creation_contract_v1_0.json").is_file())
        self.assertEqual(self.c["legacy"]["previous_open_species_selection"],
                         "SUPERSEDED_FOR_NEW_PLAYER_GAME")
        self.assertTrue(self.c["legacy"]["locked_contracts_retained"])
        self.assertTrue(self.c["legacy"]["code_migration_required"])

    def test_cinematic_plan_is_not_finished_media(self):
        intro = doc(CC + "S04_INTRO_CINEMATICA_PLAN_v1.md")
        for v in ("Nacimiento", "adolescencia", "Janeway", "Picard", "Locutus"):
            self.assertIn(v.lower(), intro.lower())
        self.assertTrue(self.c["intro"]["voice_and_music_production_not_started"])
        self.assertFalse(self.status["intro_media_created"])

    def test_runtime_not_implemented(self):
        self.assertFalse(self.c["runtime_implemented"])
        self.assertFalse(self.status["authoritative_protagonist_creation_runtime_implemented"])
        self.assertFalse(self.status["host_F10_integration_done"])
        self.assertFalse(self.status["core_rpg_capabilities_mapped"])
        self.assertFalse(self.status["real_runtime_tests_passed"])


if __name__ == "__main__":
    unittest.main()
