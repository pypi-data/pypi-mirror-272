# Cancel-contexts

This is a simple implementation of cancel-contexts (cancel tokens is C#) in Python. It is inspired by the Go programming language's context package.

## Installation

```bash 
poetry add cancel-contexts
```

or

```bash
pip install cancel-contexts
```


## Usage

```python
from cancel_contexts import CancelContext

ctx = CancelContext()
print(ctx.cancelled) # False
print(bool(ctx)) # True

ctx.cancel()
print(ctx.cancelled) # True
print(bool(ctx)) # False
```

```python
from cancel_contexts import CancelContext

ctx = CancelContext()
counter = 0
while ctx:
    counter += 1
    if counter == 10:
        ctx.cancel()

print(ctx.cancelled) # True
```
