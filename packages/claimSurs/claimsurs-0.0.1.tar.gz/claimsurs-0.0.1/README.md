# Library to show items class

## avalibe class things
- kwargs

## install

install the package using `pip3`:

```python3
pip3 install claimSurs
```

## basic use

### create a file with name 'dayone.py' or other

```python3
#!/usr/bin/env python3
from show_details import show_its

class dog:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @property
    def get_name(self):
        show_its(self.kwargs)

c = dog(name='amiko', years=12, sex='helicopter')
c.get_name
```
### start the proyect

```bash
./dayone.py
```
