from django.db import models
from django.conf import settings
from Auth.models import *


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models. ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.description}'




class Story(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text_content = models.TextField(blank=True)  # For text content
    image = models.ImageField(upload_to='story_images/', blank=True, null=True)  # For image
    video = models.FileField(upload_to='story_videos/', blank=True, null=True)  # For video
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Story by {self.user.username} at {self.created_at}'




class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=True)  # New field to indicate if the like is active or not

    def __str__(self):
        return f'Like by {self.user.username} on {self.post.description}'