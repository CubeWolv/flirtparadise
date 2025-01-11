from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.timezone import now, timedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserPayment,Escort ,Girl, Guy, BlogPost
from django.utils.timezone import now
from django.contrib import messages
from django.core.paginator import Paginator
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from django.shortcuts import render, get_object_or_404

# Create your views here.

def escorts(request):
    # Fetch all escorts
    escorts = Escort.objects.all()
    paginator = Paginator(escorts, 12)  # Paginate with 12 items per page
    page_number = request.GET.get('page')  # Get current page number from query params
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page
    return render(request, './gender/escorts.html', {'page_obj': page_obj, 'city': None})

def escorts_by_city(request, city):
    # Filter escorts linked to the specific area
    escorts = Escort.objects.filter(areas__name__iexact=city)
    paginator = Paginator(escorts, 12)  # Paginate with 12 items per page
    page_number = request.GET.get('page')  # Get current page number from query params
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page
    return render(request, './gender/escorts.html', {'page_obj': page_obj, 'city': city})

    
def view_person(request, pk):
    escort = get_object_or_404(Escort.objects.prefetch_related('services'), pk=pk)  # Prefetch services for optimization
    return render(request, './gender/viewperson.html', {'escort': escort})


genai.configure(api_key="AIzaSyCIjgG29HPVa7_db5NMrQL5O4oBgW18S5o")  # Replace with your actual API key

@login_required
def chat_room(request, profile_id):
    girl = get_object_or_404(Girl, id=profile_id)  # Fetch the girl's profile

    # Initialize the Gemini AI model
    model = genai.GenerativeModel("tunedModels/flirt-paradise-luouxnlaxjx2")

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

    # Render the chat room for GET requests, passing the girl profile
    return render(request, './gender/chatwith.html', {'girl': girl})

    # Render the chat room for GET requests
    return render(request, './gender/chatwith.html', {'girl': girl})


@login_required
def chat_with_guy(request, profile_id):
    guy = get_object_or_404(Guy, id=profile_id)  # Fetch the guy's profile

    # Initialize the Gemini AI model (if you're using an AI)
    model = genai.GenerativeModel("tunedModels/flirt-paradise-luouxnlaxjx2")

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

    # Render the chat room for GET requests, passing the guy profile
    return render(request, 'gender/chatwithguy.html', {'guy': guy})


def guys(request):
    user = request.user  # Assuming the user is logged in

    # Check if the user has an active payment and if the subscription has not expired
    subscription = UserPayment.objects.filter(username=user.username).first()

    if subscription:
        # Check if the subscription is active and not expired
        if subscription.status == "active" and subscription.expires_at > now():
            subscription_status = "active"
        else:
            subscription_status = "expired"
    else:
        subscription_status = "inactive"
    
    # Render the page with the needs_payment flag
    guys = Guy.objects.all()
    paginator = Paginator(guys, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, './gender/guys.html', {'page_obj': page_obj, 'subscription_status': subscription_status})

def girls(request):
    user = request.user  # Assuming the user is logged in

    # Fetch the subscription status for the logged-in user
    subscription = UserPayment.objects.filter(username=user.username).first()

    if subscription:
        # Check if the subscription is active and not expired
        if subscription.status == "active" and subscription.expires_at > now():
            subscription_status = "active"
        else:
            subscription_status = "expired"
    else:
        subscription_status = "inactive"

    # Fetch all girls from the database
    girls_list = Girl.objects.all()

    # Implement pagination
    paginator = Paginator(girls_list, 12)  # Show 12 girls per page
    page_number = request.GET.get('page')  # Get the page number from the query parameters
    girls = paginator.get_page(page_number)  # Get the girls for the current page

    return render(request, './gender/girls.html', {'subscription_status': subscription_status, 'girls': girls})
@login_required
def flutterwave_payment(request):
    return render(request, 'payment.html')


from django.contrib.auth.decorators import login_required

@login_required
def verify_payment(request):
    tx_ref = request.GET.get('tx_ref')
    username = request.GET.get('username')

    if not tx_ref or not username:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    # Flutterwave verification endpoint
    url = f"https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={tx_ref}"
    headers = {
        "Authorization": f"Bearer YOUR_FLUTTERWAVE_SECRET_KEY",  # Replace with your secret key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success' and data['data']['status'] == 'successful':
            # Save payment in the database
            UserPayment.objects.create(
                username=username,
                tx_ref=tx_ref,
                amount=data['data']['amount'],
                expires_at=now() + timedelta(days=1)  # Set expiration for 24 hours
            )
            return redirect('/restricted-content')  # Redirect to restricted content
        else:
            return JsonResponse({'status': 'error', 'message': 'Payment not successful'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Verification failed'}, status=response.status_code)


def save_payment_data(request):
    if request.method == "POST":
        try:
            # Parse the JSON body to retrieve username and phone number
            data = json.loads(request.body)
            username = data.get('username')
            phone_number = data.get('phone_number')

            # Check if the user already has an active payment
            existing_payment = UserPayment.objects.filter(username=username, status="active").first()

            if not existing_payment:
                # Create a new payment record
                payment = UserPayment.objects.create(
                    username=username,
                    phone_number=phone_number,
                    payment_status="pending",
                    status="active",
                    expires_at=now() + timedelta(days=1)  # Set expiry to 24 hours
                )
                return JsonResponse({"status": "success", "message": "Payment data saved."})
            else:
                # If a payment already exists, just extend the expiry time
                existing_payment.expires_at = now() + timedelta(days=1)  # Extend expiry to 24 more hours
                existing_payment.save()
                return JsonResponse({"status": "success", "message": "Subscription extended."})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})



def blog(request):
    # Fetch all blog posts, ordered by publication date
    blogs = BlogPost.objects.filter(is_published=True).order_by('-published_at')
    return render(request, './blog/blog.html', {'blogs': blogs})

def viewblog(request, blog_title):
    # Fetch a specific blog post by ID
    blog = get_object_or_404(BlogPost, slug=blog_title)
    return render(request, './blog/viewblog.html', {'blog': blog})