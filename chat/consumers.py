import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatMessage
from events.models import Meeting


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
    def save_message(self, meeting_id, user, message):
        meeting = Meeting.objects.get(id=meeting_id)
        ChatMessage.objects.create(meeting=meeting, user=user, message=message)

    @database_sync_to_async
    def get_chat_history(self, meeting_id):
        meeting = Meeting.objects.get(id=meeting_id)
        return list(ChatMessage.objects.filter(meeting=meeting).values('user__username', 'message', 'timestamp'))
