from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile
from .models import Friendz, Message

# so here we create product serializer to return product
class UserSerializer(serializers.ModelSerializer):
    image =  serializers.SerializerMethodField(read_only = True)      
    class Meta:
        model = User
        fields = [
                    'id',
                    'username',
                    'image',
                ] 

    def get_image(self, obj):
        return obj.profile.image.url

class FriendzSerializer(serializers.ModelSerializer):
    friendData = UserSerializer(source='friendObj', read_only=True)
    
    class Meta:
        model = Friendz
        fields = ['friendData'] 

class MessageSerializer(serializers.ModelSerializer):
    userData = UserSerializer(source='participant', read_only=True)
    class Meta:
        model = Message
        fields = [
                    'id',
                    'contact',
                    'userData',
                    'content',
                    'timestamp',
                ] 

    