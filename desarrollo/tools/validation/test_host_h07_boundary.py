#!/usr/bin/env python3
"""H07: comprobaciones ESTÁTICAS de frontera y planificación.

No llama a CoreRPG, no ejecuta Unreal, no emite hechos institucionales.
Los resultados requieren evidencia trazada; esta suite estática NO los ejecuta.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "proyecto/docs/architecture/host"
HOST = ROOT / "desarrollo/integration/host"
F11 = ROOT / "desarrollo/integration/f11"
F11_READER = ROOT / "desarrollo/integration/f11_host"
MATRIX = DOCS / "H07_P04_MATRIZ_ACEPTACION_v0.1_2026-11-23.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class HostH07BoundaryStaticTests(unittest.TestCase):
    def test_matrix_has_unique_traceable_cases(self) -> None:
        matrix = json.loads(read(MATRIX))
        host = matrix["host_cases"]
        external = matrix["external_f11_reference"]["cases"]
        self.assertEqual(matrix["maturity"], "TECHNICAL_EVIDENCE_NOT_CERTIFIED")
        self.assertEqual(matrix["overall_status"], "PARTIAL_TECHNICAL_EVIDENCE")
        self.assertEqual(len(host), 27)
        self.assertEqual(len(external), 33)
        self.assertEqual(len({case["id"] for case in host}), 27)
        self.assertEqual(len({case["id"] for case in external}), 33)
        self.assertTrue(all(case["status"] == "NOT_RUN" for case in external))
        for case in host:
            self.assertIn(case["status"], matrix["status_legend"])
            if case["status"] == "PASS":
                evidence = case["evidence"]
                self.assertRegex(evidence["source_sha"], r"^[0-9a-f]{40}$")
                self.assertRegex(evidence["sha256"], r"^[0-9a-f]{64}$")
                self.assertTrue(evidence["artifact"])
                self.assertTrue((DOCS / evidence["report"]).is_file())
        self.assertEqual(matrix["external_f11_reference"]["state"], "DRAFT_NOT_MERGED")
        self.assertTrue(matrix["external_f11_reference"]["not_host_tests"])

    def test_external_matrix_maps_to_valid_host_scenarios(self) -> None:
        matrix = json.loads(read(MATRIX))
        host_ids = {case["id"] for case in matrix["host_cases"]}
        cases = matrix["external_f11_reference"]["cases"]
        self.assertEqual(
            {case["gate"] for case in cases},
            {f"HOST_{index:02d}" for index in range(1, 8)},
        )
        for case in cases:
            self.assertEqual(case["owner"], "F11 (external to H07)")
            self.assertTrue(set(case["h07_related_cases"]) <= host_ids)

    def test_contract_does_not_claim_product_issuer(self) -> None:
        plan = read(DOCS / "H07_P01_AUDITORIA_PLAN_2026-11-23.md")
        contract = read(DOCS / "H07_P01_CONTRATO_FRONTERA_v0.1_2026-11-23.md")
        self.assertIn("H07-P01", plan)
        self.assertIn("H07-P05", plan)
        self.assertIn("SERVICE_UNAVAILABLE", contract)
        self.assertIn("F11_NATIVE_TEST_HOST", contract)
        self.assertIn("AcademyCampaign", contract)
        self.assertIn("NO es una API ya implementada", contract)

    def test_host_has_no_product_trial_linkage(self) -> None:
        cmake = read(HOST / "CMakeLists.txt")
        # The reference to a trial target in a negative guard is legitimate.
        self.assertIn("OR TARGET TrekF11TrialHost", cmake)
        for match in re.finditer(
            r"target_link_libraries\(TrekHost\s+(.*?)\)",
            cmake, flags=re.DOTALL,
        ):
            self.assertNotIn("TrekF11TrialHost", match.group(1))
        self.assertNotIn("add_subdirectory(../f11_host", cmake)

    def test_trial_issuer_compiled_only_under_private_macro(self) -> None:
        bridge = read(ROOT / "desarrollo/integration/f04/src/f04_bridge.cpp")
        self.assertRegex(
            bridge,
            r"#ifdef F11_NATIVE_TEST_HOST\s*#include \"f11_trial_host.inc\"\s*#endif",
        )
        trials = read(F11 / "CMakeLists.txt")
        self.assertIn("F11_NATIVE_TEST_HOST=1", trials)
        self.assertIn("add_library(TrekF11TrialHost", trials)

    def test_reader_remains_a_read_only_adapter(self) -> None:
        reader = read(F11_READER / "src/f11_host_reader.cpp")
        self.assertIn("f11_personnel(", reader)
        self.assertIn("f11_promotion(", reader)
        self.assertNotIn("f11_commit_promotion(", reader)
        self.assertNotIn("f11_bootstrap_authorized_trial", reader)

    def test_unavailable_dispatch_guard_is_before_bridge(self) -> None:
        native = read(HOST / "src/native_session.cpp")
        start = native.index("Outcome NativeSession::dispatch(")
        tail = native[start: start + 1000]
        guard = tail.index("request.operation == GatewayOp::INSTITUTIONAL")
        forward = tail.index("bridge::dispatch(")
        self.assertLess(guard, forward)
        self.assertIn("Error::SERVICE_UNAVAILABLE", tail[guard:forward])

    def test_existing_host_abi_cannot_mint_institutional_authority(self) -> None:
        abi = read(HOST / "include/trek/host/host_abi.h")
        self.assertNotIn("TREK_HOST_INSTITUTIONAL_COMMAND", abi)
        self.assertNotIn("TREK_HOST_CREATE_GRANT", abi)
        self.assertNotIn("TREK_HOST_COMMIT_PROMOTION", abi)


if __name__ == "__main__":
    unittest.main(verbosity=2)
