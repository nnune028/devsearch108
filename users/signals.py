from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs): # Whenwe create a user, a profile is automatically created
    print('Profile signal triggered!')
    if created: # If this is the first instance of the user
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete() # Deletes the user associated with the profile queried

''' This is how you do it if you do not use the decorators '''
# post_save.connect(createProfile, sender=Profile)
# post_delete.connect(deleteUser, sender=Profile)