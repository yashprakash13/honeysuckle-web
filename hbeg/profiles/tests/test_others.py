import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_new_story_add(story_add):
    """test story add into db"""
    assert story_add.story_name == "Harry Potter and the Oroborus Light"
