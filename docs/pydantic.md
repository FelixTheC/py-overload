# Pydantic Integration

`strongtyping-pyoverload` offers native integration with Pydantic, allowing for powerful runtime dispatching based on data validation.

## How it works
When you define an overload that takes a Pydantic model as a parameter, the decorator will attempt to validate the incoming data against that model's schema. If validation succeeds, that overload is selected.

This means you can pass raw dictionaries to your methods, and they will be automatically converted to Pydantic models and dispatched to the correct handler.

## Example

```python
from pydantic import BaseModel
from strongtyping_pyoverload import overload

class UserCreate(BaseModel):
    name: str
    age: int

class UserUpdate(BaseModel):
    id: int
    name: str | None = None

class UserHandler:
    @overload
    def process(self, data: UserCreate):
        return f"Creating user {data.name}"

    @overload
    def process(self, data: UserUpdate):
        return f"Updating user {data.id}"

    @overload
    def process(self, data: dict):
        return "Processing raw dictionary"

handler = UserHandler()

# Dispatches to UserCreate handler
print(handler.process({"name": "Alice", "age": 30}))  

# Dispatches to UserUpdate handler
print(handler.process({"id": 1, "name": "Bob"}))    

# Dispatches to dict handler (as it doesn't match either schema)
print(handler.process({"something": "else"}))       
```

## Benefits
- **Clean Architecture**: Separate your logic for different data schemas into distinct methods.
- **Automatic Validation**: No need to manually call `Model.model_validate()` inside your functions.
- **Type Safety**: Your methods receive fully validated Pydantic model instances.
- **Flexible APIs**: Allow your users to pass either raw dictionaries or model instances.
