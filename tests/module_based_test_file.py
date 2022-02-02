#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from strongtyping_pyoverload import overload


@overload
def module_func():
    return 0


@overload
def module_func(a: int, b: int):
    return 1


@overload
def module_func(a: str, b: str):
    return 2


@overload
def module_func(a: int, b: str):
    return 3

