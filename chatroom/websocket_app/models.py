from django.db import models
from users.models import User
from datetime import datetime 
from channels.db import database_sync_to_async


class ChatRoom(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=200, blank=True, null=True)
    last_update = models.DateTimeField(null=True, blank=True, default=None)

    @database_sync_to_async
    def get_last_message(self):
        message = self.message_set.order_by('-create').first()
        return message.text if message else None



class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField(max_length=200)
    create = models.DateTimeField()


    def save(self, *args, **kwargs):
        self.create = datetime.now()
        self.chatroom.last_update = self.create
        self.chatroom.save()
        super(Message, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['create']


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)
    