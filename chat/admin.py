from django.contrib import admin
from .models import Contact, Message, Friendz
from django.contrib.admin.options import ModelAdmin

class ContactDisplay(ModelAdmin):
    list_display = ["ourname", "friend"]
    search_fields = ["ourname", "friend"]
    list_filter = ["ourname", "friend"]
admin.site.register(Contact, ContactDisplay)


class MessageDisplay(ModelAdmin):
    list_display = ["contact", "participant", "content"]
    search_fields = ["contact", "participant", "content"]
    list_filter = ["contact", "participant", "content"]
admin.site.register(Message, MessageDisplay)


class FriendzDisplay(ModelAdmin):
    list_display = ["userObj", "friendObj"]
    search_fields = ["userObj", "friendObj"]
    list_filter = ["userObj", "friendObj"]
admin.site.register(Friendz, FriendzDisplay)

