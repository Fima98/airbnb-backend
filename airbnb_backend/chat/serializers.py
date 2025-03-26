from rest_framework import serializers
from .models import Chat, ChatMessage
from useraccount.serializers import UserDetailSerializer


class ChatListSerializer(serializers.ModelSerializer):
    users = UserDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'users', 'modified_at']

class ChatDetailSerializer(serializers.ModelSerializer):
    users = UserDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'users', 'modified_at']


class ChatMessageSerializer(serializers.ModelSerializer):
    sent_to = UserDetailSerializer(many=False, read_only=True)
    sent_by = UserDetailSerializer(many=False, read_only=True)

    class Meta:
        model = ChatMessage
        fields = ('id', 'message', 'sent_to', 'sent_by')

