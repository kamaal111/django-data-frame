from datetime import datetime

import pytest

BLOG_COLUMNS = ["id", "title", "content", "is_draft", "date_published", "date_edited"]


@pytest.fixture
def blogs_lazy_collected_polars(all_blogs_from_manager):
    data_frame = all_blogs_from_manager.to_polars().collect()

    assert data_frame.height > 0
    assert data_frame.height == all_blogs_from_manager.count()

    return data_frame


@pytest.fixture
def blogs_lazy_collected_polars_query_set(all_blogs_from_query_set):
    data_frame = all_blogs_from_query_set.to_polars().collect()

    assert data_frame.height > 0
    assert data_frame.height == all_blogs_from_query_set.count()

    return data_frame


@pytest.fixture
def blogs_eager_collected_polars(all_blogs_from_manager):
    data_frame = all_blogs_from_manager.to_eager_polars()

    assert data_frame.height > 0
    assert data_frame.height == all_blogs_from_manager.count()

    return data_frame


@pytest.fixture
def blogs_eager_collected_polars_query_set(all_blogs_from_query_set):
    data_frame = all_blogs_from_query_set.to_eager_polars()

    assert data_frame.height > 0
    assert data_frame.height == all_blogs_from_query_set.count()

    return data_frame


@pytest.fixture
def blogs_lazy_collected_narwhals_from_polars(all_blogs_from_manager):
    data_frame = all_blogs_from_manager.to_narwhals_from_polars().collect()

    assert data_frame.shape[0] > 0
    assert data_frame.shape[0] == all_blogs_from_manager.count()

    return data_frame


@pytest.fixture
def blogs_lazy_collected_narwhals_from_polars_query_set(all_blogs_from_query_set):
    data_frame = all_blogs_from_query_set.to_narwhals_from_polars().collect()

    assert data_frame.shape[0] > 0
    assert data_frame.shape[0] == all_blogs_from_query_set.count()

    return data_frame


@pytest.fixture
def blogs_eager_collected_narwhals_from_polars(all_blogs_from_manager):
    data_frame = all_blogs_from_manager.to_narwhals_from_eager_polars()

    assert data_frame.shape[0] > 0
    assert data_frame.shape[0] == all_blogs_from_manager.count()

    return data_frame


@pytest.fixture
def blogs_eager_collected_narwhals_from_polars_query_set(all_blogs_from_query_set):
    data_frame = all_blogs_from_query_set.to_narwhals_from_eager_polars()

    assert data_frame.shape[0] > 0
    assert data_frame.shape[0] == all_blogs_from_query_set.count()

    return data_frame


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data_frame_fixture_name",
    [
        "blogs_lazy_collected_polars",
        "blogs_lazy_collected_polars_query_set",
        "blogs_eager_collected_polars",
        "blogs_eager_collected_polars_query_set",
        "blogs_lazy_collected_narwhals_from_polars",
        "blogs_lazy_collected_narwhals_from_polars_query_set",
        "blogs_eager_collected_narwhals_from_polars",
        "blogs_eager_collected_narwhals_from_polars_query_set",
    ],
)
def test_all_on_manager(create_blogs, data_frame_fixture_name, request):
    data_frame = request.getfixturevalue(data_frame_fixture_name)
    assert isinstance(data_frame.get_column("title").sample(1).max(), str)
    assert isinstance(data_frame.get_column("content").sample(1).max(), str)
    assert isinstance(data_frame.get_column("is_draft").sample(1).max(), bool)
    assert isinstance(
        data_frame.get_column("date_edited").sample(1).max(),
        datetime,
    )
    assert isinstance(
        data_frame.drop_nulls("date_published")
        .get_column("date_published")
        .sample(1)
        .max(),
        datetime,
    )
    assert sorted(data_frame.columns) == sorted(BLOG_COLUMNS)
