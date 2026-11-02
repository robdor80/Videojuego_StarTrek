#pragma once
#include "f05_orders.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Additive ABI: existing F04 delegation entities and the same Core campaign.
 * One permission (issue F04_SCAN), domain SENSORS, one executor and one slot.
 * No resource, qualification, appointment or command ownership is transferred.
 * parent must be zero: subdelegation is explicitly unsupported. */
enum F05DelegationState { F05_DRAFT=1,F05_ACTIVE,F05_SUSPENDED,F05_REVOKED,F05_EXPIRED };
enum F05ControlMode { F05_MANUAL=1,F05_PROPOSAL_REQUIRES_APPROVAL,F05_DELEGATED_AUTONOMOUS };
typedef struct {
 F04Ref delegant,delegate,ship,station,executor;
 uint64_t key,expected_revision,start,end,cause,parent;
 uint32_t domain,operation,mode,reserved;
} F05DelegationRequest;
typedef struct {
 F04Ref actor;
 uint64_t delegation,key,expected_revision,cause;
 uint32_t state,mode;
} F05DelegationChange;
typedef struct {
 uint64_t id,delegant,delegate,ship,station,executor,origin,holder;
 uint64_t key,input_revision,start,end,cause,event,revision;
 uint32_t domain,operation,state,mode,effective_code,reserved;
} F05DelegationView;
typedef struct {
 uint64_t id,previous,delegation,actor,key,input_revision,cause,tick;
 uint32_t state,mode,operation,reserved; /* operation: 0=create, 1=change */
} F05DelegationEvent;
F04_API uint32_t f05_delegate(F04Session*,const F05DelegationRequest*,F05DelegationView*);
F04_API uint32_t f05_change_delegation(F04Session*,const F05DelegationChange*,F05DelegationView*);
F04_API uint32_t f05_delegation(F04Session*,F04Ref observer,uint64_t,F05DelegationView*);
F04_API uint32_t f05_delegations_page(F04Session*,F04Ref observer,uint64_t after,
 F05DelegationView*,uint64_t capacity,uint64_t* written,uint32_t* more);
F04_API uint32_t f05_delegation_events(F04Session*,F04Ref observer,uint64_t,uint64_t after,
 F05DelegationEvent*,uint64_t capacity,uint64_t* written,uint32_t* more);
/* A nonzero delegation is pinned even when issuer independently gains authority.
 * Manual/proposal orders remain issued until current delegant explicitly approves.
 * Approval never overrides suspension/revocation, time, scope or F04 rechecks. */
F04_API uint32_t f05_submit_delegated(F04Session*,const F05OrderRequest*,uint64_t delegation,F05Receipt*);
F04_API uint32_t f05_approve_order(F04Session*,F04Ref actor,uint64_t revision,uint64_t order,uint64_t cause,F05Receipt*);
#ifdef __cplusplus
}
#endif
