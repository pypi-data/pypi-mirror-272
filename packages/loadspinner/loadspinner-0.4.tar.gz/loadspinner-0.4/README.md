# loadspinner
![Pepy Total Downlods](https://img.shields.io/pepy/dt/loadspinner)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/loadspinner)
![GitHub repo size](https://img.shields.io/github/repo-size/xyzpw/loadspinner)

A CLI based loading spinner.

## Prerequisites
- Terminal that accepts ANSI codes

## Usage
Creating a spinner:
```python
import loadspinner
spinner = loadspinner.Spinner(spinner_type="classic")
```

Starting the spinner:
```python
spinner.start() # starts the spinner
spinner.stop() # stops the spinner
```

> [!HINT]
> You can also assign a timer to spinners, e.g. `spinner.start(5)` will stop the spinner after 5 seconds.

Usage with context managers:
```python
import loadspinner
with loadspinner.Spinner("newton"):
    input("press enter to stop ")
```

Usage with decorators:
```python
from loadspinner import functionSpinner
@functionSpinner("building")
def doWork():
    # code...
doWork()
```
