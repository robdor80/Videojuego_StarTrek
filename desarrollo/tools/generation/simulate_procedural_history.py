#!/usr/bin/env python3
"""P2-B05 offline history reference. Never writes CoreRPG WorldState or creates missions."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

VERSION = "0.1.0"
DOMAINS = {
    "civilizational_transition": {"civilization"},
    "colonial_milestone": {"colonization"},
    "economic_milestone": {"economy"},
    "conflict_aftermath": {"conflict"},
    "diplomatic_milestone": {"diplomacy"},
    "infrastructure_recovery": {"economy", "colonization"},
    "historical_record_update": {"record"},
}
PROVENANCE = {"game_addition", "inferred"}
VISIBILITY = {"public", "restricted", "classified"}


def need(value, message):
    if not value:
        raise ValueError(message)


def ident(value, name):
    need(isinstance(value, str) and bool(value.strip()), name + " missing")
    return value


def tick(value, name):
    need(type(value) is int and value >= 0, name + " invalid")
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def record_digest(record):
    return digest({k: v for k, v in record.items() if k != "digest"})


def validate_state(state):
    need(isinstance(state, dict), "invalid state")
    for k in ("campaign_id", "cutoff_tick", "last_tick", "facts", "entities",
              "authorities", "reserved_ids", "history"):
        need(k in state, "missing state field: " + k)
    ident(state["campaign_id"], "campaign_id")
    tick(state["cutoff_tick"], "cutoff_tick")
    tick(state["last_tick"], "last_tick")
    need(state["last_tick"] >= state["cutoff_tick"], "clock before cutoff")
    for key in ("facts", "entities", "authorities"):
        need(isinstance(state[key], dict), "invalid " + key)
    need(isinstance(state["reserved_ids"], list) and
         all(isinstance(v, str) for v in state["reserved_ids"]), "invalid reserved IDs")
    need(len(state["reserved_ids"]) == len(set(state["reserved_ids"])), "duplicate reservation")
    need(isinstance(state["history"], list), "invalid history")
    for fid, fact in state["facts"].items():
        ident(fid, "fact ID")
        need(isinstance(fact, dict), "invalid fact")
        tick(fact.get("tick"), "fact tick")
        need(fact.get("status") == "accepted", "rumor or forecast is not a fact")
        ident(fact.get("domain"), "fact domain")
        need(fact.get("campaign_id") in (state["campaign_id"], "canonical"),
             "foreign campaign fact")
    for eid, ent in state["entities"].items():
        ident(eid, "entity ID")
        tick(ent.get("exists_tick"), "entity existence")
        need(ent.get("campaign_id") in (state["campaign_id"], "canonical"),
             "foreign campaign entity")
    for actor, kinds in state["authorities"].items():
        ident(actor, "authority")
        need(isinstance(kinds, list) and set(kinds) <= set(DOMAINS), "invalid authority map")
    seen = set()
    prior = -1
    for record in state["history"]:
        ident(record.get("event_id"), "historical event")
        ident(record.get("kind"), "historical kind")
        t = tick(record.get("tick"), "history tick")
        need(t >= prior, "history order")
        need(record["event_id"] not in seen, "duplicate history event")
        need(record.get("digest") == record_digest(record), "corrupt historical record")
        need(t <= state["last_tick"], "event in future of clock")
        seen.add(record["event_id"])
        prior = t
    return True


def proposal(state, *, kind, source_refs, impact_refs, actor_ref, tick_value,
             ordinal="0", major=False, visibility="public", provenance="game_addition",
             corrects_ref=None):
    """Stable ID per campaign/causal origin, independent of LOD or player position."""
    ident(ordinal, "ordinal")
    seed = [VERSION, state["campaign_id"], kind, sorted(source_refs),
            sorted(impact_refs), ordinal]
    event_id = "hist:" + digest(seed)[:24]
    event = dict(event_id=event_id, tick=tick_value, kind=kind,
                 source_refs=list(source_refs), impact_refs=list(impact_refs),
                 actor_ref=actor_ref, major=major, visibility=visibility,
                 provenance=provenance, trigger="world")
    if corrects_ref is not None:
        event["corrects_ref"] = corrects_ref
    return event


def apply_event(state, event):
    """Atomic candidate acceptance: records history only, never mutates source facts."""
    validate_state(state)
    need(isinstance(event, dict), "invalid event")
    for k in ("event_id", "kind", "actor_ref", "provenance", "visibility", "trigger"):
        ident(event.get(k), k)
    eid = event["event_id"]
    need(event["kind"] in DOMAINS, "other block owns this event")
    need(event["provenance"] in PROVENANCE, "canon or television future cannot be fabricated")
    need(event["visibility"] in VISIBILITY, "invalid visibility")
    need(event["trigger"] == "world", "player presence cannot cause history")
    need(eid not in state["reserved_ids"], "canonical reservation collision")
    need(event["actor_ref"] in state["authorities"] and
         event["kind"] in state["authorities"][event["actor_ref"]], "authority not verified")
    need(type(event.get("major")) is bool, "major flag invalid")
    need(isinstance(event.get("source_refs"), list) and
         len(event["source_refs"]) > 0, "source evidence required")
    need(isinstance(event.get("impact_refs"), list) and
         len(event["impact_refs"]) > 0, "impacted entities required")
    need(len(set(event["source_refs"])) == len(event["source_refs"]), "duplicate source")
    need(len(set(event["impact_refs"])) == len(event["impact_refs"]), "duplicate impact")
    event_tick = tick(event.get("tick"), "event tick")
    event_hash = digest(event)
    previous = {e["event_id"]: e for e in state["history"]}
    if eid in previous:
        need(previous[eid]["source_digest"] == event_hash, "event ID reused with different payload")
        return copy.deepcopy(state)
    need(event_tick >= state["cutoff_tick"], "sealed historical prefix")
    need(event_tick >= state["last_tick"], "non-monotonic event time")
    domains = set()
    major_evidence = False
    for ref in event["source_refs"]:
        ident(ref, "source reference")
        if ref in state["facts"]:
            f = state["facts"][ref]
            need(f["tick"] <= event_tick, "future source fact")
            domains.add(f["domain"])
            major_evidence |= f.get("major_evidence") is True
        elif ref in previous:
            need(previous[ref]["tick"] <= event_tick, "future historical source")
            domains.add("record")
        else:
            raise ValueError("unknown source reference")
    need(bool(domains & DOMAINS[event["kind"]]), "missing kind-specific causal evidence")
    for ref in event["impact_refs"]:
        ident(ref, "impacted entity")
        need(ref in state["entities"], "unknown impacted entity")
        need(state["entities"][ref]["exists_tick"] <= event_tick, "entity does not exist yet")
    if event["major"]:
        need(len(event["impact_refs"]) >= 2 and major_evidence,
             "major event requires independently accepted scale evidence")
    correction = event.get("corrects_ref")
    if event["kind"] == "historical_record_update":
        need(correction in previous, "correction must reference recorded event")
        need(correction != eid, "self correction")
    else:
        need(correction is None, "correction only in historical record updates")
    record = copy.deepcopy(event)
    record["source_digest"] = event_hash
    record["digest"] = record_digest(record)
    candidate = copy.deepcopy(state)
    candidate["history"].append(record)
    candidate["last_tick"] = event_tick
    validate_state(candidate)
    return candidate


def replay(state, events):
    current = copy.deepcopy(state)
    for e in events:
        current = apply_event(current, e)
    return current


def visible_history(state, known_ids, at_tick, clearance):
    """Knowledge is an explicit observed-ID grant. Clearance alone reveals nothing."""
    validate_state(state)
    tick(at_tick, "observation tick")
    need(clearance in VISIBILITY, "invalid clearance")
    need(isinstance(known_ids, list), "invalid knowledge grants")
    level = {"public": 0, "restricted": 1, "classified": 2}
    return [copy.deepcopy(e) for e in state["history"] if
            e["event_id"] in known_ids and e["tick"] <= at_tick and
            level[e["visibility"]] <= level[clearance]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    f = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    final = replay(f["initial_state"], f["events"])
    print(canonical({"history_count": len(final["history"]),
                     "last_tick": final["last_tick"], "sha256": digest(final)}))


if __name__ == "__main__":
    main()
