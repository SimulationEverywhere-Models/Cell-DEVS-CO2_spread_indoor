cmake_minimum_required (VERSION 3.1)
set(Boost_USE_MULTITHREADED FALSE)
set (CMAKE_CXX_STANDARD 17)
set (CMAKE_CXX_COMPILER "g++")
project(cadmium_celldevs)
add_compile_options(-g)


enable_testing()

execute_process(COMMAND ${CMAKE_COMMAND} -E make_directory bin)
execute_process(COMMAND ${CMAKE_COMMAND} -E make_directory results)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../../cadmium/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../../cadmium/json/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../../DESTimes/include)

find_package(Boost COMPONENTS program_options unit_test_framework REQUIRED)
include_directories (${Boost_INCLUDE_DIRS})


add_executable(co2_lab model/co2_main.cpp)
target_link_libraries(co2_lab Boost::program_options)


