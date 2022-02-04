#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 24.01.22
@author: felix
"""
import inspect
import pprint
from collections import defaultdict
from functools import wraps
from types import MethodType

from strongtyping.cached_dict import CachedDict
from strongtyping.strong_typing_utils import check_type

__override_items__ = []
ANY = object()
IGNORE_CHARS = "<function "
START_IDX = len(IGNORE_CHARS)


class FuncInfo:
    __slots__ = ("func_", "params_", "func_name_", "cls_name_")

    def __init__(self, func_, params_: list):
        self.func_ = func_
        self.func_name_ = func_.__name__
        self.params_ = params_
        self.cls_name_ = self.extract_class_name_from_func(str(func_))

    @staticmethod
    def extract_class_name_from_func(function_str: str):
        function_mro = function_str[START_IDX : function_str.rfind(" at")]
        try:
            return function_mro.split(".")[-2]
        except IndexError:
            return ""

    @property
    def name(self):
        return self.func_name_

    @property
    def is_keyword_only(self):
        if not self.params_:
            return False
        return all(obj[1] == "KEYWORD_ONLY" for obj in self.params_)

    @property
    def is_positional_only(self):
        if not self.params_:
            return False
        return all(obj[1] == "POSITIONAL_ONLY" for obj in self.params_)

    @property
    def no_parameter(self):
        return len(self.params_) == 0

    def __str__(self):
        params_txt = "_".join(str(param) for param in self.params_)
        return f"{self.func_}_{params_txt}"

    def __eq__(self, other):
        if self.is_keyword_only:
            if len(self.params_) != len(other):
                return False
            for param in self.params_:
                if obj := other.get(param[2]):
                    if param[0] != str(ANY):
                        if not check_type(obj, param[0]):
                            return False
                else:
                    return False
            return True
        elif self.is_positional_only:
            if len(self.params_) != len(other):
                return False
            for param, arg in zip(self.params_, other):
                if param[0] != str(ANY):
                    if not check_type(arg, param[0]):
                        return False
            return True
        else:
            if self.no_parameter and other:
                return False
            args_, kwargs_ = other
            if len(self.params_) != len(args_) + len(kwargs_):
                return False
            pos_args = []
            for param in self.params_:
                if obj := kwargs_.get(param[2]):
                    if param[0] != str(ANY):
                        if not check_type(obj, param[0]):
                            return False
                else:
                    pos_args.append(param)
            for arg, param in zip(args_, pos_args):
                if param[0] != str(ANY):
                    if not check_type(arg, param[0]):
                        return False
            return True


def generate_parameter_infos(func: MethodType):
    params = inspect.signature(func).parameters
    annotations = func.__annotations__
    func_params = {
        val.name: (str(ANY), val.kind.name, val.name)
        for key, val in params.items()
        if val.name != "self"
    }
    for key, val in annotations.items():
        if elem := func_params.get(key):
            func_params[key] = (val, elem[1], elem[2])
    return func_params.values()


def generate_docstring(func_name: str):
    return "\n".join(
        obj.func_.__doc__
        for obj in __override_items__
        if obj.name == func_name and obj.func_.__doc__
    )


def find_corresponding_func(func_name, cls_name, args, kwargs):
    pos_or_kwarg_funcs = []
    data = defaultdict(list)
    for obj in __override_items__:
        if obj.name == func_name:
            data[obj.cls_name_].append(obj)
    subclass = data.pop(cls_name, [])
    [subclass.extend(obj) for obj in list(data.values())]
    for info in subclass:
        if info.is_keyword_only:
            if info == kwargs:
                return info.func_
        elif info.is_positional_only:
            if info == args:
                return info.func_
        elif info.no_parameter and not args and not kwargs:
            return info.func_
        else:
            pos_or_kwarg_funcs.append(info)
    for info in pos_or_kwarg_funcs:
        if info == (args, kwargs):
            return info.func_


def is_module(func_, cls_):
    return cls_.__class__.__name__ in func_.__qualname__


def overload(func):
    func_info = FuncInfo(func, generate_parameter_infos(func))
    __override_items__.append(func_info)
    cached_dict = CachedDict()

    @wraps(func)
    def inner(cls_=None, *args, **kwargs):
        is_module_function = is_module(func, cls_) if cls_ is not None else False
        func_class_name = FuncInfo.extract_class_name_from_func(str(func))
        if is_module_function:
            cached_key = f"{func.__name__}_{func_class_name}_{args}_{kwargs}"
        else:
            cached_key = f"{func.__name__}_{func_class_name}_{(cls_, *args)}_{kwargs}"
        if cached_result := cached_dict.get(cached_key):
            return cached_result

        if is_module_function or cls_ is None:
            required_function = find_corresponding_func(
                func.__name__, func_class_name, args, kwargs
            )
        else:
            required_function = find_corresponding_func(
                func.__name__, func_class_name, (cls_, *args), kwargs
            )
        try:
            if cls_ is None:
                result = required_function(*args, **kwargs)
            else:
                result = required_function(cls_, *args, **kwargs)
            cached_dict[cached_key] = result
            return result
        except (KeyError, TypeError):
            if is_module_function:
                info = pprint.pformat(args) if cls_ or args else pprint.pformat(kwargs)
                raise AttributeError(
                    f"`{func_class_name}` has no function which matches with your parameters `{info}`"
                )
            else:
                info = pprint.pformat((cls_, *args)) if cls_ or args else pprint.pformat(kwargs)
                raise AttributeError(
                    f"No function was found which matches your parameters `{info}`"
                )

    inner.__doc__ = generate_docstring(func.__name__)
    return inner
