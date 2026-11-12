#!/usr/bin/env python3
"""P2-B07: generador y expediente de exploración OFFLINE; nunca escribe CoreRPG."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

VERSION = "0.1.0"
ACTIONS = {"materialize", "survey", "excavate", "interpret", "advance", "communicate"}
COMMON_FAMILIES = {"astronomical", "spatial", "subspace", "gravimetric", "radiation"}
ARCHAEOLOGY = {"ruin", "derelict", "artifact_field"}
EXCEPTIONAL = {"temporal", "wormhole", "dimensional"}
CLEARANCE = {"public": 0, "restricted": 1, "classified": 2}
PHASE_TRANSITIONS = {
    "dormant": {"active", "spent"}, "active": {"quiescent", "spent"},
    "quiescent": {"active", "spent"}, "stable_ruin": {"eroding_ruin"},
    "eroding_ruin": {"lost_ruin"},
}
FORBIDDEN = {"player_presence", "player_distance", "camera_distance", "lod", "spawn_on_scan",
             "mission_id", "crisis_id", "trade_delta", "technology_unlock",
             "ship_damage", "world_delta", "time_travel", "teleport", "route_creation"}


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def ident(value, label):
    require(isinstance(value, str) and bool(value.strip()), "invalid " + label)
    return value


def tick(value, label):
    require(type(value) is int and value >= 0, "invalid " + label)
    return value


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def stable_entity_id(state, slot_ref):
    ident(slot_ref, "slot")
    return "p2b07:" + state["campaign_id"] + ":" + slot_ref


def roll_bps(state, slot_ref):
    """Seeding estable por campaña/slot; jamás por visualización, orden, nave o jugador."""
    return int(digest([VERSION, state["campaign_id"], state["world_seed"], "p2b07", slot_ref])[:12], 16) % 10000


def record_hash(record):
    return digest({k: v for k, v in record.items() if k != "digest"})


def validate(state):
    require(isinstance(state, dict), "invalid state")
    for key in ("campaign_id", "world_seed", "cutoff_tick", "last_tick", "locations",
                "actors", "instruments", "slots", "facts", "phenomena", "knowledge",
                "events", "reserved_ids"):
        require(key in state, "missing state " + key)
    ident(state["campaign_id"], "campaign")
    ident(state["world_seed"], "seed")
    tick(state["cutoff_tick"], "cutoff")
    tick(state["last_tick"], "clock")
    require(state["last_tick"] >= state["cutoff_tick"], "clock before cutoff")
    for key in ("locations", "actors", "instruments", "slots", "facts", "phenomena"):
        require(isinstance(state[key], dict), "invalid map " + key)
    for key in ("knowledge", "events", "reserved_ids"):
        require(isinstance(state[key], list), "invalid list " + key)
    require(len(state["reserved_ids"]) == len(set(state["reserved_ids"])), "duplicate reservation")
    for key in ("locations", "actors", "instruments"):
        for ref, item in state[key].items():
            ident(ref, key + " ref")
            require(isinstance(item, dict), "invalid " + key + " item")
            tick(item.get("exists_tick"), key + " creation")
    for aid, actor in state["actors"].items():
        require(isinstance(actor.get("scopes"), list)
                and set(actor["scopes"]) <= ACTIONS, "invalid actor scopes")
        require(actor.get("clearance") in CLEARANCE, "invalid actor clearance")
    for ref, fact in state["facts"].items():
        ident(ref, "fact id")
        require(isinstance(fact, dict) and fact.get("status") == "accepted",
                "non-accepted source fact")
        require(fact.get("campaign_id") in (state["campaign_id"], "canonical"),
                "foreign-campaign source fact")
        tick(fact.get("tick"), "fact time")
    for sid, slot in state["slots"].items():
        ident(sid, "slot id")
        require(isinstance(slot, dict), "invalid slot")
        require(slot.get("location_ref") in state["locations"], "slot unknown location")
        require(slot.get("family") in COMMON_FAMILIES | ARCHAEOLOGY | EXCEPTIONAL,
                "unknown phenomenon family")
        chance = slot.get("rarity_bps")
        require(type(chance) is int and 0 <= chance <= 10000, "invalid rarity")
    for eid, item in state["phenomena"].items():
        require(eid == stable_entity_id(state, item.get("slot_ref"))
                and item["location_ref"] == state["slots"][item["slot_ref"]]["location_ref"],
                "materialized identity drift")
        require(item["family"] == state["slots"][item["slot_ref"]]["family"],
                "materialized family drift")
    previous, seen = -1, set()
    for event in state["events"]:
        require(isinstance(event, dict), "invalid history item")
        ident(event.get("event_id"), "history event ID")
        et = tick(event.get("tick"), "history event tick")
        require(previous <= et <= state["last_tick"], "history chronological drift")
        require(event["event_id"] not in seen, "duplicate history event")
        require(event.get("digest") == record_hash(event), "tampered event digest")
        seen.add(event["event_id"])
        previous = et
    return True


def source_fact(state, ref, when, expected, source_ref=None):
    fact = state["facts"].get(ident(ref, "source fact"))
    require(fact is not None and fact["kind"] == expected, "missing accepted " + expected + " fact")
    require(fact["tick"] <= when, "future source fact")
    if source_ref is not None:
        require(fact.get("source_ref") == source_ref, "source provenance mismatch")
    return fact


def active_entity(state, ref, mapping, when):
    item = state[mapping].get(ident(ref, mapping + " ref"))
    require(item is not None and item["exists_tick"] <= when, "missing or future " + mapping)
    return item


def apply_event(state, event):
    """Inmutabilidad y rechazo atómico; snapshot de laboratorio, no transacción de CoreRPG."""
    validate(state)
    require(isinstance(event, dict), "invalid event")
    for k in ("event_id", "kind", "actor_ref", "trigger"):
        ident(event.get(k), k)
    require(event["kind"] in ACTIONS, "other-block operation forbidden")
    require(event["trigger"] == "world", "player-triggered creation forbidden")
    require(not (set(event) & FORBIDDEN), "cross-block mutation forbidden")
    require(event["event_id"] not in state["reserved_ids"], "canonical reservation collision")
    actor = active_entity(state, event["actor_ref"], "actors", tick(event.get("tick"), "event tick"))
    require(event["kind"] in actor["scopes"], "actor lacks authority")
    fingerprint = digest(event)
    for old in state["events"]:
        if old["event_id"] == event["event_id"]:
            require(old["source_digest"] == fingerprint, "event id payload conflict")
            return copy.deepcopy(state)
    t = event["tick"]
    require(t >= state["cutoff_tick"], "sealed historical prefix")
    require(t >= state["last_tick"], "non-monotonic event")
    new = copy.deepcopy(state)
    kind, outcome = event["kind"], "accepted"
    ref = event.get("entity_ref")

    if kind == "materialize":
        sid = ident(event.get("slot_ref"), "slot ref")
        slot = state["slots"].get(sid)
        require(slot is not None, "missing generation slot")
        location = active_entity(state, slot["location_ref"], "locations", t)
        require(not location.get("reserved", False), "canonical protected location")
        require(not slot.get("canon_reserved", False), "canonical reserved slot")
        require(sid not in state["reserved_ids"], "reserved generation slot")
        eid = stable_entity_id(state, sid)
        require(eid not in state["reserved_ids"], "reserved entity id")
        require(not any(e["slot_ref"] == sid for e in state["phenomena"].values()),
                "slot already materialized")
        family = slot["family"]
        require(family not in EXCEPTIONAL, "exceptional phenomenon requires authored Core event")
        origin_kind = "archaeological_origin" if family in ARCHAEOLOGY else "formation"
        origin = source_fact(state, slot.get("origin_fact_ref"), t, origin_kind,
                             slot["location_ref"])
        require(origin["tick"] < state["cutoff_tick"], "source not pre-existing")
        if family in ARCHAEOLOGY:
            require(ident(origin.get("culture_ref"), "archaeological culture"), "culture required")
            require(ident(slot.get("custodian_ref"), "custodian"), "custodian required")
            require(slot["custodian_ref"] in state["actors"], "unknown custodian")
            phase = "stable_ruin"
        else:
            phase = "dormant"
        require(slot.get("classification") in CLEARANCE, "invalid classification")
        if roll_bps(state, sid) < slot["rarity_bps"]:
            new["phenomena"][eid] = {
                "entity_id": eid, "slot_ref": sid, "family": family,
                "location_ref": slot["location_ref"], "origin_fact_ref": slot["origin_fact_ref"],
                "origin_tick": origin["tick"], "materialized_tick": t, "phase": phase,
                "classification": slot["classification"], "generator_version": VERSION,
                "seed_digest": digest([state["world_seed"], sid, VERSION]),
                "observations": [], "recoveries": [], "interpretations": [], "phase_changes": [],
            }
            outcome = eid
        else:
            outcome = "empty_slot"  # no retry al acercarse un jugador; historia registra el intento

    else:
        item = new["phenomena"].get(ident(ref, "entity ref"))
        require(item is not None and item["materialized_tick"] < t,
                "phenomenon must pre-exist action")
        family = item["family"]

        if kind == "survey":
            instrument = active_entity(state, event.get("instrument_ref"), "instruments", t)
            require(instrument.get("calibrated") is True and instrument.get("operational") is True,
                    "sensor not operational or calibrated")
            fact = source_fact(state, event.get("fact_ref"), t, "sensor_observation", ref)
            require(fact.get("actor_ref") == event["actor_ref"]
                    and fact.get("instrument_ref") == event["instrument_ref"],
                    "sensor provenance mismatch")
            require(fact.get("result") in {"trace", "partial", "corroborates", "contradicts"},
                    "invalid observation grade")
            require(event["fact_ref"] not in [v["fact_ref"] for v in item["observations"]],
                    "observation fact reused")
            item["observations"].append({
                "fact_ref": event["fact_ref"], "actor_ref": event["actor_ref"],
                "instrument_ref": event["instrument_ref"], "result": fact["result"],
                "tick": fact["tick"],
            })

        elif kind == "excavate":
            require(family in ARCHAEOLOGY, "cannot excavate natural phenomenon")
            slot = state["slots"][item["slot_ref"]]
            require(event.get("custodian_ref") == slot["custodian_ref"],
                    "custodian mismatch")
            require(event.get("permit") is True and ident(event.get("preservation_ref"),
                    "preservation plan"), "excavation requires permit and preservation")
            fact = source_fact(state, event.get("fact_ref"), t, "excavation", ref)
            require(fact.get("actor_ref") == event["actor_ref"]
                    and fact.get("custodian_ref") == event["custodian_ref"]
                    and fact.get("permit") is True, "excavation provenance/consent mismatch")
            ident(fact.get("artifact_ref"), "artifact ref")
            ident(fact.get("stratum_ref"), "stratigraphic layer")
            require(event["fact_ref"] not in [v["fact_ref"] for v in item["recoveries"]],
                    "excavation fact reused")
            item["recoveries"].append({
                "fact_ref": event["fact_ref"], "artifact_ref": fact["artifact_ref"],
                "stratum_ref": fact["stratum_ref"], "custodian_ref": slot["custodian_ref"],
            })  # no mueve la propiedad ni crea tecnología

        elif kind == "interpret":
            require(ident(event.get("hypothesis"), "hypothesis"), "missing hypothesis")
            good = [o for o in item["observations"] if o["result"] == "corroborates"]
            require(len({o["actor_ref"] for o in good}) >= 2 and
                    len({o["instrument_ref"] for o in good}) >= 2,
                    "independent evidence required")
            require(not any(o["result"] == "contradicts" for o in item["observations"]),
                    "unresolved contradiction")
            item["interpretations"].append({
                "actor_ref": event["actor_ref"], "hypothesis": event["hypothesis"],
                "status": "supported_not_certain", "tick": t,
            })

        elif kind == "advance":
            fact = source_fact(state, event.get("fact_ref"), t, "physical_transition", ref)
            desired = ident(event.get("target_phase"), "target phase")
            require(desired in PHASE_TRANSITIONS.get(item["phase"], set()),
                    "illegal physical transition")
            require(fact.get("from_phase") == item["phase"]
                    and fact.get("to_phase") == desired, "physical cause mismatch")
            previous = item["phase"]
            item["phase"] = desired
            item["phase_changes"].append({"from": previous, "to": desired,
                                          "fact_ref": event["fact_ref"], "tick": t})

        elif kind == "communicate":
            recipient = active_entity(state, event.get("recipient_ref"), "actors", t)
            require(len(item["observations"]) > 0, "no observation to communicate")
            fact = source_fact(state, event.get("fact_ref"), t, "communication", ref)
            require(fact.get("sender_ref") == event["actor_ref"] and
                    fact.get("recipient_ref") == event["recipient_ref"],
                    "communication provenance mismatch")
            level = ident(event.get("classification"), "communication classification")
            require(level in CLEARANCE and
                    CLEARANCE[level] >= CLEARANCE[item["classification"]],
                    "classification downgrade forbidden")
            require(CLEARANCE[recipient["clearance"]] >= CLEARANCE[level],
                    "recipient lacks clearance")
            arrival = tick(event.get("arrival_tick"), "delivery tick")
            require(arrival >= t, "backdated delivery")
            new["knowledge"].append({
                "entity_ref": ref, "sender_ref": event["actor_ref"],
                "recipient_ref": event["recipient_ref"], "classification": level,
                "arrival_tick": arrival, "fact_ref": event["fact_ref"],
            })

    record = {
        "event_id": event["event_id"], "kind": kind, "actor_ref": event["actor_ref"],
        "tick": t, "outcome": outcome, "source_digest": fingerprint,
    }
    record["digest"] = record_hash(record)
    new["events"].append(record)
    new["last_tick"] = t
    validate(new)
    return new


def replay(initial_state, events):
    current = copy.deepcopy(initial_state)
    for event in events:
        current = apply_event(current, event)
    return current


def observed(state, recipient_ref, at_tick, clearance):
    """Proyección mínima: jamás devuelve ground truth, seed, estratos ocultos ni interpretaciones."""
    validate(state)
    ident(recipient_ref, "recipient")
    at = tick(at_tick, "query tick")
    require(clearance in CLEARANCE, "invalid requested clearance")
    require(recipient_ref in state["actors"], "unknown recipient")
    allowed = min(CLEARANCE[clearance], CLEARANCE[state["actors"][recipient_ref]["clearance"]])
    results = {}
    for eid, item in state["phenomena"].items():
        if CLEARANCE[item["classification"]] > allowed:
            continue
        own = any(o["actor_ref"] == recipient_ref and o["tick"] <= at
                  for o in item["observations"])
        delivered = any(k["entity_ref"] == eid and k["recipient_ref"] == recipient_ref
                        and k["arrival_tick"] <= at and CLEARANCE[k["classification"]] <= allowed
                        for k in state["knowledge"])
        if own or delivered:
            results[eid] = {"entity_ref": eid, "classification": item["classification"],
                            "knowledge_state": "observed" if own else "communicated"}
    return [results[eid] for eid in sorted(results)]


def main():
    p = argparse.ArgumentParser(description="P2-B07 OFFLINE — no CoreRPG WorldState mutation")
    p.add_argument("--fixture", required=True, type=Path)
    args = p.parse_args()
    data = json.loads(args.fixture.read_text(encoding="utf-8"))
    out = replay(data["initial_state"], data["events"])
    print(canonical({"status": "OFFLINE_REFERENCE_ONLY", "events": len(out["events"]),
                     "phenomena": len(out["phenomena"]), "digest": digest(out)}))


if __name__ == "__main__":
    main()
