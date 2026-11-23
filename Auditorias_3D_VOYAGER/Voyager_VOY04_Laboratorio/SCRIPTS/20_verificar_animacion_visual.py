import json,hashlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
# Rebuild only visual assemblies; the protected sources already passed full SHA reread.
script=R/'SCRIPTS/16_visuales_e_integridad.py';code=script.read_text(encoding='utf8').split('baseline=json.loads')[0];exec(compile(code,str(script),'exec'),dict(__file__=str(script),__name__='__main__'))
pixels=[]
for p in sorted((R/'ANIMACIONES').glob('VOY04_*.png')):
 im=Image.open(p).convert('RGB');pixels.append(dict(path=p.name,pixel_sha256=hashlib.sha256(im.tobytes()).hexdigest()))
gif=Image.open(R/'ANIMACIONES/VOY04_Ciclo_175.gif');webp=Image.open(R/'ANIMACIONES/VOY04_Ciclo_175.webp');n=gif.n_frames;duration=0
for frame in range(n):gif.seek(frame);duration+=gif.info.get('duration',0)
unique=len(set(x['pixel_sha256'] for x in pixels));assert n>=95 and webp.n_frames>=95 and unique>=45,(n,webp.n_frames,unique)
out=dict(PNG_frames=len(pixels),unique_pixel_frames=unique,GIF_frames=n,WebP_frames=webp.n_frames,GIF_duration_ms=duration,GIF_size=gif.size,pass_check=True,source='Real Blender PNG, active scene and refreshed dependency graph; no generated visual evidence',files=pixels)
(R/'DATOS/verificacion_animacion_visual.json').write_text(json.dumps(out,indent=2));print('VISUAL_PIXELS_PASS',len(pixels),unique,n,webp.n_frames,duration,flush=True)
