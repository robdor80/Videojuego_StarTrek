#pragma once
#include "f06_bis.h"
#ifdef __cplusplus
extern "C" {
#endif
/* F06 AUTO — autonomous computer supervisor. Ship equipment profile >= 2
 * permits routine self-directed sensor analysis. The computer observes only
 * previously DETECTED contacts; it cannot create world entities or infer
 * a concealed signature, planet class or transponder.
 *
 * Auto jobs live in the same Core campaign and are persisted by F04 save/load.
 * Computer-owned observations have no PERSON relation. The automatic policy
 * cannot issue command orders, create scientific conclusions or assign watts.
 */
enum F06ComputerEventKind {
 F06_COMPUTER_CONTACT=1,
 F06_COMPUTER_LOSS=2,
 F06_COMPUTER_REACQUIRED=3,
 F06_COMPUTER_IDENTIFIED=4,
 F06_COMPUTER_ANALYSIS_STARTED=5,
 F06_COMPUTER_ANALYSIS_DONE=6,
 F06_COMPUTER_ANALYSIS_UNAVAILABLE=7
};
typedef struct {
 uint64_t tick;
 uint32_t autonomous,passive_operational,active_contacts;
 uint32_t analyses_running,analyses_completed,needs_attention,equipment_offline;
} F06ComputerStatus;
typedef struct {
 uint64_t event_token,contact_id,tick;
 uint32_t kind;
} F06ComputerEvent;
F04_API uint32_t f06_computer_status(F04Session*,F04Ref observer,F06ComputerStatus*);
/* Exact attention subjects, returning only authorized observed public IDs. */
F04_API uint32_t f06_computer_attention_contacts_page(F04Session*,F04Ref observer,
 uint64_t offset,uint64_t* contact_ids,uint64_t capacity,
 uint64_t* written,uint64_t* total);
F04_API uint32_t f06_computer_events_page(F04Session*,F04Ref observer,
 uint64_t after_event_token,F06ComputerEvent*,uint64_t capacity,
 uint64_t* written,uint32_t* more);
#ifdef __cplusplus
}
#endif
