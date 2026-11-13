// HOST-only product composition: compile the unchanged bridge exactly once,
// then add native persistence/read APIs in the same private translation unit.
// Other F04/F05/F11 compositions retain their frozen historical sources.
#include "f04_host_persistence.h"
#include "f05_player_binding.h"
#include "f04_bridge.cpp"
#include "f04_host_snapshot.inc"
#include "../../f05/src/f05_player_binding.inc"
