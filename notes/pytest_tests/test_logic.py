import pytest

from pytest_django.asserts import assertRedirects, assertFormError

from pytils.translit import slugify

from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note


def test_user_can_create_note(author_client, author, form_data):
    url = reverse('notes:add')
    responce = author_client.post(url, data=form_data)
    assertRedirects(responce, reverse('notes:success'))
    assert Note.objects.count() == 1
    new_note = Note.objects.get()
    assert new_note.title == form_data['title']
    assert new_note.text == form_data['text']
    assert new_note.slug == form_data['slug']
    assert new_note.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_note(client, form_data):
    url = reverse('notes:add')
    responce = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(responce, expected_url)
    assert Note.objects.count() == 0


def test_not_unique_slug(author_client, note, form_data):
    url = reverse('notes:add')
    form_data['slug'] = note.slug
    responce = author_client.post(url, data=form_data)
    assertFormError(responce, 'form', 'slug', errors=(note.slug + WARNING))
    assert Note.objects.count() == 1


def test_empty_slug(author_client, form_data):
    url = reverse('notes:add')
    form_data.pop('slug')
    responce = author_client.post(url, data=form_data)
    assertRedirects(responce, reverse('notes:success'))
    assert Note.objects.count() == 1
    new_note = Note.objects.get()
    expected_slug = slugify(form_data['title'])
    assert new_note.slug == expected_slug