from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class CustomUser(AbstractUser):
    email = models.EmailField(gettext_lazy('email address'), unique=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sports = models.TextField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
