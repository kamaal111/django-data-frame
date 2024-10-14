# django-data-frame

Django ORM data processing using data frames.

- [django-data-frame](#django-data-frame)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Polars](#polars)

## Installation

```shell
# TODO PyPi stuff
```

## Usage

Initializing your Django model with the `DataFrameManager`.

```python
from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django_data_frame import DataFrameManager

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)

    # Add generic variable ([Blog]) to keep on supporting chained query model type hint.
    objects: DataFrameManager[Blog] = DataFrameManager()
```

### Polars

Passing the Django models query set on to Polars to process further.

```python
# Get query as a lazy Polars data frame
Blog.objects.filter(title="Polars").to_polars()

# Get query as a eager Polars data frame
Blog.objects.filter(title="Polars").to_eager_polars()

# Get query as a lazy Narwhals data frame from Polars
Blog.objects.filter(title="Polars").to_narwhals_from_polars()

# Get query as a eager Narwhals data frame from Polars
Blog.objects.filter(title="Polars").to_narwhals_from_eager_polars()
```

To learn more about Polars or Narwhals data frame processing visit their documentation sites

- [Polars](https://docs.pola.rs)
- [Narwhals](https://narwhals-dev.github.io/narwhals/)
