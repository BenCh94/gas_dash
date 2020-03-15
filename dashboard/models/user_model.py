""" User profile model """
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .stock_model import Stock

# Create your models here.

class Profile(models.Model):
    """ The profile for user model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

    def has_stocks(self):
        """ Check if the user has added any stocks """
        if Stock.objects.filter(user_profile=self).count() > 0:
            return True
        else:
            return False

    def is_admin(self):
        """ Is the user an admin """
        if self.user.is_staff:
            return True
        else:
            return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
