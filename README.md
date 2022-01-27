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
        """
        Base information about the func
        """
        return 0

    @overload
    def my_func(self, a: int, b: int):
        """
        Why this one
        :param a:
        :param b:
        :return:
        """
        return a * b

    @overload
    def my_func(self, a: int, b: int, c: int):
        """
        What the hell
        :param a:
        :param b:
        :param c:
        :return:
        """
        return a * b * c

    @overload
    def my_func(self, *, val: int, other_val: int):
        """
        Now kwargs only
        :param val:
        :param other_val:
        :return:
        """
        return val, other_val

    @overload
    def my_func(self, val: List[int], other_val, /):
        """
        Pos only
        :param val:
        :param other_val:
        :return:
        """
        return [other_val * v for v in val]

    @overload
    def my_func(self, val: List[str], other_val, /):
        """
        Pos only but special for `string` elements
        :param val:
        :param other_val:
        :return:
        """
        return ''.join(val), other_val


if __name__ == "__main__":
    example = Example()
    assert example.my_func() == 0
    assert example.my_func(2, 3, 4) == 24
    assert example.my_func([1, 2, 3], 3) == [3, 6, 9]
    assert example.my_func(2, "3") == "33"
    assert example.my_func([1, 2, 3, 4], 10) == [10, 20, 30, 40]
    assert example.my_func(["1", "2", "3", "4"], 2) == ('1234', 2)
    help(example.my_func)
"""
Help on method my_func:

my_func(val: List[str], other_val, /) method of __main__.Example instance
    Base information about the func
    
    
    Why special
    :param a:
    :param b:
    :return:
    
    
    Why this one
    :param a:
    :param b:
    :return:
    
    
    What the hell
    :param a:
    :param b:
    :param c:
    :return:
    
    
    Now kwargs only
    :param val:
    :param other_val:
    :return:
    
    
    Pos only
    :param val:
    :param other_val:
    :return:
    
    
    Pos only but special for `string` elements
    :param val:
    :param other_val:
    :return:

"""
```