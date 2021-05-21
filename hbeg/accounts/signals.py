from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member
from profiles.models import Profile

@receiver(post_save, sender=Member)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(member=instance)
		print('Profile created!')


@receiver(post_save, sender=Member)
def update_profile(sender, instance, created, **kwargs):
	if created == False:
		instance.profile.save()
		print('Profile updated!')

