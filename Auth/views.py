from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, PostSerializer
# from django.contrib.auth.models import User
from .models import Profile, Post
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post,CustomUser

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        password = request.data.get('password')
        username=request.data.get('username')

        if not username or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)  
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username':username,
            'userId':user.id,
            
          
            
        }
        return Response(response_data, status=status.HTTP_200_OK)
    


class UpdateProfile(RetrieveUpdateAPIView):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  
        instance = self.get_object()
        profile_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.CustomUser) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserPostsView(APIView):
    def get(self, request, user_id):
        try:
           
            user_posts = Post.objects.filter(user_id=user_id)
           
            serializer = PostSerializer(user_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)