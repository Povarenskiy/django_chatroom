from django.db import models
from users.models import User


class ChatRoom(models.Model):
    room_name = models.TextField(max_length=200)
    users = models.ManyToManyField(User)


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    from_user = models.TextField(max_length=50)


