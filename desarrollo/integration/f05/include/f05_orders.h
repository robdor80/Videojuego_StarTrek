#pragma once
#include "f04_bridge.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Additive trusted-native ABI 1, enabled explicitly with F05_ENABLE_ORDERS.
 * Uses the existing F04Session and campaign; Host authenticates both refs.
 * No authority booleans, separate world, remote/Blueprint/LLM permissions.
 * All IDs are Core EntityIds; keys and cause are nonzero 48-bit campaign values.
 */
enum F05Code { F05_UNSUPPORTED=100, F05_IDEMPOTENCY_CONFLICT, F05_TRANSITION };
enum F05OrderState { F05_ISSUED=1,F05_ACCEPTED,F05_EXECUTING,F05_COMPLETED,
 F05_FAILED,F05_REFUSED,F05_CANCELLED };
enum F05TaskState { F05_TASK_ACKNOWLEDGED=1,F05_TASK_IN_PROGRESS,
 F05_TASK_COMPLETED,F05_TASK_FAILED,F05_TASK_CANCELLED };
typedef struct {
 F04Ref issuer,recipient,ship,station;
 uint64_t key,expected_revision,deadline,cause;
 uint32_t operation,reserved; /* P01 supports F04_SCAN only, no parameters. */
} F05OrderRequest;
typedef struct {
 uint64_t request,order,task,attempt,result,event,revision;
 uint32_t state,code;
} F05Receipt;
typedef struct {
 F05Receipt receipt;
 uint64_t issuer,recipient,ship,station,origin,key,deadline,cause,issued_at,input_revision;
 uint32_t operation,reserved;
} F05OrderView;
typedef struct {
 uint64_t id,order,task,executor,input_revision,tick;
 uint32_t performed,code; /* performed means ActionEngine was actually called. */
 uint32_t core_outcome,core_rejection;
 uint64_t core_revision_before,core_revision_after,stream,value;
 uint32_t consumed_random,reserved;
} F05ResultView;
typedef struct {
 uint64_t id,previous,request,order,task,attempt,result,actor,tick;
 uint32_t state,code;
} F05EventView;
F04_API uint32_t f05_submit(F04Session*,const F05OrderRequest*,F05Receipt*);
/* Receive is explicit acknowledgement by the named recipient. Acceptance has no
 * scan effect. A task is created only after successful reception/revalidation. */
F04_API uint32_t f05_receive(F04Session*,F04Ref recipient,uint64_t revision,uint64_t order,F05Receipt*);
/* Synchronous, one attempt maximum. executing and terminal events commit with
 * the true Core result in one staged campaign transaction. Never auto-retry. */
F04_API uint32_t f05_execute_order(F04Session*,F04Ref recipient,uint64_t revision,uint64_t order,F05Receipt*);
F04_API uint32_t f05_cancel(F04Session*,F04Ref actor,uint64_t revision,uint64_t order,F05Receipt*);
/* Observer must be current commander, issuer or recipient; diagnostics for the
 * trusted Host. Not a knowledge/report API and never a general NPC context. */
F04_API uint32_t f05_order(F04Session*,F04Ref observer,uint64_t order,F05OrderView*);
F04_API uint32_t f05_result(F04Session*,F04Ref observer,uint64_t order,F05ResultView*);
F04_API uint32_t f05_events_page(F04Session*,F04Ref observer,uint64_t order,uint64_t after,
 F05EventView*,uint64_t capacity,uint64_t* written,uint32_t* more);
#ifdef __cplusplus
}
#endif
