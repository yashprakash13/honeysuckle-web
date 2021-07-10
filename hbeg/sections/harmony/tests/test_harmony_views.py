import pytest
from django.urls import reverse


def test_harmony_central_page_access(client):
    """test access to harmony central page view"""
    url = reverse("harmony_central_page")
    response = client.get(url)
    assert response.status_code == 200
