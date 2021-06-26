from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StoryContrib, Profile, Tag, StoryRating, ProfileBadges

@receiver(post_save, sender=StoryContrib)
def increase_profile_story_contribs(sender, instance, created, **kwargs):
    """signal to increase the contrib value in profile after story contrib link is accepted
    """
    if not created and instance.is_accepted == True:
        profile_to_update = Profile.objects.filter(member=instance.given_by)[0]
        profile_to_update.story_contribs += 1
        profile_to_update.save()

        # TODO: Fetch story details from link in an external function 

        # delete the story contrib row, don't need it anymore
        instance.delete()


@receiver(post_save, sender=Profile)
def modify_profile_badges(sender, instance, created, **kwargs):
    """signal to change/assign new tags to profile on save
    """
    if not Tag.objects.filter(tag_name='Member'):
        create_all_tags() # WILL BE EXECUTED ONLY ONCE
    
    # profile created
    if created:
        # but first check if tags are present
        # assign initial tags--Early Adopter, Member tags
        # get the profile badge object to update
        ProfileBadges.objects.create(badges_for = instance.member)
        obj_to_update = ProfileBadges.objects.filter(badges_for = instance.member)[0]
        # add the initial badges
        obj_to_update.badges.add(Tag.objects.get(tag_name='Member'))
        if instance.is_early_adopter == True:
            obj_to_update.badges.add(Tag.objects.get(tag_name='Early Adopter'))
    # profile updated
    else:
        obj_to_update = ProfileBadges.objects.filter(badges_for = instance.member)[0]
        num_reads = StoryRating.objects.filter(created_by=instance.member).count()
        num_contribs = instance.story_contribs
        badges_to_assign = get_badges_to_assign(reads=num_reads, contribs=num_contribs)
        if badges_to_assign:
            for badge in badges_to_assign:
                tag = Tag.objects.filter(tag_name=badge)[0]
                obj_to_update.badges.add(tag)

        # check for author update or not
        if instance.is_author == True:
            obj_to_update.badges.add(Tag.objects.get(tag_name='Author'))
        else:
            # check if is_author was turned off in profile settings, meaning we need to remove the Author badge
            if Tag.objects.get(tag_name='Author') in obj_to_update.badges.all():
                obj_to_update.badges.remove(Tag.objects.get(tag_name='Author'))
        



@receiver(post_save, sender=StoryRating)
def modify_profile_badges(sender, instance, created, **kwargs):
    """signal to change/assign new 'reads' badge level to profile on save in StoryRating model
    """
    num_reads = StoryRating.objects.filter(created_by=instance.created_by).count()
    badges_to_assign = get_badges_to_assign(reads=num_reads)
    if badges_to_assign:
        obj_to_update = ProfileBadges.objects.filter(badges_for = instance.created_by)[0]
        for badge in badges_to_assign:
            tag = Tag.objects.filter(tag_name=badge)[0]
            obj_to_update.badges.add(tag)




def get_badges_to_assign(reads=None, contribs=None):
    """Get all badges to add
    """
    badges = []
    if reads:
        # number of stories read
        if reads <= 19 and reads >= 1:
            badges.append('Reader Lv1')
        elif reads <= 51 and reads >= 20:
            badges.append('Reader Lv2')
        elif reads <= 83 and reads >= 52:
            badges.append('Reader Lv3')
        elif reads <= 109 and reads >= 84:
            badges.append('Reader Lv4')
        elif reads <= 141 and reads >= 110:
            badges.append('Reader Lv5')
        elif reads <= 171 and reads >= 142:
            badges.append('Reader Lv6')
        elif reads >= 172:
            badges.append('Reader Lv7')
    
    if contribs:
        # number of contributions done
        if contribs <= 11 and contribs >= 1:
            badges.append('Contributer Lv1')
        elif contribs <= 31 and contribs >= 12:
            badges.append('Contributer Lv2')
        elif contribs <= 51 and contribs >= 32:
            badges.append('Contributer Lv3')
        elif contribs <= 79 and contribs >= 52:
            badges.append('Contributer Lv4')
        elif contribs <= 99 and contribs >= 80:
            badges.append('Contributer Lv5')
        elif contribs <= 121 and contribs >= 100:
            badges.append('Contributer Lv6')
        elif contribs >= 122:
            badges.append('Contributer Lv7')
    
    return badges
    
                


def create_all_tags():
    """EXECUTED ONLY ONCE TO CREATE ALL TAGS IN DATABASE
    """
    Tag.objects.create(tag_name='Maker', tag_color='#ff4500')
    Tag.objects.create(tag_name='Member', tag_color='#f29396')
    Tag.objects.create(tag_name='Author', tag_color='#a54079')
    Tag.objects.create(tag_name='Early Adopter', tag_color='#950f1c')

    Tag.objects.create(tag_name='Reader Lv1', tag_color='#4292b9')
    Tag.objects.create(tag_name='Reader Lv2', tag_color='#6fc4bc')
    Tag.objects.create(tag_name='Reader Lv3', tag_color='#8fd79f')
    Tag.objects.create(tag_name='Reader Lv4', tag_color='#b6a7d8')
    Tag.objects.create(tag_name='Reader Lv5', tag_color='#8d7295')
    Tag.objects.create(tag_name='Reader Lv6', tag_color='#35537a')
    Tag.objects.create(tag_name='Reader Lv7', tag_color='#2b4778')

    Tag.objects.create(tag_name='Contributer Lv1', tag_color='#5d3d52')
    Tag.objects.create(tag_name='Contributer Lv2', tag_color='#714c60')
    Tag.objects.create(tag_name='Contributer Lv3', tag_color='#b28c82')
    Tag.objects.create(tag_name='Contributer Lv4', tag_color='#ef9816')
    Tag.objects.create(tag_name='Contributer Lv5', tag_color='#a34441')
    Tag.objects.create(tag_name='Contributer Lv6', tag_color='#6c0411')
    Tag.objects.create(tag_name='Contributer Lv7', tag_color='#f3911e')


