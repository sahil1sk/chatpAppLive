# this file is just like url's but this is for routing means for websockets
from django.urls import re_path, path
from . consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
]

#re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer),