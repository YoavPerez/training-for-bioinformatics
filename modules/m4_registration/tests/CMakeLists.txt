add_executable(m4_tests test_icp.cpp)
target_link_libraries(m4_tests slam_pipeline GTest::gtest_main)
gtest_discover_tests(m4_tests PROPERTIES LABELS m4)
