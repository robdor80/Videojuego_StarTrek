#!/usr/bin/env python3
"""Deterministic minimal observable-system generator for Star Trek v0.0.1."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GENERATOR_ID = "v0_0_1_observable_system_generator"
GENERATOR_VERSION = "0.1.0"


class DeterministicRng:
    """Counter-based SHA-256 PRNG with stable cross-run behavior."""

    def __init__(self, seed_material: str) -> None:
        self.seed_material = seed_material
        self.counter = 0

    def _u256(self) -> int:
        payload = f"{self.seed_material}|{self.counter}".encode("utf-8")
        self.counter += 1
        return int.from_bytes(hashlib.sha256(payload).digest(), "big")

    def random(self) -> float:
        return self._u256() / float(1 << 256)

    def randint(self, low: int, high: int) -> int:
        if high < low:
            raise ValueError("high must be >= low")
        return low + (self._u256() % (high - low + 1))

    def choice(self, values: list[Any]) -> Any:
        if not values:
            raise ValueError("choice requires at least one value")
        return values[self._u256() % len(values)]

    def weighted_choice(self, entries: list[tuple[Any, int]]) -> Any:
        total = sum(weight for _, weight in entries)
        if total <= 0:
            raise ValueError("weights must sum to > 0")
        pick = self._u256() % total
        cursor = 0
        for value, weight in entries:
            cursor += weight
            if pick < cursor:
                return value
        return entries[-1][0]

    def uniform(self, low: float, high: float, digits: int = 6) -> float:
        value = low + (high - low) * self.random()
        return round(value, digits)


def stable_token(*parts: str, length: int = 12) -> str:
    joined = "|".join(parts).encode("utf-8")
    return hashlib.sha256(joined).hexdigest()[:length]


def entity_id(seed_key: str, entity_type: str, ordinal: int) -> str:
    token = stable_token(seed_key, entity_type, str(ordinal), length=16)
    return f"gen:{entity_type}:{token}"


def signature(
    signature_id: str,
    signature_type: str,
    strength: str,
    variability: str,
    emission_mode: str,
    source_property: str,
    *,
    masking: float = 0.0,
) -> dict[str, Any]:
    return {
        "signature_id": signature_id,
        "signature_type": signature_type,
        "strength": strength,
        "variability": variability,
        "emission_mode": emission_mode,
        "source_property": source_property,
        "detectability_modifiers": {"masking": round(masking, 3)},
    }


def base_entity(
    seed_key: str,
    entity_type: str,
    ordinal: int,
    *,
    sector_id: str,
    system_id: str,
    position_au: list[float],
    classification: str,
    properties: dict[str, Any],
    hidden_properties: dict[str, Any] | None = None,
    signatures: list[dict[str, Any]] | None = None,
    masking: list[str] | None = None,
    local_interference: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "entity_id": entity_id(seed_key, entity_type, ordinal),
        "entity_type": entity_type,
        "origin": {
            "type": "procedural",
            "source_ids": [],
            "generator_id": GENERATOR_ID,
            "seed": seed_key,
        },
        "temporal_state": {"valid_from": None, "valid_to": None, "active": True},
        "spatial_state": {
            "sector_id": sector_id,
            "system_id": system_id,
            "reference_frame": "system_barycentric",
            "position": {"unit": "AU", "xyz": position_au},
            "velocity": None,
        },
        "ground_truth": {
            "classification": classification,
            "properties": properties,
            "hidden_properties": hidden_properties or {},
        },
        "signatures": signatures or [],
        "environmental_modifiers": {
            "masking": masking or [],
            "local_interference": local_interference or [],
        },
        "persistence": {
            "persistent": True,
            "materialized": True,
            "can_be_modified_by_campaign": True,
        },
    }


@dataclass(frozen=True)
class GenerationContext:
    campaign_seed: str
    sector_id: str
    era_id: str
    campaign_date: str

    @property
    def seed_key(self) -> str:
        return f"{self.campaign_seed}|{self.sector_id}|{self.era_id}|{self.campaign_date}"


def generate(context: GenerationContext) -> dict[str, Any]:
    rng = DeterministicRng(context.seed_key)
    system_token = stable_token(context.seed_key, "system", length=10).upper()
    system_id = f"gen:system:{system_token.lower()}"
    system_name = f"PROC-{context.sector_id}-{system_token[:5]}"
    entities: list[dict[str, Any]] = []

    spectral = rng.weighted_choice([
        ("M", 40), ("K", 25), ("G", 15), ("F", 8), ("A", 5), ("B", 2), ("O", 1)
    ])
    star_temp = {
        "M": (2400, 3700), "K": (3700, 5200), "G": (5200, 6000),
        "F": (6000, 7500), "A": (7500, 10000), "B": (10000, 30000),
        "O": (30000, 45000),
    }[spectral]
    entities.append(base_entity(
        context.seed_key, "star", 1,
        sector_id=context.sector_id,
        system_id=system_id,
        position_au=[0.0, 0.0, 0.0],
        classification=f"spectral_{spectral.lower()}",
        properties={
            "spectral_class": spectral,
            "surface_temperature_k": rng.randint(*star_temp),
            "relative_luminosity": rng.uniform(0.08 if spectral in "MK" else 0.7, 8.0),
        },
        signatures=[
            signature("sig:star:em", "electromagnetic", "extreme", "stable", "passive", "stellar_output"),
            signature("sig:star:thermal", "thermal", "extreme", "stable", "passive", "stellar_heat"),
            signature("sig:star:grav", "gravimetric", "strong", "stable", "passive", "stellar_mass"),
        ],
    ))

    planet_count = rng.randint(3, 7)
    orbit = rng.uniform(0.25, 0.7)
    moon_budget = rng.randint(0, 6)
    planet_kinds = [
        ("rocky", 28), ("terrestrial", 22), ("oceanic", 10),
        ("ice_world", 12), ("gas_giant", 18), ("ice_giant", 10),
    ]

    for index in range(1, planet_count + 1):
        orbit += rng.uniform(0.25, 2.2)
        kind = rng.weighted_choice(planet_kinds)
        angle = rng.uniform(0.0, math.tau, digits=9)
        pos = [
            round(orbit * math.cos(angle), 6),
            round(orbit * math.sin(angle), 6),
            rng.uniform(-0.03, 0.03),
        ]
        mass_earth = rng.uniform(0.2, 4.0) if "giant" not in kind else rng.uniform(8.0, 180.0)
        atmosphere = kind in {"terrestrial", "oceanic", "gas_giant", "ice_giant"} or rng.random() < 0.35
        life_truth = kind in {"terrestrial", "oceanic"} and rng.random() < 0.30

        entities.append(base_entity(
            context.seed_key, "planet", index,
            sector_id=context.sector_id,
            system_id=system_id,
            position_au=pos,
            classification=kind,
            properties={
                "ordinal": index,
                "orbit_radius_au": round(orbit, 6),
                "mass_earth": mass_earth,
                "has_atmosphere": atmosphere,
            },
            hidden_properties={
                "biosphere_present": {
                    "value": life_truth,
                    "minimum_resolution": "high",
                    "preferred_filter": "biological",
                }
            },
            signatures=[
                signature(
                    f"sig:p{index}:grav", "gravimetric",
                    "moderate" if "giant" not in kind else "strong",
                    "stable", "passive", "planetary_mass"
                ),
                signature(
                    f"sig:p{index}:thermal", "thermal",
                    "weak", "stable", "passive", "planetary_temperature"
                ),
            ] + (
                [signature(
                    f"sig:p{index}:bio", "biological", "trace",
                    "intermittent", "passive", "biosphere"
                )] if life_truth else []
            ),
        ))

    moon_ordinal = 0
    for _ in range(moon_budget):
        moon_ordinal += 1
        parent_index = rng.randint(1, planet_count)
        parent = entities[parent_index]
        pxyz = parent["spatial_state"]["position"]["xyz"]
        offset = [
            rng.uniform(-0.01, 0.01),
            rng.uniform(-0.01, 0.01),
            rng.uniform(-0.002, 0.002),
        ]
        entities.append(base_entity(
            context.seed_key, "moon", moon_ordinal,
            sector_id=context.sector_id,
            system_id=system_id,
            position_au=[round(pxyz[i] + offset[i], 6) for i in range(3)],
            classification=rng.choice(["rocky_moon", "icy_moon"]),
            properties={
                "parent_entity_id": parent["entity_id"],
                "mass_lunar": rng.uniform(0.02, 2.5),
            },
            signatures=[
                signature(
                    f"sig:m{moon_ordinal}:grav", "gravimetric", "weak",
                    "stable", "passive", "moon_mass"
                )
            ],
        ))

    anomaly_count = rng.randint(1, 2)
    anomaly_types = ["subspace_distortion", "gravimetric_shear", "particle_eddy"]
    for index in range(1, anomaly_count + 1):
        kind = rng.choice(anomaly_types)
        interference = rng.choice([
            "subspace_noise", "charged_particles", "gravimetric_turbulence"
        ])
        sigs = [
            signature(
                f"sig:a{index}:sub", "subspace",
                "strong" if index == 1 else "moderate",
                "chaotic", "passive", "anomaly_field", masking=0.15
            ),
            signature(
                f"sig:a{index}:grav", "gravimetric", "moderate",
                "chaotic", "passive", "spacetime_gradient", masking=0.10
            ),
        ]
        if rng.random() < 0.75 or index == 1:
            sigs.append(signature(
                f"sig:a{index}:particle", "particle", "moderate",
                "intermittent", "passive", "particle_emission", masking=0.20
            ))

        entities.append(base_entity(
            context.seed_key, "anomaly", index,
            sector_id=context.sector_id,
            system_id=system_id,
            position_au=[
                rng.uniform(-12.0, 12.0),
                rng.uniform(-12.0, 12.0),
                rng.uniform(-1.0, 1.0),
            ],
            classification=kind,
            properties={
                "diameter_km": rng.randint(4000, 40000),
                "stability": rng.uniform(0.1, 0.95),
                "hazard_level": rng.choice(["low", "moderate", "high", "severe"]),
            },
            hidden_properties={
                "precise_nature": {
                    "value": kind,
                    "minimum_resolution": "high",
                    "preferred_filter": "subspace",
                },
                "internal_structure": {
                    "value": rng.choice(["layered", "turbulent", "coherent_core"]),
                    "minimum_resolution": "high",
                    "preferred_filter": "gravimetric",
                },
            },
            signatures=sigs,
            masking=[interference],
            local_interference=[interference],
        ))

    for index in range(1, rng.randint(0, 1) + 1):
        transponder_mode = rng.choice(["broadcasting", "silent"])
        ship_sigs = [
            signature(f"sig:s{index}:warp", "warp", "moderate", "stable", "passive", "warp_system_residue"),
            signature(f"sig:s{index}:em", "electromagnetic", "weak", "stable", "passive", "ship_power"),
        ]
        if transponder_mode == "broadcasting":
            ship_sigs.append(signature(
                f"sig:s{index}:xpdr", "artificial_transponder", "strong",
                "stable", "active", "transponder"
            ))
        entities.append(base_entity(
            context.seed_key, "starship", index,
            sector_id=context.sector_id,
            system_id=system_id,
            position_au=[
                rng.uniform(-5.0, 5.0),
                rng.uniform(-5.0, 5.0),
                rng.uniform(-0.4, 0.4),
            ],
            classification="unidentified_vessel",
            properties={
                "transponder_mode": transponder_mode,
                "estimated_size_m": rng.randint(40, 700),
            },
            hidden_properties={
                "true_affiliation": {
                    "value": rng.choice(["federation_civilian", "independent", "unknown"]),
                    "minimum_resolution": "standard",
                    "preferred_filter": "artificial_transponder",
                }
            },
            signatures=ship_sigs,
        ))

    for index in range(1, rng.randint(0, 2) + 1):
        etype = rng.choice(["probe", "beacon"])
        entities.append(base_entity(
            context.seed_key, etype, index,
            sector_id=context.sector_id,
            system_id=system_id,
            position_au=[
                rng.uniform(-4.0, 4.0),
                rng.uniform(-4.0, 4.0),
                rng.uniform(-0.2, 0.2),
            ],
            classification="artificial_object",
            properties={"operational": rng.random() < 0.85},
            signatures=[
                signature(
                    f"sig:{etype}{index}:em", "electromagnetic", "weak",
                    "periodic", "active", "artificial_emitter"
                )
            ],
        ))

    if rng.randint(0, 1):
        entities.append(base_entity(
            context.seed_key, "debris_field", 1,
            sector_id=context.sector_id,
            system_id=system_id,
            position_au=[
                rng.uniform(-6.0, 6.0),
                rng.uniform(-6.0, 6.0),
                rng.uniform(-0.2, 0.2),
            ],
            classification="debris_field",
            properties={
                "extent_km": rng.randint(50, 5000),
                "density": rng.choice(["sparse", "moderate", "dense"]),
            },
            hidden_properties={
                "origin_hint": {
                    "value": rng.choice(["natural", "artificial", "indeterminate"]),
                    "minimum_resolution": "high",
                    "preferred_filter": "electromagnetic",
                }
            },
            signatures=[
                signature("sig:debris:em", "electromagnetic", "trace", "intermittent", "passive", "residual_energy"),
                signature("sig:debris:grav", "gravimetric", "trace", "stable", "passive", "distributed_mass"),
            ],
        ))

    relations = []
    for entity in entities:
        parent = entity["ground_truth"]["properties"].get("parent_entity_id")
        if parent:
            relations.append({
                "relation": "orbits",
                "source_entity_id": entity["entity_id"],
                "target_entity_id": parent,
            })

    counts: dict[str, int] = {}
    for entity in entities:
        counts[entity["entity_type"]] = counts.get(entity["entity_type"], 0) + 1

    return {
        "schema_version": "0.1.0",
        "generator": {
            "generator_id": GENERATOR_ID,
            "generator_version": GENERATOR_VERSION,
            "algorithm": "sha256_counter_v1",
        },
        "generation_context": {
            "campaign_seed": context.campaign_seed,
            "sector_id": context.sector_id,
            "era_id": context.era_id,
            "campaign_date": context.campaign_date,
            "seed_key_hash": hashlib.sha256(context.seed_key.encode("utf-8")).hexdigest(),
        },
        "system": {
            "system_id": system_id,
            "display_name": system_name,
            "canonical_reserved": False,
            "materialized": True,
        },
        "entities": entities,
        "relations": relations,
        "summary": {
            "entity_count": len(entities),
            "counts_by_type": dict(sorted(counts.items())),
        },
    }


def validate_v0_0_1(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    entities = payload.get("entities", [])
    counts: dict[str, int] = {}
    ids: set[str] = set()

    for entity in entities:
        etype = entity.get("entity_type")
        counts[etype] = counts.get(etype, 0) + 1
        eid = entity.get("entity_id")
        if eid in ids:
            errors.append(f"duplicate entity_id: {eid}")
        ids.add(eid)

    bounds = {
        "star": (1, 1),
        "planet": (3, 7),
        "moon": (0, 6),
        "anomaly": (1, 2),
        "starship": (0, 1),
        "debris_field": (0, 1),
    }
    for etype, (minimum, maximum) in bounds.items():
        value = counts.get(etype, 0)
        if not (minimum <= value <= maximum):
            errors.append(f"{etype} count {value} outside [{minimum}, {maximum}]")

    small_objects = counts.get("probe", 0) + counts.get("beacon", 0)
    if not (0 <= small_objects <= 2):
        errors.append(f"probe/beacon count {small_objects} outside [0, 2]")

    if not any(len(e.get("signatures", [])) >= 2 for e in entities):
        errors.append("missing entity with multiple signature types")

    if not any(
        e.get("environmental_modifiers", {}).get("masking")
        or e.get("environmental_modifiers", {}).get("local_interference")
        for e in entities
    ):
        errors.append("missing entity affected by masking/interference")

    if not any(
        any(
            isinstance(value, dict) and value.get("minimum_resolution") == "high"
            for value in e.get("ground_truth", {}).get("hidden_properties", {}).values()
        )
        for e in entities
    ):
        errors.append("missing high-resolution-gated hidden property")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", required=True, help="Campaign or test seed.")
    parser.add_argument("--sector", default="041", help="Sector id.")
    parser.add_argument("--era", default="tng_ds9_voyager", help="Era profile id.")
    parser.add_argument("--date", default="2368-01-01", help="Campaign date in deterministic context.")
    parser.add_argument("--output", type=Path, help="Output JSON path. Stdout if omitted.")
    parser.add_argument("--validate", action="store_true", help="Validate the v0.0.1 profile.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = generate(GenerationContext(
        campaign_seed=args.seed,
        sector_id=args.sector,
        era_id=args.era,
        campaign_date=args.date,
    ))

    if args.validate:
        errors = validate_v0_0_1(payload)
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
