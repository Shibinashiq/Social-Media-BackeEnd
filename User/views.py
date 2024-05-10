from django.shortcuts import get_object_or_404
from rest_framework import viewsets, response 
from .serializers import *
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.views import APIView
from celery import shared_task
import logging
from rest_framework import status
from rest_framework.response import Response
from Auth.models import *
from Auth.serializers import UserSerializer
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
import random





logger = logging.getLogger(__name__)


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        queryset = Story.objects.filter(created_at__gte=one_minute_ago)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class StoryCreateDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            story = serializer.save(user=self.request.user)
            print("Story ID:", story.id)
            print("Story Created At:", story.created_at)
            if story.created_at.date() < timezone.now().date():
                
                delete_after_one_minute.apply_async(args=(story.id,), countdown=60)
                print(story.id)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@shared_task
def delete_after_one_minute(story_id):
    try:
        story = Story.objects.get(pk=story_id)
        story.delete()
        logger.debug(f"Deleted story with id {story_id}")  
    except Story.DoesNotExist:
        logger.error(f"Story with id {story_id} does not exist")
        
        
        
        
class UserDataView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
from rest_framework.decorators import api_view
    
@api_view(['POST'])
def add_comment(request):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():

            post_id = request.data.get('post')
            post = get_object_or_404(Post, id=post_id)

            serializer.validated_data['post'] = post
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_comments_by_post(request, post_id):
    if request.method == 'GET':
        if post_id:
            comments = Comment.objects.filter(post_id=post_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Post ID parameter is missing.'}, status=400)
        
        
        


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(id=comment_id)
   
            if comment.user == request.user:
                comment.delete()
                return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You are not authorized to delete this comment.'}, status=status.HTTP_403_FORBIDDEN)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        
        
        

class LikeCreateView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        

        post_id = data.get('post')
        existing_like = Like.objects.filter(post=post_id, user=request.user).first()
        
        if existing_like:
            existing_like.delete()
            
            post = existing_like.post
            post.total_likes = post.likes.count()
            post.save()

            response_data = {'liked': False, 'like_data': None, 'message': 'Post unliked successfully.'}
            return Response(response_data, status=status.HTTP_200_OK)

        serializer.save()
        
        post_id = data.get('post')
        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post:
                post.total_likes = post.likes.count()
                post.save()

        response_data = {'liked': True, 'like_data': serializer.data, 'message': 'Post liked successfully.'}
        return Response(response_data, status=status.HTTP_201_CREATED)

    
class LikedUsersListView(generics.ListAPIView):
    serializer_class = LikedUserSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if post_id:
            return Like.objects.filter(post_id=post_id)
        else:
            return Like.objects.none()
        
        
        

class CheckLikeView(generics.RetrieveAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        liked = Like.objects.filter(post=post_id, user=request.user).exists()
        return Response({'liked': liked})
    
    

from rest_framework.exceptions import ValidationError

class SavePost(APIView):
    def post(self, request):
        serializer = SavedPostSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user']  # Extract user ID from serializer
            post_id = serializer.validated_data['post_id']  # Extract post ID from serializer
            
            # Check if the post has already been saved by the user
            if SavedPost.objects.filter(user=user_id, post_id=post_id).exists():
                raise ValidationError("This post is already saved")
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    

from django.core.serializers import serialize

def get_saved_posts(request, user_id):
    try:
        saved_posts = SavedPost.objects.filter(user_id=user_id)
        serialized_posts = []
        for saved_post in saved_posts:
            post = Post.objects.get(pk=saved_post.post_id)
            serialized_post = {
                'id': saved_post.id,
                'user': saved_post.user.id,  # Convert CustomUser to its ID
                'post_id': saved_post.post_id,
                'created_at': saved_post.created_at,
                'image': post.image.url,  # Assuming 'image' is the field name for the image URL
            }
            serialized_posts.append(serialized_post)
        return JsonResponse(serialized_posts, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
 
 
 
    
class RemoveSavedPost(APIView):
    def delete(self, request, saved_post_id):  # Change 'post_id' to 'saved_post_id'
        try:
            saved_post = SavedPost.objects.get(id=saved_post_id, user=request.user)
            saved_post.delete()
            return Response("Saved post removed successfully", status=status.HTTP_204_NO_CONTENT)
        except SavedPost.DoesNotExist:
            return Response("Saved post does not exist", status=status.HTTP_404_NOT_FOUND)

    


class RandomUsers(APIView):
    def get(self, request):
        current_user = request.user
        
        users = CustomUser.objects.exclude(id=current_user.id).exclude(followers=current_user)
        
        shuffled_users = list(users)
        random.shuffle(shuffled_users)
        
        random_users = shuffled_users[:3]
        
        serializer = UserSerializer(random_users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    
    
    
@api_view(['POST'])
def submit_report(request):
    serializer = ReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from Auth.serializers import *

class UserDetailsWithPosts(APIView):
    def get(self, request, user_id):
        try:
            # Get user details
            user = CustomUser.objects.get(id=user_id)
            user_serializer = UserSerializer(user)

            # Get user's posts
            posts = Post.objects.filter(user=user)
            posts_serializer = PostSerializer(posts, many=True)

            # Combine user details and posts
            user_data = user_serializer.data
            user_data['posts'] = posts_serializer.data

            return Response(user_data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        

class FollowUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FollowUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_to_follow = serializer.validated_data['user_id']
        current_user = request.user
        
        current_user.following.add(user_to_follow)
        
        user_to_follow.followers.add(current_user)
        
        followers = current_user.followers.all()
        
        follower_serializer = UserSerializer(followers, many=True)
        
        return Response({
            "message": "User followed successfully",
            "followers": follower_serializer.data
        }, status=status.HTTP_200_OK)
    
    

class UnfollowUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UnfollowUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_to_unfollow = serializer.validated_data['user_id']
        current_user = request.user
        
        # Remove the user from the following list
        current_user.following.remove(user_to_unfollow)
        
        # Remove the current user from the followers list of the user being unfollowed
        user_to_unfollow.followers.remove(current_user)
        
        return Response("User unfollowed successfully", status=status.HTTP_200_OK)
