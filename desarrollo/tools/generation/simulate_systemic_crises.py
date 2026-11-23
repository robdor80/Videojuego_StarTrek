#!/usr/bin/env python3
"""P2-B08: crisis-chain OFFLINE reference; never writes CoreRPG or starts missions."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

VERSION = "0.1.0"
SCOPES = {"open", "add_shock", "assess", "mitigate", "contain", "resolve", "communicate"}
CLEARANCE = {"public": 0, "restricted": 1, "classified": 2}
FAMILIES = {"subspace", "environmental", "epidemic", "infrastructure",
            "economic", "energy", "ecological", "institutional", "war_aftermath"}
STATES = {"active", "contained", "resolved"}
EVENT_FIELDS = {
    "open": {"shock_ref"}, "add_shock": {"shock_ref", "crisis_ref"},
    "assess": {"crisis_ref"}, "mitigate": {"crisis_ref", "mitigation_ref", "authorization_ref",
                                        "policy_review_ref"},
    "contain": {"crisis_ref", "report_ref"}, "resolve": {"crisis_ref", "report_ref"},
    "communicate": {"crisis_ref", "recipient_ref", "classification", "arrival_tick"},
}
COMMON = {"event_id", "kind", "actor_ref", "tick", "trigger"}
NO_PLAYER_FIELDS = {"player", "player_presence", "player_distance", "camera_distance", "lod",
                    "mission_id", "quest_id", "ship_damage", "inventory_delta",
                    "population_delta", "sovereignty_delta", "route_creation",
                    "war_declaration", "technology_unlock", "world_delta", "travel_time"}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def ident(v, label):
    require(isinstance(v, str) and bool(v.strip()), "invalid " + label)
    return v


def tick(v, label):
    require(type(v) is int and v >= 0, "invalid " + label)
    return v


def bps(v, label):
    require(type(v) is int and 0 <= v <= 10000, "invalid bps " + label)
    return v


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def record_digest(value):
    return digest({k: v for k, v in value.items() if k != "digest"})


def crisis_id(campaign, shock_ref):
    return "p2b08:" + ident(campaign, "campaign") + ":" + ident(shock_ref, "shock ref")


def validate(state):
    require(isinstance(state, dict), "invalid state")
    for k in ("campaign_id", "cutoff_tick", "last_tick", "regions", "networks",
              "authorities", "facts", "crises", "knowledge", "events", "reserved_ids"):
        require(k in state, "missing " + k)
    ident(state["campaign_id"], "campaign")
    tick(state["cutoff_tick"], "cutoff")
    tick(state["last_tick"], "last_tick")
    require(state["last_tick"] >= state["cutoff_tick"], "clock before cutoff")
    for k in ("regions", "networks", "authorities", "facts", "crises"):
        require(isinstance(state[k], dict), "invalid map " + k)
    for k in ("knowledge", "events", "reserved_ids"):
        require(isinstance(state[k], list), "invalid list " + k)
    require(len(state["reserved_ids"]) == len(set(state["reserved_ids"])), "duplicate reservation")
    for rid, region in state["regions"].items():
        ident(rid, "region")
        require(isinstance(region, dict) and type(region.get("prewarp")) is bool,
                "invalid region or prewarp status")
    for nid, network in state["networks"].items():
        ident(nid, "network")
        require(isinstance(network, dict) and network.get("region_ref") in state["regions"],
                "invalid network region")
        bps(network.get("criticality_bps"), "criticality")
        require(isinstance(network.get("dependencies"), list), "invalid dependencies")
        seen = set()
        for d in network["dependencies"]:
            require(isinstance(d, dict) and set(d) == {"network_ref", "weight_bps"},
                    "invalid dependency")
            ref = ident(d["network_ref"], "dependency ref")
            require(ref in state["networks"] and ref != nid and ref not in seen,
                    "unknown/self/duplicate dependency")
            seen.add(ref)
            bps(d["weight_bps"], "dependency weight")
    for actor, auth in state["authorities"].items():
        ident(actor, "actor")
        require(isinstance(auth, dict) and isinstance(auth.get("scopes"), list)
                and len(auth["scopes"]) == len(set(auth["scopes"]))
                and set(auth["scopes"]) <= SCOPES, "invalid actor scopes")
        require(auth.get("clearance") in CLEARANCE, "invalid clearance")
    for fid, fact in state["facts"].items():
        ident(fid, "fact ref")
        require(isinstance(fact, dict) and fact.get("status") == "accepted",
                "source fact not accepted")
        require(fact.get("campaign_id") in (state["campaign_id"], "canonical"),
                "foreign-campaign fact")
        tick(fact.get("tick"), "fact time")
        if fact.get("kind") == "shock":
            require(fact.get("network_ref") in state["networks"], "unknown shock network")
            require(fact.get("family") in FAMILIES, "invalid shock family")
            bps(fact.get("loss_bps"), "shock")
        elif fact.get("kind") == "mitigation":
            require(fact.get("network_ref") in state["networks"], "unknown mitigation network")
            bps(fact.get("relief_bps"), "mitigation")
    for ref, crisis in state["crises"].items():
        ident(ref, "crisis ID")
        require(isinstance(crisis, dict) and crisis.get("crisis_id") == ref
                and crisis.get("state") in STATES, "invalid crisis")
        require(isinstance(crisis.get("shock_refs"), list) and len(crisis["shock_refs"]) > 0
                and len(set(crisis["shock_refs"])) == len(crisis["shock_refs"]),
                "invalid crisis shocks")
        require(ref == crisis_id(state["campaign_id"], crisis["shock_refs"][0]),
                "unstable crisis identity")
        for fid in crisis["shock_refs"]:
            require(fid in state["facts"] and state["facts"][fid].get("kind") == "shock",
                    "missing crisis shock")
        require(isinstance(crisis.get("mitigation_refs"), list)
                and len(set(crisis["mitigation_refs"])) == len(crisis["mitigation_refs"]),
                "invalid mitigations")
        for fid in crisis["mitigation_refs"]:
            require(fid in state["facts"] and state["facts"][fid].get("kind") == "mitigation"
                    and state["facts"][fid].get("crisis_ref") == ref,
                    "unrelated mitigation")
        require(isinstance(crisis.get("projection"), dict), "missing projection")
    seen, prev = set(), -1
    for record in state["events"]:
        require(isinstance(record, dict) and set(record) == {"event_id", "tick", "request", "digest"},
                "invalid history record")
        ident(record["event_id"], "event ID")
        at = tick(record["tick"], "history tick")
        require(prev <= at <= state["last_tick"] and record["event_id"] not in seen,
                "history replay or order violation")
        require(isinstance(record["request"], dict)
                and record["request"].get("event_id") == record["event_id"]
                and record["request"].get("tick") == at
                and record["digest"] == record_digest(record), "tampered event")
        seen.add(record["event_id"])
        prev = at
    for k in state["knowledge"]:
        require(isinstance(k, dict) and k.get("recipient_ref") in state["authorities"]
                and k.get("sender_ref") in state["authorities"]
                and k.get("crisis_ref") in state["crises"]
                and k.get("classification") in CLEARANCE, "invalid message")
        require(tick(k.get("arrival_tick"), "arrival") >= tick(k.get("sent_tick"), "sent"),
                "message arrives before sent")
    return True


def fact_at(state, ref, kind, at):
    fact = state["facts"].get(ident(ref, "source ref"))
    require(fact is not None and fact.get("kind") == kind, "missing " + kind + " fact")
    require(fact["tick"] <= at, "future source fact")
    return fact


def projection(state, crisis):
    """Non-authoritative exposure: max shock, bounded dependency graph, no stock mutations."""
    nodes = sorted(state["networks"])
    direct = {nid: 0 for nid in nodes}
    for ref in crisis["shock_refs"]:
        fact = state["facts"][ref]
        nid = fact["network_ref"]
        direct[nid] = max(direct[nid], fact["loss_bps"])
    relief = {nid: 0 for nid in nodes}
    for ref in crisis["mitigation_refs"]:
        fact = state["facts"][ref]
        nid = fact["network_ref"]
        relief[nid] = min(10000, relief[nid] + fact["relief_bps"])
    current = {nid: max(0, direct[nid] - relief[nid]) for nid in nodes}
    # Max-transfer with attenuation <= 1 cannot amplify through cycles.
    for _ in range(len(nodes)):
        updated = dict(current)
        for nid in nodes:
            for dep in state["networks"][nid]["dependencies"]:
                from_ref = dep["network_ref"]
                updated[nid] = max(updated[nid],
                                   current[from_ref] * dep["weight_bps"] // 10000)
        if updated == current:
            break
        current = updated
    exposed = {nid: current[nid] for nid in nodes if current[nid] > 0}
    pressures = {}
    for nid, value in exposed.items():
        region = state["networks"][nid]["region_ref"]
        impact = value * state["networks"][nid]["criticality_bps"] // 10000
        pressures[region] = max(pressures.get(region, 0), impact)
    maximum = max(pressures.values(), default=0)
    severity = ("none" if maximum == 0 else "low" if maximum < 2500 else
                "moderate" if maximum < 5000 else "high" if maximum < 8000 else "critical")
    return {"network_stress_bps": exposed, "region_pressure_bps": dict(sorted(pressures.items())),
            "severity": severity, "scope": len(pressures), "max_pressure_bps": maximum,
            "note": "candidate-only; no actual network, population, resource or mission mutation"}


def apply_event(state, event):
    """Immutable atomic replay; events are supplied, never scheduled or invented here."""
    validate(state)
    require(isinstance(event, dict) and event.get("kind") in SCOPES, "invalid event")
    kind = event["kind"]
    required = COMMON | (EVENT_FIELDS[kind] - {"policy_review_ref"})
    allowed = COMMON | EVENT_FIELDS[kind]
    require(required <= set(event) <= allowed and not (set(event) & NO_PLAYER_FIELDS),
            "missing/forbidden event fields")
    for field in ("event_id", "actor_ref", "trigger"):
        ident(event.get(field), field)
    require(event["trigger"] == "world", "player or LOD event trigger forbidden")
    at = tick(event.get("tick"), "event time")
    for record in state["events"]:
        if record["event_id"] == event["event_id"]:
            require(record["request"] == event, "changed payload on duplicate event ID")
            return copy.deepcopy(state)
    require(at >= state["cutoff_tick"] and at >= state["last_tick"],
            "retroactive/past event forbidden")
    require(event["event_id"] not in state["reserved_ids"], "reserved event collision")
    actor = state["authorities"].get(event["actor_ref"])
    require(actor is not None and kind in actor["scopes"], "scope not authorized")
    next_state = copy.deepcopy(state)
    if kind == "open":
        shock = fact_at(state, event["shock_ref"], "shock", at)
        require(shock["loss_bps"] > 0, "no real shock")
        ref = crisis_id(state["campaign_id"], event["shock_ref"])
        require(ref not in state["reserved_ids"] and ref not in state["crises"],
                "crisis already open or canonical reservation")
        crisis = {"crisis_id": ref, "state": "active", "started_tick": at,
                  "shock_refs": [event["shock_ref"]], "mitigation_refs": [],
                  "projection": {}}
        crisis["projection"] = projection(next_state, crisis)
        next_state["crises"][ref] = crisis
    else:
        ref = ident(event["crisis_ref"], "crisis ref")
        require(ref in next_state["crises"], "unknown crisis")
        crisis = next_state["crises"][ref]
        if kind == "add_shock":
            require(crisis["state"] != "resolved", "closed crisis cannot be reactivated")
            shock = fact_at(state, event["shock_ref"], "shock", at)
            require(shock["loss_bps"] > 0 and event["shock_ref"] not in crisis["shock_refs"],
                    "duplicate or empty shock")
            crisis["shock_refs"].append(event["shock_ref"])
            crisis["state"] = "active"
            crisis["projection"] = projection(next_state, crisis)
        elif kind == "assess":
            crisis["projection"] = projection(next_state, crisis)
        elif kind == "mitigate":
            require(crisis["state"] != "resolved", "resolved crisis")
            mitig = fact_at(state, event["mitigation_ref"], "mitigation", at)
            require(mitig.get("crisis_ref") == ref
                    and mitig.get("actor_ref") == event["actor_ref"]
                    and mitig["relief_bps"] > 0
                    and event["mitigation_ref"] not in crisis["mitigation_refs"],
                    "invalid or duplicate mitigation")
            require(mitig["network_ref"] in {state["facts"][s]["network_ref"] for s in crisis["shock_refs"]},
                    "mitigation has no direct shock target")
            authorization = fact_at(state, event["authorization_ref"], "authorization", at)
            region = state["networks"][mitig["network_ref"]]["region_ref"]
            require(authorization.get("crisis_ref") == ref
                    and authorization.get("actor_ref") == event["actor_ref"]
                    and authorization.get("region_ref") == region
                    and authorization.get("scope") == "intervene",
                    "jurisdiction or resources not authorized")
            if state["regions"][region]["prewarp"]:
                require("policy_review_ref" in event, "prewarp noninterference review missing")
                policy = fact_at(state, event["policy_review_ref"], "policy_review", at)
                require(policy.get("crisis_ref") == ref and policy.get("region_ref") == region
                        and policy.get("decision") == "approved_exception",
                        "Prime Directive requires explicit authorized exception")
            else:
                require("policy_review_ref" not in event, "unexpected policy review ref")
            crisis["mitigation_refs"].append(event["mitigation_ref"])
            crisis["projection"] = projection(next_state, crisis)
        elif kind == "contain":
            require(crisis["state"] == "active", "containment state invalid")
            report = fact_at(state, event["report_ref"], "containment_report", at)
            require(report.get("crisis_ref") == ref
                    and report.get("actor_ref") == event["actor_ref"],
                    "unverified containment")
            require(projection(next_state, crisis)["max_pressure_bps"] < 2500,
                    "cannot contain high remaining exposure")
            crisis["state"] = "contained"
            crisis["projection"] = projection(next_state, crisis)
        elif kind == "resolve":
            require(crisis["state"] == "contained", "must contain before resolution")
            report = fact_at(state, event["report_ref"], "recovery_report", at)
            require(report.get("crisis_ref") == ref
                    and report.get("actor_ref") == event["actor_ref"]
                    and report.get("all_networks_restored") is True,
                    "recovery not independently attested")
            require(not projection(next_state, crisis)["network_stress_bps"],
                    "remaining disruption prevents closure")
            crisis["state"] = "resolved"
            crisis["projection"] = projection(next_state, crisis)
        elif kind == "communicate":
            recipient = ident(event["recipient_ref"], "recipient")
            require(recipient in state["authorities"], "unknown recipient")
            classification = event["classification"]
            require(classification in CLEARANCE
                    and actor["clearance"] in CLEARANCE
                    and CLEARANCE[actor["clearance"]] >= CLEARANCE[classification]
                    and CLEARANCE[state["authorities"][recipient]["clearance"]] >= CLEARANCE[classification],
                    "classified information leakage")
            arrival = tick(event["arrival_tick"], "arrival")
            require(arrival >= at, "instantaneous backward communication")
            next_state["knowledge"].append({
                "crisis_ref": ref, "recipient_ref": recipient,
                "sender_ref": event["actor_ref"], "classification": classification,
                "sent_tick": at, "arrival_tick": arrival,
                "snapshot": copy.deepcopy(crisis["projection"]),
            })
    record = {"event_id": event["event_id"], "tick": at, "request": copy.deepcopy(event)}
    record["digest"] = record_digest(record)
    next_state["events"].append(record)
    next_state["last_tick"] = at
    validate(next_state)
    return next_state


def view_for(state, recipient_ref):
    """An actor learns only messages actually delivered, no omniscient ground truth."""
    validate(state)
    require(recipient_ref in state["authorities"], "unknown viewer")
    clearance = CLEARANCE[state["authorities"][recipient_ref]["clearance"]]
    return [{"crisis_ref": k["crisis_ref"], "sent_tick": k["sent_tick"],
             "arrival_tick": k["arrival_tick"], "projection": copy.deepcopy(k["snapshot"])}
            for k in state["knowledge"] if k["recipient_ref"] == recipient_ref
            and k["arrival_tick"] <= state["last_tick"]
            and CLEARANCE[k["classification"]] <= clearance]


def replay(state, events):
    require(isinstance(events, list), "events must be list")
    result = copy.deepcopy(state)
    for event in events:
        result = apply_event(result, event)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    source = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    state = replay(source["state"], source["events"])
    print(canonical({"authority": "OFFLINE_REFERENCE_ONLY", "version": VERSION,
                     "event_count": len(state["events"]),
                     "crises": {k: {"state": v["state"], "projection": v["projection"]}
                                for k, v in sorted(state["crises"].items())},
                     "views": {a: view_for(state, a) for a in source.get("views", [])},
                     "sha256": digest(state)}))


if __name__ == "__main__":
    main()
