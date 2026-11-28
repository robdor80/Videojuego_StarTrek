#!/usr/bin/env python3
"""Physical-first, deterministic Star Trek stellar-system generator (reference v1).

Only standard-library Python. Host/world truth; NEVER a sensor/LCARS/LLM endpoint.
Models are bounded gameplay approximations, not an N-body or atmospheric solver.
The older v0.0.1 generator remains untouched.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path

VERSION = "1.0.0"
M_EARTH_PER_SUN = 332946.0
EARTH_RADIUS_AU = 6371.0 / 149597870.7
SOLAR_RADIUS_KM = 695700.0
G_EARTH = 9.80665
AU_KM = 149597870.7
SPECTRAL = {
    "M": (.10, .45, 47), "K": (.45, .80, 24),
    "G": (.80, 1.04, 15), "F": (1.04, 1.40, 8),
    "A": (1.40, 2.10, 4), "B": (2.10, 16.0, 1.8),
    "O": (16.0, 30.0, .2),
}
SURFACE_FAMILIES = {"rocky", "super_earth", "desert", "ocean", "ice_rock", "lava"}
ENVELOPED_FAMILIES = {"mini_neptune", "ice_giant", "gas_giant"}
ALL_FAMILIES = SURFACE_FAMILIES | ENVELOPED_FAMILIES
GASES = ("H2", "He", "N2", "CO2", "O2", "Ar", "CH4", "H2O")
SECRET_KEYS = frozenset(("ground_truth", "hidden_properties", "composition", "biosphere", "planet_class"))

def token(*parts: object, length: int = 16) -> str:
    return hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()[:length]

class Rng:
    """SHA-256 counter stream; independently keyed per generated entity."""
    def __init__(self, *keys: object):
        self.key = "|".join(map(str, keys))
        self.n = 0

    def u(self) -> float:
        h = hashlib.sha256(f"{self.key}|{self.n}".encode("utf-8")).digest()
        self.n += 1
        return int.from_bytes(h, "big") / 2**256

    def between(self, lo: float, hi: float) -> float:
        return lo + (hi - lo) * self.u()

    def integer(self, lo: int, hi: int) -> int:
        return lo + int(self.u() * (hi - lo + 1))

    def choose(self, options: list):
        return options[min(int(self.u() * len(options)), len(options)-1)]

    def weighted(self, options: list[tuple]):
        total = sum(weight for _, weight in options)
        if total <= 0:
            raise ValueError("invalid weights")
        n = self.u() * total
        for value, weight in options:
            n -= weight
            if n < 0:
                return value
        return options[-1][0]

def rounded(value: float) -> float:
    return round(float(value), 9)

def stellar_luminosity(mass: float) -> float:
    if mass < .43:
        return .23 * mass ** 2.3
    if mass < 2.0:
        return mass ** 4.0
    if mass < 20:
        return 1.5 * mass ** 3.5
    return 1.5 * mass ** 3.5

def stellar_age_limit(mass: float) -> float:
    return min(13.7, 10.0 * mass / stellar_luminosity(mass))

def star_from_mass(mass: float, age_gyr: float, star_id: str, binary: bool = False) -> dict:
    if not .10 <= mass <= 30 or age_gyr <= 0 or age_gyr >= stellar_age_limit(mass):
        raise ValueError("main-sequence star mass/age incompatible")
    spec = next(k for k, (lo, hi, _) in SPECTRAL.items() if lo <= mass <= hi)
    l = stellar_luminosity(mass)
    r = mass ** .8
    temp = 5772.0 * (l / r ** 2) ** .25
    return {
        "star_id": star_id, "kind": "main_sequence", "spectral_class": spec,
        "mass_solar": rounded(mass), "radius_solar": rounded(r),
        "luminosity_solar": rounded(l), "effective_temperature_k": rounded(temp),
        "age_gyr": rounded(age_gyr), "lifetime_estimate_gyr": rounded(stellar_age_limit(mass)),
        "binary_component": binary, "radiation_environment": "intense" if spec in ("O", "B") else "ordinary",
    }

def make_primary(rng: Rng, name: str = "Primary", forced_mass: float | None = None) -> dict:
    if forced_mass is None:
        spec = rng.weighted([(s, values[2]) for s, values in SPECTRAL.items()])
        lo, hi, _ = SPECTRAL[spec]
        mass = rng.between(lo, hi)
    else:
        mass = forced_mass
    lifetime = stellar_age_limit(mass)
    age = min(lifetime * rng.between(.12, .75), 11.8)
    return star_from_mass(mass, age, name)

def compact_object(seed: str, kind: str = "black_hole") -> dict:
    """Generate a standalone remnant; it is never a normal habitable star."""
    rng = Rng(seed, "compact", kind)
    if kind == "black_hole":
        mass = rounded(rng.between(3.0, 35.0))
        return {"kind": kind, "mass_solar": mass, "event_horizon_radius_km": rounded(2.95325*mass),
                "luminosity_solar": 0.0, "accretion_state": "unmodelled",
                "surface": None, "ordinary_habitable_zone": None, "planets": []}
    if kind in ("neutron_star", "pulsar"):
        mass = rounded(rng.between(1.2, 2.1))
        radius = rounded(rng.between(10, 13))
        return {"kind": kind, "mass_solar": mass, "radius_km": radius,
                "spin_period_s": rounded(rng.between(.02, 2.0)) if kind == "pulsar" else None,
                "radiation_hazard": "extreme", "ordinary_habitable_zone": None, "planets": []}
    if kind == "white_dwarf":
        mass = rounded(rng.between(.50, 1.20))
        radius = rounded(rng.between(.008, .015))
        t = rounded(rng.between(5000, 30000))
        return {"kind": kind, "mass_solar": mass, "radius_solar": radius,
                "effective_temperature_k": t,
                "luminosity_solar": rounded(radius**2*(t/5772)**4),
                "cooling_state": "approximate", "ordinary_habitable_zone": None, "planets": []}
    if kind == "brown_dwarf":
        mass = rounded(rng.between(.015, .074))
        return {"kind": kind, "mass_solar": mass, "radius_solar": .10,
                "luminosity_solar": rounded(rng.between(.000005,.0005)),
                "nuclear_hydrogen_fusion": False, "ordinary_habitable_zone": None, "planets": []}
    raise ValueError("unknown compact/brown-dwarf kind")

def trek_class_candidate(family: str, surface_temp: float | None,
                         liquid_water: float, pressure: float | None) -> str:
    """Science-derived provisional gameplay nomenclature, NEVER a canon fact."""
    if family in ENVELOPED_FAMILIES:
        return "J" if family=="gas_giant" else "J_candidate"
    if surface_temp is None or pressure is None:
        raise ValueError("rocky world missing basic physics")
    if surface_temp>450 or pressure>30:
        return "Y_candidate"
    if 270<=surface_temp<=325 and liquid_water>=.08 and .45<=pressure<=6:
        return "M_candidate"
    if surface_temp<245:
        return "P_candidate"
    if liquid_water==0 and surface_temp>=275:
        return "H_candidate"
    return "L_candidate"


def planet_physics(star_mass: float, luminosity: float, age_gyr: float,
                   orbit_au: float, family: str, seed: str,
                   recipe: dict | None = None) -> dict:
    """Derive a planet from physical inputs; no life or Trek class inputs accepted."""
    if family not in ALL_FAMILIES or orbit_au <= 0 or luminosity <= 0 or star_mass <= 0:
        raise ValueError("invalid planet/star configuration")
    recipe = recipe or {}
    forbidden = {"planet_class", "biosphere", "life", "surface_gravity_earth", "surface_temperature_k", "star_trek_class"}
    if forbidden & recipe.keys():
        raise ValueError("derived physics/life cannot be imposed by a recipe")
    rng = Rng(seed, "body", family, round(orbit_au, 7))
    mass_range = {
        "rocky": (.2, 2.1), "super_earth": (2.1, 8.0), "desert": (.35, 2.2),
        "ocean": (.6, 3.3), "ice_rock": (.15, 3.0), "lava": (.2, 2.1),
        "mini_neptune": (5, 18), "ice_giant": (15, 70), "gas_giant": (80, 350),
    }[family]
    mass = float(recipe.get("mass_earth", rng.between(*mass_range)))
    if not mass_range[0] <= mass <= mass_range[1]:
        raise ValueError("mass outside selected composition family")
    has_surface = family in SURFACE_FAMILIES
    if family == "mini_neptune":
        radius = 2.1 + .3 * math.sqrt(mass)
    elif family == "ice_giant":
        radius = 3.2 + .25 * math.sqrt(mass)
    elif family == "gas_giant":
        radius = 9.5 + .17 * math.sqrt(mass)
    else:
        factor = 1.09 if family=="ocean" else .95 if family=="ice_rock" else 1.0
        radius = factor * mass ** .27
    gravity = mass/radius**2
    flux = luminosity/orbit_au**2
    albedo = {"rocky": .25, "super_earth": .26, "desert": .35, "ocean": .32,
              "ice_rock": .55, "lava": .12, "mini_neptune": .34, "ice_giant": .40, "gas_giant": .43}[family]
    eq_temp = 278.5 * (flux*(1-albedo))**.25
    water_inventory = float(recipe.get("water_inventory", rng.between(.0,.65) if family not in ("ocean","ice_rock") else rng.between(.55,.98)))
    if not 0 <= water_inventory <= 1:
        raise ValueError("water inventory outside [0,1]")
    if family in ("desert", "lava"):
        water_inventory = 0.0
    if not has_surface:
        water_inventory = 0.0   # hydrosphere: zero surface oceans, deep interiors may contain volatiles
    if has_surface:
        default_pressure = rng.between(.15,2.5) if mass >= .35 and eq_temp < 720 else 0.0
        pressure = float(recipe.get("pressure_bar", default_pressure))
        if pressure < 0 or pressure > 100:
            raise ValueError("invalid rocky atmosphere pressure")
        greenhouse = float(recipe.get("greenhouse_k", min(55,pressure * rng.between(9,22))))
        if not 0 <= greenhouse <= 90:
            raise ValueError("greenhouse offset outside bounded ordinary-climate model")
        # Very cold N2/CO2-bearing rocky atmospheres cannot stay at 1 bar.
        # Simplified volatile freeze-out; not a pressure-temperature chemistry solver.
        if eq_temp < 65:
            pressure=0.0
        elif eq_temp < 185:
            pressure=min(pressure,.50)
            greenhouse=min(greenhouse,10.0)
        surface_temp = eq_temp+greenhouse
        if pressure == 0:
            greenhouse=0.0
            surface_temp=eq_temp
            gases={}
            volatile_regime="collapsed_or_airless"
        elif eq_temp < 185:
            # Avoid gaseous CO2 and H2O in frozen outer terrestrial worlds.
            gases={"N2":.98,"Ar":.02} if eq_temp<90 else {"N2":.94,"CH4":.04,"Ar":.02}
            volatile_regime="cold_nitrogen_regime"
        else:
            co2=rounded(rng.between(.008,.12))
            h2o=rounded(rng.between(.0001,.02))
            ar=rounded(.01)
            gases={"N2":rounded(1-co2-h2o-ar),"CO2":co2,"H2O":h2o,"Ar":ar}
            volatile_regime="warm_or_hot_rocky_regime"
    else:
        pressure = None  # no single meaningful "surface pressure" for gas envelopes
        greenhouse = None
        surface_temp = None  # cloud-top temperature != a surface temperature
        if family == "gas_giant":
            gases={"H2":.86,"He":.13,"CH4":.01}
        else:
            gases={"H2":.77,"He":.21,"CH4":.02}
        volatile_regime="deep_gas_envelope"
    if family == "lava" and (not has_surface or eq_temp < 700):
        raise ValueError("lava world requires sufficient stellar irradiation")
    if family == "ocean" and (surface_temp is None or not 273 <= surface_temp <= 335 or pressure < .3):
        raise ValueError("ocean world requires stable surface liquid-water conditions")
    liquid_water = rounded(water_inventory if (has_surface and pressure >= .1 and 273<=surface_temp<=355) else 0)
    frozen_water = rounded(water_inventory if (has_surface and surface_temp<273) else 0)
    if not has_surface:
        terrain = ["cloud_bands"] if family=="gas_giant" else ["deep_atmosphere"]
    elif family == "lava":
        terrain=["magma","basalt"]
    elif liquid_water>.7:
        terrain=["ocean","island_crust"]
    elif frozen_water>.05:
        terrain=["ice","rock"]
    else:
        terrain=["rock","mineral_regolith"]
    radiation = "high" if flux>7 or star_mass>2.1 else "normal"
    habitable = bool(has_surface and 270<=surface_temp<=325 and .45<=pressure<=6
                     and liquid_water>=.08 and .25<=gravity<=2.5 and radiation=="normal"
                     and age_gyr>=.8)
    life_rng=Rng(seed,"biology",family,round(orbit_au,7))
    biological_stage="none"
    if habitable and life_rng.u()<.31:
        biological_stage=life_rng.weighted([("microbial",83),("complex",16.7),("sapient_potential",.3)])
    # Oxygen-rich conditions are produced only after a separately drawn biosphere process.
    photosynthesis=bool(biological_stage in ("complex","sapient_potential") and life_rng.u()<.60)
    if photosynthesis:
        o2=.19
        gases["N2"]=rounded(gases["N2"]-o2)
        gases["O2"]=o2
    if biological_stage=="none":
        biological_features=[]
    elif biological_stage=="microbial":
        biological_features=["microbial_mat","marine_microbes"] if liquid_water else ["microbial_mat"]
    else:
        biological_features=["microbial","aquatic_ecosystems"]
        if photosynthesis:
            biological_features.append("oxygenic_photosynthesis")
            if .25<=liquid_water<=.85 and 275<=surface_temp<=310:
                biological_features.append("vegetation_like")
    trek=trek_class_candidate(family,surface_temp,liquid_water,pressure)
    orbital_period=math.sqrt(orbit_au**3/star_mass)
    hill=orbit_au*(mass/(3*star_mass*M_EARTH_PER_SUN))**(1/3)
    # These attributes are broad, explicitly approximate feature seeds.
    # Rotation, tides and magnetic fields need a later temporal/thermal solver.
    tidally_locked=has_surface and orbit_au<.12*math.sqrt(luminosity)
    rotation_hours=orbital_period*365.25*24 if tidally_locked else rng.between(9,110)
    axial_tilt=0 if tidally_locked else rng.between(0,45)
    magnetosphere="possible" if has_surface and mass>=.45 and not tidally_locked else "undetermined"
    ringed=not has_surface and rng.u()<.30
    resource_families=(["iron","silicates","sulfides"] if has_surface
                      else ["hydrogen","helium","volatile_ices"])
    return {
        "family":family, "mass_earth":rounded(mass),"radius_earth":rounded(radius),
        "bulk_density_g_cm3":rounded(5.514*mass/radius**3),
        "gravity_earth":rounded(gravity),"escape_velocity_km_s":rounded(11.186*math.sqrt(mass/radius)),
        "orbit":{"semi_major_au":rounded(orbit_au),"eccentricity":rounded(rng.between(0,.08)),
                 "inclination_degrees":rounded(rng.between(0,4)),
                 "period_years":rounded(orbital_period),"hill_radius_au":rounded(hill),
                 "reference_frame":"system_barycentric_approx"},
        "rotation":{"period_hours":rounded(rotation_hours),
                    "axial_tilt_degrees":rounded(axial_tilt),
                    "tidally_locked_heuristic":tidally_locked},
        "field":{"magnetosphere":magnetosphere,
                 "estimated_radiation_exposure":radiation},
        "ring_system":{"exists":ringed,"source":"illustrative_optional_icy_debris" if ringed else None},
        "resources":{"potential_bulk_families":resource_families,
                     "deposits_surveyed":False,"extraction_sites":[]},
        "radiation":{"stellar_flux_earth":rounded(flux),"level":radiation},
        "climate":{"albedo":rounded(albedo),"equilibrium_temperature_k":rounded(eq_temp),
                   "greenhouse_delta_k":rounded(greenhouse) if greenhouse is not None else None,
                   "surface_temperature_k":rounded(surface_temp) if surface_temp is not None else None,
                   "model":"zero-dimensional energy balance; NOT a GCM"},
        "interior":{"core_materials":["iron","silicates"] if has_surface else ["rock","high_pressure_ices"],
                    "tectonics":"possible" if has_surface and .4<mass<4 else "not_surface_applicable"},
        "atmosphere":{"surface_pressure_bar":rounded(pressure) if pressure is not None else None,
                      "mole_fraction":gases,"has_solid_surface":has_surface,
                      "volatile_regime":volatile_regime},
        "hydrosphere":{"water_inventory_index":rounded(water_inventory),
                      "surface_liquid_fraction":liquid_water,"surface_ice_fraction":frozen_water},
        "surface":{"exists":has_surface,"terrain":terrain,
                   "biomes":(["microbial_ecosystem"] if biological_stage=="microbial"
                             else ["biotic_water"] if biological_stage!="none" else ["abiotic"]) if has_surface else []},
        "habitability":{"potentially_habitable_for_terran_life":habitable,
                         "not_proof_of_life":True},
        "biosphere":{"stage":biological_stage,"photosynthesis":photosynthesis,
                     "features":biological_features},
        "star_trek":{"class_candidate":trek,"classification_status":"GAMEPLAY_HEURISTIC_NOT_CANON"},
        "visual":{"asset_id":None,"surface_mesh_allowed":has_surface}
    }

def environmental_region(seed: str, kind: str, *, trek_provenance: str | None = None) -> dict:
    """Standalone environmental truth. A Star Trek anomaly needs a specific cause."""
    rng=Rng(seed,"region",kind)
    if kind in ("nebula","supernova_remnant","protoplanetary_disk"):
        return {"kind":kind,"radius_light_years":rounded(rng.between(.3,25.0)),
                "density_particles_cm3":rounded(rng.between(10,10000)),
                "composition":{"H2":.70,"He":.28,"dust_metals":.02},
                "ionizing_radiation":"elevated" if kind=="supernova_remnant" else "background",
                "sensor_interference_possible":True,"world_truth_only":True}
    if kind=="radiation_region":
        return {"kind":kind,"radius_au":rounded(rng.between(.2,50.0)),
                "flux_relative_index":rounded(rng.between(1,10)),
                "cause":"unresolved_host_cause_requires_validation","world_truth_only":True}
    if kind in ("subspace_anomaly","wormhole"):
        if not trek_provenance:
            raise ValueError("Star Trek anomalies require explicit lore/event provenance")
        return {"kind":kind,"provenance":trek_provenance,"stability":"undetermined",
                "spatial_extent":"undetermined","world_truth_only":True,
                "not_a_scientific_phenomenon_model":True}
    raise ValueError("unknown region type")


def body_entity(seed: str, name: str, entity_kind: str, ordinal: int,
                system_id: str, position_au: list[float], properties: dict,
                signatures: list[dict], *, parent_id: str | None = None) -> dict:
    body_id=f"gen:{entity_kind}:{token(seed,system_id,entity_kind,ordinal)}"
    return {
        "entity_id":body_id,"entity_type":entity_kind,
        "display_name":name,"parent_entity_id":parent_id,
        "origin":{"type":"procedural","generator_id":"trek_astro_physical_v1",
                  "generator_version":VERSION,"seed_hash":token(seed,system_id,length=32)},
        "spatial_state":{"system_id":system_id,"reference_frame":"system_barycentric_approx",
                         "position":{"unit":"AU","xyz":[rounded(c) for c in position_au]}},
        "ground_truth":{"classification":properties.get("family", entity_kind),
                        "properties":properties,"hidden_properties":{}},
        "signatures":signatures,
        "persistence":{"persistent":True,"materialized":True,"can_be_modified_by_campaign":True}
    }

def generate_system(seed: str, sector: str = "041", era: str = "tng_ds9_voyager",
                    date: str = "2383-01-01", *, profile: str = "game",
                    canonical_reserved: bool = False, forced_primary_mass: float | None = None) -> dict:
    """Create physical truth once, before observation. Callers persist the result."""
    if not seed or not sector or not era or not date or profile not in ("game","f06"):
        raise ValueError("invalid generation context")
    if canonical_reserved:
        raise ValueError("canonical reservations must be authored/loaded, never overwritten")
    root=f"{seed}|{sector}|{era}|{date}|{profile}|v{VERSION}"
    rng=Rng(root,"system")
    system_id=f"gen:system:{token(root,'system')}"
    primary=make_primary(Rng(root,"star"),"A",forced_primary_mass)
    stars=[primary]
    binary=profile=="game" and rng.u()<.12 and primary["mass_solar"]<3
    separation=0.0
    if binary:
        separation=rng.between(.04,.18)
        secondary_mass=rng.between(.10,min(primary["mass_solar"],1.8))
        age=min(primary["age_gyr"],stellar_age_limit(secondary_mass)*.8)
        secondary=star_from_mass(secondary_mass,age,"B",True)
        primary["binary_component"]=True
        stars.append(secondary)
    total_mass=sum(s["mass_solar"] for s in stars)
    total_luminosity=sum(s["luminosity_solar"] for s in stars)
    origin_star=[0.0,0.0,0.0]
    entities=[]
    for i,star in enumerate(stars):
        pos=[0.0,0.0,0.0]
        if binary:
            displacement=(stars[1]["mass_solar"] if i==0 else -stars[0]["mass_solar"])/total_mass*separation
            pos=[displacement,0.0,0.0]
        entities.append(body_entity(root,f"PROC-{sector} {star['star_id']}","star",i+1,
            system_id,pos,star,[{"type":"electromagnetic","strength":"extreme"},
                                 {"type":"thermal","strength":"extreme"},
                                 {"type":"gravimetric","strength":"strong"}]))
    nplanets=rng.integer(3,6) if profile=="f06" else rng.integer(3,9)
    a=max(.15,.20*math.sqrt(total_luminosity),separation*5.5)
    frost_line=2.7*math.sqrt(total_luminosity)
    parent_planets=[]
    previous=None
    for i in range(1,nplanets+1):
        planet_rng=Rng(root,"orbit",i)
        if i==1:
            a*=planet_rng.between(1.10,1.45)
        else:
            a*=planet_rng.between(1.75,2.25)
        if a<frost_line:
            family=planet_rng.weighted([("rocky",34),("desert",22),("super_earth",17),
                                        ("ocean",8),("mini_neptune",14),("lava",0)])
        else:
            family=planet_rng.weighted([("ice_rock",35),("ice_giant",30),
                                        ("gas_giant",27),("mini_neptune",8)])
        if family=="ocean" and not (.45<=total_luminosity/a**2<=2):
            family="rocky"
        try:
            physics=planet_physics(total_mass,total_luminosity,primary["age_gyr"],
                a,family,f"{root}|planet:{i}")
        except ValueError:
            if family!="ocean":
                raise
            # A world too hot/cold for liquid oceans is rocky, not a magical ocean world.
            family="rocky"
            physics=planet_physics(total_mass,total_luminosity,primary["age_gyr"],
                a,family,f"{root}|planet:{i}")
        if previous:
            # Recompute Hill separation with BOTH current planet masses after
            # each new orbit proposal. A new radius can change composition/mass;
            # the earlier frozen mass_sum underestimated some giant encounters.
            for attempt in range(80):
                mass_sum=previous[1]["mass_earth"]+physics["mass_earth"]
                mutual=(previous[0]+a)*.5*(mass_sum/(3*total_mass*M_EARTH_PER_SUN))**(1/3)
                if (a-previous[0])/mutual >= 9.1:
                    break
                a*=1.22
                try:
                    physics=planet_physics(total_mass,total_luminosity,primary["age_gyr"],
                        a,family,f"{root}|planet:{i}")
                except ValueError:
                    if family!="ocean":
                        raise
                    family="rocky"
                    physics=planet_physics(total_mass,total_luminosity,primary["age_gyr"],
                        a,family,f"{root}|planet:{i}")
            else:
                raise ValueError("cannot allocate safely separated planet orbit")
        angle=planet_rng.between(0,2*math.pi)
        xyz=[a*math.cos(angle),a*math.sin(angle),0.0]
        e=body_entity(root,f"PROC-{sector}-{i}","planet",i,system_id,xyz,physics,
          [{"type":"gravimetric","strength":"strong" if family in ENVELOPED_FAMILIES else "moderate"},
           {"type":"thermal","strength":"weak"}],parent_id=entities[0]["entity_id"])
        parent_planets.append(e)
        entities.append(e)
        previous=(a,physics)
        moons=planet_rng.integer(0,2 if profile=="f06" else 4)
        hill=physics["orbit"]["hill_radius_au"]
        min_distance=4.0*physics["radius_earth"]*EARTH_RADIUS_AU
        max_distance=min(.28*hill, 60*physics["radius_earth"]*EARTH_RADIUS_AU)
        for mi in range(moons):
            if max_distance<=min_distance*1.2:
                continue
            moon_rng=Rng(root,"moon",i,mi)
            orbit_moon=moon_rng.between(min_distance*1.1,max_distance*.98)
            moon_mass=physics["mass_earth"]*moon_rng.between(.00001,.008 if family in ENVELOPED_FAMILIES else .035)
            moon_mass=max(.0000001,moon_mass)
            moon_radius=max(.005,moon_mass**.27*.9)
            moon_phys={
                "parent_entity_id":e["entity_id"],"mass_earth":rounded(moon_mass),
                "radius_earth":rounded(moon_radius),
                "orbital_distance_au":rounded(orbit_moon),
                "orbital_distance_parent_radii":rounded(orbit_moon/(physics["radius_earth"]*EARTH_RADIUS_AU)),
                "parent_hill_radius_au":rounded(hill),
                "composition":"ice_rock" if a>frost_line else "silicate_rock",
                "surface":{"exists":True,"terrain":["rock","ice"] if a>frost_line else ["rock"],
                           "biomes":["abiotic"]},
                "biosphere":{"stage":"none"},
                "visual":{"asset_id":None}
            }
            angle_m=moon_rng.between(0,2*math.pi)
            mxyz=[xyz[0]+orbit_moon*math.cos(angle_m),
                  xyz[1]+orbit_moon*math.sin(angle_m),0.0]
            entities.append(body_entity(root,f"PROC-{sector}-{i}-{mi+1}","moon",
                i*10+mi+1,system_id,mxyz,moon_phys,
                [{"type":"gravimetric","strength":"weak"}],parent_id=e["entity_id"]))
    if parent_planets:
        belt_anchor=parent_planets[-1]["ground_truth"]["properties"]["orbit"]["semi_major_au"]*1.40
        belt={"kind":"asteroid_belt","semi_major_au":rounded(belt_anchor),
              "width_au":rounded(.05*belt_anchor),"composition":["silicates","metal","ice"],
              "model":"aggregate_population_not_individual_asteroids"}
        entities.append(body_entity(root,f"PROC-{sector} belt","asteroid_belt",1,
             system_id,[belt_anchor,0,0],belt,[{"type":"gravimetric","strength":"weak"}]))
        if profile=="game":
            comet_q=max(.04, .3*math.sqrt(total_luminosity))
            comet_a=belt_anchor*2.0
            comet={"kind":"comet","semi_major_au":rounded(comet_a),
                   "eccentricity":rounded(1-comet_q/comet_a),
                   "periapsis_au":rounded(comet_q),
                   "apoapsis_au":rounded(2*comet_a-comet_q),
                   "composition":["water_ice","CO2_ice","dust"]}
            entities.append(body_entity(root,f"PROC-{sector} comet","comet",1,
                system_id,[comet_a,0,0],comet,[{"type":"thermal","strength":"trace"}]))
    result={
        "schema_version":"1.0.0",
        "generator":{"generator_id":"trek_astro_physical_v1",
                     "generator_version":VERSION,"algorithm":"sha256_counter_physical_first"},
        "generation_context":{"campaign_seed":seed,"sector_id":sector,
            "era_id":era,"campaign_date":date,"seed_key_hash":token(root,length=32)},
        "system":{"system_id":system_id,"display_name":f"PROC-{sector}-{token(root,length=6).upper()}",
                  "canonical_reserved":False,"materialized":True,
                  "primary_stellar_mass_solar":rounded(total_mass),
                  "luminosity_solar":rounded(total_luminosity),
                  "stellar_age_gyr":primary["age_gyr"],
                  "architecture":"circumbinary_approx" if binary else "single",
                  "binary_separation_au":rounded(separation),
                  "frost_line_au":rounded(frost_line),
                  "habitable_flux_reference":"heuristic; not a climate/biology guarantee"},
        "entities":entities,
        "relations":[{"type":"orbits","child":x["entity_id"],"parent":x["parent_entity_id"]}
                     for x in entities if x["parent_entity_id"]],
        "summary":{"stars":len(stars),"planets":len(parent_planets),
                   "moons":sum(x["entity_type"]=="moon" for x in entities),
                   "life_candidate_planets":sum(x["ground_truth"]["properties"]["biosphere"]["stage"]!="none"
                     for x in parent_planets)}
    }
    errors=validate_system(result)
    if errors:
        raise ValueError("generated incoherent system: "+"; ".join(errors))
    return result

def validate_planet(p: dict, star_mass: float, luminosity: float, age_gyr: float) -> list[str]:
    errors=[]
    fam=p.get("family")
    surface=fam in SURFACE_FAMILIES
    if fam not in ALL_FAMILIES:
        return ["invalid family"]
    a=p["orbit"]["semi_major_au"]
    mass=p["mass_earth"]
    radius=p["radius_earth"]
    if a<=0 or mass<=0 or radius<=0:
        return ["invalid orbital/bulk value"]
    if abs(p["gravity_earth"]-mass/radius**2)>0.00001:
        errors.append("incoherent gravity")
    if abs(p["orbit"]["period_years"]**2*star_mass-a**3)>max(.0001,a**3*.00001):
        errors.append("Kepler's third law mismatch")
    if abs(p["radiation"]["stellar_flux_earth"]-luminosity/a**2)>max(.0001,luminosity/a**2*.0001):
        errors.append("flux vs distance/luminosity mismatch")
    atm=p["atmosphere"]
    water=p["hydrosphere"]
    bio=p["biosphere"]
    if atm["mole_fraction"]:
        if not math.isclose(sum(atm["mole_fraction"].values()),1.0,abs_tol=.00001):
            errors.append("atmospheric fractions do not total 1")
    elif atm["surface_pressure_bar"] != 0:
        errors.append("atmosphere without gas composition")
    if not surface:
        if atm["has_solid_surface"] or atm["surface_pressure_bar"] is not None or p["surface"]["exists"]:
            errors.append("gas envelope cannot have accessible solid surface")
        if water["surface_liquid_fraction"] or water["surface_ice_fraction"] or p["surface"]["biomes"]:
            errors.append("gas envelope cannot have surface water/forests/biomes")
        if bio["stage"]!="none" or p["habitability"]["potentially_habitable_for_terran_life"]:
            errors.append("gas envelope cannot receive terrestrial surface life")
    else:
        if not atm["has_solid_surface"] or not p["surface"]["exists"]:
            errors.append("rocky world needs a surface")
        t=p["climate"]["surface_temperature_k"]
        if water["surface_liquid_fraction"] and not (273<=t<=355 and atm["surface_pressure_bar"]>=.1):
            errors.append("liquid water incompatible with temperature/pressure")
        if bio["stage"]!="none" and not p["habitability"]["potentially_habitable_for_terran_life"]:
            errors.append("life without bounded plausible conditions")
        if p["habitability"]["potentially_habitable_for_terran_life"] and age_gyr<.8:
            errors.append("biosphere before allowable stellar age")
        if "vegetation_like" in bio["features"] and not (bio["photosynthesis"] and bio["stage"] in ("complex","sapient_potential")):
            errors.append("unmotivated vegetation")
    if atm["mole_fraction"].get("O2",0)>.10 and not bio["photosynthesis"]:
        errors.append("high oxygen without modeled biological source")
    if p["visual"]["surface_mesh_allowed"]!=surface:
        errors.append("visual representation contradicts physical structure")
    expected_trek=trek_class_candidate(fam,p["climate"]["surface_temperature_k"],
        water["surface_liquid_fraction"],atm["surface_pressure_bar"])
    if p["star_trek"]["class_candidate"]!=expected_trek:
        errors.append("Star Trek class contradicts derived physics")
    return errors

def validate_system(world: dict) -> list[str]:
    errors=[]
    sys=world["system"]
    if sys["canonical_reserved"] or not sys["materialized"]:
        errors.append("canon reservation/materialization violated")
    stars=[e for e in world["entities"] if e["entity_type"]=="star"]
    planets=[e for e in world["entities"] if e["entity_type"]=="planet"]
    moons=[e for e in world["entities"] if e["entity_type"]=="moon"]
    ids=[e["entity_id"] for e in world["entities"]]
    if not 1<=len(stars)<=2 or len(set(ids))!=len(ids):
        errors.append("star count or entity IDs invalid")
    if len(planets)<3:
        errors.append("planet count invalid")
    sm=sys["primary_stellar_mass_solar"]
    lum=sys["luminosity_solar"]
    if any(e["ground_truth"]["properties"]["kind"]!="main_sequence" for e in stars):
        errors.append("compact remnant unexpectedly used as life-hosting star")
    for e in stars:
        s=e["ground_truth"]["properties"]
        if abs(s["luminosity_solar"]-s["radius_solar"]**2*(s["effective_temperature_k"]/5772)**4)>max(.01,s["luminosity_solar"]*.0001):
            errors.append("stellar Stefan-Boltzmann mismatch")
    parents={e["entity_id"]:e for e in planets}
    seen=[]
    for e in planets:
        p=e["ground_truth"]["properties"]
        errors.extend([f"{e['entity_id']}: {err}" for err in validate_planet(p,sm,lum,sys["stellar_age_gyr"])])
        seen.append((p["orbit"]["semi_major_au"],p["mass_earth"]))
    seen.sort()
    for (a,m),(b,n) in zip(seen,seen[1:]):
        mutual=(a+b)*.5*((m+n)/(3*sm*M_EARTH_PER_SUN))**(1/3)
        if (b-a)/mutual<8:
            errors.append("adjacent planetary orbits too closely packed")
    if sys["architecture"]=="circumbinary_approx":
        if min(a for a,_ in seen)<5*sys["binary_separation_au"]:
            errors.append("circumbinary orbit too close to binary")
    for moon in moons:
        p=moon["ground_truth"]["properties"]
        if moon["parent_entity_id"] not in parents:
            errors.append("orphan moon")
            continue
        parent=parents[moon["parent_entity_id"]]["ground_truth"]["properties"]
        dist=p["orbital_distance_au"]
        hill=parent["orbit"]["hill_radius_au"]
        if not (3*parent["radius_earth"]*EARTH_RADIUS_AU<dist<.30*hill):
            errors.append("moon outside Roche/Hill approximate stable band")
        if p["mass_earth"]>=.04*parent["mass_earth"]:
            errors.append("moon mass too high for bounded fixture model")
    return errors

def public_sensor_catalog(world: dict) -> list[dict]:
    """Coarse host signatures. No hidden atmospheric/biological science leaks."""
    allowed={"star","planet","moon","asteroid_belt","comet"}
    out=[]
    for entity in world["entities"]:
        if entity["entity_type"] not in allowed:
            continue
        out.append({"key":entity["entity_id"],
                    "category":entity["entity_type"],
                    "position_au":entity["spatial_state"]["position"]["xyz"],
                    "signal_types":[x["type"] for x in entity["signatures"]]})
    return out

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--seed",required=True)
    parser.add_argument("--sector",default="041")
    parser.add_argument("--era",default="tng_ds9_voyager")
    parser.add_argument("--date",default="2383-01-01")
    parser.add_argument("--profile",choices=("game","f06"),default="game")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=generate_system(args.seed,args.sector,args.era,args.date,profile=args.profile)
    data=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data,encoding="utf-8")
    else:
        print(data)

if __name__=="__main__":
    main()
