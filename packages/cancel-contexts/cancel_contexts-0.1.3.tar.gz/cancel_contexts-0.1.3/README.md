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
from cancel_contexts.exceptions import ContextCancelledError

ctx = CancelContext()
counter = 0
while ctx:
    counter += 1
    if counter == 10:
        ctx.cancel()

print(ctx.cancelled) # True

try:
    ctx.check_cancelled()
except ContextCancelledError as e:
    print(e) # Context was cancelled
```


```python
from time import sleep
from cancel_contexts import TimeOutContext
from cancel_contexts.exceptions import ContextTimeOutError

ctx = TimeOutContext(10)

print(ctx.cancelled) # False

while ctx:
    sleep(1)
    print(ctx.cancelled) # False

print(ctx.cancelled) # True
try:
    ctx.check_cancelled()
except ContextTimeOutError as e:
    print(e) # Context was timed out
```
