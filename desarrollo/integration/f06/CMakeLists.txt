cmake_minimum_required(VERSION 3.25)
project(TrekF06 LANGUAGES CXX)
# The existing F04 bridge owns the ONLY session, Core WorldState, clock,
# version pin, save/load and F05 order pipeline. No separate sensor world.
add_subdirectory(../f05 "${CMAKE_CURRENT_BINARY_DIR}/f05")
# F04 and its CMakeLists are frozen by a historical SHA-256 oracle.
# Build F06 through an audited-source overlay in the ignored build tree, never
# by modifying the original F04 files or regenerating historical oracles.
find_package(Python3 REQUIRED COMPONENTS Interpreter)
set(F06_BRIDGE_SOURCE "${CMAKE_CURRENT_BINARY_DIR}/generated/f04_bridge_f06.cpp")
execute_process(
 COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/assemble_f04_bridge.py"
  --source "${CMAKE_CURRENT_SOURCE_DIR}/../f04/src/f04_bridge.cpp"
  --out "${F06_BRIDGE_SOURCE}"
 COMMAND_ERROR_IS_FATAL ANY
)
set_property(TARGET TrekF04Bridge PROPERTY SOURCES "${F06_BRIDGE_SOURCE}")
target_compile_definitions(TrekF04Bridge PRIVATE F06_ENABLE_SENSORS=1)
execute_process(
 COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/generate_sensor_profiles.py"
  --out "${CMAKE_CURRENT_BINARY_DIR}/generated/f06_profiles_generated.h"
 COMMAND_ERROR_IS_FATAL ANY
)
set(F06_QA_PHYSICAL "${CMAKE_CURRENT_BINARY_DIR}/generated/aster_f06_physical.json")
execute_process(
 COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/../../tools/generation/enrich_aster_f06_v1.py"
  --source "${CMAKE_CURRENT_SOURCE_DIR}/fixtures/aster_f06_qa.json"
  --output "${F06_QA_PHYSICAL}"
 COMMAND_ERROR_IS_FATAL ANY
)
execute_process(
 COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/build_validation_system.py"
  --source "${F06_QA_PHYSICAL}"
  --out "${CMAKE_CURRENT_BINARY_DIR}/generated/f06_demo_system_generated.h"
 COMMAND_ERROR_IS_FATAL ANY
)
execute_process(
 COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/build_aster_science.py"
  --source "${F06_QA_PHYSICAL}"
  --out "${CMAKE_CURRENT_BINARY_DIR}/generated/f06_aster_science_generated.h"
 COMMAND_ERROR_IS_FATAL ANY
)
target_include_directories(TrekF04Bridge PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include"
 PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/src" "${CMAKE_CURRENT_SOURCE_DIR}/../f04/src"
  "${CMAKE_CURRENT_BINARY_DIR}/generated")

enable_testing()
add_executable(f06_tests tests/f06_tests.cpp)
target_link_libraries(f06_tests PRIVATE TrekF04Bridge CoreRPG::CoreRPG)
target_compile_features(f06_tests PRIVATE cxx_std_20)
target_include_directories(f06_tests PRIVATE "${CMAKE_CURRENT_BINARY_DIR}/generated")
# Windows needs the F04 DLL beside the test executable.
set_target_properties(f06_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")
foreach(scenario IN ITEMS quiet detection partial loss reacquire focused stale unauthorized save_load eight_hours degraded science_queue tracking tracking_capacity_recovery area_scan notices_cursor power_queue f05_order world_feed profiles configuration config_live search diagnostics results_compare categories mini_system bis_science bis_timed bis_environment bis_power bis_sections)
 add_test(NAME f06.${scenario} COMMAND f06_tests ${scenario})
endforeach()
