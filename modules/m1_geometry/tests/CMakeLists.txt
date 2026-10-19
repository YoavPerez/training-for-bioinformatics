add_executable(m1_tests test_transform.cpp)
target_link_libraries(m1_tests slam_pipeline GTest::gtest_main)
gtest_discover_tests(m1_tests DISCOVERY_TIMEOUT 60 PROPERTIES LABELS m1)
