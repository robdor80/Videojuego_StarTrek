#!/usr/bin/env python3
"""F10/H06-P06-A: comprobaciones PREVIAS de borradores; nunca autoriza alta.

Esta referencia Python no es un validador autoritativo completo. No ejecuta
CoreRPG, no consulta IA y NO puede devolver VALID ni crear una PERSON.
"""
from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
CREATION = ROOT / "sistemas/gameplay/character_creation/character_creation_contract_v1_0.json"
SPECIES = ROOT / "sistemas/gameplay/species/profiles"
CANDIDATE = ROOT / "sistemas/gameplay/careers/academy_path/f10_host_candidate_factory_contract_v0.1.json"
APPROVED_YEAR = 2383
MAX_DRAFT_BYTES = 65536
SPECIES_ID = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _issue(code: str, field: str) -> dict:
    return {"code": code, "field": field}


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def _privileged_nested(value: object, forbidden: set[str], path: str = "") -> list[dict]:
    """No aceptar atributos con apariencia de autoridad escondidos en subobjetos."""
    problems = []
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}" if path else str(key)
            if key in forbidden:
                problems.append(_issue("FORBIDDEN_AUTHORITY_FIELD", child))
            problems.extend(_privileged_nested(item, forbidden, child))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            problems.extend(_privileged_nested(item, forbidden, f"{path}[{i}]"))
    return problems


def evaluate(draft: object, campaign_year: int = APPROVED_YEAR) -> dict:
    """Devuelve CHANGES_REQUIRED o REVIEW_REQUIRED, nunca un permiso de publicación.

    draft_sha256 es *solo* una huella del contenido no confiable. No autentica
    la procedencia ni equivale a validated_creation_ref.
    """
    issues: list[dict] = []
    fingerprint = None
    if type(campaign_year) is not int or campaign_year != APPROVED_YEAR:
        issues.append(_issue("INVALID_CAMPAIGN_CONTEXT", "campaign_year"))

    if not isinstance(draft, dict):
        issues.append(_issue("INVALID_DRAFT", "draft"))
    else:
        try:
            encoded = _canonical(draft)
        except (TypeError, ValueError, RecursionError):
            issues.append(_issue("MALFORMED_FIELD", "draft"))
        else:
            if len(encoded) > MAX_DRAFT_BYTES:
                issues.append(_issue("MALFORMED_FIELD", "draft"))
            else:
                fingerprint = hashlib.sha256(
                    _canonical({"campaign_year": campaign_year, "draft": draft})
                ).hexdigest()

        creation = _read(CREATION)
        candidate = _read(CANDIDATE)
        required = set(creation["required_character_fields"])
        allowed = required | set(creation["optional_character_fields"])
        forbidden = set(candidate["player_input_contract"]["forbidden_client_fields"])
        # Separar la identidad del usuario real de la biografía diegética.
        forbidden |= {"player_profile_id", "nickname", "campaign_refs",
                      "valid", "approved", "authorized", "verified",
                      "is_admin", "semantic_review_approved", "objective_valid"}

        for key in draft:
            if not isinstance(key, str):
                issues.append(_issue("MALFORMED_FIELD", "draft"))
            elif key in forbidden:
                issues.append(_issue("FORBIDDEN_AUTHORITY_FIELD", key))
            elif key not in allowed:
                issues.append(_issue("UNEXPECTED_FIELD", key))

        for key in sorted(required):
            if key not in draft:
                issues.append(_issue("MISSING_REQUIRED_FIELD", key))

        # La estructura completa y las reglas de especie son propiedad de F10.
        # Aqui solo se rechazan formas vacias o no representables.
        for key in sorted(allowed & draft.keys()):
            value = draft[key]
            if value is None or (isinstance(value, str) and not value.strip()) or (
                isinstance(value, (dict, list)) and not value):
                issues.append(_issue("MALFORMED_FIELD", key))

        for key in sorted(allowed & draft.keys()):
            issues.extend(_privileged_nested(draft[key], forbidden, key))

        species = draft.get("species_id")
        if isinstance(species, str) and SPECIES_ID.fullmatch(species):
            path = SPECIES / f"{species}_v0.1.json"
            if not path.is_file() or _read(path).get("species_id") != species:
                issues.append(_issue("UNKNOWN_SPECIES", "species_id"))
        elif "species_id" in draft:
            issues.append(_issue("UNKNOWN_SPECIES", "species_id"))

        adult = draft.get("adult_equivalent_status")
        if adult is False:
            issues.append(_issue("NON_ADULT_DECLARED", "adult_equivalent_status"))
        elif "adult_equivalent_status" in draft and adult is not True:
            issues.append(_issue("MALFORMED_FIELD", "adult_equivalent_status"))
        # Aun con True NO inferir madurez: faltan reglas por especie/contexto.

        age = draft.get("age_or_birth_date")
        if isinstance(age, bool):
            issues.append(_issue("UNSUPPORTED_BIRTH_VALUE", "age_or_birth_date"))
        elif type(age) is int:
            if age < 0:
                issues.append(_issue("UNSUPPORTED_BIRTH_VALUE", "age_or_birth_date"))
        elif isinstance(age, str) and DATE.fullmatch(age):
            try:
                birthday = date.fromisoformat(age)
            except ValueError:
                issues.append(_issue("UNSUPPORTED_BIRTH_VALUE", "age_or_birth_date"))
            else:
                if birthday.year > APPROVED_YEAR:
                    issues.append(_issue("BIRTH_AFTER_CAMPAIGN_YEAR", "age_or_birth_date"))
        elif age is not None:
            issues.append(_issue("UNSUPPORTED_BIRTH_VALUE", "age_or_birth_date"))

        # Solo coherencia temporal obvia de actividades estructuradas, sin
        # pretender evaluar solapamientos profesionales ni duraciones reales.
        activities = draft.get("prior_activities_and_hobbies")
        if isinstance(activities, list):
            for index, entry in enumerate(activities):
                if not isinstance(entry, dict):
                    continue  # pendiente de la semantica de F10
                start, end = entry.get("started_at_or_age"), entry.get("ended_at_or_current")
                path = f"prior_activities_and_hobbies[{index}]"
                if type(start) is int and start < 0:
                    issues.append(_issue("PRIOR_ACTIVITY_AGE_CONFLICT", path))
                if type(end) is int and end < 0:
                    issues.append(_issue("PRIOR_ACTIVITY_AGE_CONFLICT", path))
                if type(start) is int and type(end) is int and start > end:
                    issues.append(_issue("PRIOR_ACTIVITY_AGE_CONFLICT", path))
                if type(age) is int:
                    if type(start) is int and start > age:
                        issues.append(_issue("PRIOR_ACTIVITY_AGE_CONFLICT", path))
                    if type(end) is int and end > age:
                        issues.append(_issue("PRIOR_ACTIVITY_AGE_CONFLICT", path))

    changed = bool(issues)
    if not changed:
        issues += [
            _issue("CONTEXT_NOT_DECIDED", "campaign_month_day"),
            _issue("OBJECTIVE_RULES_NOT_IMPLEMENTED", "objective_validation"),
            _issue("SEMANTIC_REVIEW_PENDING", "semantic_validation"),
        ]
    return {
        "status": "CHANGES_REQUIRED" if changed else "REVIEW_REQUIRED",
        "issues": issues,
        "draft_sha256": fingerprint,
        "objective_gate": "NOT_IMPLEMENTED",
        "semantic_gate": "PENDING",
        "person_created": False,
        "validated_creation_ref": None,
        "effects_applied": False,
        "world_state_mutated": False,
    }
