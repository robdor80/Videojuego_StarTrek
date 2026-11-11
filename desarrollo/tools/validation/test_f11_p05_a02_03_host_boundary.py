#!/usr/bin/env python3
"""F11-P05-A02-03: non-mutating trust-boundary contract checks.

These checks inspect source and design only. They do NOT authenticate a Host,
issue a live commission, run C++, or certify Unreal.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "sistemas/gameplay/careers/promotions/f11_p05_a02_03_host_boundary_v0.1.json"


def source(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class HostBoundaryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.bridge = source("desarrollo/integration/f04/src/f04_bridge.cpp")
        cls.f04_cmake = source("desarrollo/integration/f04/CMakeLists.txt")
        cls.f05_cmake = source("desarrollo/integration/f05/CMakeLists.txt")
        cls.f11_cmake = source("desarrollo/integration/f11/CMakeLists.txt")
        cls.promotions = source("desarrollo/integration/f11/src/f11_promotions.inc")
        cls.trial = source("desarrollo/integration/f11/src/f11_trial_host.inc")
        cls.schema = source("desarrollo/integration/f11/src/f11_schema.inc")
        cls.api = source("desarrollo/integration/f11/include/f11_promotions.h")

    def test_document_is_explicitly_contract_only(self):
        self.assertEqual(self.c["phase"], "F11-P05-A02-03")
        self.assertEqual(self.c["maturity"], "CONTRACT_ONLY")
        self.assertFalse(self.c["production_host_implemented"])
        self.assertFalse(self.c["production_authority_emission_enabled"])
        self.assertTrue(self.c["static_guard_is_not_runtime_proof"])

    def test_one_authoritative_world_state(self):
        self.assertEqual(self.c["authoritative_store"], "CoreRPG.WorldState via F04Session")
        self.assertIn("sidecar_database_as_career_authority", self.c["forbidden_routes"])

    def test_pins_are_not_reassigned(self):
        self.assertEqual(source("desarrollo/integration/f05/core-revision.txt").strip(), self.c["core_pin"])
        self.assertEqual(source("desarrollo/integration/f04/core-history-revision.txt").strip(),
                         self.c["immutable_history_pin"])

    def test_trial_issuer_is_only_in_guarded_translation_unit(self):
        self.assertIn('#ifdef F11_NATIVE_TEST_HOST\n#include "f11_trial_host.inc"\n#endif', self.bridge)
        self.assertIn('#ifdef F11_ENABLE_PROMOTIONS\n#include "f11_promotions.inc"', self.bridge)
        self.assertNotIn('#include "f11_trial_host.inc"', self.promotions)

    def test_trial_macro_absent_from_product_cmake(self):
        self.assertNotIn("F11_NATIVE_TEST_HOST", self.f04_cmake)
        self.assertNotIn("F11_NATIVE_TEST_HOST", self.f05_cmake)
        self.assertIn("target_compile_definitions(TrekF04Bridge PRIVATE F11_ENABLE_PROMOTIONS=1)", self.f04_cmake)

    def test_trial_macro_is_local_to_trial_target(self):
        self.assertIn("add_library(TrekF11TrialHost SHARED", self.f11_cmake)
        self.assertIn("F11_ENABLE_PROMOTIONS=1 F11_NATIVE_TEST_HOST=1", self.f11_cmake)
        self.assertIn("target_link_libraries(f11_product_tests PRIVATE TrekF04Bridge", self.f11_cmake)

    def test_product_api_has_no_issuer_or_fault_hook(self):
        for symbol in ("f11_test_create", "f11_test_revoke", "f11_test_fault",
                       "f11_bootstrap_authorized_trial", "f11_trial_identity"):
            with self.subTest(symbol=symbol):
                self.assertNotIn(symbol, self.api)
                self.assertNotIn(symbol, self.promotions)
        for symbol in ("f11_commit_promotion", "f11_personnel", "f11_promotion"):
            self.assertIn(symbol, self.api)

    def test_trial_emitter_is_present_but_not_product(self):
        for symbol in ("f11_test_create", "f11_test_revoke", "f11_test_fault"):
            self.assertIn(symbol, self.trial)
        self.assertIn("f11_bootstrap_authorized_trial", self.trial)

    def test_trial_root_is_not_a_product_credential(self):
        self.assertEqual(self.c["historical_trial_root_cause"], 110501)
        self.assertIn("val(w,root,CAUSE)!=110501", self.schema)
        self.assertIn("root_provenance", self.c["trusted_bootstrap"])
        self.assertIn("untrusted_archive_import_without_host_authentication",
                      self.c["forbidden_routes"])

    def test_exact_promotion_pair_is_still_narrow(self):
        self.assertIn("q.from_rank==1101 && q.to_rank==1102", self.promotions)
        self.assertIn("set(*next,q->subject.id,RANK,1102)", self.promotions)
        self.assertNotIn("F04_SCAN", self.promotions)

    def test_live_authority_and_atomic_publish_are_required(self):
        self.assertIn("window(w,q.grant,t)", self.promotions)
        self.assertIn("window(w,q.order,t)", self.promotions)
        self.assertIn("f11_validate(*s->c,*q)", self.promotions)
        self.assertIn("s->c.swap(next)", self.promotions)
        self.assertIn("F11_IDEMPOTENCY_CONFLICT", self.promotions)

    def test_identity_is_not_a_local_f04_ref(self):
        self.assertIn("uint64_t high48,mid48;", self.api)
        self.assertIn("uint32_t low32,reserved;", self.api)
        self.assertIn("f11_equal(f11_identity(w,p),q.character)", self.promotions)

    def test_clients_cannot_self_approve_by_contract(self):
        for forbidden in ("player_or_blueprint_mints_f11_grant",
                          "llm_or_dialogue_commits_rank",
                          "f05_scan_used_as_personnel_order",
                          "legacy_rank_converted_without_commission"):
            self.assertIn(forbidden, self.c["forbidden_routes"])
        self.assertIn("No client-supplied verified flag", self.c["trusted_bootstrap"]["evidence_policy"])

    def test_acceptance_does_not_equate_static_checks_with_runtime(self):
        self.assertEqual(len(self.c["runtime_acceptance_gates"]), 7)
        self.assertIn("HOST_07", self.c["runtime_acceptance_gates"][-1])
        self.assertIn("unreal_ceremony", self.c["out_of_scope"])

    def test_product_host_still_needs_private_commission_flow(self):
        self.assertIn("native product Host", self.c["trusted_bootstrap"]["location"])
        self.assertIn("separate verified graduation", self.c["trusted_bootstrap"]["commissioning"])
        self.assertIn("signed-off", self.c["runtime_acceptance_gates"][2])


if __name__ == "__main__":
    unittest.main()
