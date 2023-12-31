from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs): # When we create a user, a profile is automatically created
    print('Profile signal triggered!')
    if created: # If this is the first instance of the user
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = 'Welcome to DevSearch!'
        message = 'Thank you for creating your profile! We are glad you are here!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER, # Sender
            [profile.email], # Recipient
            fail_silently=False
        )

@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False: # If this is the first instance of the profile
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete() # Deletes the user associated with the profile queried
    except:
        pass

''' This is how you do it if you do not use the decorators '''
# post_save.connect(updateUser, sender=Profile)
# post_save.connect(createProfile, sender=Profile)
# post_delete.connect(deleteUser, sender=Profile)