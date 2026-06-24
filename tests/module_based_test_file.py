#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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


@overload
def module_func(a: int, b: str):
    return b * a


@overload
def module_func(a: int, b: str, c: int):
    return 4


if __name__ == "__main__":
    print(module_func(1, 2))
    print(module_func)
