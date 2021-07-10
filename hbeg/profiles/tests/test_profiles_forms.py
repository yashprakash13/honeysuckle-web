import pytest
from django.urls import reverse
from profiles.forms import (
    AddStoryToFolderForm,
    ContribStoryForm,
    FolderEditForm,
    NewFolderForm,
    ProfileEditForm,
)


@pytest.mark.parametrize(
    "folder_name, folder_desc, is_visible, validity",
    [
        ("test_folder_name", "test_folder_desc", True, True),
        ("", "test_folder_desc", True, False),  # no folder name, so not valid
        ("test_folder_name", "test_folder_desc", False, True),
    ],
)
@pytest.mark.django_db
def test_new_folder_form(folder_name, folder_desc, is_visible, validity):
    """to test folder add form"""
    form = NewFolderForm(
        data={
            "folder_name": folder_name,
            "folder_desc": folder_desc,
            "is_visible": is_visible,
        },
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "folder_name, folder_desc, is_visible, validity",
    [
        ("test_folder_name", "test_folder_desc", True, True),
        ("test_folder_name", "", True, True),
        ("", "test_folder_desc", True, False),  # no folder name, so not valid
        ("test_folder#_name", "test_folder_desc", True, False),
        ("test_folder_name", "test_folder_desc", False, True),
    ],
)
@pytest.mark.django_db
def test_folder_edit_form(folder_name, folder_desc, is_visible, validity):
    """to test folder edit form"""
    form = FolderEditForm(
        data={
            "folder_name": folder_name,
            "folder_desc": folder_desc,
            "is_visible": is_visible,
        },
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "bio, ffn_url, is_author, validity",
    [
        ("test_profile_bio", "test_ffn_url", True, True),
        ("", "", True, True),
        ("", "test_ffn_url", False, True),
        ("test_profile_bio", "", False, True),
    ],
)
@pytest.mark.django_db
def test_profile_settings_form(bio, ffn_url, is_author, validity):
    """to test profile edit form"""
    form = ProfileEditForm(
        data={
            "bio": bio,
            "is_author": is_author,
            "ffn_url": ffn_url,
        },
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "link, validity",
    [
        ("test_story_contrib_link", True),
        ("", False),
    ],
)
@pytest.mark.django_db
def test_contrib_story_form(link, validity):
    """to test story contrib form"""
    form = ContribStoryForm(
        data={
            "link": link,
        },
    )
    assert form.is_valid() is validity
