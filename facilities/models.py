from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import CustomUser


class Facility(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images', blank=True)
    location = models.CharField(max_length=256)
    sport_type = models.CharField(max_length=128)
    is_indoor = models.BooleanField()
    contact_information = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('latitude', 'longitude')


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    comment = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Rating: {self.rating} Comment: {self.comment}'

    class Meta:
        unique_together = ('user', 'facility')
