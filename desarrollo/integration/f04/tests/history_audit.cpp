// Independent persisted-payload audit: reconstruct every seven-day original-fact
// delta from Core segments + active checkpoint and compare the complete-history
// oracle's canonical byte hash. Never reactivates or reschedules historical facts.
#include "organization_lab.h"
#include <corerpg/history.hpp>
#include <corerpg/content_catalog.hpp>
#include <filesystem>
using namespace corerpg;
std::string digest(const std::vector<uint8_t>& bytes){const char* d="0123456789abcdef";std::string s;for(auto b:HistoryPersistence::hash(bytes)){s+=d[b>>4];s+=d[b&15];}return s;}
auto catalog(){const auto p=*PackId::parse("trek.f04");const auto v=*SemanticVersion::parse("0.1.0");std::vector<ContentDefinitionInput> definitions;
 for(const char* name:{"population","person","slot","activity","appointment","delegation","event","task","order","mandate","review","department","section","function","roster_plan","roster_gap","auxiliary_defiant","class_miranda","class_intrepid","class_sovereign","class_odyssey","class_valhalla"})
  definitions.emplace_back(ResourceDefinition{*DefinitionId::parse(std::string("trek.f04:")+name),*ResourceKind::parse("structural")});
 return ContentCatalog::create({ContentPackInput{ContentManifest{p,v,v,v},std::move(definitions)}});
}
int main(int argc,char** argv){try{
 check(argc==2,"campaign directory required");const std::string path=argv[1];U profile=0,target=0,index=0,before=0;std::string future;std::ifstream metadata(path+".resume");check(bool(metadata>>profile>>target>>index>>before>>future),"metadata");
 const char* classes[]={"miranda","intrepid","sovereign","odyssey","valhalla"};const U crews[]={130,160,700,1600,1800};check(profile>=1 && profile<=5,"profile");
 Lab bootstrap(true,crews[profile-1],classes[profile-1],true,uint32_t(profile),profile==5?400:0);U previous=bootstrap.stats().entities;
 auto content=catalog();check(content.succeeded(),"independent generic catalog");HistoryArchive archive;WorldState world;RandomStreams random{0};Timeline time;
 check(HistoryPersistence::recover(std::filesystem::path(path),archive,world,random,time,content.catalog())==HistoryStatus::success,"verify every persisted segment, manifest, reduction, RNG and clock");
 const auto active=CampaignPersistence::capture(world,random,time);std::ifstream oracle(path+".oracle");check(bool(oracle),"oracle");U completed=0,verified=0,blocks=0;
 while(completed<target){U day=0,issued=0;std::string expected;check(bool(oracle>>day>>issued>>expected) && day<=target && issued>previous,"oracle block");
  auto delta=active;auto& c=delta.campaign;auto in_block=[&](EntityId id){return previous<id.value() && id.value()<=issued;};
  std::erase_if(c.definitions,[&](const auto& b){return !in_block(b.entity);});std::erase_if(c.relations,[&](const auto& b){return !in_block(b.source);});std::erase_if(c.containment,[&](const auto& b){return !in_block(b.entity);});
  c.populations.clear();c.population_memberships.clear();c.knowledge.clear();EntityId cursor{previous};bool done=false;
  while(!done){auto page=HistoryPersistence::query(archive,cursor,256);check(page.status==HistoryStatus::success,"read original historical page");
   for(const auto& fact:page.facts){if(fact.identity.entity.value()>issued){done=true;break;}check(in_block(fact.identity.entity),"ordered historical IDs");
    check(!fact.definition.empty() && fact.knowledge.empty(),"typed original F04 fact");c.definitions.emplace_back(fact.identity.entity,fact.definition);c.relations.insert(c.relations.end(),fact.relations.begin(),fact.relations.end());if(fact.container)c.containment.push_back({fact.identity.entity,*fact.container});}
   if(!page.more || page.facts.empty())done=true;cursor=page.next;
  }
  std::sort(c.definitions.begin(),c.definitions.end(),[](const auto& a,const auto& b){return a.entity<b.entity;});std::sort(c.relations.begin(),c.relations.end());std::sort(c.containment.begin(),c.containment.end(),[](auto a,auto b){return a.entity<b.entity;});
  check(c.definitions.size()==issued-previous,"every original emitted fact accounted for, without duplication");
  c.last_entity_id=issued;c.revision=issued+c.definitions.size()+c.relations.size()+c.containment.size();delta.timeline.now=day*86400-1;delta.timeline.records.clear();
  const auto bytes=CampaignPersistence::serialize(delta);check(bytes.status==CampaignArchiveStatus::success,"canonical original block");
  if(digest(bytes.bytes)!=expected)std::cerr<<"payload mismatch at day "<<day<<'\n';check(digest(bytes.bytes)==expected,"all original archived facts equal complete-history oracle, including causal links and original fields");
  verified+=issued-previous;previous=issued;completed=day;++blocks;
 }
 check(previous==before && previous==world.entity_count(),"audit reaches final published watermark");
 std::cout<<"{\"kind\":\"persisted_payload_audit\",\"profile\":"<<profile<<",\"days\":"<<target<<",\"blocks\":"<<blocks<<",\"original_facts_verified\":"<<verified<<",\"archived\":"<<archive.archived_count()<<",\"all_original_block_hashes_equal\":true}\n";return 0;
}catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<'\n';return 1;}}
