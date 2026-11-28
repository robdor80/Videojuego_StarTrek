#include "f06_equipment.h"
#include <array>
#include <cstring>
#include <iostream>
#include <stdexcept>
#include <vector>
using U=uint64_t;
void require(bool pass,const char* message){if(!pass)throw std::runtime_error(message);}
struct Fixture {
 F04Session* s=nullptr;F04Handles h{};U source=0;
 Fixture(){require(f04_create(1,"miranda",&s)==F04_OK,"create");require(f04_handles(s,&h)==F04_OK,"handles");
  F06ProfileInstall p{revision(),5,0};F06ProfileView v{};require(f06_host_install_profile(s,&p,&v)==F04_OK,"profile");}
 ~Fixture(){f04_destroy(s);}
 U revision(){F04Stats st{};require(f04_stats(s,&st)==F04_OK,"stats");return st.revision;}
 void world(bool active=true,U klass=8,U transponder=0,int x=1000){
  F04Stats st{};f04_stats(s,&st);
  F06WorldEntity e{123456,x,0,0,transponder,static_cast<unsigned>(klass),1,0,active?1u:0u,0,1};
  F06WorldSnapshot q{revision(),++source,st.now,0,0,0,1,&e};F06WorldReceipt r{};
  require(f06_host_world_snapshot(s,&q,&r)==F04_OK,"world");
 }
 F06PhysicalInput physical(){F06PhysicalInput p{};p.expected_revision=revision();p.world_entity_key=123456;p.source_revision=1;p.version=1;p.length_m=1000;
  const unsigned counts[6]={8,3,2,1,1,2};
  for(unsigned k=0;k<6;++k){p.count[k]=counts[k];p.state[k]=1;p.visibility_permille[k]=1000;}return p;}
 std::vector<F06EquipmentView> equipment(F04Ref who={}){
  if(!who.id)who=h.captain;
  std::array<F06EquipmentView,32> rows{};U n=0,total=0;
  require(f06_equipment_page(s,who,0,0,rows.data(),rows.size(),&n,&total)==F04_OK,"equipment query");
  require(n==total,"complete equipment");return {rows.begin(),rows.begin()+static_cast<long>(n)};
 }
 std::vector<uint8_t> save(){U n=0;require(f04_save(s,nullptr,0,&n)==F04_CAPACITY,"save size");std::vector<uint8_t>b(n);require(f04_save(s,b.data(),n,&n)==F04_OK,"save");return b;}
 void ready(){for(auto q:std::array<F04Request,3>{
   F04Request{h.head,0,F04_ASSIGN,0,h.sensors,h.ensign.id,0,0,42},
   F04Request{h.head,0,F04_DUTY,0,h.ensign.id,h.sensors,0,28800,42},
   F04Request{h.ensign,0,F04_MOVE,0,h.sensors,0,0,0,42}}){q.revision=revision();F04Result r{};require(f04_execute(s,&q,&r)==F04_OK,"operator setup");}}
};
int main(){try{
 Fixture f;f.world(false);auto p=f.physical();
 require(f06_host_physical(f.s,&p)==F04_OK,"physical preexists");require(f.equipment().empty(),"inactive truth must be secret");
 f.world();auto rows=f.equipment();require(rows.size()==1,"auto measure without human");
 const auto first=rows.back();require(first.class_id==8 && first.count[0]==8 && first.expected[0]==6 && first.comparison[0]==2,"independent catalog discrepancy");
 require(first.length_m==1000 && first.visible_mask==63,"useful first-cycle technical sheet");
 auto bytes=f.save();require(f06_host_physical(f.s,&p)==F04_STALE,"stale revision");require(bytes==f.save(),"stale atomicity");
 p.expected_revision=f.revision();require(f06_host_physical(f.s,&p)==F04_STALE,"stale source");
 p.source_revision=2;p.count[0]=65;require(f06_host_physical(f.s,&p)==F04_ARGUMENT,"malicious count");
 p.count[0]=8;p.version=9;require(f06_host_physical(f.s,&p)==F04_ARGUMENT,"unsupported version");
 p.version=1;p.world_entity_key=999;require(f06_host_physical(f.s,&p)==F04_SCOPE,"invented source");
 require(bytes==f.save(),"negative inputs cannot mutate");p.world_entity_key=123456;
 p.visibility_permille[3]=0;p.state[0]=3;require(f06_host_physical(f.s,&p)==F04_OK,"real update");
 rows=f.equipment();require(rows.size()==2 && rows.back().comparison[0]==3,"offensive emission red");
 require(!(rows.back().visible_mask&8) && !rows.back().count[3] && !rows.back().state[3],"hidden armour redacted");
 auto updated=f.save();f.world();require(f.equipment().size()==2,"no duplicated observation/notice");
 U n=0,total=0;F06EquipmentView out{};auto forged=f.h.captain;forged.id=999999;
 require(f06_equipment_page(f.s,forged,0,0,&out,1,&n,&total)==F04_DENIED && !n && !total,"forged observer");
 F06DeliveryView receipt{};F06DeliveryRequest d{f.revision(),51,first.contact_id,2,0};
 require(f06_deliver(f.s,f.h.captain,&d,&receipt)!=F04_OK,"captain not at sensors cannot send as officer");
 f.ready();d.expected_revision=0;require(f06_deliver(f.s,f.h.ensign,&d,&receipt)==F04_STALE,"stale delivery");
 d.expected_revision=f.revision();d.contact_id=999;require(f06_deliver(f.s,f.h.ensign,&d,&receipt)==F04_UNAVAILABLE,"invented public contact");
 d.contact_id=first.contact_id;require(f06_deliver(f.s,f.h.ensign,&d,&receipt)==F04_OK && receipt.observation_id==rows.back().observation_id,"delivery captured measured snapshot");
 const auto delivered=receipt;bytes=f.save();
 require(f06_deliver(f.s,f.h.ensign,&d,&receipt)==F04_OK && receipt.receipt_id==delivered.receipt_id && bytes==f.save(),"idempotent stale retry");
 d.recipient=3;require(f06_deliver(f.s,f.h.ensign,&d,&receipt)==F04_OVERLAP && bytes==f.save(),"conflicting request cannot mutate");
 Fixture other;require(f04_load(other.s,bytes.data(),bytes.size())==F04_OK,"other session restore");f04_handles(other.s,&other.h);
 require(other.equipment().size()==2 && other.equipment().back().observation_id==rows.back().observation_id,"persistent equipment identity");
 F06DeliveryView recovered{};require(f06_deliveries_page(other.s,other.h.captain,0,&recovered,1,&n,&total)==F04_OK && total==1 && recovered.receipt_id==delivered.receipt_id,"durable queue");
 // Unknown class has physical measurement, never a borrowed identity.
 Fixture unknown;unknown.world(false,0);auto u=unknown.physical();u.cloaked=1;require(f06_host_physical(unknown.s,&u)==F04_OK,"cloak source");unknown.world(true,0);
 require(unknown.equipment().empty(),"cloaked inventory invisible");
 F06ContactView contact{};require(f06_contacts_page(unknown.s,unknown.h.captain,0,0,&contact,1,&n,&total)==F04_OK && !total,"cloaked identity invisible");
 u.expected_revision=unknown.revision();u.source_revision=2;u.cloaked=0;
 require(f06_host_physical(unknown.s,&u)==F04_OK,"decloak");auto measured=unknown.equipment();
 require(measured.size()==1 && measured[0].class_id==0 && measured[0].catalog_version==0 && measured[0].count[0]==8 && measured[0].comparison[0]==0,"unknown physical armament without identity");
 // Explicit zero power blocks acquisition; restoration resumes autonomously.
 Fixture damaged;damaged.world(false);auto pd=damaged.physical();require(f06_host_physical(damaged.s,&pd)==F04_OK,"damage physical");
 F06ArrayInput a{damaged.revision(),1000,0,1000,1,1,1,0};F06ArrayView av{};require(f06_host_array_state(damaged.s,&a,&av)==F04_OK,"offline");damaged.world();require(damaged.equipment().empty(),"offline cannot measure");
 a.expected_revision=damaged.revision();a.power_permille=1000;require(f06_host_array_state(damaged.s,&a,&av)==F04_OK && damaged.equipment().size()==1,"autonomous recovery");
 std::cout<<"PASS physical equipment, knowledge, roles, replay, revisions, persistence, hardware\n";
 return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
