#pragma once
#include "f05_delegation.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Trusted native Host, same owner-thread F04Session. Bind the authenticated
 * player once before enabling autonomy; it cannot be changed within a campaign.
 * No Actor, UI, LLM, clock, seed or authority flags are accepted here. */
enum F05Decision { F05_NO_ACTION=1,F05_CLARIFY,F05_REPORT,F05_PROPOSE,
 F05_ISSUE_ORDER,F05_CONTINUE_TASK,F05_ESCALATE,F05_WAIT_PLAYER };
typedef struct {
 F04Ref issuer;
 uint64_t duty,key,expected_revision,due,end,cause;
} F05ScanNeedRequest;
typedef struct {
 uint64_t id,issuer,origin,duty,station,recipient,key,input_revision,due,end,cause,tick;
} F05NeedView;
typedef struct {
 F04Ref actor;
 uint64_t need,key,expected_revision;
 uint32_t max_facts,reserved; /* 1..32; incomplete context never authorizes. */
} F05Evaluation;
typedef struct {
 uint64_t id,need,actor,key,input_revision,tick,detection,order,target,revision;
 uint32_t decision,code,examined,max_facts;
} F05DecisionView;
F04_API uint32_t f05_bind_player(F04Session*,F04Ref player,uint64_t revision);
/* An authorized one-scan-per-service obligation, not a fabricated incident.
 * Source must be a real F04 Sensores DUTY and cover [due,end). No scan yet. */
F04_API uint32_t f05_scan_need(F04Session*,const F05ScanNeedRequest*,F05NeedView*);
/* Explicit formal communication. Only the effective command/authorized author
 * can brief. Teaches this obligation's immutable subset via Core knowledge. */
F04_API uint32_t f05_brief_need(F04Session*,F04Ref sender,F04Ref recipient,
 uint64_t revision,uint64_t need,uint64_t key,uint64_t cause,uint64_t* communication);
/* One need, one known service provider, at most one P01 transition per call.
 * Invoke after f04_advance/events; this does not install a global scheduler.
 * Keys are campaign-wide for evaluations, separate from P01/P02 spaces.
 * A new key re-evaluates current authorization; replay never mutates again. */
F04_API uint32_t f05_evaluate(F04Session*,const F05Evaluation*,F05DecisionView*);
/* Own decisions only. These diagnostics are never fed back as NPC knowledge. */
F04_API uint32_t f05_decisions_page(F04Session*,F04Ref actor,uint64_t after,
 F05DecisionView*,uint64_t capacity,uint64_t* written,uint32_t* more);
#ifdef __cplusplus
}
#endif
