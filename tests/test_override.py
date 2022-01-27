#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 24.01.22
@author: felix
"""
from typing import List

from pyoverload.class_tools import overload


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


def test_with_kwargs():
    example = Example()
    assert example.my_func(other_val=10, val=2) == 1024
    assert example.my_func(2, b=3) == 6
    assert example.my_func(2, c=3, b=4) == 24


def test_with_pos_only():
    example = Example()
    assert example.my_func([1, 2, 3], 2) == [2, 4, 6]
    assert example.my_func([0.1, 0.892, 3.1456], 2) == 2.0688
