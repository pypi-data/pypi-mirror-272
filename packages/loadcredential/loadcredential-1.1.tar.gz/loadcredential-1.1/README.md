# loadcredential

This is a simple python package for interfacing with systemd's `LoadCredential` mechanism.
It allows reading secrets from the credentials directory, with a fallback on environment variables if needed.

# Usage

## Basic usage

```python
from loadcredential import Credentials

credentials = Credentials()

secret1 = credentials["SECRET_1"]
```

# Changes

## v1.1 (2024-05-10)

- Added `credentials.get(key, default=None)` which returns a default value and does not raise an error when the key is absent
- Added `credentials.get_json(key, default = None)` which treats the imported secret as json data

## v1.0 (2024-05-09)

Initial version
