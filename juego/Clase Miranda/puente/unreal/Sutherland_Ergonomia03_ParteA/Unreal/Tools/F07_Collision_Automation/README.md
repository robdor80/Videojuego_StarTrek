# F07 Collision Automation

Proyecto local de pruebas Sutherland, UE 5.8.2. Alcance: colisiones; sin reimportar mallas ni modificar apariencia.

El informe principal y todas las evidencias están en `Saved/F07_Sutherland_Audit/Codex_Full_Bridge/`.

## Repetir comprobación desde disco

Con este proyecto cerrado en Unreal, desde PowerShell:

```powershell
& .\Tools\F07_Collision_Automation\run_editor.ps1 -Script verify_saved_ue.py
```

El wrapper evita escritura concurrente y usa la instalación UE 5.8. Abre una sesión oculta, ejecuta el script y sale normalmente. `verify_saved_ue.py` no regenera ni guarda assets. Produce 375 casos: 363 correctos y 12 fallos geométricos conocidos de los pasillos estrechos.

`apply_plan_ue.py` es simulación sin guardar por defecto. Solo guarda cuando existe `commit_plan.json` con SHA256 exacto de `collision_plan.json`. La autorización técnica de esta ejecución ya fue consumida y se conserva como `commit_plan.executed.json`; no existe un checkpoint activo.

`build_plan.py`, `analyze_geometry.py` y `measure_routes.py` usan NumPy/Pillow del runtime de trabajo. No ejecutarlos como si fueran scripts de UE. `audit_ue.py`, `export_geometry_ue.py`, los probes y el aplicador requieren el módulo `unreal` del editor.

## Recuperación

`rollback.ps1` comprueba hashes sin escribir. `rollback.ps1 -Apply` restaura solo los archivos entregados, con Unreal cerrado y siempre que no haya cambios posteriores. Consultar el manifiesto y conservar el backup completo.

## Límites

Hay pasos de 59,9–61,0 cm frente a cápsula de 70 cm. No se han cambiado muebles ni personaje. Las hojas de puertas aún comparten assets entre lados opuestos y requieren separación para futura animación. No se ha validado Play humano.
