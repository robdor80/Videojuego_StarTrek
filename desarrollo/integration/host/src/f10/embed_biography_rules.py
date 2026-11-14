"""Embed versioned F10 validation data. The installed module reads no draft or rules files."""
import hashlib
import json
from pathlib import Path
import sys


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def maturity_rules(policy, campaign, species):
    if (policy["contract_id"], policy["schema_version"]) != ("f10_species_playable_maturity_policy", "0.1.0"):
        raise ValueError("Unsupported playable maturity contract")
    scope = policy["scope"]
    if (scope["scenario_id"] != campaign["scenario_id"] or scope["era_id"] != campaign["era_id"]
            or type(scope["campaign_start_year"]) is not int
            or scope["campaign_start_year"] != campaign["approved_start_year"]
            or scope["campaign_start_month_day"] != campaign["start_month_day"]
            or scope["campaign_start_month_day"] != "UNDECIDED_BY_AUTHOR"
            or scope["age_unit"] != "EARTH_YEARS" or scope["subject"] != "INITIAL_PLAYER_CHARACTER"
            or scope["owner"] != "F10"):
        raise ValueError("Playable maturity policy does not match the supported campaign")
    if (policy["content_gates"]["DLC_DELTA"] != "NOT_AVAILABLE_IN_MAIN_GAME_DLC_NOT_IMPLEMENTED"
            or policy["integration"]["semantic_ai_review_still_mandatory"] is not True):
        raise ValueError("Unsupported playable maturity gate")
    for invariant in ("minimum_not_sufficient_proof_of_maturity", "adulthood_client_claim_not_evidence",
                      "applicable_species_profile_and_individual_maturity_evidence_required", "no_fixed_maximum_age"):
        if policy["rules"][invariant] is not True:
            raise ValueError(f"Unsupported playable maturity invariant: {invariant}")

    rules = {}
    special_count = delta_count = 0
    for row in policy["species"]:
        species_id = row["species_id"]
        if species_id not in species or species_id in rules:
            raise ValueError(f"Unknown or duplicate playable species: {species_id}")
        profile_ref, profile = species[species_id]
        if (row["profile_ref"] != profile_ref or row["automatic_player_eligibility"] is not False
                or row["maturity_evidence_required"] is not True
                or row["maximum_playable_age_earth_years"] is not None):
            raise ValueError(f"Invalid playable maturity constraints: {species_id}")

        availability = profile.get("content_availability", {})
        dlc = availability.get("content_id") == "dlc_delta_transwarp"
        if (row["content_scope"] != ("DLC_DELTA" if dlc else "MAIN_GAME")
                or (dlc and (availability["gameplay_spawn_in_main"] is not False
                             or availability["dlc_not_yet_implemented"] is not True))):
            raise ValueError(f"Playable content scope conflicts with profile: {species_id}")
        delta_count += dlc

        minimum = row["minimum_playable_age_earth_years"]
        rule_type = row["age_rule_type"]
        if rule_type == "SPECIAL_REVIEW_REQUIRED":
            blocker = row["special_blocker"]
            if minimum is not None or not isinstance(blocker, str) or not blocker.strip():
                raise ValueError(f"Invalid special maturity rule: {species_id}")
            special_count += 1
        elif (rule_type != "NUMERIC_PLAYABLE_FLOOR" or type(minimum) is not int
              or not 0 < minimum < 2**31 or "special_blocker" in row):
            raise ValueError(f"Invalid numeric maturity floor: {species_id}")
        rules[species_id] = {"minimum": minimum, "delta_dlc": dlc}

    if rules.keys() != species.keys() or (len(rules), special_count, delta_count) != (25, 3, 5):
        raise ValueError("Playable maturity policy must cover the approved 25 species, including 3 special rules and 5 Delta profiles")
    return rules


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: embed_biography_rules.py REPOSITORY_ROOT OUTPUT_HEADER")
    root, output = map(Path, sys.argv[1:])
    systems = root / "sistemas/gameplay"
    creation = systems / "character_creation"
    profiles = systems / "species/profiles"
    sources = {}

    def read(path):
        text = path.read_text(encoding="utf-8")
        value = json.loads(text, object_pairs_hook=unique_object) if path.suffix == ".json" else text
        sources[path.relative_to(root).as_posix()] = value
        return value

    fields = read(creation / "character_creation_contract_v1_0.json")
    interface = read(creation / "f10_biography_validation_interface_v0.1.json")
    activity = read(creation / "prior_activity_model.json")
    candidate = read(systems / "careers/academy_path/f10_host_candidate_factory_contract_v0.1.json")
    maturity = read(creation / "f10_species_maturity_policy_v0.1.json")
    technology = read(systems / "ship_operations/era_technology_matrix.json")
    for path in (
        creation / "biography_validation_rules.md",
        creation / "player_profile_contract.json",
        systems / "organizations/character_affiliation_citizenship_contract.json",
        systems / "species/species_biology_contract.json",
    ):
        read(path)

    species = {}
    for path in sorted(profiles.glob("*_v0.1.json")):
        profile = read(path)
        if profile.get("profile_type") == "transformative_character_state_not_species":
            if "species_id" in profile:
                raise ValueError("Transformative state cannot supply a species identity")
            continue
        if "species_id" not in profile:
            raise ValueError("Unrecognized profile without species identity")
        species_id = profile["species_id"]
        if path.name != f"{species_id}_v0.1.json" or species_id in species:
            raise ValueError("Invalid species profile identity")
        species[species_id] = (path.relative_to(root).as_posix(), profile)

    def canonical(value):
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)

    data = {
        "required": fields["required_character_fields"],
        "optional": fields["optional_character_fields"],
        "forbidden": (candidate["player_input_contract"]["forbidden_client_fields"]
                      + fields["forbidden_creation_mechanics"]),
        "species": maturity_rules(maturity, candidate["campaign"], species),
        "maturity_policy": maturity["contract_id"] + "/" + maturity["schema_version"],
        "activity_categories": activity["categories"],
        "technology": technology["profiles"],
        "scenario": candidate["campaign"],
        "policy": interface["contract_id"] + "/" + interface["schema_version"],
        "sources_sha256": hashlib.sha256(canonical(sources).encode("ascii")).hexdigest(),
    }
    payload = canonical(data)
    if ')f10_rules"' in payload:
        raise ValueError("Unsafe raw string delimiter")
    output.write_text(
        '#pragma once\nnamespace trek::f10::detail {\n'
        'inline constexpr char biography_rules_json[] = R"f10_rules('
        + payload + ')f10_rules";\n}\n',
        encoding="ascii",
    )


if __name__ == "__main__":
    main()
