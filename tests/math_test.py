from template_python_project.math import add
import os
def test_add():
    print(f"PY PATH: {os.environ.get('PYTHONPATH')}")
    result = add(1, 1)
    assert result == 2
