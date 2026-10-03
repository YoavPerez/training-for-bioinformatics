"""Module 0b acceptance tests (Python side): the CMake exercise."""

import os
import re
import shutil
import subprocess

import pytest

EXERCISE = "modules/m0b_cpp_foundations/starter/cmake_exercise"


@pytest.fixture
def cmakelists(repo_root):
    return (repo_root / EXERCISE / "CMakeLists.txt").read_text()


def test_cmake_uses_targets_not_directory_commands(cmakelists):
    code = "\n".join(line.split("#", 1)[0] for line in cmakelists.splitlines())
    for banned in ["include_directories(", "link_libraries(", "add_compile_options(", "add_definitions("]:
        assert not re.search(rf"(?<![_a-z]){re.escape(banned)}", code), f"use target_* commands instead of {banned}"
    for required in [
        "add_library(units",
        "target_include_directories(units",
        "target_compile_features(units",
        "add_executable(units_demo",
        "add_executable(test_units",
        "add_test(",
    ]:
        assert required in code.replace(" (", "("), f"missing {required}"
    assert re.search(r"find_package\(Eigen3[^)]*NO_MODULE", code)


def test_cmake_project_builds_and_tests_pass(repo_root, tmp_path):
    if shutil.which("cmake") is None:
        pytest.skip("cmake not installed")
    src = tmp_path / "src"
    shutil.copytree(repo_root / EXERCISE, src)  # copy: build outside the source tree, path without spaces issues
    build = tmp_path / "build"
    env = dict(os.environ)
    run = lambda *cmd: subprocess.run(cmd, cwd=tmp_path, env=env, capture_output=True, text=True)  # noqa: E731
    r = run("cmake", "-S", str(src), "-B", str(build), "-DCMAKE_BUILD_TYPE=Release")
    assert r.returncode == 0, r.stdout[-1500:] + r.stderr[-1500:]
    r = run("cmake", "--build", str(build), "-j4")
    assert r.returncode == 0, r.stdout[-1500:] + r.stderr[-1500:]
    r = run("ctest", "--test-dir", str(build), "--output-on-failure")
    assert r.returncode == 0 and "100% tests passed" in r.stdout, r.stdout[-1500:]
    assert (build / "units_demo").exists() or any(build.rglob("units_demo"))
