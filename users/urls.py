from django.urls import path
from .views import (
    register_view, login_view, logout_view, get_csrf_token,
    get_current_user, ProfileView, progress_view
)

urlpatterns = [
    # Authentication
    path('csrf/', get_csrf_token, name='csrf'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # User profile and progress
    path('profile/', get_current_user, name='profile'),
    path('profile-detail/', ProfileView.as_view(), name='profile_detail'),
    path('progress/', progress_view, name='progress'),
]
