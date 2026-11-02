cmake_minimum_required(VERSION 3.25)
project(TrekF05 LANGUAGES CXX)
set(F05_ENABLE_ORDERS ON CACHE BOOL "Explicit P01 integration" FORCE)
# F04 owns the one session, library and Core link. No second bridge/world.
add_subdirectory(../f04 "${CMAKE_CURRENT_BINARY_DIR}/f04")
enable_testing()
add_executable(f05_tests tests/f05_tests.cpp)
target_link_libraries(f05_tests PRIVATE TrekF04Bridge CoreRPG::CoreRPG)
target_compile_features(f05_tests PRIVATE cxx_std_20)
# On Windows the test executable must share the existing bridge DLL directory.
set_target_properties(f05_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f04")
foreach(case IN ITEMS scenario authority recipient unsupported scope stale reception
 duplicate revalidate expired cancel transition determinism corrupt buffers population history history_fault)
 add_test(NAME f05.${case} COMMAND f05_tests ${case} "${CMAKE_CURRENT_BINARY_DIR}/${case}")
endforeach()
add_test(NAME f05.process_save COMMAND f05_tests process_save "${CMAKE_CURRENT_BINARY_DIR}/orders")
set_tests_properties(f05.process_save PROPERTIES FIXTURES_SETUP orders)
add_test(NAME f05.process_load COMMAND f05_tests process_load "${CMAKE_CURRENT_BINARY_DIR}/orders")
set_tests_properties(f05.process_load PROPERTIES FIXTURES_REQUIRED orders)
