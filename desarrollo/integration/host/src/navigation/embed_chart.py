"""Embed the reviewed reference chart. A campaign must publish it explicitly."""
import hashlib
import json
import math
from pathlib import Path
import re
import sys

root, output = map(Path, sys.argv[1:])
navigation = root / "sistemas/gameplay/navigation"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def index(records, key):
    result = {record[key]: record for record in records}
    if len(result) != len(records):
        raise ValueError(f"duplicate {key}")
    return result


def literal(value):
    if value is None:
        return "std::nullopt"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=True)
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, list):
        return "{" + ", ".join(map(literal, value)) + "}"
    if isinstance(value, (int, float)) and math.isfinite(value):
        return repr(value)
    raise ValueError(f"unsupported chart value {value!r}")


graph = load(navigation / "anchor_route_graph.json")
distances = load(navigation / "initial_reference_distance_edges.json")
locations = load(root / "mundo/lore/astrography/systems/anchor_locations.json")
cost = load(navigation / "route_cost_model.json")
by_location = index(locations["locations"], "location_id")
by_edge = index(distances["entries"], "edge_id")
nodes = sorted(graph["nodes"])
if len(set(nodes)) != len(nodes):
    raise ValueError("duplicate chart node")
places = []
for node in nodes:
    place = by_location[node]
    places.append([node, place["display_name_es"], place["location_type"],
                   place.get("coordinates", {}).get("z_ly"), place["source_refs"]])

edges = []
for entry in graph["edges"]:
    if entry.get("enabled", True) is False:
        continue
    edge = by_edge[entry["edge_ref"]] if "edge_ref" in entry else entry
    if edge.get("usable_for_pathfinding", True) is False:
        continue
    if edge.get("valid_from") is not None or edge.get("valid_to") is not None:
        raise ValueError("dated edge requires an explicit campaign era")
    a, b = edge["origin_location_id"], edge["destination_location_id"]
    if a not in nodes or b not in nodes or a == b:
        raise ValueError(f"invalid chart endpoints {a}, {b}")
    distance = edge["distance_ly"]
    if distance is not None and (not math.isfinite(distance) or distance <= 0):
        raise ValueError("invalid distance")
    confidence = edge["confidence"]
    if confidence not in {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}:
        raise ValueError("unsupported chart confidence")
    traversal = edge.get("traversal_type", "")
    if edge.get("ordinary_warp_edge") is False and not traversal:
        raise ValueError("special edge requires a traversal type")
    sources = edge.get("source_refs", [edge["underlying_source"]] if "underlying_source" in edge else [])
    edges.append([edge["edge_id"], a, b, confidence, edge.get("distance_relation", ""),
                  edge.get("derivation_type", ""), traversal, sources, distance,
                  edge.get("directional", False)])
edges.sort()
if len({edge[0] for edge in edges}) != len(edges):
    raise ValueError("duplicate chart edge")
for item in places + edges:
    if not re.fullmatch(r"[a-z][a-z0-9_]*", item[0]):
        raise ValueError("invalid chart definition ID")
profiles = sorted((name, weights["uncertainty_weight"])
                  for name, weights in cost["preference_profiles"].items())
if any(not math.isfinite(weight) or weight < 0 for _, weight in profiles):
    raise ValueError("invalid uncertainty weight")
projection = json.dumps([places, edges, profiles], ensure_ascii=True, separators=(",", ":"))
digest = hashlib.sha256(projection.encode("ascii")).hexdigest()
publication = f'{graph["graph_id"]}@{graph["schema_version"]}+{digest}'
# The persistent stamp is stored as five scalar self-edges and a final 16-bit chunk.
parts = [int(digest[i:i+12], 16) for i in range(0, len(digest), 12)]
lines = [
    "#pragma once",
    '#include "trek/host/navigation.h"',
    "#include <array>",
    "namespace trek::host::chart_data {",
    f"inline constexpr char publication[] = {literal(publication)};",
    "inline constexpr std::array<std::uint64_t, 6> stamp" + literal(parts) + ";",
    "inline const ChartPlace places[] = {",
    *("    " + literal(place) + "," for place in places),
    "};",
    "inline const ChartEdge edges[] = {",
    *("    " + literal(edge) + "," for edge in edges),
    "};",
    "struct Profile { const char* id; double uncertainty_weight; };",
    "inline constexpr Profile profiles[] = {",
    *("    " + literal(list(profile)) + "," for profile in profiles),
    "};",
    "}",
]
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n".join(lines) + "\n", encoding="utf-8")
