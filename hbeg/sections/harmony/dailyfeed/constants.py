import os

from django.conf import settings

AO3_HARMONY_FEED_URL = "https://archiveofourown.org/tags/Hermione%20Granger*s*Harry%20Potter/works?page=1"
FEEDDATA = os.path.join(settings.BASE_DIR, "sections", "harmony", "dailyfeed", "feeddata")
