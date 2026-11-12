#!/usr/bin/env python3
"""Planificación 2/B04: deterministic Star Trek living-economy REFERENCE, not CoreRPG runtime.

Only explicit, authorized events can transform candidate state. No random spawns,
global schedule, history synthesis, universal currency or authority bypass.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

VERSION = "0.1.0"
KINDS = {"produce", "replicate", "consume", "dispatch", "deliver", "trade",
         "set_route_access", "loss"}
CONSIDERATION = {"gift", "allocation", "barter", "service", "latinum", "local_currency"}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def integer(value: Any, name: str, *, positive: bool = False) -> int:
    require(type(value) is int and value >= (1 if positive else 0),
            f"{name} must be a nonnegative integer" + (" > 0" if positive else ""))
    return value


def label(value: Any, name: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{name} missing")
    return value


def stock(store: dict[str, Any], item: str) -> int:
    return integer(store["stock"].get(item, 0), f"stock.{item}")


def decrement(store: dict[str, Any], item: str, qty: int) -> None:
    require(stock(store, item) >= qty, "insufficient stock")
    store["stock"][item] = stock(store, item) - qty


def increment(store: dict[str, Any], item: str, qty: int) -> None:
    store["stock"][item] = stock(store, item) + qty


def entry(mapping: dict[str, Any], ref: str, category: str) -> dict[str, Any]:
    label(ref, category)
    require(ref in mapping, f"unknown {category}: {ref}")
    return mapping[ref]


def digest(obj: dict[str, Any]) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def validate_state(s: dict[str, Any]) -> None:
    required = {"stores", "facilities", "routes", "vessels", "shipments",
                "wallets", "event_log", "last_tick"}
    require(required <= s.keys(), "state missing required collections")
    integer(s["last_tick"], "last_tick")
    require(isinstance(s["event_log"], list), "event_log must be a list")
    ids = [e["event_id"] for e in s["event_log"]]
    require(len(ids) == len(set(ids)), "duplicate event ID in log")
    for store_id, store in s["stores"].items():
        label(store_id, "store_id")
        label(store["owner_ref"], "owner_ref")
        label(store["location_ref"], "location_ref")
        for item, qty in store["stock"].items():
            label(item, "item")
            integer(qty, f"store.{store_id}.{item}")
    for facility_id, f in s["facilities"].items():
        entry(s["stores"], f["store_id"], "facility.store")
        integer(f["power_units"], f"{facility_id}.power_units")
        integer(f["feedstock"], f"{facility_id}.feedstock")
    for wallet_id, w in s["wallets"].items():
        label(wallet_id, "wallet")
        label(w["unit"], "currency unit")
        integer(w["balance"], "balance")
    for shipment_id, sh in s["shipments"].items():
        require(shipment_id == sh["shipment_id"], "shipment identity mismatch")
        integer(sh["quantity"], "shipment quantity", positive=True)
        integer(sh["arrival_tick"], "shipment arrival")
        require(sh["status"] == "in_transit", "delivered shipments must leave active set")
    for v in s["vessels"].values():
        label(v["location_ref"], "vessel location")
        integer(v["capacity"], "vessel capacity", positive=True)
    for r in s["routes"].values():
        label(r["from_location"], "route origin")
        label(r["to_location"], "route destination")
        integer(r["capacity"], "route capacity", positive=True)
        integer(r["min_travel_ticks"], "travel time", positive=True)


def _production(s: dict[str, Any], e: dict[str, Any], replicate: bool) -> dict[str, Any]:
    f = entry(s["facilities"], e["facility_id"], "facility")
    require(f["operational"] is True, "facility unavailable")
    store = entry(s["stores"], f["store_id"], "facility store")
    qty = integer(e["quantity"], "quantity", positive=True)
    item = label(e["item"], "item")
    max_batch = integer(f["max_batch"], "maximum batch", positive=True)
    require(qty <= max_batch, "facility batch exceeds capacity")
    if replicate:
        require(item in f["patterns"], "replication pattern unavailable")
        profile = entry(f["replication_profiles"], item, "replication profile")
        require(profile.get("permitted") is True, "replication not permitted")
        energy = integer(profile["power_per_unit"], "replication energy", positive=True) * qty
        feedstock = integer(profile["feedstock_per_unit"], "replication feedstock", positive=True) * qty
        require(f["power_units"] >= energy, "insufficient power")
        require(f["feedstock"] >= feedstock, "insufficient feedstock")
        f["power_units"] -= energy
        f["feedstock"] -= feedstock
        made = qty
    else:
        recipe = entry(f["production_recipes"], item, "production recipe")
        require(label(e["labor_ref"], "labor_ref"), "labor needed")
        energy = integer(recipe["power_per_batch_unit"], "production energy", positive=True) * qty
        inputs = recipe["inputs"]
        require(inputs, "production without material inputs")
        require(f["power_units"] >= energy, "insufficient power")
        for material, units in inputs.items():
            per_unit = integer(units, "material units", positive=True)
            require(stock(store, material) >= per_unit * qty, "insufficient raw material")
        for material, units in inputs.items():
            decrement(store, material, units * qty)
        f["power_units"] -= energy
        made = integer(recipe["yield_per_batch_unit"], "production yield", positive=True) * qty
    increment(store, item, made)
    return {"store_id": f["store_id"], "item": item, "produced": made,
            "source": "replication" if replicate else "material_production"}


def _consume(s: dict[str, Any], e: dict[str, Any], loss: bool) -> dict[str, Any]:
    label(e["cause_ref"], "cause_ref")
    store = entry(s["stores"], e["store_id"], "store")
    qty = integer(e["quantity"], "quantity", positive=True)
    item = label(e["item"], "item")
    decrement(store, item, qty)
    return {"store_id": e["store_id"], "item": item, "quantity": qty,
            "kind": "loss" if loss else "consumption", "cause_ref": e["cause_ref"]}


def _dispatch(s: dict[str, Any], e: dict[str, Any]) -> dict[str, Any]:
    label(e["operator_ref"], "operator_ref")
    label(e["agreement_ref"], "agreement_ref")
    src = entry(s["stores"], e["from_store"], "origin store")
    dst = entry(s["stores"], e["to_store"], "destination store")
    route = entry(s["routes"], e["route_id"], "route")
    vessel = entry(s["vessels"], e["vessel_id"], "vessel")
    shipment_id = label(e["shipment_id"], "shipment_id")
    require(shipment_id not in s["shipments"], "shipment ID already exists")
    require(route["from_location"] == src["location_ref"] and
            route["to_location"] == dst["location_ref"], "route does not connect stores")
    require(route["open"] is True and route["legal_access"] is True,
            "route closed or legally inaccessible")
    require(vessel["available"] is True and
            vessel["location_ref"] == src["location_ref"], "vessel not available at origin")
    qty = integer(e["quantity"], "quantity", positive=True)
    item = label(e["item"], "item")
    require(qty <= vessel["capacity"] and qty <= route["capacity"], "cargo over capacity")
    decrement(src, item, qty)
    vessel["available"] = False
    sh = {"shipment_id": shipment_id, "from_store": e["from_store"],
          "to_store": e["to_store"], "vessel_id": e["vessel_id"],
          "route_id": e["route_id"], "item": item, "quantity": qty,
          "arrival_tick": e["tick"] + route["min_travel_ticks"],
          "status": "in_transit", "cause_event_ref": e["event_id"],
          "agreement_ref": e["agreement_ref"]}
    s["shipments"][shipment_id] = sh
    return {"shipment_id": shipment_id, "arrival_tick": sh["arrival_tick"],
            "stock_location": "in_transit"}


def _deliver(s: dict[str, Any], e: dict[str, Any]) -> dict[str, Any]:
    sh = entry(s["shipments"], e["shipment_id"], "shipment")
    route = entry(s["routes"], sh["route_id"], "shipment route")
    require(e["tick"] >= sh["arrival_tick"], "shipment not yet due")
    require(route["open"] is True and route["legal_access"] is True,
            "delivery held: route closed or access revoked")
    dst = entry(s["stores"], sh["to_store"], "destination store")
    vessel = entry(s["vessels"], sh["vessel_id"], "shipment vessel")
    increment(dst, sh["item"], sh["quantity"])
    vessel["location_ref"] = dst["location_ref"]
    vessel["available"] = True
    del s["shipments"][e["shipment_id"]]
    return {"shipment_id": e["shipment_id"], "delivered": sh["quantity"],
            "item": sh["item"], "destination": sh["to_store"]}


def _trade(s: dict[str, Any], e: dict[str, Any]) -> dict[str, Any]:
    src = entry(s["stores"], e["seller_store"], "seller store")
    dst = entry(s["stores"], e["buyer_store"], "buyer store")
    require(e["seller_store"] != e["buyer_store"], "buyer and seller stores must differ")
    require(src["location_ref"] == dst["location_ref"], "remote trade requires shipping")
    label(e["seller_acceptance_ref"], "seller acceptance")
    label(e["buyer_acceptance_ref"], "buyer acceptance")
    consideration = e["consideration"]
    mode = label(consideration["mode"], "consideration mode")
    require(mode in CONSIDERATION, "unknown or unsupported consideration model")
    qty = integer(e["quantity"], "quantity", positive=True)
    item = label(e["item"], "item")
    require(stock(src, item) >= qty, "insufficient seller inventory")
    if mode in {"latinum", "local_currency"}:
        buyer = entry(s["wallets"], consideration["buyer_wallet"], "buyer wallet")
        seller = entry(s["wallets"], consideration["seller_wallet"], "seller wallet")
        unit = label(consideration["unit"], "unit")
        require(buyer["unit"] == seller["unit"] == unit, "missing explicit common accounting unit")
        amount = integer(consideration["amount"], "price amount", positive=True)
        require(buyer["balance"] >= amount, "insufficient funds")
        buyer["balance"] -= amount
        seller["balance"] += amount
    elif mode == "barter":
        bar_item = label(consideration["item"], "barter item")
        bar_qty = integer(consideration["quantity"], "barter qty", positive=True)
        require(stock(dst, bar_item) >= bar_qty, "barter goods unavailable")
        decrement(dst, bar_item, bar_qty)
        increment(src, bar_item, bar_qty)
    else:
        label(consideration.get("basis_ref"), "allocation/service/gift basis")
    decrement(src, item, qty)
    increment(dst, item, qty)
    return {"item": item, "quantity": qty, "consideration_model": mode,
            "seller_store": e["seller_store"], "buyer_store": e["buyer_store"]}


def _route_access(s: dict[str, Any], e: dict[str, Any]) -> dict[str, Any]:
    label(e["policy_ref"], "route policy_ref")
    route = entry(s["routes"], e["route_id"], "route")
    require(type(e["open"]) is bool and type(e["legal_access"]) is bool,
            "route open/legal_access must be explicit boolean values")
    route["open"], route["legal_access"] = e["open"], e["legal_access"]
    return {"route_id": e["route_id"], "open": route["open"],
            "legal_access": route["legal_access"], "policy_ref": e["policy_ref"]}


def apply_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    """Atomic, idempotent reference state transition; raises ValueError without mutating input."""
    validate_state(state)
    event_id = label(event.get("event_id"), "event_id")
    kind = label(event.get("kind"), "kind")
    require(kind in KINDS, "unknown event kind")
    tick = integer(event.get("tick"), "tick")
    label(event.get("authority_ref"), "authority_ref")
    fingerprint = digest(event)
    for existing in state["event_log"]:
        if existing["event_id"] == event_id:
            require(existing["digest"] == fingerprint, "event ID collision with divergent payload")
            return copy.deepcopy(state)
    require(tick >= state["last_tick"], "time regression")
    s = copy.deepcopy(state)
    if kind == "produce":
        effect = _production(s, event, False)
    elif kind == "replicate":
        effect = _production(s, event, True)
    elif kind in {"consume", "loss"}:
        effect = _consume(s, event, kind == "loss")
    elif kind == "dispatch":
        effect = _dispatch(s, event)
    elif kind == "deliver":
        effect = _deliver(s, event)
    elif kind == "trade":
        effect = _trade(s, event)
    else:
        effect = _route_access(s, event)
    s["event_log"].append({"event_id": event_id, "kind": kind, "tick": tick,
                           "digest": fingerprint, "effect": effect})
    s["last_tick"] = tick
    validate_state(s)
    return s


def replay(state: dict[str, Any], events: list[dict[str, Any]], *, lod: str = "high") -> dict[str, Any]:
    """LOD is intentionally presentation-only for fixed explicit event input."""
    require(lod in {"high", "low", "offscreen"}, "invalid LOD")
    out = copy.deepcopy(state)
    for event in events:
        out = apply_event(out, event)
    return out


def total_item(state: dict[str, Any], item: str) -> int:
    """Conserve item units across stores + in-transit when no production, consumption, loss."""
    return sum(stock(s, item) for s in state["stores"].values()) + sum(
        sh["quantity"] for sh in state["shipments"].values() if sh["item"] == item
    )


def shortage_view(state: dict[str, Any], demands: dict[str, dict[str, int]]) -> list[dict[str, Any]]:
    """Observation candidate only: a forecast does NOT mutate authoritative state."""
    results = []
    for store_id, wanted in sorted(demands.items()):
        st = entry(state["stores"], store_id, "demand store")
        for item, required in sorted(wanted.items()):
            integer(required, "forecast demand")
            on_hand = stock(st, item)
            results.append({"store_id": store_id, "item": item, "on_hand": on_hand,
                            "demand": required, "unmet": max(0, required - on_hand),
                            "resolution": "candidate_only"})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="reference request JSON")
    args = parser.parse_args()
    request = json.loads(args.input.read_text(encoding="utf-8"))
    out = replay(request["state"], request.get("events", []),
                 lod=request.get("lod", "high"))
    print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
