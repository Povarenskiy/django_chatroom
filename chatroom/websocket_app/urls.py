from django.urls import path 

from . import views 


urlpatterns = [
    path('', views.chatroom, name='chatroom'),
    path('create/', views.create, name='create_chatroom'),
]