#include "f05_ai_provider.h"
#include <jsoncons/json.hpp>
#include <jsoncons/json_cursor.hpp>
#include <set>
#include <vector>
#include <limits>
#include <stdexcept>
namespace trek::ai {
using json=jsoncons::json;
namespace {
void require(bool b){if(!b)throw std::runtime_error("invalid proposal");}
void keys(const json& j,std::initializer_list<const char*> names) {
 require(j.is_object() && j.size()==names.size());for(auto n:names)require(j.contains(n));
}
uint64_t number(const json& j) {
 require(j.is_uint64());auto n=j.as<uint64_t>();require(n>0 && n< (1ULL<<48));return n;
}
std::string text(const json& j,size_t max) {
 require(j.is_string());auto s=j.as<std::string>();require(!s.empty() && s.size()<=max);
 for(unsigned char c:s)require(c>=32 && c!=127);return s;
}
}
bool parse(const char* data,size_t size,Proposal& out) noexcept {
 out={};try {
  require(data && size && size<=8192);std::string raw(data,size);
  // Reject duplicate keys before the DOM can discard them. Bound nesting, even
  // for otherwise invalid schemas. jsoncons validates UTF-8/escapes/numbers.
  jsoncons::json_options options;options.max_nesting_depth(8);
  jsoncons::json_string_cursor cursor(raw,options);std::vector<std::set<std::string>> stack;
  while(!cursor.done()) {
   const auto& e=cursor.current();
   if(e.event_type()==jsoncons::staj_event_type::begin_object){stack.emplace_back();require(stack.size()<=8);}
   if(e.event_type()==jsoncons::staj_event_type::key){require(!stack.empty());require(stack.back().insert(e.get<std::string>()).second);}
   if(e.event_type()==jsoncons::staj_event_type::end_object){require(!stack.empty());stack.pop_back();}
   cursor.next();
  }
  const auto j=json::parse(raw,options);
  keys(j,{"version","actor","request","projection","revision","issued_at","expires","intent","actions","needs_clarification","insufficient_data","explanation","trace"});
  Proposal p;p.version=number(j.at("version"));require(p.version==1);
  p.actor=number(j.at("actor"));p.request=number(j.at("request"));p.projection=number(j.at("projection"));p.revision=number(j.at("revision"));
  // Core tick zero is legitimate.
  require(j.at("issued_at").is_uint64());p.issued=j.at("issued_at").as<uint64_t>();require(p.issued<(1ULL<<48));p.expires=number(j.at("expires"));
  auto intent=text(j.at("intent"),24);
  if(intent=="scan")p.intent=F05_AI_SCAN;else if(intent=="advise")p.intent=F05_AI_ADVISE;
  else if(intent=="clarify")p.intent=F05_AI_ASK;else if(intent=="insufficient")p.intent=F05_AI_UNKNOWN;else require(false);
  require(j.at("needs_clarification").is_bool() && j.at("insufficient_data").is_bool());
  p.clarification=j.at("needs_clarification").as<bool>();p.insufficient=j.at("insufficient_data").as<bool>();require(!(p.clarification && p.insufficient));
  const auto& a=j.at("actions");require(a.is_array() && a.size()<=1);
  if(a.size()){const auto& action=a.at(0);keys(action,{"operation","parameters"});require(action.at("operation").is_string() && action.at("operation").as<std::string>()=="F04_SCAN");keys(action.at("parameters"),{});p.scan=true;}
  require(p.scan==(p.intent==F05_AI_SCAN));require(p.clarification==(p.intent==F05_AI_ASK));require(p.insufficient==(p.intent==F05_AI_UNKNOWN));
  p.explanation=text(j.at("explanation"),512);p.trace=text(j.at("trace"),64);
  for(unsigned char c:p.trace)require((c>='a' && c<='z') || (c>='A' && c<='Z') || (c>='0' && c<='9') || c=='-' || c=='_');
  out=std::move(p);return true;
 }catch(...){return false;}
}
} // namespace trek::ai
