from django.http import JsonResponse
from rest_framework.decorators import api_view

from useraccount.models import User
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


@api_view(['GET'])
def create_chat(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "User not found"}, status=404)

    chat = Chat.objects.filter(users=request.user).filter(users=user).first()

    if chat:
        return JsonResponse({"success": True, "chat_id": chat.id})
    else:
        chat = Chat.objects.create()
        chat.users.add(request.user)
        chat.users.add(user)
        return JsonResponse({"success": True, "chat_id": chat.id})
