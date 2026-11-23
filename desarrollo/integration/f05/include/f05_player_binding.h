#pragma once
#include "f05_initiative.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Trusted native read only. Zero record/person means no persistent binding.
 * The immutable binding fact identifies continuity, beyond the numeric person ID. */
typedef struct { F04Ref person; uint64_t record,input_revision,tick; } F05PlayerBinding;
F04_API uint32_t f05_player_binding(F04Session*,F05PlayerBinding*);
#ifdef __cplusplus
}
#endif
