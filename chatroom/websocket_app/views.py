from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.urls import reverse
from django.views import View
from websocket_app.models import ChatRoom

from users.models import User 


class ChatRoomView(LoginRequiredMixin, View):

    template_name = 'websocket_app/chatroom.html'

    def get(self, request):
        chatrooms = ChatRoom.objects.filter(users=request.user).all()
        
        data = []
        for room in chatrooms:
            room_users = []
            for user in room.users.all():
                if user != request.user:
                    room_users.append(user.username)

            room_users = ' + '.join(room_users)
            data.append({'room_name': room.room_name, 'room_users': room_users}) 

        return render(request, self.template_name, {'data': data})



class CreateView(LoginRequiredMixin, ListView):

    model = User
    template_name = 'websocket_app/create.html'

    def post(self, request):
        chatroom = ChatRoom.objects.create(room_name='Chatroom')
        for username in request.POST.getlist('submit-users'):
            if username:
                user = User.objects.get(username=username)
                chatroom.users.add(user)
        chatroom.users.add(request.user)
        return redirect(reverse('chatroom'))

    