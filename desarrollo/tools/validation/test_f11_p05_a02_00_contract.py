#!/usr/bin/env python3
"""A02-00: comprobaciones del CONTRATO, NO pruebas C++/Core ni ascensos reales."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "sistemas/gameplay/careers/promotions/f11_p05_a02_00_personnel_contract_v0.1.json"
RANKS = ROOT / "mundo/lore/federation/starfleet/ranks/officer_ranks.json"
PIPS = ROOT / "mundo/lore/federation/starfleet/ranks/rank_insignia_standard.json"
P01 = ROOT / "sistemas/gameplay/chain_of_command/f11_p01_personnel_authority_contract_v0.1.json"
P03 = ROOT / "sistemas/gameplay/careers/promotions/f11_p03_progression_policy_v0.1.json"
SERVICE = ROOT / "sistemas/gameplay/careers/service_record/service_record_model.json"
GRAD = ROOT / "sistemas/gameplay/careers/academy_path/graduation_model.json"
F04_HEADER = ROOT / "desarrollo/integration/f04/include/f04_bridge.h"
F04_IMPL = ROOT / "desarrollo/integration/f04/src/f04_bridge.cpp"
F05_IMPL = ROOT / "desarrollo/integration/f05/src/f05_orders.inc"
F05_PIN = ROOT / "desarrollo/integration/f05/core-revision.txt"


def data(p):
    return json.loads(p.read_text(encoding="utf-8"))


class ContractF11P05A0200(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = data(CONTRACT)
        cls.ranks = cls.spec["ranks"]["rank_table"]
        cls.ids = [row["rank_id"] for row in cls.ranks]
        cls.codes = [row["f11_rank_code"] for row in cls.ranks]

    def test_01_maturity_only_contract(self):
        self.assertEqual(self.spec["maturity"], "CONTRACT_AND_OFFLINE_VALIDATION_ONLY_NO_CXX_RUNTIME")
        self.assertEqual(self.spec["validation_status"]["Core_world_mutation"], "NOT_STARTED")
        self.assertEqual(self.spec["validation_status"]["UE5_playable"], "NOT_STARTED")

    def test_02_single_core_world_system_of_record(self):
        self.assertEqual(self.spec["runtime_system_of_record"], "CoreRPG_WorldState_through_existing_F04Session")
        self.assertTrue(self.spec["general_guards"]["no_parallel_personnel_database"])

    def test_03_offline_python_never_authoritative(self):
        self.assertTrue(self.spec["general_guards"]["no_python_runtime_authority"])
        self.assertTrue(self.spec["general_guards"]["no_llm_or_blueprint_permission_grant"])

    def test_04_six_rank_ids_match_canon_design(self):
        canon = [r["id"] for r in data(RANKS)["normal_progression"]][:6]
        self.assertEqual(self.ids, canon)

    def test_05_rank_ids_match_p01_authority(self):
        self.assertEqual(self.ids, data(P01)["rank_progression"])

    def test_06_rank_pair_edges_match_p03(self):
        pairs = [(s["from_rank"], s["to_rank"]) for s in data(P03)["commissioned_rank_steps"]]
        self.assertEqual(pairs, [(a["rank_id"], a["next_rank_id"])
                                 for a in self.ranks if a["next_rank_id"] is not None])

    def test_07_display_pips_agree_with_approved_catalogue(self):
        canon = {x["rank_id"]: x["display"] for x in data(PIPS)["commissioned"]}
        self.assertEqual({x["rank_id"]: x["pips"] for x in self.ranks}, canon)

    def test_08_commissioned_rank_codes_are_unique(self):
        self.assertEqual(len(self.codes), len(set(self.codes)))
        self.assertTrue(all(type(x) is int for x in self.codes))

    def test_09_codes_never_reuse_observed_legacy_values(self):
        self.assertFalse(set(self.codes) & set(self.spec["ranks"]["source_scalars_reserved_for_legacy"]))
        self.assertEqual(self.spec["compatibility"]["f04_legacy_rank_values_in_synthetic_source"], [0, 1, 8, 10])

    def test_10_numeric_mapping_is_versioned(self):
        self.assertEqual(self.spec["ranks"]["numeric_namespace"], "F11_COMMISSIONED_V1")
        self.assertEqual(self.codes, [1101, 1102, 1103, 1104, 1105, 1106])

    def test_11_canonical_ladder_not_copied_into_legacy_rank_value(self):
        self.assertTrue(self.spec["ranks"]["cannot_cast_ladder_ordinal_to_f04_rank"])
        self.assertNotEqual([x["ladder_ordinal"] for x in self.ranks], self.codes)

    def test_12_zero_is_not_commissioned_ensign(self):
        self.assertIn("NOT_COMMISSIONED", self.spec["ranks"]["zero_means"])
        self.assertEqual(self.spec["commissioned_state"]["missing_commission_behavior"], "DENY_UNCOMMISSIONED")

    def test_13_legacy_unmapped_fails_closed(self):
        self.assertEqual(self.spec["ranks"]["legacy_unmapped_behavior"],
                         "DENY_PROMOTION_PENDING_EXPLICIT_AUTHORIZED_MAPPING")
        self.assertTrue(self.spec["ranks"]["no_rank_code_rewrite_for_legacy_on_load"])

    def test_14_flag_rank_mapping_not_in_small_scope(self):
        self.assertEqual(self.spec["ranks"]["flag_officer_mapping"], "DEFERRED_NOT_A02")
        self.assertEqual(self.spec["ranks"]["exceptional_fleet_captain_mapping"], "DEFERRED_NOT_A02")

    def test_15_character_id_is_128bit_host_issued(self):
        identity = self.spec["identity"]
        self.assertEqual(identity["id_bits"], 128)
        self.assertEqual(identity["external_format"], "lowercase_32_hex_uuid128")
        self.assertIn("trusted_Host", identity["authoritative_issuer"])

    def test_16_identity_segments_lossless_under_48_bit_scalar_limit(self):
        segments = self.spec["identity"]["storage_segments"]
        self.assertEqual([x["bits"] for x in segments], [48, 48, 32])
        self.assertEqual(sum(x["bits"] for x in segments), 128)
        self.assertTrue(all(x["bits"] <= 48 for x in segments))

    def test_17_local_ref_is_not_global_identity(self):
        self.assertEqual(self.spec["identity"]["cross_ship_resolver_status"],
                         "NOT_IMPLEMENTED_UNTIL_P05_B3")
        self.assertTrue(self.spec["compatibility"]["f04_session_scope_not_global_identity"])
        self.assertTrue(self.spec["compatibility"]["f04_ship_identity_not_global_character_identity"])

    def test_18_identity_requires_authoritative_commission(self):
        self.assertIn("commission_event_id", self.spec["commissioned_state"]["required_fields"])
        self.assertIn("rank_event_id", self.spec["commissioned_state"]["required_fields"])
        self.assertTrue(self.spec["ranks"]["f11_codes_not_authoritative_without_verified_commission"])

    def test_19_graduation_not_automatic_commission(self):
        grad = data(GRAD)
        self.assertEqual(grad["default_commission_rank"], "ensign")
        self.assertTrue(self.spec["general_guards"]["no_implicit_graduation_to_commission"])
        self.assertTrue(any("Commission/rank is not awarded" in s for s in grad["rules"]))

    def test_20_service_record_append_only_includes_promotion_and_commission(self):
        history = data(SERVICE)
        self.assertEqual(history["model"], "append_only_event_log")
        self.assertFalse(history["mutable_history"])
        self.assertIn("commission", history["event_types"])
        self.assertIn("promotion", history["event_types"])

    def test_21_promotion_record_contains_all_authoritative_fields(self):
        fields = set(data(SERVICE)["event_fields"])
        self.assertTrue(fields <= set(self.spec["promotion_operation"]["immutable_record_required_fields"]))
        self.assertIn("authority_id", fields)

    def test_22_p01_personnel_domain_preserved(self):
        d = data(P01)["decisions"]["appoint_first_officer"]
        self.assertEqual(d["domain"], "fleet_personnel")
        self.assertTrue(d["requires_external_personnel_authority"])

    def test_23_captain_may_recommend_but_not_promote_by_rank(self):
        rights = self.spec["personnel_authority"]
        self.assertEqual(rights["ship_captain_power"], "RECOMMEND_ONLY_UNLESS_SEPARATE_PERSONNEL_GRANT")
        self.assertEqual(rights["admiral_rank_power"], "NO_AUTOMATIC_PERSONNEL_GRANT")

    def test_24_bootstrap_private_not_mutable_client_switch(self):
        rights = self.spec["personnel_authority"]
        self.assertEqual(rights["grant_issuance_channel"], "TRUSTED_HOST_BOOTSTRAP_ONLY_NOT_PUBLIC_F04_EXECUTE")
        self.assertEqual(rights["authenticated_by"], "trusted_Host_local_native_capability")
        self.assertIn("live_world_revision", rights["grant_verification"])

    def test_25_f05_scan_cannot_authenticate_promotion(self):
        self.assertTrue(self.spec["compatibility"]["f05_scan_only_remains_valid"])
        self.assertIn("F04_SCAN", F05_IMPL.read_text(encoding="utf-8"))
        self.assertEqual(self.spec["personnel_authority"]["f05_ship_orders_power"],
                         "CANNOT_BE_REINTERPRETED_AS_FLEET_PERSONNEL_ORDER")

    def test_26_f04_legacy_abi_remains_protected(self):
        h = F04_HEADER.read_text(encoding="utf-8")
        self.assertIn("typedef struct F04Session F04Session", h)
        self.assertIn("typedef struct { uint64_t scope,id; } F04Ref", h)
        self.assertIn("uint32_t f04_save(", h)
        self.assertIn("uint32_t f04_load(", h)
        self.assertIn("uint32_t f04_person(", h)
        self.assertTrue(self.spec["compatibility"]["old_ABI_unmodified"])

    def test_27_observed_legacy_synthetic_rank_8_not_lore_ordinal(self):
        source = F04_IMPL.read_text(encoding="utf-8")
        self.assertRegex(source, r"set\(c,p,RANK,p==10\?10:p==3\?8:1\)")
        self.assertEqual(data(RANKS)["normal_progression"][7]["id"], "rear_admiral")

    def test_28_strict_f04_validator_needs_explicit_extension(self):
        source = F04_IMPL.read_text(encoding="utf-8")
        self.assertIn("allowed={CATEGORY,RANK,DEPT,QUAL,UNTIL}", source)
        self.assertTrue(self.spec["compatibility"]["f04_strict_person_schema_extension_required"])

    def test_29_exactly_one_initial_promotion_pair(self):
        e = self.spec["promotion_operation"]["eligibility"]
        self.assertEqual((e["source_rank_id"], e["target_rank_id"]), ("ensign", "lieutenant_junior_grade"))
        self.assertEqual((e["source_rank_code"], e["target_rank_code"]), (1101, 1102))
        self.assertEqual(e["other_transitions_in_A02"], "REJECT_AS_OUT_OF_SCOPE")

    def test_30_no_automatic_position_or_transfer(self):
        e = self.spec["promotion_operation"]["eligibility"]
        for flag in ("source_person_keeps_same_unit", "source_person_keeps_same_billet",
                     "source_person_keeps_same_department"):
            self.assertTrue(e[flag])
        self.assertTrue(self.spec["general_guards"]["no_implicit_rank_to_position"])
        self.assertTrue(self.spec["general_guards"]["no_interunit_transfer_in_A02"])

    def test_31_current_revision_and_time_mandatory(self):
        e = self.spec["promotion_operation"]["eligibility"]
        self.assertTrue(e["require_current_world_revision"])
        self.assertEqual(e["effective_tick"], "current_campaign_time_only_no_future_scheduling")

    def test_32_current_commission_evaluation_authority_mandatory(self):
        e = self.spec["promotion_operation"]["eligibility"]
        for flag in ("require_current_commission", "require_current_rank_event",
                     "require_professional_evaluation", "require_authorized_personnel_order"):
            self.assertTrue(e[flag])

    def test_33_atomicity_and_append_only_promotion(self):
        op = self.spec["promotion_operation"]
        self.assertEqual(op["atomicity"], "stage_full_campaign_copy_validate_then_publish_or_no_change")
        self.assertEqual(op["immutable_record_event_type"], "promotion")
        self.assertTrue(self.spec["commissioned_state"]["historic_rank_event_append_only"])

    def test_34_idempotent_replay_does_not_award_second_rank(self):
        key = self.spec["promotion_operation"]["idempotency"]
        self.assertEqual(key["same_key_and_same_payload"], "RETURN_ORIGINAL_COMMITTED_RECEIPT_WITHOUT_NEW_EVENT")
        self.assertTrue(key["lookup_precedes_revision_guard"])
        self.assertTrue(key["persistence_after_load_required"])

    def test_35_colliding_idempotency_key_fails_closed(self):
        key = self.spec["promotion_operation"]["idempotency"]
        self.assertEqual(key["same_key_conflicting_payload"], "DENY_IDEMPOTENCY_CONFLICT")
        self.assertEqual(key["failed_requests"], "NO_COMMITTED_PROMOTION_OR_MUTATED_WORLD")

    def test_36_previous_commit_cannot_grant_new_authority(self):
        key = self.spec["promotion_operation"]["idempotency"]
        self.assertEqual(key["replay_after_authority_revocation"],
                         "RETURN_PREVIOUS_COMMITTED_RECEIPT_ONLY_NO_NEW_AUTHORITY")

    def test_37_history_and_dedup_survive_consolidation(self):
        p = self.spec["persistence"]
        self.assertIn("idempotency_tombstones", p["segmented_history"])
        self.assertTrue(p["no_sidecar_json_as_sole_authoritative_state"])

    def test_38_existing_saves_not_rewritten_on_read(self):
        self.assertTrue(self.spec["general_guards"]["no_legacy_save_rewrite_on_read"])
        self.assertEqual(self.spec["persistence"]["old_archives"],
                         "exact_legacy_unchanged_when_not_opted_in")

    def test_39_no_CXX_implemented_or_claimed(self):
        states = self.spec["validation_status"]
        self.assertEqual(states["real_CXX_implementation"], "NOT_STARTED")
        self.assertEqual(states["native_save_load_proof"], "NOT_STARTED")

    def test_40_sources_stay_within_repo(self):
        self.assertTrue(all(".." not in Path(p).parts and (ROOT / p).is_file()
                            for p in self.spec["sources"]))

    def test_41_core_pin_still_matches_f05(self):
        self.assertEqual(self.spec["core_pinned_sha"], F05_PIN.read_text(encoding="utf-8").strip())

    def test_42_request_includes_authoritative_preconditions(self):
        required = {"subject_character_id","expected_world_revision","idempotency_key",
                    "issuer_authority_grant_id","approved_personnel_order_id",
                    "verified_evaluation_event_id","commission_event_id","expected_rank_event_id"}
        self.assertTrue(required <= set(self.spec["promotion_operation"]["request_fields"]))

    def test_43_receipt_persisted_not_ui_cache(self):
        self.assertEqual(self.spec["promotion_operation"]["receipt_source"],
                         "original_persisted_Core_record_not_response_cache")
        self.assertTrue(self.spec["promotion_operation"]["current_revision_reported_separately"])

    def test_44_p03_has_no_xp_based_promotions(self):
        self.assertFalse(data(P03)["requirements"]["no_generic_xp"] is False)
        self.assertTrue(self.spec["commissioned_state"]["no_auto_xp"])

    def test_45_no_direct_assign_for_F11_succession(self):
        self.assertTrue(self.spec["general_guards"]["no_direct_F04_ASSIGN_for_F11_succession"])

    def test_46_no_false_guarantee_of_intership_runtime(self):
        self.assertEqual(self.spec["validation_status"]["inter_ship_transfers"], "NOT_STARTED")

    def test_47_rank_mapping_does_not_depend_on_role(self):
        h = F04_HEADER.read_text(encoding="utf-8")
        self.assertIn("enum F04Role", h)
        self.assertIn("F04_CAPTAIN=1", h)
        self.assertTrue(self.spec["compatibility"]["f04_role_captain_is_not_f11_rank_captain"])

    def test_48_new_promotion_cannot_run_as_F04_command_duty(self):
        self.assertEqual(self.spec["personnel_authority"]["domain"], "fleet_personnel_promotions")
        self.assertTrue(self.spec["personnel_authority"]["no_ship_duty_required_for_authenticated_fleet_personnel_authority"])


if __name__ == "__main__":
    unittest.main()
