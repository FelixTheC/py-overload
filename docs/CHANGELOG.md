## 0.4.4
- Native Pydantic Integration: Automatically validate and dispatch based on Pydantic models.
- Performance Optimization: Implemented optimized registry and lookup logic with caching.
- AI-Ready Metadata: Added `__signature__` and `__annotations__` to overloaded functions for better IDE/AI support.
- Deep Inheritance & Mixin Support: Properly respect MRO during dispatching.
- Modern Python: Added support for `typing.Annotated` and keyword-only parameters.
- Support for Python 3.13 and 3.14.

## 0.3.0
- support *args and **kwargs
- extend Documentation

## 0.2.1
- better error messages 

## 0.2.0
- add caching
- support pure functions

## 0.1.2
- add missing test for Inheritance
- add missing test for raising AttributeError if no matching function is found
- better extraction of corresponding class

## 0.1.1
- initial version