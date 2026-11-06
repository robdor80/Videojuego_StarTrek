#pragma once
#include "f04_bridge.h"
#ifdef __cplusplus
extern "C" {
#endif
/* F06 native ABI 1, opt-in F06_ENABLE_SENSORS, same F04Session/Core campaign.
 * f06_host_signal is a PRIVILEGED trusted-host world-materialization port,
 * NEVER expose it to LCARS, dialogue, multiplayer or untrusted scripts.
 * Other queries accept authenticated in-campaign F04Ref identities.
 * Distances and positions are fixed-point milli-AU relative to the observing
 * ship. Strength/interference are normalized gameplay scores, not canon.
 */
enum F06ContactStatus { F06_ACTIVE=1, F06_LOST=2 };
enum F06NoticeKind { F06_NEW_CONTACT=1, F06_CONTACT_LOST=2,
 F06_ANOMALOUS_LOSS=3, F06_REACQUIRED=4, F06_IDENTIFIED=5 };
enum F06ExitEvidence { F06_EXIT_UNKNOWN=0, F06_EXIT_OBSERVED_WARP=1,
 F06_EXIT_OBSERVED_OCCLUSION=2, F06_EXIT_OBSERVED_OUT_OF_RANGE=3, F06_EXIT_SENSOR_OFFLINE=4 };
typedef struct {
 uint64_t expected_revision;
 uint64_t signal_id; /* zero creates; nonzero updates existing world signature */
 int64_t relative_x_milli_au,relative_y_milli_au,relative_z_milli_au;
 uint64_t transponder_id; /* trusted-world truth, never returned until resolved */
 uint32_t strength_permille; /* 0..1000 */
 uint32_t interference_permille; /* 0..550 */
 uint32_t class_id; /* catalog numeric class identifier, 0=unknown */
 uint32_t active; /* 0 or 1 */
 uint32_t observed_exit_evidence; /* trusted observation, 0 when not established */
 uint32_t reserved;
} F06SignalInput;
typedef struct {
 uint64_t signal_id,revision;
} F06SignalReceipt;
typedef struct {
 uint64_t contact_id,first_seen,last_seen;
 int64_t observed_x_milli_au,observed_y_milli_au,observed_z_milli_au;
 uint64_t transponder_id;
 uint32_t status,confidence_permille,distance_milli_au,class_id,loss_cause;
} F06ContactView;
typedef struct {
 uint64_t event_id,contact_id,tick;
 uint32_t kind;
} F06NoticeView;
/* TRUSTED SPATIAL WORLD FEED (NOT a sensor-facing/UI API).
 * Domain World Host publishes a full *authoritative* snapshot of spatial
 * entities in one shared coordinate frame. Never infer entities from scans,
 * JSON visual assets, encounter prompts or LLM narration.
 * Ingesting an entity is a materialization of existing world truth only.
 * Snapshot must cover all materialized entities for this observer, including
 * a zero-entity frame. Omitted old keys are marked inactive, NOT destroyed.
 * The ship origin must be supplied from real navigation state in the same
 * fixed coordinate frame. Position updates require new snapshots from Host.
 */
typedef struct {
 uint64_t world_entity_key; /* stable nonzero external ID, opaque and Host-only */
 int64_t absolute_x_milli_au,absolute_y_milli_au,absolute_z_milli_au;
 uint64_t transponder_id;
 uint32_t class_id,strength_permille,interference_permille;
 uint32_t active,observed_exit_evidence; /* 0..1; 0..F06_EXIT_OBSERVED_OUT_OF_RANGE */
} F06WorldEntity;
typedef struct {
 uint64_t expected_revision; /* current Core World revision */
 uint64_t source_revision; /* monotonic, durable spatial-world authority revision */
 uint64_t snapshot_tick; /* MUST equal Core campaign clock tick */
 int64_t observer_x_milli_au,observer_y_milli_au,observer_z_milli_au;
 uint64_t entity_count;
 const F06WorldEntity* entities;
} F06WorldSnapshot;
typedef struct {
 uint64_t core_revision,source_revision;
 uint32_t created,updated,retired;
} F06WorldReceipt;
F04_API uint32_t f06_host_world_snapshot(F04Session*,const F06WorldSnapshot*,F06WorldReceipt*);

/* Actual sensor hardware state, supplied ONLY by the trusted engineering/
 * operations host. No UI/AI claims repairs or power assignments directly.
 * Missing explicit override means the ship's installed nominal configuration. */
typedef struct {
 uint64_t expected_revision;
 uint32_t capability_permille,power_permille,integrity_permille;
 uint32_t short_enabled,long_enabled,focused_enabled;
 uint32_t reserved;
} F06ArrayInput;
typedef struct {
 uint32_t capability_permille,power_permille,integrity_permille;
 uint32_t short_enabled,long_enabled,focused_enabled;
} F06ArrayView;
F04_API uint32_t f06_host_array_state(F04Session*,const F06ArrayInput*,F06ArrayView*);
F04_API uint32_t f06_array_status(F04Session*,F04Ref observer,F06ArrayView*);
/* Privileged domain host: materialize/change a physical signature in Core state.
 * Does not fabricate mission events, execute a scan, or grant observer knowledge.
 * Revalidation/commit occurs against the current Core revision atomically. */
F04_API uint32_t f06_host_signal(F04Session*,const F06SignalInput*,F06SignalReceipt*);
/* Read active/lost contact memory for a real F04 observer in the ship. */
F04_API uint32_t f06_contacts_page(F04Session*,F04Ref observer,uint32_t status,
 uint64_t offset,F06ContactView*,uint64_t capacity,uint64_t* written,uint64_t* total);
/* Distinct audit notices; not all routine observations are notices. */
F04_API uint32_t f06_notices_page(F04Session*,F04Ref observer,uint64_t after_event_id,
 F06NoticeView*,uint64_t capacity,uint64_t* written,uint32_t* more);
/* Operator must currently occupy Sensors under F04. Only an ACTIVE, already
 * known contact may be targeted. No operator booleans or raw entity IDs. */
F04_API uint32_t f06_focus(F04Session*,F04Ref operator_ref,uint64_t revision,
 uint64_t contact_id,F06ContactView*);
/* A power request never changes the actual ship power allocation.
 * Only Command / Operations can approve or reject. The trusted power host
 * must separately implement a physical grant before Sensors uses it. */
enum F06PowerState { F06_POWER_QUEUED=1,F06_POWER_APPROVED=2,
 F06_POWER_DENIED=3,F06_POWER_EXPIRED=4 };
typedef struct {
 uint64_t expected_revision,request_key;
 uint32_t extra_power_permille,duration_seconds;
} F06PowerRequest;
typedef struct {
 uint64_t request_id,created_at,expires_at,decision_at;
 uint32_t extra_power_permille,state;
} F06PowerView;
F04_API uint32_t f06_request_power(F04Session*,F04Ref sensor_operator,
 const F06PowerRequest*,F06PowerView*);
F04_API uint32_t f06_decide_power(F04Session*,F04Ref command_or_ops,
 uint64_t expected_revision,uint64_t request_id,uint32_t decision,F06PowerView*);
F04_API uint32_t f06_power_requests_page(F04Session*,F04Ref observer,uint64_t offset,
 F06PowerView*,uint64_t capacity,uint64_t* written,uint64_t* total);

/* Focused scan of a coordinate/area is possible without an existing contact.
 * The result reports ONLY actually observed detections, never world signature
 * counts or internal IDs. Coordinates are milli-AU in the ship reference frame. */
typedef struct {
 uint64_t expected_revision;
 int64_t center_x_milli_au,center_y_milli_au,center_z_milli_au;
 uint32_t radius_milli_au,reserved;
} F06AreaRequest;
typedef struct {
 uint64_t revision,observed_contacts,new_contacts;
} F06AreaReceipt;
F04_API uint32_t f06_scan_area(F04Session*,F04Ref operator_ref,
 const F06AreaRequest*,F06AreaReceipt*);

/* F06 dedicated tracking is a finite resource; passive monitoring remains ON.
 * Modes: 0 passive automatic; 1 explicit normal tracking; 2 priority tracking.
 * Power/damage may reduce capacity, but never creates or deletes real contacts. */
enum F06TrackMode { F06_TRACK_PASSIVE=0, F06_TRACK_NORMAL=1, F06_TRACK_PRIORITY=2 };
typedef struct {
 uint64_t contact_id,updated_at;
 uint32_t mode,used_slots,available_slots,overloaded;
} F06TrackView;
F04_API uint32_t f06_tracking_status(F04Session*,F04Ref observer,F06TrackView*);
F04_API uint32_t f06_set_tracking(F04Session*,F04Ref operator_ref,
 uint64_t expected_revision,uint64_t contact_id,uint32_t mode,F06TrackView*);

/* Real persistent SENSOR -> SCIENCE queue on the same Core campaign.
 * Analysis is a request, not a fabricated scientific conclusion.
 * F06 science kinds: 1 classify contact; 2 investigate anomaly;
 * 3 study emissions; 4 map local environment.
 * Priority: 1 routine; 2 normal; 3 high; 4 urgent. */
typedef struct {
 uint64_t expected_revision,request_key,contact_id;
 uint32_t priority,analysis_kind;
} F06ScienceRequest;
typedef struct {
 uint64_t handoff_id,contact_id,created_at,observed_at,transponder_id;
 int64_t observed_x_milli_au,observed_y_milli_au,observed_z_milli_au;
 uint32_t priority,analysis_kind,status,class_id,confidence_permille;
} F06ScienceView;
F04_API uint32_t f06_science_handoff(F04Session*,F04Ref operator_ref,
 const F06ScienceRequest*,F06ScienceView*);
F04_API uint32_t f06_science_queue_page(F04Session*,F04Ref observer,
 uint64_t offset,F06ScienceView*,uint64_t capacity,uint64_t* written,uint64_t* total);
/* Read-only numeric catalog resolution belongs to Star Trek, not CoreRPG. */
#ifdef __cplusplus
}
#endif
