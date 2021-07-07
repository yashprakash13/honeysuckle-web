from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class MemberManager(BaseUserManager):
    def _create_user(self, nickname, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a new user
        """
        if not nickname:
            raise ValueError('Nickname is needed to make a new account.')
        if not password:
            raise ValueError('The password cannot be empty.')
        user = self.model(nickname = nickname, 
                            is_staff=is_staff, 
                            is_active=True,
                            is_superuser=is_superuser, 
                            date_joined = timezone.now(),
                            last_login = timezone.now(), 
                            **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_user(self, nickname, password, **extra_fields):
        return self._create_user(nickname, password, False, False, **extra_fields)
    
    def create_superuser(self, nickname, password, **extra_fields):
        return self._create_user(nickname, password, True, True, **extra_fields)

    def get_public_profile_link(self, nickname):
        nickname =  self.get(nickname=nickname).nickname
        username = nickname[:nickname.index('#')]
        discriminator = nickname[nickname.index('#')+1:]
        public_link = f"{username}.{discriminator}"
        return public_link


class Member(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = MemberManager()

    USERNAME_FIELD = 'nickname'

    def get_absolute_url(self):
        return "/members/%i/" % (self.pk)

    def __str__(self):
        return self.nickname



