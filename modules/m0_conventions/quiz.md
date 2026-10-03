# Module 0 — Diagnostic quiz

Time-box: 90 minutes. No searching. Write your answers in a separate file and hand them to your mentor. This quiz calibrates the program to you; it is not a pass/fail test.

## A. Linear algebra
1. Give the result of multiplying the 2×2 matrix [[0, −1], [1, 0]] by the vector (2, 1). What does this matrix do geometrically?
2. A 3×3 matrix R satisfies RᵀR = I and det(R) = 1. Name the set of such matrices. What is R⁻¹?
3. For A (m×n) with m > n and full column rank, write the normal equations for min ‖Ax − b‖².
4. What are the eigenvalues of a 3×3 rotation matrix by angle θ about some axis?
5. What does the rank of a covariance matrix tell you about the underlying random vector?
6. Compute the cross product (1, 0, 0) × (0, 1, 0). Write the 3×3 matrix [a]ₓ such that [a]ₓ b = a × b.

## B. Probability and statistics
7. X ~ N(μ, σ²). What is the distribution of aX + b?
8. Two independent Gaussian estimates of the same scalar have variances 4 and 1. What is the variance of their optimal (inverse-variance weighted) fusion?
9. State Bayes' rule for p(x | z).
10. A 3-D zero-mean Gaussian error e with covariance P: what is the distribution of eᵀP⁻¹e?
11. You report a mean error from 5 runs. Name two things you would add so that the number is interpretable.
12. What is the difference between a confidence interval and a prediction interval?

## C. C++ and Eigen
13. What is printed?
    ```cpp
    std::vector<int> v{1, 2, 3};
    for (auto x : v) x *= 2;
    std::cout << v[0] + v[1] + v[2];
    ```
14. Explain the ownership semantics of `std::unique_ptr<T>` vs `std::shared_ptr<T>`, and when to pass `const T&` vs `T` vs `T&&`.
15. What is wrong with returning a reference to a local variable?
16. Write a function template `clamp01(T x)` that clamps any arithmetic type to [0, 1].
17. In Eigen, what is the difference between `Eigen::Vector3d` and `Eigen::VectorXd`?
18. `Eigen::Quaterniond q(1, 0, 0, 0);` — which coefficient is the scalar part? In what order does `q.coeffs()` store the coefficients?
19. What does `auto` capture when used with an Eigen expression such as `auto c = a + b;`, and why can that be a problem?
20. What does `const` after a member function declaration mean?

## D. Tools
21. Write a shell one-liner that counts the lines containing "ERROR" in all `*.log` files under the current directory.
22. What is the difference between `git merge` and `git rebase`? When should you avoid rebasing?
23. How would you find which commit introduced a bug that a test now catches?
