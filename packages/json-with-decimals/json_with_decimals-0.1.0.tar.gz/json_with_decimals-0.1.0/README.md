A fork of Python's built-in JSON module, but with added support for decimal.Decimal objects.

Install using:
```
pip install json_with_decimals
```

Similar to the proposal given in [this issue](https://github.com/python/cpython/issues/118810).

By default, decoded JSON will return decimal.Decimal objects for real numbers, and the encoder supports decimal.Decimal numbers.

Encoding decimals will disable the speedup from the C encoder, so you can temporarily disable decimal support with the `support_decimal` keyword argument:
```py
import json_with_decimals as json
json.dumps(obj, support_decimal=False)
```