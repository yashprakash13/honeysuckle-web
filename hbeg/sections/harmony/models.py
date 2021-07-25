import json

from django.db import models

from .dailyfeed.constants import HP_BOOK_CHOICES

WEBSITE_CHOICES = (
    ("FFN", "Fanfiction.net"),
    ("AO3", "ArchiveOfOurOwn"),
)


class HarmonyMomentsModel(models.Model):
    """for all canon moments of Harmony"""

    moment = models.TextField()
    book = models.CharField(max_length=100, choices=HP_BOOK_CHOICES)

    def __str__(self):
        return self.book + self.moment[:7]

    class Meta:
        verbose_name_plural = "Harmony Moments"


class HarmonyTropesModel(models.Model):
    """for all HHr tropes+fics in them"""

    trope = models.CharField(max_length=100)
    stories = models.CharField(max_length=10000)

    def __str__(self):
        return self.trope

    class Meta:
        verbose_name_plural = "Harmony Tropes and Fics"

    def set_stories(self, value):
        self.stories = json.dumps(value)

    def get_stories(self):
        return json.loads(self.stories)


class HarmonyFicsBlacklist(models.Model):
    """for all dangerous to the heart HHr fics"""

    storyid = models.CharField(max_length=30)
    website = models.CharField(
        choices=WEBSITE_CHOICES,
        max_length=50,
    )
    story_name = models.CharField(max_length=150)
    author_name = models.CharField(max_length=150)
    votes = models.PositiveIntegerField(default=0)
    comments = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.storyid + "_" + self.website

    class Meta:
        verbose_name_plural = "Harmony Blacklisted Fics"
