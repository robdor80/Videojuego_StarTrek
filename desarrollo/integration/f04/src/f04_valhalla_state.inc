// Additive Trek vocabulary in Core relations. No external roster/database.
void seed_valhalla(Campaign& c,const ContentCatalog&) {
 if(val(c.world,1,TEMPLATE)!=F04_VALHALLA_FLAGSHIP)return;
 const U auxiliary=all(c.world,"auxiliary_defiant").at(0);
 U marine_command=0;std::map<U,U> marine_leads;
 for(U slot:all(c.world,"slot"))if(U p=ref(c.world,slot,PERSON)) {
  const U section=val(c.world,ref(c.world,slot,SECTION),SECTION_KEY),group=trek_templates::valhalla_group(section);
  set(c,p,SERVICE_GROUP,group);link(c,p,OPERATING_SHIP,group==F04_DEFIANT_NAVAL?auxiliary:1);
  if(group==F04_ODIN_MARINE) {
   if(!marine_command)marine_command=p;
   if(!marine_leads.contains(section))marine_leads[section]=p;
   const U superior=p==marine_command?0:p==marine_leads[section]?marine_command:marine_leads[section];
   if(superior)link(c,p,SUPERIOR,superior);
  }
 }
 U ordinal=0,first_adult=0;
 for(U p:all(c.world,"person"))if(member(c.world,p) && val(c.world,p,CATEGORY)==2) {
  need(++ordinal<=400,F04_CAPACITY);
  const U category=ordinal<=130?1:ordinal<=220?2:ordinal<=285?3:ordinal<=335?4:ordinal<=370?5:6;
  set(c,p,CIVIL_CATEGORY,category);set(c,p,RESIDENCE,100000+ordinal);set(c,p,AREA,1);set(c,p,AWAY,0);
  // A two-hour, optional logical reservation, with individual offsets. Adults
  // in the family category get community time, never an assumed job.
  set(c,p,AGENDA_KIND,category);set(c,p,AGENDA_START,32400+(ordinal%4)*1800);set(c,p,AGENDA_END,39600+(ordinal%4)*1800);
  if(!first_adult)first_adult=p;
  if(category==2)link(c,p,KIN,first_adult); // Explicit synthetic household contact.
 }
}
bool valhalla_schema(const WorldState& w) {
 const auto auxiliary=all(w,"auxiliary_defiant");
 if(val(w,1,TEMPLATE)!=5)return auxiliary.empty();
 if(auxiliary.size()!=1)return false;
 const U ship=auxiliary[0];
 if(val(w,ship,SHIP_ID)!=ship || val(w,ship,STATE)!=ACTIVE || ref(w,ship,SHIP)!=1)return false;
 std::set<U> homes;std::array<U,7> counts{};
 for(U p:all(w,"person")) {
  const U group=val(w,p,SERVICE_GROUP),category=val(w,p,CIVIL_CATEGORY);
  if(group) {
   if(group>3 || val(w,p,CATEGORY)!=1 || ref(w,p,OPERATING_SHIP)!=(group==2?ship:1))return false;
   if(group==3 && (val(w,p,QUAL)&((1ULL<<41)-2)))return false;
   if(group==2 && (val(w,p,QUAL)&((1ULL<<36)-2)))return false;
   if(category || has(w,p,RESIDENCE) || ref(w,p,KIN))return false;
   std::set<U> chain{p};U leader=ref(w,p,SUPERIOR);
   while(leader) {
    if(group!=3 || !chain.insert(leader).second || !type(w,leader,"person") || val(w,leader,SERVICE_GROUP)!=3)return false;
    leader=ref(w,leader,SUPERIOR);
   }
  } else if(ref(w,p,OPERATING_SHIP) || ref(w,p,SUPERIOR))return false;
  if(category) {
   if(category>6 || val(w,p,CATEGORY)!=2 || val(w,p,QUAL) || val(w,p,DEPT) || val(w,p,RANK) ||
    !has(w,p,AWAY) || val(w,p,AWAY)>1 || val(w,p,AREA)!=1 || !has(w,p,RESIDENCE) || val(w,p,RESIDENCE)<=100000 ||
    !homes.insert(val(w,p,RESIDENCE)).second || val(w,p,AGENDA_KIND)!=category ||
    val(w,p,AGENDA_START)>=val(w,p,AGENDA_END) || val(w,p,AGENDA_END)>86400 ||
    val(w,p,AGENDA_END)-val(w,p,AGENDA_START)!=7200)return false;
   ++counts[category];
   const U kin=ref(w,p,KIN);
   if(kin && (!type(w,kin,"person") || kin==p || val(w,kin,CIVIL_CATEGORY)!=1))return false;
  } else if(has(w,p,RESIDENCE) || has(w,p,AWAY) || has(w,p,AREA) || has(w,p,AGENDA_KIND) || has(w,p,AGENDA_START) || has(w,p,AGENDA_END) || ref(w,p,KIN))return false;
 }
 constexpr U maximum[]={0,130,90,65,50,35,30};
 for(size_t i=1;i<counts.size();++i)if(counts[i]>maximum[i])return false;
 for(U slot:all(w,"slot"))if(U p=ref(w,slot,PERSON)) {
  if(val(w,1,SEEDED) && val(w,p,SERVICE_GROUP)!=trek_templates::valhalla_group(val(w,ref(w,slot,SECTION),SECTION_KEY)))return false;
 }
 for(U a:all(w,"appointment"))if(!primary_operator(w,ref(w,a,PERSON)) || val(w,ref(w,a,PERSON),CIVIL_CATEGORY))return false;
 for(U f:all(w,"function"))if(!primary_operator(w,ref(w,f,PERSON)))return false;
 for(U a:all(w,"activity"))if(val(w,ref(w,a,PERSON),CIVIL_CATEGORY))return false;
 return true;
}
