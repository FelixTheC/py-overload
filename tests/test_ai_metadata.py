import inspect
from typing import Union
from strongtyping_pyoverload import overload

class MetadataExample:
    @overload
    def action(self, x: int) -> int:
        """Handle integer."""
        return x

    @overload
    def action(self, x: str) -> str:
        """Handle string."""
        return x

def test_signature_merging():
    example = MetadataExample()
    sig = inspect.signature(example.action)
    
    # The signature should reflect that it can take int or str
    # and return int or str (or a Union of them)
    params = sig.parameters
    assert "x" in params
    
    # Ideally, the annotation should be a Union of the overloads
    # This helps AI tools like Copilot/Cursor provide better suggestions
    annotation = params["x"].annotation
    assert annotation in (Union[int, str], "Union[int, str]", int | str)

def test_docstring_aggregation():
    example = MetadataExample()
    doc = example.action.__doc__
    
    # Docstring should contain info from all overloads
    assert "Handle integer." in doc
    assert "Handle string." in doc

def test_annotations_update():
    example = MetadataExample()
    # __annotations__ should be present and accurate on the wrapped function
    expected_keys = {"x", "return"}
    assert all(k in example.action.__annotations__ for k in expected_keys)
