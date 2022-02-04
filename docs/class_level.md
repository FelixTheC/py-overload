# How to use `strongtyping-pyoverload` on a class based level

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
```
```pycon
>>> foo = Foo()
>>> foo.func("hello")
"Called with `str`"
>>> foo.func(list("hello"))
"Called with `list`"
>>> foo.func(tuple("hello"))
"Called with `tuple`"
```

### Subclasses/Inheritance
can overwrite an existing method __but__ these __must match the exact type definition__ of the __original method__
```python
from strongtyping_pyoverload import overload


class Example:
    @overload
    def other_func(self):
        return 0

    @overload
    def other_func(self, a: int, b: int):
        return (a * a) / b


class Other(Example):

    @overload
    def other_func(self, a):
        return a ** a + a

    @overload
    def other_func(self, a: int, b: int):  # the parameters and everything are exact the same
        return ((a * a) / b) + a
```
```pycon
>>> example = Example()
>>> example.other_func(2, 3)
1.333333333333333
>>>
>>> other = Other()
>>> other.other_func()
0
>>> other.other_func(2)
6
>>> other.other_func(2, 3)
3.333333333333333
```

### A type hint for each parameter??
you only need to have one typed parameter which differ or have a __different length__ for your parameters
```python
from strongtyping_pyoverload import overload


class Other:

    @overload
    def other_func(self, a: int, b):
        return (a + b) * (a + b)

    @overload
    def other_func(self, a: str, b):
        return f'{a.lower()}_{b.lower()}'

    @overload
    def other_func(self, a: list, b):
        return len(a) * b

    @overload
    def other_func(self, a, b, c):
        return a + b + c
```
```pycon
>>> other = Other()
>>> other.other_func("Hello", "World")
hello_world
>>> other.other_func(2, 2)
16
>> > other.other_func([1, 2, 3], 2)
6
>>> other.other_func(2, 3, 4)
9
```

### No function matches
when no function matches with the parameter you're using then an `AttributError` will be raised
```python
from strongtyping_pyoverload import overload


class Example:
    @overload
    def other_func(self, a: int, b: int):
        return (a + b) * (a + b)
```
```pycon
>>> example = Example()
>>> example.other_func("Not", "Supported")
Traceback (most recent call last):
...
AttributeError: Example has no function which matches with your parameters ("Not", "Supported") {}
```