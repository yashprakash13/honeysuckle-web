import pytest
from django.urls import reverse


def test_view(client):
    """test access to search page view"""
    url = reverse("search")
    response = client.get(url)
    assert response.status_code == 200


def test_about_view(client):
    """test access to about page view"""
    url = reverse("about")
    response = client.get(url)
    assert response.status_code == 200
