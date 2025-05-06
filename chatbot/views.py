import os
import json
import random
import torch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from django.views import View
from django.shortcuts import render
from .models import ChatLog  # Import the model
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models", "intent_classifier_bert")
DATA_DIR = os.path.join(BASE_DIR, "data")

intents_data = {}
intents_files = ["intents.json", "anxiety.json", "depression.json", "suicidal.json"]
for file in intents_files:
    file_path = os.path.join(DATA_DIR, file)
    with open(file_path, "r", encoding="utf-8") as f:
        intents_data.update(json.load(f))

intent_labels = {idx: intent for idx, intent in enumerate(intents_data.keys())}

model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
tokenizer = DistilBertTokenizer.from_pretrained(MODEL_DIR)

def analyze_sentiment(user_input):
    if any(word in user_input.lower() for word in ["sad", "down", "depressed", "hopeless"]):
        return "negative"
    elif any(word in user_input.lower() for word in ["happy", "excited", "joyful", "hopeful"]):
        return "positive"
    return "neutral"

def get_response(user_input):
    sentiment = analyze_sentiment(user_input)
    inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = torch.argmax(logits, dim=-1).item()
    predicted_intent = intent_labels.get(predicted_class_idx, "fallback")

    responses = intents_data.get(predicted_intent, {}).get("responses", ["I'm here to listen."])
    response = random.choice(responses)

    if sentiment == "negative" and "fallback" not in predicted_intent:
        response += " Remember, things can improve with time. Here's a thought: 'Every day is a new beginning. Take a deep breath, smile, and start again.'"
    
    return predicted_intent, response


@method_decorator(csrf_exempt, name='dispatch')
class ChatbotAPI(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        if not user_input:
            return JsonResponse({"response": "Please enter a message."}, status=400)

        predicted_intent, response = get_response(user_input)

        # Log the chat into the database
        chat_log, created = ChatLog.objects.get_or_create(user_input=user_input)
        if created:
            chat_log.intent_matched = predicted_intent
            chat_log.response_given = response
        else:
            chat_log.increment += 1  # Increment if the user input already exists
        chat_log.save()

        return JsonResponse({"response": response})

@never_cache
@login_required
def chatbot_view(request):
    return render(request, 'chatbot/chatbot.html')