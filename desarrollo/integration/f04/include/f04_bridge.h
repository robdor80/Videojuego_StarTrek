#pragma once
#include <stdint.h>
#if defined(_WIN32)
# if defined(F04_BRIDGE_BUILD)
#  define F04_API __declspec(dllexport)
# else
#  define F04_API __declspec(dllimport)
# endif
#else
# define F04_API __attribute__((visibility("default")))
#endif
#ifdef __cplusplus
extern "C" {
#endif
typedef struct F04Session F04Session;
typedef struct { uint64_t scope,id; } F04Ref;
enum F04Code { F04_OK, F04_ARGUMENT, F04_DENIED, F04_QUALIFICATION, F04_UNAVAILABLE,
 F04_OVERLAP, F04_VACANT, F04_SCOPE, F04_EXPIRED, F04_REVOKED, F04_SAFETY,
 F04_REVIEW, F04_STALE, F04_THREAD, F04_SAVE, F04_CAPACITY, F04_INTERNAL };
enum F04Op { F04_ASSIGN=1,F04_DUTY,F04_REST,F04_ONCALL,F04_ABSENCE,F04_RELIEF,
 F04_APPOINT,F04_DELEGATE,F04_REVOKE,F04_MEDICAL,F04_POLICY,F04_SCAN,F04_BRIDGE,
 F04_IMPOSSIBLE,F04_CONTACT,F04_QUEUE,F04_RECALL,F04_SUPERIOR,F04_MOVE,F04_PROPOSE,F04_CONTACT_REVIEW };
enum F04Role { F04_CAPTAIN=1,F04_HEAD,F04_WATCH,F04_DOCTOR,F04_FIRST,F04_SECOND,F04_SUCCESSOR };
enum F04Dept { F04_SENSORS=1,F04_ENGINEERING=2,F04_COMMAND=3,F04_MEDICINE=4 };
enum F04Absence { F04_LEAVE=1,F04_SICK=2,F04_SUSPENDED=3 };
/* Host authenticates actor; all operations are intentions, never permissions.
 * target/aux depend on operation. revision must equal the current world revision.
 * cause is a stable host incident/document reference, not a permission token. */
typedef struct { F04Ref actor; uint64_t revision; uint32_t op,value;
 uint64_t target,aux,start,end,cause; } F04Request;
typedef struct { uint32_t code,reserved; uint64_t record,revision; } F04Result;
typedef struct { F04Ref ship,captain,head,ensign,watch,doctor,relief,civilian,passenger,admiral;
 uint64_t sensors,engineering,bridge; } F04Handles;
typedef struct { uint64_t entities,revision,now,crew,civilians,passengers,slots,vacancies,
 commander,pending,events,pattern; } F04Stats;
typedef struct { uint64_t id,person,department,qualification; uint32_t required,covered,authorized,reserved; } F04Slot;
typedef struct { uint64_t id,category,rank,department; uint32_t available,on_duty,localized,at_console; } F04Person;
/* label: 0 Alpha, 1 Beta, 2 Gamma, 3 Delta; seconds on Core campaign clock. */
typedef struct { uint64_t start,end; uint32_t count,label; } F04WatchWindow;
F04_API const char* f04_core_sha(void);
/* Synthetic test scenario. class_id is validated against the existing catalog. */
F04_API uint32_t f04_create(uint32_t abi,const char* class_id,F04Session** out);
F04_API uint32_t f04_destroy(F04Session*);
F04_API uint32_t f04_handles(F04Session*,F04Handles*);
F04_API uint32_t f04_stats(F04Session*,F04Stats*);
F04_API uint32_t f04_execute(F04Session*,const F04Request*,F04Result*);
/* Privileged campaign-clock service, not an NPC/AI operation. */
F04_API uint32_t f04_advance(F04Session*,uint64_t horizon,uint64_t budget,uint64_t* processed);
F04_API uint32_t f04_manifest(F04Session*,F04Ref,F04Person*,uint64_t capacity,uint64_t* count);
F04_API uint32_t f04_slots(F04Session*,F04Ref,F04Slot*,uint64_t capacity,uint64_t* count);
F04_API uint32_t f04_watch_window(F04Session*,uint64_t tick,F04WatchWindow*);
F04_API uint32_t f04_save(F04Session*,uint8_t*,uint64_t capacity,uint64_t* size);
F04_API uint32_t f04_load(F04Session*,const uint8_t*,uint64_t size);
#ifdef __cplusplus
}
#endif
