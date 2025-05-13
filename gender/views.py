from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.timezone import now, timedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserPayment,Escort ,BlogPost
from django.utils.timezone import now
from django.contrib import messages
from django.core.paginator import Paginator
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from django.shortcuts import render, get_object_or_404



def escorts(request):
    # Get the filter type from the query parameters (e.g., ?category=verified)
    category = request.GET.get('category', 'all')  # Default to 'all'

    # Fetch escorts based on the selected category
    if category == 'verified':
        escorts = Escort.objects.filter(verified=True).order_by('-premium')  # VIP escorts first
    elif category == 'new':
        escorts = Escort.objects.filter(is_new=True).order_by('-premium')  # VIP escorts first
    elif category == 'vip':
        escorts = Escort.objects.filter(premium=True)  # Only VIP escorts
    else:  # Default to all escorts
        escorts = Escort.objects.all().order_by('-premium')  # VIP escorts first

    # Paginate the results (12 items per page)
    paginator = Paginator(escorts, 12)
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    # Render the template with the filtered escorts and pagination
    return render(request, './gender/escorts.html', {
        'page_obj': page_obj,
        'category': category,  # Pass the current category to the template
    })

def escorts_by_city(request, city, sub_city=None):
    city = city.lower()
    escorts = Escort.objects.filter(city__iexact=city)

    if sub_city:
        sub_city_clean = sub_city.replace('-escorts', '').replace('-', ' ')
        escorts = escorts.filter(areas__name__icontains=sub_city_clean)

    paginator = Paginator(escorts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, './gender/escorts.html', {
        'page_obj': page_obj,
        'city': city,
        'sub_city': sub_city,
    })




def view_person(request, pk):
    escort = get_object_or_404(Escort.objects.prefetch_related('services'), pk=pk)  # Prefetch services for optimization
    return render(request, './gender/viewperson.html', {'escort': escort})


genai.configure(api_key="AIzaSyCIjgG29HPVa7_db5NMrQL5O4oBgW18S5o")  # Replace with your actual API key




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
    
    # Fetch the specific blog by title
    specific_blog_title = "Meet Verified Escorts in Uganda – flirtparadise Uganda Escorts"
    specific_blog = BlogPost.objects.filter(is_published=True, title=specific_blog_title).first()
    
    return render(request, './blog/blog.html', {'blogs': blogs, 'specific_blog': specific_blog})

def viewblog(request, blog_title):
    # Fetch a specific blog post by ID
    blog = get_object_or_404(BlogPost, slug=blog_title)
    return render(request, './blog/viewblog.html', {'blog': blog})
