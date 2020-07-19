from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime

User = get_user_model()

class Contact(models.Model):
	ourname = models.ForeignKey(User, related_name="ourname",  on_delete=models.CASCADE, null=True, blank=True)
	friend = models.ForeignKey(User, related_name="friend", on_delete=models.CASCADE, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	# def __str__(self):
	# 	return self.id  

class Message(models.Model):
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)
	participant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	# def __str__(self):
	# 	return self.content

	def last_10_messages(self):	# just getting the last 10 messages using time stamp
		return Message.objects.order_by('-timestamp').all()[:10]

class Friendz(models.Model):
	userObj = models.ForeignKey(User, related_name="userObjName",  on_delete=models.CASCADE, null=True, blank=True)
	friendObj = models.ForeignKey(User, related_name="friendObjName", on_delete=models.CASCADE, null=True, blank=True)
	isblock = models.BooleanField(default=False, null=True, blank=False)
	timestamp = models.DateTimeField(auto_now_add=True)