# AddGoto

This package adds a revolutionary feature to Python: the Goto statement<br>
It allows you to feel the essence of early days of C while using a modern language

## Installation

```
pip install addgoto
```

## How to use

```python
from addgoto import goto

x: int = 0
while x < 10:
    x += 1
    print(x)
    goto(line=4)
```

## Limitations

The line you want to jump to must have no indent blocks

For example, the following code won't work

```python
from addgoto import goto

def count_down(n: int) -> None:
    while n > 0:
        n -= 1
        print(n)
        goto(line=4)
```

This limitations will be fixed in the upcomming updated
