# Module 0b, exercise 6: write a modern, target-based CMake build for this small project.
#
# Requirements (checked by tests/test_m0b.py):
#   - a library target `units` built from src/units.cpp, whose headers in include/ are visible to its users;
#   - Eigen found with find_package(Eigen3 ... NO_MODULE) and linked to `units` as a usage requirement;
#   - C++17 required through target_compile_features, warnings enabled only for this project's targets;
#   - an executable `units_demo` from app/main.cpp, and a test executable `test_units` from tests/test_units.cpp,
#     registered with CTest so that `ctest` runs it;
#   - no directory-wide commands such as include_directories(), link_libraries() or add_compile_options().
#
# TODO(m0b): write the build.
cmake_minimum_required(VERSION 3.20)
project(units_exercise LANGUAGES CXX)
message(FATAL_ERROR "TODO(m0b): write this CMakeLists.txt")
