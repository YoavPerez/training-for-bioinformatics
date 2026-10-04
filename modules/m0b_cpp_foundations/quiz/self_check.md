# Module 0b — Self-check

Answer every question in writing **before** opening the answers file. Then score yourself:

| Score (per section) | What to do |
|---|---|
| ≥ 80 % | Proceed. |
| 50–79 % | Revisit the pointers listed for the questions you missed, then re-answer them. |
| < 50 % | Revisit the pointers and talk to your mentor before moving on. |

## Self-check 1 — Readiness

**M0B-R01.** What does RAII stand for, and what guarantee does it give when an exception is thrown?

**M0B-R02.** State the rule of zero. When do you need the rule of five instead?

**M0B-R03.** What does `std::move` actually do at runtime?

**M0B-R04.** A class has a `std::unique_ptr` member and declares no special member functions. Is it copyable? Movable?

**M0B-R05.** When do you return `std::optional<T>` and when do you throw an exception?

**M0B-R06.** What is the complexity of `std::lower_bound` on a sorted `std::vector`, and what does it return?

**M0B-R07.** Why does Eigen recommend `Eigen::Ref<const Eigen::MatrixXd>` (or templates) over `const Eigen::MatrixXd&` for function parameters that should accept blocks?

**M0B-R08.** What is aliasing in Eigen, and why is `m = m.transpose();` a problem?

**M0B-R09.** Name one class of bug that AddressSanitizer finds and one that UndefinedBehaviorSanitizer finds.

**M0B-R10.** In CMake, what is the difference between `PUBLIC`, `PRIVATE` and `INTERFACE` on `target_link_libraries` / `target_include_directories`?

## Self-check 2 — Apply

**M0B-A01.** Which special member functions did you declare for `ScanFile`, and why is that enough?

**M0B-A02.** In your `RingBuffer::pop`, how do you get the element out of the `std::optional` slot without copying it?

**M0B-A03.** Which bugs in the bug hunt were *not* found by a sanitizer, and what found them instead?

**M0B-A04.** GCC turned the dangling reference in `smoothed` into a null reference. Why is it allowed to do that?

**M0B-A05.** Your `centroid` is called with `big.middleCols(10, 20)`. How do you know no copy of the block is made?

**M0B-A06.** Your CMake build links Eigen to `units` with `PUBLIC`. What would break if you used `PRIVATE`?

## Explain to your mentor
- Walk through what happens, call by call, in `c = std::move(b);` for two open `ScanFile`s, and why no handle leaks.
- Show one sanitizer report from the bug hunt and explain every line you used to find the bug.
