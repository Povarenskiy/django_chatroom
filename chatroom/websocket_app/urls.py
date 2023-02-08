from django.urls import path 

from websocket_app.views import *


urlpatterns = [
    path('', ChatRoomView.as_view(), name='chatroom'),
    path('create/', CreateView.as_view(), name='create'),

]