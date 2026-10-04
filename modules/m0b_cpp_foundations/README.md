# Module 0b: C++ foundations
**Tentative effort:** ~4–5 days (1–2 days if your diagnostic-quiz C++ section was strong) · **Phase:** A — Foundations

## Goal
Write modern C++ the way the team does: value semantics, RAII and clear ownership, templates and the standard library, Eigen without hidden copies or aliasing bugs, sanitizers and a debugger as daily tools, and target-based CMake. Every later module builds on this.

---

## Segment 1 — Learn

### Learn from
- [LearnCpp](https://www.learncpp.com/) — free online book — Ch. 12 "Compound Types: References and Pointers", Ch. 14–15 "Introduction to Classes" / "More on Classes", Ch. 16 "Dynamic arrays: std::vector", Ch. 22 "Move Semantics and Smart Pointers", Ch. 26 "Templates and Classes", Ch. 27 "Exceptions". Skim what you know; do the chapter quizzes for what you don't.
- [Back to Basics: Smart Pointers and RAII — Inbal Levi (CppCon 2021)](https://www.youtube.com/watch?v=07rJOzFRs6M) — video — whole talk
- [Back to Basics: Move Semantics — Nicolai Josuttis (CppCon 2021)](https://www.youtube.com/watch?v=Bt3zcJZIalk) — video — whole talk
- [Back to Basics: Cpp Value Semantics — Klaus Iglberger (CppCon 2022)](https://www.youtube.com/watch?v=G9MxNwUoSt0) — video — whole talk
- [Back to Basics: Templates, part 1 — Bob Steagall (CppCon 2021)](https://www.youtube.com/watch?v=XN319NYEOcE) and [part 2](https://www.youtube.com/watch?v=2Y9XbltAfXs) — video
- [Back to Basics: Classic STL — Bob Steagall (CppCon 2021)](https://www.youtube.com/watch?v=tXUXl_RzkAk) — video — containers, iterators, algorithms
- [Back To Basics: Undefined Behavior — Sermersheim & Geller (CppCon 2021)](https://www.youtube.com/watch?v=NpL9YnxnOqM) — video — whole talk
- [Back to Basics: Debugging in C++ — Mike Shah (CppCon 2022)](https://www.youtube.com/watch?v=YzIBwqWC6EM) — video — gdb workflow
- [cppreference: rule of three/five/zero](https://en.cppreference.com/w/cpp/language/rule_of_three), [std::unique_ptr](https://en.cppreference.com/w/cpp/memory/unique_ptr), [std::optional](https://en.cppreference.com/w/cpp/utility/optional), [std::lower_bound](https://en.cppreference.com/w/cpp/algorithm/lower_bound) — docs — reference while coding
- [Eigen — Writing functions taking Eigen types as parameters](https://eigen.tuxfamily.org/dox/TopicFunctionTakingEigenTypes.html), [Aliasing](https://eigen.tuxfamily.org/dox/group__TopicAliasing.html), [Common pitfalls](https://eigen.tuxfamily.org/dox/TopicPitfalls.html) — docs — all three pages
- [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) and [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) — docs — "Usage" and the list of checks
- [An Introduction to Modern CMake](https://cliutils.gitlab.io/modern-cmake/) — free online book — "The Basics" and "Using Other Projects"
- [GoogleTest Primer](https://google.github.io/googletest/primer.html) — docs — assertions, test fixtures
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — docs — "R: Resource management", "C.20/C.21" (rule of zero/five), "F.call: Parameter passing"
- Tool: [Compiler Explorer](https://godbolt.org/) — try small snippets and see what the compiler does

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) before coding, then grade yourself.

## Segment 3 — Build

All exercise code lives in [`starter/`](starter/). Its library is built with the rest of the repository (`cmake --build build`), and the tests run with `python tools/module_tests.py m0b`.

### Assignment
1. **Ring buffer (templates, move-only types).** Implement [`ring_buffer.hpp`](starter/include/cppf/ring_buffer.hpp): a fixed-capacity FIFO that overwrites the oldest element and works with `std::unique_ptr` elements.
2. **Timed buffer (STL algorithms, invariants, exceptions).** Implement [`timed_buffer.hpp`](starter/include/cppf/timed_buffer.hpp): time-ordered samples with O(log n) interpolation, for scalars and Eigen vectors.
3. **Scan file (RAII, ownership, move semantics).** Implement [`scan_file.cpp`](starter/src/scan_file.cpp) and decide which special member functions [`scan_file.hpp`](starter/include/cppf/scan_file.hpp) needs. The tests count open file handles: a leak, a double close or a copy fails them.
4. **Point statistics (Eigen without copies).** Implement [`stats.cpp`](starter/src/stats.cpp) so the functions accept blocks and `Eigen::Map`s over raw buffers, and write through to the caller.
5. **Bug hunt (sanitizers, debugger).** Every function in [`bug_hunt.cpp`](starter/src/bug_hunt.cpp) has a bug. Its tests are built with ASan + UBSan. For each bug: reproduce it, read the report (or step through in gdb), fix it, and write one line in your PR saying which tool found it and why it was a bug.
6. **CMake.** Write [`cmake_exercise/CMakeLists.txt`](starter/cmake_exercise/CMakeLists.txt) from the requirements in its header: target-based, no directory-wide commands.
7. **Your own test.** Add one GoogleTest of your own to `tests/test_cpp_foundations.cpp` for an edge case the provided tests miss.

### Deliverables
- [ ] All seven assignment items (six exercises and your own test) merged through PR review
- [ ] Bug-hunt notes in the PR: bug, tool that found it, fix
- [ ] One extra test of your own

### Acceptance criteria
- Tests in `tests/` pass in CI (`python tools/module_tests.py m0b`), including the sanitizer build of the bug hunt.
- No compiler warnings in your code; clang-format clean.
- `ScanFile` declares no special member functions it does not need (explain your choice in the PR).

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md) about your own code, and prepare the "Explain to your mentor" prompts.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open a PR and request review.

## Where to look if stuck
- What happens to a `std::unique_ptr` member when the class is copied or moved: cppreference "rule of three/five/zero" and C++ Core Guidelines C.20.
- `std::array<std::optional<T>, N>` and moving out of an optional: cppreference `std::optional`, "Observers" and "Modifiers".
- Finding the bracketing samples in O(log n): cppreference `std::lower_bound` / `std::upper_bound`.
- `Eigen::Ref` and why a by-value or `const Matrix3Xd&` parameter copies a block: Eigen "Writing functions taking Eigen types as parameters".
- A sanitizer report: read the first frame in *your* code; rebuild with `-O0 -g` and set a breakpoint there. If an ASan binary only prints `AddressSanitizer:DEADLYSIGNAL` forever, run it with `setarch $(uname -m) -R <binary>` (a known issue with address-space randomization on recent kernels; `ctest` already does this).
- `auto` with Eigen: the "Common pitfalls" page.
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
