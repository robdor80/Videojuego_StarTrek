#!/usr/bin/env python3
"""Deterministic reference generator for procedural civilizations and First Contact.

Content/rules reference implementation only. CoreRPG remains the future
authoritative runtime owner of live World State and persistence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

TECH = ROOT / "universe/generation/civilization_technology_spaceflight_warp_grammar_v0.1.json"
SPECIES = ROOT / "universe/generation/procedural_sapient_species_morphology_biology_v0.1.json"
GOV = ROOT / "universe/generation/procedural_government_institution_representation_grammar_v0.1.json"
SETTLEMENT = ROOT / "universe/generation/procedural_settlement_colony_generation_grammar_v0.1.json"

GENERATOR_ID = "procedural_civilization_first_contact_reference_generator"
GENERATOR_VERSION = "0.1.0"

MATERIALIZATION_ORDER = ["latent", "observed", "materialized", "first_contact_preparation"]
WARP_ORDER = [
    "none","theoretical","active_research","prototype_ground_test",
    "prototype_space_test","first_successful_warp_flight",
    "repeatable_warp_capability","interstellar_warp_operations",
]

ENV_MORPHOLOGY = {
    "temperate": ["humanoid_bilateral","nonhuman_bilateral","mammalian_like_nonhuman","reptilian_like"],
    "arid": ["humanoid_bilateral","nonhuman_bilateral","reptilian_like","arthropod_like"],
    "cold": ["humanoid_bilateral","nonhuman_bilateral","mammalian_like_nonhuman"],
    "high_gravity": ["humanoid_bilateral","nonhuman_bilateral","arthropod_like"],
    "low_gravity": ["humanoid_bilateral","nonhuman_bilateral","avian_or_gliding_adapted"],
    "aquatic": ["aquatic_or_amphibious","radial_or_multilateral","nonhuman_bilateral"],
    "amphibious": ["aquatic_or_amphibious","humanoid_bilateral","nonhuman_bilateral"],
}

SURFACE_BY_FAMILY = {
    "humanoid_bilateral": ["smooth_skin","fine_scaled_skin","textured_skin"],
    "nonhuman_bilateral": ["smooth_skin","scaled_surface","fine_fur","keratinous_plates"],
    "radial_or_multilateral": ["smooth_membrane","scaled_surface","soft_dermal_plates"],
    "aquatic_or_amphibious": ["smooth_moist_skin","fine_scales","rubbery_dermis"],
    "avian_or_gliding_adapted": ["feather_like_covering","fine_filaments","smooth_skin_with_flight_membranes"],
    "arthropod_like": ["segmented_exoskeleton","soft_jointed_carapace"],
    "reptilian_like": ["fine_scales","plate_scales","smooth_scaled_skin"],
    "mammalian_like_nonhuman": ["fine_fur","dense_fur","mixed_fur_skin"],
}

SYLLABLE_ONSETS = ["k","t","m","n","r","s","v","l","d","z","sh","th","q","b","f","h"]
SYLLABLE_VOWELS = ["a","e","i","o","u","ae","ai","io","ou"]
SYLLABLE_CODAS = ["","n","r","s","l","m","th","k"]
WRITING = ["alphabetic","abugida_like","syllabic","logographic_mixed","featural"]
WORD_ORDER = ["SVO","SOV","VSO","VOS","flexible_topic_prominent"]
GOV_TYPES = [
    "unitary_republic","federal_republic","constitutional_monarchy","parliamentary_system",
    "council_governance","technocratic_governance","theocratic_governance",
    "hereditary_monarchy","oligarchic_governance","military_governance",
    "corporate_governance","confederation","city_state_network","clan_or_house_federation",
    "distributed_consensus"
]
SETTLEMENT_TYPES = [
    "capital","major_city","regional_city","industrial_settlement",
    "scientific_settlement","spaceport_settlement","agricultural_settlement"
]


class DeterministicRng:
    def __init__(self, seed_material: str) -> None:
        self.seed_material = seed_material
        self.counter = 0

    def _u256(self) -> int:
        payload = f"{self.seed_material}|{self.counter}".encode("utf-8")
        self.counter += 1
        return int.from_bytes(hashlib.sha256(payload).digest(), "big")

    def randint(self, low: int, high: int) -> int:
        return low + self._u256() % (high - low + 1)

    def choice(self, values: list[Any]) -> Any:
        return values[self._u256() % len(values)]


def stable_token(*parts: str, length: int = 16) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:length]


def word(rng: DeterministicRng, syllables_min: int = 2, syllables_max: int = 3) -> str:
    n = rng.randint(syllables_min, syllables_max)
    chunks = []
    for _ in range(n):
        chunks.append(rng.choice(SYLLABLE_ONSETS) + rng.choice(SYLLABLE_VOWELS) + rng.choice(SYLLABLE_CODAS))
    value = "".join(chunks)
    return value[0].upper() + value[1:]


def population_estimate(rng: DeterministicRng, band: str) -> int:
    bands = {
        "tiny": (10000, 250000),
        "small": (250000, 50000000),
        "medium": (50000000, 1500000000),
        "large": (1500000000, 8000000000),
        "very_large": (8000000000, 30000000000),
    }
    low, high = bands[band]
    return rng.randint(low, high)


def translation_state(samples: int) -> str:
    if samples <= 0:
        return "untranslated"
    if samples == 1:
        return "analysis_required"
    if samples == 2:
        return "universal_translator_literal_only"
    if samples <= 4:
        return "universal_translator_partial"
    return "universal_translator_confident"


def materialization_at_least(level: str, required: str) -> bool:
    return MATERIALIZATION_ORDER.index(level) >= MATERIALIZATION_ORDER.index(required)


def warp_is_post_threshold(warp_state: str) -> bool:
    return WARP_ORDER.index(warp_state) >= WARP_ORDER.index("first_successful_warp_flight")


def first_contact_assessment(
    *,
    warp_state: str,
    prior_alien_exposure: bool,
    public_alien_awareness: bool,
    political_representation_state: str,
    active_internal_conflict: bool,
    mutual_contact: bool,
) -> dict[str, Any]:
    if mutual_contact:
        eligibility = "contact_required_by_mutual_encounter_or_exposure"
        timing = "respond_now_with_controlled_disclosure"
    elif warp_state in {"none","theoretical","active_research","prototype_ground_test"}:
        if prior_alien_exposure or public_alien_awareness:
            eligibility = "limited_contact_possible"
            timing = "Prime_Directive_mitigation_and_case_review"
        else:
            eligibility = "not_eligible_normal_contact"
            timing = "observe_only"
    elif warp_state == "prototype_space_test":
        eligibility = "prepare_contact"
        timing = "continue_observation_until_threshold_or_other_cause"
    else:
        if active_internal_conflict or political_representation_state in {
            "multiple_sovereign_states","contested_planetary_authority",
            "civil_war_or_fragmentation","no_single_external_representative"
        }:
            eligibility = "prepare_contact"
            timing = "contact_possible_but_scope_and_representation_require_resolution"
        else:
            eligibility = "formal_contact_candidate"
            timing = "captain_decision_after_brief"

    if not warp_is_post_threshold(warp_state) and not (prior_alien_exposure or public_alien_awareness or mutual_contact):
        prime = "strict_non_interference"
    elif prior_alien_exposure or public_alien_awareness:
        prime = "contamination_or_prior_exposure_review"
    else:
        prime = "contact_governed_non_interference"

    scope = "planetary_possible"
    if political_representation_state in {
        "multiple_sovereign_states","contested_planetary_authority",
        "civil_war_or_fragmentation","no_single_external_representative"
    }:
        scope = "polity_or_representative_limited"

    return {
        "contact_eligibility": eligibility,
        "recommended_contact_timing": timing,
        "recommended_contact_scope": scope,
        "prime_directive_state": prime,
        "captain_decision_required": eligibility not in {"not_eligible_normal_contact"},
        "automatic_contact_forbidden": True,
    }


def generate(
    *,
    campaign_seed: str,
    world_id: str,
    civilization_slot: int,
    era_id: str,
    campaign_date: str,
    environment_class: str,
    population_band: str,
    technology_band: str,
    warp_state: str,
    political_representation_state: str,
    prior_alien_exposure: bool = False,
    public_alien_awareness: bool = False,
    active_internal_conflict: bool = False,
    mutual_contact: bool = False,
    language_samples: int = 0,
    materialization_level: str = "latent",
) -> dict[str, Any]:
    if environment_class not in ENV_MORPHOLOGY:
        raise ValueError(f"Unsupported environment class: {environment_class}")
    if population_band not in {"tiny","small","medium","large","very_large"}:
        raise ValueError(f"Unsupported population band: {population_band}")
    if technology_band not in {x["id"] for x in json.loads(TECH.read_text(encoding="utf-8"))["technology_bands"]}:
        raise ValueError(f"Unsupported technology band: {technology_band}")
    if warp_state not in WARP_ORDER:
        raise ValueError(f"Unsupported warp state: {warp_state}")
    if materialization_level not in MATERIALIZATION_ORDER:
        raise ValueError(f"Unsupported materialization level: {materialization_level}")

    civ_seed = f"{campaign_seed}|{world_id}|civilization_slot:{civilization_slot}|civilization_v0.1"
    rng = DeterministicRng(civ_seed)
    civilization_id = f"gen:civilization:{stable_token(civ_seed)}"
    population = population_estimate(rng, population_band)
    species_count = 1 if rng.randint(0, 9) < 8 else 2
    language_count = 1 if rng.randint(0, 9) < 7 else rng.randint(2, 4)

    latent = {
        "civilization_id": civilization_id,
        "world_id": world_id,
        "population_band": population_band,
        "population_estimate": population,
        "technology_band": technology_band,
        "warp_state": warp_state,
        "political_representation_state": political_representation_state,
        "species_count": species_count,
        "language_count": language_count,
        "history_seed": stable_token(civ_seed, "history", length=20),
        "culture_seed": stable_token(civ_seed, "culture", length=20),
        "economy_seed": stable_token(civ_seed, "economy", length=20),
        "settlement_distribution_seed": stable_token(civ_seed, "settlements", length=20),
    }

    result: dict[str, Any] = {
        "schema_version": "0.1.0",
        "generator": {
            "generator_id": GENERATOR_ID,
            "generator_version": GENERATOR_VERSION,
            "algorithm": "sha256_counter_v1",
        },
        "generation_context": {
            "campaign_seed": campaign_seed,
            "era_id": era_id,
            "campaign_date": campaign_date,
            "materialization_level": materialization_level,
        },
        "world_truth": latent,
        "observer_knowledge": {
            "federation_designation": f"Uncatalogued Civilization {stable_token(civilization_id, length=6).upper()}",
            "self_name_known": False,
            "known_self_name": None,
            "translation_state": translation_state(language_samples),
        },
        "first_contact": first_contact_assessment(
            warp_state=warp_state,
            prior_alien_exposure=prior_alien_exposure,
            public_alien_awareness=public_alien_awareness,
            political_representation_state=political_representation_state,
            active_internal_conflict=active_internal_conflict,
            mutual_contact=mutual_contact,
        ),
        "persistence": {
            "reroll_on_reload": False,
            "materialization_irreversible": True,
            "campaign_history_appends": True,
        },
    }

    if materialization_at_least(materialization_level, "observed"):
        result["observed_state"] = {
            "estimated_population_band": population_band,
            "observed_technology_band": technology_band,
            "observed_warp_state": warp_state,
            "detected_language_streams": min(language_count, max(1, language_samples)) if language_samples else 0,
            "observation_confidence": "medium" if language_samples < 3 else "high",
        }

    if materialization_at_least(materialization_level, "materialized"):
        species_rows = []
        for idx in range(species_count):
            srng = DeterministicRng(f"{civ_seed}|species:{idx}")
            family = srng.choice(ENV_MORPHOLOGY[environment_class])
            surface = srng.choice(SURFACE_BY_FAMILY[family])
            species_rows.append({
                "species_id": f"gen:species:{stable_token(civilization_id, str(idx))}",
                "morphology_family": family,
                "surface_cover": surface,
                "size_band": srng.choice(["small","human_comparable","large"]),
                "primary_senses": srng.choice([
                    ["vision","hearing"],["vision","hearing","chemical"],["vision","vibration"],["hearing","chemical"]
                ]),
                "respiration": "atmosphere_compatible_with_origin_world",
                "personality_lock": None,
            })

        lrng = DeterministicRng(f"{civ_seed}|language")
        language_id = f"gen:language:{stable_token(civilization_id, 'primary')}"
        language = {
            "language_id": language_id,
            "word_order": lrng.choice(WORD_ORDER),
            "writing_system_type": lrng.choice(WRITING),
            "self_name": word(lrng),
            "planet_self_name": word(lrng),
            "person_name_pattern_example": f"{word(lrng)} {word(lrng)}",
        }

        grng = DeterministicRng(f"{civ_seed}|government")
        if political_representation_state == "single_planetary_authority":
            government_count = 1
        elif political_representation_state in {"multiple_sovereign_states","contested_planetary_authority","civil_war_or_fragmentation"}:
            government_count = 3
        else:
            government_count = 2

        governments = []
        for idx in range(government_count):
            governments.append({
                "government_id": f"gen:government:{stable_token(civilization_id, str(idx))}",
                "government_type": grng.choice(GOV_TYPES),
                "display_self_name": word(grng),
                "external_representation_scope": "planetary" if government_count == 1 else "partial_polity",
            })

        srng = DeterministicRng(f"{civ_seed}|settlements")
        settlement_count = {"tiny":2,"small":3,"medium":4,"large":5,"very_large":6}[population_band]
        settlements = []
        for idx in range(settlement_count):
            stype = "capital" if idx == 0 and government_count == 1 else srng.choice(SETTLEMENT_TYPES[1:])
            settlements.append({
                "settlement_id": f"gen:settlement:{stable_token(civilization_id, str(idx))}",
                "settlement_type": stype,
                "display_self_name": word(srng),
                "persistent": True,
            })

        civilization_name = language["self_name"]
        names_known = language_samples >= 3 or materialization_level == "first_contact_preparation"
        result["materialized_civilization"] = {
            "civilization_self_name": civilization_name,
            "primary_language": language,
            "species": species_rows,
            "governments": governments,
            "major_settlements": settlements,
            "visual_profile": {
                "species_morphology_ref": species_rows[0]["species_id"],
                "technology_band": technology_band,
                "architecture_character": srng.choice([
                    "dense_vertical","low_spread","modular_functional","monumental_civic","organic_curvilinear"
                ]),
                "material_character": srng.choice([
                    "metal_ceramic","stone_composite","glass_composite","polymer_metal","mixed_local_materials"
                ]),
                "visual_profile_id": f"gen:visual_profile:{stable_token(civilization_id, 'visual')}",
            },
        }
        result["observer_knowledge"]["self_name_known"] = names_known
        result["observer_knowledge"]["known_self_name"] = civilization_name if names_known else None

    if materialization_level == "first_contact_preparation":
        mrng = DeterministicRng(f"{civ_seed}|representatives")
        governments = result["materialized_civilization"]["governments"]
        reps = []
        for idx, gov in enumerate(governments):
            reps.append({
                "character_id": f"gen:character:{stable_token(civilization_id, 'representative', str(idx))}",
                "name": word(mrng) + " " + word(mrng),
                "office": mrng.choice(["head_of_government","foreign_affairs_official","science_program_director","senior_civic_representative"]),
                "government_ref": gov["government_id"],
                "representation_scope": gov["external_representation_scope"],
                "personality_state":"resolved_separately_from_species_culture_and_office"
            })
        result["first_contact_preparation"] = {
            "representative_candidates": reps,
            "translation_state": translation_state(language_samples),
            "brief_required": True,
            "captain_decision_required": True,
        }

    return result


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    world = payload.get("world_truth", {})
    if not world.get("civilization_id", "").startswith("gen:civilization:"):
        errors.append("missing civilization id")
    if payload.get("persistence", {}).get("reroll_on_reload") is not False:
        errors.append("civilization must not reroll")
    mat = payload.get("materialized_civilization")
    if mat:
        for sp in mat.get("species", []):
            if sp.get("personality_lock") is not None:
                errors.append("species cannot lock personality")
        govs = mat.get("governments", [])
        if world.get("political_representation_state") == "multiple_sovereign_states":
            if any(g.get("external_representation_scope") == "planetary" for g in govs):
                errors.append("multi-state world cannot auto-grant planetary representation")
    if payload.get("first_contact", {}).get("automatic_contact_forbidden") is not True:
        errors.append("warp state must never auto-trigger contact")
    return errors


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", required=True)
    p.add_argument("--world-id", required=True)
    p.add_argument("--slot", type=int, default=0)
    p.add_argument("--era", default="tng_ds9_voyager")
    p.add_argument("--date", default="2372-01-01")
    p.add_argument("--environment", choices=sorted(ENV_MORPHOLOGY), default="temperate")
    p.add_argument("--population-band", choices=["tiny","small","medium","large","very_large"], default="medium")
    p.add_argument("--technology-band", required=True)
    p.add_argument("--warp-state", choices=WARP_ORDER, required=True)
    p.add_argument("--representation", required=True)
    p.add_argument("--prior-alien-exposure", action="store_true")
    p.add_argument("--public-alien-awareness", action="store_true")
    p.add_argument("--active-internal-conflict", action="store_true")
    p.add_argument("--mutual-contact", action="store_true")
    p.add_argument("--language-samples", type=int, default=0)
    p.add_argument("--materialization-level", choices=MATERIALIZATION_ORDER, default="latent")
    p.add_argument("--output", type=Path)
    p.add_argument("--validate", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    payload = generate(
        campaign_seed=args.seed, world_id=args.world_id, civilization_slot=args.slot,
        era_id=args.era, campaign_date=args.date, environment_class=args.environment,
        population_band=args.population_band, technology_band=args.technology_band,
        warp_state=args.warp_state, political_representation_state=args.representation,
        prior_alien_exposure=args.prior_alien_exposure,
        public_alien_awareness=args.public_alien_awareness,
        active_internal_conflict=args.active_internal_conflict,
        mutual_contact=args.mutual_contact,
        language_samples=args.language_samples,
        materialization_level=args.materialization_level,
    )
    if args.validate:
        errors = validate(payload)
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
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
