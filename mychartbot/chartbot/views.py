from django.shortcuts import render, redirect 
from django.http import JsonResponse 
from django.utils import timezone 
import time 
import openai 
from openai import OpenAI 
import os 
from dotenv import load_dotenv 
from .models import Chat  

# Load environment variables
load_dotenv()

# Get API key from environment variable or use the hardcoded key as a fallback
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "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")

# Set API key for both libraries (though this is not strictly necessary with the new OpenAI library)
openai.api_key = OPENAI_API_KEY

# Print success message
print("OpenAI module imported successfully!")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to get bot response
def ask_my_bot(message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return f"I would typically respond to '{message}', but the AI service is temporarily unavailable."

# Main chartbot view to handle POST requests
def chartbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_my_bot(message)  # Get the bot's response
        
        chat = Chat(
            user=request.user if request.user.is_authenticated else None,
            message=message,
            response=response
        )
        chat.save()
        
        return JsonResponse({'message': message, 'response': response})
    
    return render(request, 'chartbot.html')
