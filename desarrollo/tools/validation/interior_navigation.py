"""MAP-01: deterministic interior graph validation and route planning (stdlib only).

Not an UE5/World State integration. Never assumes an unverified link exists.
Caller must supply current access/blocked links from authoritative game state.
"""
from __future__ import annotations

import heapq
import json
from pathlib import Path


class MapValidationError(ValueError):
    pass


def validate_map(graph: dict) -> None:
    if graph.get("schema_version") != "0.1.0":
        raise MapValidationError("unsupported schema_version")
    if not graph.get("ship_id") or not graph.get("map_revision"):
        raise MapValidationError("missing ship_id/map_revision")
    locations = graph.get("locations")
    links = graph.get("links")
    if not isinstance(locations, list) or not isinstance(links, list):
        raise MapValidationError("locations and links must be arrays")
    ids = set()
    for loc in locations:
        if not isinstance(loc, dict) or any(not loc.get(k) for k in
                                            ("location_id", "display_es", "deck_or_section", "location_type")):
            raise MapValidationError("incomplete location")
        lid = loc["location_id"]
        if not isinstance(lid, str) or lid in ids:
            raise MapValidationError("duplicate/invalid location_id")
        ids.add(lid)
    link_ids = set()
    allowed = {"walk", "door", "stairs", "turbolift", "virtual_transition"}
    for link in links:
        if not isinstance(link, dict) or not isinstance(link.get("link_id"), str):
            raise MapValidationError("invalid link")
        if link["link_id"] in link_ids:
            raise MapValidationError("duplicate link_id")
        link_ids.add(link["link_id"])
        if link.get("from") not in ids or link.get("to") not in ids:
            raise MapValidationError("link references missing location")
        if link["from"] == link["to"]:
            raise MapValidationError("self-link")
        if link.get("mode") not in allowed:
            raise MapValidationError("invalid travel mode")
        if link.get("verified") is not True:
            raise MapValidationError("unverified link cannot be routed")
        cost = link.get("cost", 1)
        if isinstance(cost, bool) or not isinstance(cost, (int, float)) or not (0 < cost < float("inf")):
            raise MapValidationError("invalid link cost")
        if "bidirectional" in link and not isinstance(link["bidirectional"], bool):
            raise MapValidationError("invalid bidirectional flag")


def route(graph: dict, origin: str, destination: str, *,
          permitted_locations: set[str], blocked_links: set[str] | None = None) -> list[str] | None:
    """Return location IDs of shortest permitted route; None means no authorised path.

    Permissions are fail-closed: the caller supplies an authoritative allowlist.
    A separate World State service must supply current NPC locations.
    """
    validate_map(graph)
    known = {x["location_id"] for x in graph["locations"]}
    if origin not in known or destination not in known:
        return None
    if origin not in permitted_locations or destination not in permitted_locations:
        return None
    if origin == destination:
        return [origin]
    blocked = blocked_links or set()
    adjacency: dict[str, list[tuple[str, float]]] = {key: [] for key in known}
    for link in graph["links"]:
        if link["link_id"] in blocked:
            continue
        a, b = link["from"], link["to"]
        if a not in permitted_locations or b not in permitted_locations:
            continue
        cost = link.get("cost", 1)
        adjacency[a].append((b, cost))
        if link.get("bidirectional", False):
            adjacency[b].append((a, cost))
    frontier = [(0.0, origin)]
    distance = {origin: 0.0}
    previous: dict[str, str] = {}
    while frontier:
        dist, current = heapq.heappop(frontier)
        if dist > distance[current]:
            continue
        if current == destination:
            result = [current]
            while current in previous:
                current = previous[current]
                result.append(current)
            return list(reversed(result))
        for neighbor, cost in adjacency[current]:
            candidate = dist + cost
            if candidate < distance.get(neighbor, float("inf")):
                distance[neighbor] = candidate
                previous[neighbor] = current
                heapq.heappush(frontier, (candidate, neighbor))
    return None


def load_map(path: str | Path) -> dict:
    graph = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_map(graph)
    return graph
