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
        


class SavedPostSerializer(serializers.ModelSerializer):
    post_image = serializers.ImageField(source='post.image', read_only=True)
    post_description = serializers.CharField(source='post.description', read_only=True)

    class Meta:
        model = SavedPost
        fields = ['id', 'user', 'post_id', 'created_at', 'post_image', 'post_description']





class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['reason', 'message', 'reporter', 'reported_Post', 'created_at']
        

    
class FollowUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist")
        return user
    
class UnfollowUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist")
        return user