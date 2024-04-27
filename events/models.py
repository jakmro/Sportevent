from django.db import models
from accounts.models import CustomUser
from facilities.models import Facility

class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    sport_type = models.CharField(max_length=128)
    date = models.DateTimeField()
    is_cyclic = models.BooleanField()
    max_people_no = models.IntegerField()
    min_people_no = models.IntegerField()

    def __str__(self):
        return self.name

