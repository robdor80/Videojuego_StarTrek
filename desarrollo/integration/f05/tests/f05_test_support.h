#pragma once
#include "f05_orders.h"
#include <corerpg/campaign_persistence.hpp>
#include <corerpg/action.hpp>
#include <corerpg/content_catalog.hpp>
#include <algorithm>
#include <array>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <thread>
#include <vector>
using U=uint64_t;
using namespace corerpg;
void check(bool b,const char* msg){if(!b)throw std::runtime_error(msg);}
void eq(uint32_t got,uint32_t expected,const char* msg){if(got!=expected){std::cerr<<msg<<" got="<<got<<" expected="<<expected<<"\n";throw std::runtime_error(msg);}}
struct Lab {
 F04Session* s=nullptr;F04Handles h{};
 Lab(){eq(f04_create(1,"miranda",&s),F04_OK,"create");handles();}
 ~Lab(){if(s)f04_destroy(s);}
 void handles(){eq(f04_handles(s,&h),F04_OK,"handles");}
 F04Ref person(U id){return {h.ship.scope,id};}
 F04Stats stats(){F04Stats x{};eq(f04_stats(s,&x),F04_OK,"stats");return x;}
 F04Result op(F04Ref who,U kind,U target=0,U aux=0,U start=0,U end=0,U value=0){
  F04Request q{who,stats().revision,uint32_t(kind),uint32_t(value),target,aux,start,end,50501};
  F04Result r{};eq(f04_execute(s,&q,&r),F04_OK,"F04 fixture operation");return r;
 }
 void ready(){op(h.head,F04_ASSIGN,h.sensors,h.ensign.id);op(h.head,F04_DUTY,h.ensign.id,h.sensors,0,28800);op(h.ensign,F04_MOVE,h.sensors);}
 void advance(U t){U n=0;eq(f04_advance(s,t,4096,&n),F04_OK,"Core advance");}
 std::vector<uint8_t> save(){U n=0;eq(f04_save(s,nullptr,0,&n),F04_CAPACITY,"save size");std::vector<uint8_t>b(n);eq(f04_save(s,b.data(),n,&n),F04_OK,"save");return b;}
 std::vector<uint8_t> active(){U n=0;eq(f04_history_export_active(s,nullptr,0,&n),F04_CAPACITY,"active size");std::vector<uint8_t>b(n);eq(f04_history_export_active(s,b.data(),n,&n),F04_OK,"active checkpoint");return b;}
 void load(const std::vector<uint8_t>& b){eq(f04_load(s,b.data(),b.size()),F04_OK,"load");handles();}
 F05OrderRequest request(U key=1){return {h.captain,h.ensign,h.ship,{h.ship.scope,h.sensors},key,stats().revision,100,50501,F04_SCAN,0};}
 F05Receipt submit(const F05OrderRequest& q,uint32_t code=F04_OK){F05Receipt r{};eq(f05_submit(s,&q,&r),code,"submit");return r;}
 F05Receipt receive(U o,uint32_t code=F04_OK){F05Receipt r{};eq(f05_receive(s,h.ensign,stats().revision,o,&r),code,"receive");return r;}
 F05Receipt execute(U o,uint32_t code=F04_OK){F05Receipt r{};eq(f05_execute_order(s,h.ensign,stats().revision,o,&r),code,"execute");return r;}
 F05Receipt accepted(U key=1){return receive(submit(request(key)).order);}
 F05OrderView view(U o){F05OrderView v{};eq(f05_order(s,h.captain,o,&v),F04_OK,"order view");return v;}
 F05ResultView result(U o){F05ResultView v{};eq(f05_result(s,h.captain,o,&v),F04_OK,"result view");return v;}
 F05OrderRequest replay(U o){auto v=view(o);return {person(v.issuer),person(v.recipient),h.ship,person(v.station),v.key,v.input_revision,v.deadline,v.cause,v.operation,0};}
 std::vector<F05EventView> events(U o){std::vector<F05EventView> all;U after=0,n=0;uint32_t more=0;do{F05EventView e[2]{};eq(f05_events_page(s,h.captain,o,after,e,2,&n,&more),F04_OK,"event page");for(U i=0;i<n;++i){all.push_back(e[i]);after=e[i].id;}}while(more);return all;}
};
CampaignArchiveSnapshot decode(const std::vector<uint8_t>& b){auto d=CampaignPersistence::deserialize(b);check(d.snapshot.has_value(),"Core decode");return *d.snapshot;}
std::vector<uint8_t> encode(CampaignArchiveSnapshot d){++d.campaign.revision;std::sort(d.campaign.relations.begin(),d.campaign.relations.end());auto b=CampaignPersistence::serialize(d);check(b.status==CampaignArchiveStatus::success,"Core accepts candidate");return b.bytes;}
U field(const CampaignArchiveSnapshot& d,U id,U f){for(auto r:d.campaign.relations)if(r.source.value()==id && (r.kind.value()>>48)==0xF000+f)return r.kind.value()&((1ULL<<48)-1);throw std::runtime_error("field missing");}
U field_id(const CampaignArchiveSnapshot& d,U id,U value){for(auto r:d.campaign.relations)if(r.source.value()==id && r.target.value()==id && (r.kind.value()>>48)>=0xF000 && (r.kind.value()&((1ULL<<48)-1))==value)return (r.kind.value()>>48)-0xF000;throw std::runtime_error("field id missing");}
void change(CampaignArchiveSnapshot& d,U id,U f,U value){for(auto& r:d.campaign.relations)if(r.source.value()==id && (r.kind.value()>>48)==0xF000+f){r.kind=RelationKind{((0xF000+f)<<48)|value};return;}throw std::runtime_error("change missing");}
void write(const std::string& p,const std::vector<uint8_t>& b){std::ofstream f(p,std::ios::binary);f.write(reinterpret_cast<const char*>(b.data()),std::streamsize(b.size()));check(bool(f),"write fixture");}
std::vector<uint8_t> read(const std::string& p){std::ifstream f(p,std::ios::binary);check(bool(f),"read fixture");return {std::istreambuf_iterator<char>(f),{}};}
std::vector<U> orders(const CampaignArchiveSnapshot& d){std::vector<U> ids;for(const auto& x:d.campaign.definitions)if(x.definition_id=="trek.f04:f05_order")ids.push_back(x.entity.value());return ids;}
