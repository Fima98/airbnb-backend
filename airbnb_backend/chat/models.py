from django.db import models
import uuid
from useraccount.models import User


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['modified_at']


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='conversations')
    sent_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    sent_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # modified_at -- maybe we i'll add this field later

    class Meta:
        ordering = ['created_at']
