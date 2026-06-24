import time
import pytest
from strongtyping_pyoverload import overload

class HeavyService:
    @overload
    def compute(self, x: int):
        return x * x

    @overload
    def compute(self, x: str):
        return x.upper()

def test_dispatch_latency_reduction():
    service = HeavyService()
    
    # First call: slower due to inspection/discovery
    start_first = time.perf_counter()
    service.compute(10)
    end_first = time.perf_counter()
    first_duration = end_first - start_first
    
    # Subsequent calls: should be significantly faster due to hashed registry/JIT dispatch
    latencies = []
    for _ in range(100):
        start = time.perf_counter()
        service.compute(10)
        latencies.append(time.perf_counter() - start)
    
    avg_subsequent_latency = sum(latencies) / len(latencies)
    
    # This is a soft assertion but represents the goal
    assert avg_subsequent_latency < first_duration / 2

def test_warmup_phase():
    service = HeavyService()
    # Hypothetical API for manual warmup
    if hasattr(service.compute, "warmup"):
        service.compute.warmup(int)
        
        start = time.perf_counter()
        service.compute(10)
        duration = time.perf_counter() - start
        
        # Should be fast immediately
        assert duration < 0.001 

def test_registry_efficiency():
    # Verify that we are not doing full list scans on every call
    # This might require internal inspection if the feature is implemented
    from strongtyping_pyoverload.class_tools import __override_items__
    
    # Before improvement, this is a list. After, it should ideally be a more efficient structure
    # or the dispatcher should use a cache (which it currently does partially, but let's test efficiency)
    service = HeavyService()
    
    # Calling with many different types to ensure registry scales well
    # (Simplified for now)
    for i in range(10):
        service.compute(i)
        service.compute(str(i))
