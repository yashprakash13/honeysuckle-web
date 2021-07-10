import factory
from accounts.tests.factories import UserFactory
from profiles.models import Folder, Story


class FolderFactory(factory.django.DjangoModelFactory):
    """creat new folder factory"""

    class Meta:
        model = Folder

    created_by = factory.SubFactory(UserFactory)
    folder_name = "test_folder_name"
    folder_desc = "test_folder_desc"


class StoryFactory(factory.django.DjangoModelFactory):
    """create story factory"""

    class Meta:
        model = Story

    # mock my fav story
    story_id = 2963991
    story_name = "Harry Potter and the Oroborus Light"
    author_name = "Circusphoenix"
    link = "https://fanfiction.net/s/2963991"
