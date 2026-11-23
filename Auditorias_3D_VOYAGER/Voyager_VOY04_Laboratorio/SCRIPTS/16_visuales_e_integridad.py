import sys,json,hashlib,datetime
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from importlib import import_module
sha=import_module('00_aislar').sha
frames=[Image.open(p).convert('RGB') for p in sorted((R/'ANIMACIONES').glob('VOY04_*.png'))];assert len(frames)==101
gif=R/'ANIMACIONES/VOY04_Ciclo_175.gif';frames[0].save(gif,save_all=True,append_images=frames[1:],duration=[120 if j%2==0 else 130 for j in range(len(frames))],loop=0,optimize=False,disposal=2)
frames[0].save(R/'ANIMACIONES/VOY04_Ciclo_175.webp',save_all=True,append_images=frames[1:],duration=125,loop=0,lossless=True)
try:font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
except OSError:font=ImageFont.load_default()
def board(name,items,columns=2,w=720,h=540):
 rows=(len(items)+columns-1)//columns;out=Image.new('RGB',(columns*w,rows*(h+45)),(24,30,38));d=ImageDraw.Draw(out)
 for j,(path,label) in enumerate(items):
  im=Image.open(R/'CAPTURAS'/path).convert('RGB');im.thumbnail((w,h));x=(j%columns)*w;y=(j//columns)*(h+45);out.paste(im,(x+(w-im.width)//2,y+45+(h-im.height)//2));d.text((x+12,y+9),label,font=font,fill=(240,240,240))
 out.save(R/'CAPTURAS'/name)
board('LAMINA_ANTES_DESPUES.png',[(f'E_{state}_SECCION_{H:.2f}.png',f'{H:.2f} m | '+('Original: fallo conservado' if state=='ORIGINAL' else 'Adaptado: asiento y soporte')) for H in [1.6,1.75,1.9] for state in ['ORIGINAL','ADAPTADO']])
board('LAMINA_SECUENCIA.png',[(f'C_SECUENCIA_{f:03d}.png',f'{f:03d} | {label}') for f,label in [(1,'Referencia'),(31,'Retirada 40 cm'),(61,'Alineado'),(76,'Flexion'),(91,'Sentado'),(121,'Posicion de trabajo'),(151,'Manos en consola'),(211,'Retirada ocupada'),(241,'De pie'),(301,'Silla en referencia')]])
check=Image.open(gif);assert check.n_frames>=95,check.n_frames
print('ANIMATION',len(frames),'GIF_FRAMES',check.n_frames,'GIF_MB',round(gif.stat().st_size/1e6,2),flush=True)
baseline=json.loads((R/'DATOS/baseline.json').read_text());after=[];changed=[];missing=[]
for row in baseline['files']:
 p=Path(row['path'])
 if not p.is_file():missing.append(str(p));continue
 h=sha(p);st=p.stat();after.append(dict(path=str(p),sha256=h,bytes=st.st_size,mtime_ns=st.st_mtime_ns))
 if h!=row['sha256'] or st.st_size!=row['bytes'] or st.st_mtime_ns!=row['mtime_ns']:changed.append(dict(before=row,after=after[-1]))
old=set(x['path'] for x in baseline['files']);current=set(str(p) for root in baseline['roots'] for p in Path(root).rglob('*') if p.is_file());added=sorted(current-old)
integrity=dict(date='2026-10-22',time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),protected_count=len(baseline['files']),changed=changed,missing=missing,added=added,pass_check=not(changed or missing or added),roots=baseline['roots'],hashes_rechecked=True,files=after,scope_note='Full SHA256 and size/mtime comparison for protected VOY01/02/03, F07_Chair_AutoLab, Sutherland_ChairLab and original source files enumerated by baseline. CoreRPG/Valhalla/Unreal projects were not opened or written; no whole-disk hash baseline is claimed.')
(R/'DATOS/integridad_final.json').write_text(json.dumps(integrity,indent=2),encoding='utf8');print('INTEGRITY',len(after),'CHANGED',len(changed),'MISSING',len(missing),'ADDED',len(added),flush=True);assert integrity['pass_check']
