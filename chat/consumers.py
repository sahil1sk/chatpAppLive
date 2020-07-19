import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Contact
from django.contrib.auth.models import User
from .serializer import MessageSerializer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        usrname = data['sendBy']
        contact = data['contactId']
        participant = usrname[1:] # this is for removing the dolar sign

        usrObj = User.objects.filter(username=participant)[0]
        contactObj = Contact.objects.filter(id=int(contact))[0]
        if usrObj and contactObj:
            msg = Message.objects.create(contact=contactObj, participant=usrObj, content=message)
        else:
            msg = json.dumps({"content":"something went wrong"})    

        serializer = MessageSerializer(msg, many=False)


        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': serializer.data,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message":message}))