from django.contrib import admin
from .models import UserProfile, Chat, Message, ChatList

admin.site.register(UserProfile)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(ChatList)
