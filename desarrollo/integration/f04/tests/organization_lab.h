#pragma once
#include "f04_bridge.h"
#include <corerpg/campaign_persistence.hpp>
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using U=uint64_t;
constexpr U forever=(1ULL<<48)-1;
void check(bool b,const char* m){if(!b)throw std::runtime_error(m);}
struct Lab {
 F04Session* s=nullptr;F04Ref observer{};
 Lab(bool seed=true,U crew=130,const char* cls="miranda",bool install=true,uint32_t profile=F04_SUTHERLAND_SCIENCE) {
  F04PopulationConfig cfg{65001,404,crew,0,0,0};check(f04_create_population(1,cls,&cfg,&s)==F04_OK,"population");refresh();
  if(install){F04TemplateSpec spec{};check(f04_template_spec(profile,&spec)==F04_OK,"profile");op(F04_INSTALL_TEMPLATE,0,spec.required_equipment,0,0,profile);if(seed)op(F04_BOOTSTRAP_TEMPLATE);}
 }
 ~Lab(){f04_destroy(s);}
 void refresh(){F04Handles h{};check(f04_handles(s,&h)==F04_OK,"handles");observer={h.ship.scope,3};}
 F04Stats stats(){F04Stats x{};check(f04_stats(s,&x)==F04_OK,"stats");return x;}
 F04OrganizationStats org(){F04OrganizationStats x{};check(f04_organization_stats(s,observer,&x)==F04_OK,"organization stats");return x;}
 F04Result op(uint32_t kind,U target=0,U aux=0,U start=0,U end=0,uint32_t value=0,uint32_t expected=F04_OK,U actor=3) {
  F04Request q{{observer.scope,actor},stats().revision,kind,value,target,aux,start,end,40401};F04Result result{};
  auto code=f04_execute(s,&q,&result);if(code!=expected)std::cerr<<"op="<<kind<<" actor="<<actor<<" got="<<code<<" expected="<<expected<<"\n";
  check(code==expected,"operation");return result;
 }
 std::vector<F04Position> positions(){std::vector<F04Position> result;U offset=0,total=0,n=0;
  do{F04Position page[23]{};check(f04_positions_page(s,observer,offset,page,23,&n,&total)==F04_OK,"positions page");result.insert(result.end(),page,page+n);offset+=n;}while(offset<total);return result;}
 F04Position post(U section,U ordinal=1){for(const auto& p:positions())if(p.section==section && p.ordinal==ordinal)return p;throw std::runtime_error("post");}
 F04Person person(U p){F04Person x{};check(f04_person(s,observer,p,&x)==F04_OK,"person");return x;}
 void advance(U tick){U n=0;check(f04_advance(s,tick,4096,&n)==F04_OK,"advance");}
 void alpha(){check(op(F04_PLAN_ALPHA,0,1,28800,57600).record==1,"Alpha recorded on ship");advance(28800);}
 std::vector<uint8_t> save(){U n=0;check(f04_save(s,nullptr,0,&n)==F04_CAPACITY,"size");std::vector<uint8_t>b(n);check(f04_save(s,b.data(),n,&n)==F04_OK,"save");return b;}
 void load(const std::vector<uint8_t>& b){check(f04_load(s,b.data(),b.size())==F04_OK,"load");refresh();}
 U credentials(U p){U mask=0,expiry=0;check(f04_person_credentials(s,observer,p,&mask,&expiry)==F04_OK,"credentials");return mask;}
 std::vector<F04FunctionView> functions(){U n=0;auto code=f04_functions(s,observer,nullptr,0,&n);check(code==(n?F04_CAPACITY:F04_OK),"function size");std::vector<F04FunctionView> f(n);check(f04_functions(s,observer,f.data(),n,&n)==F04_OK,"functions");return f;}
};
void write(const std::string& p,const std::vector<uint8_t>& b){std::ofstream f(p,std::ios::binary);f.write(reinterpret_cast<const char*>(b.data()),b.size());check(bool(f),"write");}
std::vector<uint8_t> read(const std::string& p){std::ifstream f(p,std::ios::binary);check(bool(f),"read");return {std::istreambuf_iterator<char>(f),{}};}
