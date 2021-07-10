import pytest
from django.urls import reverse


def test_new_user(new_user):
    """test new user creation"""
    # print(new_user.nickname)
    assert new_user.nickname == "test_username"


def test_new_admin_user(new_admin_user):
    """test new admin user creation"""
    assert new_admin_user.nickname == "test_admin_user"


def test_user_profile_access(new_user, client):
    """check profile access for new authenticated user"""
    user = new_user
    assert user.__str__() == "test_username"

    client.force_login(user)
    url = reverse("profile")
    response = client.get(url)
    assert response.status_code == 200


def test_user_nickname_no_input(user_factory):
    """check no nickname error is raised"""

    with pytest.raises(ValueError) as e:
        test = user_factory.create(nickname="")
    assert str(e.value) == "Nickname is needed to make a new account."


def test_user_password_no_input(user_factory):
    """check no password error is raised"""

    with pytest.raises(ValueError) as e:
        test = user_factory.create(password="")
    assert str(e.value) == "The password cannot be empty."
