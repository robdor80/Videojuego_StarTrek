cmake_minimum_required(VERSION 3.25)
project(TrekF11NativeHostReader LANGUAGES CXX)
enable_testing()
# Reuse the exact approved F11/F05/F04 bridge and Core pin; no code cloning.
add_subdirectory(../f11 "${CMAKE_CURRENT_BINARY_DIR}/f11")

# This library is an internal C++ view adapter, NOT an issuer DLL or a
# client-facing ABI. Do not add F11_NATIVE_TEST_HOST to its definitions.
add_library(TrekF11HostReader STATIC src/f11_host_reader.cpp)
target_compile_features(TrekF11HostReader PUBLIC cxx_std_20)
target_include_directories(TrekF11HostReader PUBLIC include ../f11/include ../f04/include)
target_link_libraries(TrekF11HostReader PUBLIC TrekF04Bridge)
if(MSVC)
  target_compile_options(TrekF11HostReader PRIVATE /utf-8)
endif()

add_executable(f11_host_reader_tests tests/f11_host_reader_tests.cpp)
target_link_libraries(f11_host_reader_tests PRIVATE TrekF11HostReader CoreRPG::CoreRPG)
target_compile_features(f11_host_reader_tests PRIVATE cxx_std_20)
# On Windows the test must be in the same directory as TrekF04Bridge.dll.
set_target_properties(f11_host_reader_tests PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/f11/f05/f04")
if(MSVC)
  target_compile_options(f11_host_reader_tests PRIVATE /utf-8)
endif()
foreach(scenario IN ITEMS before after access legacy)
  add_test(NAME f11.host_${scenario}
    COMMAND f11_host_reader_tests "${CMAKE_CURRENT_BINARY_DIR}/f11/process" ${scenario})
  set_tests_properties(f11.host_${scenario} PROPERTIES FIXTURES_REQUIRED f11_process)
endforeach()
