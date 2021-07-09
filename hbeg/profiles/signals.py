from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StoryContrib, Profile, StoryRating
from honeysuckleAPI.views import (
    execute_ffn_search_and_response,
    initiate_save_story,
    get_story_id_from_link,
    check_if_story_exists_in_csvdb,
)


@receiver(post_save, sender=StoryContrib)
def increase_profile_story_contribs(sender, instance, created, **kwargs):
    """
    A signal to :
    1. increase the contrib value in profile after story contrib link is accepted, and
    2. save a new story into csv db if not exists with honeysuckleAPI app
    """
    if not created and instance.is_accepted == True:
        profile_to_update = Profile.objects.filter(member=instance.given_by)[0]
        profile_to_update.story_contribs += 1
        profile_to_update.save()

        # Fetch story details from link in an external function from honeysuckleAPI app
        story_id = get_story_id_from_link(instance.link)
        story_all_fields = execute_ffn_search_and_response(story_id)
        # save the story or not, check and save here if needed
        initiate_save_story(story_all_fields)

        # delete the story contrib row, don't need it anymore
        instance.delete()

    elif created:
        if not "fanfiction.net/s/" in instance.link:
            instance.delete()
        story_id = get_story_id_from_link(instance.link)
        if check_if_story_exists_in_csvdb(story_id):
            # delete the story contrib row, don't need it as the story already exists
            instance.delete()  # TODO: display some notification to show that entered story was present already to user
