#!/usr/bin/env python3
"""CI de gobierno de fases F00-F15. Solo JSON/Markdown; NO ejecuta Core/UE5."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MASTER = ROOT / 'proyecto/docs' / "roadmap" / "master"
STATE = MASTER / "ESTADO_GLOBAL.json"
PLAN = MASTER / "PLAN_MAESTRO.md"
ALLOWED_STATUS = {
    "PLANIFICADA", "EN_CURSO", "EN_REVISION", "BLOQUEADA",
    "CERRADA", "DESCARTADA_CON_MOTIVO",
}
ALLOWED_MATURITY = {
    "DOCUMENTACION_AUDITADA", "IDEA", "DISENO_VALIDADO",
    "CONTRATO_VALIDADO", "REFERENCIA_PROBADA",
    "CORE_INTEGRADO", "UE5_JUGABLE", "ACEPTACION_SUPERADA",
}
EXPECTED_STATUS = {
    "F00": "CERRADA", "F01": "CERRADA", "F02": "EN_CURSO",
    "F03": "EN_REVISION", "F04": "EN_REVISION",
    "F05": "EN_REVISION", "F06": "EN_REVISION",
}
EXPECTED_MATURITY = {
    "F00": "DOCUMENTACION_AUDITADA", "F01": "DISENO_VALIDADO",
    "F02": "DISENO_VALIDADO", "F03": "REFERENCIA_PROBADA",
    "F04": "REFERENCIA_PROBADA", "F05": "REFERENCIA_PROBADA",
    "F06": "REFERENCIA_PROBADA",
}


def check() -> list[str]:
    errors: list[str] = []
    state = json.loads(STATE.read_text(encoding="utf-8"))
    plan = PLAN.read_text(encoding="utf-8")
    phases = state.get("phases", [])
    expected_ids = [f"F{i:02d}" for i in range(16)]
    ids = [p.get("id") for p in phases]
    if ids != expected_ids:
        errors.append("16 fases consecutivas F00–F15 faltan, sobran o están desordenadas")
    if state.get("phase_count") != 16 or len(phases) != 16:
        errors.append("phase_count / longitud de phases != 16")
    if state.get("step_count") != 80:
        errors.append("step_count != 80")
    if sum(p.get("step_count", 0) for p in phases) != 80:
        errors.append("suma step_count por fases != 80")

    active = [p.get("id") for p in phases if p.get("status") == "EN_CURSO"]
    current = state.get("current_global_phase")
    if active != [current]:
        errors.append(f"única fase principal: actual {current!r}, EN_CURSO={active!r}")
    if state.get("completed_management_phase") != "F01":
        errors.append("completed_management_phase != F01")

    pr = state.get("governance_review", {})
    if pr.get("merged_prs") != [2, 3, 4, 5, 6, 7]:
        errors.append("registro de PR fusionadas no corresponde a corte F01-F06")
    if not pr.get("source_main_commit"):
        errors.append("falta SHA de línea base en governance_review")

    for p in phases:
        phase_id = p.get("id", "")
        status = p.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{phase_id}: estado {status!r} no admitido")
        steps = p.get("steps", {})
        expected_steps = [f"P{i:02d}" for i in range(1, 6)]
        if list(steps) != expected_steps or p.get("step_count") != 5:
            errors.append(f"{phase_id}: cinco pasos P01-P05 obligatorios")
        if any(v not in ALLOWED_STATUS for v in steps.values()):
            errors.append(f"{phase_id}: paso con estado inválido")
        if status == "CERRADA" and any(v != "CERRADA" for v in steps.values()):
            errors.append(f"{phase_id}: fase cerrada con pasos no cerrados")
        if p.get("target_maturity") not in ALLOWED_MATURITY:
            errors.append(f"{phase_id}: madurez objetivo no admitida")
        filepath = MASTER / p.get("file", "")
        if not filepath.is_file():
            errors.append(f"{phase_id}: README inexistente ({filepath})")

        # El plan es presentación legible y no puede falsear el registro oficial.
        pat = rf"^\| \[{re.escape(phase_id)}\]\(fases/{re.escape(phase_id)}/README\.md\) \|[^|]*\|([^|]*)\|"
        match = re.search(pat, plan, flags=re.MULTILINE)
        if not match:
            errors.append(f"{phase_id}: no figura en tabla del plan maestro")
        elif status not in match.group(1):
            errors.append(f"{phase_id}: plan maestro no refleja estado {status}")

        if phase_id in EXPECTED_STATUS:
            if status != EXPECTED_STATUS[phase_id]:
                errors.append(f"{phase_id}: estado distinto del corte documentado")
            if p.get("achieved_maturity") != EXPECTED_MATURITY[phase_id]:
                errors.append(f"{phase_id}: madurez acreditada distinta de corte")
        if phase_id in EXPECTED_STATUS and phase_id != "F00":
            levels = p.get("step_evidence_maturity", {})
            if list(levels) != expected_steps:
                errors.append(f"{phase_id}: faltan niveles por paso")
            elif any(level not in ALLOWED_MATURITY for level in levels.values()):
                errors.append(f"{phase_id}: nivel por paso no admitido")
            if not p.get("evidence_refs"):
                errors.append(f"{phase_id}: faltan referencias de evidencia")
            if status != "CERRADA" and not p.get("note"):
                errors.append(f"{phase_id}: hay trabajo abierto sin puertas registradas")

    for doc in (
        MASTER / "ACTA_RECONCILIACION_F00_F06_2026-10-13.md",
        MASTER / "fases/F01/ACTA_CIERRE_DOCUMENTAL_F01_2026-10-13.md",
        MASTER / "fases/F01/ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md",
        ROOT / "desarrollo/tools/simulation/test_f04_f05_f06_cross_phase.py",
    ):
        if not doc.is_file():
            errors.append(f"evidencia/artefacto ausente: {doc.relative_to(ROOT)}")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        raise SystemExit(1)
    print("PASS: F00-F15 (16 fases, 80 pasos), F01 cierre de diseño, "
          "F02 principal y F03-F06 en revisión; plan sincronizado. "
          "Esto NO valida Core RPG ni UE5.")
