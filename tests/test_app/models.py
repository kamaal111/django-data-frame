from __future__ import annotations

from django.db import models
from django.utils import timezone

from django_data_frame import DataFrameManager


class Blog(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    date_published = models.DateTimeField(default=None, null=True)
    date_edited = models.DateTimeField(default=timezone.now)

    objects: DataFrameManager[Blog] = DataFrameManager()

    @classmethod
    def get_sorted_fields_names(cls):
        return sorted([field.name for field in cls._meta.get_fields()])
