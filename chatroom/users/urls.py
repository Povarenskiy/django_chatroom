from django.urls import path, include

from users.views import RegisterView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]