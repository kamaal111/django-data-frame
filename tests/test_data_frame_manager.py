import pytest

from tests.test_app.models import Blog


@pytest.mark.django_db
def test_blah():
    assert Blog.objects.all().count() == 0
    Blog.objects.create(title="First", content="#Content")
    assert Blog.objects.all().count() == 1
