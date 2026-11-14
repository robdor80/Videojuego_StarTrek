"""Exercise the build-time F10 generator against copies of its authoring inputs."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main(source):
    gameplay = Path("sistemas/gameplay")
    policy_path = gameplay / "character_creation/f10_species_maturity_policy_v0.1.json"
    generator = source / "desarrollo/integration/host/src/f10/embed_biography_rules.py"

    with tempfile.TemporaryDirectory(prefix="biography-rules-", dir=Path.cwd()) as scratch:
        root = Path(scratch)
        for directory in ("character_creation", "species"):
            shutil.copytree(source / gameplay / directory, root / gameplay / directory)
        for name in (
            "careers/academy_path/f10_host_candidate_factory_contract_v0.1.json",
            "ship_operations/era_technology_matrix.json",
            "organizations/character_affiliation_citizenship_contract.json",
        ):
            path = gameplay / name
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / path, root / path)

        policy_path = root / policy_path
        approved = json.loads(policy_path.read_text(encoding="utf-8"))
        policy = copy.deepcopy(approved)
        header = root / "rules.h"

        def generate(error=None):
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(generator), str(root), str(header)], capture_output=True, text=True,
            )
            if error is not None:
                assert result.returncode != 0 and error in result.stderr, result.stderr
                return None
            assert result.returncode == 0, result.stderr
            return json.loads(header.read_text(encoding="ascii").split('R"f10_rules(', 1)[1].split(')f10_rules"', 1)[0])

        original = generate()
        human = next(row for row in policy["species"] if row["species_id"] == "human")
        human["minimum_playable_age_earth_years"] += 1
        updated = generate()
        assert updated["species"]["human"]["minimum"] == human["minimum_playable_age_earth_years"]
        assert updated["sources_sha256"] != original["sources_sha256"]
        assert updated["maturity_policy"] == original["maturity_policy"]

        human["minimum_playable_age_earth_years"] = True
        generate("Invalid numeric maturity floor")
        human["minimum_playable_age_earth_years"] = original["species"]["human"]["minimum"]
        human["maximum_playable_age_earth_years"] = 130
        generate("Invalid playable maturity constraints")
        human["maximum_playable_age_earth_years"] = None
        human["profile_ref"] = "sistemas/gameplay/species/profiles/vulcan_v0.1.json"
        generate("Invalid playable maturity constraints")

        policy = copy.deepcopy(approved)
        next(row for row in policy["species"] if row["species_id"] == "ocampan")["content_scope"] = "MAIN_GAME"
        generate("Playable content scope conflicts with profile")
        policy = copy.deepcopy(approved)
        policy["species"].pop()
        generate("must cover the approved 25 species")
        policy["species"].append(policy["species"][0])
        generate("Unknown or duplicate playable species")

        policy = copy.deepcopy(approved)
        policy["scope"]["campaign_start_year"] += 1
        generate("does not match the supported campaign")
        policy = copy.deepcopy(approved)
        policy["schema_version"] = "99.0.0"
        generate("Unsupported playable maturity contract")

        policy = copy.deepcopy(approved)
        evidence_path = policy_path.with_name("f10_biography_evidence_semantic_boundary_v0.1.json")
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence["evidence_model"]["initial_character_bootstrap"] += " Revised."
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
        updated = generate()
        assert updated["sources_sha256"] != original["sources_sha256"]
        assert updated["evidence_policy"] == original["evidence_policy"]
        evidence["schema_version"] = "99.0.0"
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
        generate("Unsupported biography evidence policy")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
