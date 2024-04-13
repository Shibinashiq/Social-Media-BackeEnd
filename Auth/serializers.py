from rest_framework import serializers
from  .models import Post,CustomUser,Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if CustomUser.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        if CustomUser.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
   
 
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user','bio']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
   
    class Meta:
        model = Post
        fields = [ 'user', 'image', 'description']
        
class LogoutSerializer(serializers.Serializer):
    access_token = serializers.CharField()