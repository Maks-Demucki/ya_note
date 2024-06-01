import pytest
from http import HTTPStatus

from django.urls import reverse


def test_home_availability_for_anonymous_user(client):
    url = reverse('notes:home')
    responce = client.get(url)
    assert responce.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('notes:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    responce = client.get(url)
    assert responce.status_code == HTTPStatus.OK

