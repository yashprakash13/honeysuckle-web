from django.db import models

from .dailyfeed.constants import HP_BOOK_CHOICES


class HarmonyMomentsModel(models.Model):
    """for all canon moments of Harmony"""

    moment = models.TextField()
    book = models.CharField(max_length=100, choices=HP_BOOK_CHOICES)

    def __str__(self):
        return self.book + self.moment[:7]

    class Meta:
        verbose_name_plural = "Harmony Moments"
