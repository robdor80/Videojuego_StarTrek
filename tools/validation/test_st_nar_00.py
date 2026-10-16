"""ST-NAR-00 hermetic offline regression tests; never runtime integration tests."""
import copy
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from st_nar_00 import (
    ROOT, inspect_pack, inspect_context, assess_pack, export_bundle,
    verify_bundle, schema_errors, build_bundle_files
)

BASE = ROOT / "validation" / "fixtures" / "seasons"
GOOD = BASE / "reference_pack"

def context():
    return json.loads((BASE / "campaign_context_full_v0.1.json").read_text(encoding="utf-8"))

def draft_copy():
    return json.loads((GOOD / "manifest.json").read_text(encoding="utf-8"))

class NarrativeContractsTest(unittest.TestCase):
    def make_pack(self, temp, manifest=None, chapters=None):
        directory = Path(temp) / "pack"
        (directory / "chapters").mkdir(parents=True)
        source = manifest or draft_copy()
        (directory / "manifest.json").write_text(json.dumps(source), encoding="utf-8")
        for name in ("chapter_demo_01", "chapter_demo_02"):
            target = json.loads((GOOD / "chapters" / (name + ".json")).read_text(encoding="utf-8"))
            if chapters and name in chapters:
                target = chapters[name]
            (directory / "chapters" / (name + ".json")).write_text(json.dumps(target), encoding="utf-8")
        return directory

    def test_valid_reference_pack(self):
        manifest, chapters, errors = inspect_pack(GOOD)
        self.assertEqual(errors, [])
        self.assertEqual(len(chapters), 2)
        self.assertEqual(manifest["publication_status"], "reference_only")

    def test_valid_full_and_delta(self):
        self.assertEqual(inspect_context(context()), [])
        delta = json.loads((BASE / "campaign_context_delta_v0.1.json").read_text(encoding="utf-8"))
        self.assertEqual(inspect_context(delta), [])

    def test_bool_not_integer(self):
        value = context()
        value["coverage"]["complete"] = 1
        self.assertTrue(inspect_context(value))

    def test_missing_cursor_sequence(self):
        value = context()
        value["history"].pop(1)
        self.assertIn("missing, duplicate or unordered history sequences", inspect_context(value))

    def test_out_of_order_event(self):
        value = context()
        value["history"][0], value["history"][1] = value["history"][1], value["history"][0]
        self.assertIn("missing, duplicate or unordered history sequences", inspect_context(value))

    def test_historical_summary_not_current_condition(self):
        value = context()
        self.assertIn("history.borg_assimilation", value["current"]["historical_fact_ids"])
        self.assertNotIn("current.assimilated", value["current"]["current_fact_ids"])
        self.assertIn("current.recovered", value["current"]["current_fact_ids"])

    def test_history_facts_not_forged(self):
        value = context()
        value["current"]["historical_fact_ids"].remove("history.borg_assimilation")
        self.assertIn("history facts diverge from complete event ledger", inspect_context(value))

    def test_future_event_rejected(self):
        value = context()
        value["history"][2]["occurred_at"] = "2400-01-01T00:00:00"
        self.assertIn("invalid or future event timestamp", inspect_context(value))

    def test_plan_without_installed_version_rejected(self):
        value = context()
        value["pending_season_plans"][0]["pack_version"] = "9.9.9"
        self.assertIn("pending plan not backed by installed pack version", inspect_context(value))

    def test_no_spoiler_as_fact(self):
        value = context()
        value["pending_season_plans"][0]["is_future_proposal"] = False
        self.assertTrue(inspect_context(value))

    def test_missing_chapter_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.make_pack(tmp)
            (p / "chapters" / "chapter_demo_02.json").unlink()
            self.assertTrue(any("missing_or_oversized_file" in e for e in inspect_pack(p)[2]))

    def test_script_injection_field_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = draft_copy()
            manifest["python_script"] = "import os"
            p = self.make_pack(tmp, manifest)
            self.assertTrue(any("unexpected python_script" in e for e in inspect_pack(p)[2]))

    def test_absolute_path_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = draft_copy()
            manifest["chapter_files"] = ["/tmp/chapter.json"]
            self.assertTrue(inspect_pack(self.make_pack(tmp, manifest))[2])

    def test_dependency_cycle_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = json.loads((GOOD / "chapters" / "chapter_demo_01.json").read_text(encoding="utf-8"))
            c["depends_on"] = ["chapter_demo_02"]
            p = self.make_pack(tmp, chapters={"chapter_demo_01": c})
            self.assertTrue(any("cycle" in e or "no root" in e for e in inspect_pack(p)[2]))

    def test_duplicate_outcome_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = json.loads((GOOD / "chapters" / "chapter_demo_01.json").read_text(encoding="utf-8"))
            c["outcomes"].append(copy.deepcopy(c["outcomes"][0]))
            p = self.make_pack(tmp, chapters={"chapter_demo_01": c})
            self.assertTrue(any("duplicate outcome" in e for e in inspect_pack(p)[2]))

    def test_reference_not_installable(self):
        result = assess_pack(GOOD, context(), True)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["reasons"], ["reference_only_not_installable"])

    def test_history_contradiction_never_silently_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = draft_copy()
            m["publication_status"] = "approved_content"
            m["constraints"]["forbid_history_fact_ids"] = ["history.borg_assimilation"]
            p = self.make_pack(tmp, m)
            result = assess_pack(p, context(), True)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertIn("contradicts_immutable_history", result["reasons"])

    def test_missing_current_fact_means_dormant_not_rewrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = draft_copy()
            m["publication_status"] = "approved_content"
            m["constraints"]["require_current_fact_ids"] = ["current.unavailable_now"]
            p = self.make_pack(tmp, m)
            self.assertEqual(assess_pack(p, context(), True)["status"], "DORMANT_ELIGIBILITY")

    def test_no_opt_in_to_existing_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = draft_copy()
            m["publication_status"] = "approved_content"
            p = self.make_pack(tmp, m)
            self.assertEqual(assess_pack(p, context(), False)["status"], "OPT_IN_REQUIRED")

    def test_stale_campaign_revision_requires_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = draft_copy()
            m["publication_status"] = "approved_content"
            m["authoring_binding"] = {"campaign_id": "campaign_test_001", "snapshot_revision": 6, "catalog_revision": 2}
            p = self.make_pack(tmp, m)
            result = assess_pack(p, context(), True)
            self.assertEqual(result["status"], "REVIEW_REQUIRED")
            self.assertIn("authoring_context_stale", result["reasons"])

    def test_missing_capability_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = draft_copy()
            m["publication_status"] = "approved_content"
            m["capability_ids"] = ["new_engine_operation_v1"]
            p = self.make_pack(tmp, m)
            self.assertEqual(assess_pack(p, context(), True)["status"], "BLOCKED")

    def test_ready_still_not_runtime_certified(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = draft_copy()
            m["publication_status"] = "approved_content"
            p = self.make_pack(tmp, m)
            result = assess_pack(p, context(), True)
            self.assertEqual(result["status"], "REVIEW_REQUIRED")
            self.assertFalse(result["runtime_certified"])
            self.assertFalse(result["installation_performed"])

    def test_no_seed_without_capability(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = draft_copy()
            m["activation"]["origin"] = "authorized_seed_candidate"
            p = self.make_pack(tmp, m)
            self.assertTrue(any("authorized seed requires" in e for e in inspect_pack(p)[2]))

    def test_export_verify_zip_and_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a.zip", Path(tmp) / "b.zip"
            export_bundle(context(), a)
            export_bundle(context(), b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertEqual(verify_bundle(a)["status"], "VALID_OFFLINE_REFERENCE_BUNDLE")
            with zipfile.ZipFile(a) as z:
                self.assertIn("RESUMEN_CAMPAÑA.md", z.namelist())
                self.assertIn("HISTORIA_REAL.json", z.namelist())

    def test_bundle_tampering_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "bad.zip"
            entries = build_bundle_files(context())
            entries["HISTORIA_REAL.json"] = b"[]"
            with zipfile.ZipFile(file, "w") as z:
                for name, payload in entries.items():
                    z.writestr(name, payload)
            with self.assertRaisesRegex(ValueError, "integrity"):
                verify_bundle(file)

    def test_incomplete_export_blocks(self):
        value = context()
        value["coverage"]["complete"] = False
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "incomplete context coverage"):
                export_bundle(value, Path(tmp) / "bad.zip")

if __name__ == "__main__":
    unittest.main()
