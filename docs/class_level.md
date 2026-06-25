# How to use `strongtyping-pyoverload` on a class based level

### Overloading methods 
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
Called with `str`
>>> foo.func(list("hello"))
Called with `list`
>>> foo.func(tuple("hello"))
Called with `tuple`
```

### Subclasses/Inheritance
The `overload` decorator respects the Method Resolution Order (MRO), allowing you to extend or override functionality in subclasses.

```python
from strongtyping_pyoverload import overload

class Base:
    @overload
    def process(self, x: int):
        return f"Base int: {x}"

class Derived(Base):
    @overload
    def process(self, x: str):
        return f"Derived str: {x}"

class SubDerived(Derived):
    @overload
    def process(self, x: float):
        return f"SubDerived float: {x}"

obj = SubDerived()
print(obj.process(1))      # Base int: 1
print(obj.process("hi"))   # Derived str: hi
print(obj.process(1.5))    # SubDerived float: 1.5
```

### Mixins
You can also combine functionality from multiple mixin classes.

```python
class Mixin1:
    @overload
    def handle(self, x: int):
        return f"Mixin1: {x}"

class Mixin2:
    @overload
    def handle(self, x: str):
        return f"Mixin2: {x}"

class Combined(Mixin1, Mixin2):
    @overload
    def handle(self, x: float):
        return f"Combined: {x}"

obj = Combined()
print(obj.handle(1))      # Mixin1: 1
print(obj.handle("hi"))   # Mixin2: hi
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

### Variable Parameter length
you can also define the same function with different no. of parameters with the same type
```python
from strongtyping_pyoverload import overload


class Other:

    @overload
    def other_func(self, a: int, b: int):
        return (a + b) * (a + b)
    
    @overload
    def other_func(self, a: int, b: int, c: int):
        return (a + b) * (a + b)
```
```pycon
>>> other = Other()
>>> other.other_func(3, 4)
49
>>> other.other_func(3, 4, 5)
245
```

### No function matches
When no function matches an `AttributeError` will be raised.
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
AttributeError: `Example` has no function which matches with your parameters `('Not', 'Supported'), {}`
```