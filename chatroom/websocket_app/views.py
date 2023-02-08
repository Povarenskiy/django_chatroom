from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .forms import CreateChatForm
from users.forms import UserCreationForm
from websocket_app.models import ChatRoom, Notification


class ChatRoomView(LoginRequiredMixin, TemplateView):
    """Отображение главной старницы"""
    template_name = 'websocket_app/chatroom_extend.html'


class CreateView(LoginRequiredMixin, CreateView):
    """
    Отображение формы создания чата
    """
    template_name = 'websocket_app/create.html'
    form_class = CreateChatForm
    success_url = reverse_lazy('chatroom')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs




