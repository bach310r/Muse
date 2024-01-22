from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def user_login(request):
    if request.method == 'POST':
        # Get username and password from request
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            # User is authenticated, log them in and redirect to a new page
            print(user)
            login(request, user)
            return redirect('generator:generator')  # Redirect to a home page or dashboard
        else:
            # Invalid credentials, handle accordingly
            return render(request, 'user_log/login.html', {'error': 'Invalid username or password'})
    
    else:
        # If not a POST request, render the login template
        return render(request, 'user_log/login.html')



def signup(request):
    return render(request, "user_log/signup.html")