from django.urls import path
from .views import CreatePostView, LogoutView, SignupView, LoginView , UpdateProfile, UserPostsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('update/<int:pk>/', UpdateProfile.as_view(), name='update-profile'),   
    path('create-post/', CreatePostView.as_view(), name='add-post'),
    path('user-posts/<int:user_id>/', UserPostsView.as_view(), name='user_posts'),
    path('logout/', LogoutView.as_view(), name='logout'),
]