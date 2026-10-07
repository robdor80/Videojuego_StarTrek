#!/usr/bin/env python3
"""Deterministic reference generator for causal Star Trek facilities.

This tool demonstrates content/rules behavior. It is not the future authoritative
runtime; CoreRPG remains responsible for live persistent World State.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

DESIGNS = ROOT / "lore/stations_and_facilities/canonical_station_design_catalogue_v0.1.json"
GRAMMAR = ROOT / "universe/generation/procedural_station_design_grammar_v0.1.json"
POLICY = ROOT / "universe/generation/procedural_facility_reference_policy_v0.1.json"
EXISTENCE = ROOT / "universe/generation/facility_existence_and_construction_causality_v0.1.json"
STAFFING = ROOT / "universe/generation/facility_staffing_population_guidance_v0.1.json"
LIFE = ROOT / "lore/stations_and_facilities/station_life_profiles_v0.1.json"

GENERATOR_ID = "procedural_facility_reference_generator"
GENERATOR_VERSION = "0.1.0"

OPERATOR_MAP = {
    "starfleet": "starfleet",
    "federation_civil": "federation_civil",
    "klingon": "klingon_imperial_military",
    "cardassian": "cardassian_military",
    "dominion": "dominion",
    "bajoran": "bajoran",
    "ferengi": "ferengi_alliance",
    "romulan": "romulan_military",
    "civilian": "civilian",
}

ROLE_TAGS = {
    "communications_relay": {"subspace_communications_relay"},
    "sensor_listening_outpost": {"border_monitoring", "science_support"},
    "research_observatory": {"scientific_research", "classified_research", "remote_laboratory", "research"},
    "medical_quarantine": {"medical_regional_support"},
    "depot_supply": {"regional_starship_support", "fleet_support", "storage", "resupply"},
    "trade_cargo_transfer": {"regional_hub", "trade_and_social_services", "cargo_transfer", "orbital_docking"},
    "orbital_habitat": {"habitation"},
    "refinery_processing": {"deuterium_refinery", "ore_processing", "industrial_processing"},
    "repair_drydock": {"construction", "refit", "maintenance_layover", "repair", "multi_ship_docking"},
    "shipyard": {"warship_construction", "major_repair", "war_industry", "construction"},
    "military_outpost": {"fortified_military_support", "regional_command", "fleet_staging_when_needed", "major_fleet_support"},
    "detention_security": {"detention", "security"},
    "diplomatic_administrative": {"diplomacy", "regional_hub"},
    "colony_support": {"regional_support", "cargo_transfer", "personnel_transfer"},
}

SCALE_ORDER = ["micro_outpost", "small_station", "standard_station", "starbase", "major_complex"]

CONTINUOUS_SHARE = {
    "communications_relay": 0.80,
    "sensor_listening_outpost": 0.70,
    "research_observatory": 0.35,
    "medical_quarantine": 0.55,
    "depot_supply": 0.55,
    "trade_cargo_transfer": 0.45,
    "orbital_habitat": 0.35,
    "refinery_processing": 0.65,
    "repair_drydock": 0.60,
    "shipyard": 0.65,
    "military_outpost": 0.70,
    "detention_security": 0.65,
    "diplomatic_administrative": 0.35,
    "colony_support": 0.50,
}


class DeterministicRng:
    def __init__(self, seed_material: str) -> None:
        self.seed_material = seed_material
        self.counter = 0

    def _u256(self) -> int:
        payload = f"{self.seed_material}|{self.counter}".encode("utf-8")
        self.counter += 1
        return int.from_bytes(hashlib.sha256(payload).digest(), "big")

    def randint(self, low: int, high: int) -> int:
        if high < low:
            raise ValueError("high must be >= low")
        return low + self._u256() % (high - low + 1)

    def choice(self, values: list[Any]) -> Any:
        if not values:
            raise ValueError("choice requires values")
        return values[self._u256() % len(values)]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def stable_token(*parts: str, length: int = 16) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:length]


def parse_year(campaign_date: str) -> int:
    return int(campaign_date.split("-", 1)[0])


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def score_need(
    *,
    need_strength: float,
    strategic_value: float,
    existing_coverage: float,
    expected_need_years: float,
    alternative_sufficiency: float,
    site_advantage: float,
    operator_capacity: float,
    sustainment: float,
) -> float:
    service_gap = 100.0 - clamp(existing_coverage)
    duration_score = min(max(expected_need_years, 0.0) / 20.0, 1.0) * 100.0
    score = (
        0.25 * clamp(need_strength)
        + 0.20 * service_gap
        + 0.15 * clamp(strategic_value)
        + 0.10 * clamp(site_advantage)
        + 0.10 * clamp(operator_capacity)
        + 0.10 * clamp(sustainment)
        + 0.10 * duration_score
        - 0.15 * clamp(alternative_sufficiency)
    )
    return round(clamp(score), 2)


def hard_gate_reasons(
    *,
    origin_trigger: str,
    need_strength: float,
    expected_need_years: float,
    alternative_sufficiency: float,
    operator_capacity: float,
    site_advantage: float,
    sustainment: float,
    existing_coverage: float,
    redundancy_need: float,
) -> list[str]:
    existence = load_json(EXISTENCE)
    policy = load_json(POLICY)
    gates = policy["hard_gates"]
    reasons: list[str] = []

    if origin_trigger in existence.get("prohibited_generation_triggers", []):
        reasons.append(f"prohibited_origin_trigger:{origin_trigger}")
    if need_strength < gates["minimum_need_strength"]:
        reasons.append("need_strength_below_permanent_threshold")
    if expected_need_years < gates["minimum_expected_need_years"]:
        reasons.append("need_not_sustained_long_enough")
    if alternative_sufficiency > gates["maximum_alternative_sufficiency"]:
        reasons.append("lower_cost_alternative_is_sufficient")
    if operator_capacity < gates["minimum_operator_capacity"]:
        reasons.append("operator_cannot_support_construction")
    if site_advantage < gates["minimum_site_advantage"]:
        reasons.append("site_not_strongly_justified")
    if sustainment < gates["minimum_sustainment"]:
        reasons.append("credible_sustainment_chain_missing")
    if existing_coverage >= 75 and redundancy_need < 70 and need_strength < 85:
        reasons.append("existing_facility_coverage_is_sufficient")
    return reasons


def desired_scale(score: float, allow_major_complex: bool) -> tuple[str | None, str | None]:
    thresholds = load_json(POLICY)["scale_thresholds"]
    for row in thresholds:
        if score >= row["minimum_score"]:
            scale = row["scale"]
            if scale == "major_complex" and not allow_major_complex:
                return None, "major_complex_requires_explicit_high_level_authorization"
            return scale, None
    return None, "need_score_prefers_temporary_or_mobile_solution"


def resolve_role_scale(role: str, desired: str) -> tuple[str | None, bool, str | None]:
    policy = load_json(POLICY)
    allowed = policy["role_scale_limits"][role]
    desired_index = SCALE_ORDER.index(desired)
    allowed_indices = [SCALE_ORDER.index(scale) for scale in allowed]

    possible_at_or_below = [idx for idx in allowed_indices if idx <= desired_index]
    if not possible_at_or_below:
        return None, False, "need_not_strong_enough_for_role_minimum_fixed_scale"

    chosen_index = max(possible_at_or_below)
    chosen = SCALE_ORDER[chosen_index]
    limited = desired_index > max(allowed_indices)
    return chosen, limited, None


def design_available(design: dict[str, Any], operator_family: str, era_id: str, year: int) -> bool:
    if operator_family not in design.get("operator_families", []):
        return False
    availability = design.get("availability", {})
    profiles = availability.get("playable_profiles", [])
    if profiles and era_id not in profiles:
        return False
    if year < int(availability.get("from_year", -10**9)):
        return False
    if year < int(availability.get("from_decade", -10**9)):
        return False
    if year > int(availability.get("to_year", 10**9)):
        return False
    return True


def design_matches_role(design: dict[str, Any], role: str) -> bool:
    tags = ROLE_TAGS[role]
    return bool(tags.intersection(set(design.get("primary_roles", []))))


def reuse_allowed(
    design: dict[str, Any],
    *,
    score: float,
    strategic_value: float,
    allow_controlled_design: bool,
    allow_restricted_design: bool,
) -> bool:
    policy = design.get("reuse_policy")
    if policy == "broadly_reusable":
        return True
    if policy == "controlled_reuse":
        return allow_controlled_design or (score >= 80 and strategic_value >= 65)
    if policy == "restricted_reuse":
        return allow_restricted_design
    return False


def select_design(
    rng: DeterministicRng,
    *,
    operator_family: str,
    era_id: str,
    year: int,
    role: str,
    scale: str,
    score: float,
    strategic_value: float,
    allow_controlled_design: bool,
    allow_restricted_design: bool,
    campaign_seed: str,
    site_type: str,
) -> dict[str, Any]:
    designs = load_json(DESIGNS)["designs"]
    candidates = [
        row for row in designs
        if row.get("scale") == scale
        and design_available(row, operator_family, era_id, year)
        and design_matches_role(row, role)
        and reuse_allowed(
            row,
            score=score,
            strategic_value=strategic_value,
            allow_controlled_design=allow_controlled_design,
            allow_restricted_design=allow_restricted_design,
        )
    ]

    if candidates:
        selected = rng.choice(sorted(candidates, key=lambda row: row["design_id"]))
        return {
            "design_id": selected["design_id"],
            "design_mode": "canonical_reusable_design",
            "design_catalogue_ref": "lore/stations_and_facilities/canonical_station_design_catalogue_v0.1.json",
            "reuse_policy": selected["reuse_policy"],
            "source_refs": selected.get("source_refs", []),
        }

    design_seed = f"{campaign_seed}|{era_id}|{operator_family}|{role}|{scale}|{site_type}|facility_design_v0.1"
    return {
        "design_id": f"gen:facility_design:{stable_token(design_seed)}",
        "design_mode": "procedural_design",
        "design_catalogue_ref": None,
        "reuse_policy": "procedural_reusable",
        "source_refs": [],
        "design_seed_hash": hashlib.sha256(design_seed.encode("utf-8")).hexdigest(),
    }


def construction_months(rng: DeterministicRng, scale: str) -> int:
    low, high = load_json(POLICY)["construction_months"][scale]
    return rng.randint(int(low), int(high))


def lifecycle_state(commit_construction: bool, elapsed_months: int, build_months: int) -> tuple[str, float]:
    if not commit_construction:
        return "authorized", 0.0
    if elapsed_months <= 0:
        return "construction", 0.0
    ratio = elapsed_months / build_months
    if ratio < 0.70:
        return "construction", round(min(ratio, 0.69), 3)
    if ratio < 1.0:
        return "partial_operation", round(ratio, 3)
    return "operational", 1.0


def staffing_target(
    rng: DeterministicRng,
    *,
    scale: str,
    role: str,
    design_id: str,
) -> int:
    guidance = load_json(STAFFING)
    anchors = guidance.get("design_anchors", {})
    anchor = anchors.get(design_id, {})
    if "operator_duty_staff" in anchor:
        return int(anchor["operator_duty_staff"])
    if "operator_duty_staff_or_total_crew_min" in anchor:
        minimum = int(anchor["operator_duty_staff_or_total_crew_min"])
        return minimum + rng.randint(0, max(1000, minimum // 10))

    low, high = guidance["scale_guidance"][scale]["operator_duty_staff"]
    role_factor = {
        "communications_relay": 0.35,
        "sensor_listening_outpost": 0.50,
        "research_observatory": 0.65,
        "medical_quarantine": 0.80,
        "depot_supply": 0.75,
        "trade_cargo_transfer": 0.80,
        "orbital_habitat": 0.55,
        "refinery_processing": 0.80,
        "repair_drydock": 0.90,
        "shipyard": 1.00,
        "military_outpost": 0.90,
        "detention_security": 0.80,
        "diplomatic_administrative": 0.65,
        "colony_support": 0.70,
    }[role]
    adjusted_high = max(int(low), int(high * role_factor))
    return rng.randint(int(low), adjusted_high)


def resident_population(
    rng: DeterministicRng,
    *,
    scale: str,
    role: str,
    duty_staff: int,
    operator_family: str,
    design_id: str,
) -> dict[str, int]:
    if design_id == "starfleet_relay_station_47_type":
        residents = 0
        dependents = 0
        visitors = rng.randint(0, 1)
        return {
            "civilian_residents": residents,
            "dependents": dependents,
            "transient_visitors_baseline": visitors,
        }

    if role in {"military_outpost", "shipyard"} and operator_family in {"klingon_imperial_military", "dominion"}:
        resident_max = max(0, duty_staff // 20)
    elif role == "orbital_habitat":
        resident_max = duty_staff * 8
    elif role in {"trade_cargo_transfer", "diplomatic_administrative"}:
        resident_max = duty_staff * 3
    elif role in {"research_observatory", "medical_quarantine"}:
        resident_max = max(0, duty_staff // 3)
    elif scale in {"starbase", "major_complex"}:
        resident_max = duty_staff * 2
    else:
        resident_max = max(0, duty_staff // 2)

    residents = rng.randint(0, resident_max) if resident_max else 0
    dependents = rng.randint(0, residents // 3) if residents >= 3 else 0

    visitor_factor = {
        "micro_outpost": 2,
        "small_station": 12,
        "standard_station": 80,
        "starbase": 500,
        "major_complex": 1500,
    }[scale]
    visitors = rng.randint(0, visitor_factor)
    return {
        "civilian_residents": residents,
        "dependents": dependents,
        "transient_visitors_baseline": visitors,
    }


def allocate_fractions(total: int, fractions: dict[str, float]) -> dict[str, int]:
    raw = {key: total * value for key, value in fractions.items()}
    floors = {key: int(value) for key, value in raw.items()}
    remaining = total - sum(floors.values())
    order = sorted(
        fractions,
        key=lambda key: (raw[key] - floors[key], key),
        reverse=True,
    )
    for key in order[:remaining]:
        floors[key] += 1
    return floors


def watch_model(operator_alias: str, role: str, duty_staff: int) -> dict[str, Any]:
    if duty_staff <= 4:
        active = 1
        on_call = max(0, duty_staff - active)
        return {
            "pattern": "custom_alternating_active_on_call",
            "continuous_watch_pool": duty_staff,
            "day_or_peak_staff": 0,
            "active_at_one_time": active,
            "on_call_or_rest": on_call,
            "allocation_total": duty_staff,
            "note": "Tiny-facility schedule; automation carries continuous background functions where design permits.",
        }

    continuous_pool = max(3, round(duty_staff * CONTINUOUS_SHARE[role]))
    continuous_pool = min(continuous_pool, duty_staff)
    day_staff = duty_staff - continuous_pool

    if operator_alias in {"starfleet", "federation_civil"}:
        fractions = {"alpha": 0.34, "beta": 0.31, "gamma": 0.30, "relief_or_float": 0.05}
        labels = ["alpha", "beta", "gamma"]
        pattern = "three_shift_plus_day_staff"
    else:
        fractions = {"watch_1": 0.34, "watch_2": 0.31, "watch_3": 0.30, "relief_or_float": 0.05}
        labels = ["watch_1", "watch_2", "watch_3"]
        pattern = "custom_three_watch_equivalent_plus_day_staff"

    allocation = allocate_fractions(continuous_pool, fractions)
    return {
        "pattern": pattern,
        "continuous_watch_pool": continuous_pool,
        "day_or_peak_staff": day_staff,
        "watch_assignments": {label: allocation[label] for label in labels},
        "relief_or_float": allocation["relief_or_float"],
        "allocation_total": continuous_pool + day_staff,
        "exact_watch_anchor": "INSTANCE_POLICY",
    }


def service_profile(role: str, design_id: str) -> dict[str, Any]:
    grammar = load_json(GRAMMAR)["role_families"][role]
    required = list(grammar.get("required", []))
    optional = list(grammar.get("optional", []))

    selected_optional: list[str] = []
    if design_id == "starfleet_relay_station_47_type" and "smallcraft_support" in optional:
        selected_optional.append("smallcraft_support")
    elif optional:
        selected_optional.append(optional[0])

    return {
        "required_capabilities": required,
        "selected_optional_capabilities": selected_optional,
        "explicitly_not_assumed": grammar.get("forbidden_by_default", []),
    }


def traffic_profile(rng: DeterministicRng, scale: str, role: str, operational: bool) -> dict[str, Any]:
    if not operational:
        return {
            "traffic_status": "construction_or_precommissioning",
            "expected_arrivals_per_30d": 0,
            "decorative_traffic_forbidden": True,
        }
    ranges = {
        "micro_outpost": (0, 3),
        "small_station": (1, 18),
        "standard_station": (8, 100),
        "starbase": (40, 500),
        "major_complex": (100, 1200),
    }
    low, high = ranges[scale]
    if role in {"communications_relay", "sensor_listening_outpost"}:
        high = min(high, 4)
    arrivals = rng.randint(low, high)
    return {
        "traffic_status": "light" if arrivals <= 5 else "normal" if arrivals <= 80 else "heavy",
        "expected_arrivals_per_30d": arrivals,
        "decorative_traffic_forbidden": True,
        "rule":"Every arrival still requires route/mission/service provenance at live runtime; this value is only planning throughput guidance."
    }


def reject(
    *,
    campaign_seed: str,
    need_id: str,
    reasons: list[str],
    score: float | None,
    recommended_solution: str,
) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "generator": {"generator_id": GENERATOR_ID, "generator_version": GENERATOR_VERSION},
        "outcome": "NO_PERMANENT_FACILITY",
        "campaign_seed": campaign_seed,
        "need_id": need_id,
        "facility_id": None,
        "need_score": score,
        "rejection_reasons": reasons,
        "recommended_solution": recommended_solution,
        "anti_convenience_rule": True,
    }


def generate(
    *,
    campaign_seed: str,
    need_id: str,
    era_id: str,
    campaign_date: str,
    operator: str,
    role: str,
    site_id: str,
    site_type: str,
    origin_trigger: str,
    need_strength: float,
    strategic_value: float,
    existing_coverage: float,
    expected_need_years: float,
    alternative_sufficiency: float,
    site_advantage: float,
    operator_capacity: float,
    sustainment: float,
    redundancy_need: float = 0.0,
    allow_major_complex: bool = False,
    allow_controlled_design: bool = False,
    allow_restricted_design: bool = False,
    commit_construction: bool = False,
    elapsed_construction_months: int = 0,
) -> dict[str, Any]:
    if operator not in OPERATOR_MAP:
        raise ValueError(f"Unsupported operator alias: {operator}")
    grammar = load_json(GRAMMAR)
    if role not in grammar["role_families"]:
        raise ValueError(f"Unsupported facility role: {role}")
    if elapsed_construction_months < 0:
        raise ValueError("elapsed construction months cannot be negative")

    score = score_need(
        need_strength=need_strength,
        strategic_value=strategic_value,
        existing_coverage=existing_coverage,
        expected_need_years=expected_need_years,
        alternative_sufficiency=alternative_sufficiency,
        site_advantage=site_advantage,
        operator_capacity=operator_capacity,
        sustainment=sustainment,
    )

    reasons = hard_gate_reasons(
        origin_trigger=origin_trigger,
        need_strength=need_strength,
        expected_need_years=expected_need_years,
        alternative_sufficiency=alternative_sufficiency,
        operator_capacity=operator_capacity,
        site_advantage=site_advantage,
        sustainment=sustainment,
        existing_coverage=existing_coverage,
        redundancy_need=redundancy_need,
    )
    if reasons:
        return reject(
            campaign_seed=campaign_seed,
            need_id=need_id,
            reasons=reasons,
            score=score,
            recommended_solution="existing_facility_or_temporary_mobile_surface_support",
        )

    desired, scale_error = desired_scale(score, allow_major_complex)
    if scale_error or desired is None:
        return reject(
            campaign_seed=campaign_seed,
            need_id=need_id,
            reasons=[scale_error or "scale_not_resolved"],
            score=score,
            recommended_solution="temporary_or_mobile_support_or_high_level_development_decision",
        )

    scale, scale_limited, role_scale_error = resolve_role_scale(role, desired)
    if role_scale_error or scale is None:
        return reject(
            campaign_seed=campaign_seed,
            need_id=need_id,
            reasons=[role_scale_error or "role_scale_not_resolved"],
            score=score,
            recommended_solution="temporary_support_or_defer_until_demand_justifies_required_scale",
        )

    year = parse_year(campaign_date)
    operator_family = OPERATOR_MAP[operator]
    seed_material = f"{campaign_seed}|{need_id}|{era_id}|{campaign_date}|{operator}|{role}|{site_id}|facility"
    rng = DeterministicRng(seed_material)

    design = select_design(
        rng,
        operator_family=operator_family,
        era_id=era_id,
        year=year,
        role=role,
        scale=scale,
        score=score,
        strategic_value=strategic_value,
        allow_controlled_design=allow_controlled_design,
        allow_restricted_design=allow_restricted_design,
        campaign_seed=campaign_seed,
        site_type=site_type,
    )

    project_id = f"gen:facility_project:{stable_token(campaign_seed, need_id, design['design_id'], site_id)}"
    build_months = construction_months(rng, scale)
    state, progress = lifecycle_state(commit_construction, elapsed_construction_months, build_months)

    facility_id = None
    designation = None
    if commit_construction:
        facility_id = f"gen:facility:{stable_token(project_id, design['design_id'], site_id)}"
        designation = f"FAC-{stable_token(facility_id, length=7).upper()}"

    duty_staff = staffing_target(rng, scale=scale, role=role, design_id=design["design_id"])
    populations = resident_population(
        rng,
        scale=scale,
        role=role,
        duty_staff=duty_staff,
        operator_family=operator_family,
        design_id=design["design_id"],
    )
    watch = watch_model(operator, role, duty_staff)
    services = service_profile(role, design["design_id"])
    traffic = traffic_profile(rng, scale, role, state == "operational")

    return {
        "schema_version": "0.1.0",
        "generator": {
            "generator_id": GENERATOR_ID,
            "generator_version": GENERATOR_VERSION,
            "algorithm": "sha256_counter_v1",
        },
        "outcome": "FACILITY_PROJECT",
        "generation_context": {
            "campaign_seed": campaign_seed,
            "need_id": need_id,
            "era_id": era_id,
            "campaign_date": campaign_date,
            "operator_alias": operator,
            "operator_family": operator_family,
            "role": role,
            "site_id": site_id,
            "site_type": site_type,
            "origin_trigger": origin_trigger,
        },
        "causality": {
            "need_score": score,
            "desired_scale": desired,
            "resolved_scale": scale,
            "role_scale_limited": scale_limited,
            "expected_need_years": expected_need_years,
            "existing_coverage": existing_coverage,
            "alternative_sufficiency": alternative_sufficiency,
            "anti_player_convenience_passed": True,
        },
        "design": design,
        "project": {
            "project_id": project_id,
            "facility_id": facility_id,
            "temporary_designation": designation,
            "construction_committed": commit_construction,
            "lifecycle_state": state,
            "construction_progress": progress,
            "estimated_construction_months": build_months,
            "elapsed_construction_months": elapsed_construction_months,
            "persistent_identity_begins_at_commitment": True,
        },
        "population_target": {
            "operator_duty_staff": duty_staff,
            **populations,
            "docked_ship_crews_excluded": True,
        },
        "operations": {
            "watch": watch,
            "services": services,
            "traffic_planning": traffic,
        },
        "persistence": {
            "reroll_on_reload": False,
            "design_reusable": True,
            "owner_operator_can_change_without_new_facility_id": True,
            "expansion_refit_damage_append_history": True,
        },
        "runtime_boundary": "Reference generation only; CoreRPG 4.5+ owns live persistent World State.",
    }


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("outcome") == "NO_PERMANENT_FACILITY":
        if payload.get("facility_id") is not None:
            errors.append("rejected proposal must not have facility_id")
        return errors

    project = payload.get("project", {})
    population = payload.get("population_target", {})
    watch = payload.get("operations", {}).get("watch", {})

    if not project.get("project_id", "").startswith("gen:facility_project:"):
        errors.append("missing project id")
    if project.get("construction_committed"):
        if not project.get("facility_id", "").startswith("gen:facility:"):
            errors.append("committed construction must have facility id")
    else:
        if project.get("facility_id") is not None:
            errors.append("uncommitted project must not yet have facility id")
    if watch.get("allocation_total") != population.get("operator_duty_staff"):
        errors.append("watch/day allocation does not equal operator duty staff")
    if payload.get("persistence", {}).get("reroll_on_reload") is not False:
        errors.append("facility project must not reroll on reload")
    if payload.get("operations", {}).get("traffic_planning", {}).get("decorative_traffic_forbidden") is not True:
        errors.append("decorative traffic must be forbidden")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--era", default="tng_ds9_voyager")
    parser.add_argument("--date", default="2372-01-01")
    parser.add_argument("--operator", choices=sorted(OPERATOR_MAP), required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--site-id", required=True)
    parser.add_argument("--site-type", default="orbital_or_deep_space")
    parser.add_argument("--origin-trigger", default="persistent_world_need")
    parser.add_argument("--need-strength", type=float, default=50)
    parser.add_argument("--strategic-value", type=float, default=50)
    parser.add_argument("--existing-coverage", type=float, default=20)
    parser.add_argument("--expected-years", type=float, default=10)
    parser.add_argument("--alternative-sufficiency", type=float, default=20)
    parser.add_argument("--site-advantage", type=float, default=70)
    parser.add_argument("--operator-capacity", type=float, default=80)
    parser.add_argument("--sustainment", type=float, default=80)
    parser.add_argument("--redundancy-need", type=float, default=0)
    parser.add_argument("--allow-major-complex", action="store_true")
    parser.add_argument("--allow-controlled-design", action="store_true")
    parser.add_argument("--allow-restricted-design", action="store_true")
    parser.add_argument("--commit-construction", action="store_true")
    parser.add_argument("--elapsed-months", type=int, default=0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = generate(
        campaign_seed=args.seed,
        need_id=args.need_id,
        era_id=args.era,
        campaign_date=args.date,
        operator=args.operator,
        role=args.role,
        site_id=args.site_id,
        site_type=args.site_type,
        origin_trigger=args.origin_trigger,
        need_strength=args.need_strength,
        strategic_value=args.strategic_value,
        existing_coverage=args.existing_coverage,
        expected_need_years=args.expected_years,
        alternative_sufficiency=args.alternative_sufficiency,
        site_advantage=args.site_advantage,
        operator_capacity=args.operator_capacity,
        sustainment=args.sustainment,
        redundancy_need=args.redundancy_need,
        allow_major_complex=args.allow_major_complex,
        allow_controlled_design=args.allow_controlled_design,
        allow_restricted_design=args.allow_restricted_design,
        commit_construction=args.commit_construction,
        elapsed_construction_months=args.elapsed_months,
    )
    if args.validate:
        errors = validate(payload)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 2

    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
