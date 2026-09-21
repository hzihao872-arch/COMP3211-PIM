# Testing Guide

Use the Python standard-library `unittest` framework. Model tests belong in `tests/model/` and should mirror the corresponding module name, for example:

```text
src/model/task.py       -> tests/model/test_task.py
src/model/criteria.py   -> tests/model/test_criteria.py
```

Each test should make its exercised behavior and expected result clear through its name, short comments or docstring where useful, and assertions.

Run all tests from the repository root:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

Test normal cases, boundary cases, and invalid input. The final submission also needs a separate line-coverage report for the `model` package.
