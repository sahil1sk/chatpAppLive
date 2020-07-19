from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes,permission_classes # importing decorators
from rest_framework.permissions import IsAuthenticated # here we importing the authentication premission
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .serializer import UserSerializer, FriendzSerializer
from .models import Contact, Message, Friendz

@login_required
def contactList(request, otherId, *args, **kwargs):
	defaultId = 00
	locationName = "global"
	data = otherId
	messages = ''
	contId = 0

	if otherId == 'global':  
		data = "0"
	elif otherId == 'friends':
		data = "00"

	if data == "0":		
		userData = User.objects.all()	 	
	else:		# in else part we getting the contacts
		locationName = "friends"
		participant = User.objects.filter(id=int(data))
		if participant.first():
			if request.user.id != participant.first().id:
				contactId = Contact.objects.filter(Q(ourname=request.user, friend=participant.first())|
												   Q(ourname=participant.first(), friend=request.user)).distinct()

				if not contactId:
					contactIdIs = Contact.objects.create(ourname=request.user, friend=participant.first())
					msg = Message.objects.create(contact=contactIdIs, participant=request.user, content="Just joined the chart")
					Friendz.objects.create(userObj=request.user, friendObj=participant.first())
					Friendz.objects.create(userObj=participant.first(), friendObj=request.user)
					messages = reversed(contactIdIs.message_set.all().order_by('-timestamp')[:10])
				else:
					contactIdIs = contactId.first() # just set the contactid
					Friendz.objects.get_or_create(userObj=request.user, friendObj=participant.first())
					Friendz.objects.get_or_create(userObj=participant.first(), friendObj=request.user)
					messages = reversed(contactId.first().message_set.all().order_by('-timestamp')[:10])
				
				contId = contactIdIs.id # just setting up the contactId to use for communication
				
		userData = Friendz.objects.filter(userObj=request.user)	
		
	
	otherUser = User.objects.filter(id=int(data))
	block = False # setting the default value
	if otherUser.first():
		if otherUser.first().id != request.user.id:
			defaultId = otherUser.first().id # just giving the id
			obj = Friendz.objects.filter(userObj=request.user, friendObj=otherUser.first(), isblock=True)
			if obj.first():
				block = True
			
	return render(request, 'chat/contacts.html', {"messages":messages, "objblock":block,"contactIdIs":contId, "userData":userData, "otherId":defaultId, "otherUser":otherUser.first(), "locationName":locationName})

@api_view(['POST'])
@permission_classes([IsAuthenticated])          # also helps to send the email when new user will register
def searching(request, searchVal, *args, **kwargs):
	if '$global' == request.data.get('locationName'):
		usrObj = User.objects.filter(username__icontains = searchVal)
		if usrObj:
			serializer = UserSerializer(usrObj,many=True)
			return Response({"usrObj":serializer.data}, status=200)
		return Response({"usrObj":""}, status=200)

	else:
		usrObj = Friendz.objects.filter(userObj__username=request.user, friendObj__username__icontains=searchVal)
		if usrObj:
			serializer = FriendzSerializer(usrObj,many=True)
			return Response({"usrObj":serializer.data}, status=200)
		return Response({"usrObj":""}, status=200)



@api_view(['GET'])
@permission_classes([IsAuthenticated])          # also helps to send the email when new user will register
def deleteFriend(request, friendId, *args, **kwargs):
	friendObj = User.objects.filter(id=friendId)[0]
	Friendz.objects.filter(userObj=request.user, friendObj=friendObj).delete()
	return Response({"message":"Success"}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])          # also helps to send the email when new user will register
def blockFriend(request, friendId, *args, **kwargs):
	friendObj = User.objects.filter(id=friendId)[0]
	objectIs = Friendz.objects.filter(userObj=request.user, friendObj=friendObj)[0]
	if objectIs.isblock == False:
		objectIs.isblock = True
	else:
		objectIs.isblock = False
	objectIs.save()
	return Response({"message":"Success"}, status=200)

# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name_json': mark_safe(json.dumps(room_name))  # so here we send the room name with safe sting so that no other html will occur if there is any send in the form of string 
#     })
#AnonymousUser 