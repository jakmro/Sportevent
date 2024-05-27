import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatMessage
from events.models import Event


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        messages = await self.get_chat_history(self.room_name)
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message['message'],
                'user': message['user__username'],
                'timestamp': message['timestamp'].isoformat()
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        await self.save_message(self.room_name, user, message)

        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat.message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, event_id, user, message):
        event = Event.objects.get(id=event_id)
        ChatMessage.objects.create(event=event, user=user, message=message)

    @database_sync_to_async
    def get_chat_history(self, event_id):
        event = Event.objects.get(id=event_id)
        return list(ChatMessage.objects.filter(event=event).values('user__username', 'message', 'timestamp'))
