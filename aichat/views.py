from django.http import JsonResponse
from django.shortcuts import render
import google.generativeai as genai
from django.contrib.auth.decorators import login_required
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure the API key for Gemini AI
genai.configure(api_key="AIzaSyCIjgG29HPVa7_db5NMrQL5O4oBgW18S5o")  # Replace with your actual API key

@login_required
def chat(request):
    model = genai.GenerativeModel("tunedModels/flirt-paradise-luouxnlaxjx2")  # Initialize the Gemini model

    if request.method == 'POST':
        # Get user input from the form
        user_input = request.POST.get('user_input', '')

        # Generate a response using Gemini AI without safety filters
        try:
            response = model.generate_content(
                user_input,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            return JsonResponse({'user_input': user_input, 'response': response.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        # If it's a GET request, just render the empty form
        return render(request, './aichat/aichat.html')
