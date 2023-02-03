from django.urls import path 

from websocket_app.views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', CreateView.as_view(), name='create'),
    path('get-chatrooms/', ChatRoomsView.as_view(), name='chatrooms'),
]