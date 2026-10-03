#!/usr/bin/env python3
"""Validate selected cross-file references in the Star Trek universe pack."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = ROOT / "sources/source_registry/source_registry.json"
DISTANCES = ROOT / "gameplay/navigation/initial_reference_distance_edges.json"
LOCATIONS = ROOT / "lore/astrography/systems/anchor_locations.json"
RELATIONS = ROOT / "gameplay/diplomacy/federation_relation_anchors.json"
WORLD_EVENTS = ROOT / "narrative/events/world_event_state.json"
OPERATIONAL_NEEDS = ROOT / "gameplay/command/operational_need_model.json"

SCAN_ROOTS = (
    ROOT / "gameplay",
    ROOT / "lore",
    ROOT / "narrative",
    ROOT / "ai",
    ROOT / "universe",
    ROOT / "validation",
)

SOURCE_SINGLE_KEYS = {"source_ref", "source_id", "underlying_source"}
SOURCE_LIST_KEYS = {"source_refs", "source_ids", "sources"}
LOCATION_KEYS = {
    "origin_location_id",
    "destination_location_id",
    "from_location_id",
    "to_location_id",
    "homeworld_id",
    "common_homeworld_id",
}
DESCRIPTOR_UNDERLYING_SOURCES = {"real_star", "40_eridani_reference"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def json_files() -> Iterable[Path]:
    for root in SCAN_ROOTS:
        if root.exists():
            yield from root.rglob("*.json")


def build_indexes():
    registry = load_json(REGISTRY)
    source_ids = {row["source_id"] for row in registry.get("sources", [])}

    distances = load_json(DISTANCES)
    edge_ids = {row["edge_id"] for row in distances.get("entries", [])}

    locations = load_json(LOCATIONS)
    location_ids = {row["location_id"] for row in locations.get("locations", [])}

    relations = load_json(RELATIONS)
    relation_ids = set()
    for relation in relations.get("relations", []):
        pair = "__".join(relation.get("pair", []))
        for anchor in relation.get("anchors", []):
            relation_ids.add(f"{pair}__{anchor['year']}")

    world_events = load_json(WORLD_EVENTS)
    world_event_types = set(world_events.get("event_types", []))

    operational_needs = load_json(OPERATIONAL_NEEDS)
    operational_need_types = set(operational_needs.get("need_types", []))

    return (
        source_ids,
        edge_ids,
        location_ids,
        relation_ids,
        world_event_types,
        operational_need_types,
    )


def walk(
    value: Any,
    *,
    file_path: Path,
    json_path: str,
    source_ids: set[str],
    edge_ids: set[str],
    location_ids: set[str],
    relation_ids: set[str],
    world_event_types: set[str],
    operational_need_types: set[str],
    errors: list[str],
) -> None:
    if isinstance(value, list):
        for index, item in enumerate(value):
            walk(
                item,
                file_path=file_path,
                json_path=f"{json_path}[{index}]",
                source_ids=source_ids,
                edge_ids=edge_ids,
                location_ids=location_ids,
                relation_ids=relation_ids,
                world_event_types=world_event_types,
                operational_need_types=operational_need_types,
                errors=errors,
            )
        return

    if not isinstance(value, dict):
        return

    for key, item in value.items():
        item_path = f"{json_path}.{key}"

        if key in SOURCE_SINGLE_KEYS and isinstance(item, str):
            validate = True
            if key == "underlying_source":
                validate = (
                    item not in DESCRIPTOR_UNDERLYING_SOURCES
                    and item.upper() == item
                    and "_" in item
                )
            if validate and item not in source_ids:
                errors.append(
                    f"{file_path.relative_to(ROOT)} {item_path}: "
                    f"unknown source id '{item}'"
                )

        if key in SOURCE_LIST_KEYS and isinstance(item, list):
            for source_id in item:
                if isinstance(source_id, str) and source_id not in source_ids:
                    errors.append(
                        f"{file_path.relative_to(ROOT)} {item_path}: "
                        f"unknown source id '{source_id}'"
                    )

        if key == "edge_ref" and isinstance(item, str) and item not in edge_ids:
            errors.append(
                f"{file_path.relative_to(ROOT)} {item_path}: "
                f"unknown edge id '{item}'"
            )

        if key in LOCATION_KEYS and isinstance(item, str) and item not in location_ids:
            errors.append(
                f"{file_path.relative_to(ROOT)} {item_path}: "
                f"unknown location id '{item}'"
            )

        if (
            key == "relation_state_ref"
            and isinstance(item, str)
            and item not in relation_ids
        ):
            errors.append(
                f"{file_path.relative_to(ROOT)} {item_path}: "
                f"unknown relation anchor '{item}'"
            )

        if (
            key == "world_event_type"
            and isinstance(item, str)
            and item not in world_event_types
        ):
            errors.append(
                f"{file_path.relative_to(ROOT)} {item_path}: "
                f"unknown world-event type '{item}'"
            )

        if key == "possible_needs" and isinstance(item, list):
            for need_type in item:
                if (
                    isinstance(need_type, str)
                    and need_type not in operational_need_types
                ):
                    errors.append(
                        f"{file_path.relative_to(ROOT)} {item_path}: "
                        f"unknown operational-need type '{need_type}'"
                    )

        walk(
            item,
            file_path=file_path,
            json_path=item_path,
            source_ids=source_ids,
            edge_ids=edge_ids,
            location_ids=location_ids,
            relation_ids=relation_ids,
            world_event_types=world_event_types,
            operational_need_types=operational_need_types,
            errors=errors,
        )


def main() -> int:
    (
        source_ids,
        edge_ids,
        location_ids,
        relation_ids,
        world_event_types,
        operational_need_types,
    ) = build_indexes()

    errors: list[str] = []
    scanned = 0

    for path in json_files():
        scanned += 1
        try:
            payload = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid/unreadable JSON: {exc}")
            continue

        walk(
            payload,
            file_path=path,
            json_path="$",
            source_ids=source_ids,
            edge_ids=edge_ids,
            location_ids=location_ids,
            relation_ids=relation_ids,
            world_event_types=world_event_types,
            operational_need_types=operational_need_types,
            errors=errors,
        )

    print(
        "Reference validation: "
        f"{scanned} JSON files; "
        f"{len(source_ids)} sources; "
        f"{len(edge_ids)} distance edges; "
        f"{len(location_ids)} anchor locations; "
        f"{len(relation_ids)} relation anchors; "
        f"{len(world_event_types)} world-event types; "
        f"{len(operational_need_types)} operational-need types."
    )

    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for error in errors:
            print(f" - {error}")
        return 1

    print("OK: no checked dangling references found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
