add_executable(m3_tests test_deskew.cpp)
target_link_libraries(m3_tests slam_pipeline GTest::gtest_main)
gtest_discover_tests(m3_tests PROPERTIES LABELS m3)
