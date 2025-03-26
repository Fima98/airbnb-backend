from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Chat, ChatMessage
from .serializers import ChatListSerializer, ChatDetailSerializer, ChatMessageSerializer


@api_view(['GET'])
def chat_list(request):
    serializer = ChatListSerializer(request.user.chats.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def chat_detail(request, pk):
    chat = request.user.chats.get(pk=pk)
    chat_serializer = ChatDetailSerializer(chat, many=False)

    messages_serializer = ChatMessageSerializer(chat.messages.all(), many=True)

    return JsonResponse({"chat": chat_serializer.data, "messages": messages_serializer.data}, safe=False)

