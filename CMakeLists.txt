cmake_minimum_required(VERSION 3.20)
project(slam_onboarding LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE RelWithDebInfo)
endif()

include(FetchContent)
FetchContent_Declare(googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.17.0.tar.gz
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE)
FetchContent_Declare(nanoflann
  URL https://github.com/jlblancoc/nanoflann/archive/refs/tags/v1.7.1.tar.gz
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE)
set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
set(NANOFLANN_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(NANOFLANN_BUILD_TESTS OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest nanoflann)

enable_testing()
include(GoogleTest)

# Found here so that every subdirectory (pipeline and module tests) sees the imported target.
find_package(Eigen3 3.4 REQUIRED NO_MODULE)

add_subdirectory(pipeline)

# Each module's visible acceptance tests. Tests are labelled by module (e.g. `ctest -L m1`).
file(GLOB module_test_dirs ${CMAKE_CURRENT_SOURCE_DIR}/modules/*/tests)
foreach(dir ${module_test_dirs})
  if(EXISTS ${dir}/CMakeLists.txt)
    get_filename_component(module_dir ${dir} DIRECTORY)
    get_filename_component(module_name ${module_dir} NAME)
    add_subdirectory(${dir} ${CMAKE_BINARY_DIR}/modules/${module_name})
  endif()
endforeach()
