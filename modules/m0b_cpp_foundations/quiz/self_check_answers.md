# Module 0b — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M0B-R01.** Resource Acquisition Is Initialization; destructors run during stack unwinding, so resources are released. See: cpp_core_guidelines — "R: Resource management" (R.1)
**M0B-R02.** Zero: let members manage resources and declare no special members; five: when the class itself manages a raw resource. See: cppref_rule_of_three — whole page
**M0B-R03.** Nothing: it is a cast to an rvalue reference that allows a move to be selected. See: cppcon_move_semantics — whole talk
**M0B-R04.** Not copyable (copy is implicitly deleted), but movable. See: cppref_unique_ptr — class description
**M0B-R05.** optional for an expected "no value" outcome; exceptions for violated preconditions/errors the caller cannot ignore. See: cppref_optional — description
**M0B-R06.** O(log n); an iterator to the first element not less than the value. See: cppref_lower_bound — whole page
**M0B-R07.** A const reference to a concrete type forces a temporary copy of blocks/expressions; Ref binds without copying. See: eigen_function_params — whole page
**M0B-R08.** The same matrix appears on both sides and is overwritten while still being read. See: eigen_aliasing — whole page
**M0B-R09.** ASan: out-of-bounds, use-after-free; UBSan: signed overflow, null reference binding. See: asan_docs — introduction
**M0B-R10.** PRIVATE: only this target; INTERFACE: only its users; PUBLIC: both. See: modern_cmake — "The Basics"

## Self-check 2 — Apply
**M0B-A01.** None (rule of zero): the unique_ptr with a custom deleter gives move-only, leak-free behaviour. See: cppref_rule_of_three — rule of zero
**M0B-A02.** `std::optional<T> out = std::move(slot); slot.reset();`. See: cppref_optional — "Modifiers"
**M0B-A03.** Eigen aliasing (Eigen's own assertion) and the `auto` expression (a failing test). See: eigen_pitfalls — "C++11 and the auto keyword"
**M0B-A04.** Binding a reference to a destroyed object is undefined behaviour, so the compiler may assume it never happens. See: cppcon_undefined_behavior — whole talk
**M0B-A05.** `Eigen::Ref` with inner stride 1 binds to the block directly; a non-matching layout would fail to compile or copy. See: eigen_function_params — "Ref"
**M0B-A06.** Users of `units` include `units.hpp`, which includes Eigen, so they need Eigen's include path. See: modern_cmake — "The Basics"
