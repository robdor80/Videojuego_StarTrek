"""Embed the reviewed F10 policy and the exact S04 source documents."""
import hashlib
import json
from pathlib import Path
import sys


def main(root, output):
    policy_path = root / "sistemas/gameplay/careers/academy_path/f10_fixed_candidate_factory_contract_v2.json"
    policy = policy_path.read_text(encoding="utf-8")
    sources = json.loads(policy)["source"]
    documents = {"policy": policy}
    for key in ("s04_contract", "s04_biography"):
        source = sources[key]
        document = (root / source["path"]).read_text(encoding="utf-8")
        if hashlib.sha256(document.encode("utf-8")).hexdigest() != source["sha256"]:
            raise ValueError(f"Unapproved S04 source: {source['path']}")
        documents[key] = document

    lines = ["#pragma once", "#include <string_view>", "namespace trek::host::detail::fixed_candidate_data {"]
    for key, document in documents.items():
        delimiter = "TREK_F10"
        if f'){delimiter}"' in document:
            raise ValueError(f"Invalid raw string delimiter in {key}")
        lines.append(f'inline constexpr std::string_view {key} = R"{delimiter}({document}){delimiter}";')
    lines.append("}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
