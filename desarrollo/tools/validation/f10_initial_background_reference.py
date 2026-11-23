#!/usr/bin/env python3
"""F10 H06-P06-A5: triaje ilustrativo offline; NUNCA emite evidencias o autoridad."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POLICY = ROOT / "sistemas/gameplay/character_creation/f10_initial_background_policy_v0.1.json"
MATURITY = ROOT / "sistemas/gameplay/character_creation/f10_species_maturity_policy_v0.1.json"

# Estos códigos son diagnósticos de referencia, no resultados del validador C++.
RESERVED = frozenset((
    "person_id", "validated_creation_ref", "admission_authorized",
    "authority_grant_id", "rank_event_id", "trusted", "approved",
    "semantic_review_approved", "host_principal", "F05PlayerBinding",
))


def _forbidden_keys(value):
    if isinstance(value, dict):
        return any(key in RESERVED or _forbidden_keys(child) for key, child in value.items())
    if isinstance(value, list):
        return any(_forbidden_keys(item) for item in value)
    return False


def evaluate_reference(scenario: dict, *, policy: dict | None = None,
                       maturity: dict | None = None) -> dict:
    """Nunca devuelve VALID ni OBJECTIVE_VALID; no inspecciona biografía libre con IA."""
    policy = policy if policy is not None else json.loads(POLICY.read_text(encoding="utf-8"))
    maturity = maturity if maturity is not None else json.loads(MATURITY.read_text(encoding="utf-8"))
    classes = {v["code"]: v for v in policy["claim_classes"]}
    species = {v["species_id"]: v for v in maturity["species"]}
    issues = []
    hard = False

    def add(code: str, *, correction: bool = False) -> None:
        nonlocal hard
        if code not in issues:
            issues.append(code)
        if correction:
            hard = True

    if _forbidden_keys(scenario):
        add("FORBIDDEN_AUTHORITY_FIELD", correction=True)
    sid = scenario.get("species_id")
    sp = species.get(sid) if isinstance(sid, str) else None
    if sp is None:
        add("UNKNOWN_SPECIES", correction=True)
    elif sp["content_scope"] == "DLC_DELTA":
        add("DLC_DELTA_UNAVAILABLE", correction=True)
    years = scenario.get("age_years")
    birth_year = scenario.get("birth_year")
    if type(years) is int and years >= 0 and birth_year is None:
        threshold_age = years
    elif type(birth_year) is int and birth_year > 0 and years is None:
        threshold_age = policy["campaign"]["start_year"] - birth_year
        if threshold_age < 0:
            add("BIRTH_AFTER_CAMPAIGN_YEAR", correction=True)
    else:
        threshold_age = None
        add("AGE_CONTEXT_NOT_SUPPORTED")
    if sp is not None:
        minimum = sp["minimum_playable_age_earth_years"]
        if minimum is None:
            add("SPECIAL_MATURITY_RULE_REQUIRED")
        elif threshold_age is not None:
            if threshold_age < minimum:
                add("BELOW_PLAYABLE_AGE", correction=True)
            elif birth_year is not None and threshold_age == minimum:
                add("PLAYABLE_AGE_UNDECIDED")
        add("INDIVIDUAL_MATURITY_EVIDENCE_REQUIRED")
    kind = scenario.get("claim_class")
    claim = classes.get(kind) if isinstance(kind, str) else None
    tier = claim["tier"] if claim else "UNKNOWN_CLAIM"
    if claim is None:
        add("CLAIM_CLASS_NOT_SUPPORTED")
    else:
        start = scenario.get("started_at_age")
        finish = scenario.get("ended_at_age")
        if start is not None and (type(start) is not int or start < 0):
            add("INVALID_ACTIVITY_AGE", correction=True)
        if finish is not None and (type(finish) is not int or finish < 0):
            add("INVALID_ACTIVITY_AGE", correction=True)
        if type(start) is int and type(finish) is int and start > finish:
            add("ACTIVITY_TIME_CONFLICT", correction=True)
        if type(start) is int and threshold_age is not None and start > threshold_age:
            add("ACTIVITY_AFTER_CURRENT_AGE", correction=True)
        if type(finish) is int and threshold_age is not None and finish > threshold_age:
            add("ACTIVITY_AFTER_CURRENT_AGE", correction=True)
        if tier == "PERSONAL_BACKGROUND":
            add("BACKGROUND_INTERNAL_REVIEW_REQUIRED")
        elif tier == "SOURCE_REVIEW":
            add("FORMAL_ATTESTATION_REQUIRED")
        elif tier == "LEGAL_STATUS_REVIEW":
            add("LEGAL_STATUS_SOURCE_REQUIRED")
        elif tier == "SPECIES_RULE_REVIEW":
            add("SPECIES_CAPABILITY_RULE_REQUIRED")
        else:
            add("INSTITUTIONAL_AUTHORITY_REQUIRED")
    return {"outcome": "CHANGES_REQUIRED" if hard else "REVIEW_REQUIRED",
            "tier": tier, "issues": issues, "person_created": False,
            "semantic_review_executed": False, "evidence_issued": False}


if __name__ == "__main__":
    raise SystemExit("F10 A5 reference is a library only; run its unittest suite")
