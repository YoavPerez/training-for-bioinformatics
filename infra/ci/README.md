# CI

GitHub Actions only reads workflows from `.github/workflows/`, so `ci.yml` lives there. The steps it runs are scripts in this folder, so they can also be run locally inside the dev container:

| Script | What it checks |
|---|---|
| `lint.sh` | ruff, clang-format, `resources/links.yaml` schema, self-check quiz consistency |
| `build.sh` | CMake configure + build |
| `test_module.sh mN` | one module's acceptance tests (pytest + `ctest -L '^mN$'`) on the CI sample |

In CI every module is its own job. Modules you have not finished yet are red; that is expected. A module's job turning green is one of its acceptance criteria.
