import json

from channels.generic.websocket import AsyncWebsocketConsumer
from websocket_app.models import *


class ChatConsumers(AsyncWebsocketConsumer):
    

    async def connect(self):
        """
        При подключении к сокету отправляется история переписки текущего чата
        """
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'
        self.auth_user = self.scope['user']


        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        async for message in Message.objects.select_related('user').filter(chatroom_id=self.room_name):
            await self.send(text_data=json.dumps({'message_text': message.text, 'message_time': message.create.strftime('%H:%m'), 'user': message.user.username}))
            await Notification.objects.filter(user=self.auth_user, chatroom_id=self.room_name).adelete()

   
    async def disconnect(self, close_code):
        """
        Разрвы соединения с сокетом 
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

 
    async def receive(self, text_data):
        """
        Получение нового сообщения
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        data = {
            "type": "chat_message",
            "message": message,
            "user": self.auth_user.username,
        }

        await self.channel_layer.group_send(self.room_group_name, data)
        await Message.objects.acreate(chatroom_id=self.room_name, user=self.auth_user, text=message)
        
        chatroom = await ChatRoom.objects.prefetch_related('users').aget(id=self.room_name)
        await Notification.objects.abulk_create([Notification(user=user, chatroom_id=self.room_name) for user in chatroom.users.all() if user != self.auth_user])
        
  
    async def chat_message(self, event):
        """
        Отправка нового сообщения с указанием автора
        """
        await self.send(text_data=json.dumps({'message': event['message'], 'user': event['user']}))





