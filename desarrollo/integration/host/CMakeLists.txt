cmake_minimum_required(VERSION 3.25)
project(TrekHost LANGUAGES C CXX)

option(TREK_HOST_TESTS "Build native HOST tests" OFF)

# H02 adopts the F05 build and its candidate Core. F11 test and product
# targets are outside this build graph.
set(host_core_sha "76a7b7b485616d8c4994f384a90f123bf333591d")
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/../f05/core-revision.txt" f05_core_sha)
string(STRIP "${f05_core_sha}" f05_core_sha)
if(NOT f05_core_sha STREQUAL host_core_sha)
  message(FATAL_ERROR "H02 requires its reviewed F05 Core revision: ${host_core_sha}")
endif()

if(F11_ENABLE_PROMOTIONS OR TARGET TrekF11TrialHost OR TARGET TrekF04Bridge)
  message(FATAL_ERROR "H02 requires a standalone F05 composition without F11 targets or a preexisting bridge")
endif()
if(NOT CORERPG_SOURCE_DIR OR NOT IS_DIRECTORY "${CORERPG_SOURCE_DIR}")
  message(FATAL_ERROR "Set CORERPG_SOURCE_DIR to the exact clean CoreRPG checkout")
endif()
find_package(Git REQUIRED)
execute_process(
  COMMAND "${GIT_EXECUTABLE}" -C "${CORERPG_SOURCE_DIR}" rev-parse HEAD
  OUTPUT_VARIABLE core_head OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ERROR_IS_FATAL ANY)
execute_process(
  COMMAND "${GIT_EXECUTABLE}" -C "${CORERPG_SOURCE_DIR}" status --porcelain --untracked-files=all
  OUTPUT_VARIABLE core_dirty OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ERROR_IS_FATAL ANY)
if(NOT core_head STREQUAL host_core_sha OR NOT core_dirty STREQUAL "")
  message(FATAL_ERROR "H02 requires a clean Core checkout at ${host_core_sha} (found ${core_head})")
endif()

find_package(Threads REQUIRED)
if(TREK_HOST_TESTS)
  enable_testing()
  add_subdirectory(../f05 f05)
else()
  add_subdirectory(../f05 f05 EXCLUDE_FROM_ALL)
endif()

get_target_property(bridge_definitions TrekF04Bridge COMPILE_DEFINITIONS)
if(NOT F05_ENABLE_ORDERS OR NOT F04_ENABLE_HISTORY OR TARGET TrekF11TrialHost
   OR bridge_definitions MATCHES "(F11_ENABLE_PROMOTIONS|F11_NATIVE_TEST_HOST)")
  message(FATAL_ERROR "Unexpected H02 bridge flags or F11 trial target")
endif()
if(NOT TREK_HOST_TESTS)
  # Keep the inherited F04 history diagnostics only in test compositions.
  list(REMOVE_ITEM bridge_definitions F04_HISTORY_TESTING=1)
  set_property(TARGET TrekF04Bridge PROPERTY COMPILE_DEFINITIONS "${bridge_definitions}")
endif()
message(STATUS "H02 Core ${core_head}, TrekF04Bridge flags: ${bridge_definitions}")

# Extend the existing product adapter without editing historical source contracts.
# This replaces its sole translation unit; it does not compile another bridge or Core.
get_target_property(host_bridge_sources TrekF04Bridge SOURCES)
if(NOT host_bridge_sources STREQUAL "src/f04_bridge.cpp")
  message(FATAL_ERROR "Review unexpected bridge sources before composing H04")
endif()
set_property(TARGET TrekF04Bridge PROPERTY SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/../f04/src/f04_host_bridge.cpp")


set(host_sources src/session_owner.cpp src/native_session.cpp src/slot_store.cpp)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
get_filename_component(star_trek_root "${CMAKE_CURRENT_SOURCE_DIR}/../../.." ABSOLUTE)
set(f10_authoring "${star_trek_root}/sistemas/gameplay")
file(GLOB f10_species_profiles CONFIGURE_DEPENDS "${f10_authoring}/species/profiles/*_v0.1.json")
set(f10_rules_dir "${CMAKE_CURRENT_BINARY_DIR}/generated/f10")
set(f10_rules_header "${f10_rules_dir}/biography_rules_data.h")
add_custom_command(OUTPUT "${f10_rules_header}"
  COMMAND "${CMAKE_COMMAND}" -E make_directory "${f10_rules_dir}"
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/src/f10/embed_biography_rules.py"
    "${star_trek_root}" "${f10_rules_header}"
  DEPENDS src/f10/embed_biography_rules.py ${f10_species_profiles}
    "${f10_authoring}/character_creation/character_creation_contract_v1_0.json"
    "${f10_authoring}/character_creation/f10_biography_validation_interface_v0.1.json"
    "${f10_authoring}/character_creation/f10_biography_evidence_semantic_boundary_v0.1.json"
    "${f10_authoring}/character_creation/f10_initial_player_rules_v0.1.json"
    "${f10_authoring}/character_creation/f10_initial_background_policy_v0.1.json"
    "${f10_authoring}/character_creation/f10_species_maturity_policy_v0.1.json"
    "${f10_authoring}/character_creation/f10_openai_semantic_policy_v0.1.json"
    "${f10_authoring}/character_creation/biography_validation_rules.md"
    "${f10_authoring}/character_creation/prior_activity_model.json"
    "${f10_authoring}/character_creation/player_profile_contract.json"
    "${f10_authoring}/careers/academy_path/f10_host_candidate_factory_contract_v0.1.json"
    "${f10_authoring}/organizations/character_affiliation_citizenship_contract.json"
    "${f10_authoring}/species/species_biology_contract.json"
    "${f10_authoring}/ship_operations/era_technology_matrix.json"
  VERBATIM)
add_custom_target(host_f10_rules DEPENDS "${f10_rules_header}")
set(f10_sources src/f10/biography_validation.cpp src/f10/openai_biography.cpp)

# F10 v2 has its own reviewed authoring inputs and runtime validation policy.
set(f10_fixed_header "${f10_rules_dir}/fixed_candidate_data.h")
add_custom_command(OUTPUT "${f10_fixed_header}"
  COMMAND "${CMAKE_COMMAND}" -E make_directory "${f10_rules_dir}"
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/src/f10/embed_fixed_candidate.py"
    "${star_trek_root}" "${f10_fixed_header}"
  DEPENDS src/f10/embed_fixed_candidate.py
    "${f10_authoring}/careers/academy_path/f10_fixed_candidate_factory_contract_v2.json"
    "${f10_authoring}/character_creation/s04_fixed_protagonist_contract_v2.json"
    "${f10_authoring}/character_creation/s04_protagonist_biography_v1.json"
  VERBATIM)
add_custom_target(host_f10_fixed_data DEPENDS "${f10_fixed_header}")

add_library(host_academy_core STATIC src/f10/academy_campaign.cpp)
add_dependencies(host_academy_core host_f10_fixed_data)
target_include_directories(host_academy_core PRIVATE include "${f10_rules_dir}")
target_link_libraries(host_academy_core PUBLIC CoreRPG::CoreRPG PRIVATE jsoncons)
set_target_properties(host_academy_core PROPERTIES
  POSITION_INDEPENDENT_CODE ON CXX_VISIBILITY_PRESET hidden VISIBILITY_INLINES_HIDDEN YES)
if(MSVC)
  target_compile_options(host_academy_core PRIVATE /utf-8)
endif()

add_library(TrekHost SHARED ${host_sources} src/f04_session_bridge.cpp src/gateway_bridge.cpp src/host_abi.cpp
  ${f10_sources})
add_dependencies(TrekHost host_f10_rules)
target_compile_features(TrekHost PUBLIC cxx_std_20)
target_compile_definitions(TrekHost PRIVATE TREK_HOST_BUILD TREK_HOST_CORE_SHA="${host_core_sha}")
target_include_directories(TrekHost PUBLIC include PRIVATE "${f10_rules_dir}")
target_link_libraries(TrekHost PRIVATE TrekF04Bridge Threads::Threads host_academy_core jsoncons)
# The validator reuses Core's pure SHA-256 implementation. Keep archive
# symbols from the static Core library outside the shared HOST interface.
target_link_options(TrekHost PRIVATE "$<$<PLATFORM_ID:Linux>:LINKER:--exclude-libs,libCoreRPG.a>")
set_target_properties(TrekHost PROPERTIES
  CXX_VISIBILITY_PRESET hidden VISIBILITY_INLINES_HIDDEN YES WINDOWS_EXPORT_ALL_SYMBOLS NO)
# Both DLLs live beside the native consumer on Windows.
set_target_properties(TrekHost PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")

if(TREK_HOST_TESTS)
  add_executable(host_native_tests tests/native_tests.cpp tests/player_native_tests.cpp)
  target_include_directories(host_native_tests PRIVATE src)
  target_link_libraries(host_native_tests PRIVATE TrekHost TrekF04Bridge Threads::Threads ${CMAKE_DL_LIBS})
  target_compile_definitions(host_native_tests PRIVATE TREK_HOST_CORE_SHA="${host_core_sha}")
  set_target_properties(host_native_tests PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")
  foreach(case IN ITEMS hc01_open hc02_open_failure hc03_duplicate hc04_double_close
      hc05_thread_boundary reopen exclusive shutdown product_boundary)
    add_test(NAME host.native.${case} COMMAND host_native_tests ${case})
    set_tests_properties(host.native.${case} PROPERTIES TIMEOUT 30 LABELS "h02;native")
  endforeach()
  foreach(case IN ITEMS hi01_first_bind hi02_unbound hi03_client_boundary hi04_replay
      hi05_conflict hi06_foreign_campaign hi07_expired hi08_concurrent hi10_stale
      hi11_invalid_person hi12_revision hi13_reopen hi19_validation)
    add_test(NAME host.native.${case} COMMAND host_native_tests ${case})
    set_tests_properties(host.native.${case} PROPERTIES TIMEOUT 30 LABELS "h03;native")
  endforeach()

  # A separate executable replaces only the private bridge bindings to force
  # lifecycle failures. The product library and real bridge are not linked.
  add_executable(host_fault_tests tests/fault_tests.cpp tests/gateway_fault_bridge.cpp ${host_sources})
  target_compile_features(host_fault_tests PRIVATE cxx_std_20)
  target_include_directories(host_fault_tests PRIVATE src include ../f04/include ../f05/include)
  target_compile_definitions(host_fault_tests PRIVATE TREK_HOST_STATIC_TEST TREK_HOST_CORE_SHA="${host_core_sha}")
  target_link_libraries(host_fault_tests PRIVATE Threads::Threads host_academy_core)
  foreach(case IN ITEMS initialization hc06_incompatible_states pending failed_destroy failed_active_probe shutdown_retry)
    add_test(NAME host.fault.${case} COMMAND host_fault_tests ${case})
    set_tests_properties(host.fault.${case} PROPERTIES TIMEOUT 30 LABELS "h02;fault-injection")
  endforeach()
  foreach(case IN ITEMS hi09_close_during_bind hi11_bind_failure hi19_incompatible_core_binding)
    add_test(NAME host.fault.${case} COMMAND host_fault_tests ${case})
    set_tests_properties(host.fault.${case} PROPERTIES TIMEOUT 30 LABELS "h03;fault-injection")
  endforeach()
endif()

if(TREK_HOST_TESTS)
  # Real bridge and product sources; failpoints exist only in this separate test executable.
  add_executable(host_persistence_tests tests/persistence_tests.cpp ${host_sources} src/f04_session_bridge.cpp src/gateway_bridge.cpp)
  target_compile_features(host_persistence_tests PRIVATE cxx_std_20)
  target_include_directories(host_persistence_tests PRIVATE src include)
  target_compile_definitions(host_persistence_tests PRIVATE TREK_HOST_STATIC_TEST TREK_HOST_PERSISTENCE_TESTING TREK_HOST_CORE_SHA="${host_core_sha}")
  target_link_libraries(host_persistence_tests PRIVATE TrekF04Bridge Threads::Threads host_academy_core)
  set_target_properties(host_persistence_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")
  foreach(case IN ITEMS roundtrip reader history_rng paths failures io queue double late renewal_failure busy save_close load_close manifest incompatible
      identity import truncated altered incomplete absent_binding wrong_binding foreign_core)
    add_test(NAME host.persistence.${case} COMMAND host_persistence_tests ${case} "${CMAKE_CURRENT_BINARY_DIR}/persistence/${case}")
    set_tests_properties(host.persistence.${case} PROPERTIES TIMEOUT 45 LABELS "h04;native")
  endforeach()
  add_test(NAME host.persistence.process COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tests/persistence_process.py"
    "$<TARGET_FILE:host_persistence_tests>" "${CMAKE_CURRENT_BINARY_DIR}/persistence/process")
  set_tests_properties(host.persistence.process PROPERTIES TIMEOUT 240 LABELS "h04;process;fault-injection")
endif()

if(TREK_HOST_TESTS)
  add_executable(host_biography_tests tests/biography_tests.cpp ${f10_sources})
  add_dependencies(host_biography_tests host_f10_rules)
  target_include_directories(host_biography_tests PRIVATE src "${f10_rules_dir}")
  target_link_libraries(host_biography_tests PRIVATE CoreRPG::CoreRPG jsoncons)
  target_compile_definitions(host_biography_tests PRIVATE TREK_F10_BIOGRAPHY_TESTING)
  foreach(case IN ITEMS production fields species playable_age maturity_dates restricted_species
      chronology evidence context malformed conjunction review
      stale evidence_stale registered_sources evidence_conflicts evidence_policy
      personal_background background_boundaries background_provenance failure privacy)
    add_test(NAME host.biography.${case} COMMAND host_biography_tests ${case})
    set_tests_properties(host.biography.${case} PROPERTIES TIMEOUT 20 LABELS "f10;h06-p06-a;native")
  endforeach()
  add_test(NAME host.biography.rules_generation
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tests/biography_rules_generation.py"
      "${star_trek_root}")
  set_tests_properties(host.biography.rules_generation PROPERTIES TIMEOUT 30 LABELS "f10;h06-p06-a")
endif()

if(TREK_HOST_TESTS)
  # Same product sources/real bridge; privileged fixture access is compiled only here.
  add_executable(host_m0_tests tests/m0_tests.cpp ${host_sources} src/f04_session_bridge.cpp src/gateway_bridge.cpp)
  target_compile_features(host_m0_tests PRIVATE cxx_std_20)
  target_include_directories(host_m0_tests PRIVATE src tests include)
  target_compile_definitions(host_m0_tests PRIVATE TREK_HOST_STATIC_TEST TREK_HOST_GATEWAY_TESTING TREK_HOST_PERSISTENCE_TESTING TREK_HOST_CORE_SHA="${host_core_sha}")
  target_link_libraries(host_m0_tests PRIVATE TrekF04Bridge host_academy_core Threads::Threads)
  set_target_properties(host_m0_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")
  foreach(case IN ITEMS bound readonly submit execute replay conflict stale unbound resolving scope authority recipient unsupported
      expired saving loading save_order close_order unknown observer institutional recover pending cancel concurrent)
    add_test(NAME host.m0.${case} COMMAND host_m0_tests ${case} "${CMAKE_CURRENT_BINARY_DIR}/m0/${case}")
    set_tests_properties(host.m0.${case} PROPERTIES TIMEOUT 120 LABELS "h05;native")
  endforeach()
  add_test(NAME host.m0.process COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tests/m0_process.py"
    "$<TARGET_FILE:host_m0_tests>" "${CMAKE_CURRENT_BINARY_DIR}/m0/process")
  set_tests_properties(host.m0.process PROPERTIES TIMEOUT 240 LABELS "h05;process")
endif()

if(TREK_HOST_TESTS)
  add_executable(host_abi_tests tests/host_abi_tests.c)
  set_target_properties(host_abi_tests PROPERTIES C_STANDARD 11 C_STANDARD_REQUIRED YES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")
  target_link_libraries(host_abi_tests PRIVATE TrekHost)
  add_test(NAME host.abi.lifecycle COMMAND host_abi_tests)
  add_test(NAME host.abi.roundtrip COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tests/abi_fixture.py"
    "$<TARGET_FILE:host_m0_tests>" "$<TARGET_FILE:host_abi_tests>" "${CMAKE_CURRENT_BINARY_DIR}/abi")
  set_tests_properties(host.abi.lifecycle PROPERTIES TIMEOUT 45 LABELS "h06;native")
  add_test(NAME host.abi.unsupported_academy_open COMMAND host_abi_tests unsupported_academy_open)
  set_tests_properties(host.abi.unsupported_academy_open PROPERTIES TIMEOUT 45 LABELS "h06-p06;native")
  set_tests_properties(host.abi.roundtrip PROPERTIES TIMEOUT 135 LABELS "h06;native;fixture")
endif()

if(TREK_HOST_TESTS)
  # F10/P06 feasibility only. The fixture has no product BIO review or HOST admission path.
  add_executable(host_academy_feasibility_tests tests/academy_core_feasibility.cpp)
  target_link_libraries(host_academy_feasibility_tests PRIVATE CoreRPG::CoreRPG)
  add_test(NAME host.academy.core_feasibility
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tests/academy_core_feasibility.py"
      "$<TARGET_FILE:host_academy_feasibility_tests>" "${CMAKE_CURRENT_BINARY_DIR}/academy-feasibility")
  set_tests_properties(host.academy.core_feasibility PROPERTIES TIMEOUT 75 LABELS "f10;h06-p06;process;feasibility")
endif()

# IA-01: one common provider service within the existing HOST; no Core API dependency.
set(host_ai_sources src/ai/service.cpp src/ai/credentials.cpp src/ai/https.cpp)
target_sources(TrekHost PRIVATE ${host_ai_sources})
if(WIN32)
  set(host_ai_platform_libraries winhttp advapi32)
else()
  find_package(PkgConfig REQUIRED)
  pkg_check_modules(HOST_CURL REQUIRED IMPORTED_TARGET libcurl>=7.85)
  set(host_ai_platform_libraries PkgConfig::HOST_CURL)
endif()
target_link_libraries(TrekHost PRIVATE ${host_ai_platform_libraries})
if(TREK_HOST_TESTS)
  add_executable(host_ai_tests tests/ai_tests.cpp ${host_ai_sources})
  target_compile_features(host_ai_tests PRIVATE cxx_std_20)
  target_compile_definitions(host_ai_tests PRIVATE TREK_HOST_STATIC_TEST)
  target_include_directories(host_ai_tests PRIVATE include)
  target_link_libraries(host_ai_tests PRIVATE jsoncons Threads::Threads ${host_ai_platform_libraries})
  add_test(NAME host.ai.offline COMMAND host_ai_tests "${CMAKE_CURRENT_BINARY_DIR}/ai-config-test.json")
  set_tests_properties(host.ai.offline PROPERTIES TIMEOUT 30 LABELS "h06;ia01;native")
  # Explicit opt-in only, never registered in CTest/CI.
  add_executable(host_ai_smoke EXCLUDE_FROM_ALL tests/ai_smoke.cpp)
  target_link_libraries(host_ai_smoke PRIVATE TrekHost)
endif()

if(TREK_HOST_TESTS)
  target_sources(host_biography_tests PRIVATE ${host_ai_sources})
  target_include_directories(host_biography_tests PRIVATE include)
  target_compile_definitions(host_biography_tests PRIVATE TREK_HOST_STATIC_TEST)
  target_link_libraries(host_biography_tests PRIVATE Threads::Threads ${host_ai_platform_libraries})
  # Product F10 sources, without TREK_F10_BIOGRAPHY_TESTING or receipt test access.
  add_executable(host_biography_ai_tests tests/biography_ai_tests.cpp ${f10_sources} ${host_ai_sources})
  add_dependencies(host_biography_ai_tests host_f10_rules)
  target_compile_features(host_biography_ai_tests PRIVATE cxx_std_20)
  target_compile_definitions(host_biography_ai_tests PRIVATE TREK_HOST_STATIC_TEST)
  target_include_directories(host_biography_ai_tests PRIVATE src include "${f10_rules_dir}")
  target_link_libraries(host_biography_ai_tests PRIVATE CoreRPG::CoreRPG jsoncons Threads::Threads ${host_ai_platform_libraries})
  add_test(NAME host.biography.openai COMMAND host_biography_ai_tests)
  set_tests_properties(host.biography.openai PROPERTIES TIMEOUT 30 LABELS "f10;ia02;native")
endif()

if(MSVC)
  target_compile_options(TrekHost PRIVATE /utf-8)
  if(TREK_HOST_TESTS)
    target_compile_options(host_biography_tests PRIVATE /utf-8)
    target_compile_options(host_biography_ai_tests PRIVATE /utf-8)
  endif()
endif()

if(TREK_HOST_TESTS)
  # Production constructors and genuine HOST profile; only HTTPS is simulated.
  add_executable(host_initial_biography_tests tests/initial_biography_tests.cpp
    ${host_sources} src/f04_session_bridge.cpp src/gateway_bridge.cpp ${f10_sources} ${host_ai_sources})
  add_dependencies(host_initial_biography_tests host_f10_rules)
  target_compile_features(host_initial_biography_tests PRIVATE cxx_std_20)
  target_compile_definitions(host_initial_biography_tests PRIVATE TREK_HOST_STATIC_TEST TREK_HOST_CORE_SHA="${host_core_sha}")
  target_include_directories(host_initial_biography_tests PRIVATE src include "${f10_rules_dir}")
  target_link_libraries(host_initial_biography_tests PRIVATE TrekF04Bridge host_academy_core jsoncons Threads::Threads ${host_ai_platform_libraries})
  set_target_properties(host_initial_biography_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")
  if(MSVC)
    target_compile_options(host_initial_biography_tests PRIVATE /utf-8)
  endif()
  add_test(NAME host.biography.initial_player COMMAND host_initial_biography_tests)
  set_tests_properties(host.biography.initial_player PROPERTIES TIMEOUT 45 LABELS "f10;ia03a;h03;native")
endif()

if(TREK_HOST_TESTS)
  # Acceptance runs through the product DLL. A separate composition of the same
  # native sources injects source and staging failures without product hooks.
  add_executable(host_academy_candidate_tests tests/academy_candidate_tests.cpp)
  target_include_directories(host_academy_candidate_tests PRIVATE src)
  target_link_libraries(host_academy_candidate_tests PRIVATE TrekHost TrekF04Bridge Threads::Threads)

  add_executable(host_academy_player_tests tests/academy_player_tests.cpp)
  target_include_directories(host_academy_player_tests PRIVATE src)
  target_link_libraries(host_academy_player_tests PRIVATE TrekHost TrekF04Bridge Threads::Threads)

  add_library(host_academy_fault_runtime STATIC
    ${host_sources} src/f10/academy_campaign.cpp src/f04_session_bridge.cpp src/gateway_bridge.cpp)
  add_dependencies(host_academy_fault_runtime host_f10_fixed_data)
  target_compile_features(host_academy_fault_runtime PUBLIC cxx_std_20)
  target_compile_definitions(host_academy_fault_runtime PUBLIC TREK_HOST_STATIC_TEST TREK_HOST_ACADEMY_TESTING
    PRIVATE TREK_HOST_CORE_SHA="${host_core_sha}")
  target_include_directories(host_academy_fault_runtime PUBLIC src include PRIVATE "${f10_rules_dir}")
  target_link_libraries(host_academy_fault_runtime PUBLIC TrekF04Bridge CoreRPG::CoreRPG PRIVATE jsoncons Threads::Threads)

  add_executable(host_academy_candidate_faults tests/academy_candidate_tests.cpp)
  target_link_libraries(host_academy_candidate_faults PRIVATE host_academy_fault_runtime)
  add_executable(host_academy_player_faults tests/academy_player_tests.cpp)
  target_link_libraries(host_academy_player_faults PRIVATE host_academy_fault_runtime)

  set_target_properties(host_academy_candidate_tests host_academy_candidate_faults
    host_academy_player_tests host_academy_player_faults PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")
  if(MSVC)
    target_compile_options(host_academy_candidate_tests PRIVATE /utf-8)
    target_compile_options(host_academy_candidate_faults PRIVATE /utf-8)
    target_compile_options(host_academy_fault_runtime PRIVATE /utf-8)
  endif()
  foreach(case IN ITEMS b02_01 b02_02 b02_03 b02_04 b02_05 b02_06 b02_08 b02_09 b02_10 b02_11 b02_13 b02_15)
    add_test(NAME host.academy.${case} COMMAND host_academy_candidate_tests ${case})
    set_tests_properties(host.academy.${case} PROPERTIES TIMEOUT 30 LABELS "f10;ia03b02;native")
  endforeach()
  foreach(case IN ITEMS b02_07 b02_11_legacy b02_12)
    add_test(NAME host.academy.${case} COMMAND host_academy_candidate_faults ${case})
    set_tests_properties(host.academy.${case} PROPERTIES TIMEOUT 30 LABELS "f10;ia03b02;fault-injection")
  endforeach()
  foreach(case IN ITEMS b03t_01 b03t_02 b03t_03a b03t_03b b03t_03d b03t_03e)
    add_test(NAME host.academy.${case} COMMAND host_academy_player_tests ${case})
    set_tests_properties(host.academy.${case} PROPERTIES TIMEOUT 30 LABELS "h03;ia03b03-02;native")
  endforeach()
  foreach(case IN ITEMS b03t_03c b03t_bind_retry)
    add_test(NAME host.academy.${case} COMMAND host_academy_player_faults ${case})
    set_tests_properties(host.academy.${case} PROPERTIES TIMEOUT 30 LABELS "h03;ia03b03-02;fault-injection")
  endforeach()
endif()
