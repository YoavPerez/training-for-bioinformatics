add_executable(m3_tests test_deskew.cpp)
target_link_libraries(m3_tests slam_pipeline GTest::gtest_main)
gtest_discover_tests(m3_tests DISCOVERY_TIMEOUT 60 PROPERTIES LABELS m3)
