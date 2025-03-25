from rest_framework import serializers
from .models import Chat, ChatMessage
from useraccount.serializers import UserDetailSerializer


class ChatListSerializer(serializers.ModelSerializer):
    users = UserDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'users', 'modified_at']
