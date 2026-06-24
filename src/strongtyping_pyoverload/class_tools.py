import inspect
import pprint
import typing
from collections import defaultdict
from functools import wraps
from types import MethodType

import itertools
from strongtyping.cached_dict import CachedDict
from strongtyping.strong_typing_utils import check_type

from strongtyping_pyoverload.func_info import FuncInfo

try:
    from pydantic import BaseModel, ValidationError
except (ModuleNotFoundError, ImportError):
    PYDANTIC_INSTALLED = False
else:
    PYDANTIC_INSTALLED = True

__override_items__ = defaultdict(list)
ANY = object()
IGNORE_CHARS = "<function "
START_IDX = len(IGNORE_CHARS)


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


def generate_docstring(lookup_key: tuple[str, str]):
    return "\n".join(
        obj.func_.__doc__ for obj in __override_items__[lookup_key] if obj.func_.__doc__
    )


def find_corresponding_func(func_name, cls_name: str | list[str], args: tuple, kwargs: dict) -> FuncInfo | None:
    pos_or_kwarg_funcs = []
    if isinstance(cls_name, str):
        data = __override_items__[(cls_name, func_name)]
    else:
        data = itertools.chain.from_iterable(
            [
                __override_items__[(cls_name_, func_name)]
                for cls_name_ in cls_name
                if cls_name_ != "object"
            ]
        )

    for info in data:
        if info.is_keyword_only:
            if info == kwargs:
                return info
        elif info.is_positional_only:
            if info == args:
                return info
        elif info.no_parameter and not args and not kwargs:
            return info
        else:
            pos_or_kwarg_funcs.append(info)
    for info in pos_or_kwarg_funcs:
        if PYDANTIC_INSTALLED:
            res = check_pydantic_model(info, args, kwargs)
            if res is not None and res:
                return info
        if info == (args, kwargs):
            return info
    return None


def check_pydantic_model(func_info, args, kwargs) -> bool | None:
    if not PYDANTIC_INSTALLED:
        return False
    is_valid = True
    if any(isinstance(param[0], type) and issubclass(param[0], BaseModel) for param in func_info.params_):
        for idx, param in enumerate(func_info.params_):
            annotation = param[0]
            try:
                # Check if it's a Pydantic BaseModel subclass
                if isinstance(annotation, type) and issubclass(annotation, BaseModel):
                    # Pydantic v2: use model_validate(); raises ValidationError on failure
                    if args:
                        model = annotation.model_validate(args[idx])
                    else:
                        model = annotation.model_validate(kwargs[param[2]])
                else:
                    is_valid = False
            except (AttributeError, TypeError, ValidationError):
                return False
            else:
                if args:
                    func_info.pydantic_params_.append(model)
                else:
                    func_info.pydantic_kwargs_.append(model)
    else:
        return None
    return is_valid


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


def generate_annotations(lookup_key):
    data = __override_items__[lookup_key]
    res = data[0].func_.__annotations__
    for obj in data[1:]:
        for key, val in obj.func_.__annotations__.items():
            try:
                res[key] = set([*res[key], val])
            except TypeError:
                res[key] = set([res[key], val])
            except KeyError:
                res[key] = val
    for key, val in res.items():
        try:
            if len(val) > 1:
                res[key] = typing.Union[*val]
        except TypeError:
            continue
    return res


def overload(func):
    func_info = FuncInfo(func, generate_parameter_infos(func))
    __override_items__[func_info.lookup_key].append(func_info)
    cached_dict = CachedDict()

    @wraps(func)
    def inner(cls_=None, *args, **kwargs):
        is_module_function = is_module(func, cls_) if cls_ is not None else False
        func_class_name = FuncInfo.extract_class_name_from_func(func)
        if is_module_function:
            cached_key = f"{func.__name__}_{func_class_name}_{args}_{kwargs}"
        else:
            cached_key = f"{func.__name__}_{func_class_name}_{(cls_, *args)}_{kwargs}"
        if cached_result := cached_dict.get(cached_key):
            return cached_result

        try:
            class_names = [obj.__name__ for obj in cls_.__class__.__mro__] if cls_ else []
            class_names.append(func_class_name)
            class_names = set(class_names)
        except (AttributeError, TypeError):
            class_names = func_class_name

        if is_module_function or cls_ is None:
            func_info = find_corresponding_func(func.__name__, class_names, args, kwargs)
        else:
            func_info = find_corresponding_func(
                func.__name__, class_names, (cls_, *args), kwargs
            )
        if not func_info:
            raise AttributeError(
                f"No function was found which matches your parameters `{args}_{kwargs}`"
            )
        try:
            arg_values = func_info.pydantic_params_ if func_info.pydantic_params_ else args
            kwarg_values = func_info.pydantic_kwargs_ if func_info.pydantic_kwargs_ else kwargs
            if cls_ is None:
                result = func_info.func_(*arg_values, **kwarg_values)
            else:
                result = func_info.func_(cls_, *arg_values, **kwarg_values)
            cached_dict[cached_key] = result
            return result
        except KeyError:
            handle_error(is_module_function, func_class_name, cls_, args, kwargs)
        except TypeError:
            if func_info is None:
                handle_error(is_module_function, func_class_name, cls_, args, kwargs)
            else:
                raise

    inner.__doc__ = generate_docstring(func_info.lookup_key)
    inner.__annotations__ = generate_annotations(func_info.lookup_key)
    inner.__signature__ = generate_signature(func_info.lookup_key, inner.__annotations__)
    return inner


def generate_signature(lookup_key, merged_annotations):
    data = __override_items__[lookup_key]
    # Collect parameter names in order of first appearance across overloads,
    # skipping 'self'.
    seen = []
    kinds = {}
    defaults = {}
    has_self = False
    for info in data:
        try:
            sig = inspect.signature(info.func_)
        except (TypeError, ValueError):
            continue
        for name, param in sig.parameters.items():
            if name == "self":
                has_self = True
                continue
            if name not in seen:
                seen.append(name)
                kinds[name] = param.kind
                if param.default is not inspect.Parameter.empty:
                    defaults[name] = param.default

    parameters = []
    if has_self:
        parameters.append(inspect.Parameter("self", inspect.Parameter.POSITIONAL_OR_KEYWORD))
    for name in seen:
        kind = kinds.get(name, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        if kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            annotation = inspect.Parameter.empty
        else:
            annotation = merged_annotations.get(name, inspect.Parameter.empty)
        if name in defaults:
            parameters.append(
                inspect.Parameter(name, kind, default=defaults[name], annotation=annotation)
            )
        else:
            parameters.append(inspect.Parameter(name, kind, annotation=annotation))

    return_annotation = merged_annotations.get("return", inspect.Signature.empty)
    try:
        return inspect.Signature(parameters=parameters, return_annotation=return_annotation)
    except ValueError:
        # Fallback: sort parameters by kind to satisfy ordering constraints.
        kind_order = {
            inspect.Parameter.POSITIONAL_ONLY: 0,
            inspect.Parameter.POSITIONAL_OR_KEYWORD: 1,
            inspect.Parameter.VAR_POSITIONAL: 2,
            inspect.Parameter.KEYWORD_ONLY: 3,
            inspect.Parameter.VAR_KEYWORD: 4,
        }
        parameters.sort(key=lambda p: kind_order[p.kind])
        return inspect.Signature(parameters=parameters, return_annotation=return_annotation)
