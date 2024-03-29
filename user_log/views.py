from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user)
            login(request, user)
            return redirect('generator:generator') 
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('user_log:user_login') 


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    login(request, user)
                    return redirect('generator:generator') 

                else:
                    messages.error(request, 'Email is already registered.')
            else:
                messages.error(request, 'Username is already taken.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'signup.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
@require_POST
def delete_account(request):
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            password = request.POST.get('password')
            user = authenticate(username=request.user.username, password=password)
            
            if user is not None:
                user.delete()
                messages.success(request, 'Your account has been deleted.')
                return redirect('user_log:user_login')

            else:
                messages.error(request, 'Password is incorrect.')

    return render(request, 'profile.html')


@login_required
def update_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email:
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'Your email has been updated.')
            return redirect('user_log:profile') 
        else:
            messages.error(request, 'Please enter a valid email.')

    return render(request, 'profile.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly.')
            return redirect('user_log:profile')

        if new_password1 and new_password1 == new_password2:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_log:profile')
        else:
            messages.error(request, 'New passwords do not match.')

    return render(request, 'profile.html')