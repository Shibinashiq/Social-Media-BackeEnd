from django.urls import path
from .views import *

urlpatterns = [
    path('stories/', StoryCreateDeleteView.as_view(), name='story-create-delete'),
    path('user-data/', UserDataView.as_view(), name='user_data'),
    
    
    #commment
    
    path('add-comment/', add_comment, name='add-comment'),
    path('comments/<int:post_id>/', get_comments_by_post, name='comments-by-post'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete-comment'),

     #Like
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    path('liked-users/<int:post_id>/', LikedUsersListView.as_view(), name='liked-users-list'),
    path('check_like/<int:post_id>/', CheckLikeView.as_view(), name='check_like'),
    
    
    
    #savedCollections
    path('save_post/', SavePost.as_view(), name='save_post'),
    path('saved_posts/<int:user_id>/', get_saved_posts, name='saved_posts'),
    path('remove_saved_post/<int:saved_post_id>/', RemoveSavedPost.as_view(), name='remove_saved_post'),
    
    
    #random users
    
    path('random_users/', RandomUsers.as_view(), name='random_users'),
    
    
    
    #Report
    path('reports/', submit_report, name='submit_report'),
    
    
    
    
    #other users details
    path('user_details_with_posts/<int:user_id>/', UserDetailsWithPosts.as_view(), name='user_details_with_posts'),
    
    
    
    #follow and unfollow
    path('follow/', FollowUserView.as_view(), name='follow-user'),
     path('unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
]
