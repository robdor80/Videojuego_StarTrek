#!/usr/bin/env python3
"""F09 pruebas de referencia: no confundir con una consola UE5 ni Core."""
import copy
import json
import unittest

from f09_interconsole_reference import (
    ROOT, MATRIX, CANONICAL, REQUIRED, PRIORITIES, STATUSES,
    assess_handoff, catalog_errors, load_catalog,
    RESULT_ACCEPT, RESULT_DENY, RESULT_CLARIFY,
)


class F09ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = load_catalog()
        cls.entries = {x["id"]: x for x in cls.matrix["families"]}

    def sample(self, source="sensors", target="science"):
        packet = {
            "package_id": "pkg-001", "source_system": source,
            "target_system": target, "created_at": "stardate:2372.1",
            "payload_refs": ["observation-001"],
            "provenance": {
                "source_refs": ["observation-001"],
                "source_system": source, "confidence": "medium",
            }, "priority": "normal", "status": "queued",
        }
        trust = {"known_refs": ["observation-001"],
                 "permitted_routes": [f"{source}->{target}"]}
        return packet, trust

    def decision(self, p, t):
        return assess_handoff(p, t, self.matrix)["decision"]

    def test_canonical_family_count_and_order(self):
        self.assertEqual(tuple(x["id"] for x in self.matrix["families"]), CANONICAL)
        self.assertEqual(len(self.matrix["families"]), 16)

    def test_catalog_against_existing_paths(self):
        self.assertEqual(catalog_errors(self.matrix), [])

    def test_catalog_has_fifteen_non_sensor_families(self):
        self.assertEqual(sum(x["id"] != "sensors" for x in self.matrix["families"]), 15)

    def test_step_coverage(self):
        self.assertTrue(all(
            any(x["step"] == s for x in self.matrix["families"])
            for s in ("P01", "P02", "P03")
        ))

    def test_every_family_can_send_safe_data(self):
        for source, family in self.entries.items():
            with self.subTest(source=source):
                target = family["allowed_data_handoff_targets"][0]
                p, t = self.sample(source, target)
                self.assertEqual(self.decision(p, t), RESULT_ACCEPT)

    def test_existing_sensors_to_science(self):
        p, t = self.sample()
        self.assertEqual(self.decision(p, t), RESULT_ACCEPT)

    def test_navigation_to_conn(self):
        p, t = self.sample("navigation", "conn")
        self.assertEqual(self.decision(p, t), RESULT_ACCEPT)

    def test_communication_to_command(self):
        p, t = self.sample("communications", "command")
        self.assertEqual(self.decision(p, t), RESULT_ACCEPT)

    def test_health_record_to_command_not_auto_authorized(self):
        p, t = self.sample("medical", "command")
        t["permitted_routes"] = []
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_unobserved_world_truth_ref_denied(self):
        p, t = self.sample()
        p["payload_refs"] = ["world-secret"]
        p["provenance"]["source_refs"] = ["world-secret"]
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_provenance_spoof_denied(self):
        p, t = self.sample()
        p["provenance"]["source_system"] = "computer"
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_no_inline_truth_in_packet(self):
        p, t = self.sample()
        p["authoritative_world_truth"] = {"enemy": True}
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_no_inline_permissions_override(self):
        p, t = self.sample()
        t["permitted_routes"] = []
        p["permitted_routes"] = ["sensors->science"]
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_missing_trust_fails_closed(self):
        p, t = self.sample()
        self.assertEqual(self.decision(p, {}), RESULT_DENY)

    def test_known_but_not_permitted_denied(self):
        p, t = self.sample()
        t["permitted_routes"] = []
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_legacy_conn_navigation_requires_resolution(self):
        p, t = self.sample()
        p["target_system"] = "conn_navigation"
        self.assertEqual(self.decision(p, t), RESULT_CLARIFY)

    def test_legacy_computer_database_requires_resolution(self):
        p, t = self.sample()
        p["target_system"] = "computer_database"
        self.assertEqual(self.decision(p, t), RESULT_CLARIFY)

    def test_route_not_declared_denied(self):
        p, t = self.sample("medical", "sensors")
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_duplicate_ref_denied(self):
        p, t = self.sample()
        p["payload_refs"] = ["observation-001", "observation-001"]
        p["provenance"]["source_refs"] = p["payload_refs"][:]
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_invalid_priority_denied(self):
        p, t = self.sample()
        p["priority"] = "SUPER-ADMIN"
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_invalid_status_denied(self):
        p, t = self.sample()
        p["status"] = "executed_action"
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_unhashable_priority_fails_closed(self):
        p, t = self.sample()
        p["priority"] = []
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_unhashable_status_fails_closed(self):
        p, t = self.sample()
        p["status"] = {"bad": 1}
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_unhashable_confidence_fails_closed(self):
        p, t = self.sample()
        p["provenance"]["confidence"] = []
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_unhashable_console_fails_closed(self):
        p, t = self.sample()
        p["target_system"] = []
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_p05_reference_scenario_fixture(self):
        path = ROOT / "desarrollo/validation/fixtures/f09/f09_interconsole_scenarios_v0.1.json"
        fixture = json.loads(path.read_text("utf-8"))
        self.assertEqual(fixture["execution_level"], "reference_only")
        self.assertEqual(fixture["case_count"], 22)
        self.assertEqual(len(fixture["cases"]), 22)
        self.assertEqual(set(c["scenario"] for c in fixture["cases"]),
                         {"averia", "combate", "mision", "multitarea", "privacidad"})
        seen = set()
        for case in fixture["cases"]:
            with self.subTest(case=case["case_id"]):
                self.assertNotIn(case["case_id"], seen)
                seen.add(case["case_id"])
                actual = assess_handoff(
                    case["packet"], case["trusted_reference_context"], self.matrix
                )
                self.assertEqual(actual["decision"], case["expected_decision"])
                self.assertIn(actual["reason"], {
                    "metadata_transfer_only", "unobserved_or_forbidden_refs",
                    "route_not_authorized", "same_family_not_handoff",
                    "route_not_designed", "ambiguous_legacy_target",
                })

    def test_missing_fields_denied(self):
        p, t = self.sample()
        del p["provenance"]
        self.assertEqual(self.decision(p, t), RESULT_DENY)

    def test_no_metadata_mutation(self):
        p, t = self.sample()
        before = copy.deepcopy((p, t, self.matrix))
        self.assertEqual(self.decision(p, t), RESULT_ACCEPT)
        self.assertEqual((p, t, self.matrix), before)

    def test_no_unverified_core_execution_or_ue5_artifacts(self):
        self.assertEqual(self.matrix["status"], "reference_only_not_runtime")
        self.assertTrue(all(e["execution_owner"].startswith("Core RPG")
                            for e in self.matrix["families"]))

    def test_existing_interconsole_contract_still_fixed(self):
        base = json.loads((ROOT / "sistemas/gameplay/ship_operations/interconsole/"
                           "interconsole_data_package_contract.json").read_text("utf-8"))
        self.assertEqual(base["status"], "fixed")
        self.assertEqual(tuple(base["required"]), REQUIRED)
        self.assertEqual(set(base["fields"]["priority"]), set(PRIORITIES))
        self.assertEqual(set(base["fields"]["status"]), set(STATUSES))

    def test_catalog_rejects_missing_reference(self):
        broken = copy.deepcopy(self.matrix)
        broken["families"][0]["existing_contract_refs"] = ["not/a/real/file.json"]
        self.assertTrue(catalog_errors(broken))

    def test_catalog_rejects_duplicate_family(self):
        broken = copy.deepcopy(self.matrix)
        broken["families"][1]["id"] = "command"
        self.assertTrue(catalog_errors(broken))


if __name__ == "__main__":
    unittest.main()
