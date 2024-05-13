from django.urls import path
from django.views.generic import TemplateView

from .views import (
    SignUpView,
    ProfileView,
    UpdateProfileView,
    DeleteProfileView,
    activate,
    user_calendar
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='user_profile'),
    path('profile/<int:pk>/calendar/', user_calendar, name='user_calendar'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/<int:pk>/delete', DeleteProfileView.as_view(), name='delete_profile'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path(
        'email_verification',
        TemplateView.as_view(template_name='users/email_verification.html'),
        name='email_verification'
    ),
    path('email_verified', TemplateView.as_view(template_name='users/email_verified.html'), name='email_verified'),
    path(
        'email_verification_error',
        TemplateView.as_view(template_name='users/email_verification_error.html'),
        name='email_verification_error'
    )
]
