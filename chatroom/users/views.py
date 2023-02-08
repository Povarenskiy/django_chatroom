from django.urls import reverse_lazy
from users.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView


class LoginView(LoginView):
    form_class = AuthenticationForm


class RegisterView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('chatroom')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)