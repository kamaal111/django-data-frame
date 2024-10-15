from __future__ import annotations

from django.db import models

from django_data_frame import DataFrameManager


class Blog(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    date_published = models.DateTimeField(default=None, null=True)
    date_edited = models.DateTimeField(default=None, null=True)

    objects: DataFrameManager[Blog] = DataFrameManager()
