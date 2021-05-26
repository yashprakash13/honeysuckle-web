from django.db import models
from accounts.models import Member


# define a single story
class Story(models.Model):
    story_name = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['story_name']
        verbose_name_plural = 'Stories'

    def __str__(self):
        return self.story_name



# to define a folder to keep stories
class Folder(models.Model):
    folder_name = models.CharField(max_length=120, unique=True)
    folder_desc = models.CharField(max_length=512, blank=True, null=True)
    BOOL_VISIBILITY_CHOICES = ((True, 'Visible'), (False, 'Invisible'))
    is_visible = models.BooleanField(choices=BOOL_VISIBILITY_CHOICES, default=True)
    created_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='Folders')
    created_at = models.DateTimeField(auto_now_add=True)
    story = models.ManyToManyField(Story, null=True, blank=True)

    def __str__(self):
        return self.folder_name
    
    class Meta:
        verbose_name_plural = 'Folders'
        ordering = ['-created_at']



# to define tags shown on member profile
class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    tag_color = models.CharField(max_length=7)

    def __str__(self):
        return self.tag_name
    

    
# define the profile created upon member registration
class Profile(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    bio = models.CharField(max_length=999, null=True, blank=True)
    profile_pic = models.ImageField(null=True, 
                                    blank=True, 
                                    upload_to="profiles/", 
                                    default="profiles/default_profile_picture.png")
    
    BOOL_ISAUTHOR_CHOICES = ((True, 'Yes,I am.'), (False, 'Nope.'))
    is_author = models.BooleanField(choices=BOOL_ISAUTHOR_CHOICES, default=False)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    
    def __str__(self):
        return str(self.member.nickname)

    
