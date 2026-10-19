add_executable(m4b_tests test_camera.cpp)
target_link_libraries(m4b_tests slam_pipeline GTest::gtest_main)
gtest_discover_tests(m4b_tests DISCOVERY_TIMEOUT 60 PROPERTIES LABELS m4b)
