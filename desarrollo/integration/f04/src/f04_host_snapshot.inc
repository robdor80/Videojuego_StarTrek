// Native product composition only. Core owns formats, hashes and validation.
uint32_t f04_history_identity(F04Session* s,uint8_t* out,U size) {
 if(!out || size!=16)return F04_ARGUMENT;std::memset(out,0,16);
 return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  need(s->c->history.has_value(),F04_SAVE);auto id=s->c->history->campaign_id();std::copy(id.begin(),id.end(),out);return F04_OK;
#else
  return F04_SAVE;
#endif
 });
}
uint32_t f04_history_snapshot(F04Session* s,const char* directory,const uint8_t* uuid,U size) {
 if(!directory || !uuid || size!=16)return F04_ARGUMENT;
 return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  namespace fs=std::filesystem;
  need(schema(*s->c),F04_SAVE);HistoryCampaignId id;std::copy_n(uuid,16,id.begin());
  const fs::path target{reinterpret_cast<const char8_t*>(directory)};HistoryArchive archive;
  if(!s->c->history) {
   need(HistoryPersistence::migrate(target,id,s->c->world,s->c->random,s->c->time,archive,{workload_rule()})==HistoryStatus::success,F04_SAVE);
  } else {
   need(s->c->history->campaign_id()==id,F04_SAVE);
   // Source is an admitted private HOST snapshot; reject links, nested files,
   // unexpected objects and excessive copies before Core reads the copied set.
   const auto source=s->c->history->directory();need(fs::create_directory(target),F04_SAVE);
   U total=0,count=0;
   for(const auto& entry:fs::directory_iterator(source)) {
    const auto name=entry.path().filename().string();
    need(!entry.is_symlink() && entry.is_regular_file() && fs::hard_link_count(entry.path())==1,F04_SAVE);
    if(name=="writer.lock" || name.find(".tmp-")!=std::string::npos)continue;
    need(name=="CURRENT" || (name.size()==68 && name.substr(64)==".obj" && name.substr(0,64).find_first_not_of("0123456789abcdef")==std::string::npos),F04_SAVE);
    auto bytes=entry.file_size();need(bytes<=64ULL*1024*1024 && ++count<=4096,F04_CAPACITY);total+=bytes;need(total<=512ULL*1024*1024,F04_CAPACITY);
    need(fs::copy_file(entry.path(),target/entry.path().filename(),fs::copy_options::none),F04_SAVE);
   }
   WorldState world;RandomStreams random{0};Timeline time;
   need(HistoryPersistence::recover(target,archive,world,random,time,s->content.catalog())==HistoryStatus::success,F04_SAVE);
   need(archive.campaign_id()==id,F04_SAVE);
   need(HistoryPersistence::publish(archive,s->c->world,s->c->random,s->c->time)==HistoryStatus::success,F04_SAVE);
  }
  // Verify the entire snapshot, including every original segment, before return.
  WorldState world;RandomStreams random{0};Timeline time;HistoryArchive verified;
  need(HistoryPersistence::recover(target,verified,world,random,time,s->content.catalog())==HistoryStatus::success,F04_SAVE);
  need(verified.campaign_id()==id,F04_SAVE);return F04_OK;
#else
  return F04_SAVE;
#endif
 });
}
