from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.timezone import now
from .models import Profile
from gender.models import UserPayment
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


@login_required
def chat(request):
    model = genai.GenerativeModel("tunedModels/flirt-paradise-luouxnlaxjx2")  # Default model initialization

    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

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
        return render(request, './aichat/aichat.html')




def profiles_list(request):
    user = request.user
    # Get the user's payment record if it exists
    subscription = UserPayment.objects.filter(username=user.username).first()
    
    subscription_status = "inactive"
    
    # Check if there is no payment or if the payment is inactive
    if subscription:
        # Check if the subscription is active and not expired
        if subscription.status == "active" and subscription.expires_at > now():
            subscription_status = "active"
    else:
        subscription_status = "no_payment"  # Added this case for no payment record

    profiles = Profile.objects.all()
    paginator = Paginator(profiles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, './aichat/profiles.html', {'page_obj': page_obj, 'subscription_status': subscription_status})

@login_required
def chat_with_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    # Fetch prompts from the profile
    profile_prompts = profile.prompts

    # Initialize the model with the profile's API model
    model = genai.GenerativeModel(profile.api_model)

    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        # Get the chat history from the session, or initialize if it doesn't exist
        chat_history = request.session.get(f'chat_history_{profile_id}', [])

        # Add the current user input to the history (limit to last user input and bot response)
        chat_history = [f"User: {user_input}"]

        try:
            # Combine the profile's prompts with the current user input to provide focused context
            prompt_with_context = f"{profile_prompts}\n" + "\n".join(chat_history) + "\nBot:"

            # Generate a response based on the current context
            response = model.generate_content(
                prompt_with_context,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                }
            )

            # Get the bot's response and add it to the history
            bot_response = response.text.strip()
            chat_history.append(f"Bot: {bot_response}")

            # Save the updated chat history to the session (only the latest user and bot messages)
            request.session[f'chat_history_{profile_id}'] = chat_history

            return JsonResponse({'user_input': user_input, 'response': bot_response})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, './aichat/chatwith.html', {'profile': profile})
