# Eidospy

Python SDK for Eidos

## Install

```shell
py -m pip install eidospy
```

## Usage

### read data from a table

```python
from eidospy import Eidos


if __name__ == "__main__":
    eidos = Eidos("https://api.eidos.space/rpc/585067c5-d5e3-4e05-bf60-ba69d75eb7c7")
    space = eidos.space("eidos3")
    table = space.table("532b30d66d984c8a9d9a0ef0245b0afb")
    for row in table.rows():
        print(row)
```

### write data to a table

```python
from eidospy import Eidos

if __name__ == "__main__":
    eidos = Eidos("https://api.eidos.space/rpc/585067c5-d5e3-4e05-bf60-ba69d75eb7c7")
    space = eidos.space("eidos3")
    table = space.table("532b30d66d984c8a9d9a0ef0245b0afb")
    table.add({"title": "test"})
```

## Development

### build

```shell
py -m build
```

### install

```shell
py -m pip install .\dist\eidospy-0.0.1-py3-none-any.whl --force-reinstall
```

### test

```shell
py -m unittest
```
