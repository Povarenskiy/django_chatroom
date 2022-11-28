from django.urls import path 

from . import views 


urlpatterns = [
    path('', views.enter, name='enter'),
    path('<str:room_name>/', views.chatroom, name='chatroom')
]