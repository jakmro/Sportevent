from django.db import models
from events.models import Meeting
from accounts.models import CustomUser


class ChatMessage(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f'{self.user.username}: {self.message} ({self.timestamp})'
