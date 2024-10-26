from django.contrib import admin
from .models import Message, Conversation

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'created_at')
    ordering = ('-created_at',)

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    ordering = ('-created_at',)

admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation, ConversationAdmin)