from django.urls import path
from .views import UserBlockAPIView, UserUnblockAPIView,UserListView

urlpatterns = [
    
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/block/', UserBlockAPIView.as_view(), name='user_block'),
    path('users/<int:user_id>/unblock/', UserUnblockAPIView.as_view(), name='user_unblock'),
]
