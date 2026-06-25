# How to write cleaner Python code with `strongtyping-pyoverload`

Python's flexibility is one of its greatest strengths, but as your codebase grows, managing complex function logic based on varying input types can quickly turn into a messy web of `if isinstance(...)` checks.

What if you could write cleaner, more expressive code by defining multiple versions of the same function, each tailored to specific types?

### ✨ The Solution: Elegant Overloading
With `strongtyping-pyoverload`, you can separate these concerns into distinct, beautifully typed methods. The decorator handles the dispatching logic at runtime, ensuring the right code runs for the right data.

```python
from strongtyping_pyoverload import overload

class DataProcessor:
    @overload
    def process(self, data: str):
        return data.upper()

    @overload
    def process(self, data: list):
        return [item * 2 for item in data]

    @overload
    def process(self, data: MyPydanticModel):
        return data.model_dump()
```

### 🛡️ Native Pydantic Integration
Stop manually validating dictionaries. You can define overloads that take Pydantic models. If you pass a dictionary that matches a model's schema, `strongtyping-pyoverload` can automatically validate it and dispatch to the correct handler.

```python
from pydantic import BaseModel
from strongtyping_pyoverload import overload

class UserCreate(BaseModel):
    name: str
    age: int

class UserHandler:
    @overload
    def process(self, data: UserCreate):
        return f"Creating user {data.name}"

    @overload
    def process(self, data: dict):
        return "Processing raw dictionary"

handler = UserHandler()
# Automatically validates dict against UserCreate schema
print(handler.process({"name": "Alice", "age": 30}))  # Output: Creating user Alice
```

### 🧬 Deep Inheritance & Mixin Support
It plays well with others. Whether you're using deep class hierarchies or mixing in functionality from multiple sources, the `overload` decorator respects the Method Resolution Order (MRO), ensuring that the most specific implementation is always found.

### 🤖 AI-Ready Code
By utilizing `__signature__` and `__annotations__` metadata, this library makes your code more "readable" for AI coding assistants and modern IDEs. Your tools will understand exactly which version of a function is being called, providing better autocompletion and insights.

### ⚡ High Performance
The library uses a structured registry and optimized lookup logic to ensure that the overhead of runtime dispatching is kept to an absolute minimum.

### 🐍 Support for Modern Python Features
Full support for `typing.Annotated`, `Keyword-Only` parameters, and Python 3.13+. It’s built for the modern Python ecosystem.
