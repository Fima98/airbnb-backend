from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Chat, ChatMessage
from .serializers import ChatListSerializer


@api_view(['GET'])
def chat_list(request):
    serializer = ChatListSerializer(request.user.chats.all(), many=True)
    return JsonResponse(serializer.data, safe=False)
