from django.shortcuts import get_object_or_404
from rest_framework import viewsets, response  # Combined import
from .models import Story
from .serializers import StorySerializer
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
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer



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
            # Retrieve post object based on post ID
            post_id = request.data.get('post')
            post = get_object_or_404(Post, id=post_id)
            # Set post object for the comment
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
