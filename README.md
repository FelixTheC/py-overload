# pyoverload
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)


## A Runtime method override decorator which should behave like a compiled language
- there is a `override` decorator from `typing` which works only for static type checking
- this decorator works on `runtime`

### Example

```python
from typing import List

from pyoverload.class_tools import overload


class Example:
    @overload
    def my_func(self):
        return 0

    @overload
    def my_func(self, a: int, b: int):
        return a * b

    @overload
    def my_func(self, a: int, b: int, c: int):
        return a * b * c

    @overload
    def my_func(self, *, val: int, other_val: int):
        return val, other_val

    @overload
    def my_func(self, val: List[int], other_val, /):
        return [other_val * v for v in val]

    @overload
    def my_func(self, val: List[str], other_val, /):
        return val, other_val


if __name__ == "__main__":
    example = Example()
    assert example.my_func() == 0
    assert example.my_func(2, 3, 4) == 24
    assert example.my_func([1, 2, 3], 3) == [3, 6, 9]
    assert example.my_func(2, "3") == "33"
```