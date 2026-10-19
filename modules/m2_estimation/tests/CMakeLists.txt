add_executable(m2_tests test_eskf.cpp)
target_link_libraries(m2_tests slam_pipeline GTest::gtest_main)
gtest_discover_tests(m2_tests DISCOVERY_TIMEOUT 60 PROPERTIES LABELS m2)
