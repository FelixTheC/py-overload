# strongtyping-pyoverload
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
![Python application](https://github.com/FelixTheC/py-overload/workflows/Python%20application/badge.svg)
![Python tox](https://github.com/FelixTheC/py-overload/workflows/Python%20tox/badge.svg)
![image](https://codecov.io/gh/FelixTheC/py-overload/graph/badge.svg)

[__*strongtyping-pyoverload*__](https://github.com/FelixTheC/py-overload) provides you with a decorator `overload`, which add overloading capacity similar to C++.

### The Problem
With the introduction of Type-Hints in Python, now one is able to define the intended input types of a certain function. 

This works pretty well, but often we end up in one of the following or similar situation.

```python
def func(a: Union[str, int]):
    if isinstance(a, str):
        ...
    else:
        ...
```

or

```python
def _func_str(a: str):
    ...

def _func_int(a: int):
    ...

def func(a: Union[str, int]):
    if isinstance(a, str):
        _func_str(a)
    else:
        _func_int(a)
```
we define functions and sometimes allow multiple parameters because the end result will be more or less the same, 
but we need to make some additional parsing or so. To have cleaner code we now create also some helper functions.


### The Solution
with the `overload` decorator you can define dedicated functions with the same name.
```python
from typing import List

from strongtyping_pyoverload import overload


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
```
If you now investigate the class with `dir()` you will see (besides a lot of other methods) only one method for `my_func` `['_class_', '_delattr_', ..., '_weakref_', 'my_func']`. 

This also works with pure functions inside of a module

_module_a.py_
```python
from strongtyping_pyoverload import overload


@overload
def module_func():
    return 0


@overload
def module_func(a: int, b: int):
    return a * b


@overload
def module_func(a: str, b: str):
    return a + b
```
```pycon
>>> from module_a import module_func
>>> module_func()
0
>>> module_func(2, 2)
4
>>> module_func("foo", "bar")
"foobar"
```

_With this behavior we can get rid of the Union typehint in some cases. and allow more control over the intended function behaviour_

Detailed information can be found in the **User's guide** section