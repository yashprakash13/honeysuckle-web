import pytest
from pytest_factoryboy import register
from selenium import webdriver

from accounts.tests.factories import UserFactory
from profiles.tests.factories import FolderFactory, StoryFactory

register(UserFactory)
register(StoryFactory)
register(FolderFactory)


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


@pytest.fixture
def get_new_folders(db, folder_factory, user_factory):
    user = user_factory.create()
    folder1 = folder_factory.create(folder_name="test_folder_name1", folder_desc="test_folder_desc1", created_by=user)
    folder2 = folder_factory.create(folder_name="test_folder_name2", folder_desc="test_folder_desc2", created_by=user)
    folder3 = folder_factory.create(folder_name="test_folder_name3", folder_desc="test_folder_desc3", created_by=user)
    return (folder1, folder2, folder3)


# ============================LIVE TESTS==================================
@pytest.fixture(autouse=False)
def use_debug_true_for_selenium_tests(settings):
    settings.DEBUG = True


@pytest.fixture(params=["chrome1920"], scope="class")  # , "chrome411"
def driver_init(request):
    binaryPath = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    if request.param == "chrome1920":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.binary_location = binaryPath
        web_driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
        request.cls.browser = "Chrome1920x1080"
    # if request.param == "chrome411":
    #     options = webdriver.ChromeOptions()
    #     options.add_argument("--headless")
    #     options.add_argument("--window-size=411,823")
    #     options.binary_location = binaryPath
    #     web_driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    #     request.cls.browser = "Chrome411x823"

    request.cls.driver = web_driver
    yield
    web_driver.close()
