#!/usr/bin/env python3
"""Static F10 <-> HOST candidate-contract checks; never creates Core entities.

These checks validate a proposed interface against existing locked content.
Passing them does NOT certify an Academy factory, CoreRPG, UE or M1.
"""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ACADEMY = ROOT / "sistemas/gameplay/careers/academy_path"
CONTRACT_PATH = ACADEMY / "f10_host_candidate_factory_contract_v0.1.json"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected object: {path}")
    return value


def audit(contract: dict, creation: dict, academy_state: dict, admission: dict) -> None:
    """Fail closed on interface drift. No runtime/admission decision is made."""
    if contract.get("status") != "PROPOSED_NOT_IMPLEMENTED":
        raise ValueError("Must not claim implemented factory")
    if contract.get("classification") != "ARCHITECTURE_CONTRACT_ONLY_NO_CORE_MUTATION":
        raise ValueError("Contract classification drift")
    owners = contract.get("owners", {})
    if owners != {
        "domain": "F10",
        "session_and_player_binding": "HOST_H03",
        "persistence": "HOST_H04",
        "engine_adapter": "HOST_H06",
        "professional_commission": "F11",
    }:
        raise ValueError("Authority owners drift")

    campaign = contract.get("campaign", {})
    if (campaign.get("scenario_id") != "starfleet_academy"
            or campaign.get("approved_start_year") != 2383
            or campaign.get("start_month_day") != "UNDECIDED_BY_AUTHOR"
            or campaign.get("runtime_core_sha")
            != "76a7b7b485616d8c4994f384a90f123bf333591d"
            or campaign.get("fixed_calendar_date_prohibited") is not True
            or campaign.get("ship_template_as_academy_prohibited") is not True):
        raise ValueError("Campaign must not invent a date or a ship campus")

    payload = contract.get("player_input_contract", {})
    required = payload.get("required_biography_fields")
    optional = payload.get("optional_biography_fields")
    forbidden = payload.get("forbidden_client_fields")
    if (required != creation.get("required_character_fields")
            or optional != creation.get("optional_character_fields")):
        raise ValueError("Biography fields changed from locked creation baseline")
    if (not isinstance(forbidden, list)
            or len(set(forbidden)) != len(forbidden)
            or set(forbidden) & (set(required) | set(optional))
            or not {
                "person_id", "F04Ref", "scope", "generation",
                "core_revision", "trusted_origin", "validated_creation_ref",
                "admission_authorized", "academy_population_slot_id",
                "commission_event_id", "f11_character_id",
                "authority_grant_id", "rank", "host_principal"
            }.issubset(set(forbidden))):
        raise ValueError("Client may influence authoritative identity or powers")
    if payload.get("payload_semantics") != "untrusted_draft_not_approval":
        raise ValueError("Client proposal cannot be credential")

    validation = contract.get("validation", {})
    if (set(validation.get("required_before_candidate_commit", [])) != {
            "objective_rules_valid", "semantic_coherence_review_valid",
            "source_profile_eligible", "campaign_context_valid"}
            or validation.get("review_unavailable_behavior") != "KEEP_DRAFT_UNBOUND"
            or validation.get("invalid_or_pending_behavior")
            != "NO_PERSON_NO_PUBLISHED_CAMPAIGN"
            or validation.get("review_is_evidence_not_authority") is not True):
        raise ValueError("Unvalidated drafts cannot materialize a PERSON")

    stages = contract.get("candidate_lifecycle", [])
    if [stage.get("state") for stage in stages] != [
            "candidate", "admitted", "cadet_year_1"]:
        raise ValueError("Candidate/admission order drift")
    if not all(stage["state"] in academy_state.get("lifecycle", []) for stage in stages):
        raise ValueError("Phase absent from Academy lifecycle")
    if [stage.get("cadet_slot") for stage in stages] != [
            "NONE", "CONSUME_ONCE", "RETAIN_SAME"]:
        raise ValueError("Cadet slot must be consumed exactly once after admission")
    if any(stage.get("service_rank") != "NONE"
           or stage.get("f05_initiative") != "NONE" for stage in stages):
        raise ValueError("Cadet cannot inherit commission or naval initiative")

    operation_ids = [entry.get("semantic_id")
                     for entry in contract.get("product_operations_proposed", [])]
    if operation_ids != [
            "f10_stage_candidate", "f10_commit_candidate",
            "host_bind_candidate", "f10_confirm_admission",
            "host_restore_academy"]:
        raise ValueError("Factory/domain/binding/restore stages drift")
    if len(operation_ids) != len(set(operation_ids)):
        raise ValueError("Duplicate operation")

    authority = set(contract.get("authority_invariants", []))
    if not {
            "ONE_CORE_WORLD_STATE_PER_CAMPAIGN",
            "STAGING_BEFORE_ATOMIC_PUBLICATION",
            "REPLAY_SAME_INTENT_NO_DUPLICATE_PERSON_SLOT_HISTORY",
            "NO_F05_BIND_REQUIRED_FOR_CANDIDATE",
            "NO_F11_COMMISSION_FROM_CANDIDATE_OR_ADMISSION",
            "NO_PUBLIC_CLIENT_SETTER_FOR_PERSON_OR_PLAYER_BINDING",
            "IMPORT_WITHOUT_TRUSTED_PROVENANCE_FAIL_CLOSED"
            }.issubset(authority):
        raise ValueError("Critical boundary guarantee removed")
    identity = contract.get("identity", {})
    if (identity.get("professional_f11_character_id")
            != "ABSENT_UNTIL_AUTHORIZED_COMMISSION"
            or identity.get("candidate_to_f11_mapping")
            != "REQUIRES_EXPLICIT_F10_F11_AGREEMENT"):
        raise ValueError("F11 identity cannot be preissued")
    persistence = contract.get("save_restore", {})
    if (persistence.get("legacy_host_slot") != "TREKHOST4 1"
            or persistence.get("academy_slot_format") != "TO_BE_VERSIONED_BY_H04"
            or persistence.get("legacy_no_silent_migration") is not True
            or persistence.get("untrusted_restore_behavior") != "NO_ACTIVE_SESSION_SWAP"):
        raise ValueError("Unsafe save/restore interpretation")

    if not {"admitted", "admitted_with_support"}.issubset(
            set(admission.get("possible_outcomes", []))):
        raise ValueError("Academy outcomes no longer match the domain")
    evidence = contract.get("evidence_gate", {})
    if (evidence.get("runtime_factory") != "NOT_IMPLEMENTED"
            or evidence.get("unreal_acceptance") != "NOT_RUN"
            or evidence.get("m1") != "PARTIAL"):
        raise ValueError("Unverified runtime cannot be declared successful")


class HostCandidateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = load(CONTRACT_PATH)
        cls.creation = load(
            ROOT / "sistemas/gameplay/character_creation/character_creation_contract_v1_0.json")
        cls.state = load(ACADEMY / "academy_state.json")
        cls.admission = load(ACADEMY / "admission_flow.json")

    def verify(self, document: dict) -> None:
        audit(document, self.creation, self.state, self.admission)

    def test_contract_aligns_with_locked_f10_sources(self) -> None:
        self.verify(self.contract)
        paths = self.contract["source_contract_paths"]
        self.assertEqual(len(paths), len(set(paths)))
        for relative in paths:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_never_claims_product_is_live(self) -> None:
        doc = copy.deepcopy(self.contract)
        doc["status"] = "IMPLEMENTED"
        with self.assertRaisesRegex(ValueError, "Must not claim"):
            self.verify(doc)

    def test_biography_cannot_bypass_semantic_validation(self) -> None:
        doc = copy.deepcopy(self.contract)
        doc["validation"]["required_before_candidate_commit"].remove(
            "semantic_coherence_review_valid")
        with self.assertRaisesRegex(ValueError, "Unvalidated drafts"):
            self.verify(doc)

    def test_client_cannot_choose_an_entity(self) -> None:
        doc = copy.deepcopy(self.contract)
        doc["player_input_contract"]["forbidden_client_fields"].remove("person_id")
        with self.assertRaisesRegex(ValueError, "Client may influence"):
            self.verify(doc)

    def test_no_imaginary_admission(self) -> None:
        doc = copy.deepcopy(self.contract)
        doc["candidate_lifecycle"][0]["cadet_slot"] = "CONSUME_ONCE"
        with self.assertRaisesRegex(ValueError, "Cadet slot"):
            self.verify(doc)

    def test_f05_is_not_the_cadet_identity(self) -> None:
        doc = copy.deepcopy(self.contract)
        doc["candidate_lifecycle"][0]["f05_initiative"] = "REQUIRED"
        with self.assertRaisesRegex(ValueError, "Cadet cannot inherit"):
            self.verify(doc)

    def test_f11_cannot_issue_a_commission_automatically(self) -> None:
        doc = copy.deepcopy(self.contract)
        doc["identity"]["professional_f11_character_id"] = "ISSUED_ON_ADMISSION"
        with self.assertRaisesRegex(ValueError, "F11 identity"):
            self.verify(doc)

    def test_no_silent_legacy_save_upgrade(self) -> None:
        doc = copy.deepcopy(self.contract)
        doc["save_restore"]["legacy_no_silent_migration"] = False
        with self.assertRaisesRegex(ValueError, "Unsafe save"):
            self.verify(doc)

    def test_no_unsupported_precise_calendar_date(self) -> None:
        doc = copy.deepcopy(self.contract)
        doc["campaign"]["start_month_day"] = "09-01"
        with self.assertRaisesRegex(ValueError, "Campaign must"):
            self.verify(doc)


if __name__ == "__main__":
    unittest.main()
