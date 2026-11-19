#pragma once
#include "f06_sensors.h"
#ifdef __cplusplus
extern "C" {
#endif
/* F06-BIS additive native ABI. Trusted host functions must never be made
 * available to LCARS, Blueprints, NPC dialogue, or untrusted content.
 * These interfaces use the SAME F04Session, Core campaign and save/load. */

/* Environmental readings are asserted by the trusted spatial Host, not by
 * a sensor query. They apply at the current ship origin until superseded. */
enum F06Band { F06_BAND_EM=1,F06_BAND_THERMAL=2,F06_BAND_GRAVIMETRIC=3,
 F06_BAND_SUBSPACE=4,F06_BAND_BIOLOGICAL=5 };
typedef struct {
 uint64_t expected_revision,source_revision;
 uint32_t em_permille,thermal_permille,gravimetric_permille,
   subspace_permille,biological_permille,reserved;
} F06EnvironmentInput;
typedef struct {
 uint64_t source_revision;
 uint32_t em_permille,thermal_permille,gravimetric_permille,
   subspace_permille,biological_permille;
} F06EnvironmentView;
F04_API uint32_t f06_host_environment(F04Session*,const F06EnvironmentInput*,F06EnvironmentView*);
F04_API uint32_t f06_environment_status(F04Session*,F04Ref,F06EnvironmentView*);

/* Independent primary-saucer and battle-section array materialization.
 * linked=1 only if the array belongs to the current observer's sensor network.
 * A detached section is retained in Core but does not help this observer.
 * The separation/navigation event itself MUST come from a trusted ship Host. */
enum F06Section { F06_SECTION_SAUCER=1,F06_SECTION_BATTLE=2 };
typedef struct {
 uint64_t expected_revision;
 uint32_t section_id,linked,capability_permille,power_permille,integrity_permille,
  short_enabled,long_enabled,focused_enabled;
} F06SectionInput;
typedef struct {
 uint32_t section_id,configured,linked,capability_permille,power_permille,
  integrity_permille,short_enabled,long_enabled,focused_enabled;
} F06SectionView;
F04_API uint32_t f06_host_section_array(F04Session*,const F06SectionInput*,F06SectionView*);
F04_API uint32_t f06_section_status(F04Session*,F04Ref,uint32_t section_id,F06SectionView*);

/* Focused scans with time, finite concurrent slots and interruption states.
 * No synthetic immediate result: a true scan observation is committed only on
 * F04 campaign-clock advance after authority/equipment/source revalidation.
 * Cost units are gameplay reservations, not verified ship watt-hours. */
enum F06TimedScanStatus {
 F06_TIMED_QUEUED=1,F06_TIMED_FINISHED=2,F06_TIMED_FAILED=3,F06_TIMED_CANCELLED=4
};
typedef struct {
 uint64_t expected_revision,request_key,contact_id;
 uint32_t nominal_seconds,reserved;
} F06TimedScanRequest;
typedef struct {
 uint64_t scan_id,contact_id,started_at,finishes_at,result_id;
 uint32_t status,reserved_cost_permille;
} F06TimedScanView;
F04_API uint32_t f06_begin_timed_scan(F04Session*,F04Ref,const F06TimedScanRequest*,F06TimedScanView*);
F04_API uint32_t f06_cancel_timed_scan(F04Session*,F04Ref,uint64_t expected_revision,
 uint64_t scan_id,F06TimedScanView*);
F04_API uint32_t f06_timed_scans_page(F04Session*,F04Ref,uint64_t offset,
 F06TimedScanView*,uint64_t capacity,uint64_t* written,uint64_t* total);

/* Sensor -> Science: a queued Core handoff may be resolved ONLY by an
 * authorized trusted instrument/Science host with an actual focused result
 * from the SAME public contact. The Host supplies measurement evidence; this
 * API does not create world truth and does not classify blindly from catalogue.
 * Bio: 0 not tested, 1 no signal observed, 2 possible, 3 corroborated.
 * 3 requires a prior independent possible-biosignal report for this contact. */
enum F06PlanetClass { F06_PLANET_UNKNOWN=0,F06_PLANET_M=1,F06_PLANET_H=2,
 F06_PLANET_J=3,F06_PLANET_L=4,F06_PLANET_P=5,F06_PLANET_Y=6 };
enum F06ScienceStatus { F06_SCIENCE_QUEUED=1,F06_SCIENCE_COMPLETED=2 };
typedef struct {
 uint64_t expected_revision,request_key,handoff_id,focused_result_id,
  instrument_revision;
 uint32_t temperature_k,pressure_mbar,water_permille,
  nitrogen_permille,oxygen_permille,co2_permille,
  solid_surface,biological_evidence,quality_permille,reserved;
} F06ScienceSample;
typedef struct {
 uint64_t report_id,handoff_id,contact_id,focused_result_id,analyzed_at;
 uint32_t temperature_k,pressure_mbar,water_permille,
  nitrogen_permille,oxygen_permille,co2_permille,
  solid_surface,biological_evidence,quality_permille,
  confidence_permille,planet_class,provisional;
} F06ScienceReportView;
F04_API uint32_t f06_host_complete_science(F04Session*,const F06ScienceSample*,F06ScienceReportView*);
F04_API uint32_t f06_science_reports_page(F04Session*,F04Ref,uint64_t offset,
 F06ScienceReportView*,uint64_t capacity,uint64_t* written,uint64_t* total);

/* Approval is not a physical grant. Only the trusted Engineering/Operations
 * allocator can apply a real power change, after checking ship-wide budget.
 * One approved request may materialize ONE documented allocation. */
typedef struct {
 uint64_t expected_revision,request_id,allocator_revision;
 uint32_t new_total_power_permille,reserved;
} F06PowerApplication;
typedef struct {
 uint64_t request_id,allocator_revision,applied_at;
 uint32_t new_total_power_permille,applied;
} F06PowerApplicationView;
F04_API uint32_t f06_host_apply_power(F04Session*,const F06PowerApplication*,F06PowerApplicationView*);
F04_API uint32_t f06_power_application_status(F04Session*,F04Ref,uint64_t request_id,F06PowerApplicationView*);
#ifdef __cplusplus
}
#endif
