from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LogoutSerializer, UserSerializer,  PostSerializer, UserUpdateSerializer
# from django.contrib.auth.models import User
from .models import Profile, Post
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
    
from rest_framework_simplejwt.state import token_backend  
    
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                access_token = serializer.validated_data["access_token"]
                token = token_backend.decode(access_token, verify=False)
                if token is not None:
                    token_backend.blacklist(token)
                    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        user = request.user
        if str(user.id) != str(user_id):
            return Response({"message": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if request data is empty
        if not request.data:
            return Response({"message": "No data provided for update."})
        
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save(user=request.user)
            
            request.user.refresh_from_db()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    
    
class UserPostsView(APIView):
    def get(self, request, user_id):
        try:
            user_posts = Post.objects.filter(user_id=user_id)
            serializer = PostSerializer(user_posts, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


class PostListInHomePage(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

