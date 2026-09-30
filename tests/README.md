# Testing Guide

Use the Python standard-library `unittest` framework. Model tests belong in `tests/model/` and mirror their corresponding module names, for example:

```text
src/model/records.py -> tests/model/test_records.py
src/model/search.py  -> tests/model/test_search.py
```

Each test should make its exercised behavior and expected result clear through its name, short comments or docstring where useful, and assertions.

Run all tests from the repository root:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
```

The explicit `-t .` keeps `tests/model` from shadowing `src/model`. Storage and controller tests live in their own subdirectories; `tests/test_acceptance.py` runs the actual CLI process. The final submission also needs a separate line-coverage report for the `model` package.
