from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from channels.db import database_sync_to_async


class User(AbstractUser):

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        Profile.objects.get_or_create(user=self)    
    
    @database_sync_to_async
    def get_profile_picture_url(self):
        picture =  self.profile.first().picture
        return picture.url if picture else None

class Profile(models.Model):

    def user_custom_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT / path
        return f'profile_pic/user_{instance.user.id}.{filename.split(".")[-1]}'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to =user_custom_path, default=None, blank=True) 

    
