#include "f11_host_reader.h"
#include "../../f05/tests/f05_test_support.h"
#include <string>

// The fixture is produced by f11.process_save in a DIFFERENT CTest process.
// This test links only the PRODUCT bridge. It never loads a test issuer.
int main(int argc,char** argv) {
  try {
    check(argc==3,"expected fixture prefix and scenario");
    const std::string prefix=argv[1],mode=argv[2];
    Lab lab;
    using namespace trek::f11_host;
    Career career_view{};
    Promotion promotion_view{};
    if(mode=="legacy") {
      const auto original=lab.save();
      eq(career(lab.s,lab.h.ensign,&career_view),F11_UNCOMMISSIONED,"legacy is not commissioned");
      check(career_view.local_person==0 && career_view.rank==0,"legacy output cleared");
      check(original==lab.save(),"legacy read must not mutate Core");
    } else if(mode=="after" || mode=="before" || mode=="access") {
      lab.load(read(prefix+(mode=="before"?"-before.f04":"-after.f04")));
      std::uint64_t order=0,revision=0,key=0,event=0,commit=0;
      std::ifstream receipt(prefix+".txt");
      receipt>>order>>revision>>key>>event>>commit;
      check(bool(receipt) && event!=0,"fixture must contain actual Core promotion");
      const auto original=lab.save();
      eq(career(lab.s,lab.h.ensign,&career_view),F04_OK,"read commissioned person via product");
      check(career_view.local_person==lab.h.ensign.id && career_view.commission!=0 &&
            career_view.character.reserved==0,"professional identity from Core");
      if(mode=="before") {
        check(career_view.rank==F11_ENSIGN,"rank before confirmed promotion");
        eq(promotion(lab.s,lab.h.ensign,event,&promotion_view),F04_ARGUMENT,
           "no future event projected before the commit");
        check(!promotion_view.promotion_event,"missing event output cleared");
      } else {
        check(career_view.rank==F11_LIEUTENANT_JUNIOR_GRADE &&
              career_view.rank_event==event,"grade and rank event after confirmed promotion");
        eq(promotion(lab.s,lab.h.ensign,event,&promotion_view),F04_OK,"read promotion through product");
        check(promotion_view.promotion_event==event &&
              promotion_view.original_revision==commit &&
              promotion_view.effective_tick==0 &&
              promotion_view.from_rank==F11_ENSIGN &&
              promotion_view.to_rank==F11_LIEUTENANT_JUNIOR_GRADE &&
              promotion_view.visibility==F11_SUBJECT_AND_PERSONNEL,
              "native Host must project exact authoritative facts");
        check(promotion_view.character.high48==career_view.character.high48 &&
              promotion_view.character.mid48==career_view.character.mid48 &&
              promotion_view.character.low32==career_view.character.low32,
              "event belongs to same permanent officer");
        if(mode=="access") {
          promotion_view={};
          eq(promotion(lab.s,lab.h.captain,event,&promotion_view),F04_DENIED,
             "no captain access to another person's event");
          check(!promotion_view.promotion_event,"denied output cleared");
          auto forged=lab.h.ensign;forged.scope++;
          eq(career(lab.s,forged,&career_view),F04_SCOPE,"stale F04 session scope denied");
          check(!career_view.local_person,"stale scope output cleared");
          eq(career(lab.s,lab.h.ensign,nullptr),F04_ARGUMENT,"null rank destination");
          eq(promotion(lab.s,lab.h.ensign,event,nullptr),F04_ARGUMENT,"null event destination");
        }
      }
      check(original==lab.save(),"read-only native adapter preserves Core byte for byte");
    } else throw std::runtime_error("invalid scenario");
    std::cout<<"PASS f11.host."<<mode<<" product projection without issuer\n";
    return 0;
  } catch(const std::exception& e) {
    std::cerr<<"FAIL: "<<e.what()<<"\n";
    return 1;
  }
}
