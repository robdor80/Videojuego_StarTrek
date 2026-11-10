import {CATEGORY_NAMES,normalizeSnapshot,acceptSnapshot,visibleContacts,
  visibleRadius,projectPoint,canIssue,makeIntent,groupForCategory} from "./core.mjs";
import {DEMO} from "./demo.mjs";

const $=id=>document.getElementById(id);
const create=(tag,cls,text)=>{
  const node=document.createElement(tag);
  if(cls)node.className=cls;
  if(text!==undefined)node.textContent=String(text);
  return node;
};
let current=normalizeSnapshot(DEMO);
let selectedId="C-001";
let tab="sensores",mode="general",sector="all",search="",centered=false;
let groupSet=new Set(["ships","objects","celestial","energy"]);
let localHistory=[],message="Banco de pruebas: ningún dato procede de CoreRPG.";
let commandHandler=null,previewFrame=null,pending=false;
const colors={ships:"#69d8ff",objects:"#ffbf75",celestial:"#6ee9a6",energy:"#fa93d1"};
const glyphs={ships:"◇",objects:"✦",celestial:"●",energy:"◆"};
const tabNames={sensores:"VISTA ESPACIAL",analisis:"ANÁLISIS DE OBSERVACIONES",
  contactos:"CONTACTOS DETECTADOS",sectores:"SECTORES DE OBSERVACIÓN",
  registros:"REGISTROS DE SENSORES"};
const kindNames={new:"NUEVO CONTACTO",lost:"CONTACTO PERDIDO",
  reacquired:"READQUIRIDO",identified:"IDENTIFICADO",warning:"AVISO",request:"SOLICITUD"};

function showMessage(text) {
  message=String(text);
  $("notice-line").textContent=message;
}
function getSelected(){return current.contacts.find(c=>c.id===selectedId)||null;}
function filtered(){return visibleContacts(current,groupSet,{anomalies:mode==="anomalias",sector,search});}
function select(id) {
  if(!current.contacts.some(c=>c.id===id))return;
  selectedId=id;
  previewFrame=null;
  render();
}
function activeRange(list) {
  const base=visibleRadius(list.length?list:current.contacts);
  return mode==="largo"?base*2:mode==="detalle"?Math.max(50,base*.5):base;
}
function infoRow(parent,key,val){
  parent.append(create("span","key",key),create("span","value",val));
}
function renderInfo(){
  const c=getSelected(),dest=$("contact-info");
  dest.replaceChildren();
  $("contact-title").textContent=c?"CONTACTO "+c.id:"CONTACTO SELECCIONADO";
  $("contact-state").textContent=c?(c.status==="active"?"ACTIVO":"PERDIDO"):"—";
  if(!c){
    infoRow(dest,"Estado","Sin selección");
  } else {
    infoRow(dest,"Categoría",CATEGORY_NAMES[c.observed_category]);
    infoRow(dest,"Distancia",(c.distance_milli_au/1000).toFixed(3)+" UA");
    infoRow(dest,"Confianza",(c.confidence_permille/10).toFixed(1)+" %");
    infoRow(dest,"Clase",c.class_id?(c.class_label||"ID "+c.class_id):"No identificada");
    infoRow(dest,"Transpondedor",c.transponder_id||"No resuelto");
    infoRow(dest,"Seguimiento",["Pasivo","Normal","Prioritario"][c.tracking_mode]);
    infoRow(dest,"Última lectura","Tick "+c.last_seen);
  }
  const slot=$("model-slot");
  slot.replaceChildren();
  $("preview-state").textContent=c?.model?"RECURSO VERIFICADO":"SIN MODELO";
  if(!c){
    slot.textContent="Selecciona un contacto en el radar o en CONTACTOS.";
  }else if(!c.model){
    slot.textContent="Sin modelo 3D verificado para este contacto. No se sustituye por una nave ficticia.";
  }else if(previewFrame && previewFrame.asset_id===c.model.asset_id){
    const img=create("img");
    img.alt="Fotograma del modelo 3D verificado "+c.model.asset_id;
    img.src=previewFrame.data_url;
    img.style.cssText="width:100%;height:100%;object-fit:contain;";
    slot.append(img);
  }else{
    slot.textContent="Modelo "+c.model.asset_id+" certificado. Esperando fotogramas del visor UE5 ("+c.model.render_slot+").";
  }
  $("track-btn").textContent=c && c.tracking_mode?"DEJAR SEGUIR":"SEGUIR";
  $("track-btn").disabled=pending||!canIssue(current,"tracking",c);
  $("focus-btn").disabled=pending||!canIssue(current,"focus",c);
  $("center-btn").disabled=!c;
  $("analyze-btn").disabled=!c;
  $("center-btn").textContent=centered?"VOLVER A NAVE":"CENTRAR";
}
function renderRadar(){
  const layer=$("contact-layer"),map=$("map-view"),list=filtered();
  layer.replaceChildren();
  const center=centered&&getSelected()?getSelected().position_milli_au:[0,0,0];
  const range=activeRange(list);
  $("range-label").textContent="RADIO "+(range/1000).toFixed(2)+" UA · "+list.length+" VISIBLES";
  const origin=projectPoint([0,0,0],center,range);
  $("ship-marker").style.left=origin.x+"%";
  $("ship-marker").style.top=origin.y+"%";
  const rings=$("radar-rings");
  rings.style.left=origin.x+"%";rings.style.top=origin.y+"%";
  for(const c of list){
    const pos=projectPoint(c.position_milli_au,center,range);
    if(pos.x < -2||pos.x > 102||pos.y < -2||pos.y>102)continue;
    const kind=groupForCategory(c.observed_category);
    const b=create("button","contact-dot"+(c.id===selectedId?" is-selected":"")+
      (c.status==="lost"?" is-lost":""));
    b.type="button";
    b.style.left=pos.x+"%";b.style.top=pos.y+"%";
    b.style.setProperty("--contact-color",colors[kind]);
    b.title=c.id+" · "+CATEGORY_NAMES[c.observed_category]+
      " · "+(c.distance_milli_au/1000).toFixed(3)+" UA";
    b.setAttribute("aria-label","Seleccionar "+b.title);
    b.append(create("span","glyph",glyphs[kind]),create("span",null,c.id));
    b.addEventListener("click",()=>select(c.id));
    layer.append(b);
  }
  $("map-legend").textContent="DETECTADOS "+list.length+" / "+current.contacts.length+
    " · "+(current.session.source==="DEMO"?"SIMULACIÓN":"OBSERVADOR CORE");
  map.hidden=false;$("other-view").hidden=true;
}
function makeListButton(label,secondary,callback,active=false){
  const b=create("button","list-item"+(active?" active":""));
  b.type="button";
  b.append(create("span",null,label),create("span","dim",secondary));
  b.addEventListener("click",callback);
  return b;
}
function renderOther(){
  $("map-view").hidden=true;
  const host=$("other-view");
  host.hidden=false;host.replaceChildren();
  const list=filtered();
  $("range-label").textContent=list.length+" CONTACTOS A LA VISTA";
  if(tab==="contactos"){
    const input=create("input","search-bar");
    input.type="search";input.placeholder="Buscar por ID, categoría o clase observada";
    input.setAttribute("aria-label","Buscar contactos");
    input.value=search;
    input.addEventListener("input",()=>{
      const start=input.selectionStart||0;
      search=input.value;
      renderOther();
      const again=host.querySelector("input");
      if(again){again.focus();again.setSelectionRange(start,start);}
    });
    host.append(input);
    const grid=create("div","list-grid");
    for(const c of list){
      grid.append(makeListButton(c.id+" · "+CATEGORY_NAMES[c.observed_category],
        (c.distance_milli_au/1000).toFixed(3)+" UA",
        ()=>select(c.id),c.id===selectedId));
    }
    host.append(grid);
    if(!list.length)host.append(create("p","view-note","Ningún contacto cumple los filtros."));
  }else if(tab==="sectores"){
    host.append(create("p","view-note","Cuadrantes según posiciones observadas, respecto a nuestra nave."));
    const controls=create("div","sector-buttons");
    for(const [key,label] of [["all","TODOS"],["a","NE (+,+)"],["b","NO (-,+)"],
      ["c","SO (-,-)"],["d","SE (+,-)"]]){
      const b=create("button",sector===key?"selected":"",label);
      b.type="button";
      b.addEventListener("click",()=>{sector=key;render();});
      controls.append(b);
    }
    host.append(controls);
    host.append(create("p","view-note","Selección: "+(sector==="all"?"todos los sectores":sector.toUpperCase())+
      " · "+list.length+" contactos visibles. El filtro afecta también al radar."));
    const back=create("button","list-item","VER EN RADAR");
    back.addEventListener("click",()=>{tab="sensores";render();});
    host.append(back);
  }else if(tab==="analisis"){
    const c=getSelected();
    if(!c){
      host.append(create("p","view-note","Selecciona primero un contacto."));
      return;
    }
    host.append(create("p","view-note","Resultados focales registrados para "+c.id+
      " (solo observaciones autorizadas)."));
    const results=current.results.filter(r=>r.contact_id===c.id)
      .sort((a,b)=>b.tick-a.tick);
    if(!results.length)host.append(create("p","view-note",
      "Aún no existen observaciones focales. IDENTIFICAR puede solicitar un barrido, pero no inventa resultados."));
    const grid=create("div","list-grid");
    for(const r of results)
      grid.append(makeListButton("TICK "+r.tick+" · "+(r.confidence_permille/10).toFixed(1)+" %",
        (r.distance_milli_au/1000).toFixed(3)+" UA",()=>showMessage("Resultado "+r.id+" observado en Core.")));
    host.append(grid);
    if(results.length>=2){
      const a=results[0],b=results[1];
      host.append(create("p","view-note","Variación de confianza: "+
        ((a.confidence_permille-b.confidence_permille)/10).toFixed(1)+" puntos; distancia: "+
        ((a.distance_milli_au-b.distance_milli_au)/1000).toFixed(3)+" UA."));
    }
    if(canIssue(current,"science",c)){
      const button=create("button","list-item","SOLICITAR ESTUDIO A CIENCIA");
      button.addEventListener("click",()=>issue("science"));
      host.append(button);
    }
  }else if(tab==="registros"){
    host.append(create("p","view-note","Avisos observados y peticiones de esta sesión. No equivalen a verdad mundial."));
    const grid=create("div","list-grid");
    for(const n of [...localHistory,...current.notices].sort((a,b)=>b.tick-a.tick)){
      grid.append(makeListButton(kindNames[n.kind]||"AVISO",
        "TICK "+n.tick+" · "+(n.contact_id||"SISTEMA"),
        ()=>{if(n.contact_id)select(n.contact_id);}));
    }
    host.append(grid);
    if(!grid.childElementCount)host.append(create("p","view-note","No hay registros."));
  }
}
function render(){
  $("ship-name").textContent=current.session.ship_label;
  $("station-name").textContent=current.session.station_label;
  $("view-label").textContent=tabNames[tab];
  $("source-tag").textContent=current.session.source==="DEMO"?"DEMOSTRACIÓN":"CORE F06";
  $("connection-status").textContent=current.session.sensors_online?"SENSORES EN LÍNEA":"SENSORES FUERA DE SERVICIO";
  $("connection-status").style.color=current.session.sensors_online?"#55e5b5":"#ff8e91";
  $("tick-label").textContent="TICK "+current.session.tick+" · REV "+current.session.revision;
  $("notice-line").textContent=message;
  document.querySelectorAll("[data-tab]").forEach(b=>{
    const active=b.dataset.tab===tab;
    b.classList.toggle("active",active);
    b.setAttribute("aria-pressed",String(active));
  });
  document.querySelectorAll("[data-mode]").forEach(b=>{
    const active=b.dataset.mode===mode;
    b.classList.toggle("selected",active);
    b.setAttribute("aria-pressed",String(active));
  });
  renderInfo();
  if(tab==="sensores")renderRadar();else renderOther();
}
function applyObserverSnapshot(raw){
  try{
    const next=acceptSnapshot(current,raw);
    if(next===current){showMessage("Se ignoró una proyección Core obsoleta o degradada.");return false;}
    if(next.session.source!==current.session.source)localHistory=[];
    current=next;
    if(!getSelected())selectedId=current.contacts[0]?.id||null;
    centered=false;previewFrame=null;
    showMessage(current.session.source==="DEMO"?
      "Proyección sintética para probar botones, sin efectos en CoreRPG.":
      "Proyección autorizada recibida de CoreRPG. Acciones sujetas al servidor.");
    render();return true;
  }catch(error){showMessage("Proyección rechazada: "+error.message);return false;}
}
async function issue(command){
  const c=getSelected();
  if(!canIssue(current,command,c)){showMessage("Operación no disponible para este contacto.");return;}
  if(pending)return;
  const intent=makeIntent(current,command,c);
  pending=true;renderInfo();
  try{
    if(current.session.source==="DEMO"){
      localHistory.push({id:"local-"+(localHistory.length+1),kind:"request",
        contact_id:c.id,tick:current.session.tick});
      if(command==="tracking"){
        const updated={...DEMO,session:{...current.session,revision:current.session.revision+1},
          contacts:current.contacts.map(x=>({...x,tracking_mode:
            x.id===c.id?intent.mode:x.tracking_mode})),
          notices:current.notices,results:current.results};
        current=normalizeSnapshot(updated);
        showMessage("SIMULACIÓN: seguimiento "+(intent.mode?"activado":"desactivado")+
          ". No se ha modificado CoreRPG.");
      }else{
        showMessage("SIMULACIÓN: petición de "+(command==="focus"?"barrido focal":"estudio científico")+
          " registrada. No se ha fabricado ningún resultado.");
      }
    }else if(!commandHandler){
      showMessage("Sin enlace UE5/F06: no se ha enviado la orden.");
    }else{
      const result=await commandHandler(intent);
      if(!result || result.accepted!==true){
        showMessage("CoreRPG rechazó la orden: "+(result?.reason||"sin respuesta válida"));
      }else{
        showMessage("Orden recibida por F06; esperando nueva proyección autorizada.");
        if(result.snapshot)applyObserverSnapshot(result.snapshot);
      }
    }
  }catch(error){
    showMessage("No se completó la solicitud: "+(error?.message||"error"));
  }finally{pending=false;render();}
}
function selectNext(step){
  const contacts=filtered();
  if(!contacts.length)return;
  const index=contacts.findIndex(c=>c.id===selectedId);
  select(contacts[index<0?(step<0?contacts.length-1:0):(index+step+contacts.length)%contacts.length].id);
}
function centerMap(){
  if(!getSelected())return;
  centered=!centered;tab="sensores";render();
}
function showHelp(){
  if(typeof $("help-dialog").showModal==="function")$("help-dialog").showModal();
}
document.querySelectorAll("[data-tab]").forEach(b=>b.addEventListener("click",()=>{
  tab=b.dataset.tab;render();
}));
document.querySelectorAll("[data-mode]").forEach(b=>b.addEventListener("click",()=>{
  mode=b.dataset.mode;tab="sensores";centered=false;render();
}));
document.querySelectorAll("[data-group]").forEach(b=>b.addEventListener("change",()=>{
  if(b.checked)groupSet.add(b.dataset.group);else groupSet.delete(b.dataset.group);
  render();
}));
$("track-btn").addEventListener("click",()=>issue("tracking"));
$("focus-btn").addEventListener("click",()=>issue("focus"));
$("analyze-btn").addEventListener("click",()=>{tab="analisis";render();});
$("center-btn").addEventListener("click",centerMap);
$("ship-marker").addEventListener("click",()=>{centered=false;render();});
$("help-btn").addEventListener("click",showHelp);
$("close-help").addEventListener("click",()=>$("help-dialog").close());
document.addEventListener("keydown",event=>{
  if(event.altKey||event.ctrlKey||event.metaKey)return;
  const tag=event.target?.tagName;
  if(tag==="INPUT"||tag==="TEXTAREA"||$("help-dialog").open)return;
  const key=event.key.toLowerCase();
  const tabs=["sensores","analisis","contactos","sectores","registros"];
  if(/^[1-5]$/.test(key)){tab=tabs[Number(key)-1];render();}
  else if(key==="arrowright"){event.preventDefault();selectNext(1);}
  else if(key==="arrowleft"){event.preventDefault();selectNext(-1);}
  else if(key==="c")centerMap();
  else if(key==="t")issue("tracking");
  else if(key==="f")issue("focus");
  else if(key==="a"){tab="analisis";render();}
  else if(key==="escape"){tab="sensores";render();}
  else if(key==="?")showHelp();
});
window.F07Console=Object.freeze({
  applyObserverSnapshot,
  setCommandHandler(fn){
    if(fn!==null&&typeof fn!=="function")throw new TypeError("Command handler must be a function");
    commandHandler=fn;
  },
  /* A trusted UE renderer may push an actual SceneCapture frame for a
   * separately verified model. Without BOTH evidence and frame: placeholder. */
  applyVerifiedModelFrame(frame){
    const selected=getSelected();
    if(!selected?.model || !frame || frame.asset_id!==selected.model.asset_id ||
      typeof frame.data_url!=="string" || frame.data_url.length>2500000 ||
      !/^data:image\/(png|jpeg);base64,[A-Za-z0-9+/=]+$/.test(frame.data_url))
      return false;
    previewFrame={asset_id:frame.asset_id,data_url:frame.data_url};
    renderInfo();return true;
  },
  getStatus(){return Object.freeze({source:current.session.source,
    revision:current.session.revision,selected_contact_id:selectedId});}
});
render();
