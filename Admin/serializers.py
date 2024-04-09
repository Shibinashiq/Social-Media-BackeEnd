from rest_framework import serializers
from Auth.models import CustomUser
from Auth.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'blocked']

class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'blocked']
        
        