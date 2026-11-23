cmake_minimum_required(VERSION 3.25)
project(TrekHostProductConsumer LANGUAGES C CXX)

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
add_executable(academy_c_product_client ../academy_abi_tests.c)
set_target_properties(academy_c_product_client PROPERTIES C_STANDARD 11 C_STANDARD_REQUIRED YES)
target_include_directories(academy_c_product_client PRIVATE ../../include)
target_link_libraries(academy_c_product_client PRIVATE TrekHost)
add_executable(legacy_c_product_client ../host_abi_tests.c)
set_target_properties(legacy_c_product_client PROPERTIES C_STANDARD 11 C_STANDARD_REQUIRED YES)
target_include_directories(legacy_c_product_client PRIVATE ../../include)
target_link_libraries(legacy_c_product_client PRIVATE TrekHost)
add_test(NAME product.abi.v1 COMMAND legacy_c_product_client)
add_test(NAME product.academy.c_lifecycle COMMAND academy_c_product_client)
add_test(NAME product.academy.c_process
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/../academy_abi_process.py"
    "$<TARGET_FILE:academy_c_product_client>" "$<TARGET_FILE:academy_product_client>"
    "${CMAKE_CURRENT_BINARY_DIR}/c-proof")
add_test(NAME product.academy.c_pagination
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/../academy_abi_process.py" pagination
    "$<TARGET_FILE:academy_c_product_client>" "$<TARGET_FILE:academy_product_client>"
    "${CMAKE_CURRENT_BINARY_DIR}/c-proof")
set_tests_properties(product.academy.c_pagination PROPERTIES TIMEOUT 300
  ENVIRONMENT_MODIFICATION "PATH=path_list_prepend:$<TARGET_FILE_DIR:TrekHost>")
set_tests_properties(product.abi.v1 product.academy.c_lifecycle product.academy.c_process PROPERTIES TIMEOUT 180
  ENVIRONMENT_MODIFICATION "PATH=path_list_prepend:$<TARGET_FILE_DIR:TrekHost>")
if(MSVC)
  target_compile_options(academy_product_client PRIVATE /utf-8)
endif()

add_test(NAME product.academy.process
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/../academy_persistence_process.py" process
    "${CMAKE_CURRENT_BINARY_DIR}/proof" "$<TARGET_FILE:academy_product_client>")
set_tests_properties(product.academy.process PROPERTIES TIMEOUT 150
  ENVIRONMENT_MODIFICATION "PATH=path_list_prepend:$<TARGET_FILE_DIR:TrekHost>")
