import json 

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from websocket_app.models import Message, ChatRoom
from users.models import User


class ChatConsumers(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.auth_user_name = self.scope['user']
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        self.room = await database_sync_to_async(self.get_room)()  
        self.history = await database_sync_to_async(self.get_history)()

        async for message in self.history:
            await self.send(text_data=json.dumps({'message': message.text, 'user': message.from_user}))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": user,
            })

        await database_sync_to_async(self.save_message)(message, user)


    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        await self.send(text_data=json.dumps({'message': message, 'user': user}))



    def get_room(self): 
        try:
            room = ChatRoom.objects.get(room_name=self.room_name)
        except:
            room = ChatRoom(room_name=self.room_name)
            room.save()
        user = User.objects.get(username=self.auth_user_name)
        user.chatroom_set.add(room)
        return room


    def get_history(self):
        return Message.objects.filter(chatroom__room_name=self.room_name).all()

    
    def save_message(self, text, username): 
        self.room.message_set.create(text=text, from_user=username)
        