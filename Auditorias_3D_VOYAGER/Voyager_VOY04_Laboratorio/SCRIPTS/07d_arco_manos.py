import json,sys,shutil,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for name in ['trayectorias','resultados_cinematica']:
 src=R/'DATOS'/f'{name}.json';dest=R/'DATOS'/f'{name}_A3_FALLO_MANOS.json';assert not dest.exists();shutil.copy2(src,dest)
runpy.run_path(str(R/'SCRIPTS/07c_contacto_controles.py'),run_name='__main__')
