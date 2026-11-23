#pragma once
#include "f06_equipment.h"
#include <array>
#include <vector>
// Controlled QA generation, not F13. Equipment exists before observation.
// Numerical equipment counts are fictional balance fixtures, never canon.
struct AsterX1Unit {
 F06WorldEntity world;
 F06PhysicalInput physical;
 uint64_t arrival;
};
inline std::vector<AsterX1Unit> aster_x1_units(uint64_t seed,uint64_t tick) {
 uint64_t random=seed;
 auto draw=[&](){random=random*6364136223846793005ULL+1442695040888963407ULL;return random>>32;};
 std::vector<AsterX1Unit> units;
 for(unsigned i=0;i<6;++i){
  AsterX1Unit u{};
  u.arrival=std::array<uint64_t,6>{0,60,150,240,360,0}[i];
  u.world.world_entity_key=910001+i;
  u.world.absolute_x_milli_au=i==5?40000:1000+static_cast<int>(draw()%500)+i*200;
  u.world.absolute_y_milli_au=100+static_cast<int>(draw()%150);
  u.world.class_id=(i==2?8:i==3?0:18);
  u.world.transponder_id=i<2?71001+i:0;
  u.world.strength_permille=950;u.world.signature_category=F06_CATEGORY_STARSHIP;
  u.world.active=tick>=u.arrival;
  auto& p=u.physical;p.version=1;p.world_entity_key=u.world.world_entity_key;
  p.length_m=i==2?1040:i==3?400+draw()%200:220;
  p.source_revision=1;p.cloaked=i==4 && tick<390;
  const std::array<unsigned,6> baseline=i==2?std::array<unsigned,6>{8,3,2,1,1,2}:
    i==3?std::array<unsigned,6>{6+static_cast<unsigned>(draw()%3),2,2,1,1,2}:
          std::array<unsigned,6>{0,0,1,1,1,2};
  for(unsigned k=0;k<6;++k){p.count[k]=baseline[k];p.state[k]=baseline[k]?1:0;p.visibility_permille[k]=1000;}
  // A real configuration change, independent of contact/public IDs.
  if(i==1 && tick>=210){p.count[0]=1;p.state[0]=2;p.source_revision=2;}
  if(i==2 && tick>=300){p.state[0]=3;p.source_revision=2;}
  if(i==3){p.visibility_permille[3]=0;} // unobservable internal armour stays secret
  if(i==4 && tick>=390){p.source_revision=2;p.cloaked=0;}
  units.push_back(u);
 }
 return units;
}
