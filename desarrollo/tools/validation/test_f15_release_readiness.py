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

    def test_performance_rejects_non_finite_metrics(self):
        required = {
            "fps_avg": 60,
            "fps_1pct_low": 45,
            "vram_mb_peak": 7200,
            "ram_mb_peak": 18000,
            "cpu_ms_avg": 8.5,
            "session_minutes": 120,
        }
        for bad in (float("inf"), float("nan")):
            with self.subTest(metric=repr(bad)):
                metrics = {**required, "fps_avg": bad}
                result = performance_gate({
                    "executed_on_msi": True,
                    "provider_failure_recovered": True,
                    "metrics": metrics,
                    "evidence_ref": "perf.json",
                })
                self.assertIn("performance_metrics_incomplete", result["reasons"])

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
            "channel": "private_local",
            "artifact_sha256": "bad",
            "build_executed": True,
            "e2e_passed": True,
            "migration_tested": True,
            "rollback_tested": True,
            "backup_restore_tested": True,
            "blocker_count": 0,
            "evidence_refs": ["build"],
        })
        self.assertIn("invalid_build_hash", result["reasons"])

    def test_release_bool_is_strict(self):
        result = release_gate({
            "version": "0.9.0-beta.1",
            "channel": "private_local",
            "artifact_sha256": "1" * 64,
            "build_executed": 1,
            "e2e_passed": True,
            "migration_tested": True,
            "rollback_tested": True,
            "backup_restore_tested": True,
            "blocker_count": 0,
            "evidence_refs": ["build"],
        })
        self.assertIn("invalid_release_record", result["reasons"])

    def test_release_ready_metadata_is_not_release_certification(self):
        result = release_gate({
            "version": "0.9.0-beta.1",
            "channel": "private_candidate",
            "artifact_sha256": "1" * 64,
            "build_executed": True,
            "e2e_passed": True,
            "migration_tested": True,
            "rollback_tested": True,
            "backup_restore_tested": True,
            "blocker_count": 0,
            "evidence_refs": ["build", "e2e", "migration", "rollback"],
        })
        self.assertEqual(result["status"], REVIEW)
        self.assertFalse(result["release_certified"])


    def test_public_release_channels_are_forbidden(self):
        base = {
            "version": "1.0.0",
            "artifact_sha256": "1" * 64,
            "build_executed": True,
            "e2e_passed": True,
            "migration_tested": True,
            "rollback_tested": True,
            "backup_restore_tested": True,
            "blocker_count": 0,
            "evidence_refs": ["msi-build", "recovery"],
        }
        for channel in ("beta", "release_candidate", "internal_beta", "steam"):
            with self.subTest(channel=channel):
                self.assertIn(
                    "invalid_release_channel",
                    release_gate({**base, "channel": channel})["reasons"],
                )

    def test_private_build_requires_backup_restore(self):
        result = release_gate({
            "version": "1.0.0",
            "channel": "private_local",
            "artifact_sha256": "1" * 64,
            "build_executed": True,
            "e2e_passed": True,
            "migration_tested": True,
            "rollback_tested": True,
            "backup_restore_tested": False,
            "blocker_count": 0,
            "evidence_refs": ["msi-build"],
        })
        self.assertIn("backup_restore_not_tested", result["reasons"])

    def test_repository_state_may_advance_without_freezing_f15(self):
        here = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            required = (
                "proyecto/docs/roadmap/master/PLAN_MAESTRO.md",
                "proyecto/docs/roadmap/master/ESTADO_GLOBAL.json",
                "proyecto/docs/roadmap/master/CRITERIOS_DE_CIERRE.md",
                "proyecto/docs/roadmap/master/fases/F15/README.md",
                "desarrollo/tools/validation/f08_acceptance_gate.py",
                "desarrollo/tools/validation/f14_audiovisual_reference.py",
                "proyecto/docs/decisions/prototype_validation_and_release_policy.md",
                "audiovisual/localization/README.md",
                "audiovisual/ui/README.md",
            )
            for relative in required:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((here / relative).read_bytes())
            state_file = root / required[1]
            state = json.loads(state_file.read_text(encoding="utf-8"))
            f15 = next(x for x in state["phases"] if x["id"] == "F15")
            f15["status"] = "EN_REVISION"
            state_file.write_text(json.dumps(state), encoding="utf-8")
            result = audit_repository(root)
            self.assertEqual(result["status"], REVIEW)
            self.assertEqual(result["f15_status"], "EN_REVISION")

    def test_no_ejecutado_capture_template_is_blocked(self):
        here = Path(__file__).resolve().parents[3]
        payload = json.loads(
            (here / "desarrollo/validation/fixtures/f15/f15_beta_capture_template_v0.1.json").read_text(encoding="utf-8")
        )
        result = validate_capture(payload)
        self.assertEqual(result["status"], BLOCKED)
        self.assertIn("f15_capture_not_ready", result["reasons"])

    def test_fixture_has_no_failures(self):
        here = Path(__file__).resolve().parents[3]
        report = execute_fixture(
            here / "desarrollo/validation/fixtures/f15/f15_release_readiness_scenarios_v0.1.json"
        )
        self.assertEqual(report["cases_total"], 38)
        self.assertEqual(report["cases_failed"], 0)

    def test_repository_audit_blocks_missing_root(self):
        with tempfile.TemporaryDirectory() as folder:
            result = audit_repository(folder)
            self.assertEqual(result["status"], BLOCKED)
            self.assertIn("repository_reference_files_missing", result["reasons"])

    def test_repository_audit_accepts_current_reference_state(self):
        here = Path(__file__).resolve().parents[3]
        result = audit_repository(here)
        self.assertEqual(result["status"], REVIEW)
        self.assertEqual(result["f15_status"], "PLANIFICADA")
        self.assertFalse(result["runtime_certified"])
        self.assertFalse(result["release_certified"])

if __name__ == "__main__":
    unittest.main()
