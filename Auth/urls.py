from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('update-profile/<int:user_id>/', UserUpdateView.as_view(), name='update_profile'),
    
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('create-post/', CreatePostView.as_view(), name='add-post'),
    path('user-posts/<int:user_id>/', UserPostsView.as_view(), name='user_posts'),
    path('posts/', PostListInHomePage.as_view(), name='post-list'),
    path('logout/', LogoutView.as_view(), name='logout'),
]