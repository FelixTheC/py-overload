# Multiple `__init__` definitions
with the overload decorator it is now possible to have dedicated `__init__` functions

```python
import logging
import time

from strongtyping_pyoverload import overload


class Example:
    @overload
    def __init__(self):
        self.a = int(time.time())
        self.b = self.a * 10
        self.c = None

    @overload
    def __init__(self, a: int):
        self.a = a
        self.b = self.a * 10
        self.c = None

    @overload
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b
        self.c = None

    @overload
    def __init__(self, a: int, b: int, c: logging.Logger):
        self.a = a
        self.b = b
        self.c = c
```
#### Default case
```pycon
>>> example = Example()
>>> example.a
1644660239
>>> example.b
16446602390
>>> example.c
None
```
#### Partial parameter definition
```pycon
>>> example = Example(20)
>>> example.a
20
>>> example.b
200
>>> example.c
None
```
```pycon
>>> example = Example(21, 42)
>>> example.a
21
>>> example.b
42
>>> example.c
None
```
#### Define each parameter
```pycon
>>> example = Example(42, 84, logging.getLogger(__name__))
>>> example.a
42
>>> example.b
84
>>> example.c
<Logger __main__ (WARNING)>
```
#### Not supported types
```pycon
>>> example = Example("42", 84, logging.getLogger(__name__))
AttributeError: `Example` has no function which matches with your parameters `('42', 84, <Logger __main__ (WARNING)>)`
```