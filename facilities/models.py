from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Facility(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    images = models.ImageField(upload_to='images', blank=True)
    location = models.CharField(max_length=256)
    sport_type = models.CharField(max_length=64)
    capacity = models.IntegerField()
    is_indoor = models.BooleanField(default=False)
    contact_information = models.TextField()

    def __str__(self):
        return self.name


class OpenHours(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='operating_hours')
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f'{self.get_day_display()} - {self.open_time.strftime("%H:%M")} to {self.close_time.strftime("%H:%M")}'

    class Meta:
        unique_together = ('facility', 'day')
        ordering = ['facility', 'day']


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0),
        ]
    )
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
