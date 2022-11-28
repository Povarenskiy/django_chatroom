import json

from django.shortcuts import render
from django.utils.safestring import mark_safe


def enter(request):
    return render(request, 'websocket_app/enter.html', {})


def chatroom(request, room_name):
    return render(request, 'websocket_app/chatroom.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
