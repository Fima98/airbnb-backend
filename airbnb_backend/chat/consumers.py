# import json
# from asgiref.sync import sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer

# from chat.models import ChatMessage

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)

#         chat_id = data['data']['chat_id']
#         sent_to_id = data['data']['sent_to_id']
#         name = data['data']['name']
#         body = data['data']['body']

#         # За бажанням можна зберігати повідомлення у базі даних тут

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',  # важливо, щоб цей ключ відповідав імені методу нижче
#                 'body': body,
#                 'name': name
#             }
#         )

#         await self.save_message(chat_id, body, sent_to_id)

#     async def chat_message(self, event):
#         body = event['body']
#         name = event['name']

#         await self.send(text_data=json.dumps({
#             'body': body,
#             'name': name
#         }))

#     @sync_to_async
#     def save_message(self, chat_id, body, sent_to_id):
#         user = self.scope['user']
#         ChatMessage.objects.create(
#             chat_id=chat_id,
#             message=body,
#             sent_to_id=sent_to_id,
#             sent_by=user
#         )


import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        chat_id = data['data']['chat_id']
        sent_to_id = data['data']['sent_to_id']
        name = data['data']['name']
        message = data['data']['message']  # Now using 'message'

        # Optionally save the message in the database
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,  # Using 'message'
                'name': name
            }
        )

        await self.save_message(chat_id, message, sent_to_id)

    async def chat_message(self, event):
        message = event['message']  # Updated key to 'message'
        name = event['name']

        await self.send(text_data=json.dumps({
            'message': message,  # Updated key to 'message'
            'name': name
        }))

    @sync_to_async
    def save_message(self, chat_id, message, sent_to_id):
        user = self.scope['user']
        ChatMessage.objects.create(
            chat_id=chat_id,
            message=message,
            sent_to_id=sent_to_id,
            sent_by=user
        )
