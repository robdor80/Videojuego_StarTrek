import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
MODULE_PATH = HERE.with_name("f14_audiovisual_reference.py")
spec = importlib.util.spec_from_file_location("f14", MODULE_PATH)
f14 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(f14)

FIXTURE = HERE.parents[3] / "desarrollo/validation" / "fixtures" / "f14" / "f14_audiovisual_scenarios_v0.1.json"


class F14ScenarioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_all_declared_scenarios(self):
        seen = set()
        for case in self.payload["cases"]:
            with self.subTest(case=case["id"]):
                self.assertNotIn(case["id"], seen)
                seen.add(case["id"])
                result = f14.run_case(case)
                self.assertEqual(result["status"], case["expected_status"])
                self.assertIn(case["expected_reason"], result["reasons"])
                self.assertEqual(result["authority"], f14.AUTHORITY)

    def test_fixture_is_large_enough_to_cover_all_five_steps(self):
        operations = {c["operation"] for c in self.payload["cases"]}
        self.assertEqual(
            operations,
            {"nap_alignment", "rights", "priority", "presentation", "optimization", "traceability"},
        )
        self.assertGreaterEqual(len(self.payload["cases"]), 40)

    def test_unknown_operation_fails_closed(self):
        result = f14.run_case({"operation": "invent_magic_asset", "input": {}})
        self.assertEqual(result["status"], f14.BLOCKED)
        self.assertIn("unknown_operation", result["reasons"])

    def test_truthy_strings_never_count_as_boolean_evidence(self):
        p = {
            "asset_id": "a",
            "priority": 1,
            "need_ref": "n",
            "source_state": "REFERENCE_ONLY",
            "rights_state": "UNKNOWN",
            "ue5_claim": "false",
        }
        self.assertEqual(f14.priority_gate(p)["status"], f14.BLOCKED)

    def test_rights_verified_is_not_distribution_permission(self):
        r = {
            "asset_id": "a",
            "source_ref": "src",
            "author_declared": "author",
            "license_declared": "project_original",
            "rights_verified": True,
        }
        result = f14.rights_gate(r)
        self.assertEqual(result["status"], f14.REVIEW)
        self.assertFalse(result["distribution_allowed"])

    def test_optimization_never_certifies_ue5(self):
        item = {
            "asset_id": "a",
            "original_sha256": "1" * 64,
            "derivative_sha256": "2" * 64,
            "overwrite_original": False,
            "claim_optimized": True,
            "metrics": {"fps": 60, "vram_mb": 1000, "draw_calls": 100},
            "lod_verified": True,
            "streaming_verified": True,
        }
        result = f14.optimization_gate(item)
        self.assertEqual(result["status"], f14.REVIEW)
        self.assertFalse(result["optimized_claim_certified"])

    def test_build_claim_requires_execution_and_evidence(self):
        item = {
            "asset_id": "a",
            "source_ref": "src",
            "original_sha256": "1" * 64,
            "derivative_sha256": "2" * 64,
            "manifest_ref": "manifest",
            "external_repo_ref": "repo@sha",
            "claim_build_functional": True,
            "ue5_execution": "NO_EJECUTADO",
            "build_evidence_ref": None,
            "recovery_tested": False,
            "recovery_evidence_ref": None,
        }
        result = f14.traceability_gate(item)
        self.assertEqual(result["status"], f14.BLOCKED)
        self.assertIn("build_claim_without_execution_evidence", result["reasons"])

    def test_execute_fixture_reproducible(self):
        a = f14.execute_fixture(FIXTURE)
        b = f14.execute_fixture(FIXTURE)
        self.assertEqual(a["scenario_sha256"], b["scenario_sha256"])
        self.assertEqual(a["cases_total"], b["cases_total"])
        self.assertEqual(a["cases_failed"], 0)
        self.assertEqual(a, b)

    def test_repository_audit_validates_real_priority_manifests(self):
        root = HERE.parents[3]
        result = f14.audit_repository(root)
        self.assertEqual(f14.REVIEW, result["status"])
        self.assertGreater(result["asset_priority_entries"], 0)
        self.assertGreater(result["presentation_priority_families"], 0)


if __name__ == "__main__":
    unittest.main()
