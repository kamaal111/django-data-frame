from datetime import datetime, timezone

import pytest

from tests.test_app.models import Blog


@pytest.mark.django_db
def test_filter_on_manager(create_blogs):
    data_frame = (
        Blog.objects.filter(
            title="Draft",
            date_edited=datetime(2022, 10, 14, tzinfo=timezone.utc),
            is_draft=True,
        )[:1]
        .to_polars()
        .collect()
    )

    assert data_frame.height == 1
