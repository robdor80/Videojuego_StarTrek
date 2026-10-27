"""F10: historical web provenance must not bypass curriculum parity checks."""
import json
import tempfile
import unittest
from pathlib import Path

from f10_academy_reference import ROOT
from f10_web_parity import check_web_parity


class WebParityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.web_root = Path(self.temp.name)
        curriculum = ROOT / "sistemas/gameplay/careers/academy_path/curriculum"
        game = json.loads((curriculum / "curriculum_manifest_v1_0.json").read_text(encoding="utf-8"))
        self.web = {
            "sourceRepository": "robdor80/Videojuego_StarTrek",
            "sourceManifest": "gameplay/careers/academy_path/curriculum/curriculum_manifest_v1_0.json",
            "years": [],
            "branchLibrary": [],
        }
        for year, web_id in zip(game["years"], ("4-clase", "3-clase", "2-clase", "1-clase")):
            manifest = json.loads((curriculum / year["manifest_ref"]).read_text(encoding="utf-8"))
            subjects = [self.subject("courseId", course_id) for course_id in manifest["course_ids"]]
            self.web["years"].append({
                "id": web_id,
                "trimesters": [{"subjects": subjects[i:i + 5]} for i in range(0, 15, 5)],
            })
        self.web["branchLibrary"] = [self.subject("branchId", branch_id) for branch_id in game["branch_ids"]]

    def subject(self, key, identity):
        subject = {key: identity}
        for field in ("dataFile", "assessmentFile"):
            relative = f"data/{identity}_{field}.json"
            target = self.web_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("{}", encoding="utf-8")
            subject[field] = relative
        return subject

    def check(self):
        (self.web_root / "data/curriculum.json").write_text(json.dumps(self.web), encoding="utf-8")
        return check_web_parity(self.web_root)

    def test_historical_manifest_path_keeps_content_checks(self):
        report = self.check()
        self.assertEqual(report["static_content_parity"], "PASS")
        self.assertEqual((report["course_ids_matched"], report["branch_ids_matched"]), (60, 7))

    def test_reorganized_manifest_path(self):
        self.web["sourceManifest"] = "sistemas/" + self.web["sourceManifest"]
        self.assertEqual(self.check()["static_content_parity"], "PASS")

    def test_unrelated_manifest_is_rejected(self):
        self.web["sourceManifest"] = "other/curriculum_manifest_v1_0.json"
        with self.assertRaisesRegex(ValueError, "no apunta a la fuente"):
            self.check()

    def test_historical_path_does_not_allow_course_drift(self):
        self.web["years"][0]["trimesters"][0]["subjects"][0]["courseId"] = "different-course"
        with self.assertRaisesRegex(ValueError, "Desajuste o reordenación de IDs"):
            self.check()

    def test_historical_path_does_not_allow_branch_drift(self):
        self.web["branchLibrary"][0]["branchId"] = "different-branch"
        with self.assertRaisesRegex(ValueError, "siete ramas web divergen"):
            self.check()

    def test_historical_path_still_requires_published_files(self):
        self.web["years"][0]["trimesters"][0]["subjects"][0]["dataFile"] = "data/missing.json"
        with self.assertRaisesRegex(ValueError, "Archivo publicado no existe"):
            self.check()


if __name__ == "__main__":
    unittest.main()
