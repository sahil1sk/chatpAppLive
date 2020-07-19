from django.urls import path, re_path
from .views import searching, contactList, blockFriend, deleteFriend

app_name = 'chat'

urlpatterns = [
	path('chat/<str:otherId>/', contactList, name='contactList'),	# this is for getting the user
	path('search/<str:searchVal>/', searching, name='searching'),
	path('removefriend/<int:friendId>/', deleteFriend, name='deleteFriend'),
	path('blockfriend/<int:friendId>/', blockFriend, name='blockFriend'),
]

#re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),