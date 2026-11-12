# P2-B05 · Fixture sintético (NO canon)

Este caso reproduce la reconstrucción de dos instalaciones tras daños ya resueltos por sus responsables. No materializa una guerra, un tratado, una fábrica, naves o población nuevos. Los hechos anteriores se proporcionan como **entradas aceptadas de prueba**, con una autoridad declarada dentro del fixture; no demuestran verificación en CoreRPG real.

Ejecutar:

```bash
python desarrollo/tools/generation/simulate_procedural_history.py --fixture desarrollo/validation/fixtures/procedural_history/procedural_history_reconstruction_v0.1.json
python -m unittest discover -s desarrollo/tools/generation -p 'test_simulate_procedural_history.py' -v
```

El caso produce un acontecimiento relevante y una rectificación posterior. Ninguno modifica inventario o soberanía. La noticia restringida requiere conocimiento explícito y autorización independiente.
