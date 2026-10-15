import json
import tempfile
import unittest
from pathlib import Path

from f15_release_readiness import (
    BLOCKED,
    REVIEW,
    JOURNEY_STAGES,
    audit_repository,
    execute_fixture,
    journey_gate,
    performance_gate,
    qa_gate,
    release_gate,
    ux_gate,
    validate_capture,
)

class F15ReleaseReadinessTests(unittest.TestCase):
    def test_qa_never_certifies_runtime(self):
        result = qa_gate({
            "domain_ci": True,
            "core_integration": True,
            "ue5_automation": True,
            "evidence_refs": ["ci", "core", "ue5"],
        })
        self.assertEqual(result["status"], REVIEW)
        self.assertFalse(result["runtime_certified"])
        self.assertFalse(result["release_certified"])

    def test_qa_bool_is_strict(self):
        self.assertEqual(qa_gate({
            "domain_ci": 1,
            "core_integration": True,
            "ue5_automation": True,
            "evidence_refs": ["x"],
        })["status"], BLOCKED)

    def test_journey_requires_exact_sequence(self):
        result = journey_gate({
            "stages": ["academy", "mission"],
            "executed": True,
            "save_load_continuity": True,
            "evidence_refs": ["trace"],
        })
        self.assertIn("journey_stage_contract_mismatch", result["reasons"])

    def test_journey_requires_save_load(self):
        result = journey_gate({
            "stages": list(JOURNEY_STAGES),
            "executed": True,
            "save_load_continuity": False,
            "evidence_refs": ["trace"],
        })
        self.assertIn("e2e_save_load_continuity_failed", result["reasons"])

    def test_journey_valid_capture_still_requires_manual_acceptance(self):
        result = journey_gate({
            "stages": list(JOURNEY_STAGES),
            "executed": True,
            "save_load_continuity": True,
            "evidence_refs": ["trace", "save", "load"],
        })
        self.assertEqual(result["status"], REVIEW)

    def test_performance_requires_complete_measurements(self):
        result = performance_gate({
            "executed_on_msi": True,
            "provider_failure_recovered": True,
            "metrics": {"fps_avg": 60},
            "evidence_ref": "perf.json",
        })
        self.assertIn("performance_metrics_incomplete", result["reasons"])

    def test_performance_has_no_hidden_threshold(self):
        result = performance_gate({
            "executed_on_msi": True,
            "provider_failure_recovered": True,
            "metrics": {
                "fps_avg": 1,
                "fps_1pct_low": 1,
                "vram_mb_peak": 1,
                "ram_mb_peak": 1,
                "cpu_ms_avg": 1,
                "session_minutes": 1,
            },
            "evidence_ref": "perf.json",
        })
        self.assertEqual(result["status"], REVIEW)
        self.assertFalse(result["thresholds_applied"])

    def test_ux_requires_all_seven_areas(self):
        result = ux_gate({
            "locale": "es-ES",
            "checks": {"castellano": "PASS"},
            "evidence_refs": ["x"],
        })
        self.assertIn("ux_checklist_incomplete", result["reasons"])

    def test_ux_pass_needs_evidence(self):
        checks = {k: "PASS" for k in (
            "castellano", "controls", "accessibility", "ux",
            "logs", "migrations", "recoverable_errors"
        )}
        result = ux_gate({"locale": "es-ES", "checks": checks, "evidence_refs": []})
        self.assertIn("ux_pass_without_evidence", result["reasons"])

    def test_release_rejects_bad_hash(self):
        result = release_gate({
            "version": "0.9.0-beta.1",
            "channel": "beta",
            "artifact_sha256": "bad",
            "build_executed": True,
            "e2e_passed": True,
            "migration_tested": True,
            "rollback_tested": True,
            "blocker_count": 0,
            "evidence_refs": ["build"],
        })
        self.assertIn("invalid_build_hash", result["reasons"])

    def test_release_bool_is_strict(self):
        result = release_gate({
            "version": "0.9.0-beta.1",
            "channel": "beta",
            "artifact_sha256": "1" * 64,
            "build_executed": 1,
            "e2e_passed": True,
            "migration_tested": True,
            "rollback_tested": True,
            "blocker_count": 0,
            "evidence_refs": ["build"],
        })
        self.assertIn("invalid_release_record", result["reasons"])

    def test_release_ready_metadata_is_not_release_certification(self):
        result = release_gate({
            "version": "0.9.0-beta.1",
            "channel": "release_candidate",
            "artifact_sha256": "1" * 64,
            "build_executed": True,
            "e2e_passed": True,
            "migration_tested": True,
            "rollback_tested": True,
            "blocker_count": 0,
            "evidence_refs": ["build", "e2e", "migration", "rollback"],
        })
        self.assertEqual(result["status"], REVIEW)
        self.assertFalse(result["release_certified"])

    def test_no_ejecutado_capture_template_is_blocked(self):
        here = Path(__file__).resolve().parents[2]
        payload = json.loads(
            (here / "validation/fixtures/f15/f15_beta_capture_template_v0.1.json").read_text(encoding="utf-8")
        )
        result = validate_capture(payload)
        self.assertEqual(result["status"], BLOCKED)
        self.assertIn("f15_capture_not_ready", result["reasons"])

    def test_fixture_has_no_failures(self):
        here = Path(__file__).resolve().parents[2]
        report = execute_fixture(
            here / "validation/fixtures/f15/f15_release_readiness_scenarios_v0.1.json"
        )
        self.assertEqual(report["cases_total"], 37)
        self.assertEqual(report["cases_failed"], 0)

    def test_repository_audit_blocks_missing_root(self):
        with tempfile.TemporaryDirectory() as folder:
            result = audit_repository(folder)
            self.assertEqual(result["status"], BLOCKED)
            self.assertIn("repository_reference_files_missing", result["reasons"])

if __name__ == "__main__":
    unittest.main()
