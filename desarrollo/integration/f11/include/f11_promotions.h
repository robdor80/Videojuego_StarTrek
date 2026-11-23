#pragma once
#include "f04_bridge.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Additive trusted-native ABI 1. No grant/commission issuance endpoint.
 * The owning Host authenticates callers; never expose this ABI to AI/Blueprint.
 * Numeric IDs refer to existing Core facts, not assertions of authority.
 */
enum F11Code { F11_UNCOMMISSIONED=200, F11_AUTHORITY, F11_EVALUATION,
 F11_RANK, F11_IDEMPOTENCY_CONFLICT, F11_IDENTITY, F11_ORDER };
enum F11Rank { F11_ENSIGN=1101, F11_LIEUTENANT_JUNIOR_GRADE=1102 };
enum F11Visibility { F11_SUBJECT_AND_PERSONNEL=1 };
typedef struct {
 uint64_t high48,mid48;
 uint32_t low32,reserved;
} F11CharacterId;
typedef struct {
 F04Ref subject;
 F11CharacterId character;
 uint64_t expected_revision,key,grant,order,evaluation,commission,rank_event,effective_tick,cause;
 uint32_t from_rank,to_rank;
} F11PromotionRequest;
typedef struct {
 F11CharacterId character;
 uint64_t key,promotion_event_id,personnel_order_id,rank_event_id;
 uint64_t original_commit_revision,current_revision,effective_at;
 uint32_t from_rank,to_rank,status,reserved;
} F11PromotionReceipt;
typedef struct {
 F11CharacterId character;
 uint64_t person,commission,rank_event,ship,billet,department,revision;
 uint32_t rank,service_status;
} F11PersonnelView;
typedef struct {
 F11PromotionReceipt receipt;
 uint64_t person,ship,billet,department,grant,authority,origin;
 uint64_t commission,previous_rank_event,evaluation,cause,input_revision;
 uint32_t visibility,reserved;
} F11PromotionView;
/* Same key + semantic payload returns original persisted receipt even with an
 * old expected_revision or revoked authority. Revision and process scope are
 * preconditions, not semantic payload. Rebind subject after loading.
 * Denials and exceptions never publish changes, including denial audit events.
 */
F04_API uint32_t f11_commit_promotion(F04Session*,const F11PromotionRequest*,F11PromotionReceipt*);
/* Subject-only diagnostic projections for the trusted Host. Not NPC knowledge. */
F04_API uint32_t f11_personnel(F04Session*,F04Ref subject,F11PersonnelView*);
F04_API uint32_t f11_promotion(F04Session*,F04Ref subject,uint64_t event,F11PromotionView*);
#ifdef __cplusplus
}
#endif
