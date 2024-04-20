from django.urls import path
from .views import *

urlpatterns = [
    path('stories/', StoryCreateDeleteView.as_view(), name='story-create-delete'),
     path('user-data/', UserDataView.as_view(), name='user_data'),
      path('add-comment/', add_comment, name='add-comment'),
      path('comments/<int:post_id>/', get_comments_by_post, name='comments-by-post'),
    
]
