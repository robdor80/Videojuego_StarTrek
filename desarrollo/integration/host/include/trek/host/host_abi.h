#ifndef TREK_HOST_ABI_H
#define TREK_HOST_ABI_H

#include <stdint.h>

#if defined(_WIN32)
# if defined(TREK_HOST_BUILD)
#  define TREK_HOST_ABI_API __declspec(dllexport)
# else
#  define TREK_HOST_ABI_API __declspec(dllimport)
# endif
# define TREK_HOST_ABI_CALL __cdecl
#else
# define TREK_HOST_ABI_API __attribute__((visibility("default")))
# define TREK_HOST_ABI_CALL
#endif

#ifdef __cplusplus
extern "C" {
#endif

/* ABI 1, default alignment, 64-bit targets. No allocator or C++ type crosses
 * this boundary. The client owns inputs and outputs. Inputs are copied before
 * return and output pointers are never retained. Use exact v1 struct sizes. */
#define TREK_HOST_ABI_VERSION 1u
#define TREK_HOST_ABI_MAX_PENDING 8u
#define TREK_HOST_ABI_MAX_ROOT_BYTES 16384u
#define TREK_HOST_ABI_CAMPAIGN_BYTES 32u

typedef struct TrekHostClient TrekHostClient;

typedef uint32_t TrekHostCode;
enum {
    TREK_HOST_OK = 0,
    TREK_HOST_INVALID_ARGUMENT = 1,
    TREK_HOST_SESSION_CLOSED = 2,
    TREK_HOST_BUSY_STATE = 3,
    TREK_HOST_WRONG_THREAD = 4,
    TREK_HOST_GENERATION_EXPIRED = 5,
    TREK_HOST_CAPACITY_LIMIT = 6,
    TREK_HOST_DOMAIN_REJECTED = 7,
    TREK_HOST_INTERNAL_ERROR = 8,
    TREK_HOST_PRINCIPAL_UNBOUND = 9,
    TREK_HOST_ACCESS_DENIED = 10,
    TREK_HOST_SCOPE_INVALID = 11,
    TREK_HOST_REVISION_STALE = 12,
    TREK_HOST_IDEMPOTENCY_CONFLICT = 13,
    TREK_HOST_SAVE_INCOMPATIBLE = 14,
    TREK_HOST_SAVE_UNTRUSTED = 15,
    TREK_HOST_PERSISTENCE_FAILED = 16,
    TREK_HOST_PUBLICATION_UNCERTAIN = 17,
    TREK_HOST_SAVE_CORRUPT = 18,
    TREK_HOST_IDENTITY_MISMATCH = 19,
    TREK_HOST_PATH_REJECTED = 20,
    TREK_HOST_SERVICE_UNAVAILABLE = 21,

    TREK_HOST_ABI_MISMATCH = 100,
    TREK_HOST_RETRY = 101, /* Contention. No request admitted or result consumed. */
    TREK_HOST_PENDING = 102,
    TREK_HOST_UNKNOWN_TICKET = 103
};

enum {
    TREK_HOST_CLOSED = 0, TREK_HOST_OPENING = 1, TREK_HOST_ACTIVE = 2,
    TREK_HOST_SAVING = 3, TREK_HOST_LOADING = 4, TREK_HOST_FAILED = 5,
    TREK_HOST_FAILED_RECOVERABLE = 6, TREK_HOST_CLOSING = 7
};

enum {
    TREK_HOST_OPEN = 1, TREK_HOST_CLOSE = 2, TREK_HOST_QUERY_VIEW = 3,
    TREK_HOST_SUBMIT_SCAN = 4, TREK_HOST_QUERY_ORDER = 5,
    TREK_HOST_CANCEL_ORDER = 6, TREK_HOST_SAVE = 7, TREK_HOST_RESTORE = 8
};

typedef struct {
    const char* data;
    uint32_t size; /* Bytes, without a terminator. NUL bytes are invalid. */
    uint32_t reserved;
} TrekHostText;

typedef struct {
    TrekHostText class_id; /* Existing campaign class, max 64 ASCII bytes. */
    uint64_t ship_identity, seed, crew, residents, passengers, maximum;
} TrekHostPopulation;

typedef struct {
    TrekHostText campaign; /* 32 lowercase hex bytes. */
    TrekHostText slot;     /* 1..32 bytes, validated by H04. */
    uint64_t version;      /* 0 selects newest committed version. */
} TrekHostSlot;

typedef struct {
    uint64_t recipient, station, key, expected_revision, deadline, cause;
} TrekHostScan;

typedef struct {
    uint64_t id, expected_revision; /* Revision only for CANCEL_ORDER. */
} TrekHostOrderRef;

typedef struct {
    uint32_t size;
    uint32_t operation;
    uint64_t generation; /* 0 for OPEN, CLOSE and RESTORE from CLOSED. */
    union {
        TrekHostPopulation population; /* OPEN */
        TrekHostText slot;              /* SAVE */
        TrekHostSlot restore;           /* RESTORE */
        TrekHostScan scan;              /* SUBMIT_SCAN */
        TrekHostOrderRef order;         /* QUERY_ORDER / CANCEL_ORDER */
    } input;
} TrekHostRequest;

typedef struct {
    uint32_t size;
    uint32_t state;
    uint64_t generation;
    TrekHostCode principal;     /* OK if bound; other codes describe the gate. */
    TrekHostCode institutional; /* SERVICE_UNAVAILABLE in v1. */
} TrekHostStatus;

typedef struct {
    uint64_t revision, tick, person, ship;
} TrekHostCampaignView;

enum {
    TREK_HOST_ISSUED = 1, TREK_HOST_ACCEPTED = 2, TREK_HOST_EXECUTING = 3,
    TREK_HOST_COMPLETED = 4, TREK_HOST_ORDER_FAILED = 5,
    TREK_HOST_REFUSED = 6, TREK_HOST_CANCELLED = 7
};

typedef struct {
    uint64_t order, key, revision, result, value;
    uint32_t state;
    uint32_t performed; /* 1 if Core performed the action; value is a roll. */
} TrekHostOrderView;

typedef struct {
    uint32_t size;
    TrekHostCode code; /* Domain outcome. No payload unless OK. */
    uint32_t operation;
    uint32_t reserved;
    uint64_t ticket;
    uint64_t generation; /* 0 for CLOSE and failures. */
    char campaign[TREK_HOST_ABI_CAMPAIGN_BYTES + 1]; /* OPEN / RESTORE only. */
    uint8_t padding[7];
    union {
        TrekHostCampaignView view;
        TrekHostOrderView order;
    } output;
} TrekHostCompletion;

TREK_HOST_ABI_API uint32_t TREK_HOST_ABI_CALL trek_host_abi_version(void);

/* Create once per game instance. The root is an existing, absolute, private
 * local directory from trusted application configuration, encoded as UTF-8.
 * A zero-length root disables persistence via the existing H04 policy.
 * Create starts a native worker; destroy joins it. Use a non-Game Thread
 * for teardown, retaining both DLLs until destroy returns. */
TREK_HOST_ABI_API TrekHostCode TREK_HOST_ABI_CALL trek_host_create(
    uint32_t version, const char* root, uint32_t root_size, TrekHostClient** out);
TREK_HOST_ABI_API void TREK_HOST_ABI_CALL trek_host_destroy(TrekHostClient* client);

/* Serialize calls on each live client and quiesce them before destroying it.
 * Status/submit/poll never wait for Core work or future completion. Set size
 * on every request and output. Output structs are valid only on transport OK.
 * Poll consumes the ticket once. Discard releases its observation slot without
 * cancelling native work. CLOSE has a reserved slot, invalidates the native
 * generation on admission, and can be submitted even if all 8 slots are full.
 * After delivery, callers still revalidate generation before applying a result. */
TREK_HOST_ABI_API TrekHostCode TREK_HOST_ABI_CALL trek_host_status(
    TrekHostClient* client, TrekHostStatus* out);
TREK_HOST_ABI_API TrekHostCode TREK_HOST_ABI_CALL trek_host_submit(
    TrekHostClient* client, const TrekHostRequest* request, uint64_t* ticket);
TREK_HOST_ABI_API TrekHostCode TREK_HOST_ABI_CALL trek_host_poll(
    TrekHostClient* client, uint64_t ticket, TrekHostCompletion* out);
TREK_HOST_ABI_API TrekHostCode TREK_HOST_ABI_CALL trek_host_discard(
    TrekHostClient* client, uint64_t ticket);

#ifdef __cplusplus
}
#endif
#endif
