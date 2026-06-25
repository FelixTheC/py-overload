import pytest
from pydantic import BaseModel, Field, ValidationError
from strongtyping_pyoverload import overload

class UserCreateSchema(BaseModel):
    name: str
    age: int

class UserUpdateSchema(BaseModel):
    id: int
    name: str | None = None

class DataHandler:
    @overload
    def process(self, data: UserCreateSchema):
        return f"Created user {data.name}"

    @overload
    def process(self, data: UserUpdateSchema):
        return f"Updated user {data.id}"

    @overload
    def process(self, data: dict):
        return "Processed dict"

def test_pydantic_schema_dispatching():
    handler = DataHandler()
    
    # Test dispatch to UserCreateSchema
    res1 = handler.process({"name": "Alice", "age": 30})
    assert res1 == "Created user Alice"
    
    # Test dispatch to UserUpdateSchema
    res2 = handler.process({"id": 1, "name": "Bob"})
    assert res2 == "Updated user 1"
    
    # Test dispatch to dict (when it doesn't match schemas)
    res3 = handler.process({"something": "else"})
    assert res3 == "Processed dict"

def test_pydantic_validation_error_fallback():
    # If it looks like a schema but fails validation, it should fallback to dict overload
    handler = DataHandler()
    
    # Invalid for both schemas (missing required fields)
    res = handler.process({"name": "Only Name"})
    assert res == "Processed dict"

def test_pydantic_direct_model_instances():
    handler = DataHandler()
    
    user = UserCreateSchema(name="Charlie", age=25)
    res = handler.process(user)
    assert res == "Created user Charlie"

class ComplexPydanticHandler(DataHandler):
    @overload
    def process(self, data: UserCreateSchema, *, priority: int = 0):
        return f"Created user {data.name} with priority {priority}"

def test_complex_pydantic_dispatching():
    handler = ComplexPydanticHandler()
    
    # Matches ComplexPydanticHandler.process because of keyword arg
    assert handler.process({"name": "Alice", "age": 30}, priority=1) == "Created user Alice with priority 1"
    
    # Matches ComplexPydanticHandler.process even without priority because it has a default value
    # and it is defined in the subclass, which usually takes precedence if it matches.
    assert handler.process({"name": "Alice", "age": 30}) == "Created user Alice with priority 0"
    assert handler.process({"id": 1, "name": "Bob"}) == "Updated user 1"
