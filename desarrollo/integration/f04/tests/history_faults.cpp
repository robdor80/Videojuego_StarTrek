#include "organization_lab.h"
#include <corerpg/history.hpp>
#include <filesystem>
#include <chrono>
#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#endif
constexpr U day=86400;
struct HistoryLab:Lab {
 std::string path;
 HistoryLab():Lab(true,130,"miranda",true,1){path=(std::filesystem::temp_directory_path()/("f04-history-faults-"+std::to_string(std::chrono::steady_clock::now().time_since_epoch().count()))).string();}
 void migrate(){const std::array<uint8_t,16> id{4,4};check(f04_history_migrate(s,path.c_str(),id.data(),16)==F04_OK,"migrate");}
 auto active(){U n=0;check(f04_history_export_active(s,nullptr,0,&n)==F04_CAPACITY,"active size");std::vector<uint8_t> b(n);check(f04_history_export_active(s,b.data(),n,&n)==F04_OK,"active");return b;}
 auto history(){F04HistoryStats x{};check(f04_history_stats(s,&x)==F04_OK,"history stats");return x;}
 void recover(){check(f04_history_open(s,path.c_str())==F04_OK,"recover");refresh();}
 void plan(U start,U days){auto st=stats();op(F04_PLAN_WATCHES,0,start==0?1:0,start*day,(start+days)*day,F04_ROTATING,F04_OK,st.commander);}
};
int main(){try{
 HistoryLab l;const auto legacy=l.save();l.migrate();check(l.active()==legacy,"migration preserves exact original bytes");
 check(f04_load(l.s,legacy.data(),legacy.size())==F04_SAVE && l.active()==legacy,"cannot silently leave history mode and reset issued identities through legacy load");
 l.plan(0,14);l.advance(14*day-1);check(f04_history_publish(l.s,0)==F04_OK,"publish real pre-archive campaign");auto original=l.active();const auto initial=l.history();
 for(uint32_t fault=1;fault<=5;++fault){check(f04_history_consolidate(l.s,7*day-1,fault)==F04_SAVE,"injected failure");check(l.active()==original && l.history().generation==initial.generation,"prepublish failure keeps complete live state and root");l.recover();check(l.active()==original,"prepublish recovery same generation");}
#ifdef _WIN32
 // Real OS storage failure after preparation: allow reading CURRENT but deny
 // DELETE sharing, making its write-through atomic replacement fail.
 auto current=std::filesystem::path(l.path)/L"CURRENT";HANDLE held=CreateFileW(current.c_str(),GENERIC_READ,FILE_SHARE_READ,nullptr,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,nullptr);
 check(held!=INVALID_HANDLE_VALUE,"hold publication pointer");auto failed=f04_history_publish(l.s,0);CloseHandle(held);check(failed==F04_SAVE,"actual atomic replacement storage failure");l.recover();check(l.active()==original && l.history().generation==initial.generation,"actual storage failure preserves complete generation");
#endif
 // A torn uncommitted object is ignored by recovery, and cannot later be
 // mistaken for a valid prepared segment on retry.
 std::filesystem::path orphan;for(const auto& entry:std::filesystem::directory_iterator(l.path)){if(entry.path().extension()!=".obj")continue;std::ifstream f(entry.path(),std::ios::binary);char magic[8]{};f.read(magic,8);if(std::string(magic,8)=="CRPGSEG1"){orphan=entry.path();break;}}
 check(!orphan.empty(),"prepared orphan segment");auto orphan_bytes=read(orphan.string());auto torn=orphan_bytes;torn.resize(torn.size()/2);write(orphan.string(),torn);l.recover();check(l.active()==original,"torn uncommitted segment is not authority");check(f04_history_consolidate(l.s,7*day-1,0)==F04_SAVE && l.active()==original,"torn object cannot be published on retry");write(orphan.string(),orphan_bytes);
 check(f04_history_consolidate(l.s,7*day-1,6)==F04_SAVE,"loss after publication");F04Stats blocked{};check(f04_stats(l.s,&blocked)==F04_SAVE,"uncertain session requires recovery");l.recover();auto archived=l.history();check(archived.archived>0 && archived.generation==initial.generation+1,"new complete generation recovered");
 U n=0;check(f04_save(l.s,nullptr,0,&n)==F04_SAVE,"cannot export projection as full legacy save");
 F04HistoryFact facts[2]{};uint32_t more=0;check(f04_history_page(l.s,l.observer,initial.generation,0,facts,2,&n,&more)==F04_STALE && n==0,"stale historical cursor rejected");
 auto live=l.active();std::filesystem::path segment;
 for(const auto& entry:std::filesystem::directory_iterator(l.path)){if(entry.path().extension()!=".obj")continue;std::ifstream f(entry.path(),std::ios::binary);char magic[8]{};f.read(magic,8);if(std::string(magic,8)=="CRPGSEG1"){segment=entry.path();break;}}
 check(!segment.empty(),"actual immutable segment");auto bytes=read(segment.string());auto corrupt=bytes;corrupt[corrupt.size()/2]^=1;write(segment.string(),corrupt);
 check(f04_history_page(l.s,l.observer,archived.generation,0,facts,2,&n,&more)==F04_SAVE && n==0,"corruption is not empty history");
 check(f04_history_open(l.s,l.path.c_str())==F04_SAVE && l.active()==live,"failed recovery leaves previous session intact");write(segment.string(),bytes);l.recover();check(l.active()==live,"storage restored, original live state recovered");
 auto root_path=std::filesystem::path(l.path)/"CURRENT";auto root_bytes=read(root_path.string());auto truncated=root_bytes;truncated.resize(21);write(root_path.string(),truncated);check(f04_history_open(l.s,l.path.c_str())==F04_SAVE && l.active()==live,"incomplete publication root never mixes or silently rewinds generations");write(root_path.string(),root_bytes);l.recover();
 // Open debt remains operational after its old interval; no age-based erasure.
 HistoryLab debt;U person=0;for(auto p:debt.positions())if(p.person && !p.responsibility && p.department==F04_SENSORS){person=p.person;break;}check(person!=0,"existing debt person");
 U absent=0;for(auto p:debt.positions())if(p.person && p.person!=person && !p.responsibility && p.department==F04_SENSORS){absent=p.person;break;}check(absent!=0,"existing absence person");
 U rest=debt.op(F04_REST,person,0,0,day).record;debt.op(F04_RECALL,rest,0,0,0,43200);U absence=debt.op(F04_ABSENCE,absent,0,0,40*day,F04_SICK).record;
 debt.migrate();debt.plan(0,14);debt.advance(14*day-1);debt.plan(14,14);debt.advance(28*day-1);
 check(f04_history_consolidate(debt.s,21*day-1,0)==F04_OK,"retire closed facts with live debt");auto d=corerpg::CampaignPersistence::deserialize(debt.active());check(d.snapshot.has_value(),"debt checkpoint");bool retained=false,absence_retained=false;for(auto b:d.snapshot->campaign.definitions){retained|=b.entity.value()==rest;absence_retained|=b.entity.value()==absence;}check(retained && absence_retained,"outstanding debt and crossing absence not retired by age");
 debt.recover();debt.plan(28,7);auto after=corerpg::CampaignPersistence::deserialize(debt.active());
 for(auto def:after.snapshot->campaign.definitions)if(def.definition_id=="trek.f04:activity"){U p=0,kind=0,start=0;for(auto r:after.snapshot->campaign.relations)if(r.source==def.entity){if(r.kind.value()==2)p=r.target.value();if((r.kind.value()>>48)==0xf003)kind=r.kind.value()&forever;if((r.kind.value()>>48)==0xf001)start=r.kind.value()&forever;}check((p!=person && p!=absent) || kind!=F04_DUTY || start<28*day,"archived campaigns retain authoritative rest debt and absence in future planning");}
 HistoryLab revoked;revoked.migrate();revoked.plan(0,14);auto prepared=corerpg::CampaignPersistence::deserialize(revoked.active());U function=0;
 for(const auto& def:prepared.snapshot->campaign.definitions)if(def.definition_id=="trek.f04:function"){function=def.entity.value();break;}check(function!=0,"original real service function");
 revoked.op(F04_REVOKE,function,0,0,0,0,F04_OK,revoked.stats().commander);auto original_revoked=corerpg::CampaignPersistence::deserialize(revoked.active());std::vector<F04HistoryRelation> original_edges;
 for(auto edge:original_revoked.snapshot->campaign.relations)if(edge.source.value()==function)original_edges.push_back({edge.source.value(),edge.kind.value(),edge.target.value()});
 revoked.advance(14*day-1);revoked.plan(14,14);revoked.advance(28*day-1);check(f04_history_consolidate(revoked.s,21*day-1,0)==F04_OK,"archive explicitly revoked function");revoked.recover();
 auto revoked_state=revoked.history();F04HistoryRelation historical[256]{};U count=0,total=0;
 check(f04_history_relations(revoked.s,revoked.observer,revoked_state.generation,function,0,historical,256,&count,&total)==F04_OK && total==original_edges.size() && count==total,"query original revoked authority");
 for(U i=0;i<count;++i)check(historical[i].source==original_edges[i].source && historical[i].kind==original_edges[i].kind && historical[i].target==original_edges[i].target,"original revocation cannot be rewritten");
 auto operational=corerpg::CampaignPersistence::deserialize(revoked.active());for(auto def:operational.snapshot->campaign.definitions)check(def.entity.value()!=function,"historical revoked function never reactivated");revoked.plan(28,7);
 std::cout<<"F04 history faults, recovery, migration, cursor, full-save boundary, open debt/absence and revoked history PASS\n";return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
