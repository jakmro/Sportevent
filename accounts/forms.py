from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import DateInput
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'avatar',
            'date_of_birth',
            'description',
            'sports'
        )
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'avatar',
            'date_of_birth',
            'description',
            'sports'
        )
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }
