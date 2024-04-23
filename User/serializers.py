from rest_framework import serializers
from .models import *

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'user', 'text_content', 'image', 'video', 'created_at']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','post', 'user', 'content', 'created_at']


        
class LikeSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at', 'is_liked']

    def get_is_liked(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return instance.post.likes.filter(user=request.user).exists()
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


        
class LikedUserSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Like
        fields = ['user_name']