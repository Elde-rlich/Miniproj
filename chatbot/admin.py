from django.contrib import admin
from .models import ChatLog

# Register ChatLog model
@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user_input', 'intent_matched', 'response_given', 'increment')
    search_fields = ('user_input', 'intent_matched')