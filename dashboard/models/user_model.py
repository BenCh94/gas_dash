""" User profile model """
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_cryptography.fields import encrypt
from .stock_model import Stock

# Create your models here.

class Profile(models.Model):
    """ The profile for user model """
    colorPalettes = [('dark_knight', 'Dark Knight'), ('ice_man', 'Ice Man'), ('bright_eyes', 'Bright Eyes'), ('gun_metal', 'Gun Metal'), ('acid_rap', 'Acid Rap')]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    palette = models.TextField(default='dark_knight', choices=colorPalettes)
    iex_api_key = encrypt(models.CharField(max_length=100, null=True))

    def __str__(self):
        return self.user.username

    def has_stocks(self):
        """ Check if the user has added any stocks """
        return bool(Stock.objects.filter(user_profile=self).count() > 0)

    def is_admin(self):
        """ Is the user an admin """
        return bool(self.user.is_staff)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # profile creation skipped in testing env to allow manual creation in fixtures
    if created and not kwargs.get('raw', False):
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        instance.profile.save()
