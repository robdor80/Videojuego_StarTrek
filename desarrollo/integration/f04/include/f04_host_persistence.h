#pragma once
#include "f04_bridge.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Additive native HOST composition. No mutation of the live campaign. New
 * destination only; preserves full original history through Core recover/publish. */
F04_API uint32_t f04_history_snapshot(F04Session*,const char* directory,const uint8_t* campaign_id,uint64_t size);
F04_API uint32_t f04_history_identity(F04Session*,uint8_t* campaign_id,uint64_t size);
#ifdef __cplusplus
}
#endif
