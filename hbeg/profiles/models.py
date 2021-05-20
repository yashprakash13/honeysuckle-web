from django.db import models
from accounts.models import Member

# to define a folder to keep stories
class Folder(models.Model):
    folder_name = models.CharField(max_length=120, unique=True)
    folder_desc = models.CharField(max_length=512, blank=True, null=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.folder_name

# to define tags shown on member profile
class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    tag_color = models.CharField(max_length=7)

    def __str__(self):
        return self.tag_name
    
    
# the profile created upon member registration
class Profile(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profiles", default="images/default_profile_picture.png")
    is_author = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    

    def __str__(self):
        return str(self.member)

    
