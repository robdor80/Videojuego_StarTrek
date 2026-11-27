#ifndef TREK_HOST_INSTITUTIONAL_ABI_H
#define TREK_HOST_INSTITUTIONAL_ABI_H
#include "host_abi.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Read-only extension v1. Same client, lifetime, serialization, capacity and
 * discard as ABI v1. No observer, identity, permission or issuer input.
 * Poll is nonblocking and consumes only a matching ticket. Errors have zero
 * generation, epoch and facts. Revalidate immediately before displaying facts.
 * SAVE/RESTORE/CLOSE invalidate all previous epochs, including queued reads. */
#define TREK_HOST_INSTITUTIONAL_VERSION 1u
enum { TREK_HOST_CAREER = 1, TREK_HOST_PROMOTION = 2 };
typedef struct {
    uint32_t size, version, operation, reserved;
    uint64_t generation, correlation, event_id;
} TrekHostInstitutionalRequest;
typedef struct {
    uint32_t size;
    TrekHostCode code;
    uint32_t operation, reserved;
    uint64_t ticket, correlation, generation, epoch, world_revision;
    uint64_t event_id, effective_tick, original_revision;
    uint32_t rank, service_status, from_rank, to_rank;
} TrekHostInstitutionalCompletion;
TREK_HOST_ABI_API uint32_t TREK_HOST_ABI_CALL trek_host_institutional_version(void);
TREK_HOST_ABI_API TrekHostCode TREK_HOST_ABI_CALL trek_host_institutional_submit(
    TrekHostClient*, const TrekHostInstitutionalRequest*, uint64_t* ticket);
TREK_HOST_ABI_API TrekHostCode TREK_HOST_ABI_CALL trek_host_institutional_poll(
    TrekHostClient*, uint64_t ticket, TrekHostInstitutionalCompletion*);
/* OK = current, RETRY = busy (hide facts and retry), otherwise expired. */
TREK_HOST_ABI_API TrekHostCode TREK_HOST_ABI_CALL trek_host_institutional_current(
    TrekHostClient*, uint64_t generation, uint64_t epoch);
#ifdef __cplusplus
}
#endif
#endif
