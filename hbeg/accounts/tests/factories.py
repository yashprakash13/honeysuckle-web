import factory
from django.contrib.auth import get_user_model

Member = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """to create new users and admin users"""

    class Meta:
        model = Member

    nickname = "test_username"
    password = "test_password"
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(nickname=kwargs["nickname"], password=kwargs["password"])
        else:
            return manager.create_user(nickname=kwargs["nickname"], password=kwargs["password"])
