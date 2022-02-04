# How to use `strongtyping-pyoverload` on a module based level

### Overloading function
- module_a.py
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

### No function matches
when no function matches an `AttributError` will be raised
```pycon
>>> from module_a import module_func
>>> module_func(21)
AttributeError: No function was found which matches your parameters `(21,)`
```