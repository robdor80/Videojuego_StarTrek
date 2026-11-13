// Additive read-only HOST adapter. Included once in the HOST bridge composition.
uint32_t f05_player_binding(F04Session* s,F05PlayerBinding* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  const auto& w=s->c->world;const auto ids=all(w,"f05_player");need(ids.size()<=1,F04_SAVE);
  if(ids.empty())return F04_OK;
  const U id=ids[0],person=ref(w,id,PERSON);need(observer(s,{s->scope,person}),F04_SAVE);
  *out={{s->scope,person},id,val(w,id,F05_REVISION),val(w,id,TICK)};return F04_OK;
 });
}
