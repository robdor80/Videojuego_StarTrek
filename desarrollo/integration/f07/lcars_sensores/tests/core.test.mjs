import test from "node:test";
import assert from "node:assert/strict";
import {DEMO} from "../demo.mjs";
import {CATEGORY_NAMES,normalizeSnapshot,acceptSnapshot,groupForCategory,
  visibleContacts,visibleRadius,projectPoint,canIssue,makeIntent} from "../core.mjs";
const copy=()=>structuredClone(DEMO);
test("synthetic observer contract loads and is labelled DEMO",()=>{
  const s=normalizeSnapshot(copy());
  assert.equal(s.session.source,"DEMO");
  assert.equal(s.contacts.length,5);
  assert.equal(s.contacts[0].class_label,null);
});
test("rejects unexpected schema",()=>{
  const v=copy();v.schema="f06.host.truth";
  assert.throws(()=>normalizeSnapshot(v),/schema/);
});
test("rejects duplicate contacts",()=>{
  const v=copy();v.contacts[1].id=v.contacts[0].id;
  assert.throws(()=>normalizeSnapshot(v),/contact id/);
});
test("rejects non-finite observed positions",()=>{
  const v=copy();v.contacts[0].position_milli_au[1]=NaN;
  assert.throws(()=>normalizeSnapshot(v),/observed position/);
});
test("rejects contacts from future clock ticks",()=>{
  const v=copy();v.contacts[0].last_seen=99999999;
  assert.throws(()=>normalizeSnapshot(v),/contact tick/);
});
test("rejects out of range categories and confidence",()=>{
  const v=copy();v.contacts[0].observed_category=42;
  assert.throws(()=>normalizeSnapshot(v),/category/);
  v.contacts[0].observed_category=1;v.contacts[0].confidence_permille=1001;
  assert.throws(()=>normalizeSnapshot(v),/confidence/);
});
test("never copies private science truth, host metadata or world entity IDs",()=>{
  const v=copy();
  v.science_truth={species:"SECRET"};
  v.contacts[0].host_entity_id=441;
  v.contacts[0].science_truth={life:true};
  const s=normalizeSnapshot(v);
  assert.equal("science_truth" in s,false);
  assert.equal("host_entity_id" in s.contacts[0],false);
  assert.equal("science_truth" in s.contacts[0],false);
});
test("unverified asset can never reach 3D viewer",()=>{
  const v=copy();
  v.contacts[0].class_id=2;
  v.contacts[0].model={verified:false,asset_id:"sovereign",render_slot:"F07"};
  assert.equal(normalizeSnapshot(v).contacts[0].model,null);
  v.contacts[0].model.verified=true;
  assert.deepEqual(normalizeSnapshot(v).contacts[0].model,
    {asset_id:"sovereign",render_slot:"F07"});
});
test("no viewer without observed class, even verified asset",()=>{
  const v=copy();
  v.contacts[0].model={verified:true,asset_id:"sovereign",render_slot:"F07"};
  assert.equal(normalizeSnapshot(v).contacts[0].model,null);
});
test("rejects file paths in verified viewer metadata",()=>{
  const v=copy();v.contacts[0].class_id=1;
  v.contacts[0].model={verified:true,asset_id:"../../host_secret",render_slot:"F07"};
  assert.equal(normalizeSnapshot(v).contacts[0].model,null);
});
test("group mapping preserves all F06 observer categories",()=>{
  assert.equal(Object.keys(CATEGORY_NAMES).length,18);
  for(let i=0;i<18;i++)assert.ok(groupForCategory(i));
  assert.equal(groupForCategory(1),"ships");
  assert.equal(groupForCategory(13),"celestial");
  assert.equal(groupForCategory(11),"objects");
  assert.equal(groupForCategory(7),"energy");
});
test("UI filtering does not create contacts",()=>{
  const s=normalizeSnapshot(copy());
  const all=new Set(["ships","objects","celestial","energy"]);
  assert.equal(visibleContacts(s,all).length,5);
  assert.equal(visibleContacts(s,new Set(["ships"])).length,2);
  assert.equal(visibleContacts(s,all,{anomalies:true}).length,1);
  assert.equal(visibleContacts(s,all,{search:"c-002"}).length,1);
  assert.equal(visibleContacts(s,all,{sector:"b"}).length,1);
  assert.equal(s.contacts.length,5);
});
test("projection centers selected contact without altering data",()=>{
  const c=[100,-50,0];
  assert.deepEqual(projectPoint(c,c,200),{x:50,y:50});
  assert.deepEqual(projectPoint([0,0,0],[0,0,0],200),{x:50,y:50});
  assert.throws(()=>projectPoint(c,c,0),/projection/);
});
test("radius never zero and grows with observations",()=>{
  assert.ok(visibleRadius([])>0);
  assert.ok(visibleRadius(normalizeSnapshot(copy()).contacts)>=1000);
});
test("lost contacts cannot receive orders",()=>{
  const v=copy();v.contacts[0].status="lost";
  const s=normalizeSnapshot(v);
  assert.equal(canIssue(s,"focus",s.contacts[0]),false);
  assert.equal(canIssue(s,"tracking",s.contacts[0]),false);
  assert.throws(()=>makeIntent(s,"focus",s.contacts[0]),/unavailable/);
});
test("offline arrays cannot receive orders",()=>{
  const v=copy();v.session.sensors_online=false;
  const s=normalizeSnapshot(v);
  assert.equal(canIssue(s,"focus",s.contacts[0]),false);
});
test("capability gates do not infer rank permissions",()=>{
  const v=copy();v.capabilities={track:false,focus:false,science:false};
  const s=normalizeSnapshot(v);
  assert.equal(canIssue(s,"focus",s.contacts[0]),false);
  assert.equal(canIssue(s,"science",s.contacts[0]),false);
});
test("intents carry expected revision, never trusted authorization",()=>{
  const s=normalizeSnapshot(copy());
  const track=makeIntent(s,"tracking",s.contacts[0]);
  assert.deepEqual(track,{protocol:"f07.intent.v1",command:"tracking",
    contact_id:"C-001",expected_revision:1,mode:1});
  assert.equal("operator_is_authorized" in track,false);
  const focus=makeIntent(s,"focus",s.contacts[0]);
  assert.equal("source_world_entity_id" in focus,false);
});
test("no stale Core projection can roll back revision",()=>{
  const a=copy();a.session.source="CORE_F06";a.session.revision=10;
  const old=copy();old.session.source="CORE_F06";old.session.revision=9;
  const cur=normalizeSnapshot(a);
  assert.strictEqual(acceptSnapshot(cur,old),cur);
  old.session.revision=11;
  assert.equal(acceptSnapshot(cur,old).session.revision,11);
});
test("invalid data never spoofs confirmed labels",()=>{
  const v=copy();
  v.contacts[0].class_label="Galaxy";
  v.contacts[0].transponder_id="</script>";
  const s=normalizeSnapshot(v);
  assert.equal(s.contacts[0].class_label,null);
  assert.equal(s.contacts[0].transponder_id,null);
});
