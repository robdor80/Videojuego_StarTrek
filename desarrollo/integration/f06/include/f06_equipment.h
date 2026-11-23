#pragma once
#include "f06_sensors.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Opt-in physical signature port v1. Existing ABI and legacy saves unchanged.
 * TRUSTED HOST ONLY, same privilege boundary as f06_host_world_snapshot.
 * Slots: offensive energy emitters, launchers, shields, armour, warp, impulse.
 * Counts are installed devices, NOT ammunition. State: 0 unavailable, 1 idle,
 * 2 powered, 3 offensive emission active (valid only in offensive slots).
 * visibility is an instrument signal score, not an observer permission flag.
 * Materialize an inactive world entity first, then its physical configuration,
 * then publish its observable spatial state. Private fields never reach UI.
 */
typedef struct {
 uint64_t expected_revision,world_entity_key,source_revision;
 uint32_t version,length_m,cloaked,reserved;
 uint32_t count[6],state[6],visibility_permille[6];
} F06PhysicalInput;
typedef struct {
 uint64_t observation_id,contact_id,tick;
 uint32_t class_id,catalog_version,length_m,confidence_permille,visible_mask;
 uint32_t count[6],state[6],expected[6],comparison[6];
 /* comparison: 0 grey/no reference, 1 green/match, 2 amber/difference,
  * 3 red/actual offensive emission. Catalog counts are explicitly QA fiction. */
} F06EquipmentView;
typedef struct {
 uint64_t expected_revision,request_key,contact_id;
 uint32_t recipient,reserved; /* 1 superior, 2 Tactical QA, 3 Science QA */
} F06DeliveryRequest;
typedef struct {
 uint64_t receipt_id,contact_id,observation_id,tick;
 uint32_t recipient,status; /* 1 = durably delivered to authenticated QA queue */
} F06DeliveryView;
F04_API uint32_t f06_host_physical(F04Session*,const F06PhysicalInput*);
F04_API uint32_t f06_equipment_page(F04Session*,F04Ref,uint64_t contact_id,
 uint64_t offset,F06EquipmentView*,uint64_t capacity,uint64_t* written,uint64_t* total);
F04_API uint32_t f06_deliver(F04Session*,F04Ref,const F06DeliveryRequest*,F06DeliveryView*);
F04_API uint32_t f06_deliveries_page(F04Session*,F04Ref,uint64_t offset,
 F06DeliveryView*,uint64_t capacity,uint64_t* written,uint64_t* total);
/* Additive v2 queue: immutable public evidence only. kind: 1 equipment,
 * 2 focused position observation, 3 completed Science report. Retries bind
 * actor, contact, recipient AND source. No Host identifiers are accepted. */
typedef struct {
 uint64_t expected_revision,request_key,contact_id,source_id;
 uint32_t recipient,kind;
} F06EvidenceDeliveryRequest;
F04_API uint32_t f06_deliver_evidence(F04Session*,F04Ref,
 const F06EvidenceDeliveryRequest*,F06DeliveryView*);
F04_API uint32_t f06_contact_tracking(F04Session*,F04Ref,uint64_t,F06TrackView*);
/* Derived science, never a new assertion of hidden physical truth. Valid bits:
 * 1 Dalton partial pressures (microbar); 2 angular extent (nanoradian);
 * 4 displacement between archived observations; 8 equipment history.
 * No crew, mission, spectral composition or intention can be inferred here. */
typedef struct {
 uint64_t contact_id,position_source,science_source,equipment_source;
 uint64_t oxygen_microbar,co2_microbar,angular_nanoradian;
 uint64_t interval_seconds,displacement_micro_au,equipment_changes;
 uint32_t valid_mask,reserved;
} F06DeepAnalysisView;
F04_API uint32_t f06_deep_analysis(F04Session*,F04Ref,uint64_t,F06DeepAnalysisView*);
#ifdef __cplusplus
}
#endif
