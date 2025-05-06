from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import default_storage

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', blank = True, null = True)

    def __str__(self):
        return self.user.username

def save(self, *args, **kwargs):
    # If no profile picture is set, or if the existing file doesn't exist,
    # set the default image.
    if not self.profile_picture:
        self.profile_picture = 'profile_pics/default.jpg'
    elif self.profile_picture and not default_storage.exists(self.profile_picture.name):
        # If the file doesn't exist in storage, set to default
        self.profile_picture = 'profile_pics/default.jpg'
    
    super().save(*args, **kwargs)

