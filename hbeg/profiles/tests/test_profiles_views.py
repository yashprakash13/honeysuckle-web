import pytest
from django.urls import reverse


def test_access_profile_settings(new_user, client):
    """test access to profile settings page view"""
    user = new_user
    client.force_login(user)
    url = reverse("profile_settings")
    response = client.get(url)
    assert response.status_code == 200


def test_go_to_story_contrib_view(new_user, client):
    """test access to story contrib view"""
    user = new_user
    client.force_login(user)
    url = reverse("story_contrib")
    response = client.get(url)
    assert response.status_code == 200


def test_go_to_folder_add_view(new_user, client):
    """test access to folder add view"""
    user = new_user
    client.force_login(user)
    url = reverse("folder_add")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_new_story_add_to_folder(story_add, client):
    """test story add into db and story detail is protected from unauth view"""
    assert story_add.story_name == "Harry Potter and the Oroborus Light"
    story_id = story_add.story_id
    url = reverse("story_detail", kwargs={"story_id": story_id})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_new_story_add_to_folder_detail(new_user, client):
    """test story detail view is accessible by authenticated user"""
    url = reverse("story_detail", kwargs={"story_id": 2963991})
    client.force_login(new_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_new_story_add_to_folder_add(new_user, client):
    """test story add to folder form view is accessible by authenticated user"""
    url = reverse("story_add", kwargs={"story_id": 2963991})
    client.force_login(new_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_new_story_add_to_folder_rating(new_user, client):
    """test rate story form view is accessible by authenticated user"""
    url = reverse("story_rating", kwargs={"story_id": 2963991})
    client.force_login(new_user)
    response = client.get(url)
    assert response.status_code == 200
