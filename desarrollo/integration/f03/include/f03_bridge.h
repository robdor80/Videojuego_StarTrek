#pragma once
#include <stdint.h>
#if defined(_WIN32)
# if defined(F03_BRIDGE_BUILD)
#  define F03_API __declspec(dllexport)
# else
#  define F03_API __declspec(dllimport)
# endif
#else
# define F03_API __attribute__((visibility("default")))
#endif
#ifdef __cplusplus
extern "C" {
#endif
/* Trusted native Host ABI 1, not a network/Blueprint/AI/sensor protocol.
 * Owner thread only. Host authenticates the observer before selecting its ref.
 * No caller-supplied grants, world pointers, STL, exceptions or file IO.
 * IDs/stats/marker states are privileged laboratory diagnostics only.
 */
typedef struct F03Session F03Session;
typedef struct F03Ref { uint64_t scope,id; } F03Ref;
typedef struct F03Handles { F03Ref primary,secondary; } F03Handles;
enum { F03_OK=0,F03_ARGUMENT=1,F03_THREAD=2,F03_DENIED=3,F03_REJECTED=4,
       F03_SAVE_REJECTED=5,F03_CAPACITY=6,F03_INTERNAL=7,F03_VERSION=8,F03_MORE=9 };
typedef struct F03Stats { uint64_t entities,revision,tick,scheduled,finished; } F03Stats;
typedef struct F03Fact {
    uint64_t contact,reference_contact;
    uint32_t kind,present,classification,provenance;
} F03Fact;
typedef struct F03MarkerState { uint64_t identity; uint32_t location; uint32_t reserved; } F03MarkerState;
F03_API uint32_t f03_abi_version(void);
F03_API const char* f03_core_sha(void);
F03_API uint32_t f03_create(uint32_t abi,uint64_t seed,F03Session** out);
F03_API uint32_t f03_destroy(F03Session*);
F03_API uint32_t f03_handles(F03Session*,F03Handles*);
F03_API uint32_t f03_stats(F03Session*,F03Stats*);
F03_API uint32_t f03_set_permission(F03Session*,uint32_t allowed);
F03_API uint32_t f03_schedule_route(F03Session*);
F03_API uint32_t f03_advance(F03Session*,uint64_t horizon,uint64_t max_actions,uint64_t* processed);
/* channel 1: direct observation, secondary co-located with target at arrival.
 * channel 2: authorized formal report to primary, existence subset only. */
F03_API uint32_t f03_acquire(F03Session*,F03Ref observer,uint32_t channel);
F03_API uint32_t f03_view(F03Session*,F03Ref observer,uint32_t context_only,F03Fact*,uint64_t capacity,uint64_t* count);
F03_API uint32_t f03_marker_state(F03Session*,F03Ref,F03MarkerState*);
F03_API uint32_t f03_roll(F03Session*,F03Ref,uint64_t expected_revision,uint64_t* result);
F03_API uint32_t f03_save(F03Session*,uint8_t*,uint64_t capacity,uint64_t* size);
F03_API uint32_t f03_load(F03Session*,const uint8_t*,uint64_t size);
#ifdef __cplusplus
}
#endif
