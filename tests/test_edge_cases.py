import pytest
from strongtyping_pyoverload import overload
from strongtyping_pyoverload.exception import InvalidOverloadException


class Base:
    @overload
    def process(self, x: int):
        return f"Base int: {x}"

class Derived(Base):
    @overload
    def process(self, x: str):
        return f"Derived str: {x}"

class SubDerived(Derived):
    @overload
    def process(self, x: float):
        return f"SubDerived float: {x}"

def test_deeper_inheritance():
    obj = SubDerived()
    assert obj.process(1) == "Base int: 1"
    assert obj.process("hello") == "Derived str: hello"
    assert obj.process(1.5) == "SubDerived float: 1.5"

class Mixin1:
    @overload
    def handle(self, x: int):
        return f"Mixin1 int: {x}"

class Mixin2:
    @overload
    def handle(self, x: str):
        return f"Mixin2 str: {x}"

class Combined(Mixin1, Mixin2):
    @overload
    def handle(self, x: float):
        return f"Combined float: {x}"

def test_mixins():
    obj = Combined()
    assert obj.handle(1) == "Mixin1 int: 1"
    assert obj.handle("hello") == "Mixin2 str: hello"
    assert obj.handle(1.5) == "Combined float: 1.5"

class PartialTyping:
    @overload
    def compute(self, x: int, y):
        return f"int, any: {x}, {y}"
    
    @overload
    def compute(self, x: str, y: int):
        return f"str, int: {x}, {y}"

def test_partial_typing():
    obj = PartialTyping()
    assert obj.compute(1, "any") == "int, any: 1, any"
    assert obj.compute("hello", 2) == "str, int: hello, 2"

class KeywordOnly:
    @overload
    def find(self, *, name: str):
        return f"name: {name}"
    
    @overload
    def find(self, *, id: int):
        return f"id: {id}"

def test_keyword_only():
    obj = KeywordOnly()
    assert obj.find(name="Alice") == "name: Alice"
    assert obj.find(id=42) == "id: 42"
    with pytest.raises(InvalidOverloadException):
        obj.find("Alice")

class MixedArgs:
    @overload
    def info(self, name: str, *, age: int):
        return f"str, age={age}"
    
    @overload
    def info(self, id: int, *, active: bool):
        return f"int, active={active}"

def test_mixed_args():
    obj = MixedArgs()
    assert obj.info("Bob", age=30) == "str, age=30"
    assert obj.info(1, active=True) == "int, active=True"

class DeepInheritancePartialTyping(SubDerived):
    @overload
    def process(self, x: int, y):
        return f"Deep int, any: {x}, {y}"

def test_deep_inheritance_partial_typing():
    obj = DeepInheritancePartialTyping()
    assert obj.process(1) == "Base int: 1"
    assert obj.process("hello") == "Derived str: hello"
    assert obj.process(1.5) == "SubDerived float: 1.5"
    assert obj.process(1, "extra") == "Deep int, any: 1, extra"
