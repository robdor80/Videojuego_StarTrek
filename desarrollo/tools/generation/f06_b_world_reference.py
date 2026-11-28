#!/usr/bin/env python3
"""F06-B: private, deterministic world-generation candidate (OFFLINE only).
The original astro and naval generators remain the owners of their baseline
algorithms. This module composes and enriches their outputs, never sensors.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import date
from pathlib import Path

import astro_physics_v1 as astro
import generate_starship_instance as military
import generate_civilian_starship as civilian

ROOT = Path(__file__).resolve().parents[3]
CATALOG = ROOT / "sistemas/universe/generation/f06_b_reference_catalog_v1.json"
STATUS = "PRIVATE_OFFLINE_CANDIDATE_NO_WORLD_STATE_MUTATION"
VERSION = "1.0.0"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def integer(value, low, high, field):
    require(type(value) is int and low <= value <= high, field)
    return value


def key(*parts):
    # Length-safe canonical encoding, independent of Python's salted hash.
    data = json.dumps(parts, ensure_ascii=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(data.encode("ascii")).hexdigest()[:24]


def rng(*parts):
    return military.DeterministicRng(key(*parts))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False).encode("ascii")).hexdigest()


def human_atmosphere(p):
    """Conservative fictional gameplay screening, not a medical guarantee.
    The v1 M candidate is a climate heuristic; no alteration of physical gases.
    """
    atm = p["atmosphere"]
    pressure = atm["surface_pressure_bar"]
    if not atm["has_solid_surface"] or pressure is None:
        return {"status":"NOT_APPLICABLE", "oxygen_partial_bar":None, "co2_partial_bar":None,
                "class_m_status":"NOT_APPLICABLE"}
    gases = atm["mole_fraction"]
    # v1's complete atmospheric fractions define absent constituent as zero.
    o2 = round(pressure * gases.get("O2", 0), 9)
    co2 = round(pressure * gases.get("CO2", 0), 9)
    basic = .5 <= pressure <= 1.5 and .16 <= o2 <= .30 and co2 <= .005
    return {"status":"PASSES_BASIC_HUMAN_SCREEN" if basic else "FAILS_BASIC_HUMAN_SCREEN",
            "oxygen_partial_bar":o2, "co2_partial_bar":co2,
            "class_m_status":("CANDIDATE_REQUIRES_FURTHER_TESTS" if basic else
                              "M_CLIMATE_CANDIDATE_NOT_BREATHABLE") if
                p["star_trek"]["class_candidate"] == "M_candidate" else "NOT_M_CANDIDATE",
            "not_certified_safe":True, "profile":"qa_human_atmosphere_screen_v1"}


def physical_system(request):
    result = astro.generate_system(request["seed"], request["sector"], request["era_id"],
                                    request["date"], profile="f06")
    for entity in result["entities"]:
        p = entity["ground_truth"]["properties"]
        if entity["entity_type"] == "planet":
            p["human_atmosphere_screen"] = human_atmosphere(p)
        elif entity["entity_type"] == "moon":
            p["gravity_earth"] = round(p["mass_earth"] / p["radius_earth"] ** 2, 9)
            p["bulk_density_g_cm3"] = round(5.514 * p["mass_earth"] / p["radius_earth"] ** 3, 9)
            p["atmosphere_status"] = "NOT_MODELED"
            p["surface_temperature_k"] = None
        elif entity["entity_type"] == "star":
            p["composition_status"] = "NOT_MODELED"
    require(not astro.validate_system(result), "physical model failed validation")
    return result


def catalog_checked(c):
    require(c["schema_version"] == 1 and c["status"] == "OFFLINE_REFERENCE_QA_NON_CANON",
            "catalog authority mismatch")
    for name, tech in c["technologies"].items():
        require(name.startswith("qa_") and tech["family"] and tech["band"], "technology metadata")
        require(tech["kind"] in {"energy_weapon","launcher","shield","reactor","propulsion",
                                  "cloak","life_support","sensor"}, "unsupported technology kind")
        for field in ("idle","active"):
            integer(tech[field], 0, 100000, field)
        require(tech["idle"] <= tech["active"], "power ordering")
        if tech["kind"] == "reactor":
            integer(tech["supply"], 1, 100000, "reactor supply")
        if tech["kind"] in ("energy_weapon","launcher","shield"):
            integer(tech["effect"], 0, 100000, "effect index")
        if tech["kind"] == "launcher":
            integer(tech["magazine"], 1, 100000, "magazine")
            require(tech["ammo_kind"], "ammunition type")
    for name, design in c["designs"].items():
        require(len(design["dimensions_m"]) == 3, "dimension axes")
        for dim in design["dimensions_m"]:
            integer(dim, 1, 100000, "hull dimensions")
        integer(design["decks"], 1, 200, "decks")
        integer(design["cargo_capacity_kg"], 0, 10**12, "cargo capacity")
        require(design["hull_materials"] and design["silhouette"], "hull description")
        for tech, count in design["loadout"].items():
            require(tech in c["technologies"], "technology reference")
            integer(count, 1, 1024, "module count")
            require(c["technologies"][tech]["operator"] in ("any", design["operator"]),
                    "operator technology compatibility")
        require(any(c["technologies"][t]["kind"] == "reactor" for t in design["loadout"]),
                "missing reactor")
    return c


def vector(value, field):
    require(isinstance(value, list) and len(value) == 3, field)
    return [integer(x, -10**15, 10**15, field) for x in value]


def instantiate_base(req, need):
    common = dict(campaign_seed=req["seed"], need_id=need["need_id"],
                  era_id=req["era_id"], campaign_date=req["date"], role=need["role"])
    if need["mode"] == "military":
        result = military.generate(operator=need["operator"], **common)
        require(not military.validate(result), "military reference invalid")
        design_key = result["ship"]["class_id"]
    elif need["mode"] == "civilian":
        require(need["operator"] == "independent_civilian", "civil operator")
        result = civilian.generate(operator_context=need["operator"], **common)
        require(not civilian.validate(result), "civil reference invalid")
        design_key = "civilian_" + result["design"]["size_band"]
    else:
        raise ValueError("unsupported vessel source")
    return result, design_key


def make_compartments(sid, design, people):
    # A small functional topology, not a finished interior or mesh.
    functions = ("command","engineering","habitation","cargo","medical","systems")
    compartments = []
    for deck in range(1, design["decks"] + 1):
        for function in functions:
            cid = "gen:compartment:" + key(sid, deck, function)
            compartments.append({"id":cid, "deck":deck, "function":function,
                "capacity_people":max(1, (people + design["decks"] - 1)//design["decks"])
                    if function == "habitation" else max(1, people//4),
                "cargo_capacity_kg":design["cargo_capacity_kg"]//design["decks"]
                    if function == "cargo" else 0,
                "integrity_permille":1000, "pressurized":True})
    # Conserve cargo capacity exactly after integer division.
    cargo = [c for c in compartments if c["function"] == "cargo"]
    cargo[0]["cargo_capacity_kg"] += design["cargo_capacity_kg"] - sum(c["cargo_capacity_kg"] for c in cargo)
    return compartments


def make_manifest(req, sid, base, need, c, compartments):
    pop = base["population"]
    categories = [("crew",pop["duty_crew_target"]),("resident",pop["civilian_residents"]),
                  ("passenger",pop["passengers"])]
    people = sum(n for _,n in categories)
    integer(people,1,8192,"population limit in reference")
    mix = need["species_weights"]
    require(isinstance(mix, dict) and mix and set(mix) <= set(c["population_profiles"]),
            "explicit supported population context required")
    weights = [(species,integer(mix[species],1,100000,"species weight")) for species in sorted(mix)]
    habitation = [room for room in compartments if room["function"] == "habitation"]
    out=[]
    for category,total in categories:
        for index in range(total):
            pid = "gen:person:" + key(sid, category, index)
            stream = rng(req["seed"], pid, "bio", VERSION)
            species = stream.weighted_choice(weights)
            lo,hi = c["population_profiles"][species]["adult_age_years"]
            # Synthetic adult profiles only; sex does not determine assignment or loyalty.
            out.append({"person_id":pid,"designation":"QA-" + key(pid,"designation")[:10].upper(),
                        "name_status":"TEMPORARY_REFERENCE_LABEL_NOT_CANON_NAME",
                        "category":category,"species":species,"age_years_at_epoch":stream.randint(lo,hi),
                        "sex_category":stream.choice(["female","male"]),
                        "life_state":"alive","medical_state":"nominal_reference_baseline",
                        "compartment_id":habitation[len(out)//habitation[0]["capacity_people"]]["id"],
                        "provenance":"QA_POPULATION_CONTEXT_NOT_SPECIES_CANON"})
    return out


def make_modules(sid, design, c, compartments):
    modules=[]
    for tech_id,count in sorted(design["loadout"].items()):
        tech=c["technologies"][tech_id]
        function = "engineering" if tech["kind"] in ("reactor","propulsion") else "systems"
        rooms=[room for room in compartments if room["function"] == function]
        for index in range(count):
            mid="gen:module:"+key(sid,tech_id,index)
            m={"module_id":mid,"technology_id":tech_id,"compartment_id":rooms[index%len(rooms)]["id"],
               "state":"idle","integrity_permille":1000,"installation_revision":1,
               "ammo":None,"modification_refs":[]}
            if tech["kind"] == "launcher":
                m["ammo"]={"type":tech["ammo_kind"],"quantity":tech["magazine"],"capacity":tech["magazine"]}
            if tech["kind"] in ("reactor","life_support","sensor"):
                m["state"]="active"
            modules.append(m)
    return modules


def energy(modules,c):
    available=used=0
    for m in modules:
        t=c["technologies"][m["technology_id"]]
        if m["state"] != "offline":
            if t["kind"]=="reactor" and m["state"]=="active":
                available+=t["supply"]*m["integrity_permille"]//1000
            else:
                used+=t["active"] if m["state"] in ("active","energized") else t["idle"]
    require(used<=available,"insufficient reference power budget")
    return {"available_qa_units":available,"allocated_qa_units":used,"reserve_qa_units":available-used}


def cargo_for(sid, need, stock, compartments):
    remaining={room["id"]:room["cargo_capacity_kg"] for room in compartments if room["function"]=="cargo"}
    cargo=[]
    seen=set()
    for order in need["cargo_orders"]:
        oid=order["order_id"]
        require(oid and oid not in seen,"duplicate cargo order")
        seen.add(oid)
        source=(need["origin"],order["commodity"])
        qty=integer(order["mass_kg"],1,10**12,"cargo quantity")
        require(stock.get(source,0)>=qty,"unfunded cargo demand")
        require(sum(remaining.values())>=qty,"cargo exceeds physical capacity")
        stock[source]-=qty
        left=qty
        for cid,capacity in remaining.items():
            amount=min(capacity,left)
            if amount:
                cargo.append({"cargo_id":"gen:cargo:"+key(sid,oid,cid),"order_id":oid,
                              "commodity":order["commodity"],"mass_kg":amount,
                              "source_location":need["origin"],"destination":need["destination"],
                              "compartment_id":cid})
                remaining[cid]-=amount
                left-=amount
            if not left: break
    return cargo


def generate(request, catalog=None):
    c=catalog_checked(copy.deepcopy(catalog if catalog is not None else load(CATALOG)))
    require(request["seed"] and request["sector"],"missing generation context")
    d=date.fromisoformat(request["date"])
    require(str(d.year)==c["epoch"] and request["era_id"]==c["era_id"],"unsupported catalog era")
    require(not request.get("canonical_reserved",False),"canonical system reserved")
    # The input is authoring evidence; no observer or scan parameters allowed.
    require(set(request)=={"seed","sector","era_id","date","locations","stock","needs","canonical_reserved"},
            "request fields are closed; no sensor-driven generation")
    locations={}
    for location in request["locations"]:
        lid=location["location_id"]
        require(lid and lid not in locations,"duplicate location")
        locations[lid]=vector(location["position_m"],"location")
    stock={}
    for row in request["stock"]:
        k=(row["location_id"],row["commodity"])
        require(k[0] in locations and k[1] and k not in stock,"invalid source stock")
        stock[k]=integer(row["mass_kg"],0,10**12,"source stock")
    initial_stock=stock.copy()
    system=physical_system(request)
    ships=[]
    seen=set()
    for need in sorted(request["needs"],key=lambda x:x["need_id"]):
        nid=need["need_id"]
        require(nid and nid not in seen and need["cause_ref"] and need["purpose"],"missing/duplicate causal need")
        seen.add(nid)
        require(need["origin"] in locations and need["destination"] in locations
                and need["origin"]!=need["destination"],"invalid route")
        start=integer(need["departure_tick"],0,10**8,"departure tick")
        end=integer(need["arrival_tick"],start+1,10**8,"arrival tick")
        base,design_key=instantiate_base(request,need)
        require(design_key in c["designs"],"no reviewed reference design: "+design_key)
        design=copy.deepcopy(c["designs"][design_key])
        sid=base["ship"]["ship_id"]
        operator=base["ship"].get("operator",base["ship"].get("operator_context"))
        require(operator==design["operator"],"design/operator mismatch")
        people=base["population"]["total_people_aboard_initial"]
        compartments=make_compartments(sid,design,people)
        manifest=make_manifest(request,sid,base,need,c,compartments)
        modules=make_modules(sid,design,c,compartments)
        cargo=cargo_for(sid,need,stock,compartments)
        ships.append({"ship_id":sid,"designation":base["ship"]["designation"],
            "registry_status":"TEMPORARY_GENERATED_DESIGNATION","design_key":design_key,
            "design_id":base.get("design",{}).get("design_id",design_key),"operator":operator,
            "reference_baseline":base,"physical_design":design,"compartments":compartments,
            "people":manifest,"modules":modules,"cargo":cargo,"energy":energy(modules,c),
            "mission":{"need_id":nid,"cause_ref":need["cause_ref"],"purpose":need["purpose"],
                       "origin":need["origin"],"destination":need["destination"],
                       "departure_tick":start,"arrival_tick":end},
            "position_m":locations[need["origin"]].copy(),"activity":"waiting" if start else "in_transit",
            "revision":1})
    world={"schema_version":VERSION,"status":STATUS,"epoch":request["date"],
           "system":system,"ships":ships,"locations":locations,"tick":0,"revision":1,
           "catalog_sha256":digest(c),"generation_request_sha256":digest(request),
           "initial_stock":[{"location_id":k[0],"commodity":k[1],"mass_kg":v} for k,v in sorted(initial_stock.items())],
           "remaining_stock":[{"location_id":k[0],"commodity":k[1],"mass_kg":v} for k,v in sorted(stock.items())],
           "events":[]}
    validate_world(world,c)
    return world


def position_at(ship, locations, tick):
    m=ship["mission"]
    origin=locations[m["origin"]]; destination=locations[m["destination"]]
    duration=m["arrival_tick"]-m["departure_tick"]
    elapsed=min(duration,max(0,tick-m["departure_tick"]))
    return [a+(b-a)*elapsed//duration for a,b in zip(origin,destination)]


def evolve(world, tick, catalog=None):
    """Offline replay on a copy; not a campaign clock, warp or economy engine."""
    c=catalog_checked(copy.deepcopy(catalog if catalog is not None else load(CATALOG)))
    validate_world(world,c)
    integer(tick,world["tick"],10**8,"monotonic tick")
    result=copy.deepcopy(world)
    if tick==world["tick"]: return result
    for ship in result["ships"]:
        m=ship["mission"]
        for at,kind in [(m["departure_tick"],"departed"),(m["arrival_tick"],"arrived")]:
            if world["tick"]<at<=tick:
                result["events"].append({"event_id":"gen:event:"+key(ship["ship_id"],kind,at),
                    "ship_id":ship["ship_id"],"tick":at,"kind":kind,"cause_ref":m["cause_ref"]})
        ship["position_m"]=position_at(ship,result["locations"],tick)
        ship["activity"]="waiting" if tick<m["departure_tick"] else "arrived" if tick>=m["arrival_tick"] else "in_transit"
        # Revisions depend on elapsed simulation time, not number of replay calls.
        ship["revision"]=1+tick
    result["tick"]=tick
    result["revision"]=1+tick
    result["events"].sort(key=lambda e:(e["tick"],e["event_id"]))
    validate_world(result,c)
    return result


def validate_world(world,catalog=None):
    c=catalog if catalog is not None else load(CATALOG)
    require(world["status"]==STATUS and world["schema_version"]==VERSION
            and world["catalog_sha256"]==digest(c),"world/catalog boundary")
    integer(world["tick"],0,10**8,"world tick")
    require(world["revision"]==1+world["tick"],"revision")
    require(not astro.validate_system(world["system"]),"astronomical consistency")
    for e in world["system"]["entities"]:
        p=e["ground_truth"]["properties"]
        if e["entity_type"]=="planet":
            require(p["human_atmosphere_screen"]==human_atmosphere(p),"incorrect atmospheric assessment")
    all_ids=set()
    cargo_sum={}
    for ship in world["ships"]:
        sid=ship["ship_id"]
        require(sid not in all_ids and sid.startswith("gen:starship:"),"ship identity")
        all_ids.add(sid)
        design=c["designs"][ship["design_key"]]
        require(ship["physical_design"]==design and ship["operator"]==design["operator"],"design provenance")
        rooms={r["id"]:r for r in ship["compartments"]}
        require(len(rooms)==len(ship["compartments"]),"duplicate compartments")
        for rid,r in rooms.items():
            require(rid not in all_ids and rid=="gen:compartment:"+key(sid,r["deck"],r["function"]),
                    "compartment identity")
            all_ids.add(rid)
        baseline=ship["reference_baseline"]["population"]
        expected={"crew":baseline["duty_crew_target"],"resident":baseline["civilian_residents"],"passenger":baseline["passengers"]}
        counts={k:0 for k in expected}; occupancy={}
        for p in ship["people"]:
            pid=p["person_id"]
            require(pid not in all_ids and p["compartment_id"] in rooms,"person identity/containment")
            all_ids.add(pid)
            require(p["category"] in counts and p["species"] in c["population_profiles"],"person classification")
            counts[p["category"]]+=1
            lo,hi=c["population_profiles"][p["species"]]["adult_age_years"]
            integer(p["age_years_at_epoch"],lo,hi,"age")
            require(p["life_state"] in ("alive","dead") and p["sex_category"] in ("male","female"),"biological state")
            rid=p["compartment_id"];occupancy[rid]=occupancy.get(rid,0)+1
        require(counts==expected,"manifest not reconciled with reference population")
        require(all(n<=rooms[r]["capacity_people"] for r,n in occupancy.items()),"overoccupied compartment")
        actual={}
        for m in ship["modules"]:
            mid=m["module_id"];tid=m["technology_id"]
            require(mid not in all_ids and tid in c["technologies"] and m["compartment_id"] in rooms,"module identity/location")
            all_ids.add(mid);actual[tid]=actual.get(tid,0)+1
            require(m["state"] in ("offline","idle","energized","active"),"module condition")
            integer(m["integrity_permille"],0,1000,"integrity")
            require(m["integrity_permille"]>0 or m["state"]=="offline","destroyed module active")
            t=c["technologies"][tid]
            if t["kind"]=="launcher":
                require(m["ammo"]["type"]==t["ammo_kind"] and m["ammo"]["capacity"]==t["magazine"],"ammo compatibility")
                integer(m["ammo"]["quantity"],0,t["magazine"],"ammo quantity")
            else:
                require(m["ammo"] is None,"non-launcher ammunition")
        require(actual==design["loadout"],"installed configuration mismatch")
        require(ship["energy"]==energy(ship["modules"],c),"energy ledger mismatch")
        room_cargo={}
        for row in ship["cargo"]:
            cid=row["cargo_id"];rid=row["compartment_id"]
            require(cid not in all_ids and rid in rooms,"cargo identity/location")
            all_ids.add(cid)
            n=integer(row["mass_kg"],1,10**12,"cargo mass")
            room_cargo[rid]=room_cargo.get(rid,0)+n
            require(row["source_location"]==ship["mission"]["origin"] and row["destination"]==ship["mission"]["destination"],"cargo route")
            k=(row["source_location"],row["commodity"]);cargo_sum[k]=cargo_sum.get(k,0)+n
        require(all(n<=rooms[r]["cargo_capacity_kg"] for r,n in room_cargo.items()),"cargo over capacity")
        require(ship["position_m"]==position_at(ship,world["locations"],world["tick"]),"position not derived from route")
        require(ship["revision"]==1+world["tick"],"ship revision")
    original={(x["location_id"],x["commodity"]):x["mass_kg"] for x in world["initial_stock"]}
    remaining={(x["location_id"],x["commodity"]):x["mass_kg"] for x in world["remaining_stock"]}
    require(set(original)==set(remaining) and set(cargo_sum)<=set(original),"stock keys")
    require(all(0<=remaining[k] and original[k]==remaining[k]+cargo_sum.get(k,0) for k in original),"stock conservation")
    require(len({e["event_id"] for e in world["events"]})==len(world["events"]),"event replay duplicate")
    return True


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--tick",type=int,default=0)
    args=parser.parse_args()
    world=evolve(generate(load(args.request)),args.tick)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(world,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    print("OFFLINE candidate:",len(world["ships"]),"ships;",sum(len(s["people"]) for s in world["ships"]),"individuals; digest",digest(world))


if __name__=="__main__":
    main()
