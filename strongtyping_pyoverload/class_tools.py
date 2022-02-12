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
    def contains_args(self):
        if not self.params_:
            return False
        return any(obj[1] == "VAR_POSITIONAL" for obj in self.params_)

    @property
    def contains_kwargs(self):
        if not self.params_:
            return False
        return any(obj[1] == "VAR_KEYWORD" for obj in self.params_)

    @property
    def no_parameter(self):
        return len(self.params_) == 0

    @property
    def first_var_positional_pos(self):
        return [obj[1] == "VAR_POSITIONAL" for obj in self.params_].index(True)

    @property
    def first_var_keyword_pos(self):
        return [obj[1] == "VAR_KEYWORD" for obj in self.params_].index(True)

    def __str__(self):
        params_txt = "_".join(str(param) for param in self.params_)
        return f"{self.func_}_{params_txt}"

    def __repr__(self):
        return f"{self.cls_name_}-{self.func_name_}"

    def _validated_keyword_only(self, other):
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

    def _validate_positional_only(self, other):
        if len(self.params_) != len(other):
            return False
        for param, arg in zip(self.params_, other):
            if param[0] != str(ANY):
                if not check_type(arg, param[0]):
                    return False
        return True

    def _validate_general(self, args_, kwargs_):
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

    def _validate_with_var_positional(self, args_: tuple, kwargs_: dict):
        arg_values = args_[: self.first_var_positional_pos]
        return self._validate_general(arg_values, kwargs_)

    def _validate_with_var_keyword(self, args_: tuple, kwargs_: dict):
        kwarg_values = [obj[2] for obj in list(self.params_)[: self.first_var_keyword_pos]]
        if not any(obj in kwargs_ for obj in kwarg_values) and not args_:
            if kwarg_values:
                return False
            return True
        return self._validate_general(
            args_, {key: kwargs_[key] for key in kwarg_values if key in kwargs_}
        )

    def _validate_with_var_pos_and_keyword(self, args_: tuple, kwargs_: dict):
        if kv := (set([obj[2] for obj in self.params_]) & set(kwargs_.keys())):
            return self._validate_general(tuple(), {key: kwargs_[key] for key in kv})
        else:
            return self._validate_general(args_[: self.first_var_positional_pos], kwargs_)

    def __eq__(self, other):
        if self.is_keyword_only:
            return self._validated_keyword_only(other)
        elif self.is_positional_only:
            return self._validate_positional_only(other)
        else:
            if self.no_parameter and other:
                return False
            args_, kwargs_ = other
            if len(self.params_) != len(args_) + len(kwargs_):
                if self.contains_args and self.contains_kwargs:
                    return self._validate_with_var_pos_and_keyword(args_, kwargs_)
                elif self.contains_args:
                    if len(self.params_) == 1 and not kwargs_:
                        return True
                    elif len(self.params_) == 1 and kwargs_:
                        return False
                    return self._validate_with_var_positional(args_, kwargs_)
                elif self.contains_kwargs:
                    if len(self.params_) == 1 and not args_:
                        return True
                    elif len(self.params_) == 1 and args_:
                        return False
                    return self._validate_with_var_keyword(args_, kwargs_)
                return False
            return self._validate_general(args_, kwargs_)


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


def handle_error(is_module_function, func_class_name, cls_, args, kwargs, /):
    if is_module_function:
        info = pprint.pformat(args) if cls_ or args else pprint.pformat(kwargs)
        raise AttributeError(
            f"`{func_class_name}` has no function which matches with your parameters `{info}`"
        )
    else:
        info = pprint.pformat((cls_, *args)) if cls_ or args else pprint.pformat(kwargs)
        raise AttributeError(f"No function was found which matches your parameters `{info}`")


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
        except KeyError:
            handle_error(is_module_function, func_class_name, cls_, args, kwargs)
        except TypeError:
            if required_function is None:
                handle_error(is_module_function, func_class_name, cls_, args, kwargs)
            else:
                raise

    inner.__doc__ = generate_docstring(func.__name__)
    return inner
