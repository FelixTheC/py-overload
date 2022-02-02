# How to write cleaner Pythoncode with `strongtyping-pyoverload`

- With starting of Type-Hints in Python we can now better define what input we expect 
we can say we only want to get a specific kind of Type, or we allow multiple once
```python
def func_a(a: int):
    ...

# in python 3.10 we can also write `str | int` instead of Union
def func(a: Union[str, int]):
    ...
```
- the same works on class level too
```python
class Foo:
    def func_a(self, a: list):
        ...

    # in python 3.10 we can also write `str | int` instead of Union
    def func(self, a: Union[list, tuple]):
        if isinstance(a, list):
            ...
        if isinstance(a, tuple):
            ...
```
- wouldn't it not be nice to have a dedicated method for each parameter without renaming it
```python
class Foo:
    def func(self, a: str):
        print("Called with `str`")

    def func(self, a: list):
        print("Called with `list`")

    def func(self, a: tuple):
        print("Called with `tuple`")
```
- Python will raise no error if you do this but if you call the function
```python
>>> foo = Foo()
>>> foo.func([1, 2, 3])
"Called with `tuple`"
>>> foo.func((1, 2, 3))
"Called with `tuple`"
```
- Python will always use the latest definition for both cases
- This is where the `overload` decorator from `strongtyping-pyoverload` comes into play
```python
from strongtyping_pyoverload import overload


class Foo:
    
    @overload
    def func(self, a: str):
        print("Called with `str`")

    @overload
    def func(self, a: list):
        print("Called with `list`")

    @overload
    def func(self, a: tuple):
        print("Called with `tuple`")


>>> foo = Foo()
>>> foo.func("hello")
"Called with `str`"
>>> foo.func(list("hello"))
"Called with `list`"
>>> foo.func(tuple("hello"))
"Called with `tuple`"
```
- The same works on module level too
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
- I think this will help to write cleaner code as a function now will only be called if the parameters are matching
- Otherwise you will get an `AttributeError`
