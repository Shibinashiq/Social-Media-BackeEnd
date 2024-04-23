from django.urls import path
from .views import *

urlpatterns = [
    path('stories/', StoryCreateDeleteView.as_view(), name='story-create-delete'),
    path('user-data/', UserDataView.as_view(), name='user_data'),
    path('add-comment/', add_comment, name='add-comment'),
    path('comments/<int:post_id>/', get_comments_by_post, name='comments-by-post'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete-comment'),

    path('likes/', LikeCreateView.as_view(), name='like-create'),
    #  path('unlike/<int:pk>/', UnlikeView.as_view(), name='unlike'),
     path('liked-users/<int:post_id>/', LikedUsersListView.as_view(), name='liked-users-list'),
     path('check_like/<int:post_id>/', CheckLikeView.as_view(), name='check_like'),
    
    
]
