# strongtyping-pyoverload
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/release/python-3140/)
![Python application](https://github.com/FelixTheC/py-overload/workflows/Python%20application/badge.svg)
![Python tox](https://github.com/FelixTheC/py-overload/workflows/Python%20tox/badge.svg)
![image](https://codecov.io/gh/FelixTheC/py-overload/graph/badge.svg)
![](https://img.shields.io/pypi/dm/pyoverload)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![AI Agents](https://img.shields.io/badge/AI_Agents-SKILL.md-blue?logo=robotframework&logoColor=white)](SKILL.md)

## Runtime method overloading for Python

`strongtyping-pyoverload` provides a powerful `overload` decorator that brings true runtime method overloading to Python, similar to C++.

### Key Features
- **Native Pydantic Integration**: Automatically validate and dispatch based on Pydantic models.
- **Deep Inheritance & Mixin Support**: Respects Method Resolution Order (MRO) for complex class hierarchies.
- **AI-Ready Metadata**: Sets `__signature__` and `__annotations__` for better IDE and AI assistant support.
- **High Performance**: Optimized lookup logic with caching for minimal overhead.
- **Modern Python**: Full support for `typing.Annotated`, keyword-only parameters, and Python 3.13+.

### Quick Start
```python
from strongtyping_pyoverload import overload

class DataProcessor:
    @overload
    def process(self, data: str):
        return data.upper()

    @overload
    def process(self, data: list):
        return [item * 2 for item in data]
```

## Documentation
Full documentation can be found at [readthedocs](https://strongtyping-pyoverload.readthedocs.io/en/latest/).
