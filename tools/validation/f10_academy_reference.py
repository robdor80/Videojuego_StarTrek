#!/usr/bin/env python3
"""F10: auditoría estática y filtro de PROPUESTAS académicas, sin Core/UE5.

No concede notas, convalidaciones, grados, promociones o destinos.
El argumento trusted_context SOLO puede construirse fuera de este módulo
desde un adaptador Core/Host autenticado. El marcador literal no autentica nada.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACADEMY = ROOT / "gameplay/careers/academy_path"
CURRICULUM = ACADEMY / "curriculum"
ALLOWED_ACTIONS = frozenset({
    "study_progress", "import_study_evidence", "choose_specialization",
    "advance_year", "review_simulation", "confirm_graduation",
    "commission", "assign_first_post"
})
PROPOSAL_FIELDS = frozenset({
    "action", "subject_id", "evidence_ref", "specialization_id", "scenario_id"
})
DECISION_DENY = "DENY"
DECISION_READ = "READ_ONLY"
DECISION_REVIEW = "REQUIRES_CORE_REVIEW"


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Esperado objeto JSON: {path}")
    return value


def audit_sources(root: Path = ROOT) -> dict:
    """Comprueba la coherencia de fuentes locales, sin consultar la web externa."""
    a = root / "gameplay/careers/academy_path"
    c = a / "curriculum"
    manifest = _load(c / "curriculum_manifest_v1_0.json")
    years = _load(a / "academic_year_trimester_model.json")
    structure = _load(a / "curriculum_structure.json")
    special = _load(a / "specializations.json")
    external = _load(a / "external_study_profile_contract.json")
    state = _load(a / "academy_state.json")
    progression = _load(a / "cadet_progression.json")
    graduation = _load(a / "graduation_model.json")
    records = _load(a / "life/academy_record_integration_contract_v0.1.json")
    assignment = _load(a / "first_assignment_model.json")
    simulation = _load(a / "simulation_model.json")
    expected_classes = [
        "cadet_fourth_class", "cadet_third_class",
        "cadet_second_class", "cadet_first_class"
    ]
    ms = manifest["years"]
    if [x["cadet_class_id"] for x in ms] != expected_classes:
        raise ValueError("Secuencia académica del manifiesto incompatible")
    if [x["sequence_year"] for x in structure["years"]] != [1, 2, 3, 4]:
        raise ValueError("Secuencia interna 1-4 incompatible")
    if [x["cadet_class_id"] for x in structure["years"]] != expected_classes:
        raise ValueError("Clases del currículo incompatibles")
    if [x["display_year"] for x in years["sequence"]] != [
        "4th_year", "3rd_year", "2nd_year", "1st_year"
    ]:
        raise ValueError("Años visibles incompatibles")
    if any(x["trimesters"] != 3 for x in years["sequence"]):
        raise ValueError("Debe haber tres trimestres por año")
    if sum(x["course_count"] for x in ms) != 60 or manifest["main_course_components"] != 60:
        raise ValueError("60 asignaturas principales no coinciden")
    if any(x["course_instances"] != 15 for x in structure["years"]):
        raise ValueError("15 asignaturas/año no coinciden")
    if manifest["branch_curricula"] != 7 or special["canonical_specialization_count"] != 7:
        raise ValueError("Número de especializaciones incompatible")
    branch_ids = [x["id"] for x in special["specializations"]]
    if len(branch_ids) != 7 or len(set(branch_ids)) != 7 or set(branch_ids) != set(manifest["branch_ids"]):
        raise ValueError("Identificadores de las 7 ramas no coinciden")
    for year in ms:
        if not (c / year["manifest_ref"]).is_file():
            raise ValueError(f"Manifiesto anual ausente: {year['manifest_ref']}")
    if [x["cadet_class_id"] for x in progression["year_progression"]] != expected_classes:
        raise ValueError("Progresión de clases incompatible")
    if state["lifecycle"][-2:] != ["graduation_pending", "graduated"]:
        raise ValueError("Graduación no separada de la finalización académica")
    if graduation["academy_state_transition"] != {"from": "graduation_pending", "to": "graduated"}:
        raise ValueError("Transición de graduación incompatible")
    if graduation["default_commission_rank"] != "ensign" or assignment["normal_entry_rank"] != "ensign":
        raise ValueError("Rango de ingreso incompatible")
    if records["record_model"] != "append_only_event_log":
        raise ValueError("El expediente debe ser append-only")
    if not {"academy_graduation", "commission", "specialization_selected", "practical_evaluation"}.issubset(
        set(records["recordable_families"])
    ):
        raise ValueError("Faltan familias de expediente")
    if "practice_history" not in external["profile_fields"] or "theory_progress" not in external["profile_fields"]:
        raise ValueError("Perfil externo sin historial de estudio")
    if not any("not automatically authoritative" in s for s in external["rules"]):
        raise ValueError("Falta la prohibición de autoridad automática de la web")
    if simulation["resolution_authority"] != "core_rules_and_world_state":
        raise ValueError("La IA no puede decidir la simulación")
    return {
        "checked": True, "years": 4, "trimesters": 12, "main_courses": 60,
        "specializations": 7, "branch_stages": manifest["branch_stage_components"],
        "designed_units": manifest["unit_design_count"], "external_runtime_checked": False,
        "core_runtime_checked": False, "unreal_checked": False
    }


def _result(decision: str, reason: str) -> dict:
    return {
        "decision": decision,
        "reason": reason,
        "effects_applied": False,
        "world_state_mutated": False,
        "grade_awarded": False,
        "rank_awarded": False,
        "posting_awarded": False,
    }


def _ref(value: object) -> bool:
    return isinstance(value, str) and 0 < len(value) <= 128 and value.strip() == value


def evaluate(proposal: object, trusted_context: object = None) -> dict:
    """Solo filtrado de metadatos. NO comprueba criptográficamente la procedencia Core."""
    deny = lambda reason: _result(DECISION_DENY, reason)
    if not isinstance(proposal, dict) or set(proposal) - PROPOSAL_FIELDS:
        return deny("campos_de_propuesta_prohibidos")
    action = proposal.get("action")
    if not isinstance(action, str) or action not in ALLOWED_ACTIONS:
        return deny("accion_desconocida")
    required_fields = {
        "study_progress": {"subject_id"}, "import_study_evidence": {"evidence_ref"},
        "choose_specialization": {"specialization_id"}, "advance_year": {"evidence_ref"},
        "review_simulation": {"scenario_id", "evidence_ref"},
        "confirm_graduation": {"evidence_ref"}, "commission": {"evidence_ref"},
        "assign_first_post": {"evidence_ref"}
    }
    permitted_fields = required_fields[action] | {"action"}
    if set(proposal) != permitted_fields:
        return deny("campos_de_accion_incorrectos")
    if not all(_ref(proposal[k]) for k in required_fields[action]):
        return deny("referencia_invalida")
    if action == "study_progress":
        return _result(DECISION_READ, "estudio_externo_sin_efectos_en_partida")
    if not isinstance(trusted_context, dict) or trusted_context.get("trusted_origin") != "CORE_HOST_VERIFIED":
        return deny("contexto_core_host_no_verificado")
    if not _ref(trusted_context.get("character_ref")):
        return deny("identidad_de_personaje_no_verificada")
    year = trusted_context.get("academic_year")
    if type(year) is not int or year not in (1, 2, 3, 4):
        return deny("curso_actual_invalido")
    status = trusted_context.get("academy_status")
    valid_statuses = {
        "cadet_year_1", "cadet_year_2", "cadet_year_3", "cadet_year_4",
        "graduation_pending", "graduated"
    }
    if status not in valid_statuses:
        return deny("estado_academico_invalido")
    if status.startswith("cadet_year_") and status != f"cadet_year_{year}":
        return deny("incoherencia_curso_estado")
    known = trusted_context.get("known_evidence_refs")
    if not isinstance(known, list) or not all(_ref(r) for r in known) or len(known) != len(set(known)):
        return deny("evidencias_core_no_validas")
    if action not in {"choose_specialization"} and proposal.get("evidence_ref") not in known:
        return deny("evidencia_no_conocida_por_core")
    review = lambda reason: _result(DECISION_REVIEW, reason)
    if action == "import_study_evidence":
        return review("importacion_externa_necesita_verificacion_sin_nota_automatica")
    if action == "choose_specialization":
        spec = _load(ACADEMY / "specializations.json")
        ids = {s["id"] for s in spec["specializations"]}
        if proposal["specialization_id"] not in ids:
            return deny("especializacion_no_canonica")
        if year != 2 or status != "cadet_year_2":
            return deny("fuera_ventana_de_especializacion")
        if trusted_context.get("selection_window_open") is not True or trusted_context.get("explicit_player_choice") is not True:
            return deny("eleccion_jugador_no_confirmada")
        return review("eleccion_requiere_evento_autoritativo_de_core")
    if action == "advance_year":
        if status != f"cadet_year_{year}" or year == 4:
            return deny("progresion_directa_no_admitida")
        if trusted_context.get("authorized_academic_review") is not True or trusted_context.get("period_complete") is not True:
            return deny("revision_o_periodo_no_acreditados")
        if year == 2 and (
            trusted_context.get("selected_specialization") not in {s["id"] for s in _load(ACADEMY / "specializations.json")["specializations"]}
            or trusted_context.get("explicit_player_choice") is not True
        ):
            return deny("especializacion_jugador_pendiente")
        return review("core_debe_resolver_resultado_y_transicion")
    if action == "review_simulation":
        if proposal["scenario_id"] not in {"kobayashi_maru", "sensors_training"}:
            return deny("simulacion_no_catalogada")
        if trusted_context.get("simulation_resolved_in_core") is not True:
            return deny("simulacion_sin_resultado_autoritativo")
        return review("debrief_no_sustituye_evaluacion_core")
    if action == "confirm_graduation":
        if (year != 4 or status != "graduation_pending" or
                trusted_context.get("graduation_eligible") is not True or
                trusted_context.get("authorized_academic_review") is not True):
            return deny("graduacion_no_acreditada")
        return review("graduacion_confirmable_solo_por_core")
    if action == "commission":
        if status != "graduated" or trusted_context.get("commission_authorized") is not True:
            return deny("comision_no_autorizada")
        if trusted_context.get("confirmed_graduation_event_ref") != proposal["evidence_ref"]:
            return deny("graduacion_no_confirmada_para_comision")
        return review("rango_alferez_solo_mediante_evento_core")
    if action == "assign_first_post":
        if (status != "graduated" or trusted_context.get("commission_confirmed") is not True or
                trusted_context.get("posting_authorized") is not True or
                trusted_context.get("vacancy_confirmed") is not True):
            return deny("destino_sin_comision_orden_o_vacante")
        return review("destino_solo_mediante_orden_y_vacante_core")
    return deny("estado_no_contemplado")


def main() -> int:
    print(json.dumps(audit_sources(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
