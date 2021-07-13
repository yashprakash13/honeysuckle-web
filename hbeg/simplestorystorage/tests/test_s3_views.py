import pytest
from django.urls import reverse


def test_access_profile_settings(new_user, client):
    """test access to all stories page view"""
    user = new_user
    client.force_login(user)
    url = reverse("library")
    response = client.get(url)
    assert response.status_code == 200
