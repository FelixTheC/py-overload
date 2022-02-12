# Defaults
Often we want to have only a few special functions but want also a default function like in match-case or in a switch case

## Defaults *args
```python
from strongtyping_pyoverload import overload


class Example:
    @overload
    def other_func(self, a: str, b: str):
        return f"{a.lower()}-{b.lower()}"

    @overload
    def other_func(self, *args):
        return sum(args)
```
```pycon
>>> example = Example()
>>> example.other_func("Foo", "Bar")
foo-bar
>>> example.other_func(1, 2, 3.5, 0.5, -1, 42.12213412)
48.12213412
```
you can also have multiple defaults but then the first parameter must be different
```python
import decimal

from strongtyping_pyoverload import overload


class Example:
    @overload
    def other_func(self, a: str, b: str):
        return f"{a.lower()}-{b.lower()}"

    @overload
    def other_func(self, a: decimal.Decimal, *args):
        return decimal.Decimal(sum(args)) * a

    @overload
    def other_func(self, a: int, *args):
        return sum(args) / a
```
```pycon
>>> example = Example()
>>> example.other_func("Foo", "Bar")
foo-bar
>>> example.other_func(decimal.Decimal(5), 1, 2, 3.5, 0.5, -1, 2.12213412)
40.61067060000000061847913457
>>> example.other_func(1, 2, 3.5, 0.5, -1, 42.12213412)
1.624426824
```

## Defaults **kwargs
```python
from strongtyping_pyoverload import overload


class Example:
    @overload
    def other_func(self, a: str, b: str):
        return f"{a.lower()}-{b.lower()}"

    @overload
    def other_func(self, **kwargs):
        return ", ".join([str(obj) for obj in kwargs.values()])
```
```pycon
>>> example = Example()
>>> example.other_func("Foo", "Bar")
foo-bar
>>> example.other_func(foo="bar", bar=12, foobar=42.21)
bar, 12, 42.21
```
you can also have multiple defaults but then the first parameter must be different
```python
from strongtyping_pyoverload import overload


class Example:
    @overload
    def other_func(self, a: str, b: str):
        return f"{a.lower()}-{b.lower()}"

    @overload
    def other_func(self, val_a: str, **kwargs):
        return val_a + "# " + ", ".join([str(obj) for obj in kwargs.values()])

    @overload
    def other_func(self, val_a: int, **kwargs):
        return ", ".join([str(obj) for obj in kwargs.values()]) * val_a
```
```pycon
>>> example = Example()
>>> example.other_func("Foo", "Bar")
foo-bar
>>> example.other_func("log", foo="bar", bar=12, foobar=42.21)
log# bar, 12, 42.21
>>> example.other_func(val_a="timestamp", foo="bar", bar=12, foobar=42.21)
timestamp# bar, 12, 42.21
>>> example.other_func(2, foo="bar", bar=12, foobar=42.21)
bar, 12, 42.21bar, 12, 42.21
>>> example.other_func(val_a=3, foo="bar", bar=12, foobar=42.21)
bar, 12, 42.21bar, 12, 42.21bar, 12, 42.21
```

## Defaults *args and **kwargs
```python
from strongtyping_pyoverload import overload


class Example:
    @overload
    def other_func(self, a: str, b: str):
        return f"{a.lower()}-{b.lower()}"

    @overload
    def other_func(self, *args, **kwargs):
        return sum(args) * sum(kwargs.values())
```
```pycon
>>> example = Example()
>>> example.other_func("Foo", "Bar")
foo-bar
>>> example.other_func(1, 3, 5, bar=2, foo=4, barfoo=6)
108
```
you can also have multiple defaults but then the first parameter must be different
```python
from strongtyping_pyoverload import overload


class Example:
    @overload
    def other_func(self, a: str, b: str):
        return f"{a.lower()}-{b.lower()}"

    @overload
    def other_func(self, val_a: int, *args, **kwargs):
        return sum(args) * sum(kwargs.values()) / val_a

    @overload
    def other_func(self, val_a: str, *args, **kwargs):
        return f"{val_a}: {sum(args) * sum(kwargs.values())}"
```
```pycon
>>> example = Example()
>>> example.other_func("Foo", "Bar")
foo-bar
>>> example.other_func(10, 3, 5, bar=2, foo=4, barfoo=6)
9.6
>>> example.other_func("example", 3, 5, bar=2, foo=4, barfoo=6)
example: 96
```
