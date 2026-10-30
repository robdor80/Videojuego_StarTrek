uint32_t f04_specialists_page(F04Session* s,F04Ref who,U offset,F04Specialist* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;need(val(w,1,TEMPLATE)==5);
  std::vector<U> people;std::map<U,U> sections;
  for(U slot:all(w,"slot"))if(U p=ref(w,slot,PERSON))sections[p]=val(w,ref(w,slot,SECTION),SECTION_KEY);
  for(U p:all(w,"person"))if(val(w,p,SERVICE_GROUP))people.push_back(p);
  *total=people.size();need(offset<=*total);*written=std::min(capacity,*total-offset);
  for(U i=0;i<*written;++i) {
   const U p=people[size_t(offset+i)],tick=s->c->time.now();
   out[i]={p,val(w,p,SERVICE_GROUP),sections[p],1,ref(w,p,OPERATING_SHIP),ref(w,p,SUPERIOR),
    uint32_t(available(w,p,tick)),uint32_t(available(w,p,tick) && scheduled(w,p,tick))};
  }return F04_OK;
 });
}
uint32_t f04_residents_page(F04Session* s,F04Ref who,U offset,F04Resident* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;need(val(w,1,TEMPLATE)==5);
  std::vector<U> people;for(U p:all(w,"person"))if(val(w,p,CIVIL_CATEGORY))people.push_back(p);
  *total=people.size();need(offset<=*total);*written=std::min(capacity,*total-offset);
  for(U i=0;i<*written;++i) {
   const U p=people[size_t(offset+i)],tick=s->c->time.now()%86400;
   const bool present=member(w,p) && !val(w,p,AWAY);
   out[i]={p,val(w,p,CIVIL_CATEGORY),val(w,p,RESIDENCE),val(w,p,AREA),ref(w,p,KIN),val(w,p,AGENDA_KIND),val(w,p,AGENDA_START),val(w,p,AGENDA_END),
    uint32_t(present),uint32_t(present && val(w,p,AGENDA_START)<=tick && tick<val(w,p,AGENDA_END))};
  }return F04_OK;
 });
}
uint32_t f04_auxiliary(F04Session* s,F04Ref who,F04Auxiliary* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;need(val(w,1,TEMPLATE)==5);
  const auto ships=all(w,"auxiliary_defiant");need(ships.size()==1,F04_REVIEW);
  *out={ships[0],1,val(w,ships[0],SHIP_ID),1,0};return F04_OK;
 });
}
