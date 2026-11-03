#pragma once
#include "f05_initiative.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Trusted owner-thread Host API. Provider sees Context only; never Session/refs.
 * Optional language layer: P03 remains callable while any request is pending. */
enum F05AiRoute { F05_AI_DETERMINISTIC=1,F05_AI_FAST,F05_AI_REASONING };
enum F05AiStatus { F05_AI_PENDING=0,F05_AI_VALID,F05_AI_CLARIFICATION,
 F05_AI_INSUFFICIENT,F05_AI_REJECTED,F05_AI_STALE,F05_AI_FALLBACK,F05_AI_APPLIED,F05_AI_APPROVAL };
enum F05AiError { F05_AI_NONE=0,F05_AI_NOT_CONFIGURED,F05_AI_NETWORK,F05_AI_TIMEOUT,
 F05_AI_HTTP,F05_AI_QUOTA,F05_AI_EMPTY,F05_AI_MALFORMED,F05_AI_BINDING,
 F05_AI_RESTRICTION,F05_AI_RECOVERED };
enum F05AiIntent { F05_AI_ADVISE=1,F05_AI_SCAN,F05_AI_ASK,F05_AI_UNKNOWN };
typedef struct {
 F04Ref actor;
 uint64_t need,key,expected_revision,expires;
 uint32_t route,reserved;
} F05AiRequest;
/* Closed allowlist, assembled from the actor's P03 ObserverView. Unknown IDs
 * are never echoed. No private memories, truth, raw save or diagnostics. */
typedef struct {
 uint64_t request,actor,projection,revision,issued_at,expires;
 uint64_t need,duty,station,operator_id,due,end;
 uint32_t version,route,complete,allowed_operation;
} F05AiContext;
typedef struct {
 uint64_t request,actor,context_revision,settled_revision,issued_at,expires;
 uint64_t decision,order,revision;
 uint32_t status,error,intent,route;
} F05AiView;
F04_API uint32_t f05_ai_begin(F04Session*,const F05AiRequest*,F05AiContext*);
/* Strict bounded JSON v1; text/trace remain untrusted ephemeral content. A
 * finish never issues/receives/executes orders, teaches facts or approves. */
F04_API uint32_t f05_ai_finish(F04Session*,F04Ref actor,uint64_t request,
 const char* json,uint64_t size,uint32_t transport_error,F05AiView*);
F04_API uint32_t f05_ai_view(F04Session*,F04Ref actor,uint64_t request,F05AiView*);
/* Explicit Host handoff of a VALID scan candidate to unchanged P03. Authority,
 * player consent and all P01/P02 checks remain there. Not player approval.
 * Advice/clarification/fallback cannot be applied as model actions. */
F04_API uint32_t f05_ai_apply(F04Session*,F04Ref actor,uint64_t request,F05AiView*);
#ifdef __cplusplus
}
#endif
