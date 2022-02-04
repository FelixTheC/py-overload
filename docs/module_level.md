# How to use `strongtyping-pyoverload` on a module based level

```python
# module_a.py
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

...
# module_b.py
from module_a import module_func
>>> module_func()
0
>>> module_func(2, 2)
4
>>> module_func("foo", "bar")
"foobar"
```