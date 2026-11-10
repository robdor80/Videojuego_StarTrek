/* F07 presentation contract. No privileged Core/F06 calls in the browser. */
export const CATEGORY_NAMES = Object.freeze({
  0:"Sin clasificar",1:"Nave",2:"Lanzadera",3:"Sonda",4:"Ser vivo",
  5:"Artificial",6:"Energía",7:"Warp",8:"Subespacial",9:"Señal",
  10:"Partículas",11:"Anomalía",12:"Estrella",13:"Planeta",
  14:"Luna",15:"Nebulosa",16:"Estación",17:"Asteroide"
});
export const KIND_GROUPS = Object.freeze({
  ships:[1,2,3,16], objects:[0,4,5,9,10,11,17],
  celestial:[12,13,14,15], energy:[6,7,8]
});
const ALLOWED_NOTICES = new Set(["new","lost","reacquired","identified","warning","request"]);
function validInteger(value,min=0,max=Number.MAX_SAFE_INTEGER) {
  return Number.isSafeInteger(value) && value>=min && value<=max;
}
function validLabel(value,max=90) {
  return typeof value==="string" && value.length>0 && value.length<=max && !/[\u0000-\u001f<>]/.test(value);
}
function assert(ok,what) { if (!ok) throw new TypeError("F07 contrato inválido: "+what); }
function optionalLabel(value,max=90) { return value==null?null:(validLabel(value,max)?value:null); }
function validPoint(value) {
  return Array.isArray(value) && value.length===3 &&
    value.every(x=>validInteger(x,-1e9,1e9));
}
/* This is an observer projection. Whitelisting prevents host-only secrets,
 * model paths, science_truth, private IDs, and unknown metadata reaching UI. */
export function normalizeSnapshot(raw) {
  assert(raw && typeof raw==="object" && raw.schema==="f07.observer.v1","schema");
  const s=raw.session;
  assert(s && validLabel(s.ship_label) && validLabel(s.station_label)
    && validInteger(s.tick) && validInteger(s.revision)
    && (s.source==="DEMO" || s.source==="CORE_F06")
    && typeof s.sensors_online==="boolean","session");
  assert(Array.isArray(raw.contacts) && raw.contacts.length<=512,"contacts");
  const seen=new Set();
  const contacts=raw.contacts.map((c,i)=>{
    assert(c && validLabel(c.id,40) && !seen.has(c.id),"contact id "+i);
    seen.add(c.id);
    assert(c.status==="active"||c.status==="lost","contact status");
    assert(validPoint(c.position_milli_au),"observed position");
    assert(validInteger(c.distance_milli_au,0,1e9),"observed distance");
    assert(validInteger(c.confidence_permille,0,1000),"confidence");
    assert(validInteger(c.observed_category,0,17),"observed category");
    assert(validInteger(c.class_id,0,100000),"observed class");
    assert(validInteger(c.last_seen,0,s.tick),"contact tick");
    assert(c.tracking_mode===0||c.tracking_mode===1||c.tracking_mode===2,"tracking mode");
    // Do not show a class/identity supplied as unverified decoration.
    const classLabel=c.class_id>0?optionalLabel(c.class_label):null;
    const identity=c.transponder_id && validLabel(c.transponder_id,40)
      ?c.transponder_id:null;
    const m=c.model;
    const model=m && m.verified===true && c.class_id>0 &&
      validLabel(m.asset_id,100) && /^[a-zA-Z0-9_.-]+$/.test(m.asset_id)
      && validLabel(m.render_slot,64) && /^[a-zA-Z0-9_.-]+$/.test(m.render_slot)
      ?{asset_id:m.asset_id,render_slot:m.render_slot}:null;
    return Object.freeze({
      id:c.id,status:c.status,position_milli_au:[...c.position_milli_au],
      distance_milli_au:c.distance_milli_au,confidence_permille:c.confidence_permille,
      observed_category:c.observed_category,class_id:c.class_id,
      class_label:classLabel,transponder_id:identity,
      last_seen:c.last_seen,tracking_mode:c.tracking_mode,model
    });
  });
  const notices=Array.isArray(raw.notices)?raw.notices.slice(0,120).filter(n=>
    n && validLabel(n.id,40) && ALLOWED_NOTICES.has(n.kind) &&
    validInteger(n.tick,0,s.tick) && (!n.contact_id || seen.has(n.contact_id))
  ).map(n=>({id:n.id,kind:n.kind,tick:n.tick,contact_id:n.contact_id||null})):[];
  const results=Array.isArray(raw.results)?raw.results.slice(0,200).filter(x=>
    x && validLabel(x.id,40) && seen.has(x.contact_id) &&
    validInteger(x.tick,0,s.tick) && validInteger(x.confidence_permille,0,1000) &&
    validInteger(x.distance_milli_au,0,1e9)
  ).map(x=>({id:x.id,contact_id:x.contact_id,tick:x.tick,
    confidence_permille:x.confidence_permille,distance_milli_au:x.distance_milli_au})):[];
  return Object.freeze({
    schema:raw.schema,
    session:Object.freeze({
      ship_label:s.ship_label,station_label:s.station_label,tick:s.tick,
      revision:s.revision,source:s.source,sensors_online:s.sensors_online
    }),
    contacts,notices,results,
    capabilities:{
      track:raw.capabilities?.track===true,
      focus:raw.capabilities?.focus===true,
      science:raw.capabilities?.science===true
    }
  });
}
export function groupForCategory(category) {
  for (const [group,ids] of Object.entries(KIND_GROUPS))
    if(ids.includes(category)) return group;
  return "objects";
}
export function visibleContacts(snapshot,enabledGroups,{anomalies=false,sector="all",search=""}={}) {
  const needle=search.toLocaleLowerCase("es");
  return snapshot.contacts.filter(c=>{
    const point=c.position_milli_au;
    const inSector=sector==="all" ||
      (sector==="a" && point[0]>=0 && point[1]>=0) ||
      (sector==="b" && point[0]<0 && point[1]>=0) ||
      (sector==="c" && point[0]<0 && point[1]<0) ||
      (sector==="d" && point[0]>=0 && point[1]<0);
    return enabledGroups.has(groupForCategory(c.observed_category)) && inSector
      && (!anomalies || [6,8,11].includes(c.observed_category))
      && (!needle || (c.id+" "+CATEGORY_NAMES[c.observed_category]+" "+
           (c.class_label||"")).toLocaleLowerCase("es").includes(needle));
  }).sort((a,b)=>a.distance_milli_au-b.distance_milli_au || a.id.localeCompare(b.id));
}
/* Coordinates in milli-AU, not fake kilometres. Screen y is inverted. */
export function projectPoint(point,center,range) {
  assert(validPoint(point)&&validPoint(center)&&Number.isFinite(range)&&range>0,"projection");
  return {x:50+((point[0]-center[0])/range)*46,
          y:50-((point[1]-center[1])/range)*46};
}
export function visibleRadius(contacts) {
  const max=contacts.reduce((m,c)=>Math.max(m,Math.hypot(c.position_milli_au[0],
                                                   c.position_milli_au[1])),0);
  return Math.max(100,Math.ceil(max/200)*200);
}
export function canIssue(snapshot,command,contact) {
  if(!snapshot || !snapshot.session.sensors_online || !contact ||
     contact.status!=="active") return false;
  if(command==="tracking") return snapshot.capabilities.track;
  if(command==="focus") return snapshot.capabilities.focus;
  if(command==="science") return snapshot.capabilities.science;
  return false;
}
export function makeIntent(snapshot,command,contact) {
  assert(["tracking","focus","science"].includes(command),"intent command");
  assert(canIssue(snapshot,command,contact),"intent unavailable");
  const intent={protocol:"f07.intent.v1",command,contact_id:contact.id,
                expected_revision:snapshot.session.revision};
  if(command==="tracking") intent.mode=contact.tracking_mode?0:1;
  if(command==="science") intent.analysis_kind=1;
  return Object.freeze(intent);
}
export function acceptSnapshot(current,incoming) {
  const next=normalizeSnapshot(incoming);
  if(current && current.session.source==="CORE_F06" &&
    next.session.source==="CORE_F06" &&
    next.session.revision<current.session.revision) return current;
  return next;
}
