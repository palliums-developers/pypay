init:
    python3 -m venv ./venv

    ./venv/bin/pip install --upgrade pip wheel setuptools
    ./venv/bin/pip install -r requirements.txt

format:
    ./venv/bin/python -m black pypay tests

test: format
    ./venv/bin/pytest tests/test_* -k "$(TEST)" -vv
