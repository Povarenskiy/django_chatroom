from django.urls import path 

from websocket_app.views import *


urlpatterns = [
    path('', EnterView.as_view(), name='enter'),
    path('chatroom/', ChatRoomView.as_view(), name='chatroom'),
    path('create/', CreateView.as_view(), name='create'),

]