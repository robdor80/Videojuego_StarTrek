cmake_minimum_required(VERSION 3.25)
project(TrekHostProductConsumer LANGUAGES CXX)

find_package(Threads REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
enable_testing()

add_library(TrekHost SHARED IMPORTED)
set_target_properties(TrekHost PROPERTIES IMPORTED_LOCATION "${TREK_HOST_RUNTIME}")
if(WIN32)
  set_target_properties(TrekHost PROPERTIES IMPORTED_IMPLIB "${TREK_HOST_LIBRARY}")
endif()

add_executable(academy_product_client ../academy_persistence_tests.cpp)
target_compile_features(academy_product_client PRIVATE cxx_std_20)
target_include_directories(academy_product_client PRIVATE ../../include ../../src ../../../f04/include)
target_link_libraries(academy_product_client PRIVATE TrekHost Threads::Threads)
if(MSVC)
  target_compile_options(academy_product_client PRIVATE /utf-8)
endif()

add_test(NAME product.academy.process
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/../academy_persistence_process.py" process
    "${CMAKE_CURRENT_BINARY_DIR}/proof" "$<TARGET_FILE:academy_product_client>")
set_tests_properties(product.academy.process PROPERTIES TIMEOUT 150
  ENVIRONMENT_MODIFICATION "PATH=path_list_prepend:$<TARGET_FILE_DIR:TrekHost>")
