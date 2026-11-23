#!/usr/bin/env python3
"""ARCHIVO HISTÓRICO A7, sustituido por edad declarada. NO USAR en runtime F10."""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POLICY = ROOT / "sistemas/gameplay/character_creation/f10_individual_maturity_policy_v0.1.json"
SPECIES = ROOT / "sistemas/gameplay/character_creation/f10_species_maturity_policy_v0.1.json"

UNTRUSTED_AUTHORITY_FIELDS = frozenset({
    "person_id", "validated_creation_ref", "admission_authorized", "rank_event_id",
    "authority_grant_id", "internal_issuer_identity", "issuer", "source_identity",
    "adult_stage_attested", "maturity_evidence_approved", "stage_rule_id",
    "semantic_approved", "core_revision", "professional_f11_character_id",
})


def _authority_injected(value: object) -> bool:
    if isinstance(value, dict):
        return any(k in UNTRUSTED_AUTHORITY_FIELDS or _authority_injected(v) for k, v in value.items())
    if isinstance(value, list):
        return any(_authority_injected(x) for x in value)
    return False


def evaluate_reference(draft: dict, *, policy: dict | None = None,
                       species_policy: dict | None = None) -> dict:
    """Solo CHANGES_REQUIRED/REVIEW_REQUIRED; ni reglas de etapa ni autoridad de producto."""
    policy = policy if policy is not None else json.loads(POLICY.read_text(encoding="utf-8"))
    species_policy = species_policy if species_policy is not None else json.loads(SPECIES.read_text(encoding="utf-8"))
    known = {x["species_id"]: x for x in species_policy["species"]}
    issues: list[str] = []
    correction = False

    def add(code: str, *, changes: bool = False) -> None:
        nonlocal correction
        if code not in issues:
            issues.append(code)
        correction |= changes

    if not isinstance(draft, dict):
        return _result("CHANGES_REQUIRED", ["INVALID_DRAFT"])
    if _authority_injected(draft):
        add("FORBIDDEN_AUTHORITY_FIELD", changes=True)

    sid = draft.get("species_id")
    profile = known.get(sid) if isinstance(sid, str) else None
    if profile is None:
        add("UNKNOWN_SPECIES", changes=True)
    else:
        if profile["content_scope"] == "DLC_DELTA":
            add("DLC_DELTA_UNAVAILABLE", changes=True)

    adult_claim = draft.get("adult_equivalent_status")
    if type(adult_claim) is not bool:
        add("MALFORMED_ADULT_STATUS", changes=True)
    elif not adult_claim:
        add("NON_ADULT_DECLARED", changes=True)

    years = draft.get("age_or_birth_date")
    floor = profile["minimum_playable_age_earth_years"] if profile else None
    if floor is None and profile is not None:
        add("SPECIAL_MATURITY_RULE_REQUIRED")
    elif type(years) is int and years >= 0 and floor is not None:
        if years < floor:
            add("BELOW_PLAYABLE_AGE", changes=True)
        if years >= policy["scope"]["campaign_start_year"]:
            add("AGE_OUTSIDE_CALENDAR")
    elif isinstance(years, str) and len(years) == 10 and years[4] == "-" and years[7] == "-":
        try:
            birthday = date.fromisoformat(years)
        except ValueError:
            add("MALFORMED_BIRTH_DATE", changes=True)
        else:
            if birthday.year > policy["scope"]["campaign_start_year"]:
                add("BIRTH_AFTER_CAMPAIGN_YEAR", changes=True)
            elif floor is not None:
                threshold = policy["scope"]["campaign_start_year"] - floor
                if birthday.year > threshold:
                    add("BELOW_PLAYABLE_AGE", changes=True)
                elif birthday.year == threshold:
                    add("PLAYABLE_AGE_UNDECIDED")
    else:
        add("MALFORMED_AGE_OR_BIRTH_DATE", changes=True)

    if profile is not None:
        # Ninguna especie tiene aquí una regla de etapa vital de producto aprobada.
        # Ni el campo adult_equivalent_status ni la apariencia pueden suplirla.
        if not policy["stage_rule_registry"]["entries"]:
            add("MATURITY_EVIDENCE_REQUIRED")
        else:
            add("MATURITY_STAGE_SOURCE_NOT_EVALUATED_OFFLINE")

    return _result("CHANGES_REQUIRED" if correction else "REVIEW_REQUIRED", issues)


def _result(outcome: str, issues: list[str]) -> dict:
    return {
        "outcome": outcome,
        "issue_codes": issues,
        "objective_valid": False,
        "semantic_review_executed": False,
        "individual_maturity_attested": False,
        "person_created": False,
        "cadet_admitted": False,
        "rank_issued": False,
    }


if __name__ == "__main__":
    raise SystemExit("Use python -m unittest discover; A7 no es un validador runtime")
