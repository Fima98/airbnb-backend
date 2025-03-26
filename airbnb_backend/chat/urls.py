from django.urls import path  # type: ignore
from . import api

urlpatterns = [
    path('', api.chat_list, name='chat_list'),
    path('<uuid:pk>/', api.chat_detail, name='chat_detail')
]
