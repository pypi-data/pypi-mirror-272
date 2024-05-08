This package contains constants and shared function for PVRADAR SDK and API client

# Installation

```sh
pip install pvradar
```

# Usage

```python
import pvradar
modeled_soiling = pvradar.sdk.get_soiling_ratio({
    'location': { 'lat': 37.63, 'lon': -2.95 },
    'period': { 'year': 2022 }})

modeled_soiling.plot()
```
