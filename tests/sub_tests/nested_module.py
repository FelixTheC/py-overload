from strongtyping_pyoverload import overload

@overload
def nested_func(a: int):
    return f"int: {a}"

@overload
def nested_func(a: str):
    return f"str: {a}"
