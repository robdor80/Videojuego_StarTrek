// Shapes for the same Core WorldState used by F04/F05.
namespace {
bool f06_shape(const WorldState& w,U id,std::set<U>& allowed,
 std::set<U>& required,std::set<U>& ar,std::set<U>& rr) {
 if(type(w,id,"f06_signal")) {
  allowed={F06_X,F06_Y,F06_Z,F06_STRENGTH,F06_INTERFERENCE,
   F06_CLASS,F06_TRANSPONDER,F06_ACTIVE_FLAG,F06_EXIT};
  required=allowed;ar={SHIP};rr=ar;return true;
 }
 if(type(w,id,"f06_contact")) {
  allowed={F06_FIRST,F06_LAST,F06_STATUS,F06_CONFIDENCE,F06_DISTANCE,
   F06_SEEN_CLASS,F06_SEEN_TRANSPONDER,F06_VISIBLE_X,F06_VISIBLE_Y,F06_VISIBLE_Z,F06_LOSS_REASON,F06_PUBLIC_ID};
  required=allowed;ar={SHIP,F06_SIGNAL_REF};rr=ar;return true;
 }
 return false;
}
bool f06_schema(const Campaign& c) {
 const auto& w=c.world;
 std::set<U> signals,public_ids;
 const auto source=all(w,"f06_signal");
 if(source.size()>2048 || all(w,"f06_contact").size()>2048)return false;
 for(U id:source) {
  if(val(w,id,F06_STRENGTH)>1000 || val(w,id,F06_INTERFERENCE)>550 ||
   val(w,id,F06_ACTIVE_FLAG)>1 || val(w,id,F06_EXIT)>F06_EXIT_OBSERVED_OUT_OF_RANGE)return false;
 }
 for(U id:all(w,"f06_contact")) {
  const U s=ref(w,id,F06_SIGNAL_REF);
  if(!type(w,s,"f06_signal") || !signals.insert(s).second ||
   !val(w,id,F06_PUBLIC_ID) || !public_ids.insert(val(w,id,F06_PUBLIC_ID)).second ||
   val(w,id,F06_FIRST)>val(w,id,F06_LAST) ||
   val(w,id,F06_LAST)>c.time.now() ||
   val(w,id,F06_STATUS)<F06_ACTIVE || val(w,id,F06_STATUS)>F06_LOST ||
   val(w,id,F06_CONFIDENCE)>1000 ||
   val(w,id,F06_LOSS_REASON)>F06_EXIT_OBSERVED_OUT_OF_RANGE ||
   val(w,id,F06_DISTANCE)>50000 ||
   false)return false; // classification remains historical even if the source changes
 }
 return true;
}
} // namespace
