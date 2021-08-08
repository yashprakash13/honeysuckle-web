from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models

from .constants import WORK_GENRES, WORK_RATINGS, WORK_STATUS

Member = get_user_model()


class Works(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    description = models.TextField(max_length=999)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(choices=WORK_RATINGS)
    num_words = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=WORK_STATUS)
    genres = models.IntegerField(choices=WORK_GENRES)

    class Meta:
        verbose_name_plural = "Works"
        verbose_name = "Work"
        ordering = ["-updated_on"]

    def __str__(self):
        return self.title


class Chapters(models.Model):
    work = models.ForeignKey(Works, on_delete=models.CASCADE)
    chapter_num = models.PositiveIntegerField()
    words = models.PositiveIntegerField(default=0)
    content = RichTextField()
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Chapters"
        verbose_name = "Chapter"

    def __str__(self):
        return self.work.title + "_" + str(self.chapter_num)


class Reviews(models.Model):
    review = models.TextField(max_length=512)
    review_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    work = models.ForeignKey(Works, on_delete=models.CASCADE)
    review_on = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Reviews"
        verbose_name = "Review"

    def __str__(self):
        return self.review[:50]
