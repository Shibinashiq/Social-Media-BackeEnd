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
    text_content = models.TextField(blank=True) 
    image = models.ImageField(upload_to='story_images/', blank=True, null=True)  
    video = models.FileField(upload_to='story_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Story by {self.user.username} at {self.created_at}'




class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=True)  
    def __str__(self):
        return f'Like by {self.user.username} on {self.post.description}'
    
    
    

class SavedPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    


class Report(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate content'),
        ('violence', 'Violence or harmful behavior'),
        ('other', 'Other'),
    ]

    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    message = models.TextField()
    reporter = models.ForeignKey(CustomUser, related_name='reported_by', on_delete=models.CASCADE)
    reported_Post = models.ForeignKey(Post, related_name='reported_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reporter.username} on {self.reported_Post} for {self.reason}"
    
    
    



