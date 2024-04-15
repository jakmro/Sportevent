from django.urls import path
from .views import SignUpView, ProfileView, UpdateProfileView, DeleteProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='user_profile'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/<int:pk>/delete', DeleteProfileView.as_view(), name='delete_profile')
]
