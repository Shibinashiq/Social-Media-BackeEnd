from rest_framework import serializers
from  .models import Post,CustomUser,Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'bio' , 'photo']
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
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio' , 'photo']
    def validate_photo(self, value):
        if not value:
            raise serializers.ValidationError("You must provide an image for your profile.")
        return value
   
 



class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_photo = serializers.SerializerMethodField()
   
    class Meta:
        model = Post
        fields = ['username','id', 'user_photo' ,'image', 'description']
        
    def get_username(self, obj):
        return obj.user.username
    def get_user_photo(self, obj):
        return obj.user.photo.url if obj.user.photo else None

        
class LogoutSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    
    
