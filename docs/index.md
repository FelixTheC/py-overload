# strongtyping-pyoverload
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/release/python-3140/)
![Python application](https://github.com/FelixTheC/py-overload/workflows/Python%20application/badge.svg)
![Python tox](https://github.com/FelixTheC/py-overload/workflows/Python%20tox/badge.svg)
![image](https://codecov.io/gh/FelixTheC/py-overload/graph/badge.svg)

[__*strongtyping-pyoverload*__](https://github.com/FelixTheC/py-overload) provides you with a decorator `overload`, which add overloading capacity similar to C++.

### The Problem
With the introduction of Type-Hints in Python, now one is able to define the intended input types of a certain function. 

This works pretty well, but often we end up in a situation where we need to handle multiple types in a single function using `isinstance` checks.

```python
def process(data):
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, list):
        return [item * 2 for item in data]
    # ... it grows and becomes hard to maintain
```

### The Solution
With the `overload` decorator you can define dedicated functions with the same name, each tailored to specific types.

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

### Key Benefits
- **Native Pydantic Integration**: Automatically validate and dispatch based on Pydantic models.
- **Deep Inheritance & Mixin Support**: Respects Method Resolution Order (MRO) for complex class hierarchies.
- **AI-Ready Metadata**: Sets `__signature__` and `__annotations__` for better IDE and AI assistant support.
- **High Performance**: Optimized lookup logic with caching for minimal overhead.
- **Modern Python**: Full support for `typing.Annotated`, keyword-only parameters, and Python 3.13+.

Detailed information can be found in the **User's guide** section.