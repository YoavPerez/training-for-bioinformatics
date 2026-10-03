add_executable(m5_odometry_tests test_odometry.cpp)
target_link_libraries(m5_odometry_tests slam_pipeline GTest::gtest_main)
gtest_discover_tests(m5_odometry_tests PROPERTIES LABELS m5)

if(TARGET slam_backend)
  add_executable(m5_graph_tests test_graph.cpp)
  target_link_libraries(m5_graph_tests slam_backend GTest::gtest_main)
  gtest_discover_tests(m5_graph_tests PROPERTIES LABELS m5)
endif()
