#pragma once
#include "f05_test_support.h"
#include "f05_initiative.h"
struct InitiativeLab:Lab {
 U next=10000,service=0;
 void bind(F04Ref p){eq(f05_bind_player(s,p,stats().revision),F04_OK,"bind authenticated player");}
 void prepare(F04Ref player={}) {
  op(h.head,F04_ASSIGN,h.sensors,h.ensign.id);
  service=op(h.head,F04_DUTY,h.ensign.id,h.sensors,0,28800).record;
  op(h.ensign,F04_MOVE,h.sensors);bind(player.id?player:h.doctor);
 }
 F05NeedView requirement(U due=0,U end=80) {
  F05ScanNeedRequest q{h.captain,service,next++,stats().revision,due,end,50301};F05NeedView n{};
  eq(f05_scan_need(s,&q,&n),F04_OK,"authorized actual service obligation");return n;
 }
 U brief(U n,F04Ref to) {
  U b=0;eq(f05_brief_need(s,h.captain,to,stats().revision,n,next++,50302,&b),F04_OK,"explicit formal report");return b;
 }
 U ready_need(F04Ref player={}){prepare(player);auto n=requirement();brief(n.id,h.captain);brief(n.id,h.ensign);return n.id;}
 F05Evaluation input(F04Ref actor,U n,U budget=32){return {actor,n,next++,stats().revision,uint32_t(budget),0};}
 F05DecisionView evaluate(const F05Evaluation& q,U code=F04_OK) {
  F05DecisionView d{};eq(f05_evaluate(s,&q,&d),uint32_t(code),"bounded initiative");return d;
 }
 F05DecisionView step(F04Ref actor,U n,U budget=32){return evaluate(input(actor,n,budget));}
 U issue(U n,F04Ref actor={}){auto d=step(actor.id?actor:h.captain,n);check(d.decision==F05_ISSUE_ORDER && d.order && d.detection,"need -> decision -> real P01 order");return d.order;}
 void finish(U n){check(step(h.ensign,n).decision==F05_CONTINUE_TASK,"NPC receive");check(step(h.ensign,n).decision==F05_CONTINUE_TASK,"NPC execute");}
 U grant(U mode=F05_DELEGATED_AUTONOMOUS,U end=80) {
  op(h.captain,F04_ASSIGN,h.bridge,h.watch.id);op(h.captain,F04_DUTY,h.watch.id,h.bridge,0,28800);
  F05DelegationRequest q{h.captain,h.watch,h.ship,person(h.sensors),h.ensign,next++,stats().revision,stats().now,end,50303,0,F04_SENSORS,F04_SCAN,uint32_t(mode),0};
  F05DelegationView d{};eq(f05_delegate(s,&q,&d),F04_OK,"P02 draft");change(d.id,F05_ACTIVE,mode);return d.id;
 }
 void change(U id,U state,U mode=F05_DELEGATED_AUTONOMOUS){F05DelegationChange q{h.captain,id,next++,stats().revision,50304,uint32_t(state),uint32_t(mode)};F05DelegationView d{};eq(f05_change_delegation(s,&q,&d),F04_OK,"P02 change");}
 std::vector<F05DecisionView> decisions(F04Ref who){std::vector<F05DecisionView> a;U after=0,n=0;uint32_t more=0;do{F05DecisionView d[2]{};eq(f05_decisions_page(s,who,after,d,2,&n,&more),F04_OK,"own decisions page");for(U i=0;i<n;++i){a.push_back(d[i]);after=d[i].id;}}while(more);return a;}
};
std::vector<U> kind_ids(const CampaignArchiveSnapshot& d,const std::string& kind){std::vector<U> a;for(const auto& x:d.campaign.definitions)if(x.definition_id=="trek.f04:"+kind)a.push_back(x.entity.value());return a;}
