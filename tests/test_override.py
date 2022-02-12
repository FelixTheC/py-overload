#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 24.01.22
@author: felix
"""
from typing import List

import pytest

from strongtyping_pyoverload import overload


class Example:
    @overload
    def other_func(self):
        return 0

    @overload
    def other_func(self, a: int, b: int):
        return (a + b) * (a + b)

    @overload
    def my_func(self):
        return 0

    @overload
    def my_func(self, a: str, b: str):
        return b + a

    @overload
    def my_func(self, a: int, b: str):
        return b * a

    @overload
    def my_func(self, a: int, b: int):
        return a * b

    @overload
    def my_func(self, a: int, b: int, c: int):
        return a * b * c

    @overload
    def my_func(self, *, val: int, other_val: int):
        return val ** other_val

    @overload
    def my_func(self, val: List[int], other_val, /):
        return [other_val * v for v in val]

    @overload
    def my_func(self, val: List[float], other_val, /):
        return sum(val) / other_val


def test_with_simple_args():
    example = Example()
    assert example.my_func(2, 3) == 6
    assert example.my_func(2, "3") == "33"
    assert example.my_func() == 0
    assert example.my_func(2, 3, 4) == 24
    assert example.my_func("world", "hello") == "helloworld"


def test_with_kwargs():
    example = Example()
    assert example.my_func(other_val=10, val=2) == 1024
    assert example.my_func(2, b=3) == 6
    assert example.my_func(2, c=3, b=4) == 24


def test_with_pos_only():
    example = Example()
    assert example.my_func([1, 2, 3], 2) == [2, 4, 6]
    assert example.my_func([0.1, 0.892, 3.1456], 2) == 2.0688


def test_not_existing_option_raises_default_exception():
    class Other:
        pass

    other = Other()

    with pytest.raises(AttributeError):
        other.missing_function()

    example = Example()
    with pytest.raises(AttributeError):
        example.my_func("This", "Not", "Supported")


def test_inheritance_works_like_expected():
    class Base:
        @overload
        def other_func(self, a: int, b: int):
            return (a + b) * (a + b)

    class Child(Base):
        @overload
        def other_func(self, a: int, b: int):
            return ((a + b) * (a + b)) / (a ** 2)

    base = Base()
    base_result = base.other_func(3, 5)

    child = Child()
    child_result = child.other_func(3, 5)

    assert base_result != child_result


def test_caching_works_pure():
    example = Example()
    assert all(example.my_func(other_val=10, val=2) == 1024 for _ in range(1024))


def test_works_for_normal_functions():
    @overload
    def my_func(a: int, b: int):
        return a * b

    @overload
    def my_func(a: int, b: int, c: int):
        return a * b * c

    assert my_func(2, 3) == 6
    assert my_func(2, 3, 4) == 24


def test_on_module_level():
    from .module_based_test_file import module_func

    assert module_func() == 0
    assert module_func(1, 2) == 1
    assert module_func("1", "2") == 2
    assert module_func(1, "2") == 3
    assert module_func(b=10, a=20) == 1
    assert module_func(10, "20", c=2) == 4


def test_with_args():
    class Bar:
        @overload
        def other_func(self, a: int, b: int):
            return (a + b) * (a + b)

        @overload
        def other_func(self, a: str, *args):
            return f"{a} - {sum(args)}"

        @overload
        def other_func(self, *args):
            return sum(args)

    bar = Bar()
    assert bar.other_func(2, 2) == 16
    assert bar.other_func(2, 3, 4, 5, 6) == 20
    assert bar.other_func("2", 2, 3, 4, 5, 6) == "2 - 20"


def test_with_star_kwargs():
    class FooBar:
        @overload
        def other_func(self, a: int, b: int):
            return (a + b) * (a + b)

        @overload
        def other_func(self, a: str, **kwargs):
            return f"{a} - {sum(kwargs.values())}"

        @overload
        def other_func(self, **kwargs):
            return sum(kwargs.values())

    foobar = FooBar()
    assert foobar.other_func(2, 2) == 16
    assert foobar.other_func(f=2, b=3, c=4, d=5, e=6) == 20
    assert foobar.other_func(a="2", f=2, b=3, c=4, d=5, e=6) == "2 - 20"
    assert foobar.other_func("2", f=2, b=3, c=4, d=5, e=6) == "2 - 20"


def test_with_args_and_kwargs():
    class Foo:
        @overload
        def other_func(self, a: int, b: int):
            return (a + b) * (a + b)

        @overload
        def other_func(self, a: str, b: int, *args, **kwargs):
            return f"{a}, {b} - {sum([*args, *kwargs.values()])}"

        @overload
        def other_func(self, *args, **kwargs):
            return sum([*args, *kwargs.values()])

    foo = Foo()
    assert foo.other_func(2, 2) == 16
    assert foo.other_func(2, 3, 4, d=5, e=6) == 20
    assert foo.other_func("2", 2, 3, 4, d=5, e=6) == "2, 2 - 18"


def test_different_defaults():
    class MyOther:
        @overload
        def other_func(self, a: int, b: int):
            return (a + b) * (a + b)

        @overload
        def other_func(self, *args):
            return sum(args)

        @overload
        def other_func(self, **kwargs):
            return sum([*kwargs.values()]) * 10

        @overload
        def other_func(self, *args, **kwargs):
            return sum([*kwargs.values()]) * 10 + sum(args)

    other = MyOther()
    assert other.other_func(5, 5) == 100
    assert other.other_func(1, 2, 3, 4, 5) == 15
    assert other.other_func(a=1, b=2, c=3, d=4, e=5) == 150
    assert other.other_func(5, 6, a=1, b=2, c=3, d=4, e=5) == 161
