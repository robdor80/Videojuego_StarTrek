cmake_minimum_required(VERSION 3.25)
project(TrekHost LANGUAGES CXX)

option(TREK_HOST_TESTS "Build H02 lifecycle tests" OFF)

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
message(STATUS "H02 Core ${core_head}, TrekF04Bridge flags: ${bridge_definitions}")

set(host_sources src/session_owner.cpp src/native_session.cpp)
add_library(TrekHost SHARED ${host_sources} src/f04_session_bridge.cpp)
target_compile_features(TrekHost PUBLIC cxx_std_20)
target_compile_definitions(TrekHost PRIVATE TREK_HOST_BUILD TREK_HOST_CORE_SHA="${host_core_sha}")
target_include_directories(TrekHost PUBLIC include)
target_link_libraries(TrekHost PRIVATE TrekF04Bridge Threads::Threads)
set_target_properties(TrekHost PROPERTIES
  CXX_VISIBILITY_PRESET hidden VISIBILITY_INLINES_HIDDEN YES WINDOWS_EXPORT_ALL_SYMBOLS NO)
# Both DLLs live beside the native consumer on Windows.
set_target_properties(TrekHost PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")

if(TREK_HOST_TESTS)
  add_executable(host_native_tests tests/native_tests.cpp)
  target_link_libraries(host_native_tests PRIVATE TrekHost TrekF04Bridge Threads::Threads ${CMAKE_DL_LIBS})
  target_compile_definitions(host_native_tests PRIVATE TREK_HOST_CORE_SHA="${host_core_sha}")
  set_target_properties(host_native_tests PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")
  foreach(case IN ITEMS hc01_open hc02_open_failure hc03_duplicate hc04_double_close
      hc05_thread_boundary reopen exclusive shutdown product_boundary)
    add_test(NAME host.native.${case} COMMAND host_native_tests ${case})
    set_tests_properties(host.native.${case} PROPERTIES TIMEOUT 30 LABELS "h02;native")
  endforeach()

  # A separate executable replaces only the private bridge bindings to force
  # lifecycle failures. The product library and real bridge are not linked.
  add_executable(host_fault_tests tests/fault_tests.cpp ${host_sources})
  target_compile_features(host_fault_tests PRIVATE cxx_std_20)
  target_include_directories(host_fault_tests PRIVATE src include ../f04/include)
  target_compile_definitions(host_fault_tests PRIVATE TREK_HOST_STATIC_TEST TREK_HOST_CORE_SHA="${host_core_sha}")
  target_link_libraries(host_fault_tests PRIVATE Threads::Threads)
  foreach(case IN ITEMS initialization hc06_incompatible_states pending failed_destroy failed_active_probe shutdown_retry)
    add_test(NAME host.fault.${case} COMMAND host_fault_tests ${case})
    set_tests_properties(host.fault.${case} PROPERTIES TIMEOUT 30 LABELS "h02;fault-injection")
  endforeach()
endif()
