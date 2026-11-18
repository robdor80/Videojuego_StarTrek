"""S18 author-approved number / proposed policy: DOCUMENTARY consistency only.

Not a security implementation, CoreRPG evaluator, UE5 door test or biometric test.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "sistemas/gameplay/access_control"


def doc(file):
    return (D / file).read_text(encoding="utf-8")


def load(file):
    return json.loads(doc(file))


class S18AccessControlContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.identity = load("s18_identity_assertion_contract_v0.1.json")
        cls.policy = load("s18_door_and_room_policy_v0.1.json")
        cls.decision = load("s18_access_decision_contract_v0.1.json")
        cls.cases = load("s18_acceptance_cases_v0.1.json")
        cls.state = load("s18_status_v0.1.json")

    def test_number_and_status(self):
        self.assertEqual(self.state["system_id"], "S18_IDENTITY_AUTH_ACCESS")
        self.assertEqual(self.state["number"], 18)
        self.assertTrue(self.state["author_approved_number_and_scope"])
        self.assertEqual(self.state["detailed_policy_status"],
                         "PROPOSED_FOR_TECHNICAL_IMPLEMENTATION")

    def test_no_false_claim_of_runtime(self):
        for key in ("authenticated_shared_policy_runtime_implemented",
                    "UE5_access_panel_blueprints_integrated",
                    "Sutherland_door_artifact_audited",
                    "npc_identity_press_runtime_validated",
                    "grants_and_revocations_runtime_implemented",
                    "full_gameplay_tests_passed"):
            self.assertFalse(self.state[key], key)
        self.assertFalse(self.decision["runtime_implemented"])

    def test_uses_persistent_core_character_ids(self):
        self.assertEqual(self.identity["truth_owner"], "CoreRPG")
        self.assertEqual(self.identity["transport_owner"], "HOST")
        ref = self.identity["source_identity_ref"]
        self.assertTrue((ROOT / ref).is_file())
        self.assertIn("PLAYER_PERSON", self.identity["subjects"])
        self.assertIn("NPC_PERSON", self.identity["subjects"])

    def test_source_contracts_still_exist(self):
        for ref in ("sistemas/gameplay/ship_operations/ship_computer/access_control_rules.json",
                    "sistemas/gameplay/ship_operations/interior_location_model.json",
                    "sistemas/gameplay/characters/character_runtime_model.json",
                    "sistemas/gameplay/ship_operations/interior_navigation_graph_v0.1.schema.json"):
            self.assertTrue((ROOT / ref).is_file(), ref)

    def test_no_identity_spoof_from_client_or_voice(self):
        rules = self.identity["binding_rules"]
        for key in ("untrusted_client_actor_id_is_never_proof",
                    "untrusted_natural_language_identity_claim_never_proof",
                    "proximity_is_not_proof",
                    "uniform_or_rank_appearance_is_not_proof",
                    "identity_must_resolve_via_authoritative_actor_binding",
                    "player_and_NPC_use_same_principal_verification",
                    "missing_or_conflicting_identity_fails_closed"):
            self.assertTrue(rules[key], key)

    def test_no_real_person_biometrics(self):
        self.assertTrue(self.identity["binding_rules"]
                        ["biometrics_are_fictional_game_state_only_no_real_user_data"])

    def test_three_door_families(self):
        cats = self.policy["policy_categories"]
        self.assertEqual([x["key"] for x in cats],
                         ["PUBLIC_AUTO", "PRIVATE_BUTTON", "RESTRICTED"])
        self.assertEqual(cats[0]["trigger"], "PROXIMITY")
        self.assertEqual(cats[1]["trigger"], "PANEL_PRESS")
        self.assertTrue(all(x["s12_responsible_for_actuation"] for x in cats))

    def test_private_resident_and_invited_only(self):
        categories = self.policy["policy_categories"]
        self.assertEqual(categories[1]["default_access"],
                         "CHECK_RESIDENT_OR_GUEST_OR_VALID_TASK")
        self.assertEqual(categories[1]["unknown_behavior"],
                         "RING_OR_REJECT_NO_REVEAL")
        self.assertIn("authoritative_residency_assignment",
                      self.policy["authorization_sources"])
        self.assertIn("explicit_guest_grant",
                      self.policy["authorization_sources"])

    def test_grants_must_be_scoped_and_revocable(self):
        fields = set(self.policy["grant_fields"])
        for field in ("grantee_principal_id", "resource_scope",
                      "valid_from", "expires_at", "revoked_at",
                      "grant_event_ref", "policy_revision"):
            self.assertIn(field, fields)
        self.assertTrue(self.policy["rules"]["expired_grant_invalid"])
        self.assertTrue(self.policy["rules"]["revocation_immediate_next_check"])

    def test_captain_not_universal_override(self):
        self.assertTrue(self.policy["rules"]["rank_alone_never_universal_key"])

    def test_emergency_and_egress_separate(self):
        rules = self.policy["rules"]
        self.assertTrue(rules["egress_safety_separate_from_entry"])
        self.assertTrue(rules["quarantine_and_decompression_have_explicit_emergency_owner"])
        self.assertTrue(rules["emergency_override_incident_evidence_required"])
        self.assertTrue(self.decision["security"]["explicit_emergency_incident_and_authority"])

    def test_ai_cannot_open_or_authorize(self):
        s = self.decision["separation"]
        self.assertTrue(s["ALLOW_does_not_open_door"])
        self.assertTrue(s["voice_only_proposes_intention"])
        self.assertTrue(s["AI_never_authorizes"])

    def test_physical_block_is_not_denial(self):
        results = self.decision["physical_after_auth_results"]
        self.assertIn("PHYSICALLY_BLOCKED", results)
        self.assertIn("POWER_UNAVAILABLE", results)
        self.assertTrue(self.policy["rules"]["physical_openability_checked_separately_by_S12"])

    def test_error_default_fails_closed_and_no_privacy_leak(self):
        s = self.decision["security"]
        self.assertTrue(s["default_deny_if_essential_data_missing"])
        self.assertTrue(s["never_leak_resident_presence_on_denial"])
        self.assertTrue(s["private_audit_access_controlled"])

    def test_idempotence_and_cache_revalidation(self):
        s = self.decision["security"]
        self.assertTrue(s["request_idempotent"])
        self.assertTrue(s["revalidate_issued_grant_against_authoritative_clock_and_revision"])
        self.assertTrue(s["do_not_ever_cache_stale_privileges"])

    def test_twenty_four_scenarios_are_proposals(self):
        cases = self.cases["cases"]
        ids = [c["id"] for c in cases]
        self.assertEqual(len(ids), 24)
        self.assertEqual(len(set(ids)), 24)
        self.assertTrue(all(c["runtime_state"] == "NOT_RUN" for c in cases))
        self.assertEqual(self.cases["runtime_pass_count"], 0)

    def test_registered_in_decisions_index(self):
        index = (ROOT / "proyecto/docs/decisions/README.md").read_text(encoding="utf-8")
        self.assertIn("DEC-0024", index)
        self.assertIn("Sistema 18", index)
        decision = (ROOT / "proyecto/docs/decisions/s18_identidad_autenticacion_control_accesos_2026-11-18.md").read_text(encoding="utf-8")
        self.assertIn("Sistema 18", decision)
        self.assertIn("S12", decision)

    def test_separate_system12_and_f12(self):
        self.assertTrue(self.state["prerequisite_for_S12_private_restricted_doors"])
        f12 = (ROOT / "proyecto/docs/roadmap/master/fases/F12/README.md").read_text(encoding="utf-8")
        self.assertIn("Vida a bordo", f12)
        self.assertIn("Sistema 12", doc("S18_IDENTIDAD_CONTROL_ACCESOS_DISENO_v1.md"))


if __name__ == "__main__":
    unittest.main()
