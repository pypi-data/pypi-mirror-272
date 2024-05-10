# tiny_progress_bar

Progress Bar for Python 3. Does not use any external libraries and the code is very very tiny.

![Example gif](./example.gif)

# How to use

Import the `progress_bar` function into your script.

Then wrap any iterable with it. Then you'll see it running.

### Example:

```
from tiny_progress_bar import progress_bar as pb
from time import sleep

array = range(10)
counter = 0

for i in pb(array):
    sleep(0.1)  # Your long running process
    counter += i

print(sum(array) == counter)
```

## Bar Length

You can also specify the length of the progress bar by changing the `bar_length` parameter.

Note the minimum `bar_length` is 10.

### Smaller Bar Example

```
# Smaller bar
length = 10
array = range(100)
for _ in pb(array, bar_length=length):
    sleep(0.1)  # Your long running process
```

### Larger Bar Example

```
# Larger bar
length = 100
array = range(100)
for _ in pb(array, bar_length=length):
    sleep(0.1)  # Your long running process
```

# Testing

A test file is included in this package.

Feel free to run `pytest` or `pytest test_tiny_progress_bar.py`
