#!/usr/bin/env python3
"""Pruebas positivas y adversariales del anexo LORE, no de UE/HOST/Core."""
import copy
import unittest
from pathlib import Path
from validate_operacion_lore_20261122 import read, problems, ROOT, CATALOGUE, ANNEX, VALHALLA, LEGACY_TECH

class OperationLoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = read()
    def check_bad(self, mutate):
        altered = copy.deepcopy(self.original)
        mutate(altered)
        self.assertTrue(problems(altered), "una mutación insegura debe detectarse")
    def test_integridad_documental(self):
        self.assertEqual(problems(self.original), [])
    def test_cambio_de_clase_enterprise_d_rechazado(self):
        self.check_bad(lambda d: d[VALHALLA]["subject"].__setitem__("class_id", "valhalla"))
    def test_alta_2387_forzada_rechazada(self):
        self.check_bad(lambda d: d[VALHALLA]["future"].__setitem__("readiness_2387_guaranteed", True))
    def test_valtec_duplicada_rechazada(self):
        self.check_bad(lambda d: d[LEGACY_TECH]["decisions"].__setitem__(1, d[LEGACY_TECH]["decisions"][0]))
    def test_lore_no_importa_runtime(self):
        self.check_bad(lambda d: d[CATALOGUE].__setitem__("runtime_import_allowed", True))
    def test_lore_no_causa_materializacion(self):
        self.check_bad(lambda d: d[CATALOGUE]["records"][0].__setitem__("auto_materialize", True))
    def test_acciones_se_someten_a_core(self):
        self.check_bad(lambda d: d[CATALOGUE]["records"][1].__setitem__("release_gate", "ALLOW_ALWAYS"))
    def test_no_filtrar_exp_reservado(self):
        self.check_bad(lambda d: d[CATALOGUE]["records"][-3].__setitem__("default_visibility", "WORLD_ACCESS_FREE"))
    def test_no_borrar_fuente(self):
        self.check_bad(lambda d: d[CATALOGUE]["records"][0].__setitem__("source_paths", ["mundo/lore/NO_SUCH_SOURCE.md"]))
    def test_nombre_del_jugador_editable(self):
        self.check_bad(lambda d: d[ANNEX]["identity"].__setitem__("public_name", "Nombre bloqueado"))
    def test_edad_fija(self):
        self.check_bad(lambda d: d[ANNEX]["identity"].__setitem__("age_at_academy_entry", 30))
    def test_sin_fecha_falsa(self):
        self.check_bad(lambda d: d[ANNEX]["identity"].__setitem__("exact_birth_date", "2338-02-01"))
    def test_no_regresar_genealogia_inventada(self):
        self.check_bad(lambda d: d[ANNEX]["lineage"].append({"generation": 1, "name": "Antepasado ficticio"}))
    def test_apellido_rise(self):
        self.check_bad(lambda d: d[ANNEX]["identity"].__setitem__("surname", "Vale"))
    def test_piano_unico(self):
        self.check_bad(lambda d: d[ANNEX]["skills"].__setitem__("music", ["cello"]))
    def test_no_recrear_maestros(self):
        self.check_bad(lambda d: d[ANNEX]["teachers"].append({"name": "Inventado"}))
    def test_nueve_capacidades(self):
        self.check_bad(lambda d: d[ANNEX].__setitem__("genetic_traits", ["strength"]))
    def test_libertad_del_jugador(self):
        self.check_bad(lambda d: d[ANNEX]["initial_personality"].__setitem__("player_choices_unrestricted", False))
    def test_padres_civiles(self):
        self.check_bad(lambda d: d[ANNEX]["identity"]["parentage"]["mother"].__setitem__("starfleet_service", True))
    def test_sin_invencion_suplantando_legacy(self):
        self.check_bad(lambda d: d[LEGACY_TECH].__setitem__("class_identity", "galaxy"))
    def test_no_suplantar_core(self):
        self.check_bad(lambda d: d[CATALOGUE].__setitem__("core_rpg_authority", "LORE"))
if __name__ == "__main__":
    unittest.main()
