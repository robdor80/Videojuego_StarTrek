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
 F04_IMPOSSIBLE,F04_CONTACT,F04_QUEUE,F04_RECALL,F04_SUPERIOR,F04_MOVE,F04_PROPOSE,F04_CONTACT_REVIEW,
 F04_EMBARK,F04_DEPART,F04_CREATE_SLOT,
 F04_INSTALL_TEMPLATE,F04_BOOTSTRAP_TEMPLATE,F04_CREDENTIAL,F04_TRANSFER,
 F04_FUNCTION,F04_PLAN_ALPHA };
enum F04Role { F04_CAPTAIN=1,F04_HEAD,F04_WATCH,F04_DOCTOR,F04_FIRST,F04_SECOND,F04_SUCCESSOR,F04_DEPUTY };
/* Existing department and qualification IDs 1..4 never change. */
enum F04Dept { F04_SENSORS=1,F04_ENGINEERING=2,F04_COMMAND=3,F04_MEDICINE=4,
 F04_OPERATIONS=5,F04_SECURITY=6,F04_LOGISTICS=7 };
enum F04Qualification { F04_Q_HELM=8,F04_Q_MISSION,F04_Q_PROPULSION,F04_Q_POWER,
 F04_Q_LIFE_SUPPORT,F04_Q_REPAIR,F04_Q_ASTROMETRY,F04_Q_PHYSICS,F04_Q_BIOLOGY,
 F04_Q_GEOLOGY,F04_Q_LAB,F04_Q_COMMUNICATIONS,F04_Q_TRANSPORTER,F04_Q_COMPUTING,
 F04_Q_TACTICAL,F04_Q_INTERIOR_SECURITY,F04_Q_EMERGENCY,F04_Q_SHUTTLE,
 F04_Q_HANGAR,F04_Q_CARGO,F04_Q_CLINICAL,F04_Q_NURSING,F04_Q_DIAGNOSTICS };
enum F04Station { F04_ST_COMMAND=1,F04_ST_HELM=2,F04_ST_SENSORS=4,
 F04_ST_ENGINEERING=8,F04_ST_COMMUNICATIONS=16,F04_ST_TRANSPORTER=32,
 F04_ST_COMPUTER=64,F04_ST_TACTICAL=128,F04_ST_HANGAR=256,F04_ST_MEDICAL=512,
 F04_ST_LAB=1024,F04_ST_CARGO=2048,F04_ST_SECURITY=4096 };
enum F04Coverage { F04_DAY_ACTIVITY=1,F04_CONTINUOUS_CANDIDATE,F04_URGENT_PENDING };
enum F04Template { F04_SUTHERLAND_SCIENCE=1, F04_INTREPID_EXPLORATION=2 };
#define F04_SUTHERLAND_EQUIPMENT UINT64_C(8191)
/* Functional system references; counts and special technology remain configurable. */
#define F04_INTREPID_EQUIPMENT UINT64_C(8191)
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
 commander,pending,events,pattern,alert; } F04Stats;
typedef struct { uint64_t id,person,department,qualification; uint32_t required,covered,authorized,reserved; } F04Slot;
typedef struct { uint64_t id,category,rank,department; uint32_t available,on_duty,localized,at_console; } F04Person;
/* label: 0 Alpha, 1 Beta, 2 Gamma, 3 Delta; seconds on Core campaign clock. */
typedef struct { uint64_t start,end; uint32_t count,label; } F04WatchWindow;
F04_API const char* f04_core_sha(void);
/* Synthetic test scenario. class_id is validated against the existing catalog. */
F04_API uint32_t f04_create(uint32_t abi,const char* class_id,F04Session** out);
/* Additive ABI 1 extension: trusted host bootstrap. Zero maximum means unspecified,
 * never the nominal complement. Counts describe real individuals, not slots.
 * ship_identity is a stable campaign ID supplied by the host; seed persists in Core. */
typedef struct { uint64_t ship_identity,seed,crew,residents,passengers,maximum; } F04PopulationConfig;
typedef struct { uint64_t ship_identity,nominal_crew,nominal_residents,maximum,
 assigned,present,residents,passengers,departed,nominal_vacancies; } F04PopulationStats;
F04_API uint32_t f04_create_population(uint32_t abi,const char* class_id,const F04PopulationConfig*,F04Session**);
F04_API uint32_t f04_population_stats(F04Session*,F04PopulationStats*);
/* Paged manifest returns current members only, total and written independently. */
F04_API uint32_t f04_manifest_page(F04Session*,F04Ref,uint64_t offset,F04Person*,uint64_t capacity,uint64_t* written,uint64_t* total);
F04_API uint32_t f04_person(F04Session*,F04Ref observer,uint64_t id,F04Person*);
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
/* Additive ABI 1 / SCHEMA 3. All runtime rows below project Core relations.
 * INSTALL: value=template, aux=installed equipment mask; creates vacancies only.
 * BOOTSTRAP: explicit synthetic fixture, once, existing unconfigured crew only.
 * CREDENTIAL: target=person, aux=qualification mask, end=expiry, cause=evidence.
 * TRANSFER: target=destination slot, aux=person; cancels old duties/functions.
 * FUNCTION: target=person, aux=nominal slot, value=one station, start/end.
 * PLAN_ALPHA: start/end=08:00..16:00 of one day, aux=1 appoints first as watch.
 * Mutations require current commander; FUNCTION also allows own department head.
 */
typedef struct { uint64_t id,department,total,alpha,qualification,stations,coverage;
 const char *name,*responsibilities,*equipment; } F04SectionSpec;
typedef struct { uint64_t id,nominal_crew,nominal_residents,required_equipment;
 const char *class_id,*configuration,*mission,*era; } F04TemplateSpec;
typedef struct { uint64_t id,stable_id,department,section,ordinal,person,
 qualification,qualification_mask,responsibility,stations,coverage,alpha,duty_record;
 uint32_t on_duty,at_station; } F04Position;
typedef struct { uint64_t template_id,departments,sections,positions,assigned,vacant,
 on_duty,alpha_expected,alpha_present,alpha_deficit,continuous_candidates,
 continuous_required,continuous_covered,urgent_response;
 uint32_t coverage_validated,reserved; } F04OrganizationStats;
typedef struct { uint64_t person,slot,station,start,end; uint32_t active,reserved; } F04FunctionView;
F04_API uint32_t f04_template_spec(uint64_t,F04TemplateSpec*);
F04_API uint32_t f04_template_sections(uint64_t,F04SectionSpec*,uint64_t capacity,uint64_t* count);
F04_API uint32_t f04_organization_stats(F04Session*,F04Ref,F04OrganizationStats*);
F04_API uint32_t f04_positions_page(F04Session*,F04Ref,uint64_t offset,F04Position*,uint64_t capacity,uint64_t* written,uint64_t* total);
F04_API uint32_t f04_person_credentials(F04Session*,F04Ref,uint64_t person,uint64_t* mask,uint64_t* expiry);
F04_API uint32_t f04_functions(F04Session*,F04Ref,F04FunctionView*,uint64_t capacity,uint64_t* count);
#ifdef __cplusplus
}
#endif
