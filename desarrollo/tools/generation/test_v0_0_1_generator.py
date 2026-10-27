#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "generate_v0_0_1_system.py"
spec = importlib.util.spec_from_file_location("generator", MODULE_PATH)
generator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = generator
spec.loader.exec_module(generator)


class GeneratorTests(unittest.TestCase):
    def context(self, seed: str = "academy_sensor_test_001"):
        return generator.GenerationContext(
            campaign_seed=seed,
            sector_id="041",
            era_id="tng_ds9_voyager",
            campaign_date="2368-01-01",
        )

    def test_same_context_is_identical(self):
        self.assertEqual(
            generator.generate(self.context()),
            generator.generate(self.context()),
        )

    def test_different_seed_changes_world(self):
        a = generator.generate(self.context("academy_sensor_test_001"))
        b = generator.generate(self.context("academy_sensor_test_002"))
        self.assertNotEqual(
            a["generation_context"]["seed_key_hash"],
            b["generation_context"]["seed_key_hash"],
        )
        self.assertNotEqual(a["system"]["system_id"], b["system"]["system_id"])

    def test_profile_validation_passes(self):
        self.assertEqual(generator.validate_v0_0_1(
            generator.generate(self.context())
        ), [])

    def test_profile_validation_across_seed_sample(self):
        for index in range(32):
            payload = generator.generate(self.context(f"sample_{index:02d}"))
            self.assertEqual(
                generator.validate_v0_0_1(payload),
                [],
                msg=f"seed sample_{index:02d}",
            )

    def test_entity_ids_are_unique(self):
        payload = generator.generate(self.context())
        ids = [e["entity_id"] for e in payload["entities"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_anomaly_has_hidden_high_resolution_truth(self):
        payload = generator.generate(self.context())
        anomalies = [e for e in payload["entities"] if e["entity_type"] == "anomaly"]
        self.assertTrue(anomalies)
        self.assertTrue(any(
            any(
                isinstance(value, dict) and value.get("minimum_resolution") == "high"
                for value in anomaly["ground_truth"]["hidden_properties"].values()
            )
            for anomaly in anomalies
        ))

    def test_reference_render_digest_is_locked(self):
        payload = generator.generate(self.context())
        rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        digest = hashlib.sha256(rendered.encode("utf-8")).hexdigest()
        self.assertEqual(
            digest,
            "93910893838ae631ab0e57a8a0409ba14bb405cd7677fcfa04fd3c758cde2f10",
        )


if __name__ == "__main__":
    unittest.main()
