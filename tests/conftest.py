from datetime import datetime, timezone

import pytest

from tests.test_app.models import Blog


@pytest.fixture
def create_blogs():
    Blog.objects.create(
        title="First",
        content="#Content",
        is_draft=False,
        date_published=datetime(2024, 8, 14, tzinfo=timezone.utc),
    )
    Blog.objects.create(
        title="Second",
        content="#Header",
        is_draft=False,
        date_published=datetime(2024, 9, 14, tzinfo=timezone.utc),
    )
    Blog.objects.create(
        title="Draft",
        content="#ToDo",
        is_draft=True,
        date_edited=datetime(2024, 10, 14, tzinfo=timezone.utc),
    )


@pytest.fixture
def all_blogs_from_manager():
    blogs = Blog.objects

    assert blogs.count() > 0

    return blogs


@pytest.fixture
def all_blogs_from_query_set():
    blogs = Blog.objects.all().all()

    assert blogs.count() > 0

    return blogs
