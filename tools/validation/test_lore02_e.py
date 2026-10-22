#!/usr/bin/env python3
"""LORE-02 E negative mutation probes against a valid documentary baseline."""
from __future__ import annotations

import copy
import unittest
from validate_lore02_e import inputs, validate, validate_data


class Lore02ECrossAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = inputs()

    def mutate(self, edit, expected):
        value = copy.deepcopy(self.data)
        edit(value)
        errors, _ = validate_data(value, check_paths=False)
        self.assertTrue(any(expected in err for err in errors), errors)

    def test_baseline(self):
        self.assertGreaterEqual(validate()["cross_reference_checks"], 350)

    def test_orphan_technology(self):
        self.mutate(lambda d: d["phenomena"]["records"][0].update(
            technology_refs=["l02a_missing"]), "orphan technology_refs")

    def test_orphan_equipment(self):
        self.mutate(lambda d: d["procedures"]["records"][0].update(
            equipment_refs=["l02b_missing"]), "orphan equipment_refs")

    def test_orphan_condition(self):
        self.mutate(lambda d: d["medical_matrix"]["records"][0].update(
            condition_ref="l02c_missing"), "orphan condition_ref")

    def test_orphan_medical_agent(self):
        self.mutate(lambda d: d["medical_matrix"]["records"][0].update(
            possible_agent_links=[{"agent_ref": "l02c_agent_missing"}]),
            "orphan possible_agent_links")

    def test_orphan_scientific_specialist(self):
        self.mutate(lambda d: d["science_cases"]["records"][0].update(
            specialist_refs=["l02d_role_missing"]), "orphan specialist_refs")

    def test_duplicate_tech_id(self):
        self.mutate(lambda d: d["technology"]["records"][1].update(
            technology_id=d["technology"]["records"][0]["technology_id"]),
            "duplicate or empty identifier")

    def test_duplicate_medical_condition(self):
        self.mutate(lambda d: d["conditions"]["catalogue"][1].update(
            condition_id=d["conditions"]["catalogue"][0]["condition_id"]),
            "duplicate or empty identifier")

    def test_source_spoof(self):
        self.mutate(lambda d: d["disciplines"]["records"][0]["provenance"].update(
            source_ids=["FAKE_SOURCE_ID"]), "unregistered provenance")

    def test_species_medical_overreach(self):
        self.mutate(lambda d: d["species"]["records"][0].update(
            species_specific_doses={"default": 1}), "fabricated physiology")

    def test_medical_privacy(self):
        self.mutate(lambda d: d["medical_matrix"]["records"][0].update(
            privacy="PUBLIC"), "medical privacy leak")

    def test_unlicensed_equipment(self):
        self.mutate(lambda d: d["loadouts"]["profiles"][0].update(
            conditional_equipment_ids=["l02b_fake"]), "orphan conditional_equipment_ids")

    def test_science_requires_observations(self):
        self.mutate(lambda d: d["phenomena"]["records"][0].update(
            knowledge_state="TRUE_CAUSE_KNOWN"), "revealed hidden world truth")

    def test_autonomous_science(self):
        self.mutate(lambda d: d["phenomena"]["records"][0].update(
            presence_rule="PLAYER_ONLY"), "player-dependent science")

    def test_protected_authorship(self):
        self.mutate(lambda d: d["legacy_policy"]["scientific_legacy"].update(
            naming_is_not_automatic=False), "missing persistent naming safeguard")

    def test_installation_is_not_global(self):
        self.mutate(lambda d: d["legacy_policy"]["scientific_legacy"].update(
            ship_must_have_commissioned_technology_to_claim_its_function=False),
            "missing persistent naming safeguard")

    def test_shipyard_not_bypassed(self):
        self.mutate(lambda d: d["legacy_policy"]["scientific_research_technology_transfer"].pop(5),
            "instant or incomplete shipyard process")

    def test_omega_mission_is_mandatory(self):
        self.mutate(lambda d: d["legacy_policy"]["exception_rules"]["omega"].update(
            author_mandatory_special_mission=False), "Omega exception weakened")

    def test_time_travel_prohibition(self):
        self.mutate(lambda d: d["legacy_policy"]["exception_rules"].update(
            playable_time_travel_allowed=True), "forbidden time travel")

    def test_wormhole_rarity(self):
        self.mutate(lambda d: d["legacy_policy"]["exception_rules"]["wormholes"].update(
            rarity="COMMON"), "unrestricted wormholes")

    def test_no_premature_lore02e_closure(self):
        self.mutate(lambda d: d.update(status=d["status"].replace(
            "| E — Integración y auditoría A–D | 🟨 IN_PROGRESS |",
            "| E — Integración y auditoría A–D | ✅ COMPLETE |")),
            "E wrongly closed before author approval")

    def test_core_only_world_state(self):
        self.mutate(lambda d: d["legacy_policy"].update(authority="AI"),
            "fake imported CoreRPG content")

    def test_original_catalogue_still_present(self):
        self.mutate(lambda d: d["legacy_technology"].update(records=[]),
            "catalogue count regression")


if __name__ == "__main__":
    unittest.main(verbosity=2)
