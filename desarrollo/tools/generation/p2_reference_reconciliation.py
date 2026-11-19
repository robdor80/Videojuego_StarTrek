#!/usr/bin/env python3
"""Offline P2 cross-domain reconciliation gates; no runtime, I/O, or authority.

Producers are synthetic reference adapters. CoreRPG must own real facts,
snapshot tokens, grants, idempotent commits, replay and persistence during F13.
"""
from __future__ import annotations
from collections import Counter


def require(ok, why):
    if not ok:
        raise ValueError(why)


def verify_consistent_read(view):
    """Allow historical fact origin revisions, not a mixed *read* snapshot."""
    require(isinstance(view, dict), "snapshot shape")
    require(isinstance(view.get("campaign_id"), str) and view["campaign_id"], "campaign")
    require(isinstance(view.get("read_token"), str) and view["read_token"], "read token")
    rev = view.get("read_revision")
    tick = view.get("snapshot_tick")
    require(type(rev) is int and rev >= 0 and type(tick) is int and tick >= 0,
            "invalid snapshot revision or tick")
    require(isinstance(view.get("facts"), list), "facts collection required")
    seen = set()
    for fact in view["facts"]:
        require(isinstance(fact, dict), "fact shape")
        fid = fact.get("fact_id")
        require(isinstance(fid, str) and fid and fid not in seen, "duplicate fact ID")
        seen.add(fid)
        origin, version, at = (fact.get("origin_revision"),
                               fact.get("version_revision"), fact.get("tick"))
        require(type(origin) is int and type(version) is int and
                0 <= origin <= version <= rev, "fact revision beyond read snapshot")
        require(type(at) is int and 0 <= at <= tick, "fact tick beyond read snapshot")
        require(fact.get("campaign_id") == view["campaign_id"], "foreign campaign fact")
        require(fact.get("status") == "accepted", "unaccepted read fact")
        require(isinstance(fact.get("issuer_ref"), str) and fact["issuer_ref"],
                "unknown accepted-fact issuer")
    return True


def verify_causal_bridge(bridge):
    """Contract reconciliation of *one shared synthetic ledger* across B01–B10.

    Records must be attributed to owner domains and have causal predecessors.
    Mutation envelopes cannot be fabricated by B08 forecasts or B10 proposals.
    Movement ledgers have double entries; inventory is never manufactured.
    """
    require(isinstance(bridge, dict), "bridge shape")
    campaign = bridge.get("campaign_id")
    require(isinstance(campaign, str) and campaign, "bridge campaign")
    records = bridge.get("records")
    require(isinstance(records, list), "bridge records")
    known = set(bridge.get("seed_refs", []))
    require(len(known) == len(bridge.get("seed_refs", [])), "duplicate seed reference")
    used = set()
    population = {}
    inventory = {}
    roster = {}
    last_tick = -1
    for rec in records:
        require(isinstance(rec, dict), "record shape")
        rid, domain, tick = rec.get("record_id"), rec.get("domain"), rec.get("tick")
        require(isinstance(rid, str) and rid not in known and rid not in used,
                "duplicate fact or event identity")
        require(domain in {"B01","B02","B03","B04","B05","B06","B07","B08","B09","B10"},
                "unknown source domain")
        require(type(tick) is int and last_tick <= tick, "clock regression")
        require(rec.get("campaign_id") == campaign, "cross-campaign bridge")
        require(rec.get("status") == "accepted_synthetic" if domain != "B10" else
                rec.get("status") == "proposal_only", "invalid reference acceptance")
        require(isinstance(rec.get("source_refs"), list) and
                len(rec["source_refs"]) > 0 and all(x in known or x in used for x in rec["source_refs"]),
                "missing causal predecessor")
        for action in rec.get("ledger", []):
            require(isinstance(action, dict), "ledger action")
            kind = action.get("kind")
            if domain in {"B08","B10"}:
                raise ValueError("forecast or scheduler cannot mutate WorldState")
            if kind == "population_transfer":
                key = action.get("transfer_id")
                require(isinstance(key, str) and key, "population transfer ID")
                population.setdefault(key, []).append((action.get("account_ref"), action.get("delta")))
            elif kind == "inventory_transfer":
                key = action.get("transfer_id")
                require(isinstance(key, str) and key, "inventory transfer ID")
                inventory.setdefault(key, []).append((action.get("account_ref"),
                                                        action.get("item_ref"), action.get("delta")))
            elif kind == "unit_ownership":
                uid, owner = action.get("unit_id"), action.get("owner_ref")
                require(isinstance(uid, str) and isinstance(owner, str)
                        and uid and owner and uid not in roster, "duplicate military identity")
                roster[uid] = owner
            elif kind == "knowledge_grant":
                require(domain == "B05" and action.get("issuer_domain") == "CoreRPG/B05"
                        and action.get("source_ref") in known | used
                        and isinstance(action.get("actor_ref"), str),
                        "unverified disclosure grant")
            else:
                raise ValueError("unknown bridge ledger operation")
        used.add(rid)
        last_tick = tick
    for movement, sides in population.items():
        require(len(sides) == 2 and all(type(n) is int and n != 0 for _, n in sides)
                and sides[0][0] != sides[1][0] and sum(n for _, n in sides) == 0,
                "unbalanced or duplicated population movement: " + movement)
    for movement, sides in inventory.items():
        require(len(sides) == 2 and all(type(n) is int and n != 0 for _, _, n in sides)
                and sides[0][0] != sides[1][0]
                and sides[0][1] == sides[1][1]
                and sum(n for _, _, n in sides) == 0,
                "unbalanced or duplicated resource transfer: " + movement)
    return {"records": len(records), "domains": sorted({r["domain"] for r in records}),
            "population_transfers": len(population), "inventory_transfers": len(inventory),
            "unique_units": len(roster), "last_tick": last_tick}
