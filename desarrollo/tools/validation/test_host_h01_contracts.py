#!/usr/bin/env python3
"""H01 documentary contract checks; no HOST runtime or Core modifications."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "proyecto/docs/architecture/host"
REGISTRY = DOCS / "H01_REGISTRO_CONTRATOS_v1.json"

DOC_NAMES = (
    "H01_P01_ARQUITECTURA_v1.0_2026-11-11.md",
    "H01_P02_CONTRATOS_v1.0_2026-11-11.md",
    "H01_P03_CONFIANZA_v1.0_2026-11-11.md",
    "H01_P04_COMPATIBILIDAD_v1.0_2026-11-11.md",
    "H01_MATRIZ_CONFORMIDAD_v1.0_2026-11-11.md",
    "H01_ACTA_2026-11-11.md",
)
EXPECTED_OPS = {
    "OPEN_CAMPAIGN", "CLOSE_CAMPAIGN", "RESOLVE_PRINCIPAL", "QUERY_VIEW",
    "F04_COMMAND", "F05_SUBMIT_ORDER", "F05_RECEIVE_ORDER",
    "F05_EXECUTE_ORDER", "F05_CANCEL_ORDER", "ADVANCE_CAMPAIGN",
    "SAVE_SLOT", "RESTORE_SLOT", "F11_READ_PERSONNEL",
    "F11_INSTITUTIONAL_COMMAND", "SUBSCRIBE_EVENTS",
}
EXPECTED_ERRORS = {
    "INVALID_ARGUMENT", "SESSION_CLOSED", "BUSY_STATE", "WRONG_THREAD",
    "GENERATION_EXPIRED", "PRINCIPAL_UNBOUND", "ACCESS_DENIED",
    "SCOPE_INVALID", "REVISION_STALE", "DOMAIN_REJECTED",
    "IDEMPOTENCY_CONFLICT", "CAPACITY_LIMIT", "SAVE_INCOMPATIBLE",
    "SAVE_UNTRUSTED", "PERSISTENCE_FAILED", "SERVICE_UNAVAILABLE",
    "INTERNAL_ERROR",
}
PIN_FILES = {
    "F03": "desarrollo/integration/f03/core-revision.txt",
    "F04": "desarrollo/integration/f04/core-revision.txt",
    "F04_HISTORY": "desarrollo/integration/f04/core-history-revision.txt",
    "F05_F11": "desarrollo/integration/f05/core-revision.txt",
}
HEADERS = (
    "desarrollo/integration/f04/include/f04_bridge.h",
    "desarrollo/integration/f05/include/f05_orders.h",
    "desarrollo/integration/f05/include/f05_initiative.h",
    "desarrollo/integration/f11_host/include/f11_host_reader.h",
)


class ContractDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.docs = {n: (DOCS / n).read_text(encoding="utf-8") for n in DOC_NAMES}

    def test_version_scope_and_maturity(self):
        r = self.registry
        self.assertEqual(r["spec_version"], "1.0")
        self.assertEqual(r["scope"], "offline-single-player")
        self.assertEqual(r["status"], "DESIGNED_NOT_RUNTIME")
        self.assertIs(r["runtime_available"], False)
        self.assertEqual(r["core_authority"], "CoreRPG")
        self.assertNotEqual(r["institutional_authority"], "HOST")

    def test_operations_unique_complete_and_owners(self):
        ops = self.registry["operations"]
        names = [o["name"] for o in ops]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), EXPECTED_OPS)
        self.assertEqual({o["owner"] for o in ops}, {"HOST", "F04", "F05", "F11"})
        for op in ops:
            self.assertIn(op["kind"], {"read", "mutation", "lifecycle", "persistence", "unavailable"})
            self.assertIsInstance(op["requires_revision"], bool)

    def test_f11_is_private_and_unavailable(self):
        r = self.registry
        issuer = next(x for x in r["operations"] if x["name"] == "F11_INSTITUTIONAL_COMMAND")
        self.assertEqual(issuer["owner"], "F11")
        self.assertEqual(issuer["kind"], "unavailable")
        self.assertIsNone(issuer["existing_api"])
        self.assertIs(r["trust_policy"]["trial_issuer_in_product"], False)
        self.assertIs(r["trust_policy"]["privileged_f11_issuer_available"], False)
        for op in r["operations"]:
            self.assertNotIn("f11_trial_host", op["existing_api"] or "")
            self.assertNotIn("TrekF11TrialHost", op["existing_api"] or "")

    def test_common_messages_and_error_catalogue(self):
        r = self.registry
        self.assertEqual(set(r["message_required"]), {
            "host_contract", "session_generation", "correlation_id", "operation"
        })
        self.assertEqual(len(r["errors"]), len(set(r["errors"])))
        self.assertEqual(set(r["errors"]), EXPECTED_ERRORS)
        self.assertIn("expected_core_revision resolved in domain", r["mutation_constraints"])
        self.assertIn("no automatic mutation retry", r["mutation_constraints"])

    def test_one_session_generation_and_provenance(self):
        r = self.registry
        self.assertEqual(r["session_model"]["max_active"], 1)
        self.assertIs(r["session_model"]["owner_thread_only"], True)
        self.assertIs(r["session_model"]["rebind_on_restore"], True)
        self.assertIs(r["session_model"]["generation_ephemeral"], True)
        self.assertTrue({"CLOSED", "ACTIVE", "SAVING", "LOADING", "CLOSING"}.issubset(
            r["session_model"]["states"]
        ))
        self.assertEqual(set(r["provenance_classes"]), {
            "CREATED_LOCALLY", "KNOWN_LOCAL", "IMPORTED_UNVERIFIED", "REJECTED"
        })
        self.assertIs(r["trust_policy"]["checksum_is_authentication"], False)
        self.assertIs(r["trust_policy"]["f04ref_is_credential"], False)

    def test_cases_unique_and_documented(self):
        identifiers = self.registry["contract_case_ids"]
        self.assertEqual(identifiers, [f"HC-{i:02d}" for i in range(1, 36)])
        matrix = self.docs[DOC_NAMES[4]]
        rows = re.findall(r"^\|\s*(HC-\d{2})\s*\|", matrix, flags=re.MULTILINE)
        self.assertEqual(rows, identifiers)

    def test_documents_are_explicitly_design_only(self):
        for name, content in self.docs.items():
            with self.subTest(document=name):
                self.assertGreater(len(content), 1200)
                self.assertIn("H01", content)
                self.assertRegex(content, r"(?i)no implementad|no ejecutad|no probado|no runtime|diseñ[oa]")

    def test_pins_match_checked_in_files(self):
        pins = self.registry["historical_core_pins"]
        self.assertEqual(self.registry["candidate_core_pin"], pins["F05_F11"])
        for key, filename in PIN_FILES.items():
            self.assertEqual((ROOT / filename).read_text(encoding="utf-8").strip(), pins[key])
        f02 = (ROOT / "desarrollo/integration/f02/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn(pins["F02"], f02)

    def test_existing_api_references_are_real_symbols(self):
        joined = "\n".join((ROOT / p).read_text(encoding="utf-8") for p in HEADERS)
        for op in self.registry["operations"]:
            for full_name in (op["existing_api"] or "").split(";"):
                if not full_name:
                    continue
                symbol = full_name.rsplit("::", 1)[-1]
                with self.subTest(op=op["name"], symbol=symbol):
                    self.assertRegex(joined, r"\b" + re.escape(symbol) + r"\s*\(")

    def test_f05_f11_cmake_boundary(self):
        f04 = (ROOT / "desarrollo/integration/f04/CMakeLists.txt").read_text(encoding="utf-8")
        f05 = (ROOT / "desarrollo/integration/f05/CMakeLists.txt").read_text(encoding="utf-8")
        f11 = (ROOT / "desarrollo/integration/f11/CMakeLists.txt").read_text(encoding="utf-8")
        reader = (ROOT / "desarrollo/integration/f11_host/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("F05_ENABLE_ORDERS", f04)
        self.assertIn("F11_ENABLE_PROMOTIONS", f04)
        self.assertIn("add_subdirectory(../f04", f05)
        self.assertIn("TrekF11TrialHost", f11)  # EXISTING TEST fixture only
        self.assertIn("TrekF11HostReader", reader)
        self.assertIn("TrekF04Bridge", reader)

    def test_no_mislabelled_executable_proof(self):
        self.assertIn("NO EJECUTADOS", self.docs[DOC_NAMES[4]])
        self.assertIn("F11", self.docs[DOC_NAMES[2]])
        self.assertIn("f04_history_export_active", self.docs[DOC_NAMES[3]].lower())
        self.assertIn("H02", self.docs[DOC_NAMES[0]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
