from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    blocked = models.BooleanField(default=False)
    bio = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True)

  
class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    description = models.TextField()

    def __str__(self):
        return self.description