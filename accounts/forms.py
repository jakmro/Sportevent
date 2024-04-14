from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'avatar',
            'date_of_birth',
            'description',
            'sports'
        ]

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'avatar',
            'date_of_birth',
            'description',
            'sports'
        ]