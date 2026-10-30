#pragma once
#include <stdint.h>

#if defined(_WIN32)
# if defined(F02_BRIDGE_BUILD)
#  define F02_API __declspec(dllexport)
# else
#  define F02_API __declspec(dllimport)
# endif
#else
# define F02_API __attribute__((visibility("default")))
#endif
#ifdef __cplusplus
extern "C" {
#endif

/* Trusted native Host API v1, NOT a Blueprint, network, AI, or sensor protocol.
 * Owner thread only, including destruction; caller must keep session alive.
 * All buffers belong to the caller. No STL, allocations, exceptions or Core
 * pointers cross this DLL boundary. IDs are diagnostic fixture IDs, not contacts.
 */
typedef struct F02Session F02Session;
typedef struct F02Ref { uint64_t scope; uint64_t id; } F02Ref;
typedef struct F02Handles { F02Ref subject; F02Ref room; } F02Handles;
enum { F02_OK=0, F02_ARGUMENT=1, F02_THREAD=2, F02_DENIED=3,
       F02_CORE_REJECTED=4, F02_SAVE_REJECTED=5, F02_CAPACITY=6,
       F02_INTERNAL=7, F02_VERSION=8 };
typedef struct F02ActionResult {
    uint32_t status;
    uint32_t core_rejection; /* Diagnostic only; Core enum is not this API's ABI. */
    uint64_t revision_before;
    uint64_t revision_after;
    uint64_t rolled;
} F02ActionResult;
typedef struct F02Fact {
    uint64_t subject;
    uint64_t reference;
    uint32_t kind;
    uint32_t present;
} F02Fact;

F02_API uint32_t f02_abi_version(void);
F02_API const char* f02_core_sha(void); /* immutable DLL-owned static literal */
F02_API uint32_t f02_create(uint32_t abi, uint64_t seed, F02Session** out);
F02_API uint32_t f02_destroy(F02Session* session);
F02_API uint32_t f02_handles(F02Session*, F02Handles* out);
F02_API uint32_t f02_contains(F02Session*, F02Ref, uint32_t* out);
F02_API uint32_t f02_revision(F02Session*, uint64_t* out); /* trusted diagnostic */
F02_API uint32_t f02_place(F02Session*, F02Ref, F02Ref room,
                          uint64_t expected_revision, F02ActionResult* out);
F02_API uint32_t f02_roll(F02Session*, F02Ref, uint64_t minimum, uint64_t maximum,
                         uint64_t expected_revision, F02ActionResult* out);
F02_API uint32_t f02_set_permission(F02Session*, uint32_t allowed);
/* Fixed authenticated observer from the fixture; no caller-supplied grants.
 * context_only selects the subject's facts via the real ContextBuilder. */
F02_API uint32_t f02_view(F02Session*, uint32_t context_only,
                         F02Fact* out, uint64_t capacity, uint64_t* count);
/* Query size using null/zero, then copy. No persistence/file writes on size failure. */
F02_API uint32_t f02_save(F02Session*, uint8_t* out, uint64_t capacity, uint64_t* size);
F02_API uint32_t f02_load(F02Session*, const uint8_t* bytes, uint64_t size);

#ifdef __cplusplus
}
#endif
