from datetime import datetime

import pytest

BLOG_COLUMNS = ["id", "title", "content", "is_draft", "date_published", "date_edited"]


@pytest.fixture
def blogs_lazy_collected_polars(create_blogs, all_blogs):
    data_frame = all_blogs.to_polars().collect()

    assert data_frame.height > 0
    assert data_frame.height == all_blogs.count()

    return data_frame


@pytest.fixture
def blogs_eager_collected_polars(create_blogs, all_blogs):
    data_frame = all_blogs.to_eager_polars()

    assert data_frame.height > 0
    assert data_frame.height == all_blogs.count()

    return data_frame


@pytest.fixture
def blogs_lazy_collected_narwhals_from_polars(create_blogs, all_blogs):
    data_frame = all_blogs.to_narwhals_from_polars().collect()

    assert data_frame.shape[0] > 0
    assert data_frame.shape[0] == all_blogs.count()

    return data_frame


@pytest.fixture
def blogs_eager_collected_narwhals_from_polars(create_blogs, all_blogs):
    data_frame = all_blogs.to_narwhals_from_eager_polars()

    assert data_frame.shape[0] > 0
    assert data_frame.shape[0] == all_blogs.count()

    return data_frame


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data_frame_fixture_name",
    [
        "blogs_lazy_collected_polars",
        "blogs_eager_collected_polars",
        "blogs_lazy_collected_narwhals_from_polars",
        "blogs_eager_collected_narwhals_from_polars",
    ],
)
def test_all_on_manager(data_frame_fixture_name, request):
    data_frame = request.getfixturevalue(data_frame_fixture_name)
    assert isinstance(data_frame.get_column("title").head(1).max(), str)
    assert isinstance(data_frame.get_column("content").head(1).max(), str)
    assert isinstance(data_frame.get_column("is_draft").head(1).max(), bool)
    assert isinstance(
        data_frame.drop_nulls("date_edited").get_column("date_edited").head(1).max(),
        datetime,
    )
    assert isinstance(
        data_frame.drop_nulls("date_published")
        .get_column("date_published")
        .head(1)
        .max(),
        datetime,
    )
    assert sorted(data_frame.columns) == sorted(BLOG_COLUMNS)
