import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {resolve,dirname} from "node:path";
const root=resolve(dirname(fileURLToPath(import.meta.url)),"..");
const read=name=>readFileSync(resolve(root,name),"utf8");
test("LCARS shell exposes functional tabs, filters and command actions",()=>{
  const html=read("index.html");
  for(const tab of ["sensores","analisis","contactos","sectores","registros"])
    assert.match(html,new RegExp('data-tab="'+tab+'"'));
  for(const mode of ["general","largo","detalle","anomalias"])
    assert.match(html,new RegExp('data-mode="'+mode+'"'));
  for(const group of ["ships","objects","celestial","energy"])
    assert.match(html,new RegExp('data-group="'+group+'"'));
  for(const control of ["track-btn","center-btn","analyze-btn","focus-btn"])
    assert.match(html,new RegExp('id="'+control+'"'));
  const app=read("app.mjs");
  for(const action of ['issue("tracking")','issue("focus")','centerMap',
    'tab="analisis"','applyObserverSnapshot','applyVerifiedModelFrame'])
    assert.ok(app.includes(action),action);
});
test("panoramic console has no CDN or decorative fake 3D asset",()=>{
  const html=read("index.html"),app=read("app.mjs"),css=read("style.css");
  assert.doesNotMatch(html,/https?:\/\/|<iframe|<img[^>]+src=/i);
  assert.doesNotMatch(app,/fetch\(|WebSocket\(|eval\(|innerHTML\s*=/);
  assert.match(css,/grid-template-rows/);
  assert.match(css,/min-width:0/);
  assert.match(app,/SIN MODELO/);
});
test("UI contains no privileged F06 host write API",()=>{
  const app=read("app.mjs"),core=read("core.mjs");
  for(const fn of ["f06_host_signal","f06_host_world_snapshot","f06_host_environment",
    "f06_host_apply_power","f06_host_complete_science"])
    assert.ok(!app.includes(fn)&&!core.includes(fn),fn);
});
