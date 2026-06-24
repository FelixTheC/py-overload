from strongtyping.strong_typing_utils import check_type
ANY = object()


class FuncInfo:
    pydantic_args_: list
    pydantic_kwargs_: dict
    __slots__ = ("func_", "params_", "func_name_", "cls_name_", "pydantic_params_", "pydantic_kwargs_")

    def __init__(self, func_, params_: list):
        self.func_ = func_
        self.func_name_ = func_.__name__
        self.params_ = params_
        self.cls_name_ = self.extract_class_name_from_func(func_)
        self.pydantic_params_ = []
        self.pydantic_kwargs_ = {}

    @staticmethod
    def extract_class_name_from_func(function: object):
        try:
            return function.__qualname__.split(".")[-2]
        except IndexError:
            return ""

    @property
    def name(self) -> str:
        return self.func_name_

    @property
    def lookup_key(self) -> tuple[str, str]:
        return self.cls_name_, self.func_name_

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
