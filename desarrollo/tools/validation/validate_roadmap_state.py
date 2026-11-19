#!/usr/bin/env python3
"""Gobierno verificable F00–F15; no certifica CoreRPG, Unreal ni CI externa.

El JSON contiene una fotografía versionada. Las pruebas de runtime se acreditan
por evidencias/actas y NO se deducen del número de PR o del estado administrativo.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MASTER = ROOT / "proyecto/docs/roadmap/master"
STATE = MASTER / "ESTADO_GLOBAL.json"
PLAN = MASTER / "PLAN_MAESTRO.md"

ALLOWED_STATUS = frozenset({
    "PLANIFICADA", "EN_CURSO", "EN_REVISION", "BLOQUEADA",
    "CERRADA", "DESCARTADA_CON_MOTIVO",
})
ALLOWED_MATURITY = frozenset({
    "IDEA", "DOCUMENTACION_AUDITADA", "DISENO_VALIDADO", "CONTRATO_VALIDADO",
    "REFERENCIA_PROBADA", "CORE_INTEGRADO", "UE5_JUGABLE",
    "ACEPTACION_SUPERADA",
})
ALLOWED_PR_STATUS = frozenset({"FUSIONADA", "DRAFT", "ABIERTA", "CERRADA_SIN_MERGE"})
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
PHASE_IDS = [f"F{i:02d}" for i in range(16)]
STEP_IDS = [f"P{i:02d}" for i in range(1, 6)]


def _is_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate(state: dict, plan: str, root: Path = ROOT) -> list[str]:
    """Invariantes estables: admite evolución de fases sin editar el script."""
    errors: list[str] = []
    phases = state.get("phases")
    if not isinstance(phases, list):
        return ["phases debe ser una lista"]
    if state.get("schema_version") != "1.1.0":
        errors.append("schema_version: se requiere registro de gobierno 1.1.0")
    if not _is_date(state.get("date")):
        errors.append("date: fecha ISO inválida")
    ids = [p.get("id") for p in phases]
    if ids != PHASE_IDS or state.get("phase_count") != 16:
        errors.append("se exigen exactamente F00-F15 consecutivas y phase_count=16")
    if state.get("step_count") != 80 or sum(p.get("step_count", 0) for p in phases) != 80:
        errors.append("se exigen exactamente 80 pasos")
    by_id = {p.get("id"): p for p in phases}
    current = state.get("current_global_phase")
    if current not in by_id or by_id[current].get("status") in {"CERRADA", "DESCARTADA_CON_MOTIVO"}:
        errors.append("current_global_phase debe apuntar a un frente de trabajo abierto")
    # No prohibimos trabajo paralelo; el foco global es solo una prioridad.
    contiguous = None
    for p in phases:
        if p.get("status") == "CERRADA":
            if contiguous is not None or p.get("id") == "F00":
                contiguous = p.get("id")
        else:
            break
    if state.get("completed_management_phase") != contiguous:
        errors.append(f"completed_management_phase no coincide con el prefijo cerrado ({contiguous})")

    master = root / "proyecto/docs/roadmap/master"
    for p in phases:
        phase = p.get("id", "?")
        status = p.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{phase}: estado de fase inválido")
        steps = p.get("steps")
        if p.get("step_count") != 5 or not isinstance(steps, dict) or list(steps) != STEP_IDS:
            errors.append(f"{phase}: cinco pasos ordenados P01-P05 obligatorios")
            continue
        if any(v not in ALLOWED_STATUS for v in steps.values()):
            errors.append(f"{phase}: estado de paso inválido")
        if status == "CERRADA" and any(v != "CERRADA" for v in steps.values()):
            errors.append(f"{phase}: fase cerrada con pasos abiertos")
        if p.get("target_maturity") not in ALLOWED_MATURITY:
            errors.append(f"{phase}: madurez objetivo inválida")
        achieved = p.get("achieved_maturity")
        if achieved is not None and achieved not in ALLOWED_MATURITY:
            errors.append(f"{phase}: madurez demostrada inválida")
        levels = p.get("step_evidence_maturity", {})
        if levels:
            if not isinstance(levels, dict) or list(levels) != STEP_IDS:
                errors.append(f"{phase}: madurez por paso requiere P01-P05")
            elif any(level not in ALLOWED_MATURITY for level in levels.values()):
                errors.append(f"{phase}: madurez por paso inválida")
        if achieved and not p.get("evidence_refs"):
            errors.append(f"{phase}: madurez acreditada sin referencias")
        if status == "CERRADA":
            closure = p.get("closure")
            if not isinstance(closure, dict) or not _is_date(closure.get("date")) or not closure.get("scope") or not closure.get("evidence_refs"):
                errors.append(f"{phase}: CERRADA sin acta, alcance, fecha y evidencia")
            if achieved != p.get("target_maturity"):
                errors.append(f"{phase}: cierre no acreditado en la meta de su alcance")
            if not levels or any(v is None for v in levels.values()):
                errors.append(f"{phase}: cierre sin nivel explícito por paso")
        if achieved in {"UE5_JUGABLE", "ACEPTACION_SUPERADA"}:
            proof = p.get("runtime_acceptance", {})
            if not isinstance(proof, dict) or not all(proof.get(x) for x in ("environment", "build_sha", "run_url", "acceptance_record")):
                errors.append(f"{phase}: UE5/aceptación sin build, ejecución MSI y acta")
        relative = p.get("file")
        if not isinstance(relative, str) or relative != f"fases/{phase}/README.md":
            errors.append(f"{phase}: ruta README no canónica")
        elif not (master / relative).is_file():
            errors.append(f"{phase}: falta README")
        match = re.search(
            rf"^\|\s*\[{re.escape(phase)}\]\(fases/{re.escape(phase)}/README\.md\)\s*\|[^|]*\|([^|]*)\|",
            plan, re.MULTILINE,
        )
        if not match or not re.search(rf"\b{re.escape(str(status))}\b", match.group(1)):
            errors.append(f"{phase}: tabla de PLAN_MAESTRO no concuerda con JSON")
        if status == "DESCARTADA_CON_MOTIVO" and not p.get("note"):
            errors.append(f"{phase}: descartada sin motivación")

    prs = state.get("tracked_pull_requests")
    if not isinstance(prs, list) or not prs:
        errors.append("falta seguimiento verificable de PR")
    else:
        seen = set()
        for pr in prs:
            n = pr.get("number")
            if not isinstance(n, int) or n <= 0 or n in seen:
                errors.append(f"PR #{n}: número duplicado o inválido")
            seen.add(n)
            if pr.get("phase") not in by_id:
                errors.append(f"PR #{n}: fase propietaria inválida")
            status = pr.get("status")
            if status not in ALLOWED_PR_STATUS:
                errors.append(f"PR #{n}: estado inválido")
            if not SHA_PATTERN.fullmatch(str(pr.get("head_sha", ""))):
                errors.append(f"PR #{n}: sin SHA exacto de HEAD")
            merge_sha = pr.get("merge_commit_sha")
            merged_at = pr.get("merged_at")
            if status == "FUSIONADA":
                if not SHA_PATTERN.fullmatch(str(merge_sha or "")) or not _is_date(merged_at):
                    errors.append(f"PR #{n}: declarada fusionada sin merge SHA y fecha")
            elif merge_sha or merged_at:
                errors.append(f"PR #{n}: borrador/abierta no puede atribuirse merge")
    # El archivo governance_review es HISTÓRICO: jamás se usa como whitelist de PR.
    review = state.get("governance_review", {})
    if not review.get("source_main_commit") or not review.get("merged_prs"):
        errors.append("se ha perdido la evidencia histórica de gobierno")
    return errors


def check() -> list[str]:
    return validate(json.loads(STATE.read_text(encoding="utf-8")), PLAN.read_text(encoding="utf-8"), ROOT)


if __name__ == "__main__":
    problems = check()
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        raise SystemExit(1)
    print("PASS gobierno F00-F15: 16 fases, 80 pasos, cierres con evidencia, "
          "PR versionadas y PLAN sincronizado. NO certifica Core/UE5/jugabilidad.")
