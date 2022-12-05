import json

from django.shortcuts import render, redirect
from websocket_app.models import ChatRoom
from django.urls import reverse

def enter(request):
    return render(request, 'websocket_app/enter.html', {})


def chatroom(request):
    if request.user.is_authenticated:
        chatrooms = ChatRoom.objects.filter(users=request.user).all()
        data = []
        for room in chatrooms:
            room_users = []
            for user in room.users.all():
                if user != request.user:
                    room_users.append(user.username)

            room_users = '; '.join(room_users)
            data.append({'room_name': room.room_name, 'room_users': room_users}) 

        return render(request, 'websocket_app/chatroom.html', {'data': data})
    else:
        return redirect(reverse('login'))

def create(request):
    
    return render(request, 'websocket_app/create.html', {})