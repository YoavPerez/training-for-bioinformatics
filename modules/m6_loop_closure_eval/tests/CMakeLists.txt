add_executable(m6_loop_tests test_loop.cpp)
target_link_libraries(m6_loop_tests slam_pipeline GTest::gtest_main)
gtest_discover_tests(m6_loop_tests DISCOVERY_TIMEOUT 60 PROPERTIES LABELS m6)

if(TARGET slam_backend)
  add_executable(m6_graph_tests test_false_loop.cpp)
  target_link_libraries(m6_graph_tests slam_backend GTest::gtest_main)
  gtest_discover_tests(m6_graph_tests DISCOVERY_TIMEOUT 60 PROPERTIES LABELS m6)
endif()
