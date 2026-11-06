cmake_minimum_required(VERSION 3.25)
project(TrekF06 LANGUAGES CXX)
# The existing F04 bridge owns the ONLY session, Core WorldState, clock,
# version pin, save/load and F05 order pipeline. No separate sensor world.
set(F06_ENABLE_SENSORS ON CACHE BOOL "Native sensor extension on F04/Core" FORCE)
add_subdirectory(../f05 "${CMAKE_CURRENT_BINARY_DIR}/f05")
enable_testing()
add_executable(f06_tests tests/f06_tests.cpp)
target_link_libraries(f06_tests PRIVATE TrekF04Bridge CoreRPG::CoreRPG)
target_compile_features(f06_tests PRIVATE cxx_std_20)
# Windows needs the F04 DLL beside the test executable.
set_target_properties(f06_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f05/f04")
foreach(scenario IN ITEMS quiet detection partial loss reacquire focused stale unauthorized save_load eight_hours degraded)
 add_test(NAME f06.${scenario} COMMAND f06_tests ${scenario})
endforeach()
