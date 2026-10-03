# Module 0b: C++ foundations. The exercise library is built from the module's starter/ folder.
set(CPPF_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../starter)

add_library(cppf ${CPPF_DIR}/src/scan_file.cpp ${CPPF_DIR}/src/stats.cpp)
target_include_directories(cppf PUBLIC ${CPPF_DIR}/include)
target_compile_features(cppf PUBLIC cxx_std_17)
target_link_libraries(cppf PUBLIC Eigen3::Eigen)
target_compile_options(cppf PRIVATE -Wall -Wextra)

add_executable(m0b_tests test_cpp_foundations.cpp)
target_link_libraries(m0b_tests cppf GTest::gtest_main)
gtest_discover_tests(m0b_tests PROPERTIES LABELS m0b TIMEOUT 30)

# The bug hunt is built with AddressSanitizer + UndefinedBehaviorSanitizer; any finding aborts the test.
# Debug-style flags (-O1, frame pointers) make the reports readable.
add_executable(m0b_bug_hunt_tests test_bug_hunt.cpp ${CPPF_DIR}/src/bug_hunt.cpp)
target_include_directories(m0b_bug_hunt_tests PRIVATE ${CPPF_DIR}/include)
target_link_libraries(m0b_bug_hunt_tests Eigen3::Eigen GTest::gtest_main)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  set(SANITIZE -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer -O1 -g)
  target_compile_options(m0b_bug_hunt_tests PRIVATE ${SANITIZE} -UNDEBUG)
  target_link_options(m0b_bug_hunt_tests PRIVATE -fsanitize=address,undefined)
endif()
# On recent kernels (vm.mmap_rnd_bits = 32) older ASan runtimes loop forever printing
# "AddressSanitizer:DEADLYSIGNAL". Running without address-space randomization avoids it.
find_program(SETARCH setarch)
if(SETARCH AND CMAKE_SYSTEM_NAME STREQUAL "Linux")
  set_target_properties(m0b_bug_hunt_tests PROPERTIES
    CROSSCOMPILING_EMULATOR "${SETARCH};${CMAKE_HOST_SYSTEM_PROCESSOR};-R")
endif()
gtest_discover_tests(m0b_bug_hunt_tests
  PROPERTIES LABELS m0b TIMEOUT 60
             ENVIRONMENT "ASAN_OPTIONS=detect_leaks=0;UBSAN_OPTIONS=print_stacktrace=1"
  DISCOVERY_MODE PRE_TEST)
