# lib-version
A version-aware library that can can be asked for the version of the library.


## Methods
- `get_version()`: Returns the version of the library.
- `print_version()`: Prints the version of the library.

## Usage
```python
from lib_version_team11 import VersionUtil

# Get the version of the library
version = VersionUtil.get_version()
```

## Installation
```bash
pip install lib_version_team11
```

## Releasing
Create a new git tag and push it to the repository. The CI/CD pipeline will automatically publish the new version to PyPi.

```bash
git tag v0.1.0
git push origin v0.1.0
```

Note: The version number should follow the semantic versioning format, i.e., `vX.Y.Z` where `X`, `Y`, and `Z` are non-negative integers. Note that the version number should be prefixed with a `v`.
