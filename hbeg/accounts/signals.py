from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member
from profiles.models import Profile

@receiver(post_save, sender=Member)
def create_profile(sender, instance, created, **kwargs):
	"""signal to create profile for a member created
	"""
	if created:
		profile_obj = Profile.objects.create(member=instance)


@receiver(post_save, sender=Member)
def update_profile(sender, instance, created, **kwargs):
	if created == False:
		instance.profile.save()
		

