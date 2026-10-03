# The trainee's growing pipeline library. Each module adds sources here.
find_package(GTSAM QUIET)

add_library(slam_pipeline
  src/geometry/transform.cpp
  src/estimation/eskf.cpp
  src/sensors/deskew.cpp
  src/registration/normals.cpp
  src/registration/icp.cpp
  src/io/kitti.cpp
  src/loop/scan_context.cpp
  src/odometry/lidar_odometry.cpp
)
target_include_directories(slam_pipeline PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(slam_pipeline PUBLIC Eigen3::Eigen nanoflann::nanoflann)
target_compile_options(slam_pipeline PRIVATE -Wall -Wextra)

if(GTSAM_FOUND)
  add_library(slam_backend
    src/backend/graph_builder.cpp
  )
  target_include_directories(slam_backend PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
  target_link_libraries(slam_backend PUBLIC slam_pipeline gtsam)
  target_compile_options(slam_backend PRIVATE -Wall -Wextra)
else()
  message(WARNING "GTSAM not found: module 5/6 back-end targets are skipped.")
endif()

add_subdirectory(apps)

add_executable(pipeline_smoke_tests tests/test_smoke.cpp)
target_link_libraries(pipeline_smoke_tests slam_pipeline GTest::gtest_main)
gtest_discover_tests(pipeline_smoke_tests PROPERTIES LABELS smoke)
