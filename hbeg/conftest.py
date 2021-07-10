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
