#pragma once
#include "f04_bridge.h"
#include <array>
#include <span>

namespace trek_templates {
// Immutable domain definitions, never a second store of people or assignments.
// Append profiles to this registry when their equipment/organization is approved.
inline constexpr F04TemplateSpec sutherland{F04_SUTHERLAND_SCIENCE,130,0,
 F04_SUTHERLAND_EQUIPMENT,"miranda","sutherland_science_multirole_modernized",
 "science_multirole","configurable"};
inline constexpr std::array<F04SectionSpec,32> sections{{
 {1,F04_COMMAND,1,1,F04_COMMAND,F04_ST_COMMAND,F04_DAY_ACTIVITY,"Capitán","Mando de la nave","Puente"},
 {2,F04_COMMAND,1,1,F04_COMMAND,F04_ST_COMMAND,F04_DAY_ACTIVITY,"Primer oficial","Segundo al mando; coordinación operativa y supervisión departamental","Puente"},
 {3,F04_COMMAND,3,1,F04_COMMAND,F04_ST_COMMAND,F04_CONTINUOUS_CANDIDATE,"Oficiales de guardia y mando","Supervisión rutinaria; relevos y mando delegado","Puente"},
 {4,F04_COMMAND,5,2,F04_Q_HELM,F04_ST_HELM,F04_CONTINUOUS_CANDIDATE,"Timón y navegación","Pilotaje de nave principal y navegación","Timón del puente"},
 {5,F04_COMMAND,2,1,F04_Q_MISSION,F04_ST_COMMAND,F04_DAY_ACTIVITY,"Coordinación de misiones","Planificación y seguimiento operativo","Puente y comunicaciones"},
 {6,F04_ENGINEERING,2,1,F04_ENGINEERING,F04_ST_ENGINEERING,F04_CONTINUOUS_CANDIDATE,"Jefe de ingeniería y adjunto","Dirección técnica y prioridades de mantenimiento","Ingeniería"},
 {7,F04_ENGINEERING,8,3,F04_Q_PROPULSION,F04_ST_ENGINEERING,F04_DAY_ACTIVITY,"Motores warp e impulso","Mantenimiento de propulsión","Propulsión warp e impulso"},
 {8,F04_ENGINEERING,6,2,F04_Q_POWER,F04_ST_ENGINEERING,F04_DAY_ACTIVITY,"Reactor y distribución de energía","Generación y distribución de energía","Reactor y red energética"},
 {9,F04_ENGINEERING,7,2,F04_Q_LIFE_SUPPORT,F04_ST_ENGINEERING,F04_DAY_ACTIVITY,"Soporte vital e integridad estructural","Sistemas ambientales y estructurales","Soporte vital y estructura"},
 {10,F04_ENGINEERING,9,3,F04_Q_REPAIR,F04_ST_ENGINEERING,F04_DAY_ACTIVITY,"Reparaciones y mantenimiento general","Reparación técnica de sistemas de otros departamentos, sin asumir su operación","Equipamiento instalado"},
 {11,F04_SENSORS,2,1,F04_SENSORS,F04_ST_SENSORS|F04_ST_LAB,F04_DAY_ACTIVITY,"Jefe científico y adjunto","Dirección científica","Sensores modernizados y laboratorios polivalentes"},
 {12,F04_SENSORS,8,3,F04_SENSORS,F04_ST_SENSORS,F04_CONTINUOUS_CANDIDATE,"Sensores y astrometría","Operación y análisis de sensores; astrometría","Sensores modernizados"},
 {13,F04_SENSORS,6,3,F04_Q_PHYSICS,F04_ST_LAB,F04_DAY_ACTIVITY,"Física y astrofísica","Investigación física y astronómica","Laboratorios polivalentes"},
 {14,F04_SENSORS,5,2,F04_Q_BIOLOGY,F04_ST_LAB,F04_DAY_ACTIVITY,"Biología y xenobiología","Estudios biológicos","Laboratorios polivalentes"},
 {15,F04_SENSORS,4,2,F04_Q_GEOLOGY,F04_ST_LAB,F04_DAY_ACTIVITY,"Geología y planetología","Estudios geológicos y planetarios","Laboratorios polivalentes"},
 {16,F04_SENSORS,5,3,F04_Q_LAB,F04_ST_LAB,F04_DAY_ACTIVITY,"Laboratorios y análisis de muestras","Análisis instrumental y de muestras","Laboratorios polivalentes"},
 {17,F04_OPERATIONS,2,1,F04_OPERATIONS,F04_ST_COMPUTER,F04_DAY_ACTIVITY,"Jefe de operaciones y adjunto","Coordinación operativa","Comunicaciones, transportadores y sistemas informáticos"},
 {18,F04_OPERATIONS,5,2,F04_Q_COMMUNICATIONS,F04_ST_COMMUNICATIONS,F04_CONTINUOUS_CANDIDATE,"Comunicaciones","Operación de comunicaciones","Sistemas de comunicaciones"},
 {19,F04_OPERATIONS,5,1,F04_Q_TRANSPORTER,F04_ST_TRANSPORTER,F04_DAY_ACTIVITY,"Transportadores","Operación; reparación técnica a cargo de personal habilitado de mantenimiento","Transportadores"},
 {20,F04_OPERATIONS,6,2,F04_Q_COMPUTING,F04_ST_COMPUTER,F04_DAY_ACTIVITY,"Sistemas informáticos y recursos","Sistemas informáticos y asignación de recursos","Sistemas informáticos"},
 {21,F04_SECURITY,2,1,F04_SECURITY,F04_ST_TACTICAL|F04_ST_SECURITY,F04_CONTINUOUS_CANDIDATE,"Jefe de seguridad y adjunto","Dirección de seguridad y táctica; consola táctica si está habilitado","Fáseres, torpedos, escudos y seguridad"},
 {22,F04_SECURITY,5,1,F04_Q_TACTICAL,F04_ST_TACTICAL,F04_CONTINUOUS_CANDIDATE,"Especialistas tácticos","Operación táctica; apoyo o relevo del jefe de servicio","Fáseres y torpedos en barra superior; escudos"},
 {23,F04_SECURITY,6,2,F04_Q_INTERIOR_SECURITY,F04_ST_SECURITY,F04_DAY_ACTIVITY,"Seguridad interior","Protección interior","Instalaciones de seguridad"},
 {24,F04_SECURITY,3,1,F04_Q_EMERGENCY,F04_ST_SECURITY,F04_DAY_ACTIVITY,"Respuesta a emergencias y abordajes","Intervención en emergencias y abordajes","Instalaciones de seguridad"},
 {25,F04_LOGISTICS,1,1,F04_LOGISTICS,F04_ST_HANGAR|F04_ST_CARGO,F04_DAY_ACTIVITY,"Jefe de sección","Coordinación de servicios auxiliares","Hangares posteriores y almacenes"},
 {26,F04_LOGISTICS,3,1,F04_Q_SHUTTLE,F04_ST_HANGAR,F04_DAY_ACTIVITY,"Pilotos de lanzaderas","Pilotaje de lanzaderas, distinto del pilotaje de nave principal","Lanzaderas; número configurable"},
 {27,F04_LOGISTICS,4,2,F04_Q_HANGAR,F04_ST_HANGAR,F04_DAY_ACTIVITY,"Hangares y mantenimiento","Preparación y mantenimiento de hangares y naves auxiliares","Hangares posteriores y lanzaderas"},
 {28,F04_LOGISTICS,4,2,F04_Q_CARGO,F04_ST_CARGO,F04_DAY_ACTIVITY,"Suministros, almacenes y carga","Inventarios, suministros y carga","Almacenes y espacios habitables"},
 {29,F04_MEDICINE,1,1,F04_MEDICINE,F04_ST_MEDICAL,F04_URGENT_PENDING,"Médico jefe","Dirección sanitaria; no mando general de la nave","Enfermería"},
 {30,F04_MEDICINE,2,1,F04_Q_CLINICAL,F04_ST_MEDICAL,F04_URGENT_PENDING,"Médicos","Atención clínica","Enfermería"},
 {31,F04_MEDICINE,5,2,F04_Q_NURSING,F04_ST_MEDICAL,F04_URGENT_PENDING,"Enfermería","Cuidados de enfermería","Enfermería"},
 {32,F04_MEDICINE,2,1,F04_Q_DIAGNOSTICS,F04_ST_MEDICAL,F04_URGENT_PENDING,"Técnicos sanitarios y diagnóstico","Diagnóstico y asistencia técnica sanitaria","Enfermería"}
}};
inline uint64_t responsibility(uint64_t section_id,uint64_t ordinal) {
 if(section_id==1)return F04_CAPTAIN;
 if(section_id==2)return F04_FIRST;
 if(section_id==29)return F04_DOCTOR;
 if(section_id==6 || section_id==11 || section_id==17 || section_id==21)
  return ordinal==1?F04_HEAD:F04_DEPUTY;
 if(section_id==25)return F04_HEAD;
 return 0;
}
inline uint64_t qualifications(const F04SectionSpec& s) {
 uint64_t mask=1ULL<<s.qualification;
 if(s.id==12)mask|=1ULL<<F04_Q_ASTROMETRY;
 if(s.id==21)mask|=1ULL<<F04_Q_TACTICAL;
 if(s.id==29)mask|=1ULL<<F04_Q_CLINICAL;
 return mask;
}
// The engine consumes this interface; section IDs and staffing rules belong to
// each profile. Future classes supply their own tables/callbacks and coverage.
struct Profile {
 const F04TemplateSpec& spec;
 std::span<const F04SectionSpec> sections;
 uint64_t (*qualification_mask)(const F04SectionSpec&);
 uint64_t (*post_responsibility)(uint64_t,uint64_t);
 std::span<const uint64_t> continuous_stations;
};
inline constexpr uint64_t sutherland_continuous[]={F04_ST_COMMAND,F04_ST_HELM,
 F04_ST_SENSORS,F04_ST_COMMUNICATIONS,F04_ST_ENGINEERING,F04_ST_TACTICAL};

// Intrepid owns its section IDs; no Miranda table or staffing is changed.
inline constexpr F04TemplateSpec intrepid{F04_INTREPID_EXPLORATION,160,0,
 F04_INTREPID_EQUIPMENT,"intrepid","intrepid_long_range_exploration",
 "science_exploration_patrol_independent","post_nemesis"};
inline constexpr std::array<F04SectionSpec,34> intrepid_sections{{
 {1,F04_COMMAND,1,1,F04_COMMAND,F04_ST_COMMAND,F04_DAY_ACTIVITY,"Capitán","Mando de la nave","Puente"},
 {2,F04_COMMAND,1,1,F04_COMMAND,F04_ST_COMMAND,F04_DAY_ACTIVITY,"Primer oficial","Segundo al mando; coordinación operativa y supervisión departamental","Puente"},
 {3,F04_COMMAND,4,1,F04_COMMAND,F04_ST_COMMAND,F04_CONTINUOUS_CANDIDATE,"Oficiales de guardia y mando","Supervisión rutinaria; relevos y mando delegado","Puente"},
 {4,F04_COMMAND,7,3,F04_Q_HELM,F04_ST_HELM,F04_CONTINUOUS_CANDIDATE,"Timón y navegación","Pilotaje de nave principal y navegación","Timón del puente"},
 {5,F04_COMMAND,3,1,F04_Q_MISSION,F04_ST_COMMAND,F04_DAY_ACTIVITY,"Coordinación de misiones","Planificación y seguimiento operativo","Puente y comunicaciones"},
 {6,F04_ENGINEERING,2,1,F04_ENGINEERING,F04_ST_ENGINEERING,F04_CONTINUOUS_CANDIDATE,"Jefe de ingeniería y adjunto","Dirección técnica y prioridades de mantenimiento","Ingeniería"},
 {7,F04_ENGINEERING,9,3,F04_Q_PROPULSION,F04_ST_ENGINEERING,F04_DAY_ACTIVITY,"Motores warp, impulso y geometría variable","Propulsión y mecanismos de barquillas de geometría variable","Propulsión warp e impulso"},
 {8,F04_ENGINEERING,8,3,F04_Q_POWER,F04_ST_ENGINEERING,F04_DAY_ACTIVITY,"Núcleo warp y distribución energética","Generación y distribución de energía","Reactor y red energética"},
 {9,F04_ENGINEERING,6,2,F04_Q_LIFE_SUPPORT,F04_ST_ENGINEERING,F04_DAY_ACTIVITY,"Soporte vital e integridad estructural","Sistemas ambientales y estructurales","Soporte vital y estructura"},
 {10,F04_ENGINEERING,7,3,F04_Q_REPAIR,F04_ST_ENGINEERING,F04_DAY_ACTIVITY,"Reparaciones y mantenimiento general","Reparación técnica de sistemas de otros departamentos, sin asumir su operación","Equipamiento instalado"},
 {11,F04_ENGINEERING,4,1,F04_Q_REPAIR,F04_ST_ENGINEERING,F04_DAY_ACTIVITY,"Deflectores y emisores técnicos","Reparación técnica; operación científica separada","Deflectores y emisores"},
 {12,F04_SENSORS,2,1,F04_SENSORS,F04_ST_SENSORS|F04_ST_LAB,F04_DAY_ACTIVITY,"Jefe científico y adjunto","Dirección científica","Sensores y laboratorios; configuración de nave"},
 {13,F04_SENSORS,10,4,F04_SENSORS,F04_ST_SENSORS,F04_CONTINUOUS_CANDIDATE,"Sensores y astrometría","Operación y análisis de sensores; astrometría","Sensores y astrometría estándar; modificaciones opcionales"},
 {14,F04_SENSORS,7,3,F04_Q_PHYSICS,F04_ST_LAB,F04_DAY_ACTIVITY,"Física y astrofísica","Investigación física y astronómica","Laboratorios polivalentes"},
 {15,F04_SENSORS,6,2,F04_Q_BIOLOGY,F04_ST_LAB,F04_DAY_ACTIVITY,"Biología y xenobiología","Estudios biológicos","Laboratorios polivalentes"},
 {16,F04_SENSORS,4,2,F04_Q_GEOLOGY,F04_ST_LAB,F04_DAY_ACTIVITY,"Geología y planetología","Estudios geológicos y planetarios","Laboratorios polivalentes"},
 {17,F04_SENSORS,5,2,F04_Q_LAB,F04_ST_LAB,F04_DAY_ACTIVITY,"Laboratorios y datos científicos","Análisis instrumental y de muestras","Laboratorios polivalentes"},
 {18,F04_OPERATIONS,2,1,F04_OPERATIONS,F04_ST_COMPUTER,F04_DAY_ACTIVITY,"Jefe de operaciones y adjunto","Coordinación operativa","Comunicaciones, transportadores y sistemas informáticos"},
 {19,F04_OPERATIONS,6,2,F04_Q_COMMUNICATIONS,F04_ST_COMMUNICATIONS,F04_CONTINUOUS_CANDIDATE,"Comunicaciones","Operación de comunicaciones","Sistemas de comunicaciones"},
 {20,F04_OPERATIONS,6,2,F04_Q_TRANSPORTER,F04_ST_TRANSPORTER,F04_DAY_ACTIVITY,"Transportadores","Operación; reparación técnica a cargo de personal habilitado de mantenimiento","Transportadores"},
 {21,F04_OPERATIONS,7,3,F04_Q_COMPUTING,F04_ST_COMPUTER,F04_DAY_ACTIVITY,"Sistemas bioneurales y ordenadores","Administración y diagnóstico bioneural; coordinación técnica con Ingeniería","Ordenadores y paquetes bioneurales"},
 {22,F04_OPERATIONS,4,2,F04_OPERATIONS,F04_ST_COMPUTER,F04_DAY_ACTIVITY,"Coordinación de recursos y holocubiertas","Reservas y prioridades de recursos; instalaciones lógicas configurables","Recursos y holocubiertas; contrato mínimo sin 3D"},
 {23,F04_SECURITY,2,1,F04_SECURITY,F04_ST_TACTICAL|F04_ST_SECURITY,F04_CONTINUOUS_CANDIDATE,"Jefe de seguridad y adjunto","Dirección de seguridad y táctica; consola táctica si está habilitado","Fáseres, torpedos, escudos y seguridad"},
 {24,F04_SECURITY,5,2,F04_Q_TACTICAL,F04_ST_TACTICAL,F04_CONTINUOUS_CANDIDATE,"Especialistas tácticos","Operación táctica; apoyo o relevo del jefe de servicio","Matrices fáser, lanzadores de torpedos integrados en el casco y escudos"},
 {25,F04_SECURITY,8,3,F04_Q_INTERIOR_SECURITY,F04_ST_SECURITY,F04_DAY_ACTIVITY,"Seguridad interior","Protección interior","Instalaciones de seguridad"},
 {26,F04_SECURITY,3,1,F04_Q_EMERGENCY,F04_ST_SECURITY,F04_DAY_ACTIVITY,"Respuesta a emergencias y abordajes","Intervención en emergencias y abordajes","Instalaciones de seguridad"},
 {27,F04_LOGISTICS,1,1,F04_LOGISTICS,F04_ST_HANGAR|F04_ST_CARGO,F04_DAY_ACTIVITY,"Jefe de sección","Coordinación de servicios auxiliares","Hangares posteriores y almacenes"},
 {28,F04_LOGISTICS,4,2,F04_Q_SHUTTLE,F04_ST_HANGAR,F04_DAY_ACTIVITY,"Pilotos de lanzaderas","Pilotaje de lanzaderas, distinto del pilotaje de nave principal","Lanzaderas; número configurable"},
 {29,F04_LOGISTICS,7,2,F04_Q_HANGAR,F04_ST_HANGAR,F04_DAY_ACTIVITY,"Hangares y mantenimiento","Preparación y mantenimiento de hangares y naves auxiliares","Hangares posteriores y lanzaderas"},
 {30,F04_LOGISTICS,5,2,F04_Q_CARGO,F04_ST_CARGO,F04_DAY_ACTIVITY,"Suministros, almacenes y carga","Inventarios, suministros y carga","Almacenes y espacios habitables"},
 {31,F04_MEDICINE,1,1,F04_MEDICINE,F04_ST_MEDICAL,F04_URGENT_PENDING,"Médico jefe","Dirección sanitaria; no mando general de la nave","Enfermería"},
 {32,F04_MEDICINE,3,1,F04_Q_CLINICAL,F04_ST_MEDICAL,F04_URGENT_PENDING,"Médicos","Atención clínica","Enfermería"},
 {33,F04_MEDICINE,7,3,F04_Q_NURSING,F04_ST_MEDICAL,F04_URGENT_PENDING,"Enfermería","Cuidados de enfermería","Enfermería"},
 {34,F04_MEDICINE,3,1,F04_Q_DIAGNOSTICS,F04_ST_MEDICAL,F04_URGENT_PENDING,"Técnicos sanitarios, diagnóstico y soporte EMH","Diagnóstico, equipos médicos y soporte operativo EMH; EMH no es tripulante","Enfermería"}
}};
inline uint64_t intrepid_responsibility(uint64_t section_id,uint64_t ordinal) {
 if(section_id==1)return F04_CAPTAIN;
 if(section_id==2)return F04_FIRST;
 if(section_id==31)return F04_DOCTOR;
 if(section_id==6 || section_id==12 || section_id==18 || section_id==23)
  return ordinal==1?F04_HEAD:F04_DEPUTY;
 if(section_id==27)return F04_HEAD;
 return 0;
}
inline uint64_t intrepid_qualifications(const F04SectionSpec& s) {
 uint64_t mask=1ULL<<s.qualification;
 if(s.id==13)mask|=1ULL<<F04_Q_ASTROMETRY;
 if(s.id==23)mask|=1ULL<<F04_Q_TACTICAL;
 if(s.id==31)mask|=1ULL<<F04_Q_CLINICAL;
 return mask;
}
// Operations and communications are checked independently for this profile.
inline constexpr uint64_t intrepid_continuous[]={F04_ST_COMMAND,F04_ST_HELM,
 F04_ST_SENSORS,F04_ST_COMPUTER,F04_ST_COMMUNICATIONS,F04_ST_ENGINEERING,F04_ST_TACTICAL};

inline const Profile* profile(uint64_t id) {
 static const Profile registry[]={{sutherland,sections,qualifications,responsibility,sutherland_continuous},
  {intrepid,intrepid_sections,intrepid_qualifications,intrepid_responsibility,intrepid_continuous}};
 for(const auto& p:registry)if(p.spec.id==id)return &p;
 return nullptr;
}
inline const F04TemplateSpec* find(uint64_t id) {const auto* p=profile(id);return p?&p->spec:nullptr;}
inline const F04SectionSpec* section(const Profile& p,uint64_t id) {
 for(const auto& s:p.sections)if(s.id==id)return &s;
 return nullptr;
}
}
