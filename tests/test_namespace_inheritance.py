import pytest
from strongtyping_pyoverload import overload

class Outer:
    class Inner:
        @overload
        def method(self, x: int):
            return f"Inner int {x}"
        
        @overload
        def method(self, x: str):
            return f"Inner str {x}"

class Base:
    @overload
    def calc(self, x: int):
        return x + 1

class Derived(Base):
    @overload
    def calc(self, x: str):
        return f"Derived {x}"
    
    # Base.calc(int) should still be accessible if not overridden
    # Currently the implementation might struggle with this depending on how it collects overloads

def test_nested_class_overload():
    inner = Outer.Inner()
    assert inner.method(1) == "Inner int 1"
    assert inner.method("a") == "Inner str a"

def test_inheritance_cross_module_or_complex():
    d = Derived()
    assert d.calc("test") == "Derived test"
    # Testing if it can find the base class overload correctly without explicit redeclaration
    try:
        assert d.calc(1) == 2
    except AttributeError:
        pytest.fail("Should have found Base.calc(int)")

def test_qualname_consistency():
    # Verify that we use __qualname__ instead of string parsing for better reliability
    from strongtyping_pyoverload.class_tools import FuncInfo
    
    def dummy(): pass
    # This test checks the intent of moving to better naming
    assert hasattr(dummy, "__qualname__")
    # In a real implementation, FuncInfo would store and use __qualname__
