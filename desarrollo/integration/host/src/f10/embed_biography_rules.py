"""Embed versioned F10 validation data. The installed module reads no draft or rules files."""
import hashlib
import json
from pathlib import Path
import sys


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
        value = json.loads(text) if path.suffix == ".json" else text
        sources[path.relative_to(root).as_posix()] = value
        return value

    fields = read(creation / "character_creation_contract_v1_0.json")
    interface = read(creation / "f10_biography_validation_interface_v0.1.json")
    activity = read(creation / "prior_activity_model.json")
    candidate = read(systems / "careers/academy_path/f10_host_candidate_factory_contract_v0.1.json")
    technology = read(systems / "ship_operations/era_technology_matrix.json")
    for path in (
        creation / "biography_validation_rules.md",
        creation / "player_profile_contract.json",
        systems / "organizations/character_affiliation_citizenship_contract.json",
        systems / "species/species_biology_contract.json",
    ):
        read(path)

    species = []
    for path in sorted(profiles.glob("*_v0.1.json")):
        profile = read(path)
        if "species_id" in profile:
            species.append(profile["species_id"])
            if path.name != f"{species[-1]}_v0.1.json":
                raise ValueError("Invalid species profile identity")
        elif profile.get("profile_type") != "transformative_character_state_not_species":
            raise ValueError("Unrecognized profile without species identity")
    if not species or len(set(species)) != len(species):
        raise ValueError("Invalid species catalog")

    def canonical(value):
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    data = {
        "required": fields["required_character_fields"],
        "optional": fields["optional_character_fields"],
        "forbidden": (candidate["player_input_contract"]["forbidden_client_fields"]
                      + fields["forbidden_creation_mechanics"]),
        "species": sorted(species),
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
