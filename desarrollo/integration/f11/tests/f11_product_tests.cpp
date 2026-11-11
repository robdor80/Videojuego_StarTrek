#include "f11_promotions.h"
#include "../../f05/tests/f05_test_support.h"
#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#else
#include <dlfcn.h>
#endif

// This executable links the PRODUCT bridge. It has no trial issuer, test
// revocation or failure injection symbols and cannot mint personnel authority.
int main(int argc,char** argv) {
 try {
  // Inspect the actual product module on both platforms, not merely an nm log.
#ifdef _WIN32
  const auto module=LoadLibraryA("TrekF04Bridge.dll");check(module!=nullptr,"load product DLL");
  for(const char* name:{"f11_test_create","f11_test_revoke","f11_test_fault"})
   check(GetProcAddress(module,name)==nullptr,"test issuer must not be exported by product DLL");
  check(GetProcAddress(module,"f11_commit_promotion")!=nullptr,"product promotion export");FreeLibrary(module);
#else
  Dl_info info{};check(dladdr(reinterpret_cast<void*>(&f11_commit_promotion),&info)!=0,"locate product module");
  void* module=dlopen(info.dli_fname,RTLD_NOW|RTLD_LOCAL);check(module!=nullptr,"load product module");
  for(const char* name:{"f11_test_create","f11_test_revoke","f11_test_fault"})
   check(dlsym(module,name)==nullptr,"test issuer must not be exported by product module");
  check(dlsym(module,"f11_commit_promotion")!=nullptr,"product promotion export");dlclose(module);
#endif
  check(argc==2,"persisted native Host fixture required");const std::string path=argv[1];Lab c;
  const auto before=read(path+"-before.f04"),after=read(path+"-after.f04");c.load(before);
  F11PersonnelView person{};eq(f11_personnel(c.s,c.h.ensign,&person),F04_OK,"product commissioned identity");
  U order=0,revision=0,key=0,event=0,commit_revision=0;
  std::ifstream in(path+".txt");in>>order>>revision>>key>>event>>commit_revision;check(bool(in),"Host receipt");
  const auto snapshot=decode(before);
  auto ref=[&](U kind){for(auto edge:snapshot.campaign.relations)if(edge.source.value()==order && edge.kind.value()==kind)return edge.target.value();return U(0);};
  F11PromotionRequest q{c.h.ensign,person.character,revision,key,ref(258),order,ref(263),person.commission,person.rank_event,0,ref(265),1101,1102};
  F11PromotionReceipt receipt{};eq(f11_commit_promotion(c.s,&q,&receipt),F04_OK,"product commit");
  check(c.save()==after && receipt.promotion_event_id==event && receipt.original_commit_revision==commit_revision,"product equals native Host persisted future");
  c.load(after);q.subject=c.h.ensign;eq(f11_commit_promotion(c.s,&q,&receipt),F04_OK,"product replay after load");
  check(c.save()==after && receipt.promotion_event_id==event,"product no duplicate");
  F11PromotionView view{};eq(f11_promotion(c.s,c.h.ensign,event,&view),F04_OK,"product historical projection");
  check(view.receipt.effective_at==0 && view.receipt.to_rank==1102 && view.visibility==F11_SUBJECT_AND_PERSONNEL,"product narrative fact");
  std::cout<<"PASS product commit/load/replay without test bootstrap symbols\n";return 0;
 }catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<'\n';return 1;}
}
