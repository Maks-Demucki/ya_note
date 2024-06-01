from http import HTTPStatus

from django.urls import reverse


def test_home_availability_for_anonymous_user(client):
    url = reverse('notes:home')
    responce = client.get(url)
    assert responce.status_code == HTTPStatus.OK
