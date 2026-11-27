// HOST-only product composition: compile the unchanged bridge exactly once,
// then add native persistence/read APIs in the same private translation unit.
// Other F04/F05/F11 compositions retain their frozen historical sources.
#include "f04_host_persistence.h"
#include "f05_player_binding.h"

#if defined(F11_ENABLE_PROMOTIONS) || defined(F11_NATIVE_TEST_HOST)
#error "The HOST bridge only accepts its reviewed F11 read composition"
#endif
#ifdef F11_HOST_READ_ONLY
// Select the existing F11 vocabulary and archive validation in this unit.
// F11_HOST_READ_ONLY excludes the commit entry point and its write helpers.
#define F11_ENABLE_PROMOTIONS 1
#endif
#include "f04_bridge.cpp"
#include "f04_host_snapshot.inc"
#include "../../f05/src/f05_player_binding.inc"
