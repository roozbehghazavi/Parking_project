from django.db import models

# Create your models here.
from users.models import CustomUser


class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    room_name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
