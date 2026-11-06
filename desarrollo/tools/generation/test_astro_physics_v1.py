#!/usr/bin/env python3
"""Coherence, regression and F06 handoff tests for astro_physics_v1."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0,str(HERE))

import astro_physics_v1 as astro
import enrich_aster_f06_v1 as aster


class AstroV1Tests(unittest.TestCase):
    def test_determinism_without_global_rng(self):
        one=astro.generate_system("campaign/fixture/alpha","089")
        two=astro.generate_system("campaign/fixture/alpha","089")
        three=astro.generate_system("campaign/fixture/beta","089")
        self.assertEqual(one,two)
        self.assertNotEqual(one["system"]["system_id"],three["system"]["system_id"])
        self.assertEqual(astro.validate_system(one),[])
        self.assertEqual(len({e["entity_id"] for e in one["entities"]}),len(one["entities"]))

    def test_many_seeds_and_both_scopes(self):
        binaries=0
        for profile in ("game","f06"):
            for i in range(80):
                world=astro.generate_system(f"physics-stress-{i}","041",profile=profile)
                self.assertEqual(astro.validate_system(world),[],msg=(profile,i))
                binaries+=world["system"]["architecture"]=="circumbinary_approx"
                for e in world["entities"]:
                    if e["entity_type"]=="planet":
                        p=e["ground_truth"]["properties"]
                        if p["family"] in astro.ENVELOPED_FAMILIES:
                            self.assertIsNone(p["climate"]["surface_temperature_k"])
                            self.assertFalse(p["surface"]["exists"])
                            self.assertEqual(p["biosphere"]["stage"],"none")
                            self.assertEqual(p["surface"]["biomes"],[])
                        if p["biosphere"]["stage"]!="none":
                            self.assertTrue(p["habitability"]["potentially_habitable_for_terran_life"])
                            self.assertGreaterEqual(p["hydrosphere"]["surface_liquid_fraction"],.08)
        self.assertGreater(binaries,0)

    def test_forced_star_spectra(self):
        for mass in (.12,.60,.95,1.20,1.80,7.0,24.0):
            world=astro.generate_system(f"mass-{mass}",forced_primary_mass=mass)
            self.assertEqual(astro.validate_system(world),[])
            self.assertEqual(world["entities"][0]["entity_type"],"star")

    def test_no_canonical_overwrite(self):
        with self.assertRaisesRegex(ValueError,"canonical"):
            astro.generate_system("vulcan",canonical_reserved=True)
        with self.assertRaisesRegex(ValueError,"derived physics"):
            astro.planet_physics(1.0,1.0,4.0,1.0,"rocky","bad",
                                 {"biosphere":"sapient"})
        with self.assertRaisesRegex(ValueError,"ocean world"):
            astro.planet_physics(1.0,1.0,4.0,.12,"ocean","boiling",
                                 {"mass_earth":1.0,"pressure_bar":1,
                                  "greenhouse_k":5})
        with self.assertRaisesRegex(ValueError,"lava world"):
            astro.planet_physics(1.0,1.0,4.0,5.0,"lava","frozen")

    def test_reject_forest_on_giant_and_unmotivated_life(self):
        world=astro.generate_system("validation-attack")
        giant=next((e for e in world["entities"] if e["entity_type"]=="planet" and
                e["ground_truth"]["properties"]["family"] in astro.ENVELOPED_FAMILIES),None)
        if giant is None:
            giant=astro.planet_physics(1,1,4,5,"gas_giant","gas")
            giant["surface"]["biomes"]=["forest"]
            self.assertIn("gas envelope", " ".join(astro.validate_planet(giant,1,1,4)))
        else:
            copied=copy.deepcopy(world)
            target=next(e for e in copied["entities"] if e["entity_id"]==giant["entity_id"])
            target["ground_truth"]["properties"]["surface"]["biomes"]=["forest"]
            self.assertTrue(astro.validate_system(copied))
        p=astro.planet_physics(1,1,4,5,"ice_rock","dry")
        p["biosphere"]["stage"]="complex"
        self.assertTrue(astro.validate_planet(p,1,1,4))

    def test_remnants_are_not_stars_with_habitable_planets(self):
        for kind in ("black_hole","white_dwarf","neutron_star","pulsar","brown_dwarf"):
            obj=astro.compact_object("compact",kind)
            self.assertEqual(obj["kind"],kind)
            self.assertIsNone(obj["ordinary_habitable_zone"])
            self.assertEqual(obj["planets"],[])
            self.assertEqual(obj,astro.compact_object("compact",kind))
        self.assertGreater(astro.compact_object("compact")["event_horizon_radius_km"],0)

    def test_sensor_projection_does_not_expose_life_atmosphere(self):
        world=astro.generate_system("sensor-nonleak")
        projection=astro.public_sensor_catalog(world)
        self.assertTrue(projection)
        txt=json.dumps(projection).lower()
        for field in ("ground_truth","biosphere","atmosphere","planet_class",
                      "surface_temperature","photosynthesis","m_candidate"):
            self.assertNotIn(field,txt)

    def test_planet_physical_orbital_constraints(self):
        p=astro.planet_physics(1.0,1.0,4.6,1.0,"rocky","earth-like",
                               {"mass_earth":1.0,"pressure_bar":1,"greenhouse_k":33,
                                "water_inventory":.7})
        self.assertEqual(astro.validate_planet(p,1.0,1.0,4.6),[])
        tampered=copy.deepcopy(p)
        tampered["star_trek"]["class_candidate"]="J"
        self.assertIn("Star Trek class contradicts derived physics",
                      astro.validate_planet(tampered,1.0,1.0,4.6))
        self.assertAlmostEqual(p["gravity_earth"],1,places=7)
        self.assertAlmostEqual(p["orbit"]["period_years"],1,places=7)
        self.assertAlmostEqual(p["radiation"]["stellar_flux_earth"],1,places=7)
        self.assertTrue(p["hydrosphere"]["surface_liquid_fraction"]>.0)

    def test_very_cold_rocky_atmospheres_collapse(self):
        frozen=astro.planet_physics(1.0,1.0,4.6,30.0,"ice_rock","condensation",
                                   {"mass_earth":1.0,"pressure_bar":1.0,
                                    "greenhouse_k":50})
        self.assertEqual(frozen["atmosphere"]["surface_pressure_bar"],0)
        self.assertEqual(frozen["atmosphere"]["mole_fraction"],{})
        self.assertEqual(frozen["atmosphere"]["volatile_regime"],"collapsed_or_airless")
        self.assertEqual(frozen["hydrosphere"]["surface_liquid_fraction"],0)
        self.assertEqual(astro.validate_planet(frozen,1.0,1.0,4.6),[])

    def test_aster_six_planets_and_host_only_truth(self):
        src=ROOT/"integration/f06/fixtures/aster_f06_qa.json"
        base=json.loads(src.read_text(encoding="utf-8"))
        enriched=aster.enrich(base)
        self.assertEqual(enriched,aster.enrich(base))
        self.assertNotIn("science_generation",base)
        objs={x["key"]:x for x in enriched["entities"]}
        self.assertEqual(len([x for x in enriched["entities"] if x["kind"]=="planet"]),6)
        self.assertEqual(objs[202]["science_truth"]["planet_class"],"M_candidate")
        self.assertEqual(objs[204]["science_truth"]["planet_class"],"J")
        self.assertEqual(objs[203]["science_truth"]["planet_class"],"P_candidate")
        for key in aster.RECIPES:
            p=objs[key]["science_truth"]["physical_planet"]
            self.assertEqual(astro.validate_planet(p,1.0,1.0,4.6),[])
        for k in aster.MOON_OFFSETS:
            self.assertLess(objs[k]["science_truth"]["orbital_distance_au"],
                            .3*objs[k]["science_truth"]["parent_hill_radius_au"])
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp)
            fixture=tmp/"physical.json"
            header=tmp/"f06_system.h"
            fixture.write_text(json.dumps(enriched),encoding="utf-8")
            compiler=ROOT/"integration/f06/build_validation_system.py"
            subprocess.run([sys.executable,str(compiler),"--source",str(fixture),
                            "--out",str(header)],check=True)
            generated=header.read_text(encoding="utf-8")
            for secret in ("M_candidate","P_candidate","photosynthesis","biosphere","mass_earth"):
                self.assertNotIn(secret,generated)
            self.assertIn("F06_DEMO_FRAMES",generated)

if __name__=="__main__":
    unittest.main(verbosity=2)
