from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import CustomUser
from facilities.models import Facility


class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    sport_type = models.CharField(max_length=128)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    repeat_every_n_days = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1)
        ]
    )
    min_people_no = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    max_people_no = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        return self.name


class EventRegistration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')
