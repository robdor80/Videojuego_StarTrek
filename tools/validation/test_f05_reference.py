"""Unit safety and acceptance checks for the F05 *reference*, not the actual Core."""
import json
import unittest
from pathlib import Path

from f05_reference import VERDICTS, assess as assess_raw, verify_fixture


def assess(case: dict) -> dict:
    """Fuente de evidencias explícita para los tests; no es un adaptador confiable."""
    base = dict(phase="issue", channel="actor", authority_verdict="allow",
                knowledge_visible=True, appointment_active=True, medical_fit=True,
                actor_id="test:captain", action_id="bridge_order",
                station_id="test:bridge", state_revision=3, current_tick=100,
                duty_active=True, executor_qualified=True, executor_authorized=True,
                capability_available=True, resources_available=True, temporal_conflict=False)
    base.update(case)
    if base.get("channel") == "actor" and base.get("authority_verdict") == "allow":
        base.setdefault("authorization_binding", dict(
            source="F04_REFERENCE", decision="ALLOW", actor_id=base["actor_id"],
            action_id=base["action_id"], station_id=base["station_id"],
            state_revision=base["state_revision"], issued_tick=90, expires_tick=110))
    return assess_raw(base)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "validation/fixtures/f05/order_initiative_reference_v0.1.json"


class TestF05Reference(unittest.TestCase):
    def test_fixture(self):
        count, errors = verify_fixture(FIXTURE)
        self.assertGreaterEqual(count, 30)
        self.assertEqual(errors, [])

    def test_coverage_routes(self):
        cases = json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"]
        routes = {x["route"] for x in cases}
        self.assertTrue({"npc_to_npc", "npc_to_player", "player_captain_to_npc"} <= routes)

    def test_no_world_mutation_ever(self):
        for inp in ({"phase": "execute"}, {"phase": "issue"},
                    {"channel": "ai"}, {"channel": "actor", "direct_world_mutation": True}):
            out = assess(inp)
            self.assertFalse(out["authoritative"])
            self.assertFalse(out["core_integrated"])
            self.assertEqual(out["effects_applied"], 0)

    def test_ai_is_only_proposal(self):
        out = assess({"channel": "ai", "phase": "ai_response"})
        self.assertEqual(out["verdict"], "PROPOSAL_ONLY")

    def test_revoke_blocks_reexecution(self):
        out = assess({"phase": "execute", "delegation_required": True,
                      "delegation_status": "revoked"})
        self.assertEqual((out["verdict"], out["reason"]), ("REFUSE", "delegation_inactive"))

    def test_no_captain_autoapproval(self):
        out = assess({"control_mode": "proposal_requires_approval", "issuer_role": "xo",
                      "policy_change": True})
        self.assertEqual(out["verdict"], "WAIT_APPROVAL")

    def test_captain_can_decide_lawful_policy(self):
        out = assess({"control_mode": "manual", "issuer_role": "captain",
                      "policy_change": True})
        self.assertEqual(out["verdict"], "ALLOW_REFERENCE")

    def test_revalidation_blocks_late_proposal(self):
        out = assess({"channel": "ai", "phase": "ai_response", "context_stale": True})
        self.assertEqual(out["verdict"], "REJECT_STALE")

    def test_no_ranking_grants_command(self):
        out = assess({"phase": "issue", "issuer_rank": "admiral",
                      "authority_verdict": "deny"})
        self.assertEqual(out["reason"], "authority_denied")

    def test_offscreen_does_not_disable_logic(self):
        a = assess({"phase": "execute", "actor_3d_loaded": True})
        b = assess({"phase": "execute", "actor_3d_loaded": False})
        self.assertEqual(a, b)

    def test_idempotent_replay(self):
        a = assess({"phase": "execute", "idempotency": "same"})
        b = assess({"phase": "execute", "idempotency": "conflict"})
        self.assertEqual(a["verdict"], "REPLAY")
        self.assertEqual(b["reason"], "idempotency_conflict")

    def test_first_directive_not_universal_hard_block(self):
        out = assess({"regulatory_review": True})
        self.assertEqual(out["verdict"], "REVIEW")

    def test_provider_timeout_has_safe_outcome(self):
        out = assess({"channel": "ai", "provider_status": "timeout",
                      "fallback_authorized": True})
        self.assertEqual(out["verdict"], "FALLBACK")
        self.assertEqual(out["effects_applied"], 0)

    def test_invalid_enums_and_unknown_phase(self):
        self.assertEqual(assess({"phase": "teleport"} )["reason"], "invalid_payload")
        self.assertEqual(assess({"authority_verdict": "GOD"})["reason"], "invalid_payload")

    def test_contract_reference_exists_and_is_proposed(self):
        p = ROOT / "docs/roadmap/master/fases/F05/CONTRATOS_P01_P02.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        self.assertFalse(d["is_core_api"])
        self.assertIn("revoked", d["delegation_statuses"])
        self.assertIn("executing", d["transitions"]["queued"])

    def test_legacy_canonical_sources_unmodified(self):
        p = ROOT / "gameplay/orders/starship_order_contract.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(d["state_mutation_authority"], "core_rules")
        self.assertFalse(d["ai_direct_state_mutation"])
        self.assertIn("completed", d["outcome_states"])


    def test_missing_authority_is_never_allowed(self):
        for item in ({}, {"phase": "issue", "channel": "actor"},
                     {"phase": "issue", "channel": "actor", "authority_verdict": "allow"}):
            self.assertNotEqual(assess_raw(item)["verdict"], "ALLOW_REFERENCE")

    def test_binding_actor_station_revision_and_expiry(self):
        base = dict(phase="execute", channel="actor", authority_verdict="allow",
                    knowledge_visible=True, appointment_active=True, medical_fit=True,
                    actor_id="captain:1", action_id="sensor_scan", station_id="sensor:1",
                    state_revision=7, current_tick=100, duty_active=True,
                    executor_qualified=True, executor_authorized=True,
                    capability_available=True, resources_available=True,
                    temporal_conflict=False)
        binding = dict(source="F04_REFERENCE", decision="ALLOW", actor_id="captain:1",
                       action_id="sensor_scan", station_id="sensor:1",
                       state_revision=7, issued_tick=90, expires_tick=105)
        self.assertEqual(assess_raw({**base, "authorization_binding": binding})["verdict"],
                         "ALLOW_REFERENCE")
        for mutation in ({"actor_id": "captain:other"}, {"station_id": "sensor:2"},
                         {"state_revision": 8}, {"action_id": "torpedo_fire"}):
            bad = {**base, **mutation, "authorization_binding": binding}
            self.assertEqual(assess_raw(bad)["reason"], "authority_binding_invalid")
        self.assertEqual(assess_raw({**base, "current_tick": 105,
                                    "authorization_binding": binding})["verdict"],
                         "REJECT_STALE")
        self.assertEqual(assess_raw({**base, "authority_verdict": "deny",
                                    "authorization_binding": binding})["verdict"],
                         "REFUSE")

    def test_explicit_execution_evidence_required(self):
        good = dict(phase="execute", channel="actor", authority_verdict="allow",
                    knowledge_visible=True, appointment_active=True, medical_fit=True,
                    actor_id="captain:1", action_id="sensor_scan", station_id="sensor:1",
                    state_revision=7, current_tick=100, duty_active=True,
                    executor_qualified=True, executor_authorized=True,
                    capability_available=True, resources_available=True,
                    temporal_conflict=False,
                    authorization_binding=dict(source="F04_REFERENCE", decision="ALLOW",
                        actor_id="captain:1", action_id="sensor_scan",
                        station_id="sensor:1", state_revision=7, issued_tick=90,
                        expires_tick=105))
        for field in ("knowledge_visible", "appointment_active", "medical_fit",
                      "resources_available", "executor_qualified", "duty_active",
                      "temporal_conflict"):
            invalid = good.copy()
            invalid.pop(field)
            self.assertNotEqual(assess_raw(invalid)["verdict"], "ALLOW_REFERENCE")


if __name__ == "__main__":
    unittest.main()
