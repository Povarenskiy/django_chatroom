from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic import CreateView
from .forms import CreateChatForm

from websocket_app.models import ChatRoom, Notification


class ChatRoomsView(LoginRequiredMixin, ListView):
    """Отображение группы чатов и уведомлений пользователя"""
    models = ChatRoom
    template_name = 'websocket_app/rooms.html'

    def get_queryset(self):
        return ChatRoom.objects.filter(users=self.request.user).prefetch_related('users').order_by('-last_update').all()

    def get_context_data(self, **kwargs):
        # Получаем уведомление для пользователя и количество чатов
        user = self.request.user
        object_list = [{'room': room, 'notification': room.notification_set.filter(user=user)} for room in self.get_queryset()]
        return {'object_list' : object_list, 'rooms_count': len(object_list)}


class HomeView(LoginRequiredMixin, TemplateView):
    """Отображение главной старницы"""
    template_name = 'websocket_app/chatroom.html'


class PassRequestToFormViewMixin:
    """Передача пользователя в конструктор формы для исключения его из списка выпадающих контактов"""
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
        

class CreateView(LoginRequiredMixin, PassRequestToFormViewMixin, CreateView):
    """
    Отображение формы создания чата
    """
    template_name = 'websocket_app/create.html'
    form_class = CreateChatForm
    success_url = 'home'


