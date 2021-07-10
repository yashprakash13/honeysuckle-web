import pytest
from pytest_factoryboy import register

from accounts.tests.factories import UserFactory

register(UserFactory)


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
