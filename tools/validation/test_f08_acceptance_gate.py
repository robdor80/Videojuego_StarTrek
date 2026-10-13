#!/usr/bin/env python3
"""Pruebas SINTÉTICAS del validador F08, nunca test Core/UE5 ni ejecución MSI."""
import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "tools/validation/f08_acceptance_gate.py"
spec = importlib.util.spec_from_file_location("f08_acceptance_gate", PATH)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
FIXTURE = gate.reference_fixture()


def test_record(base: Path) -> dict:
    """Un manifiesto artificial para comprobar el validador, NO evidencia jugable."""
    artifacts = {}
    for name in sorted(gate.REQUIRED_ARTIFACTS):
        path = base / (name + ".test")
        data = ("FAKE TEST FILE / F08 / " + name).encode()
        path.write_bytes(data)
        artifacts[name] = {"path": path.name, "sha256": hashlib.sha256(data).hexdigest()}
    def evt(etype, idx, subjects, parent=None):
        item = {
            "event_id": "evt-" + str(idx), "event_type": etype,
            "occurred_at": "2372-03-14T10:42:" + f"{idx:02d}",
            "scope": {"ship_id": "test_ship", "console_family": "sensors"},
            "actor_refs": {"character_id": "test:officer"},
            "subject_refs": subjects,
            "provenance": {"system": "CoreRPG"},
            "visibility": {"initial_scopes": ["participants"]},
        }
        if parent:
            item["causal_refs"] = [parent]
        return item
    events = [
        evt("ORDER_ISSUED", 1, {"order_id": "ord-1"}),
        evt("ORDER_ACKNOWLEDGED", 2, {"order_id": "ord-1"}, "evt-1"),
        evt("ACTION_STARTED", 3, {"operation_id": "scan-1", "order_id": "ord-1"}, "evt-2"),
        evt("RESULT_CREATED", 4, {"operation_id": "scan-1", "result_id": "result-1"}, "evt-3"),
        evt("REPORT_MADE", 5, {"order_id": "ord-1", "result_id": "result-1"}, "evt-4"),
    ]
    context = copy.deepcopy(FIXTURE["campaign_context"])
    checkpoint = {
        "entity_ids": ["entity-1", "entity-2"],
        "known_contact_ids": ["contact-a"],
        "event_ids": [e["event_id"] for e in events],
        "pending_order_ids": ["ord-1"],
        "campaign_seed": context["campaign_seed"],
        "observer_id": "test_ship",
        "revision": 42,
    }
    return {
        "fixture_id": FIXTURE["fixture_id"],
        "campaign_context": context,
        "execution_kind": "core_ue5_runtime",
        "environment": {
            "trek_commit": "test-trek", "core_commit": "test-core",
            "ue_version": "5.x.test", "map_name": "L_Sutherland_Test",
            "build_hash": "test-build", "build_type": "Development",
            "msi_model": "MSI Raider GE78 HX 14V",
        },
        "order": {
            "order_id": "ord-1", "issuer_character_id": "test:captain",
            "recipient_character_id": "test:officer",
            "authorization": {
                "checked_by": "CoreRPG", "decision": "allow", "validated": True,
            },
        },
        "events": events,
        "public_projection": {
            "detections": [{"contact_id": "contact-a",
                            "observed": {"signature_type": "subspace"}}],
        },
        "save_load": {"before": checkpoint, "after": copy.deepcopy(checkpoint)},
        "artifacts": artifacts,
        "cases": {
            item["id"]: {"status": "PASS", "evidence_ids": ["core_trace"]}
            for item in FIXTURE["must_pass"]
        },
    }


class F08GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.example = test_record(self.base)

    def check_has(self, code, record=None, folder=None):
        result = gate.validate_capture(
            record if record is not None else self.example,
            artifact_dir=self.base if folder is None else folder,
            fixture=FIXTURE,
        )
        self.assertIn(code, result["problems"])
        self.assertFalse(result["runtime_certified"])
        return result

    def test_01_official_13_cases_and_identity(self):
        self.assertEqual(len(FIXTURE["must_pass"]), 13)
        self.assertEqual(len({i["id"] for i in FIXTURE["must_pass"]}), 13)
        self.assertEqual(FIXTURE["fixture_id"], "sensors_vertical_slice_acceptance_v0_0_1")

    def test_02_coherent_fake_is_review_not_certification(self):
        result = gate.validate_capture(self.example, artifact_dir=self.base, fixture=FIXTURE)
        self.assertEqual(result["verdict"], "READY_FOR_MANUAL_REVIEW")
        self.assertEqual(result["problems"], [])
        self.assertFalse(result["runtime_certified"])

    def test_03_no_executed_cases_cannot_pass(self):
        for case in self.example["cases"].values():
            case["status"] = "NO_EJECUTADO"
            case["evidence_ids"] = []
        result = gate.validate_capture(self.example, artifact_dir=self.base, fixture=FIXTURE)
        self.assertEqual(result["verdict"], "BLOCKED")
        self.assertFalse(result["acceptance_pass_claims"])

    def test_04_missing_or_extra_required_case_rejected(self):
        self.example["cases"].pop("event_chain")
        self.check_has("ACCEPTANCE_CASE_IDS_MISMATCH")
        self.example["cases"]["event_chain"] = {"status": "PASS", "evidence_ids": ["core_trace"]}
        self.example["cases"]["invented_test"] = {"status": "PASS", "evidence_ids": ["core_trace"]}
        self.check_has("ACCEPTANCE_CASE_IDS_MISMATCH")

    def test_05_pass_without_evidence_rejected(self):
        self.example["cases"]["anti_leakage"]["evidence_ids"] = []
        self.check_has("PASS_WITHOUT_EVIDENCE:anti_leakage")

    def test_06_wrong_campaign_context_and_source(self):
        self.example["campaign_context"]["campaign_date"] = "2399-01-01"
        self.example["execution_kind"] = "reference_python"
        self.check_has("CAMPAIGN_CONTEXT_MISMATCH")
        self.check_has("NO_CORE_UE5_RUNTIME_DECLARED")

    def test_07_invalid_or_missing_core_order_authority(self):
        self.example["order"]["authorization"]["validated"] = "true"
        self.check_has("CORE_ORDER_AUTHORIZATION_UNVERIFIED")

    def test_08_event_order_and_linkage_rejected(self):
        self.example["events"][2], self.example["events"][3] = (
            self.example["events"][3], self.example["events"][2])
        self.check_has("ORDER_SCAN_REPORT_CHAIN_INVALID")

    def test_09_unrelated_or_forward_causal_reference(self):
        self.example["events"][2]["causal_refs"] = ["evt-5"]
        self.check_has("CAUSAL_REFERENCE_NOT_PRIOR")

    def test_10_duplicate_event_id_rejected(self):
        self.example["events"][4]["event_id"] = "evt-4"
        self.check_has("EVENT_ID_DUPLICATE_OR_INVALID")

    def test_11_reference_candidates_never_authoritative(self):
        self.example["events"][3]["candidate_only"] = True
        self.example["events"][3]["requires_core_confirmation"] = True
        self.example["events"][3]["provenance"]["system"] = "f06_reference_only"
        self.check_has("CANDIDATE_EVENT_NOT_COMMITTED")
        self.check_has("REFERENCE_EVENT_NOT_AUTHORITATIVE")

    def test_12_public_projections_have_no_secret_ids(self):
        self.example["public_projection"]["detections"][0]["observed"]["ground_truth"] = "hidden"
        self.check_has("PUBLIC_PROJECTION_CONTAINS_HIDDEN_FIELDS")
        del self.example["public_projection"]["detections"][0]["observed"]["ground_truth"]
        self.example["public_projection"]["detections"][0]["entity_id"] = "hidden"
        self.check_has("PUBLIC_PROJECTION_CONTAINS_HIDDEN_FIELDS")

    def test_13_save_reload_preserves_ids_and_revision(self):
        self.example["save_load"]["after"]["entity_ids"][0] = "regen"
        self.example["save_load"]["after"]["revision"] = 0
        self.check_has("SAVE_LOAD_CONTINUITY_FAILURE:entity_ids")
        self.check_has("SAVE_LOAD_REVISION_INVALID")

    def test_14_corrupted_evidence_is_not_accepted(self):
        (self.base / "core_trace.test").write_bytes(b"modified")
        self.check_has("ARTIFACT_INTEGRITY_FAILURE:core_trace")

    def test_15_missing_evidence_file_blocks(self):
        (self.base / "ue5_log.test").unlink()
        self.check_has("ARTIFACT_MISSING_OR_OUTSIDE_ROOT:ue5_log")

    def test_16_path_traversal_forbidden(self):
        self.example["artifacts"]["screenshot"]["path"] = "../secret.bin"
        self.check_has("ARTIFACT_PATH_UNSAFE:screenshot")

    def test_17_broken_environment_or_different_msi(self):
        self.example["environment"]["msi_model"] = "other PC"
        self.check_has("MSI_PLATFORM_NOT_CONFIRMED")

    def test_18_unknown_evidence_reference(self):
        self.example["cases"]["event_chain"]["evidence_ids"] = ["nothing"]
        self.check_has("PASS_EVIDENCE_REFERENCE_UNKNOWN:event_chain")

    def test_19_missing_evidence_dir(self):
        self.check_has("ARTIFACT_BASE_DIRECTORY_MISSING", folder=Path("/does-not-exist")) if False else None
        result = gate.validate_capture(self.example, fixture=FIXTURE)
        self.assertIn("ARTIFACT_BASE_DIRECTORY_MISSING", result["problems"])

    def test_20_invalid_input_fails_closed(self):
        self.assertEqual(gate.validate_capture(None)["verdict"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
