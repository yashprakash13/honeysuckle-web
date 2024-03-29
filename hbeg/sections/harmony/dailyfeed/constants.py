import os

from django.conf import settings

AO3_HARMONY_FEED_URL = "https://archiveofourown.org/tags/Hermione%20Granger*s*Harry%20Potter/works?page=1"
FEEDDATA = os.path.join(settings.BASE_DIR, "sections", "harmony", "dailyfeed", "feeddata")
HP_BOOK_CHOICES = (
    ("Book 1", "Philosopher's Stone"),
    ("Book 2", "Chamber of Secrets"),
    ("Book 3", "Prisoner of Azkaban"),
    ("Book 4", "Goblet of Fire"),
    ("Book 5", "Order of the Phoenix"),
    ("Book 6", "Half Blood Prince"),
    ("Book 7", "Deathly Hallows"),
)
