import json,sys,collections,numpy as np,csv
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import *;from geom import ray
def save(n,x):(R/'DATOS'/n).write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding='utf8')
seqs=json.loads((R/'DATOS/trayectorias.json').read_text());clearance=[]
for seq in seqs:
 cfg=seq['config'];e=Env().adapted(cfg['drop'],cfg['backshift']).rail(cfg['D']);console=e.tri[np.isin(e.names,['Object_129','Object_126','Object_127'])];body=seq['poses'][150]['body'];legs=[]
 for part in body['parts']:
  if part['name'].startswith(('MUSLO','PANTORRILLA','PIE')):legs.append(dict(part=part['name'],minimum_console_surface_gap_m=float(segment_tri(np.array(part['p']),np.array(part['q']),console).min()-part['r'])))
 clearance.append(dict(H=seq['H'],legs=legs))
save('holguras_piernas_consola.json',clearance)
bear=[]
for m in json.loads((R/'DATOS/inventario_medidas.json').read_text()):
 e=Env(m['id']);low=min(x['lo'][2] for x in m['pieces']);ix=np.where(~e.chair)[0];hit=ray(e.tri[ix],[0,0,low-e.P[2]+.002],[0,0,-1],1.2)
 bear.append(dict(id=m['id'],under_chair_bearing_object=str(e.names[ix[hit['triangle']]]) if hit else None,under_chair_bearing_z_m=float(hit['point'][2]+e.P[2]) if hit else None,floor_reference_z_m=m['floor_m'],note='Bearing under chair and floor reached by feet are separate measurements.'))
save('apoyos_bases.json',bear)
# Internal surface contact candidates: exact SAT inherited from VOY02, in separate Blender script if needed.
props=dict(definition='Proportional laboratory mannequin, neither population percentile nor biomechanics standard',H_m=[1.6,1.75,1.9],standing_hip=.53,ankle=.045,femur=.245,tibia=.245,shoulder_above_hip=.288,head_center_above_hip=.407,head_radius=.063,upper_arm=.186,forearm=.146,hand_length=.035,thigh_radius=.043,shin_radius=.029,foot_radius=.027,foot_axis_length=.105,pelvis_half_width=.055,trunk_capsule_radius=.055,maximum_total_standing_height_formula='.53H + .407H + .063H = H',rig='18 independent rigid bones with Armature modifier and weight=1 per body capsule; IK solved analytically; no skin deformation',limits='Ellipsoids, musculature, clothing and fingers omitted; capsule envelopes conservatively bound rendered surfaces; limbs fixed length in all keyframes')
save('proporciones_maniqui.json',props)
save('fuentes_contextuales.json',[dict(title='Roddenberry Archive: USS Voyager (2371)',url='https://roddenberry.x.io/2371-uss-voyager-ncc-74656/',consulted_date='2026-10-22',usage='Contextual identification: captain port, first officer starboard, conn forward, science port low, engineering starboard low, operations/tactical rear standing; mapping to model is an inference from forward -Y.'),dict(title='F07-CHAIR-01',path=str(R/'REFERENCIAS/SUTHERLAND_INFORME.md'),usage='Isolation, independent pieces, fixed base, local controls, intermediate samples, return, reload and UV verification. No transfer of the 0.30m stroke.')])
print('LEG_CLEARANCES',clearance,flush=True);print('BASE_BEARINGS',bear,flush=True)
