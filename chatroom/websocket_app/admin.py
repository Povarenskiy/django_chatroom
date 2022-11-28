from django.contrib import admin
from websocket_app.models import Message, ChatRoom


admin.site.register(ChatRoom)
admin.site.register(Message)


