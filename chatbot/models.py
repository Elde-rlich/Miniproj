from django.db import models

class ChatLog(models.Model):
    user_input = models.TextField(unique=True)  # Ensure unique inputs for easier increment logic
    intent_matched = models.CharField(max_length=255)  # Store the matched intent
    response_given = models.TextField()  # Store the bot's response
    increment = models.PositiveIntegerField(default=1)  # Count occurrences

    def __str__(self):
        return self.user_input