"""Unit safety and acceptance checks for the F05 *reference*, not the actual Core."""
import json
import unittest
from pathlib import Path

from f05_reference import VERDICTS, assess, verify_fixture

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


if __name__ == "__main__":
    unittest.main()
