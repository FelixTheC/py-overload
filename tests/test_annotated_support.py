import pytest
from typing import Annotated
from strongtyping_pyoverload import overload

# Simulating validators or using actual ones if available
def gt_zero(v): return v > 0
def lt_zero(v): return v < 0

class GuardedExample:
    @overload
    def process(self, x: Annotated[int, gt_zero]):
        return "Positive"

    @overload
    def process(self, x: Annotated[int, lt_zero]):
        return "Negative"

    @overload
    def process(self, x: int):
        return "Zero"

def test_annotated_guard_dispatch():
    ex = GuardedExample()
    assert ex.process(10) == "Positive"
    assert ex.process(-5) == "Negative"
    assert ex.process(0) == "Zero"

def test_complex_annotated_types():
    class ComplexService:
        @overload
        def handle(self, data: Annotated[list[int], "length > 0"]):
            return sum(data)
        
        @overload
        def handle(self, data: list):
            return 0
            
    service = ComplexService()
    assert service.handle([1, 2, 3]) == 6
    assert service.handle([]) == 0

def test_annotated_with_metadata_fallback():
    # Ensure that if Annotated is used but no specific guard matches, 
    # it still respects the base type
    class FallbackExample:
        @overload
        def do(self, val: Annotated[str, "priority"]):
            return f"Priority {val}"
        
        @overload
        def do(self, val: str):
            return f"Normal {val}"
            
    ex = FallbackExample()
    # If the dispatcher can't evaluate the string "priority", 
    # it should at least match str
    assert "Normal test" in ex.do("test") or "Priority test" in ex.do("test")
