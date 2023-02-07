import json

from channels.generic.websocket import AsyncWebsocketConsumer
from websocket_app.models import *
from django.conf import settings

# def get_message(chatroom):
#     return chatroom.get_last_message().text


class MessagesConsumers(AsyncWebsocketConsumer):
    
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

            text_data = json.dumps({
                'user': message.user.username,
                'message_text': message.text,
                'message_time': message.create.strftime(settings.MESSAGE_TIME_FORMAT),
                'profile_picture': await message.user.get_profile_picture_url()
            })
            await self.send(text_data)
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
        message = await Message.objects.acreate(chatroom_id=self.room_name, user=self.auth_user, text=text_data_json['message'])
        
  

        message_data = {
            "type": "chat_message",
            "user": self.auth_user.username,
            "message_text": message.text,
            "message_time": message.create.strftime(settings.MESSAGE_TIME_FORMAT),
            'profile_picture': await self.auth_user.get_profile_picture_url()
        }
        
        await self.channel_layer.group_send(self.room_group_name, message_data)
    
        chatroom = await ChatRoom.objects.prefetch_related('users').aget(id=self.room_name)
        rooms_data = {
                "type": "chat_message",
                'room_id': chatroom.id, 
                'room_name': chatroom.name, 
                'last_message':  await chatroom.get_last_message(),
        }
        async for user in chatroom.users.all():
            if user != self.auth_user:
                await Notification.objects.acreate(user=user, chatroom_id=self.room_name)
                rooms_data['notification'] = await chatroom.notification_set.filter(user=user).acount()
            else:
                rooms_data['notification'] = 0
            await self.channel_layer.group_send(f'room_{user}', rooms_data)


    async def chat_message(self, event):
        """
        Парсинг??
        """
        await self.send(text_data=json.dumps(event))


class RoomsConsumers(AsyncWebsocketConsumer):
    
    async def connect(self):
        """
        При подключении к сокету отправляется информация о текущих чатах польхзователя
        """

        self.auth_user = self.scope['user']
        self.room_group_name = f'room_{self.auth_user}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        async for chatroom in self.auth_user.chatroom_set.all().order_by('last_update'):
            await self.send(text_data=json.dumps({
                'room_id': chatroom.id, 
                'room_name': chatroom.name, 
                'notification': await chatroom.notification_set.filter(user=self.auth_user).acount(),
                'last_message':  await chatroom.get_last_message()
            }))


    async def disconnect(self, close_code):
        """
        Разрвы соединения с сокетом 
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

  

    async def chat_message(self, event):
        """
        Парсинг Handler??
        """
        await self.send(text_data=json.dumps(event))




