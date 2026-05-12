---
name: pyoverload
description: Adds C++ like function overloading capacity to Python using a decorator.
---

### pyoverload

`strongtyping-pyoverload` provides a decorator `overload` that allows defining multiple versions of a function or method with the same name but different type signatures.

#### Key Features

*   **Method Overloading**: Define multiple methods with the same name in a class, distinguished by their parameter types and count.
*   **Module-level Overloading**: Apply overloading to pure functions within a module.
*   **Multiple `__init__`**: Support for multiple constructor definitions based on different input arguments.
*   **Inheritance Support**: Subclasses can override overloaded methods, provided they match the original type definitions when intended.
*   **Default Case Support**: Use `*args` and `**kwargs` to define fallback or default implementations.
*   **Minimal Type Hinting**: Only one differing typed parameter or a different parameter length is needed to distinguish between overloads.

#### Usage Example

```python
from strongtyping_pyoverload import overload

class Example:
    @overload
    def my_func(self):
        return 0

    @overload
    def my_func(self, a: int, b: int):
        return a * b

    @overload
    def my_func(self, a: str, b: str):
        return a + b
```