#!/usr/bin/env python3
import copy
import unittest
from pathlib import Path
import f06_b_world_reference as b
import astro_physics_v1 as astro

FIXTURE = b.ROOT / "desarrollo/validation/fixtures/f06_b/world_request_v1.json"


class WorldReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.request=b.load(FIXTURE)
        cls.catalog=b.load(b.CATALOG)
        cls.world=b.generate(cls.request)

    def modified(self, fn):
        r=copy.deepcopy(self.request);fn(r);return r

    def test_repeatability(self):
        self.assertEqual(self.world,b.generate(self.request))

    def test_reorder_needs_no_reroll(self):
        r=self.modified(lambda x:x["needs"].reverse())
        self.assertEqual(self.world["ships"],b.generate(r)["ships"])

    def test_seed_changes_identity(self):
        r=self.modified(lambda x:x.update(seed="different-campaign"))
        other=b.generate(r)
        self.assertNotEqual(self.world["system"]["system"]["system_id"],other["system"]["system"]["system_id"])
        self.assertTrue(set(s["ship_id"] for s in self.world["ships"]).isdisjoint(s["ship_id"] for s in other["ships"]))

    def test_physical_system(self):
        self.assertEqual(astro.validate_system(self.world["system"]),[])
        for e in self.world["system"]["entities"]:
            p=e["ground_truth"]["properties"]
            if e["entity_type"]=="planet":
                self.assertIn("human_atmosphere_screen",p)
                self.assertIn("gravity_earth",p)
            if e["entity_type"]=="moon":
                self.assertGreater(p["gravity_earth"],0)

    def test_aster_ii_not_breathable(self):
        p=astro.planet_physics(1.0,1.0,4.6,1.3,"rocky","aster|202",
            {"mass_earth":1.05,"pressure_bar":1.0,"greenhouse_k":65,"water_inventory":.68})
        self.assertEqual(p["star_trek"]["class_candidate"],"M_candidate")
        self.assertEqual(p["atmosphere"]["mole_fraction"].get("O2",0),0)
        self.assertEqual(b.human_atmosphere(p)["class_m_status"],"M_CLIMATE_CANDIDATE_NOT_BREATHABLE")
        self.assertEqual(round(p["climate"]["surface_temperature_k"]),292)

    def test_gas_giant_not_surface_vacuum(self):
        p=astro.planet_physics(1,1,4.6,5.8,"gas_giant","gas",{"mass_earth":170})
        self.assertIsNone(p["atmosphere"]["surface_pressure_bar"])
        self.assertEqual(b.human_atmosphere(p)["status"],"NOT_APPLICABLE")
        self.assertGreater(p["atmosphere"]["mole_fraction"]["H2"],0)

    def test_ship_design_and_instance_distinct(self):
        a,z=[s for s in self.world["ships"] if s["operator"]=="independent_civilian"]
        self.assertEqual(a["design_id"],z["design_id"])
        self.assertNotEqual(a["ship_id"],z["ship_id"])
        self.assertNotEqual(a["designation"],z["designation"])
        self.assertNotEqual(a["mission"]["need_id"],z["mission"]["need_id"])
        self.assertEqual(a["physical_design"],z["physical_design"])

    def test_military_weapon_types_and_ammo(self):
        s=next(s for s in self.world["ships"] if s["operator"]=="romulan_military")
        self.assertEqual(s["design_key"],"dderidex")
        launch=[m for m in s["modules"] if m["technology_id"]=="qa_plasma_launcher"]
        self.assertEqual(len(launch),3)
        self.assertTrue(all(m["ammo"]["type"]=="plasma_torpedo" for m in launch))
        self.assertEqual(len([m for m in s["modules"] if m["technology_id"]=="qa_disruptor"]),8)

    def test_effect_not_equivalent_to_count(self):
        t=self.catalog["technologies"]
        self.assertGreater(t["qa_exotic_projector"]["effect"],64*t["qa_primitive_projectile"]["effect"])
        self.assertNotEqual(t["qa_exotic_projector"]["family"],t["qa_primitive_projectile"]["family"])

    def test_people_conserved_and_individual(self):
        for s in self.world["ships"]:
            self.assertEqual(len(s["people"]),s["reference_baseline"]["population"]["total_people_aboard_initial"])
            self.assertEqual(len({p["person_id"] for p in s["people"]}),len(s["people"]))
            self.assertTrue(all(p["species"] and p["life_state"]=="alive" for p in s["people"]))

    def test_cargo_conservation(self):
        total=sum(x["mass_kg"] for x in self.world["initial_stock"])
        remaining=sum(x["mass_kg"] for x in self.world["remaining_stock"])
        loaded=sum(x["mass_kg"] for s in self.world["ships"] for x in s["cargo"])
        self.assertEqual(loaded,15000)
        self.assertEqual(total,remaining+loaded)

    def test_replay_chunk_invariant(self):
        direct=b.evolve(self.world,540)
        chunked=b.evolve(b.evolve(b.evolve(self.world,10),250),540)
        self.assertEqual(direct,chunked)
        self.assertEqual(self.world["tick"],0)
        self.assertEqual(len(direct["events"]),9)
        self.assertTrue(b.verify_candidate(self.request,direct))
        self.assertEqual(direct,b.evolve(direct,540))
        for s,old in zip(direct["ships"],self.world["ships"]):
            self.assertEqual([p["person_id"] for p in s["people"]],[p["person_id"] for p in old["people"]])
            self.assertEqual([m["module_id"] for m in s["modules"]],[m["module_id"] for m in old["modules"]])

    def test_no_scan_driven_request(self):
        with self.assertRaises(ValueError):
            b.generate(self.modified(lambda x:x.update(observer_id="player")))

    def test_reserved_system_rejected(self):
        with self.assertRaises(ValueError):
            b.generate(self.modified(lambda x:x.update(canonical_reserved=True)))

    def test_wrong_era_rejected(self):
        with self.assertRaises(ValueError):
            b.generate(self.modified(lambda x:x.update(date="2259-01-01")))

    def test_missing_cause_rejected(self):
        with self.assertRaises(ValueError):
            b.generate(self.modified(lambda x:x["needs"][0].update(cause_ref="")))

    def test_duplicate_need_rejected(self):
        with self.assertRaises(ValueError):
            b.generate(self.modified(lambda x:x["needs"].append(copy.deepcopy(x["needs"][0]))))

    def test_unfunded_cargo_rejected(self):
        with self.assertRaises(ValueError):
            b.generate(self.modified(lambda x:x["needs"][0]["cargo_orders"][0].update(mass_kg=50001)))

    def test_unknown_population_rejected(self):
        with self.assertRaises(ValueError):
            b.generate(self.modified(lambda x:x["needs"][0].update(species_weights={"unknown":1})))

    def test_tamper_person_location(self):
        w=copy.deepcopy(self.world);w["ships"][0]["people"][0]["compartment_id"]="nonexistent"
        with self.assertRaises(ValueError): b.validate_world(w)

    def test_tamper_technology(self):
        w=copy.deepcopy(self.world);w["ships"][0]["modules"][0]["technology_id"]="fake"
        with self.assertRaises(ValueError): b.validate_world(w)

    def test_tamper_energy(self):
        w=copy.deepcopy(self.world);w["ships"][0]["energy"]["available_qa_units"]+=1
        with self.assertRaises(ValueError): b.validate_world(w)

    def test_tamper_cargo(self):
        w=copy.deepcopy(self.world);w["remaining_stock"][0]["mass_kg"]+=1
        with self.assertRaises(ValueError): b.validate_world(w)

    def test_civilian_refit_is_individual_and_energizes(self):
        civil=[s for s in self.world["ships"] if s["operator"]=="independent_civilian"]
        self.assertEqual([len(s["refits"]) for s in civil],[0,1])
        armed=next(s for s in b.evolve(self.world,210)["ships"] if s["refits"])
        emitter=next(m for m in armed["modules"] if m["technology_id"]=="qa_civil_defensive_emitter")
        self.assertEqual(emitter["state"],"energized")
        self.assertEqual(emitter["installation_revision"],1)

    def test_readiness_drill_and_medical_event(self):
        def patrol(at):
            return next(s for s in b.evolve(self.world,at)["ships"] if s["operator"]=="romulan_military")
        mid=next(m["module_id"] for m in patrol(300)["modules"] if m["technology_id"]=="qa_disruptor")
        self.assertEqual(next(m["state"] for m in patrol(300)["modules"] if m["module_id"]==mid),"active")
        self.assertEqual(next(m["state"] for m in patrol(420)["modules"] if m["module_id"]==mid),"idle")
        self.assertEqual(patrol(320)["people"][0]["medical_severity"],35)
        self.assertEqual(patrol(319)["people"][0]["medical_severity"],0)

    def test_unknown_design_has_private_geometry_and_real_technology(self):
        r=self.modified(lambda x:None)
        need=copy.deepcopy(r["needs"][0])
        need.update(need_id="qa:need:experimental",cause_ref="qa:cause:experimental",mode="experimental",
                    operator="qa_unknown",role="survey",cargo_orders=[],refits=[])
        r["needs"].append(need)
        r["causes"].append({"cause_ref":need["cause_ref"],"kind":"experimental_test","need_id":need["need_id"],
                             "authority_ref":"qa:authoring:experimental"})
        w=b.generate(r)
        s=next(s for s in w["ships"] if s["operator"]=="qa_unknown")
        self.assertTrue(s["geometry"]["parts"])
        self.assertEqual(len([m for m in s["modules"] if m["technology_id"]=="qa_exotic_projector"]),1)
        self.assertTrue(b.verify_candidate(r,w))

    def test_quantum_torpedo_configuration(self):
        r=self.modified(lambda x:None)
        n=copy.deepcopy(r["needs"][2])
        n.update(need_id="qa:need:sf",cause_ref="qa:cause:sf",operator="starfleet",role="high_threat_response",
                 species_weights={"human":1})
        r["needs"].append(n)
        r["causes"].append({"cause_ref":n["cause_ref"],"kind":"patrol_order","need_id":n["need_id"],"authority_ref":"qa:sf-command"})
        w=b.generate(r)
        s=next(s for s in w["ships"] if s["operator"]=="starfleet")
        self.assertEqual(s["design_key"],"sovereign")
        self.assertTrue(any(m["ammo"] and m["ammo"]["type"]=="quantum_torpedo" for m in s["modules"]))

    def test_mismatched_refit_authority_rejected(self):
        with self.assertRaises(ValueError):
            b.generate(self.modified(lambda x:x["needs"][1]["refits"][0].update(cause_ref=x["needs"][0]["cause_ref"])))

    def test_action_wrong_scope_rejected(self):
        with self.assertRaises(ValueError):
            b.generate(self.modified(lambda x:x["actions"][1].update(cause_ref=x["actions"][0]["cause_ref"])))

    def test_journal_tamper_rejected(self):
        w=b.evolve(self.world,540);w["events"].pop()
        with self.assertRaises(ValueError): b.validate_world(w)

    def test_same_count_different_person_rejected_by_source_replay(self):
        w=copy.deepcopy(self.world)
        p=w["ships"][0]["people"][0]
        p["age_years_at_epoch"]=21 if p["age_years_at_epoch"]!=21 else 22
        with self.assertRaises(ValueError): b.verify_candidate(self.request,w)

    def test_no_action_triggered_by_scan_input(self):
        with self.assertRaises(ValueError):
            b.generate(self.modified(lambda x:x["needs"][0].update(observer_scan=True)))

    def test_backwards_time_rejected(self):
        with self.assertRaises(ValueError): b.evolve(b.evolve(self.world,100),99)


if __name__=="__main__":
    unittest.main(verbosity=2)
