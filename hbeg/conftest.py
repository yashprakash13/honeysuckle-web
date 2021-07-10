import pytest
from pytest_factoryboy import register

from accounts.tests.factories import UserFactory
from profiles.tests.factories import StoryFactory

register(UserFactory)
register(StoryFactory)


# ==============================APP: ACCOUNTS==============================
@pytest.fixture
def new_user(db, user_factory):
    user = user_factory.create()
    return user


@pytest.fixture
def new_admin_user(db, user_factory):
    user = user_factory.create(nickname="test_admin_user", is_superuser=True)
    return user


@pytest.fixture
def new_user_get_public_profile_link(db, user_factory):
    user = user_factory.create()
    link = user.get_public_profile_link(user.nickname, "localhost:8000")
    return link


# ==============================APP: PROFILES==============================
@pytest.fixture
def folder_add(db, folder_factory):
    new_folder = folder_factory.create()
    return new_folder


@pytest.fixture
def story_add(db, story_factory):
    new_story = story_factory.create()
    return new_story
