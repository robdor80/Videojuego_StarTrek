#ifndef TREK_HOST_ACADEMY_ABI_H
#define TREK_HOST_ACADEMY_ABI_H

#include "host_abi.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Additive Academy extension 2 (independent of the frozen naval C ABI 1).
 * Draft Academy extension 1 is rejected with ABI_MISMATCH; no layout grows.
 * Resolve version/submit/poll together; version 0 means
 * unavailable. Uses the v1 client, status, discard, SAVE, RESTORE and CLOSE.
 * Never pass extension tickets to v1 poll (or conversely). Wrong poll leaves
 * the ticket intact. All calls share v1's serialization/lifetime rules. */
#define TREK_HOST_ACADEMY_VERSION 2u
#define TREK_HOST_ACADEMY_NAME_BYTES 96u
#define TREK_HOST_ACADEMY_MAX_SLOTS 64u

enum {
    TREK_HOST_ACADEMY_CREATE = 1,
    TREK_HOST_ACADEMY_QUERY = 2,
    TREK_HOST_ACADEMY_SLOTS = 3
};
enum { TREK_HOST_KIND_UNKNOWN = 0, TREK_HOST_KIND_NAVAL = 1, TREK_HOST_KIND_ACADEMY = 2 };
enum { TREK_HOST_CANDIDATE = 1 };
enum {
    TREK_HOST_CREATED_LOCALLY = 0, TREK_HOST_KNOWN_LOCAL = 1,
    TREK_HOST_IMPORTED_UNVERIFIED = 2, TREK_HOST_REJECTED = 3
};

typedef struct {
    uint32_t size, version, operation, reserved;
    uint64_t generation;
    /* CREATE only: nonzero, monotonically increasing per live client. Retry
     * the same key and exact name (even after discard); different name conflicts.
     * generation must be 0. CLOSE/RESTORE/OPEN retire this intent: its old key
     * expires forever in this client. A higher key starts only from CLOSED.
     * No durable creation before SAVE: process death loses unsaved campaigns. */
    union {
        uint64_t creation_key;
        uint64_t slot_cursor; /* SLOTS only: 0 starts; otherwise next_cursor. */
    };
    TrekHostText display_name; /* CREATE only, validated UTF-8/S04, 1..96 bytes. */
} TrekHostAcademyRequest;

typedef struct {
    uint64_t person, creation_fact, revision, tick;
    uint32_t kind, candidate_state;
    char campaign[33];
    char display_name[TREK_HOST_ACADEMY_NAME_BYTES + 1];
    char source_digest[65];
    uint8_t padding[5];
} TrekHostAcademyView;

typedef struct {
    uint64_t version;
    uint32_t kind, format, provenance;
    TrekHostCode reason;
    uint32_t compatible, recoverable;
    char campaign[33], slot[33];
    uint8_t padding[6];
} TrekHostSlotMetadata;

typedef struct {
    uint32_t size;
    TrekHostCode code; /* No payload/generation unless OK. */
    uint32_t operation, reserved;
    uint64_t ticket, generation;
    union {
        TrekHostAcademyView candidate;
        struct {
            uint32_t count, next_cursor; /* 0 ends the walk; otherwise continue. */
            TrekHostSlotMetadata entries[TREK_HOST_ACADEMY_MAX_SLOTS];
        } slots;
    } output;
} TrekHostAcademyCompletion;

/* QUERY requires the exact live generation and a confirmed H03 binding.
 * SLOTS requires the current generation (0 in CLOSED); runs H04 inspection
 * on the owner thread. Up to 64 rows per page, ordered by campaign ASCII,
 * slot ASCII, then version descending. Follow next_cursor until 0, including
 * empty pages (bounded traversal of empty directories). Each row includes
 * H04 integrity errors; metadata never authorizes RESTORE.
 * Cursors are opaque observations, scoped to this client/current generation.
 * SAVE, OPEN, CREATE, RESTORE and CLOSE retire them. The last 32 positions are
 * retained; an evicted/foreign/retired cursor returns GENERATION_EXPIRED.
 * Retry/discard may reread a retained position. External filesystem changes
 * are revalidated per page; restart at 0 to include new rows before a cursor.
 * This is a live keyset walk, not a disk snapshot or a retained storage lock.
 * Both submit/poll are nonblocking; RETRY admits/consumes nothing. The eight
 * observation slots are shared with v1 and CLOSE retains its reserved slot. */
TREK_HOST_ABI_API uint32_t TREK_HOST_ABI_CALL trek_host_academy_version(void);
TREK_HOST_ABI_API TrekHostCode TREK_HOST_ABI_CALL trek_host_academy_submit(
    TrekHostClient*, const TrekHostAcademyRequest*, uint64_t* ticket);
TREK_HOST_ABI_API TrekHostCode TREK_HOST_ABI_CALL trek_host_academy_poll(
    TrekHostClient*, uint64_t ticket, TrekHostAcademyCompletion*);

#ifdef __cplusplus
}
#endif
#endif
