
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login as dj_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import SignupForm
from django.db.models import Q
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'User already exists.')
                return render(request, './join/signup.html', {'form': form})

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Log in the user
            user = authenticate(username=username, password=password)
            dj_login(request, user)

            return redirect('girls')  # Replace 'home' with your home page URL
    else:
        form = SignupForm()

    return render(request, './join/signup.html', {'form': form})

def login(request):
    page = 'login'

    # Check if the user is already logged in
    if request.user.is_authenticated:
        return redirect('girls')

    # Check if the user is coming from a page that needs login
    next_page = request.GET.get('next', 'girls')  # Default to 'home' if no next param exists

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            dj_login(request, user)
            # Redirect to the page user was trying to visit before login
            return redirect(next_page)

        else:
            messages.info(request, 'Invalid username or password')
            return redirect("login")

    return render(request, './join/login.html', {'next': next_page})




def custom_logout(request):
    logout(request)
    return redirect('girls')

